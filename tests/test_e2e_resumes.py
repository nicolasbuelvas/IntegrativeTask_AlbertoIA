"""End-to-end checks for the synthetic plain-text resume dataset."""

import json
from dataclasses import dataclass
from pathlib import Path

import pytest
from pyformlang.finite_automaton import Symbol

from src.dsl.parser import DSLParser
from src.dsl.serializer import DSLSerializer
from src.dsl.validators import validate_resume_model
from src.extraction.contact_extractor import ContactExtractor
from src.extraction.skill_extractor import SkillExtractor
from src.main import run_pipeline
from src.models.profiles import ProfileType
from src.normalization.pipeline import NormalizationPipeline
from src.recognition.data_automata import DataAutomata
from src.recognition.software_automata import SoftwareAutomata
from src.visualization.html_renderer import render_html
from src.visualization.md_renderer import render_markdown

_RESUME_DIRECTORY = Path(__file__).resolve().parents[1] / "data" / "resumes"


@dataclass(frozen=True)
class ResumeCase:
    """Expected target-profile outcome for one synthetic resume."""

    filename: str
    expected_accepted: tuple[ProfileType, ...]
    expected_not_accepted: tuple[ProfileType, ...]


EXPECTATIONS = (
    ResumeCase(
        "fullstack_valid.txt",
        (ProfileType.FULL_STACK_DEVELOPER,),
        (),
    ),
    ResumeCase(
        "fullstack_invalid.txt",
        (),
        (ProfileType.FULL_STACK_DEVELOPER,),
    ),
    ResumeCase(
        "backend_sample.txt",
        (ProfileType.BACKEND_DEVELOPER,),
        (),
    ),
    ResumeCase(
        "ml_engineer_valid.txt",
        (ProfileType.MACHINE_LEARNING_ENGINEER,),
        (),
    ),
    ResumeCase(
        "ml_engineer_invalid.txt",
        (),
        (ProfileType.MACHINE_LEARNING_ENGINEER,),
    ),
    ResumeCase(
        "data_engineer_sample.txt",
        (ProfileType.DATA_ENGINEER,),
        (),
    ),
)


@dataclass(frozen=True)
class _ResumeResult:
    """Artifacts produced by the available extraction and DSL stages."""

    source_text: str
    name: str
    email: str
    accepted_profiles: tuple[ProfileType, ...]
    dsl: str


def _case_id(case: ResumeCase) -> str:
    """Return a readable parametrized-test identifier."""
    return Path(case.filename).stem


def _quote_dsl_string(value: str) -> str:
    """Quote one string using the DSL's double-quoted string syntax."""
    return json.dumps(value, ensure_ascii=False)


def _accepts_profile(
    profile: ProfileType,
    skills: tuple[str, ...],
    normalizer: NormalizationPipeline,
    software_automata: SoftwareAutomata,
    data_automata: DataAutomata,
) -> bool:
    """Run the real recognizer for one profile on its canonical skill sequence."""
    sequence = normalizer.sort_for_profile(skills, profile)
    symbols = [Symbol(skill) for skill in sequence]
    if profile is ProfileType.FULL_STACK_DEVELOPER:
        return software_automata.fullstack_dfa.accepts(symbols)
    if profile is ProfileType.BACKEND_DEVELOPER:
        return software_automata.backend_dfa.accepts(symbols)
    if profile is ProfileType.MACHINE_LEARNING_ENGINEER:
        return data_automata.ml_dfa.accepts(symbols)
    if profile is ProfileType.DATA_ENGINEER:
        return data_automata.data_dfa.accepts(symbols)
    raise ValueError(f"Unsupported profile: {profile!r}")


def _build_dsl(
    name: str,
    title: str,
    email: str,
    phone: str | None,
    github: str | None,
    linkedin: str | None,
    skills: tuple[str, ...],
    accepted_profiles: tuple[ProfileType, ...],
) -> str:
    """Build DSL input because no plain-text resume-to-DSL API exists yet."""
    lines = [
        f"CANDIDATE_PROFILE {_quote_dsl_string(name)}",
        f"TITLE: {_quote_dsl_string(title)}",
        "CONTACT",
        f"email= {_quote_dsl_string(email)}",
    ]
    if phone:
        lines.append(f"phone= {_quote_dsl_string(phone)}")
    if github:
        lines.append(f"github= {_quote_dsl_string(github)}")
    if linkedin:
        lines.append(f"linkedin= {_quote_dsl_string(linkedin)}")
    lines.extend(("EXPERIENCE:", "EDUCATION:"))
    lines.append("SKILLS: " + ", ".join(_quote_dsl_string(skill) for skill in skills))
    lines.append("EVALUATIONS:")
    lines.extend(
        f"{_quote_dsl_string(profile.value)} : "
        f"{'ACCEPTED' if profile in accepted_profiles else 'REJECTED'}"
        for profile in ProfileType
    )
    return "\n".join(lines)


def _process_resume(case: ResumeCase) -> _ResumeResult:
    """Connect existing extraction, normalization, recognition, and DSL APIs."""
    source_path = _RESUME_DIRECTORY / case.filename
    source_text = source_path.read_text(encoding="utf-8")
    contact = ContactExtractor.extract(source_text)
    if contact.name is None or contact.email is None:
        raise ValueError(f"Resume is missing a required name or email: {case.filename}")

    lines = source_text.splitlines()
    if len(lines) < 2:
        raise ValueError(f"Resume is missing a title: {case.filename}")
    title = lines[1].strip()
    raw_skills = SkillExtractor.extract_unique_skills(source_text)
    normalizer = NormalizationPipeline()
    skills = tuple(normalizer.process_raw_skills(raw_skills))
    software_automata = SoftwareAutomata()
    data_automata = DataAutomata()
    accepted_profiles = tuple(
        profile
        for profile in ProfileType
        if _accepts_profile(
            profile,
            skills,
            normalizer,
            software_automata,
            data_automata,
        )
    )
    dsl_input = _build_dsl(
        contact.name,
        title,
        contact.email,
        contact.phone,
        contact.github,
        contact.linkedin,
        skills,
        accepted_profiles,
    )
    return _ResumeResult(
        source_text=source_text,
        name=contact.name,
        email=contact.email,
        accepted_profiles=accepted_profiles,
        dsl=run_pipeline(dsl_input),
    )


@pytest.mark.parametrize("case", EXPECTATIONS, ids=_case_id)
def test_e2e_resume_components_process_file_without_exception(case: ResumeCase) -> None:
    # Arrange / Act
    result = _process_resume(case)

    # Assert
    assert result.dsl


@pytest.mark.parametrize("case", EXPECTATIONS, ids=_case_id)
def test_e2e_resume_profiles_match_dataset_intent(case: ResumeCase) -> None:
    # Arrange
    result = _process_resume(case)

    # Act / Assert
    for profile in case.expected_accepted:
        assert profile in result.accepted_profiles
    for profile in case.expected_not_accepted:
        assert profile not in result.accepted_profiles


@pytest.mark.parametrize("case", EXPECTATIONS, ids=_case_id)
def test_e2e_resume_dsl_round_trip_parses_and_validates(case: ResumeCase) -> None:
    # Arrange
    result = _process_resume(case)

    # Act
    model = DSLParser().parse_string(result.dsl)

    # Assert
    assert validate_resume_model(model) is True
    assert DSLSerializer.serialize_to_dsl(model) == result.dsl


@pytest.mark.parametrize("case", EXPECTATIONS, ids=_case_id)
def test_e2e_resume_email_matches_source(case: ResumeCase) -> None:
    # Arrange
    result = _process_resume(case)

    # Act
    email = ContactExtractor.extract_email(result.source_text)

    # Assert
    assert result.email == email


@pytest.mark.parametrize("case", EXPECTATIONS, ids=_case_id)
def test_e2e_resume_dsl_output_is_deterministic(case: ResumeCase) -> None:
    # Arrange / Act
    first = _process_resume(case).dsl
    second = _process_resume(case).dsl

    # Assert
    assert first == second


@pytest.mark.parametrize("case", EXPECTATIONS, ids=_case_id)
def test_e2e_resume_visualizations_include_candidate_name(case: ResumeCase) -> None:
    # Arrange
    result = _process_resume(case)
    model = DSLParser().parse_string(result.dsl)

    # Act
    html = render_html(model)
    markdown = render_markdown(model)

    # Assert
    assert result.name in html
    assert result.name in markdown


def test_e2e_resume_expectations_cover_every_dataset_file() -> None:
    # Arrange
    expected_filenames = {case.filename for case in EXPECTATIONS}

    # Act
    dataset_filenames = {path.name for path in _RESUME_DIRECTORY.glob("*.txt")}

    # Assert
    assert dataset_filenames == expected_filenames
