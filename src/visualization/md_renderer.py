"""Render validated resume models as Markdown summaries."""

from pathlib import Path

from src.visualization.view_model import ReportView, build_report_view

_MARKDOWN_SPECIAL_CHARACTERS = frozenset("\\*_[]`#|<>")
_UNAVAILABLE = "No disponible"


def render_markdown(model: object) -> str:
    """Render a validated resume model as a deterministic Markdown summary."""
    return _render_view(build_report_view(model))


def write_markdown(model: object, output_path: Path) -> Path:
    """Render a Markdown summary and write it to ``output_path`` as UTF-8."""
    destination = Path(output_path)
    rendered = render_markdown(model)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="\n") as output_file:
        output_file.write(rendered)
    return destination


def _render_view(view: ReportView) -> str:
    """Format a presentation model in the same section order as the HTML report."""
    lines = [
        f"# {_escape_md(view.name)}",
        "",
        f"_{_escape_md(view.title)}_",
        "",
        "## Datos personales",
        "",
        f"- **Nombre:** {_escape_md(view.name)}",
        f"- **Perfil profesional:** {_escape_md(view.title)}",
        "",
        "## Contacto",
        "",
        f"- **Email:** {_escape_md(view.contact.email)}",
        f"- **Teléfono:** {_escape_md(view.contact.phone or _UNAVAILABLE)}",
        f"- **GitHub:** {_escape_md(view.contact.github or _UNAVAILABLE)}",
        f"- **LinkedIn:** {_escape_md(view.contact.linkedin or _UNAVAILABLE)}",
        "",
        "## Experiencia",
        "",
    ]
    if view.experiences:
        lines.extend(
            f"- {_escape_md(experience.position)} en {_escape_md(experience.company)} "
            f"({experience.years} años)"
            for experience in view.experiences
        )
    else:
        lines.append(f"- {_UNAVAILABLE}")
    lines.extend(("", "## Habilidades", ""))
    if view.skills:
        lines.extend(f"- {_escape_md(skill.name)}" for skill in view.skills)
    else:
        lines.append(f"- {_UNAVAILABLE}")
    lines.extend(("", "## Clasificación de perfiles", ""))
    if view.profile_results:
        lines.extend(("| Perfil | Estado |", "| --- | --- |"))
        lines.extend(
            f"| {_escape_md(result.profile)} | "
            f"{'Aceptado' if result.accepted else 'Rechazado'} |"
            for result in view.profile_results
        )
    else:
        lines.append(_UNAVAILABLE)
    return "\n".join(lines) + "\n"


def _escape_md(value: str) -> str:
    """Escape Markdown punctuation in untrusted text values."""
    return "".join(
        f"\\{character}" if character in _MARKDOWN_SPECIAL_CHARACTERS else character
        for character in value
    )
