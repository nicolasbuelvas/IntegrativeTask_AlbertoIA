"""Unit tests for Stage 1: Regular expression extraction of contact details and technical skills."""

import pytest

from src.extraction.contact_extractor import ContactExtractor, ContactInfo
from src.extraction.skill_extractor import SkillExtractor


SAMPLE_FULLSTACK_RESUME = """
John Doe
Software Engineer
Email: john.doe@example.com
Phone: +1 (555) 123-4567
LinkedIn: linkedin.com/in/johndoe-dev
GitHub: github.com/johndoe
Portfolio: https://johndoe.io

Summary:
Full Stack Developer with 5+ years of experience building web applications.

Technical Skills:
JavaScript, TypeScript, React.js, Node.js, Express, Docker, PostgreSQL, Git
"""

SAMPLE_AI_RESUME = """
Candidate: Jane Smith
jane.smith@datascience.org | +57 300 123 4567
https://linkedin.com/in/janesmith-ai | https://github.com/janesmith
https://janesmith.tech

Profile:
Machine Learning Engineer with 3.5 years of professional experience in deep learning.

Core Competencies:
Python, PyTorch, TensorFlow, Scikit-Learn, Pandas, NumPy, SQL, Docker, Git
"""


class TestContactExtractor:
    """Tests for contact information and metadata regex extraction."""

    def test_extract_explicit_name(self):
        text = "Candidate: Alice Montgomery\nEmail: alice@test.com"
        assert ContactExtractor.extract_name(text) == "Alice Montgomery"

    def test_extract_inferred_name_header(self):
        text = "Bob Charlie Vance\nSenior Engineer\nEmail: bob@test.com"
        assert ContactExtractor.extract_name(text) == "Bob Charlie Vance"

    def test_extract_email_valid(self):
        text = "Contact me at dev.engineer_01@company.co.uk please."
        assert ContactExtractor.extract_email(text) == "dev.engineer_01@company.co.uk"

    def test_extract_phone_various_formats(self):
        cases = [
            ("+1 (555) 123-4567", "+1 (555) 123-4567"),
            ("+57 300 123 4567", "+57 300 123 4567"),
            ("Phone: 312-456-7890", "312-456-7890"),
        ]
        for raw, expected in cases:
            extracted = ContactExtractor.extract_phone(raw)
            assert extracted is not None
            assert expected in extracted

    def test_extract_linkedin_url_and_handle(self):
        text = "LinkedIn: https://www.linkedin.com/in/octocat-profile/"
        assert ContactExtractor.extract_linkedin(text) == "https://linkedin.com/in/octocat-profile"

    def test_extract_github_url_and_handle(self):
        text = "Check repos: github.com/octocat"
        assert ContactExtractor.extract_github(text) == "https://github.com/octocat"

    def test_extract_portfolio_excluding_socials(self):
        text = "Portfolio: https://myportfolio.dev/projects and github.com/octocat"
        assert ContactExtractor.extract_portfolio(text) == "https://myportfolio.dev/projects"

    def test_extract_years_of_experience(self):
        text = "Senior developer with 7+ years of experience in distributed systems."
        assert ContactExtractor.extract_years_of_experience(text) == 7.0

        fractional = "With 2.5 yrs of professional experience in data analysis."
        assert ContactExtractor.extract_years_of_experience(fractional) == 2.5

    def test_extract_contact_info_dataclass(self):
        info = ContactExtractor.extract(SAMPLE_FULLSTACK_RESUME)
        assert isinstance(info, ContactInfo)
        assert info.name == "John Doe"
        assert info.email == "john.doe@example.com"
        assert info.linkedin == "https://linkedin.com/in/johndoe-dev"
        assert info.github == "https://github.com/johndoe"
        assert info.years_of_experience == 5.0


class TestSkillExtractor:
    """Tests for technical skill entity regex extraction."""

    def test_extract_skills_section(self):
        section = SkillExtractor.extract_skills_section(SAMPLE_FULLSTACK_RESUME)
        assert section is not None
        assert "JavaScript" in section
        assert "PostgreSQL" in section

    def test_extract_raw_skills_order(self):
        text = "Hands-on with React, Docker, and Python in production."
        raw_skills = SkillExtractor.extract_raw_skills(text)
        assert raw_skills == ["React", "Docker", "Python"]

    def test_extract_unique_skills_preserves_first_seen(self):
        text = "Proficient in Python, React, python, and REACT."
        unique = SkillExtractor.extract_unique_skills(text)
        assert len(unique) == 2
        assert unique[0].lower() == "python"
        assert unique[1].lower() == "react"

    def test_lexical_variations_detection(self):
        variations = [
            ("Experienced in JS and TS", ["JS", "TS"]),
            ("Built with React.js and Node.js", ["React.js", "Node.js"]),
            ("Deploying on Spring Boot and FastAPI", ["Spring Boot", "FastAPI"]),
            ("Databases: Postgres, MySQL, MongoDB", ["Postgres", "MySQL", "MongoDB"]),
            ("AI Stack: PyTorch, scikit-learn, TensorFlow", ["PyTorch", "scikit-learn", "TensorFlow"]),
            ("Big Data: Apache Spark, Hadoop, Airflow", ["Spark", "Hadoop", "Airflow"]),
        ]
        for snippet, expected_matches in variations:
            extracted = SkillExtractor.extract_raw_skills(snippet)
            for expected in expected_matches:
                assert any(expected.lower() in token.lower() for token in extracted), (
                    f"Expected '{expected}' in '{snippet}', got {extracted}"
                )

    def test_no_false_positives_boundary_checks(self):
        # "Java" must not trigger on "JavaScript" twice
        text = "JavaScript is great, Java is also great"
        skills = SkillExtractor.extract_raw_skills(text)
        assert "JavaScript" in skills
        assert "Java" in skills

        # "Git" must not trigger inside "GitHub"
        text_git = "GitHub repository link with Git cli"
        skills_git = SkillExtractor.extract_raw_skills(text_git)
        assert skills_git == ["Git"]

    def test_sample_ai_resume_extraction(self):
        skills = SkillExtractor.extract_unique_skills(SAMPLE_AI_RESUME)
        expected_subset = {"Python", "PyTorch", "TensorFlow", "Pandas", "NumPy", "Docker", "Git"}
        lower_extracted = {s.lower() for s in skills}
        for exp in expected_subset:
            assert exp.lower() in lower_extracted, f"Missing {exp} in extracted AI skills: {skills}"
