"""End-to-end ResumeLens screening pipeline integrating Stages 1 to 5."""

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from pyformlang.finite_automaton import Symbol

from src.dsl.parser import DSLParser
from src.dsl.serializer import DSLSerializer
from src.dsl.validators import validate_resume_model
from src.extraction.contact_extractor import ContactExtractor, ContactInfo
from src.extraction.skill_extractor import SkillExtractor
from src.models.profiles import ProfileType
from src.normalization.pipeline import NormalizationPipeline
from src.recognition.data_automata import DataAutomata
from src.recognition.software_automata import SoftwareAutomata
from src.visualization.html_renderer import render_html, write_html
from src.visualization.md_renderer import render_markdown, write_markdown


def quote_dsl_string(value: str) -> str:
    """Quote a string according to DSL double-quoted string syntax."""
    return json.dumps(value, ensure_ascii=False)


@dataclass(frozen=True)
class ResumeAnalysisResult:
    """Complete analysis artifact produced by the ResumeLens pipeline."""

    source_text: str
    contact: ContactInfo
    title: str
    raw_skills: Tuple[str, ...]
    canonical_skills: Tuple[str, ...]
    evaluations: Dict[ProfileType, bool]
    accepted_profiles: Tuple[ProfileType, ...]
    dsl_text: str
    dsl_model: object

    @property
    def name(self) -> str:
        return self.contact.name or "Unknown Candidate"

    @property
    def email(self) -> str:
        return self.contact.email or ""

    def render_html_report(self, output_path: Optional[Path | str] = None) -> str:
        """Render the HTML visualization, optionally saving to disk."""
        content = render_html(self.dsl_model)
        if output_path is not None:
            write_html(self.dsl_model, Path(output_path))
        return content

    def render_markdown_report(self, output_path: Optional[Path | str] = None) -> str:
        """Render the Markdown summary, optionally saving to disk."""
        content = render_markdown(self.dsl_model)
        if output_path is not None:
            write_markdown(self.dsl_model, Path(output_path))
        return content


class ResumeLensPipeline:
    """Coordinates information extraction, FST normalization, automata recognition, DSL, and reporting."""

    def __init__(
        self,
        normalizer: Optional[NormalizationPipeline] = None,
        software_automata: Optional[SoftwareAutomata] = None,
        data_automata: Optional[DataAutomata] = None,
        parser: Optional[DSLParser] = None,
    ) -> None:
        self.normalizer = normalizer if normalizer is not None else NormalizationPipeline()
        self.software_automata = software_automata if software_automata is not None else SoftwareAutomata()
        self.data_automata = data_automata if data_automata is not None else DataAutomata()
        self.parser = parser if parser is not None else DSLParser()

    def evaluate_profile(self, profile: ProfileType, canonical_skills: Tuple[str, ...]) -> bool:
        """Evaluate whether canonical skills satisfy the pattern automaton for a profile."""
        sequence = self.normalizer.sort_for_profile(canonical_skills, profile)
        symbols = [Symbol(skill) for skill in sequence]

        if profile is ProfileType.FULL_STACK_DEVELOPER:
            return self.software_automata.fullstack_dfa.accepts(symbols)
        if profile is ProfileType.BACKEND_DEVELOPER:
            return self.software_automata.backend_dfa.accepts(symbols)
        if profile is ProfileType.MACHINE_LEARNING_ENGINEER:
            return self.data_automata.ml_dfa.accepts(symbols)
        if profile is ProfileType.DATA_ENGINEER:
            return self.data_automata.data_dfa.accepts(symbols)

        raise ValueError(f"Unsupported profile type: {profile!r}")

    def generate_dsl(
        self,
        contact: ContactInfo,
        title: str,
        canonical_skills: Tuple[str, ...],
        evaluations: Dict[ProfileType, bool],
    ) -> str:
        """Construct valid DSL text from extracted entities and evaluation states."""
        name = contact.name or "Candidate"
        email = contact.email or "candidate@example.com"

        lines = [
            f"CANDIDATE_PROFILE {quote_dsl_string(name)}",
            f"TITLE: {quote_dsl_string(title)}",
            "CONTACT",
            f"email= {quote_dsl_string(email)}",
        ]
        if contact.phone:
            lines.append(f"phone= {quote_dsl_string(contact.phone)}")
        if contact.github:
            lines.append(f"github= {quote_dsl_string(contact.github)}")
        if contact.linkedin:
            lines.append(f"linkedin= {quote_dsl_string(contact.linkedin)}")

        lines.extend(("EXPERIENCE:", "EDUCATION:"))
        lines.append("SKILLS: " + ", ".join(quote_dsl_string(skill) for skill in canonical_skills))
        lines.append("EVALUATIONS:")
        lines.extend(
            f"{quote_dsl_string(profile.value)} : "
            f"{'ACCEPTED' if is_accepted else 'REJECTED'}"
            for profile, is_accepted in evaluations.items()
        )
        return "\n".join(lines)

    def process_text(self, text: str, default_title: Optional[str] = None) -> ResumeAnalysisResult:
        """Run the complete 5-stage screening pipeline on raw resume text."""
        # Stage 1: Regular Expression Information Extraction
        contact = ContactExtractor.extract(text)
        if not contact.name or not contact.email:
            raise ValueError("Resume missing required candidate name or email contact information.")

        lines = [line.strip() for line in text.splitlines() if line.strip()]
        title = default_title or (lines[1] if len(lines) > 1 else "Software Professional")

        raw_skills = tuple(SkillExtractor.extract_unique_skills(text))

        # Stage 2: Qualification Normalization via FST
        canonical_skills = tuple(self.normalizer.process_raw_skills(raw_skills))

        # Stage 3: Qualification Pattern Recognition via Automata
        evaluations: Dict[ProfileType, bool] = {}
        accepted_list: List[ProfileType] = []
        for profile in ProfileType:
            is_accepted = self.evaluate_profile(profile, canonical_skills)
            evaluations[profile] = is_accepted
            if is_accepted:
                accepted_list.append(profile)

        # Stage 4: DSL Specification, Validation and AST Generation
        dsl_source = self.generate_dsl(contact, title, canonical_skills, evaluations)
        dsl_model = self.parser.parse_string(dsl_source)
        validate_resume_model(dsl_model)
        validated_dsl = DSLSerializer.serialize_to_dsl(dsl_model)

        return ResumeAnalysisResult(
            source_text=text,
            contact=contact,
            title=title,
            raw_skills=raw_skills,
            canonical_skills=canonical_skills,
            evaluations=evaluations,
            accepted_profiles=tuple(accepted_list),
            dsl_text=validated_dsl,
            dsl_model=dsl_model,
        )

    def process_file(self, file_path: Path | str) -> ResumeAnalysisResult:
        """Read a resume file from disk and execute the screening pipeline."""
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Resume file not found: {path}")
        text = path.read_text(encoding="utf-8")
        return self.process_text(text)
