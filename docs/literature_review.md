# Literature Review: Formal Language Models in Automated Resume Screening

Universidad Icesi  
Curso: Estructuras Discretas III (CyED III, Código 09772)  
Proyecto Integrador: ResumeLens  
Equipo: Nicolás Santiago Buelvas González, Daniel Alexander Nastul Flórez, Albert Valencia Escobar  
Profesor: Andrés Aristizábal (Grupo 3)

---

## 1. Introduction and Problem Context

Automated resume screening is a critical component of modern talent acquisition systems. Traditional approaches frequently rely on keyword searching (which is fragile and susceptible to lexical variations) or deep neural language models (which introduce non-deterministic hallucinations, algorithmic bias, and high computational latency).

ResumeLens establishes a mathematically grounded alternative using formal language theory and automata. By decomposing candidate analysis into formal grammatical hierarchies, the system achieves predictable, auditable, and transparent screening without opaque heuristics.

---

## 2. Review of Formal Models in Text Processing

### 2.1 Information Extraction via Regular Expressions
Regular expressions (Chomsky Type-3 grammars) provide the theoretical foundation for deterministic token recognition. In technical resume processing, contact information (RFC 5322 emails, E.164 phone formats, URL slugs) and technology mentions possess regular lexical structures (Hopcroft, Motwani, & Ullman, 2006). Compiling regular patterns with boundary anchors ($\backslash b$) ensures precise entity identification with $\mathcal{O}(n)$ processing time relative to candidate resume length.

### 2.2 Token Normalization using Finite-State Transducers (FST)
In natural language processing and morphological analysis, Finite-State Transducers (Mohri, 1997; Roche & Schabes, 1997) are standard tools for mapping sequences of characters to standardized representations. Unlike conventional hash tables or dictionaries, FSTs model prefix sharing and sequential transformation directly through a 7-tuple:

$$M = (Q, \Sigma, \Gamma, \delta, \omega, q_0, F)$$

In ResumeLens, FSTs normalize diverse lexical aliases (e.g. `JS`, `React.js`, `postgres`) into canonical alphabet tokens (`JAVASCRIPT`, `REACT`, `POSTGRESQL`). This decouples downstream classification from surface text spelling differences.

### 2.3 Sequential Pattern Recognition via Deterministic Finite Automata (DFA)
A recognized limitation of standard keyword matching is order-insensitivity. Professional job profiles possess conceptual dependencies (e.g., UI language $\to$ UI library $\to$ backend runtime $\to$ persistence). By applying a canonical ordering algorithm based on category priority, qualifications are structured as formal words over an alphabet $\Sigma_{profile}$. 

Deterministic Finite Automata (Aho, Lam, Sethi, & Ullman, 2006) then accept or reject candidate qualification words based on state transitions, providing clear mathematical proofs of candidate eligibility without scoring ambiguity.

### 2.4 Structured Document Modeling with Context-Free Grammars (CFG) and DSLs
Domain-Specific Languages (DSLs) backed by Context-Free Grammars (Type-2 in the Chomsky hierarchy) allow high-level declarative modeling of domain problems (Fowler, 2010). Modern parser generators like textX (Dejanović et al., 2017) derive meta-models directly from Extended Backus-Naur Form (EBNF) specifications, generating typed Abstract Syntax Trees (ASTs). In ResumeLens, textX guarantees that candidate profiles adhere to strict structural schemas before HTML and Markdown rendering.

---

## 3. Comparative Summary

| Paradigm | Interpretability | Determinism | Computational Complexity | Susceptibility to Noise |
|:---|:---:|:---:|:---:|:---:|
| **Keyword Search** | High | Low | $\mathcal{O}(n)$ | Very High (spelling variants missed) |
| **LLMs / Neural NLP** | Extremely Low | Low (stochastic) | $\mathcal{O}(n^2)$ / High GPU cost | Vulnerable to prompt injection |
| **Formal Automata (ResumeLens)** | **100% (Mathematical proof)** | **100% Deterministic** | $\mathcal{O}(n)$ Linear | **Low (Normalized by FST)** |

---

## 4. References

1. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Addison-Wesley.
2. Dejanović, I., Vaderna, R., Milosavljević, G., & Vuković, Ž. (2017). *textX: A Python tool for Domain-Specific Language implementation*. Knowledge-Based Systems, 115, 1-4.
3. Fowler, M. (2010). *Domain-Specific Languages*. Addison-Wesley Professional.
4. Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.). Pearson.
5. Mohri, M. (1997). *Finite-State Transducers in Language and Speech Processing*. Computational Linguistics, 23(2), 269–311.
6. Roche, E., & Schabes, Y. (1997). *Finite-State Language Processing*. MIT Press.
