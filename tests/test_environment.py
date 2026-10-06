import pytest


def test_required_libraries_available():
    import pyformlang
    import textx
    from pyformlang.fst import FST
    from pyformlang.finite_automaton import DeterministicFiniteAutomaton

    assert pyformlang is not None
    assert textx is not None
    assert FST is not None
    assert DeterministicFiniteAutomaton is not None
