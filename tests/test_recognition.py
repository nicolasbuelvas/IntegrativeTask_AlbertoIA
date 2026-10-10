import pytest

from src.recognition.data_automata import DataAutomata
from src.recognition.software_automata import SoftwareAutomata

@pytest.mark.parametrize(
    "sequence",
    [
        ["PYTHON", "PANDAS", "TENSORFLOW", "SQL", "GIT"],
        ["PYTHON", "NUMPY", "SCIKIT_LEARN", "SQL", "GIT"],
    ],
)
def test_ml_automata_accepts_valid_sequences(sequence):
    automata = DataAutomata()

    assert automata.ml_dfa.accepts(sequence) is True


@pytest.mark.parametrize(
    "sequence",
    [
        ["PYTHON", "PANDAS"],
        ["PANDAS", "PYTHON", "TENSORFLOW", "SQL", "GIT"],
        ["PYTHON", "TENSORFLOW", "PANDAS", "SQL", "GIT"],
        ["PYTHON", "PANDAS", "SQL", "GIT"],
    ],
)
def test_ml_automata_rejects_invalid_sequences(sequence):
    automata = DataAutomata()

    assert automata.ml_dfa.accepts(sequence) is False


def test_data_automata_acceptance():
    automaton = DataAutomata()
    assert automaton.accepts_token("PYTHON") is True
    assert automaton.accepts_token("SQL") is True
    assert automaton.accepts_token("MARKETING") is False

def test_software_automata_acceptance():
    automaton = SoftwareAutomata()
    assert automaton.accepts_backend_token("BACKEND") is True
    assert automaton.accepts_backend_token("POSTGRESQL") is True
    assert automaton.accepts_backend_token("COOKING") is False
