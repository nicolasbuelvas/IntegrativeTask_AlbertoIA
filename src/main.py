"""CLI and main entrypoint for the ResumeLens resume screening system."""

import argparse
from pathlib import Path
import sys
from typing import Optional

from src.dsl.parser import DSLParser
from src.dsl.serializer import DSLSerializer
from src.dsl.validators import DSLValidationError, validate_resume_model
from src.pipeline import ResumeAnalysisResult, ResumeLensPipeline


def run_pipeline(dsl_text_content: str) -> str:
    """Parse, validate, and serialize a DSL resume model string."""
    parser = DSLParser()
    model = parser.parse_string(dsl_text_content)
    validate_resume_model(model)
    return DSLSerializer.serialize_to_dsl(model)


def print_summary(result: ResumeAnalysisResult) -> None:
    """Print candidate analysis report to stdout."""
    print("=" * 60)
    print(f"CANDIDATE: {result.name}")
    print(f"TITLE:     {result.title}")
    print(f"EMAIL:     {result.email}")
    if result.contact.phone:
        print(f"PHONE:     {result.contact.phone}")
    if result.contact.linkedin:
        print(f"LINKEDIN:  {result.contact.linkedin}")
    if result.contact.github:
        print(f"GITHUB:    {result.contact.github}")
    print("-" * 60)
    print(f"RAW SKILLS EXTRACTED ({len(result.raw_skills)}):")
    print("  " + (", ".join(result.raw_skills) if result.raw_skills else "None"))
    print(f"NORMALIZED CANONICAL SKILLS ({len(result.canonical_skills)}):")
    print("  " + (", ".join(result.canonical_skills) if result.canonical_skills else "None"))
    print("-" * 60)
    print("PROFILE EVALUATIONS (FINITE AUTOMATA):")
    for profile, accepted in result.evaluations.items():
        status = "[ACCEPTED]" if accepted else "[REJECTED]"
        print(f"  {profile.value:<30} {status}")
    print("=" * 60)


def run_demo(pipeline: ResumeLensPipeline, resumes_dir: Path) -> None:
    """Run screening on all synthetic resumes and display summary table."""
    print("Running ResumeLens evaluation across dataset:")
    print(f"{'RESUME FILE':<30} {'CANDIDATE':<22} {'ACCEPTED PROFILES'}")
    print("-" * 80)
    for txt_file in sorted(resumes_dir.glob("*.txt")):
        try:
            res = pipeline.process_file(txt_file)
            accepted = ", ".join(p.value for p in res.accepted_profiles) or "None"
            print(f"{txt_file.name:<30} {res.name:<22} {accepted}")
        except Exception as err:
            print(f"{txt_file.name:<30} ERROR: {err}")
    print("-" * 80)


def build_arg_parser() -> argparse.ArgumentParser:
    """Configure CLI command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="ResumeLens: Formal Language-Based Resume Screening System"
    )
    parser.add_argument(
        "resume_path",
        nargs="?",
        default=None,
        help="Path to candidate resume plain-text file (.txt)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["summary", "dsl", "html", "markdown", "all"],
        default="summary",
        help="Output format (default: summary)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        help="Destination file path for generated output (HTML, Markdown, or DSL)",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run batch screening demo across all sample resumes in data/resumes/",
    )
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    default_sample = project_root / "data" / "resumes" / "fullstack_valid.txt"
    resumes_dir = project_root / "data" / "resumes"

    pipeline = ResumeLensPipeline()

    if args.demo:
        run_demo(pipeline, resumes_dir)
        return

    target_file = Path(args.resume_path) if args.resume_path else default_sample

    if not target_file.is_file():
        print(f"Error: Resume file '{target_file}' not found.", file=sys.stderr)
        sys.exit(1)

    try:
        result = pipeline.process_file(target_file)
    except Exception as exc:
        print(f"Error processing resume '{target_file}': {exc}", file=sys.stderr)
        sys.exit(1)

    out_path = Path(args.output) if args.output else None

    if args.format == "summary":
        print_summary(result)
        if out_path:
            out_path.write_text(result.dsl_text, encoding="utf-8")
            print(f"Saved DSL output to: {out_path}")
    elif args.format == "dsl":
        if out_path:
            out_path.write_text(result.dsl_text, encoding="utf-8")
            print(f"Wrote DSL to {out_path}")
        else:
            print(result.dsl_text)
    elif args.format == "html":
        html_content = result.render_html_report(out_path)
        if out_path:
            print(f"Wrote HTML report to {out_path}")
        else:
            print(html_content)
    elif args.format == "markdown":
        md_content = result.render_markdown_report(out_path)
        if out_path:
            print(f"Wrote Markdown summary to {out_path}")
        else:
            print(md_content)
    elif args.format == "all":
        print_summary(result)
        prefix = out_path.stem if out_path else target_file.stem
        parent = out_path.parent if out_path else target_file.parent
        html_dest = parent / f"{prefix}_report.html"
        md_dest = parent / f"{prefix}_summary.md"
        dsl_dest = parent / f"{prefix}.dsl"
        result.render_html_report(html_dest)
        result.render_markdown_report(md_dest)
        dsl_dest.write_text(result.dsl_text, encoding="utf-8")
        print(f"Generated artifacts:\n - {html_dest}\n - {md_dest}\n - {dsl_dest}")


if __name__ == "__main__":
    main()