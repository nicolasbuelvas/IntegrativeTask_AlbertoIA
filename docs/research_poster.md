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
Automated resume screening is prone to high false-rejection rates due to lexical aliases (e.g., `JS` vs `JavaScript`) and opaque decisions from statistical models. We present **ResumeLens**, a deterministic screening framework founded entirely on formal language theory. ResumeLens pipelines candidate texts across four discrete computational models: (1) Chomsky Type-3 regular expressions for contact and entity extraction, (2) 7-tuple Finite-State Transducers (FST) for qualification normalization into canonical alphabets, (3) Deterministic Finite Automata (DFA) for profile pattern recognition over canonically sorted sequences, and (4) Context-Free Grammars (CFG) in EBNF via textX for structured profile modeling. Evaluated across synthetic multi-domain datasets, ResumeLens achieved 100% deterministic classification across 99 automated test cases without algorithmic bias or stochastic hallucinations.

---

### Section 2: Problem Statement & Motivation
- **Lexical Fragmentation**: The same technical competency takes multiple textual representations (`PostgreSQL`, `Postgres`, `postgres`).
- **Order Insensitivity in Naive Systems**: Unstructured keyword search ignores architectural hierarchies (e.g., requiring UI language $\to$ Framework $\to$ Server $\to$ Database).
- **Interpretability Deficit**: Deep learning recruiters lack formal auditability, introducing compliance risks and unexplained rejections.
- **Objective**: Develop a mathematically verifiable candidate screening engine that guarantees auditability and deterministic outcomes.

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
- **Determinism Proof**: $\forall q \in Q, a \in \Sigma, |\delta(q, a)| \le 1$; no $\varepsilon$-transitions.

#### 4. Context-Free Grammar (CFG)
$$G = (V_N, V_T, P, S)$$
- Formulates candidate data into typed Abstract Syntax Trees (AST) using textX.

---

### Section 5: Experimental Evaluation & Results

The system was evaluated against synthetic multi-role resumes with automated unit and E2E tests:

| Role Profile | Evaluated Sequence | Sorter Order | Automaton Verdict | Correctness |
|:---|:---|:---|:---:|:---:|
| **Full Stack** | `JS, React.js, Node, Postgres, Git` | Lang $\to$ UI $\to$ Srv $\to$ DB $\to$ VCS | **ACCEPTED** | Verified |
| **Full Stack (Missing Lang)** | `React.js, Node, Postgres, Git` | UI $\to$ Srv $\to$ DB $\to$ VCS | **REJECTED** | Verified |
| **Machine Learning** | `Python, Pandas, TensorFlow, SQL, Git` | Lang $\to$ ETL $\to$ Model $\to$ DB $\to$ VCS | **ACCEPTED** | Verified |
| **Machine Learning (No Model)**| `Python, Pandas, SQL, Git` | Lang $\to$ ETL $\to$ DB $\to$ VCS | **REJECTED** | Verified |
| **Backend Developer** | `Python, PostgreSQL, Git` | Lang $\to$ DB $\to$ VCS | **ACCEPTED** | Verified |
| **Data Engineer** | `Python, Apache Spark, SQL` | Lang $\to$ Engine $\to$ Warehouse | **ACCEPTED** | Verified |

---

### Section 6: Key Conclusions & Future Work
- **Mathematical Rigor**: Formal transducers and DFAs eliminate false rejections caused by naming variations without resorting to black-box models.
- **Auditability**: Every decision corresponds to a deterministic path through a finite state machine, allowing candidate feedback with exact missing transitions.
- **Future Improvements**:
  1. Integrating Context-Sensitive Grammars (Type-1) to model prerequisite experience years bound to specific technologies.
  2. Multi-language lexicons supporting Spanish and multilingual qualification synonyms.
