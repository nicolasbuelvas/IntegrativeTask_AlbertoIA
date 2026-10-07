"""Precompiled regular expressions for candidate contact information and metadata."""

import re

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_PATTERN = re.compile(
    r"(?:(?:\+|00)\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{3,4}\b"
)

LINKEDIN_PATTERN = re.compile(
    r"(?:https?://)?(?:www\.)?linkedin\.com/in/([A-Za-z0-9_-]+)/?",
    re.IGNORECASE,
)

GITHUB_PATTERN = re.compile(
    r"(?:https?://)?(?:www\.)?github\.com/([A-Za-z0-9_-]+)/?",
    re.IGNORECASE,
)

PORTFOLIO_PATTERN = re.compile(
    r"https?://(?:www\.)?(?!github\.com|linkedin\.com)[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+(?:/[^\s]*)?",
    re.IGNORECASE,
)

EXPERIENCE_YEARS_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\s*(?:\+\s*)?(?:years?|yrs?)\s+(?:of\s+)?(?:experience|professional\s+experience|work\s+experience)",
    re.IGNORECASE,
)

EXPERIENCE_SUMMARY_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?\s*(?:\+\s*)?(?:years?|yrs?)\s+(?:of\s+)?(?:experience|professional\s+experience|work\s+experience)[^\n.]*)",
    re.IGNORECASE,
)

EXPLICIT_NAME_PATTERN = re.compile(
    r"^(?:Name|Candidate|Full\s*Name)\s*[:\-]\s*([A-Za-zÀ-ÿ]+(?:\s+[A-Za-zÀ-ÿ]+)+)$",
    re.IGNORECASE | re.MULTILINE,
)

SECTION_HEADER_PATTERN = re.compile(
    r"^(?:technical\s+skills|skills|experience|work\s+experience|education|projects|summary|contact|profile)\b",
    re.IGNORECASE,
)
