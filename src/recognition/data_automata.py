from src.recognition.automata_builder import ProfileAutomatonBuilder
from pyformlang.finite_automaton import Symbol

class DataAutomata:
    def __init__(self):
        self.ml_dfa = self._build_ml_dfa()
        self.data_dfa = self._build_data_dfa()

    def _build_ml_dfa(self):
        """
        Construye el autómata de Machine Learning según la especificación del proyecto:
        q0 --(ROL/LANG)--> q1 --(PANDAS/NUMPY)--> q2 --(FRAMEWORK_ML)--> q3 --(DB)--> q4 --(GIT)--> q5 (FINAL)
        """
        builder = ProfileAutomatonBuilder()
        transitions = []

        ml_roles_and_langs = [
            "MACHINE_LEARNING", "ML", "DATA_SCIENTIST", "MACHINE_LEARNING_ENGINEER", "AI_ENGINEER", "ML_ENGINEER",
            "PYTHON", "R", "JULIA"
        ]
        data_prep = ["PANDAS", "NUMPY"]
        ml_frameworks = ["SCIKIT_LEARN", "TENSORFLOW", "PYTORCH", "KERAS", "XGBOOST", "LIGHTGBM"]
        databases = ["SQL", "POSTGRESQL", "MYSQL", "MONGODB"]
        tools = ["GIT", "DOCKER", "KUBERNETES", "AWS", "GCP", "AZURE"]

        # q0 -> q1 (Rol o Lenguaje Core)
        for r in ml_roles_and_langs:
            transitions.extend([
                ("q0_start", r, "q1_lang"),
                ("q1_lang", r, "q1_lang")
            ])

        # q1 -> q2 (Data prep: Pandas / NumPy)
        for dp in data_prep:
            transitions.extend([
                ("q1_lang", dp, "q2_prep"),
                ("q2_prep", dp, "q2_prep")
            ])

        # q2 -> q3 (ML Framework)
        for fw in ml_frameworks:
            transitions.extend([
                ("q2_prep", fw, "q3_framework"),
                ("q3_framework", fw, "q3_framework")
            ])

        # q3 -> q4 (Database)
        for db in databases:
            transitions.extend([
                ("q3_framework", db, "q4_db"),
                ("q4_db", db, "q4_db")
            ])

        # q4 -> q5_final (Git / Tools)
        for t in tools:
            transitions.extend([
                ("q4_db", t, "q5_final"),
                ("q5_final", t, "q5_final")
            ])

        return builder.build_automaton(
            start_state="q0_start",
            transitions=transitions,
            final_states=["q5_final"]
        )

    def _build_data_dfa(self):
        """
        Construye el autómata de Data Engineer / Data Platform Engineer:
        q0 --(ROL)--> q1_role --(CORE_LANG)--> q2_core --(PROCESSING/PANDAS/SPARK)--> q3_proc --(STORAGE/SQL/BI)--> q4_final (FINAL)
        """
        builder = ProfileAutomatonBuilder()
        transitions = []

        de_roles = ["DATA", "DATA_ENGINEER", "DATA_ANALYST", "DATA_PLATFORM_ENGINEER", "DATA_ARCHITECT", "PLATFORM"]
        core_lang = ["PYTHON", "SQL", "SCALA", "JAVA", "R"]
        processing = ["ETL", "SPARK", "AIRFLOW", "HADOOP", "DATABRICKS", "PANDAS", "KAFKA", "FLINK", "DBT"]
        storage_tools = [
            "SQL", "POSTGRESQL", "MYSQL", "MARIADB", "SNOWFLAKE", "BIGQUERY", "REDSHIFT",
            "POWERBI", "TABLEAU", "GIT", "DOCKER", "AWS", "GCP", "AZURE"
        ]

        # Nivel 1: Rol
        for r in de_roles:
            transitions.extend([
                ("q0_start", r, "q1_role"),
                ("q1_role", r, "q1_role")
            ])

        # Nivel 2: Lenguaje Core
        for c in core_lang:
            transitions.extend([
                ("q0_start", c, "q2_core"),
                ("q1_role", c, "q2_core"),
                ("q2_core", c, "q2_core")
            ])

        # Nivel 3: Procesamiento / ETL
        for pr in processing:
            transitions.extend([
                ("q0_start", pr, "q3_proc"),
                ("q1_role", pr, "q3_proc"),
                ("q2_core", pr, "q3_proc"),
                ("q3_proc", pr, "q3_proc")
            ])

        # Nivel 4: Almacenamiento / BI / Herramientas
        for st in storage_tools:
            transitions.extend([
                ("q3_proc", st, "q4_final"),
                ("q4_final", st, "q4_final")
            ])

        return builder.build_automaton(
            start_state="q0_start",
            transitions=transitions,
            final_states=["q3_proc", "q4_final"]
        )

    def accepts_ml_token(self, token: str) -> bool:
        symbols = [Symbol(w) for w in token.upper().split()]
        return self.ml_dfa.accepts(symbols)

    def accepts_data_token(self, token: str) -> bool:
        symbols = [Symbol(w) for w in token.upper().split()]
        return self.data_dfa.accepts(symbols)

    def accepts_token(self, token: str) -> bool:
        symbols = [Symbol(w) for w in token.upper().split()]
        return self.ml_dfa.accepts(symbols) or self.data_dfa.accepts(symbols)