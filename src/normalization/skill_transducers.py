"""Domain-specific finite-state transducers for qualification normalization.

Maps lexical variations of skills to canonical alphabet tokens using FSTs.
"""

from typing import Dict, List, Optional
from src.normalization.transducer_builder import Transducer7Tuple, TransducerBuilder

# Lexical variations mapped to canonical tokens for Software Engineering.
SOFTWARE_SKILL_SYNONYMS: Dict[str, str] = {
    # Frontend languages
    "JS": "JAVASCRIPT",
    "JavaScript": "JAVASCRIPT",
    "Javascript": "JAVASCRIPT",
    "javascript": "JAVASCRIPT",
    "TS": "TYPESCRIPT",
    "TypeScript": "TYPESCRIPT",
    "Typescript": "TYPESCRIPT",
    "typescript": "TYPESCRIPT",
    # Frontend frameworks
    "React": "REACT",
    "React.js": "REACT",
    "ReactJS": "REACT",
    "react": "REACT",
    "react.js": "REACT",
    "Angular": "ANGULAR",
    "AngularJS": "ANGULAR",
    "Angular.js": "ANGULAR",
    "angular": "ANGULAR",
    "Vue": "VUE",
    "Vue.js": "VUE",
    "VueJS": "VUE",
    "vue": "VUE",
    # Backend frameworks
    "Node": "NODE_JS",
    "Node.js": "NODE_JS",
    "NodeJS": "NODE_JS",
    "node.js": "NODE_JS",
    "nodejs": "NODE_JS",
    "Django": "DJANGO",
    "django": "DJANGO",
    "Spring Boot": "SPRING_BOOT",
    "SpringBoot": "SPRING_BOOT",
    "Spring": "SPRING_BOOT",
    "spring boot": "SPRING_BOOT",
    "FastAPI": "FASTAPI",
    "fastapi": "FASTAPI",
    "Express": "EXPRESS",
    "Express.js": "EXPRESS",
    "ExpressJS": "EXPRESS",
    "express": "EXPRESS",
    # General languages
    "Java": "JAVA",
    "java": "JAVA",
    "Go": "GO",
    "Golang": "GO",
    "golang": "GO",
    # Databases
    "Postgres": "POSTGRESQL",
    "PostgreSQL": "POSTGRESQL",
    "postgres": "POSTGRESQL",
    "postgresql": "POSTGRESQL",
    "MySQL": "MYSQL",
    "mysql": "MYSQL",
    "MongoDB": "MONGODB",
    "Mongo": "MONGODB",
    "mongodb": "MONGODB",
    "Redis": "REDIS",
    "redis": "REDIS",
    "SQL": "SQL",
    "sql": "SQL",
    # Tools & APIs
    "Git": "GIT",
    "git": "GIT",
    "Docker": "DOCKER",
    "docker": "DOCKER",
    "REST": "REST_APIS",
    "REST APIs": "REST_APIS",
    "RESTful": "REST_APIS",
    "REST API": "REST_APIS",
    "GraphQL": "GRAPHQL",
    "graphql": "GRAPHQL",
}

# Lexical variations mapped to canonical tokens for AI and Data Science.
AI_DATA_SKILL_SYNONYMS: Dict[str, str] = {
    # Core language
    "Python": "PYTHON",
    "python": "PYTHON",
    "Python3": "PYTHON",
    "Scala": "SCALA",
    "scala": "SCALA",
    # AI / Data Core
    "Pandas": "PANDAS",
    "pandas": "PANDAS",
    "NumPy": "NUMPY",
    "numpy": "NUMPY",
    "Numpy": "NUMPY",
    "scikit-learn": "SCIKIT_LEARN",
    "Scikit-learn": "SCIKIT_LEARN",
    "scikit learn": "SCIKIT_LEARN",
    "sklearn": "SCIKIT_LEARN",
    "Sklearn": "SCIKIT_LEARN",
    # Deep Learning Frameworks
    "TensorFlow": "TENSORFLOW",
    "Tensor Flow": "TENSORFLOW",
    "tensorflow": "TENSORFLOW",
    "PyTorch": "PYTORCH",
    "Py Torch": "PYTORCH",
    "pytorch": "PYTORCH",
    # Distributed Computing & Orchestration
    "Spark": "SPARK",
    "Apache Spark": "SPARK",
    "spark": "SPARK",
    "Hadoop": "HADOOP",
    "Apache Hadoop": "HADOOP",
    "hadoop": "HADOOP",
    "Flink": "FLINK",
    "Apache Flink": "FLINK",
    "flink": "FLINK",
    "Airflow": "AIRFLOW",
    "Apache Airflow": "AIRFLOW",
    "airflow": "AIRFLOW",
    "Snowflake": "SNOWFLAKE",
    "snowflake": "SNOWFLAKE",
    "BigQuery": "BIGQUERY",
    "Google BigQuery": "BIGQUERY",
    "bigquery": "BIGQUERY",
    # Databases & Tools
    "SQL": "SQL",
    "sql": "SQL",
    "Postgres": "POSTGRESQL",
    "PostgreSQL": "POSTGRESQL",
    "postgres": "POSTGRESQL",
    "Git": "GIT",
    "git": "GIT",
    "Docker": "DOCKER",
    "docker": "DOCKER",
}


def build_software_engineering_transducer() -> TransducerBuilder:
    """Build FST for Software Engineering qualification normalization."""
    builder = TransducerBuilder(name="SoftwareEngineeringFST")
    builder.add_batch_mappings(SOFTWARE_SKILL_SYNONYMS)
    return builder


def build_ai_data_transducer() -> TransducerBuilder:
    """Build FST for AI and Data qualification normalization."""
    builder = TransducerBuilder(name="AIDataFST")
    builder.add_batch_mappings(AI_DATA_SKILL_SYNONYMS)
    return builder


def build_unified_skill_transducer() -> TransducerBuilder:
    """Build combined FST covering all software engineering and AI/data qualifications."""
    builder = TransducerBuilder(name="UnifiedSkillFST")
    combined_mappings = dict(SOFTWARE_SKILL_SYNONYMS)
    combined_mappings.update(AI_DATA_SKILL_SYNONYMS)
    builder.add_batch_mappings(combined_mappings)
    return builder
