# Formal Methods for Resume Analysis: A Short Literature Review

Universidad Icesi  
Curso: Estructuras Discretas III (CyED III, Código 09772)  
Proyecto Integrador: ResumeLens  
Equipo: Nicolás Santiago Buelvas González, Daniel Alexander Nastul Flórez, Albert Valencia Escobar  
Profesor: Andrés Aristizábal (Grupo 3)

---

## 1. The problem

A resume contains information that can help determine whether a candidate may fit a job. However, resumes use different layouts and wording. The same skill may appear with different spellings, and useful details may be placed in different sections. A screening program must first find and organize information, then compare it with the profiles or requirements it knows.

Finding a word does not prove that someone has a skill, and failing to find it does not prove that they do not. Automated screening can also affect who gets an interview. Raghavan et al. (2020) study algorithmic hiring assessments and explain why their data, goals, and fairness claims should be examined carefully.

This review connects those issues to ResumeLens, a university project that uses regular expressions, finite-state transducers, automata, and a small domain-specific language (DSL). It is an academic demonstration, not a validated hiring system.

## 2. Approaches to resume screening

### Rules and keywords

A rule searches for a pattern specified by a programmer, such as an email address or the name of a technology. Rules are relatively easy to inspect: we can see which pattern matched. Given the same input and rules, the result is repeatable.

Rules only find patterns that have been included. A skill written in an unexpected way may be missed. A word match can also be misleading if the resume mentions a skill in a negative or unrelated context. Lin et al. (2016) describe rule-based and manually weighted approaches as an alternative to systems that learn to match resumes and jobs from examples.

### Machine learning

Machine-learning systems learn patterns from examples instead of requiring every decision to be written as a separate rule. Lin et al. (2016) describe a resume-job matching approach that combines resume features, classifiers, and aggregated predictions. This can identify patterns that were not written as individual rules, but it depends on suitable data and a clearly defined prediction goal.

A model can repeat problems found in its training examples. It should be evaluated on separate data, and its errors should be examined. Learning from data does not guarantee that a score is fair or measures a person’s actual ability.

### Deep learning and language models

Bhatia et al. (2019) present a system that uses heuristics to organize resume sections and BERT to classify text and compare work experience with job descriptions. Unlike an exact keyword search, BERT can use the surrounding words as context. However, the reported results apply to that study’s data and evaluation; they do not guarantee the same performance with other formats or groups.

Language models can summarize text and answer questions, but a fluent answer is not necessarily supported by the resume. In hiring, their output would need testing and human review. Raghavan et al. (2020) also emphasize that fairness depends on choices about data and prediction goals, not just on the model itself.

## 3. Formal methods used in ResumeLens

### Regular expressions and finite automata

A regular expression describes a text pattern, such as the general structure of an email address. A finite automaton can check whether an input follows a defined pattern. For a given input and automaton, we can follow its states and see why it accepted or rejected the input.

ResumeLens uses regular expressions to extract information and automata to recognize profiles from normalized skills. This is useful when the patterns are known, but it does not understand sentence meaning. For example, a skill mentioned in a negative statement could still be mistaken for a skill the candidate uses.

### Finite-state transducers

A finite-state transducer reads symbols and produces output symbols. In ResumeLens, transducers map supported spelling variants of skills to a common token before classification. Mohri (1997) describes the use of finite-state transducers in language and speech processing.

This step helps reduce the effect of spelling differences. Its limitation is the list of variants: if a form is not included in the transducer rules, the program cannot infer that it means the same thing.

### Grammar and the DSL with textX

A grammar defines which text structures are allowed. ResumeLens uses a DSL to store a candidate’s name, contact details, experience, education, skills, and profile evaluations in a consistent format. textX can turn a grammar into a parser and Python model objects; Dejanović et al. (2017) describe it as a tool for implementing domain-specific languages.

The ResumeLens parser checks the DSL structure. Its validators then check a few conditions, such as a non-empty name, an email containing `@`, and at least one profile evaluation. These checks do not confirm that the resume is truthful or that a listed skill belongs to the candidate.

## 4. Comparison

This table gives a general comparison. It is not a performance measurement of ResumeLens.

| Aspect | Rules and formal methods | Machine learning and language models |
|:---|:---|:---|
| Repeatability | Repeatable with the same input and rules | Depends on data, model, and settings |
| Explanation | Patterns and automaton transitions can be inspected | It may be hard to show which evidence led to an output |
| Coverage | Limited to included rules and variants | May recognize learned patterns or use context |
| Training data | No training corpus is needed, but rules and test cases are | Needs suitable examples, goals, and evaluation |
| Main risk | Misses unknown wording; a match may be misleading | May learn biases from its data and be harder to audit |

Neither approach solves the whole problem. Formal rules are easier to inspect, while learned models may cover more variations but require data and careful checks.

## 5. ResumeLens: contribution, limits, and next steps

ResumeLens connects four stages: extraction with regular expressions, skill normalization with transducers, profile classification with automata, and structured output with a textX DSL. This separation makes the project useful for learning: each stage can be studied and its output checked before it moves to the next stage.

The system recognizes four profiles: Full Stack, ML Engineer, Backend, and Data Engineer. Its rules use a defined skill vocabulary and specific token combinations. It does not understand general paraphrases or sentence meaning. It also does not measure a candidate’s real experience or predict future job performance. The result should therefore be understood as the output of the project’s current rules, not as a hiring recommendation.

For future work, the team could test more skill variants using fictional resumes, measure extraction errors, and add examples where a skill word appears in a misleading context. If the team compares the system with machine learning, both approaches should use the same evaluation data. Any hiring-related use would also need broader validation, fairness checks, and human oversight.

The main conclusion is that formal methods make a small, clearly defined screening pipeline easier to inspect and test. Their fixed vocabulary also limits what they can recognize. More flexible models may handle context better, but they bring data and audit challenges. Neither approach can replace careful human judgment in a consequential hiring decision.

## References

APA 7 style. Every reference below is cited in the text.

- Bhatia, V., Rawat, P., Kumar, A., & Shah, R. R. (2019). *End-to-end resume parsing and finding candidates for a job description using BERT*. arXiv:1910.03089. https://arxiv.org/abs/1910.03089
- Dejanović, I., Vaderna, R., Milosavljević, G., & Vuković, Ž. (2017). TextX: A Python tool for domain-specific languages implementation. *Knowledge-Based Systems, 115*, 1–4. https://doi.org/10.1016/j.knosys.2016.10.023
- Lin, Y., Lei, H., Addo, P. C., & Li, X. (2016). *Machine learned resume-job matching solution*. arXiv:1607.07657. https://arxiv.org/abs/1607.07657
- Mohri, M. (1997). Finite-state transducers in language and speech processing. *Computational Linguistics, 23*(2), 269–311. https://aclanthology.org/J97-2003/
- Raghavan, M., Barocas, S., Kleinberg, J., & Levy, K. (2020). Mitigating bias in algorithmic hiring: Evaluating claims and practices. In *Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency* (pp. 469–481). Association for Computing Machinery. https://doi.org/10.1145/3351095.3372828