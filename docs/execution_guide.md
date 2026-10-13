# ResumeLens Execution Guide

## Requirements

- Python 3.10 or newer (`requires-python` in `pyproject.toml`).
- pip, included with a standard Python installation.
- Internet access for the first dependency installation.
- Run commands from the repository root unless an absolute resume path is provided.

The project declares `pyformlang>=1.0.10`, `textx>=3.1.0`, and `jinja2>=3.1.0`. Install the `dev` extra to add pytest.

## Installation

### Windows — PowerShell

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

If script execution is blocked by PowerShell policy, activate the environment from Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

The Windows, macOS, and Linux commands follow the platform’s standard venv and pip usage. The tests and CLI examples below were verified on Windows with the repository’s existing Python 3.13.0 virtual environment (`.venv`); `python -m src.main --demo`, the `summary` and `dsl` modes, and the full test suite were re-run for this revision. A from-scratch install with the exact `py -3.10` command, and macOS and Linux, were not re-run.

## Running the CLI

The actual entry point is `src.main`; there is no `src.cli` module. Check the options with:

```bash
python -m src.main --help
```

The parser accepts an optional resume path, `--format`/`-f` with `summary`, `dsl`, `html`, `markdown`, or `all`, `--output`/`-o`, and `--demo`. These commands were run from a temporary copy of the repository using the project’s existing environment.

### Summary mode

```bash
python -m src.main data/resumes/fullstack_valid.txt --format summary
python -m src.main data/resumes/backend_sample.txt --format summary
```

Observed Full Stack excerpt:

```text
CANDIDATE: Lina Marquez
TITLE:     Full Stack Engineer
EMAIL:     lina.marquez@example.com
NORMALIZED CANONICAL SKILLS (5):
  POSTGRESQL, REACT, GIT, JAVASCRIPT, NODE_JS
  Full Stack Developer           [ACCEPTED]
  Machine Learning Engineer      [REJECTED]
  Backend Developer              [ACCEPTED]
  Data Engineer                  [REJECTED]
```

Observed Backend excerpt:

```text
CANDIDATE: Sara Beltran
TITLE:     Backend Developer
EMAIL:     sara.beltran@example.com
NORMALIZED CANONICAL SKILLS (3):
  GIT, POSTGRESQL, PYTHON
  Backend Developer              [ACCEPTED]
```

If no resume path is supplied, the CLI selects `data/resumes/fullstack_valid.txt` relative to the installed source tree. For a supplied relative path, the path is interpreted from the current working directory.

### DSL mode

Print the serialized DSL:

```bash
python -m src.main data/resumes/fullstack_valid.txt --format dsl
```

Write it to a file in the current directory:

```bash
python -m src.main data/resumes/fullstack_valid.txt --format dsl --output fullstack.dsl
```

The second command writes to the exact path passed to `--output`. Its parent directory must already exist.

### HTML and Markdown modes

```bash
python -m src.main data/resumes/fullstack_valid.txt --format html --output output/fullstack.html
python -m src.main data/resumes/fullstack_valid.txt --format markdown --output output/fullstack.md
```

The commands were executed successfully. They printed `Wrote HTML report to output\fullstack.html` and `Wrote Markdown summary to output\fullstack.md` on Windows. The renderers create missing parent directories. If `--output` is omitted, the generated HTML or Markdown is printed to the console.

### Generate all artifacts

```bash
python -m src.main data/resumes/backend_sample.txt --format all --output output/backend
```

Observed files:

```text
output/backend_report.html
output/backend_summary.md
output/backend.dsl
```

Here, `output/backend` is a filename prefix. If `--output` is omitted, the CLI uses the input resume’s directory and filename as the prefix. In `summary` mode, specifying `--output` saves the DSL text; it does not save the printed summary.

### Batch demo

```bash
python -m src.main --demo
```

The demo processes files in sorted filename order and prints the accepted profiles. The verified run produced:

| Resume | Accepted profiles observed |
|:---|:---|
| `backend_sample.txt` | Backend Developer |
| `data_engineer_sample.txt` | Data Engineer |
| `fullstack_invalid.txt` | Backend Developer |
| `fullstack_valid.txt` | Full Stack Developer; Backend Developer |
| `ml_engineer_invalid.txt` | Backend Developer; Data Engineer |
| `ml_engineer_valid.txt` | Machine Learning Engineer; Backend Developer |

These are the current code’s observed outputs. Some resumes also match non-target profiles; acceptance is not an exclusive role label.

## Output locations

- HTML and Markdown: exactly the file path passed to `--output`; parent directories are created by the renderers.
- DSL: exactly the path passed to `--output`; create its parent directory first if needed.
- `all`: three files named `<prefix>_report.html`, `<prefix>_summary.md`, and `<prefix>.dsl` under the prefix’s parent directory.
- No `--output`: HTML/Markdown/DSL print to the console for their individual format. In `all`, artifacts are placed beside the input resume (or beside the default sample).
- Summary `--output`: writes the serialized DSL to that path.

## Tests

Run all tests from the repository root with:

```bash
python -m pytest -q
```

On this checkout, pytest collected 100 tests and all 100 passed. These focused commands were also run:

```bash
# Stage 1: extraction
python -m pytest -q tests/test_extraction.py

# Stage 2: normalization
python -m pytest -q tests/test_normalization.py

# Stage 3 and profile taxonomy
python -m pytest -q tests/test_recognition.py tests/test_taxonomy.py

# DSL, pipeline, and resume dataset integration
python -m pytest -q tests/test_dsl.py tests/test_pipeline.py tests/test_e2e_resumes.py

# HTML and Markdown reports
python -m pytest -q tests/test_visualization_html.py tests/test_visualization_md.py

# Runtime dependency check
python -m pytest -q tests/test_environment.py
```

The observed focused results were 15 extraction tests, 10 normalization tests, 14 recognition/taxonomy tests (9 recognition + 5 taxonomy), 44 DSL/pipeline/E2E tests (3 + 4 + 37), 16 visualization tests (10 HTML + 6 Markdown), and 1 environment test. The groups together cover all 100 tests.

To list tests without running them:

```bash
python -m pytest --collect-only -q
```

## Troubleshooting

1. **`ModuleNotFoundError: No module named 'src'` — possible cause.** Run from the repository root or install the package into the active virtual environment with `python -m pip install -e ".[dev]"`.
2. **`No module named src.cli` — anticipated entry-point mismatch.** This checkout has `src/main.py`, not `src/cli.py`; invoke `python -m src.main`.
3. **`ModuleNotFoundError` for `pyformlang`, `textx`, or `jinja2` — possible cause.** The dependencies are declared in `pyproject.toml`; activate the intended venv and install the project. Check `python -m pip show pyformlang textx jinja2`.
4. **Editable installation cannot fetch `setuptools>=61.0` — possible cause.** The editable install needs network access to the package index for the build backend. If pip reports a DNS or connection failure, retry when the connection is available.
5. **textX `TextXSyntaxError` — reproduced with malformed DSL.** The parser reported `None:1:19: Expected STRING => 'E_PROFILE *unquoted'` for `CANDIDATE_PROFILE unquoted`. Check quoted strings and the section order in `src/dsl/grammar/resume.tx`. The resume CLI accepts plain-text resumes; its DSL parser handles generated DSL internally.
6. **`UnicodeDecodeError` — possible cause.** `ResumeLensPipeline.process_file` reads input as UTF-8. Save the resume as UTF-8 and try again.
7. **`Resume file '…' not found` — reproduced with a missing relative path.** Relative input paths are resolved from the current working directory. Check the filename or pass an absolute path.
8. **A non-target profile is also accepted — reproduced in `--demo`.** Some current automata accept broader token sequences than the dataset’s intended target; for example, the Backend automaton accepts any `language → database → tool` sequence. This guide reports the actual output.
9. **`Error processing resume ...: Resume missing required candidate name or email contact information.` — reproduced.** The pipeline needs both a name and an email. Put the name on its own line near the top (two to four capitalized words) and include an email address.
10. **`TextXSyntaxError ... Expected STRING => ' SKILLS:  *EVALUATION'` when processing a resume — reproduced.** The resume contained a name and email but no skill that the extractor and transducers recognize, and the grammar requires at least one skill. Add a supported skill spelled as listed in `src/normalization/skill_transducers.py`; see also “Known limitations” in the README.
11. **A skill is in the resume but missing from `NORMALIZED CANONICAL SKILLS` — reproduced.** The extraction regexes are case-insensitive, but the transducers only know the exact spellings in `src/normalization/skill_transducers.py`. For example, `PYTHON`, `REACT`, `Node JS`, and `RESTful APIs` are extracted but not normalized; `Python`, `React`, `Node.js`, and `REST APIs` are.
9. **Output file cannot be written — possible cause.** Check the destination path and permissions. For DSL-only mode, create the parent directory before passing a nested `--output` path.
