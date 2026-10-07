"""Information extraction stage using regular expressions."""

from src.extraction.contact_extractor import ContactExtractor, ContactInfo
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

__all__ = [
    "ContactExtractor",
    "ContactInfo",
    "EMAIL_PATTERN",
    "EXPLICIT_NAME_PATTERN",
    "EXPERIENCE_SUMMARY_PATTERN",
    "EXPERIENCE_YEARS_PATTERN",
    "GITHUB_PATTERN",
    "LINKEDIN_PATTERN",
    "PHONE_PATTERN",
    "PORTFOLIO_PATTERN",
    "SECTION_HEADER_PATTERN",
]
