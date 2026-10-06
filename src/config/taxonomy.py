"""Canonical skill taxonomy and profile alphabets for formal language screening."""

from typing import Dict, List, Set
from src.models.profiles import ProfileCategory, ProfileDefinition, ProfileType

FRONTEND_LANGUAGES: Set[str] = {"JAVASCRIPT", "TYPESCRIPT"}
FRONTEND_FRAMEWORKS: Set[str] = {"REACT", "ANGULAR", "VUE"}
BACKEND_FRAMEWORKS: Set[str] = {"NODE_JS", "DJANGO", "SPRING_BOOT", "FASTAPI", "EXPRESS"}
GENERAL_LANGUAGES: Set[str] = {"PYTHON", "JAVA", "GO", "SCALA"}
DATABASES: Set[str] = {"POSTGRESQL", "MYSQL", "MONGODB", "REDIS", "SQL"}
AI_DATA_CORE: Set[str] = {"PANDAS", "NUMPY", "SCIKIT_LEARN"}
AI_FRAMEWORKS: Set[str] = {"TENSORFLOW", "PYTORCH"}
DATA_ENGINEERING_TOOLS: Set[str] = {"SPARK", "HADOOP", "FLINK", "AIRFLOW", "SNOWFLAKE", "BIGQUERY"}
TOOLS_INFRA: Set[str] = {"GIT", "DOCKER", "REST_APIS", "GRAPHQL"}

ALL_CANONICAL_SKILLS: Set[str] = (
    FRONTEND_LANGUAGES
    | FRONTEND_FRAMEWORKS
    | BACKEND_FRAMEWORKS
    | GENERAL_LANGUAGES
    | DATABASES
    | AI_DATA_CORE
    | AI_FRAMEWORKS
    | DATA_ENGINEERING_TOOLS
    | TOOLS_INFRA
)

FULL_STACK_ALPHABET: Set[str] = (
    FRONTEND_LANGUAGES
    | FRONTEND_FRAMEWORKS
    | BACKEND_FRAMEWORKS
    | DATABASES
    | {"REST_APIS", "GIT"}
)

FULL_STACK_ORDER: List[str] = [
    "FRONTEND_LANGUAGE",
    "FRONTEND_FRAMEWORK",
    "BACKEND_FRAMEWORK",
    "DATABASE",
    "API",
    "VERSION_CONTROL",
]

MACHINE_LEARNING_ALPHABET: Set[str] = (
    {"PYTHON"}
    | AI_DATA_CORE
    | AI_FRAMEWORKS
    | DATABASES
    | {"GIT"}
)

MACHINE_LEARNING_ORDER: List[str] = [
    "LANGUAGE",
    "DATA_PROCESSING",
    "ML_LIBRARY",
    "DEEP_LEARNING",
    "DATABASE",
    "VERSION_CONTROL",
]

BACKEND_ALPHABET: Set[str] = (
    GENERAL_LANGUAGES
    | BACKEND_FRAMEWORKS
    | DATABASES
    | {"REST_APIS", "GRAPHQL", "DOCKER", "GIT"}
)

BACKEND_ORDER: List[str] = [
    "LANGUAGE",
    "BACKEND_FRAMEWORK",
    "DATABASE",
    "API",
    "INFRASTRUCTURE",
    "VERSION_CONTROL",
]

DATA_ENGINEER_ALPHABET: Set[str] = (
    {"PYTHON", "SCALA", "SQL"}
    | DATA_ENGINEERING_TOOLS
    | DATABASES
    | {"DOCKER", "GIT"}
)

DATA_ENGINEER_ORDER: List[str] = [
    "LANGUAGE",
    "DISTRIBUTED_COMPUTING",
    "ORCHESTRATION",
    "WAREHOUSE_DATABASE",
    "INFRASTRUCTURE",
    "VERSION_CONTROL",
]

SKILL_TO_CATEGORY: Dict[str, str] = {
    "JAVASCRIPT": "FRONTEND_LANGUAGE",
    "TYPESCRIPT": "FRONTEND_LANGUAGE",
    "REACT": "FRONTEND_FRAMEWORK",
    "ANGULAR": "FRONTEND_FRAMEWORK",
    "VUE": "FRONTEND_FRAMEWORK",
    "NODE_JS": "BACKEND_FRAMEWORK",
    "DJANGO": "BACKEND_FRAMEWORK",
    "SPRING_BOOT": "BACKEND_FRAMEWORK",
    "FASTAPI": "BACKEND_FRAMEWORK",
    "EXPRESS": "BACKEND_FRAMEWORK",
    "PYTHON": "LANGUAGE",
    "JAVA": "LANGUAGE",
    "GO": "LANGUAGE",
    "SCALA": "LANGUAGE",
    "SQL": "DATABASE",
    "POSTGRESQL": "DATABASE",
    "MYSQL": "DATABASE",
    "MONGODB": "DATABASE",
    "REDIS": "DATABASE",
    "PANDAS": "DATA_PROCESSING",
    "NUMPY": "DATA_PROCESSING",
    "SCIKIT_LEARN": "ML_LIBRARY",
    "TENSORFLOW": "DEEP_LEARNING",
    "PYTORCH": "DEEP_LEARNING",
    "SPARK": "DISTRIBUTED_COMPUTING",
    "HADOOP": "DISTRIBUTED_COMPUTING",
    "FLINK": "DISTRIBUTED_COMPUTING",
    "AIRFLOW": "ORCHESTRATION",
    "SNOWFLAKE": "WAREHOUSE_DATABASE",
    "BIGQUERY": "WAREHOUSE_DATABASE",
    "REST_APIS": "API",
    "GRAPHQL": "API",
    "DOCKER": "INFRASTRUCTURE",
    "GIT": "VERSION_CONTROL",
}

PROFILES: Dict[ProfileType, ProfileDefinition] = {
    ProfileType.FULL_STACK_DEVELOPER: ProfileDefinition(
        profile_type=ProfileType.FULL_STACK_DEVELOPER,
        category=ProfileCategory.SOFTWARE_ENGINEERING,
        canonical_alphabet=FULL_STACK_ALPHABET,
        canonical_order=FULL_STACK_ORDER,
        description="Client and server web development pipeline.",
    ),
    ProfileType.MACHINE_LEARNING_ENGINEER: ProfileDefinition(
        profile_type=ProfileType.MACHINE_LEARNING_ENGINEER,
        category=ProfileCategory.AI_DATA,
        canonical_alphabet=MACHINE_LEARNING_ALPHABET,
        canonical_order=MACHINE_LEARNING_ORDER,
        description="Predictive modeling, machine learning, and data processing.",
    ),
    ProfileType.BACKEND_DEVELOPER: ProfileDefinition(
        profile_type=ProfileType.BACKEND_DEVELOPER,
        category=ProfileCategory.SOFTWARE_ENGINEERING,
        canonical_alphabet=BACKEND_ALPHABET,
        canonical_order=BACKEND_ORDER,
        description="Backend services, APIs, database architectures, and infrastructure.",
    ),
    ProfileType.DATA_ENGINEER: ProfileDefinition(
        profile_type=ProfileType.DATA_ENGINEER,
        category=ProfileCategory.AI_DATA,
        canonical_alphabet=DATA_ENGINEER_ALPHABET,
        canonical_order=DATA_ENGINEER_ORDER,
        description="Data pipelines, distributed computing, and data warehouses.",
    ),
}
