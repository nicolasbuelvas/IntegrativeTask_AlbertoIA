# Research Poster Content: ResumeLens

Universidad Icesi — Departamento de Tecnologías de Información y Comunicaciones  
Curso: Estructuras Discretas III (CyED III, Código 09772)  
Autores: Nicolás Santiago Buelvas González, Daniel Alexander Nastul Flórez, Albert Valencia Escobar  
Profesor: Andrés Aristizábal  
Fecha: Octubre 2026  

---

## Poster Title:
**ResumeLens: Formal Language-Based Resume Screening Using Transducers, Automata, and Context-Free Grammars**

---

### Section 1: Abstract
Automated resume screening can be affected by lexical variation and opaque decision rules. **ResumeLens** is an educational prototype that applies formal-language techniques: regular expressions for extraction, finite-state transducers (FSTs) for skill normalization, finite automata for profile recognition, and a textX grammar for structured resume data. On this checkout, `pytest` collects 94 tests and the six synthetic-resume end-to-end cases include a check that repeated runs produce identical DSL output. These tests do not establish real-world classification accuracy, fairness, or absence of bias. The classifier can accept a resume for more than one profile.

---

### Section 2: Problem Statement & Motivation
- **Lexical Fragmentation**: The same technical competency takes multiple textual representations (`PostgreSQL`, `Postgres`, `postgres`).
- **Order Insensitivity in Naive Systems**: Unstructured keyword search ignores architectural hierarchies (e.g., requiring UI language $\to$ Framework $\to$ Server $\to$ Database).
- **Interpretability Deficit**: Deep learning recruiters lack formal auditability, introducing compliance risks and unexplained rejections.
- **Objective**: Build a small, inspectable prototype whose rule-based decisions can be traced through the implemented extraction, normalization, and automata stages.

---

### Section 3: Formal Methodology & Pipeline

```text
+-----------------------+     +-------------------------------+     +--------------------------------+
|  Raw Plain-Text CV    | --> | Stage 1: Extraction (Regex)   | --> | Stage 2: Normalization (FST)   |
|  (ASCII / Unicode)    |     | Entities & Surface Tokens     |     | M = (Q, Σ, Γ, δ, ω, q0, F)     |
+-----------------------+     +-------------------------------+     +--------------------------------+
                                                                                    |
                                                                                    v
+-----------------------+     +-------------------------------+     +--------------------------------+
|  Final Visual Reports | <-- | Stage 4: DSL Specification    | <-- | Stage 3: Recognition (DFA)     |
|  (HTML / Markdown)    |     | CFG / EBNF via textX          |     | M = (Q, Σ, δ, q0, F)           |
+-----------------------+     +-------------------------------+     +--------------------------------+
```

---

### Section 4: Mathematical Models

#### 1. Normalization Transducers (FST 7-tuple)
$$M = (Q, \Sigma, \Gamma, \delta, \omega, q_0, F)$$
- **Input Alphabet ($\Sigma$)**: Raw characters $\{ \text{A-Z}, \text{a-z}, \text{0-9}, '.', '-', '\_', '\ ' \}$
- **Output Alphabet ($\Gamma$)**: Canonical tokens $\{ \text{JAVASCRIPT}, \text{REACT}, \text{POSTGRESQL}, \text{SCIKIT\_LEARN}, \dots \}$
- **Emission Function**: $\omega(q, c) = \varepsilon$ for prefix transitions; $\omega(q_{end}, c) = K \in \Gamma$ upon reaching final state.

#### 2. Canonical Ordering Hierarchy
To achieve order invariance relative to the raw resume layout:
$$\text{Sort}(S, P) = \text{order by } (\text{Priority}(\text{Category}(s, P)), s) \quad \forall s \in (S \cap \Sigma_P)$$

#### 3. Classification Automata (DFA 5-tuple)
$$M_{profile} = (Q, \Sigma, \delta, q_0, F)$$
- Evaluates the ordered sequence against strict role dependencies.
- **Automata property**: The documented profile machines are classified from their actual transition structures. This describes the machines, not a proof of end-to-end fairness or correctness.

#### 4. Context-Free Grammar (CFG)
$$G = (V_N, V_T, P, S)$$
- Formulates candidate data into typed Abstract Syntax Trees (AST) using textX.

---

### Section 5: Experimental Evaluation & Results

The repository has six fictional resume files and 94 collected tests on this checkout. The table below summarizes the accepted profiles observed when the CLI processed the dataset; these are implementation outputs, not accuracy scores or fairness measurements.

| Synthetic resume | Accepted profile(s) observed |
|:---|:---|
| `fullstack_valid.txt` | Full Stack Developer; Backend Developer |
| `fullstack_invalid.txt` | Backend Developer |
| `backend_sample.txt` | Backend Developer |
| `ml_engineer_valid.txt` | Machine Learning Engineer; Backend Developer |
| `ml_engineer_invalid.txt` | Backend Developer; Data Engineer |
| `data_engineer_sample.txt` | Data Engineer |

---

### Section 6: Key Conclusions & Future Work
- **Implemented approach**: Transducers map supported skill variants to canonical tokens, and finite automata classify the resulting sequence according to the configured rules.
- **Scope of evidence**: The tests exercise synthetic examples and software behavior. They do not demonstrate broad resume coverage, lower false-rejection rates, candidate suitability, or unbiased outcomes. Observed acceptance of non-target profiles shows that profile overlap remains a limitation.
- **Future Improvements**:
  1. Integrating Context-Sensitive Grammars (Type-1) to model prerequisite experience years bound to specific technologies.
  2. Multi-language lexicons supporting Spanish and multilingual qualification synonyms.
