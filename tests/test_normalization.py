"""Unit tests for Stage 2: Qualification normalization using Finite-State Transducers."""

import pytest

from src.models.profiles import ProfileType
from src.normalization.pipeline import NormalizationPipeline
from src.normalization.skill_transducers import (
    build_ai_data_transducer,
    build_software_engineering_transducer,
    build_unified_skill_transducer,
)
from src.normalization.transducer_builder import Transducer7Tuple, TransducerBuilder


class TestTransducerBuilder:
    """Tests for the formal Finite-State Transducer builder and 7-tuple model."""

    def test_formal_7_tuple_properties(self):
        builder = TransducerBuilder(name="SampleFST")
        builder.add_word_mapping("JS", "JAVASCRIPT")

        tup = builder.get_formal_tuple()
        assert isinstance(tup, Transducer7Tuple)
        assert len(tup.Q) >= 3  # q0, intermediate, final
        assert "J" in tup.Sigma and "S" in tup.Sigma
        assert "JAVASCRIPT" in tup.Gamma
        assert tup.q0.value == "q0"
        assert len(tup.F) == 1

        # Mathematical 7-tuple unpack
        Q, Sigma, Gamma, delta, omega, q0, F = tup.as_tuple()
        assert Q == tup.Q
        assert Sigma == tup.Sigma
        assert Gamma == tup.Gamma

    def test_word_translation_match_and_mismatch(self):
        builder = TransducerBuilder(name="SingleMapping")
        builder.add_word_mapping("PyTorch", "PYTORCH")

        assert builder.translate_word("PyTorch") == "PYTORCH"
        assert builder.translate_word("Torch") is None
        assert builder.translate_word("") is None

    def test_dot_graph_export(self):
        builder = TransducerBuilder(name="GraphExport")
        builder.add_word_mapping("Go", "GO")
        dot = builder.to_dot()
        assert "digraph GraphExport" in dot
        assert "shape=doublecircle" in dot
        assert "G / " in dot


class TestDomainTransducers:
    """Tests for domain skill normalization transducers."""

    def test_software_engineering_canonical_mappings(self):
        fst = build_software_engineering_transducer()

        # Rubric specified examples
        assert fst.translate_word("JS") == "JAVASCRIPT"
        assert fst.translate_word("Javascript") == "JAVASCRIPT"
        assert fst.translate_word("React.js") == "REACT"
        assert fst.translate_word("ReactJS") == "REACT"
        assert fst.translate_word("NodeJS") == "NODE_JS"
        assert fst.translate_word("Node.js") == "NODE_JS"
        assert fst.translate_word("Postgres") == "POSTGRESQL"
        assert fst.translate_word("PostgreSQL") == "POSTGRESQL"
        assert fst.translate_word("Spring Boot") == "SPRING_BOOT"
        assert fst.translate_word("Git") == "GIT"

    def test_ai_data_canonical_mappings(self):
        fst = build_ai_data_transducer()

        # Rubric specified examples
        assert fst.translate_word("pandas") == "PANDAS"
        assert fst.translate_word("sklearn") == "SCIKIT_LEARN"
        assert fst.translate_word("scikit learn") == "SCIKIT_LEARN"
        assert fst.translate_word("Scikit-learn") == "SCIKIT_LEARN"
        assert fst.translate_word("Tensor Flow") == "TENSORFLOW"
        assert fst.translate_word("TensorFlow") == "TENSORFLOW"
        assert fst.translate_word("Py Torch") == "PYTORCH"
        assert fst.translate_word("PyTorch") == "PYTORCH"
        assert fst.translate_word("Spark") == "SPARK"
        assert fst.translate_word("Airflow") == "AIRFLOW"


class TestNormalizationPipeline:
    """Tests for the full normalization pipeline and canonical sorting."""

    def test_full_stack_canonical_sorting_rubric_example(self):
        pipeline = NormalizationPipeline()
        # Direct example from rubric specification:
        # "Git, NodeJS, JS, Postgres, React.js -> JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT"
        raw_input = ["Git", "NodeJS", "JS", "Postgres", "React.js"]
        sorted_output = pipeline.process_raw_skills(
            raw_input,
            profile_type=ProfileType.FULL_STACK_DEVELOPER,
        )

        expected = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
        assert sorted_output == expected

    def test_machine_learning_canonical_sorting(self):
        pipeline = NormalizationPipeline()
        # Direct example from rubric specification:
        # "PYTHON, PANDAS, TENSORFLOW, POSTGRESQL, GIT"
        raw_input = ["Git", "Postgres", "TensorFlow", "Pandas", "Python", "scikit-learn"]
        sorted_output = pipeline.process_raw_skills(
            raw_input,
            profile_type=ProfileType.MACHINE_LEARNING_ENGINEER,
        )

        # Expected order: LANGUAGE -> DATA_PROCESSING -> ML_LIBRARY -> DEEP_LEARNING -> DATABASE -> VERSION_CONTROL
        expected = ["PYTHON", "PANDAS", "SCIKIT_LEARN", "TENSORFLOW", "POSTGRESQL", "GIT"]
        assert sorted_output == expected

    def test_backend_canonical_sorting(self):
        pipeline = NormalizationPipeline()
        raw_input = ["Git", "Docker", "PostgreSQL", "FastAPI", "Python", "REST APIs"]
        sorted_output = pipeline.process_raw_skills(
            raw_input,
            profile_type=ProfileType.BACKEND_DEVELOPER,
        )

        # Expected order: LANGUAGE -> BACKEND_FRAMEWORK -> DATABASE -> API -> INFRASTRUCTURE -> VERSION_CONTROL
        expected = ["PYTHON", "FASTAPI", "POSTGRESQL", "REST_APIS", "DOCKER", "GIT"]
        assert sorted_output == expected

    def test_data_engineer_canonical_sorting(self):
        pipeline = NormalizationPipeline()
        raw_input = ["Git", "Docker", "Snowflake", "Airflow", "Spark", "Python"]
        sorted_output = pipeline.process_raw_skills(
            raw_input,
            profile_type=ProfileType.DATA_ENGINEER,
        )

        # Expected order: LANGUAGE -> DISTRIBUTED_COMPUTING -> ORCHESTRATION -> WAREHOUSE_DATABASE -> INFRASTRUCTURE -> VERSION_CONTROL
        expected = ["PYTHON", "SPARK", "AIRFLOW", "SNOWFLAKE", "DOCKER", "GIT"]
        assert sorted_output == expected

    def test_process_resume_text_end_to_end(self):
        pipeline = NormalizationPipeline()
        resume_snippet = """
        Technical Skills:
        JS, React.js, NodeJS, Postgres, Git.
        """
        output = pipeline.process_resume_text(
            resume_snippet,
            profile_type=ProfileType.FULL_STACK_DEVELOPER,
        )
        assert output == ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
