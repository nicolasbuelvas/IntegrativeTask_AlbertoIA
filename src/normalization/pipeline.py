"""Canonical qualification normalization and sorting pipeline."""

from typing import Iterable, List, Optional, Set
from src.config.taxonomy import ALL_CANONICAL_SKILLS, PROFILES, SKILL_TO_CATEGORY
from src.extraction.skill_extractor import SkillExtractor
from src.models.profiles import ProfileDefinition, ProfileType
from src.normalization.skill_transducers import build_unified_skill_transducer
from src.normalization.transducer_builder import TransducerBuilder


class NormalizationPipeline:
    """End-to-end normalization pipeline converting raw skill tokens to canonical sequences."""

    def __init__(self, transducer: Optional[TransducerBuilder] = None) -> None:
        self.transducer = transducer if transducer is not None else build_unified_skill_transducer()

    def normalize_token(self, token: str) -> Optional[str]:
        """Normalize a single raw skill token to its canonical symbol."""
        if not token:
            return None
        canon = self.transducer.translate_word(token)
        if canon:
            return canon
        cleaned = token.strip()
        if cleaned.upper() in ALL_CANONICAL_SKILLS:
            return cleaned.upper()
        for variant in (cleaned, cleaned.lower(), cleaned.title(), cleaned.capitalize()):
            canon = self.transducer.translate_word(variant)
            if canon:
                return canon
        return None

    def normalize_tokens(self, tokens: Iterable[str]) -> List[str]:
        """Normalize an iterable of skill tokens, removing duplicates while preserving order."""
        normalized: List[str] = []
        seen: Set[str] = set()

        for token in tokens:
            canon = self.normalize_token(token)
            if canon and canon not in seen:
                seen.add(canon)
                normalized.append(canon)

        return normalized

    def sort_for_profile(self, canonical_skills: Iterable[str], profile_type: ProfileType) -> List[str]:
        """Filter skills to profile alphabet and sort according to profile canonical order."""
        profile: ProfileDefinition = PROFILES[profile_type]
        valid_skills: List[str] = [s for s in canonical_skills if s in profile.canonical_alphabet]

        order_map = {category: idx for idx, category in enumerate(profile.canonical_order)}

        def sort_key(skill: str) -> tuple[int, str]:
            category = SKILL_TO_CATEGORY.get(skill, "")
            cat_priority = order_map.get(category, len(order_map))
            return (cat_priority, skill)

        return sorted(valid_skills, key=sort_key)

    def process_raw_skills(
        self,
        raw_skills: Iterable[str],
        profile_type: Optional[ProfileType] = None,
    ) -> List[str]:
        """Normalize raw skills and optionally filter/sort for a target profile."""
        normalized = self.normalize_tokens(raw_skills)
        if profile_type is not None:
            return self.sort_for_profile(normalized, profile_type)
        return normalized

    def process_resume_text(
        self,
        resume_text: str,
        profile_type: Optional[ProfileType] = None,
    ) -> List[str]:
        """Extract raw skills from resume text, normalize, and sort for target profile."""
        raw_skills = SkillExtractor.extract_unique_skills(resume_text)
        return self.process_raw_skills(raw_skills, profile_type=profile_type)
