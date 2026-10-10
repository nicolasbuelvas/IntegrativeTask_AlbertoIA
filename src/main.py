import os
from src.dsl.parser import DSLParser
from src.dsl.validators import validate_resume_model, DSLValidationError
from src.dsl.serializer import DSLSerializer

def run_pipeline(dsl_text_content: str) -> str:
    """
    Ejecuta el flujo completo de ResumeLens sobre una hoja de vida en texto DSL.
    
    1. Parsea el texto a un AST de Python.
    2. Aplica validaciones semánticas.
    3. Serializa de vuelta el modelo validado.
    """
    # 1. Parsear el texto usando la gramática
    parser = DSLParser()
    model = parser.parse_string(dsl_text_content)
    
    # 2. Validar reglas semánticas de negocio
    validate_resume_model(model)
    
    # 3. Serializar el AST validado de vuelta a formato DSL
    output_dsl = DSLSerializer.serialize_to_dsl(model)
    return output_dsl

def main():
    sample_candidate_dsl = """
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
    print("=== Ejecutando Pipeline de ResumeLens ===")
    try:
        result = run_pipeline(sample_candidate_dsl)
        print("\n[ÉXITO] Modelo procesado y serializado correctamente:")
        print("--------------------------------------------------")
        print(result)
        print("--------------------------------------------------")
    except DSLValidationError as e:
        print(f"\n[ERROR SEMÁNTICO]: {e}")
    except Exception as e:
        print(f"\n[ERROR DE SINTAXIS O PROCESAMIENTO]: {e}")

if __name__ == "__main__":
    main()