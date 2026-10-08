"""Formal Finite-State Transducer (FST) builder and 7-tuple representation.

Models 7-tuples: M = (Q, Sigma, Gamma, delta, omega, q0, F) using pyformlang.
"""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

from pyformlang.finite_automaton import State
from pyformlang.fst import FST


@dataclass(frozen=True)
class Transducer7Tuple:
    """Mathematical 7-tuple representation of a Finite-State Transducer.

    M = (Q, Sigma, Gamma, delta, omega, q0, F)
    """

    states: Set[State]
    input_alphabet: Set[str]
    output_alphabet: Set[str]
    transitions: Dict[Tuple[State, str], State]
    outputs: Dict[Tuple[State, str], List[str]]
    start_state: State
    final_states: Set[State]

    @property
    def Q(self) -> Set[State]:
        """Finite set of states."""
        return self.states

    @property
    def Sigma(self) -> Set[str]:
        """Finite input alphabet."""
        return self.input_alphabet

    @property
    def Gamma(self) -> Set[str]:
        """Finite output alphabet."""
        return self.output_alphabet

    @property
    def delta(self) -> Dict[Tuple[State, str], State]:
        """Transition relation delta: (state, input_sym) -> next_state."""
        return self.transitions

    @property
    def omega(self) -> Dict[Tuple[State, str], List[str]]:
        """Output relation omega: (state, input_sym) -> output_symbols."""
        return self.outputs

    @property
    def q0(self) -> State:
        """Initial state."""
        return self.start_state

    @property
    def F(self) -> Set[State]:
        """Set of accepting / final states."""
        return self.final_states

    def as_tuple(self) -> Tuple[Set[State], Set[str], Set[str], Dict, Dict, State, Set[State]]:
        """Return the mathematical 7-tuple (Q, Sigma, Gamma, delta, omega, q0, F)."""
        return (
            self.Q,
            self.Sigma,
            self.Gamma,
            self.delta,
            self.omega,
            self.q0,
            self.F,
        )


class TransducerBuilder:
    """Builder for constructing formal finite-state transducers using pyformlang."""

    def __init__(self, name: str = "Transducer") -> None:
        self.name = name
        self._fst = FST()
        self._q0: State = State("q0")
        self._fst.add_start_state(self._q0)

        self._states: Set[State] = {self._q0}
        self._input_alphabet: Set[str] = set()
        self._output_alphabet: Set[str] = set()
        self._final_states: Set[State] = set()
        self._transitions: Dict[Tuple[State, str], State] = {}
        self._outputs: Dict[Tuple[State, str], List[str]] = {}
        self._transition_list: List[Tuple[State, str, State, List[str]]] = []
        self._mapping_index: int = 0

    def _ensure_state(self, state: State | str) -> State:
        """Coerce string or State into State instance and register in state set."""
        st = state if isinstance(state, State) else State(str(state))
        self._states.add(st)
        return st

    def set_start_state(self, state: State | str) -> "TransducerBuilder":
        """Set the initial state q0."""
        st = self._ensure_state(state)
        self._q0 = st
        self._fst.add_start_state(st)
        return self

    def add_state(self, state: State | str) -> "TransducerBuilder":
        """Register a state in Q."""
        self._ensure_state(state)
        return self

    def add_final_state(self, state: State | str) -> "TransducerBuilder":
        """Register a state in F (final / accepting states)."""
        st = self._ensure_state(state)
        self._final_states.add(st)
        self._fst.add_final_state(st)
        return self

    def add_transition(
        self,
        source: State | str,
        input_symbol: str,
        target: State | str,
        output_symbols: Optional[Sequence[str]] = None,
    ) -> "TransducerBuilder":
        """Add a transition step (source, input_symbol) -> (target, output_symbols)."""
        src = self._ensure_state(source)
        tgt = self._ensure_state(target)
        outs = list(output_symbols) if output_symbols is not None else []

        self._input_alphabet.add(input_symbol)
        for sym in outs:
            self._output_alphabet.add(sym)

        self._transitions[(src, input_symbol)] = tgt
        self._outputs[(src, input_symbol)] = outs

        transition_tuple = (src, input_symbol, tgt, outs)
        self._transition_list.append(transition_tuple)
        self._fst.add_transitions([transition_tuple])
        return self

    def add_word_mapping(
        self,
        variant: str,
        canonical: str,
        branch_id: Optional[str] = None,
    ) -> "TransducerBuilder":
        """Add a character-by-character recognition branch for variant string to canonical."""
        if not variant:
            return self

        self._mapping_index += 1
        prefix = branch_id if branch_id is not None else f"b{self._mapping_index}"
        chars = list(variant)
        current_state = self._q0

        for idx, char in enumerate(chars):
            is_last = idx == len(chars) - 1
            next_state_name = f"{prefix}_{idx + 1}"
            next_state = self._ensure_state(next_state_name)

            if is_last:
                self.add_final_state(next_state)
                output = [canonical]
            else:
                output = []

            self.add_transition(current_state, char, next_state, output)
            current_state = next_state

        return self

    def add_batch_mappings(self, mappings: Dict[str, str]) -> "TransducerBuilder":
        """Add multiple variant -> canonical word mappings."""
        for variant, canonical in mappings.items():
            self.add_word_mapping(variant, canonical)
        return self

    def build(self) -> FST:
        """Return the compiled pyformlang FST object."""
        return self._fst

    def get_formal_tuple(self) -> Transducer7Tuple:
        """Return the formal 7-tuple M = (Q, Sigma, Gamma, delta, omega, q0, F)."""
        return Transducer7Tuple(
            states=set(self._states),
            input_alphabet=set(self._input_alphabet),
            output_alphabet=set(self._output_alphabet),
            transitions=dict(self._transitions),
            outputs=dict(self._outputs),
            start_state=self._q0,
            final_states=set(self._final_states),
        )

    def translate_word(self, word: str) -> Optional[str]:
        """Translate a single input string through the transducer."""
        if not word:
            return None
        input_symbols = list(word)
        try:
            results = list(self._fst.translate(input_symbols))
        except Exception:
            return None

        if not results:
            return None

        first_result = results[0]
        if not first_result:
            return ""
        return "".join(first_result)

    def translate_tokens(self, tokens: Iterable[str]) -> List[str]:
        """Translate an iterable of words, keeping unmapped tokens unchanged."""
        normalized: List[str] = []
        for token in tokens:
            result = self.translate_word(token)
            normalized.append(result if result is not None else token)
        return normalized

    def to_dot(self) -> str:
        """Export the transducer state graph to Graphviz DOT format."""
        lines = [f"digraph {self.name} {{", '    rankdir=LR;', '    node [shape=circle];']

        for fs in self._final_states:
            lines.append(f'    "{fs.value}" [shape=doublecircle];')

        lines.append(f'    __start__ [shape=point, style=invis];')
        lines.append(f'    __start__ -> "{self._q0.value}";')

        for src, sym, tgt, outs in self._transition_list:
            out_str = "".join(outs) if outs else "ε"
            lines.append(f'    "{src.value}" -> "{tgt.value}" [label="{sym} / {out_str}"];')

        lines.append("}")
        return "\n".join(lines)
