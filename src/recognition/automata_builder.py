from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State, Symbol

class ProfileAutomatonBuilder:
    
    def __init__(self):
        self.dfa = DeterministicFiniteAutomaton()

    def build_automaton(self, start_state: str, transitions: list, final_states: list) -> DeterministicFiniteAutomaton:
        # 1. Estado inicial q0
        self.dfa.add_start_state(State(start_state))        
        # 2. Función de transición delta
        for src, symbol, dst in transitions:
            self.dfa.add_transition(State(src), Symbol(symbol), State(dst))
        # 3. Conjunto de estados finales F
        for final in final_states:
            self.dfa.add_final_state(State(final))
        return self.dfa