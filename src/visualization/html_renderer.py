"""Render validated resume models as safe HTML reports."""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined, TemplateError

from src.visualization.view_model import ReportModelStructureError, ReportView, build_report_view

_TEMPLATE_DIRECTORY = Path(__file__).parent / "templates"
_TEMPLATE_NAME = "report.html"
_STYLE_PATH = _TEMPLATE_DIRECTORY / "style.css"


class ReportRenderError(ValueError):
    """Raised when a resume model cannot be rendered as an HTML report."""


def render_html(
    model: object,
    *,
    inline_css: str | None = None,
    include_default_css: bool = True,
) -> str:
    """Validate and render a textX resume model to an HTML document."""
    try:
        view = build_report_view(model)
        css = inline_css
        if css is None and include_default_css:
            css = _STYLE_PATH.read_text(encoding="utf-8")
        return _render_view(view, css)
    except ReportRenderError:
        raise
    except (ReportModelStructureError, TemplateError, OSError, TypeError) as exc:
        raise ReportRenderError("Unable to render the resume model.") from exc


def write_html(model: object, output_path: Path) -> Path:
    """Render a resume report and write it to ``output_path`` as UTF-8."""
    destination = Path(output_path)
    rendered = render_html(model)
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", encoding="utf-8", newline="\n") as output_file:
            output_file.write(rendered)
    except OSError as exc:
        raise ReportRenderError(f"Unable to write HTML report to {destination}.") from exc
    return destination


def _render_view(view: ReportView, inline_css: str | None) -> str:
    """Render an already prepared view model with autoescaped template data."""
    if not isinstance(view, ReportView):
        raise ReportRenderError("Expected a ReportView instance.")
    environment = Environment(
        loader=FileSystemLoader(str(_TEMPLATE_DIRECTORY)),
        autoescape=True,
        undefined=StrictUndefined,
    )
    try:
        template = environment.get_template(_TEMPLATE_NAME)
        return template.render(view=view, inline_css=inline_css)
    except TemplateError as exc:
        raise ReportRenderError("Unable to render the resume view.") from exc
