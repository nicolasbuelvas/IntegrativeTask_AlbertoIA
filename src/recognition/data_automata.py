from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State, Symbol

class DataAutomata:
    """Contiene los autómatas de reconocimiento para perfiles de Data y AI."""

    def __init__(self):
        self.ml_dfa = self._build_ml_dfa()
        self.data_dfa = self._build_data_dfa()

    def _build_ml_dfa(self) -> DeterministicFiniteAutomaton:
        dfa = DeterministicFiniteAutomaton()
        
        # Estado inicial q0
        dfa.add_start_state(State("q0"))
        
        # Transiciones de ML: Lenguaje -> Librería -> Framework -> DB -> Git
        dfa.add_transition(State("q0"), Symbol("PYTHON"), State("q1"))
        
        # Opciones en q1: PANDAS o NUMPY
        dfa.add_transition(State("q1"), Symbol("PANDAS"), State("q2"))
        dfa.add_transition(State("q1"), Symbol("NUMPY"), State("q2"))
        
        # Opciones en q2: SCIKIT_LEARN o TENSORFLOW
        dfa.add_transition(State("q2"), Symbol("SCIKIT_LEARN"), State("q3"))
        dfa.add_transition(State("q2"), Symbol("TENSORFLOW"), State("q3"))
        
        # Persistencia y Control de versiones
        dfa.add_transition(State("q3"), Symbol("SQL"), State("q4"))
        dfa.add_transition(State("q4"), Symbol("GIT"), State("q5"))
        
        # Estado final
        dfa.add_final_state(State("q5"))
        return dfa

    def _build_data_dfa(self) -> DeterministicFiniteAutomaton:
        """Builds a DFA to recognize data engineering/science keywords."""
        dfa = DeterministicFiniteAutomaton()
        s0 = State("s0")
        s1 = State("s1")

        dfa.add_start_state(s0)
        dfa.add_final_state(s1)

        data_keywords = ["DATA", "SQL", "PYTHON", "ETL", "PANDAS", "SPARK", "POWERBI"]

        for keyword in data_keywords:
            dfa.add_transition(s0, Symbol(keyword), s1)
            dfa.add_transition(s1, Symbol(keyword), s1)

        return dfa

    def accepts_token(self, token: str) -> bool:
        """Checks if a given token is accepted by the Data DFA."""
        symbols = [Symbol(w) for w in token.upper().split()]
        return self.data_dfa.accepts(symbols)