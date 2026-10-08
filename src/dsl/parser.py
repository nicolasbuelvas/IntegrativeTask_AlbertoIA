import os
from textx import metamodel_from_file

class DSLParser:
    def __init__(self, grammar_path: str = None):
        if grammar_path is None:
            # Ruta por defecto a la gramática resume.tx
            base_dir = os.path.dirname(os.path.dirname(__file__))
            grammar_path = os.path.join(base_dir, "dsl", "grammar", "resume.tx")
            
        # Genera el meta-modelo a partir del archivo .tx
        self.metamodel = metamodel_from_file(grammar_path)

    def parse_file(self, file_path: str):
        """Lee un archivo de texto y retorna el AST (objeto Python)."""
        return self.metamodel.model_from_file(file_path)

    def parse_string(self, text_content: str):
        """Parsea directamente una cadena de texto en formato DSL."""
        return self.metamodel.model_from_str(text_content)