"""Technical skill entity extraction from resume text using regular expressions."""

import re
from typing import List, Optional, Set

from src.extraction.regex_patterns import SECTION_HEADER_PATTERN

# Precompiled regular expressions for candidate skill surface variations.
SKILL_PATTERNS: List[re.Pattern] = [
    # Frontend languages
    re.compile(r"\b(?:JavaScript|Javascript|JS)\b"),
    re.compile(r"\b(?:TypeScript|Typescript|TS)\b"),
    # Frontend frameworks
    re.compile(r"\bReact(?:\.js|JS)?\b", re.IGNORECASE),
    re.compile(r"\bAngular(?:\.js|JS)?\b", re.IGNORECASE),
    re.compile(r"\bVue(?:\.js|JS)?\b", re.IGNORECASE),
    # Backend frameworks
    re.compile(r"\bNode(?:\.js|JS|\s+JS)?\b", re.IGNORECASE),
    re.compile(r"\bDjango\b", re.IGNORECASE),
    re.compile(r"\bSpring\s*Boot\b", re.IGNORECASE),
    re.compile(r"\bFastAPI\b", re.IGNORECASE),
    re.compile(r"\bExpress(?:\.js|JS)?\b", re.IGNORECASE),
    # General-purpose languages
    re.compile(r"\bPython(?:3)?\b", re.IGNORECASE),
    re.compile(r"\bJava(?!\s*Script|\s*Doc)\b"),
    re.compile(r"\b(?:Golang|Go)\b"),
    re.compile(r"\bScala\b", re.IGNORECASE),
    # Databases
    re.compile(r"\bPostgre(?:SQL|s)\b", re.IGNORECASE),
    re.compile(r"\bMySQL\b", re.IGNORECASE),
    re.compile(r"\bMongo(?:\s*DB)?\b", re.IGNORECASE),
    re.compile(r"\bRedis\b", re.IGNORECASE),
    re.compile(r"\bSQL\b(?!\s*Server)"),
    # AI / Data core
    re.compile(r"\bPandas\b", re.IGNORECASE),
    re.compile(r"\bNumPy\b", re.IGNORECASE),
    re.compile(r"\b(?:scikit[- ]learn|sklearn)\b", re.IGNORECASE),
    # AI frameworks
    re.compile(r"\bTensor\s*Flow\b", re.IGNORECASE),
    re.compile(r"\bPy\s*Torch\b", re.IGNORECASE),
    # Data engineering
    re.compile(r"\b(?:Apache\s+)?Spark\b", re.IGNORECASE),
    re.compile(r"\b(?:Apache\s+)?Hadoop\b", re.IGNORECASE),
    re.compile(r"\b(?:Apache\s+)?Flink\b", re.IGNORECASE),
    re.compile(r"\b(?:Apache\s+)?Airflow\b", re.IGNORECASE),
    re.compile(r"\bSnowflake\b", re.IGNORECASE),
    re.compile(r"\b(?:Google\s+)?Big\s*Query\b", re.IGNORECASE),
    # Tools and infrastructure
    re.compile(r"\bGit(?!\s*Hub|\s*Lab)\b", re.IGNORECASE),
    re.compile(r"\bDocker\b", re.IGNORECASE),
    re.compile(r"\bREST(?:ful)?(?:\s+APIs?)?\b", re.IGNORECASE),
    re.compile(r"\bGraphQL\b", re.IGNORECASE),
]

SKILLS_SECTION_PATTERN = re.compile(
    r"(?:technical\s+skills|skills|technologies|core\s+competencies)\s*[:\-]?\s*(.*?)(?=\n\s*(?:experience|education|projects|summary|profile|contact)\b|\Z)",
    re.IGNORECASE | re.DOTALL,
)


class SkillExtractor:
    """Extracts raw technical skill tokens from resume text using regular expressions."""

    @classmethod
    def extract_skills_section(cls, text: str) -> Optional[str]:
        """Extracts the body of the technical skills section if explicitly present."""
        match = SKILLS_SECTION_PATTERN.search(text)
        return match.group(1).strip() if match else None

    @classmethod
    def extract_raw_skills(cls, text: str, section_only: bool = False) -> List[str]:
        """Finds all raw skill tokens in text, preserving occurrence order without deduplicating."""
        target_text = text
        if section_only:
            section = cls.extract_skills_section(text)
            if section:
                target_text = section

        matches: List[tuple[int, str]] = []
        for pattern in SKILL_PATTERNS:
            for match in pattern.finditer(target_text):
                matches.append((match.start(), match.group(0).strip()))

        # Sort matches by appearance in text
        matches.sort(key=lambda m: m[0])

        return [token for _, token in matches]

    @classmethod
    def extract_unique_skills(cls, text: str, section_only: bool = False) -> List[str]:
        """Extracts unique raw skill tokens in first-seen order."""
        raw_tokens = cls.extract_raw_skills(text, section_only=section_only)
        seen: Set[str] = set()
        unique: List[str] = []
        for token in raw_tokens:
            token_key = token.lower()
            if token_key not in seen:
                seen.add(token_key)
                unique.append(token)
        return unique
