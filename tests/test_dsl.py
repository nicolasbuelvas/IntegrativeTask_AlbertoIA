import pytest
from textx.exceptions import TextXSyntaxError
from src.dsl.parser import DSLParser
from src.dsl.validators import validate_resume_model, DSLValidationError
from src.dsl.serializer import DSLSerializer

# Ejemplo de hoja de vida válida en formato DSL
VALID_DSL_SAMPLE = """
CANDIDATE_PROFILE "Daniel Nastul"
TITLE: "Software Developer"
CONTACT
email= "daniel@example.com"
EXPERIENCE:
- "Backend Developer" at "Tech Corp" (2 years)
EDUCATION:
- "Systems Engineering" from "Universidad Icesi"
SKILLS: "PYTHON", "POSTGRESQL", "GIT"
EVALUATIONS:
"Backend Developer" : ACCEPTED
"Machine Learning Engineer" : REJECTED
"""

# Ejemplo con correo sin '@' (inválido semánticamente)
INVALID_EMAIL_DSL = """
CANDIDATE_PROFILE "Daniel Nastul"
TITLE: "Software Developer"
CONTACT
email= "daniel_sin_arroba.com"
EXPERIENCE:
EDUCATION:
SKILLS: "PYTHON"
EVALUATIONS:
"Backend Developer" : ACCEPTED
"""

def test_dsl_parsing_and_serialization():
    parser = DSLParser()
    model = parser.parse_string(VALID_DSL_SAMPLE)
    
    # 1. Verificación del AST generado por textX
    assert model.name == "Daniel Nastul"
    assert model.contact.email == "daniel@example.com"
    assert len(model.skills) == 3
    assert len(model.evaluations) == 2
    
    # 2. Verificación de reglas semánticas
    assert validate_resume_model(model) is True
    
    # 3. Verificación de la reconversión a texto DSL (Serialización)
    serialized_text = DSLSerializer.serialize_to_dsl(model)
    assert 'CANDIDATE_PROFILE "Daniel Nastul"' in serialized_text
    assert 'email= "daniel@example.com"' in serialized_text

def test_dsl_semantic_validation_failure():
    parser = DSLParser()
    model = parser.parse_string(INVALID_EMAIL_DSL)
    
    # Debe arrojar DSLValidationError al no tener '@'
    with pytest.raises(DSLValidationError):
        validate_resume_model(model)

def test_dsl_syntax_error():
    parser = DSLParser()
    bad_syntax_dsl = "CANDIDATE_PROFILE texto_sin_formato_ni_comillas"
    
    # textX debe arrojar TextXSyntaxError por sintaxis incorrecta
    with pytest.raises(TextXSyntaxError):
        parser.parse_string(bad_syntax_dsl)