"""Tests for Markdown resume summaries."""

from pathlib import Path

from src.visualization.html_renderer import render_html
from src.visualization.md_renderer import _escape_md, render_markdown, write_markdown
from tests.test_visualization_html import _validated_model


def test_render_markdown_contains_expected_sections_and_resume_data() -> None:
    # Arrange
    model = _validated_model()

    # Act
    markdown = render_markdown(model)

    # Assert
    assert "## Datos personales" in markdown
    assert "## Contacto" in markdown
    assert "## Experiencia" in markdown
    assert "## Habilidades" in markdown
    assert "## Clasificación de perfiles" in markdown
    assert "Daniel Nastul" in markdown
    assert "daniel@example.com" in markdown
    assert "Backend Developer | Aceptado" in markdown


def test_escape_md_escapes_markdown_punctuation() -> None:
    # Arrange
    text = "*bold* _under_ [link] `code` #tag | <tag>"

    # Act
    escaped = _escape_md(text)

    # Assert
    assert escaped == r"\*bold\* \_under\_ \[link\] \`code\` \#tag \| \<tag\>"


def test_render_markdown_is_deterministic() -> None:
    # Arrange
    model = _validated_model()

    # Act
    first = render_markdown(model)
    second = render_markdown(model)

    # Assert
    assert first == second


def test_render_markdown_ends_with_newline() -> None:
    # Arrange
    model = _validated_model()

    # Act
    markdown = render_markdown(model)

    # Assert
    assert markdown.endswith("\n")


def test_write_markdown_creates_parent_directories_and_file(tmp_path: Path) -> None:
    # Arrange
    model = _validated_model()
    output_path = tmp_path / "nested" / "reports" / "resume.md"

    # Act
    result = write_markdown(model, output_path)

    # Assert
    assert result == output_path
    assert output_path.is_file()
    assert output_path.read_text(encoding="utf-8") == render_markdown(model)


def test_markdown_content_matches_html_report() -> None:
    # Arrange
    model = _validated_model()

    # Act
    markdown = render_markdown(model)
    html = render_html(model)

    # Assert
    for value in ("Daniel Nastul", "daniel@example.com", "Backend Developer", "Machine Learning Engineer"):
        assert value in markdown
        assert value in html
