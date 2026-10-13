from src.recognition.automata_builder import ProfileAutomatonBuilder
from pyformlang.finite_automaton import Symbol

class SoftwareAutomata:
    def __init__(self):
        self.fullstack_dfa = self._build_fullstack_dfa()
        self.backend_dfa = self._build_backend_dfa()

    def _build_backend_dfa(self):
        builder = ProfileAutomatonBuilder()
        transitions = []

        roles_and_langs = [
            "BACKEND", "BACKEND_DEVELOPER", "BACKEND_ENGINEER", "SOFTWARE_ENGINEER", "APPLICATION_ENGINEER",
            "PYTHON", "JAVA", "RUBY", "GO", "C_SHARP", "PHP", "SCALA"
        ]
        backend_tech = [
            "SPRING", "SPRING_BOOT", "DJANGO", "FASTAPI", "EXPRESS", "NODE_JS"
        ]
        databases = ["POSTGRESQL", "MYSQL", "MONGODB", "ORACLE", "REDIS", "SQL", "DYNAMODB", "MARIADB", "CASSANDRA"]
        tools = ["GIT", "DOCKER", "KUBERNETES", "REST", "API", "REST_APIS", "GRAPHQL", "POSTMAN", "LINUX", "AWS"]

        for r in roles_and_langs:
            transitions.extend([
                ("q0_start", r, "q1_be_tech"),
                ("q1_be_tech", r, "q1_be_tech")
            ])

        for be in backend_tech:
            transitions.extend([
                ("q0_start", be, "q1_be_tech"),
                ("q1_be_tech", be, "q1_be_tech")
            ])

        for db in databases:
            transitions.extend([
                ("q1_be_tech", db, "q2_db"),
                ("q2_db", db, "q2_db")
            ])

        for t in tools:
            transitions.extend([
                ("q2_db", t, "q3_tools"),
                ("q3_tools", t, "q3_tools")
            ])

        return builder.build_automaton(
            start_state="q0_start",
            transitions=transitions,
            final_states=["q3_tools"]
        )

    def _build_fullstack_dfa(self):
        builder = ProfileAutomatonBuilder()
        transitions = []

        fs_roles_and_langs = [
            "FULLSTACK", "FULLSTACK_DEVELOPER", "FULL_STACK_DEVELOPER", "FULL_STACK_ENGINEER",
            "JAVASCRIPT", "TYPESCRIPT"
        ]
        frontend = ["REACT", "ANGULAR", "VUE", "HTML", "CSS", "NEXT_JS", "SASS", "REDUX", "TAILWIND"]
        backend = ["NODE_JS", "JAVA", "DJANGO", "SPRING_BOOT", "FASTAPI", "EXPRESS", "PYTHON", "RUBY", "GO", "C_SHARP", "PHP"]
        databases = ["POSTGRESQL", "MYSQL", "MONGODB", "REDIS", "SQL", "DYNAMODB", "MARIADB", "CASSANDRA"]
        tools = ["GIT", "DOCKER", "KUBERNETES", "REST", "API", "REST_APIS", "GRAPHQL", "POSTMAN", "LINUX", "AWS"]

        # Paso 1: Rol / Lenguaje Web obligatorio para iniciar el perfil Full Stack
        for rl in fs_roles_and_langs:
            transitions.extend([
                ("q0_start", rl, "q1_lang"),
                ("q1_lang", rl, "q1_lang")
            ])

        # Paso 2: Tecnologías Frontend
        for fe in frontend:
            transitions.extend([
                ("q1_lang", fe, "q2_fe"),
                ("q2_fe", fe, "q2_fe")
            ])

        # Paso 3: Tecnologías Backend
        for be in backend:
            transitions.extend([
                ("q2_fe", be, "q3_be"),
                ("q3_be", be, "q3_be")
            ])

        # Paso 4: Base de Datos
        for db in databases:
            transitions.extend([
                ("q3_be", db, "q4_db"),
                ("q4_db", db, "q4_db")
            ])

        # Paso 5: Herramientas / Control de versiones (Estado Final de Aceptación)
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

    def accepts_backend_token(self, token: str) -> bool:
        symbols = [Symbol(w) for w in token.upper().split()]
        return self.backend_dfa.accepts(symbols)

    def accepts_fullstack_token(self, token: str) -> bool:
        symbols = [Symbol(w) for w in token.upper().split()]
        return self.fullstack_dfa.accepts(symbols)

    def accepts_token(self, token: str) -> bool:
        symbols = [Symbol(w) for w in token.upper().split()]
        return self.backend_dfa.accepts(symbols) or self.fullstack_dfa.accepts(symbols)