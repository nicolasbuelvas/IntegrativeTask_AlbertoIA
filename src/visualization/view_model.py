"""Immutable presentation models for HTML resume reports."""

from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlsplit

from src.dsl.validators import validate_resume_model

_ACCEPTED = "ACCEPTED"
_REJECTED = "REJECTED"


@dataclass(frozen=True)
class ContactView:
    """Contact details prepared for display."""

    email: str
    phone: Optional[str]
    github: Optional[str]
    linkedin: Optional[str]
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None


@dataclass(frozen=True)
class ExperienceView:
    """A work experience item prepared for display."""

    position: str
    company: str
    years: int


@dataclass(frozen=True)
class SkillView:
    """A skill label prepared for display."""

    name: str


@dataclass(frozen=True)
class ProfileResultView:
    """A profile evaluation prepared for display."""

    profile: str
    accepted: bool


@dataclass(frozen=True)
class ReportView:
    """All resume data required by the report template."""

    name: str
    title: str
    contact: ContactView
    experiences: tuple[ExperienceView, ...]
    skills: tuple[SkillView, ...]
    profile_results: tuple[ProfileResultView, ...]


def build_report_view(model: object) -> ReportView:
    """Validate and convert a textX resume model to presentation data."""
    try:
        validate_resume_model(model)
        name = _required_text(model.name, "name")
        title = _required_text(model.title, "title")
        contact_model = model.contact
        github = _optional_text(contact_model, "github")
        linkedin = _optional_text(contact_model, "linkedin")
        contact = ContactView(
            email=_required_text(contact_model.email, "contact.email"),
            phone=_optional_text(contact_model, "phone"),
            github=github,
            linkedin=linkedin,
            github_url=_safe_external_url(github),
            linkedin_url=_safe_external_url(linkedin),
        )
        experiences = tuple(
            ExperienceView(
                position=_required_text(item.position, "experience.position"),
                company=_required_text(item.company, "experience.company"),
                years=_required_years(item.years),
            )
            for item in _required_sequence(model.experiences, "experiences")
        )
        skills = tuple(
            SkillView(_required_text(skill, "skill"))
            for skill in _required_sequence(model.skills, "skills")
        )
        profile_results = tuple(
            _profile_result(item)
            for item in _required_sequence(model.evaluations, "evaluations")
        )
        return ReportView(
            name=name,
            title=title,
            contact=contact,
            experiences=experiences,
            skills=skills,
            profile_results=profile_results,
        )
    except Exception as exc:
        if isinstance(exc, ReportModelStructureError):
            raise
        raise ReportModelStructureError("The resume model has an unexpected structure.") from exc


class ReportModelStructureError(ValueError):
    """Raised when a resume model cannot be converted for presentation."""


def _required_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReportModelStructureError(f"Expected non-empty text for {field_name}.")
    return value


def _optional_text(model: object, field_name: str) -> Optional[str]:
    value = getattr(model, field_name, None)
    if value is None or value == "":
        return None
    if not isinstance(value, str):
        raise ReportModelStructureError(f"Expected text for contact.{field_name}.")
    return value


def _required_sequence(value: object, field_name: str) -> tuple[object, ...]:
    if not isinstance(value, (list, tuple)):
        raise ReportModelStructureError(f"Expected a sequence for {field_name}.")
    return tuple(value)


def _safe_external_url(value: Optional[str]) -> Optional[str]:
    """Return only absolute HTTP(S) URLs for use in link destinations."""
    if value is None:
        return None
    try:
        parsed_url = urlsplit(value)
    except ValueError:
        return None
    if parsed_url.scheme.lower() not in {"http", "https"} or not parsed_url.hostname:
        return None
    return value


def _required_years(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ReportModelStructureError("Expected an integer for experience.years.")
    return value


def _profile_result(item: object) -> ProfileResultView:
    profile = _required_text(item.profile, "evaluation.profile")
    status = item.status
    if status not in (_ACCEPTED, _REJECTED):
        raise ReportModelStructureError("Expected ACCEPTED or REJECTED evaluation status.")
    return ProfileResultView(profile=profile, accepted=status == _ACCEPTED)
