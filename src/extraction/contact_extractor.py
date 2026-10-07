"""Contact information and candidate metadata extraction using regular expressions."""

from dataclasses import dataclass
from typing import Optional
import re

from src.extraction.regex_patterns import (
    EMAIL_PATTERN,
    EXPLICIT_NAME_PATTERN,
    EXPERIENCE_SUMMARY_PATTERN,
    EXPERIENCE_YEARS_PATTERN,
    GITHUB_PATTERN,
    LINKEDIN_PATTERN,
    PHONE_PATTERN,
    PORTFOLIO_PATTERN,
    SECTION_HEADER_PATTERN,
)


@dataclass(frozen=True)
class ContactInfo:
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    years_of_experience: Optional[float] = None
    experience_summary: Optional[str] = None


class ContactExtractor:
    """Extracts candidate contact details and experience metadata from raw resume text."""

    @classmethod
    def extract_name(cls, text: str) -> Optional[str]:
        explicit_match = EXPLICIT_NAME_PATTERN.search(text)
        if explicit_match:
            return explicit_match.group(1).strip()

        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            if SECTION_HEADER_PATTERN.search(line):
                break

            if EMAIL_PATTERN.search(line) or PHONE_PATTERN.search(line):
                continue

            if EXPERIENCE_YEARS_PATTERN.search(line):
                break

            words = line.split()
            if 2 <= len(words) <= 4:
                all_capitalized = all(
                    w[0].isupper() and w.isalpha() for w in words
                )
                if all_capitalized:
                    return line

        return None

    @classmethod
    def extract_email(cls, text: str) -> Optional[str]:
        match = EMAIL_PATTERN.search(text)
        return match.group(0).strip() if match else None

    @classmethod
    def extract_phone(cls, text: str) -> Optional[str]:
        for match in PHONE_PATTERN.finditer(text):
            candidate = match.group(0).strip()
            digits_only = re.sub(r"\D", "", candidate)
            if 7 <= len(digits_only) <= 15:
                return candidate
        return None

    @classmethod
    def extract_linkedin(cls, text: str) -> Optional[str]:
        match = LINKEDIN_PATTERN.search(text)
        if match:
            handle = match.group(1)
            return f"https://linkedin.com/in/{handle}"
        return None

    @classmethod
    def extract_github(cls, text: str) -> Optional[str]:
        match = GITHUB_PATTERN.search(text)
        if match:
            handle = match.group(1)
            return f"https://github.com/{handle}"
        return None

    @classmethod
    def extract_portfolio(cls, text: str) -> Optional[str]:
        match = PORTFOLIO_PATTERN.search(text)
        return match.group(0).strip() if match else None

    @classmethod
    def extract_years_of_experience(cls, text: str) -> Optional[float]:
        match = EXPERIENCE_YEARS_PATTERN.search(text)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None

    @classmethod
    def extract_experience_summary(cls, text: str) -> Optional[str]:
        match = EXPERIENCE_SUMMARY_PATTERN.search(text)
        return match.group(1).strip() if match else None

    @classmethod
    def extract(cls, text: str) -> ContactInfo:
        return ContactInfo(
            name=cls.extract_name(text),
            email=cls.extract_email(text),
            phone=cls.extract_phone(text),
            linkedin=cls.extract_linkedin(text),
            github=cls.extract_github(text),
            portfolio=cls.extract_portfolio(text),
            years_of_experience=cls.extract_years_of_experience(text),
            experience_summary=cls.extract_experience_summary(text),
        )
