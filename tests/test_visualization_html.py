"""Tests for HTML reports generated from validated DSL resumes."""

from html.parser import HTMLParser
from pathlib import Path

import pytest

from src.dsl.parser import DSLParser
from src.dsl.validators import validate_resume_model
from src.visualization.html_renderer import ReportRenderError, _render_view, render_html, write_html
from src.visualization.view_model import ContactView, ReportView
from tests.test_dsl import VALID_DSL_SAMPLE

_OPTIONAL_FIELDS_DSL = '''
CANDIDATE_PROFILE "Fictional Candidate"
TITLE: "Software Developer"
CONTACT
email= "candidate@example.test"
EXPERIENCE:
EDUCATION:
SKILLS: "PYTHON"
EVALUATIONS:
"Backend Developer" : ACCEPTED
'''


def _validated_model(source: str = VALID_DSL_SAMPLE) -> object:
    model = DSLParser().parse_string(source)
    assert validate_resume_model(model) is True
    return model


class _StructureCheckingParser(HTMLParser):
    """Check that report tags are properly nested, including void tags."""

    _VOID_TAGS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in self._VOID_TAGS:
            self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        assert self.stack, f"Unexpected closing tag: {tag}"
        assert self.stack.pop() == tag, f"Mismatched closing tag: {tag}"

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        return


def test_render_html_includes_candidate_contact_and_accepted_profiles() -> None:
    # Arrange
    model = _validated_model()

    # Act
    html = render_html(model)

    # Assert
    assert "Daniel Nastul" in html
    assert "daniel@example.com" in html
    assert "Backend Developer: Aceptado" in html
    assert "Machine Learning Engineer: Rechazado" in html


def test_render_html_shows_unavailable_for_absent_optional_fields() -> None:
    # Arrange
    model = _validated_model(_OPTIONAL_FIELDS_DSL)

    # Act
    html = render_html(model)

    # Assert
    assert html.count("No disponible") >= 3


def test_render_html_has_well_nested_html_structure() -> None:
    # Arrange
    model = _validated_model()
    parser = _StructureCheckingParser()

    # Act
    parser.feed(render_html(model))
    parser.close()

    # Assert
    assert parser.stack == []


def test_render_html_is_deterministic() -> None:
    # Arrange
    model = _validated_model()

    # Act
    first = render_html(model)
    second = render_html(model)

    # Assert
    assert first == second


def test_write_html_creates_parent_directories_and_file(tmp_path: Path) -> None:
    # Arrange
    model = _validated_model()
    output_path = tmp_path / "nested" / "reports" / "resume.html"

    # Act
    result = write_html(model, output_path)

    # Assert
    assert result == output_path
    assert output_path.is_file()
    assert output_path.read_text(encoding="utf-8") == render_html(model)


def test_render_view_escapes_untrusted_html_text() -> None:
    # Arrange
    view = ReportView(
        name="<script>alert('x')</script>",
        title="Developer",
        contact=ContactView("candidate@example.test", None, None, None),
        experiences=(),
        skills=(),
        profile_results=(),
    )

    # Act
    html = _render_view(view, None)

    # Assert
    assert "&lt;script&gt;" in html
    assert "<script>alert('x')</script>" not in html


def test_render_html_rejects_model_without_expected_structure() -> None:
    # Arrange
    invalid_model = object()

    # Act / Assert
    with pytest.raises(ReportRenderError):
        render_html(invalid_model)


def test_render_html_inlines_default_css() -> None:
    # Arrange
    model = _validated_model()

    # Act
    html = render_html(model)

    # Assert
    assert "<style>" in html
    assert "--color-heading" in html


def test_render_html_omits_default_css_when_disabled() -> None:
    # Arrange
    model = _validated_model()

    # Act
    html = render_html(model, include_default_css=False)

    # Assert
    assert "<style>" not in html
    assert "--color-heading" not in html


def test_render_html_prefers_explicit_inline_css() -> None:
    # Arrange
    model = _validated_model()
    custom_css = "body { color: navy; }"

    # Act
    html = render_html(model, inline_css=custom_css)

    # Assert
    assert custom_css in html
    assert "--color-heading" not in html
