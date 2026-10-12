"""Unit tests for the centralized ResumeLens end-to-end pipeline."""

from pathlib import Path
import pytest

from src.models.profiles import ProfileType
from src.pipeline import ResumeLensPipeline


_RESUME_DIR = Path(__file__).resolve().parents[1] / "data" / "resumes"


def test_pipeline_processes_valid_fullstack_resume() -> None:
    pipeline = ResumeLensPipeline()
    resume_file = _RESUME_DIR / "fullstack_valid.txt"
    result = pipeline.process_file(resume_file)

    assert result.name == "Lina Marquez"
    assert result.email == "lina.marquez@example.com"
    assert ProfileType.FULL_STACK_DEVELOPER in result.accepted_profiles
    assert ProfileType.MACHINE_LEARNING_ENGINEER not in result.accepted_profiles
    assert len(result.canonical_skills) > 0
    assert "CANDIDATE_PROFILE" in result.dsl_text


def test_pipeline_renders_html_and_markdown(tmp_path: Path) -> None:
    pipeline = ResumeLensPipeline()
    resume_file = _RESUME_DIR / "backend_sample.txt"
    result = pipeline.process_file(resume_file)

    html_path = tmp_path / "report.html"
    md_path = tmp_path / "summary.md"

    html_content = result.render_html_report(html_path)
    md_content = result.render_markdown_report(md_path)

    assert html_path.is_file()
    assert md_path.is_file()
    assert result.name in html_content
    assert result.name in md_content


def test_pipeline_raises_on_nonexistent_file() -> None:
    pipeline = ResumeLensPipeline()
    with pytest.raises(FileNotFoundError):
        pipeline.process_file("nonexistent_resume_file.txt")


def test_pipeline_raises_on_invalid_text() -> None:
    pipeline = ResumeLensPipeline()
    with pytest.raises(ValueError, match="missing required candidate name or email"):
        pipeline.process_text("Just some text without name or email")
