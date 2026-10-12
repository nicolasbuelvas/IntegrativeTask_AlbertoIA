# ResumeLens: Formal Language-Based Resume Screening

Proyecto Integrador - Estructuras Discretas III (CyED III, Código 09772)  
Universidad Icesi, Semestre 2026-2  
Profesor: Andrés Aristizábal (Grupo 3)

---

## 1. Integrantes del Equipo

- Nicolás Santiago Buelvas González
- Daniel Alexander Nastul Flórez
- Albert Valencia Escobar

Entorno de desarrollo principal: Visual Studio Code / Cursor  
Gestor de paquetes y entorno virtual: `uv`  
Intérprete base: Python 3.11+

---

## 2. Descripción General del Sistema

ResumeLens es un sistema formal para el análisis y clasificación de hojas de vida basadas en texto plano. En lugar de utilizar modelos heurísticos o de lenguaje estadístico opacos, el sistema implementa una arquitectura rigurosa dividida en 5 etapas fundamentadas en la teoría de lenguajes formales y autómatas:

1. **Extracción Léxica (Expresiones Regulares)**: Identificación de metadatos de contacto (nombre, correo electrónico, teléfono, LinkedIn, GitHub) y extracción de menciones crudas de habilidades tecnológicas mediante patrones regulares compilados con `re`.
2. **Normalización de Cualificaciones (Transductores de Estados Finitos - FST)**: Mapeo formal 7-tupla implementado con `pyformlang` que convierte variaciones léxicas y sinónimos (e.g. `JS`, `React.js`, `postgres`) en símbolos canónicos unificados (`JAVASCRIPT`, `REACT`, `POSTGRESQL`). Incluye ordenamiento canónico determinista por jerarquía de rol.
3. **Reconocimiento de Patrones (Autómatas Finitos Deterministas - DFA)**: Clasificación de perfiles profesionales mediante autómatas que evalúan si la secuencia ordenada de cualificaciones canónicas satisface los patrones definidos para el rol.
4. **Especificación en DSL (Gramáticas Libres de Contexto - CFG con textX)**: Generación, validación sintáctica/semántica y serialización del perfil resultante en un lenguaje de dominio específico definido en EBNF.
5. **Visualización y Reportes**: Generación de documentos finales en HTML autocontenido (con estilos CSS integrados) y Markdown estructurado a partir del AST validado.

---

## 3. Perfiles Profesionales Soportados

El sistema soporta cuatro perfiles evaluados de forma simultánea e independiente:

1. **Full Stack Developer** (Predefinido): Requiere lenguajes frontend, frameworks frontend, frameworks backend, bases de datos y herramientas de control de versiones.
2. **Machine Learning Engineer** (Predefinido): Requiere lenguaje Python, librerías de manipulación de datos (Pandas/NumPy), frameworks de deep learning/ML (Scikit-Learn/TensorFlow), SQL y Git.
3. **Backend Developer** (Selección del equipo - Software Engineering): Enfocado en lenguajes de servidor, frameworks backend, bases de datos relacionales/NoSQL y arquitecturas API.
4. **Data Engineer** (Selección del equipo - AI/Data): Enfocado en computación distribuida (Spark), orquestación y bases de datos analíticas.

---

## 4. Instalación y Requisitos

El proyecto utiliza `uv` como gestor de paquetes y dependencias.

### Prerrequisitos
- Python 3.11 instalado en el sistema.
- `uv` instalado (`pip install uv` o mediante el instalador oficial).

### Configuración del entorno
Clonar el repositorio y sincronizar el entorno virtual:

```bash
git clone https://github.com/nicolasbuelvas/IntegrativeTask_AlbertoIA.git
cd IntegrativeTask_AlbertoIA
uv sync
```

---

## 5. Guía de Uso de la Interfaz de Línea de Comandos (CLI)

El punto de entrada principal es el módulo `src.main`.

### Ejecución básica (Resumen en consola)
Procesa una hoja de vida en texto plano y muestra la extracción, normalización y resultados de clasificación por autómata:

```bash
uv run python -m src.main data/resumes/fullstack_valid.txt
```

### Generación de reporte HTML
Genera un archivo HTML visualmente enriquecido con el resultado del análisis:

```bash
uv run python -m src.main data/resumes/fullstack_valid.txt --format html --output output/reporte_lina.html
```

### Generación de resumen Markdown
Genera el reporte estructurado en formato Markdown:

```bash
uv run python -m src.main data/resumes/fullstack_valid.txt --format markdown --output output/resumen_lina.md
```

### Exportación del modelo en formato DSL
Exporta la especificación formal del candidato en la gramática de ResumeLens (`.dsl`):

```bash
uv run python -m src.main data/resumes/fullstack_valid.txt --format dsl --output output/candidato.dsl
```

### Generación de todos los artefactos simultáneamente
Genera el resumen por consola y guarda los 3 archivos (`.html`, `.md`, `.dsl`) a la vez:

```bash
uv run python -m src.main data/resumes/fullstack_valid.txt --format all --output output/resultado_completo
```

### Modo Demostración (Batch sobre el dataset)
Ejecuta la clasificación sobre todas las hojas de vida sintéticas ubicadas en `data/resumes/` y presenta una tabla comparativa de estados:

```bash
uv run python -m src.main --demo
```

---

## 6. Ejecución de Pruebas Automatizadas

La suite de pruebas automatizadas está construida sobre `pytest` y cubre pruebas unitarias de cada etapa formal, pruebas de gramática y pruebas de integración extremo a extremo:

```bash
uv run pytest
```

Para ejecutar pruebas con detalle de cobertura y ejecución verbosa:

```bash
uv run pytest -v
```

---

## 7. Estructura del Repositorio

```text
IntegrativeTask_AlbertoIA/
├── data/
│   └── resumes/                     # Dataset sintético de hojas de vida (.txt)
├── docs/
│   ├── formal_transducers.md        # Especificaciones formales 7-tuplas de FST
│   └── formal_automata.md           # Especificaciones formales 5-tuplas de DFA
├── src/
│   ├── config/                      # Taxonomía canónica y alfabetos de perfiles
│   ├── dsl/                         # Gramática textX (resume.tx), parser y serializador
│   ├── extraction/                  # Extractores basados en expresiones regulares
│   ├── models/                      # Clases de dominio y dataclasses
│   ├── normalization/               # Transductores FST y pipeline de normalización
│   ├── recognition/                 # Autómatas DFA para clasificación de perfiles
│   ├── visualization/               # Renderers HTML (Jinja2) y Markdown
│   ├── pipeline.py                  # Orquestador del flujo formal completo
│   └── main.py                      # Interfaz de línea de comandos (CLI)
├── tests/                           # Suite completa de pruebas con pytest (99 tests)
├── pyproject.toml                   # Configuración del proyecto y dependencias
├── requirements.txt                 # Exportación estándar de dependencias
└── README.md                        # Documentación general y guía de ejecución
```
