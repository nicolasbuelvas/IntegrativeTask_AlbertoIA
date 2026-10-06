import pytest
from src.models.profiles import ProfileCategory, ProfileType
from src.config.taxonomy import (
    ALL_CANONICAL_SKILLS,
    PROFILES,
    SKILL_TO_CATEGORY,
    FULL_STACK_ALPHABET,
    MACHINE_LEARNING_ALPHABET,
    BACKEND_ALPHABET,
    DATA_ENGINEER_ALPHABET,
)


def test_four_profiles_defined():
    assert len(PROFILES) == 4
    assert ProfileType.FULL_STACK_DEVELOPER in PROFILES
    assert ProfileType.MACHINE_LEARNING_ENGINEER in PROFILES
    assert ProfileType.BACKEND_DEVELOPER in PROFILES
    assert ProfileType.DATA_ENGINEER in PROFILES


def test_profile_categories():
    assert PROFILES[ProfileType.FULL_STACK_DEVELOPER].category == ProfileCategory.SOFTWARE_ENGINEERING
    assert PROFILES[ProfileType.MACHINE_LEARNING_ENGINEER].category == ProfileCategory.AI_DATA
    assert PROFILES[ProfileType.BACKEND_DEVELOPER].category == ProfileCategory.SOFTWARE_ENGINEERING
    assert PROFILES[ProfileType.DATA_ENGINEER].category == ProfileCategory.AI_DATA


def test_canonical_skills_contain_core_technologies():
    expected = {"JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "PYTHON", "TENSORFLOW", "GIT"}
    assert expected.issubset(ALL_CANONICAL_SKILLS)


def test_all_canonical_skills_mapped_to_category():
    for skill in ALL_CANONICAL_SKILLS:
        assert skill in SKILL_TO_CATEGORY, f"Skill {skill} missing from SKILL_TO_CATEGORY"


def test_alphabets_are_subsets_of_all_canonical():
    assert FULL_STACK_ALPHABET.issubset(ALL_CANONICAL_SKILLS)
    assert MACHINE_LEARNING_ALPHABET.issubset(ALL_CANONICAL_SKILLS)
    assert BACKEND_ALPHABET.issubset(ALL_CANONICAL_SKILLS)
    assert DATA_ENGINEER_ALPHABET.issubset(ALL_CANONICAL_SKILLS)
