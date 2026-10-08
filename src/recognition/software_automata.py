from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State, Symbol

class SoftwareAutomata:
    """Contiene los autómatas de reconocimiento para perfiles de Software."""
    
    def __init__(self):
        self.fullstack_dfa = self._build_fullstack_dfa()
        self.backend_dfa = self._build_backend_dfa()

    def _build_fullstack_dfa(self) -> DeterministicFiniteAutomaton:
        dfa = DeterministicFiniteAutomaton()
        
        # 1. Estado inicial q0
        q0 = State("q0")
        dfa.add_start_state(q0)
        # Desde q0 (Frontend)
        dfa.add_transition(State("q0"), Symbol("JAVASCRIPT"), State("q1"))
        dfa.add_transition(State("q0"), Symbol("TYPESCRIPT"), State("q1"))
        
        dfa.add_transition(State("q1"), Symbol("REACT"), State("q2"))
        dfa.add_transition(State("q1"), Symbol("ANGULAR"), State("q2"))
        
        # Desde q2 (Backend)
        dfa.add_transition(State("q2"), Symbol("NODE_JS"), State("q3"))
        dfa.add_transition(State("q2"), Symbol("PYTHON"), State("q3"))
        
        # Desde q3 (Database & Tools)
        dfa.add_transition(State("q3"), Symbol("POSTGRESQL"), State("q4"))
        dfa.add_transition(State("q4"), Symbol("GIT"), State("q5"))
        
        # 3. Estado final de aceptación
        dfa.add_final_state(State("q5"))
        return dfa

    def _build_backend_dfa(self) -> DeterministicFiniteAutomaton:
        # Estructura similar enfocada exclusivamente en lógica de servidor y BD
        ...