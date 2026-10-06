"""Domain models for professional job profiles and canonical alphabets."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Set


class ProfileCategory(str, Enum):
    SOFTWARE_ENGINEERING = "Software Engineering"
    AI_DATA = "AI/Data"


class ProfileType(str, Enum):
    FULL_STACK_DEVELOPER = "Full Stack Developer"
    MACHINE_LEARNING_ENGINEER = "Machine Learning Engineer"
    BACKEND_DEVELOPER = "Backend Developer"
    DATA_ENGINEER = "Data Engineer"


@dataclass(frozen=True)
class ProfileDefinition:
    profile_type: ProfileType
    category: ProfileCategory
    canonical_alphabet: Set[str] = field(default_factory=set)
    canonical_order: List[str] = field(default_factory=list)
    description: str = ""
