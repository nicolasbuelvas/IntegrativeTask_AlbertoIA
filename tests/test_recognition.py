import pytest
from src.recognition.data_automata import DataAutomata
from src.recognition.software_automata import SoftwareAutomata

def test_data_automata_canonical_order():
    automaton = DataAutomata()
    # Orden válido: Rol -> Core -> Processing -> Storage
    assert automaton.accepts_token("DATA PYTHON PANDAS POWERBI") is True
    assert automaton.accepts_token("DATA_ENGINEER SQL ETL SNOWFLAKE") is True
    
    # Orden desordenado / Inválido: Storage -> Rol -> Processing
    assert automaton.accepts_token("POWERBI DATA PANDAS") is False

def test_software_automata_canonical_order():
    automaton = SoftwareAutomata()
    # Orden válido: Rol -> Language -> Database -> Tool
    assert automaton.accepts_backend_token("BACKEND PYTHON POSTGRESQL GIT") is True
    assert automaton.accepts_backend_token("SOFTWARE_ENGINEER JAVA SPRING MYSQL DOCKER") is True
    
    # Orden desordenado / Inválido: Database -> Rol -> Language
    assert automaton.accepts_backend_token("POSTGRESQL BACKEND PYTHON") is False

def test_fullstack_automata_canonical_order():
    automaton = SoftwareAutomata()
    # Orden válido con variantes (React o Vue, Python o Django)
    assert automaton.accepts_fullstack_token("FULLSTACK REACT DJANGO POSTGRESQL GIT") is True
    assert automaton.accepts_fullstack_token("FULLSTACK_DEVELOPER VUE SPRING_BOOT MYSQL DOCKER") is True
    
    # Orden desordenado / Inválido
    assert automaton.accepts_fullstack_token("POSTGRESQL REACT FULLSTACK") is False