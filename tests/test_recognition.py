import pytest

## Para ejecutar los tests, abre la terminal y navega a la carpeta del proyecto. Luego, ejecuta el siguiente comando:
## cd "c:/Users/Danna/OneDrive/Escritorio/Semestre_6/Discretas III/semana 10/Integradora/IntegrativeTask_AlbertoIA"
## py -3.13 -m pytest tests/test_recognition.py -q
from src.recognition.data_automata import DataAutomata


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
