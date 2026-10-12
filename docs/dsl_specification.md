# ResumeLens DSL: EBNF Specification and Design Principles

Universidad Icesi  
Course: Discrete Structures III (CyED III)  
Integrative Project: ResumeLens

---

## 1. Purpose and Role in Stage 4

The ResumeLens DSL is a readable, structured representation of a candidate profile. In Stage 4 it provides the text parsed into a textX model, checked by semantic validators, and serialized back to DSL. The available `src.main.run_pipeline` implements that parse–validate–serialize sequence. Automatic conversion from arbitrary plain-text resumes into DSL is [TODO: verificar].

The grammar is the source of the syntactic structure. `validate_resume_model` adds a small set of business checks after parsing; it does not perform a complete email, skill-taxonomy, or profile-name validation.

---

## 2. Design Principles and Evidence

| Principle | Evidence in the implementation | Current scope or gap |
|:---|:---|:---|
| Readability | Literal section labels such as `CONTACT`, `EXPERIENCE:`, `SKILLS:` and quoted `STRING` values make the document understandable without knowing the AST. | The grammar fixes section order. |
| Explicit, low-ambiguity structure | `ResumeModel` requires sections in a fixed order; `Experience`, `Education`, and `ProfileEvaluation` have explicit delimiters and keywords. | textX parses the declared grammar; this document does not claim a separate proof that the grammar is unambiguous. |
| Closed vocabulary aligned with the taxonomy | `StatusType` is a closed choice between `ACCEPTED` and `REJECTED`. | Skills and profile names are generic `STRING` values. Neither the grammar nor `validators.py` checks them against the taxonomy, so taxonomy alignment is not currently enforced. |
| Early failure with actionable errors | textX raises a syntax error for malformed input, and `validate_resume_model` raises `DSLValidationError` for an empty name or email without `@`. Examples and captured messages appear in Section 6. | Syntax and semantic validation are separate calls; `DSLParser.parse_string` does not call the semantic validator. |
| Serializer round-trip | `DSLSerializer.serialize_to_dsl` emits the fields in grammar order; the valid sample below was serialized and reparsed successfully. | The serializer interpolates strings directly and does not escape embedded quotes; arbitrary strings are not guaranteed to round-trip. |

---

## 3. Context-Free Grammar

The grammar in `src/dsl/grammar/resume.tx` defines $G = (V, \Sigma, R, S)$:

- $V = \{ResumeModel, ContactInfo, Experience, Education, ProfileEvaluation, StatusType\}$
- $\Sigma$ is the set of literal terminals in Table 1 together with textX's built-in terminals `STRING` and `INT`.
- $S = ResumeModel$
- $R$ is the set of productions transcribed in Section 5.

The terminals `STRING` and `INT` are built-ins from the installed textX runtime. Their match rules in that runtime are:

```text
STRING := r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')'
INT    := r'[-+]?[0-9]+'
```

`STRING` accepts single- or double-quoted values and escaped matching quotes. `INT` accepts a signed or unsigned sequence of decimal digits; the current semantic validator does not constrain experience years to be positive.

### Table 1. Terminals

| Terminal / match rule | Meaning in the DSL |
|:---|:---|
| `CANDIDATE_PROFILE` | Begins a candidate profile. |
| `TITLE:` | Introduces the candidate title. |
| `CONTACT` | Begins contact information. |
| `email=` | Introduces the required email string. |
| `phone=` | Introduces the optional phone string. |
| `github=` | Introduces the optional GitHub string. |
| `linkedin=` | Introduces the optional LinkedIn string. |
| `EXPERIENCE:` | Begins the zero-or-more experience entries. |
| `-` | Begins an experience or education entry. |
| `at` | Separates an experience position from its company. |
| `(` and `years)` | Delimit the integer year count in an experience. |
| `EDUCATION:` | Begins the zero-or-more education entries. |
| `from` | Separates a degree from its institution. |
| `SKILLS:` | Begins the skill list. |
| `,` | Separates skill strings in the list. |
| `EVALUATIONS:` | Begins the one-or-more profile evaluations. |
| `:` | Separates an evaluated profile from its status. |
| `ACCEPTED` | One allowed `StatusType` value. |
| `REJECTED` | The other allowed `StatusType` value. |
| `STRING` | textX built-in quoted-string match rule shown above. |
| `INT` | textX built-in signed decimal integer match rule shown above. |

### Table 2. Non-terminals

| Non-terminal | Rule | What it models |
|:---|:---|:---|
| `ResumeModel` | `ResumeModel:` | Complete profile, including contact, experience, education, skills, and evaluations. |
| `ContactInfo` | `ContactInfo:` | Required email and optional phone, GitHub, and LinkedIn values. |
| `Experience` | `Experience:` | Position, company, and integer years. |
| `Education` | `Education:` | Degree and institution. |
| `ProfileEvaluation` | `ProfileEvaluation:` | Profile name and its status. |
| `StatusType` | `StatusType:` | Closed choice of `ACCEPTED` or `REJECTED`. |

---

## 4. TextX Assignment and Repetition Notation

In the grammar, `field=Rule` assigns a parsed object or value to a model attribute. `items*=Rule` means zero or more occurrences; `items+=Rule` means one or more. A trailing `?` makes the parenthesized group optional. `STRING[',']` is textX's separated-list notation; here `skills+=STRING[',']` requires at least one string and uses commas between additional strings. References such as `contact=ContactInfo` and `experiences*=Experience` invoke other grammar rules and populate the corresponding model attributes.

---

## 5. Standard EBNF Transcription

The following EBNF is a direct transcription of `resume.tx`; quoted words and punctuation are terminals, while `STRING` and `INT` use the textX match rules in Section 3.

```ebnf
ResumeModel = "CANDIDATE_PROFILE", STRING,
              "TITLE:", STRING,
              ContactInfo,
              "EXPERIENCE:", { Experience },
              "EDUCATION:", { Education },
              "SKILLS:", STRING, { ",", STRING },
              "EVALUATIONS:", ProfileEvaluation, { ProfileEvaluation } ;

ContactInfo = "CONTACT", "email=", STRING,
              [ "phone=", STRING ],
              [ "github=", STRING ],
              [ "linkedin=", STRING ] ;

Experience = "-", STRING, "at", STRING, "(", INT, "years)" ;
Education = "-", STRING, "from", STRING ;
ProfileEvaluation = STRING, ":", StatusType ;
StatusType = "ACCEPTED" | "REJECTED" ;
```

The optional contact fields have a fixed order when present: phone, GitHub, then LinkedIn. `EXPERIENCE:` and `EDUCATION:` may have no entries; `SKILLS:` and `EVALUATIONS:` require at least one entry.

---

## 6. Semantic Validation

`validate_resume_model` applies these checks after syntactic parsing:

| Rule | Condition | Error raised |
|:---|:---|:---|
| Candidate name | `model.name` is empty or contains only whitespace. | `DSLValidationError`: `El nombre del candidato no puede estar vacío.` |
| Email | `model.contact.email` is empty or does not contain `@`. | `DSLValidationError`: `El correo '<value>' no tiene un formato válido.` |
| At least one evaluation | `model.evaluations` is absent or empty. | `DSLValidationError`: `El perfil debe incluir al menos una evaluación de perfil.` |

The grammar's `evaluations+=ProfileEvaluation` already requires one or more evaluations, so the final validator rule is redundant for ordinary parser-created models. It remains relevant if a model is constructed or modified outside the parser. The email check only looks for `@`; it is not full email-address validation.

---

## 7. Serialized Valid Example and Derivation

The example below was generated by executing the real `DSLSerializer.serialize_to_dsl` on a parsed and validated projection of `data/resumes/data_engineer_sample.txt`. The candidate name, contact values, title, and canonical skills were obtained from the synthetic source using the repository extractors and normalizer; the education entries reproduce that source's content. No experience entry is added because the resume gives an overall experience duration without assigning it to a specific employer. The serialized result was parsed and validated again.

```resume-dsl
CANDIDATE_PROFILE "Rafaela Quintero"
TITLE: "Data Platform Engineer"
CONTACT
email= "rafaela.quintero@example.com"
phone= "+57 300 555 0243"
github= "https://github.com/rafaela-quintero-data"
linkedin= "https://linkedin.com/in/rafaela-quintero-data"
EXPERIENCE:
EDUCATION:
- "Bachelor of Information Systems" from "Universidad de Nariño"
- "Certificate in cloud data fundamentals" from "Centro Académico Imaginario"
SKILLS: "PYTHON", "SPARK", "SQL"
EVALUATIONS:
"Data Engineer" : ACCEPTED
```

Simplified derivation tree for the parsed model:

```text
ResumeModel
├── "CANDIDATE_PROFILE" STRING("Rafaela Quintero")
├── "TITLE:" STRING("Data Platform Engineer")
├── ContactInfo
│   ├── "CONTACT" "email=" STRING("rafaela.quintero@example.com")
│   ├── "phone=" STRING(...) "github=" STRING(...) "linkedin=" STRING(...)
├── "EXPERIENCE:" Experience* (zero entries)
├── "EDUCATION:" Education Education
├── "SKILLS:" STRING STRING STRING
└── "EVALUATIONS:" ProfileEvaluation
    └── STRING("Data Engineer") ":" StatusType("ACCEPTED")
```

---

## 8. Invalid Examples and Captured Errors

Each example was run through `DSLParser.parse_string`; semantic examples were then passed to `validate_resume_model`.

### Syntax error: unquoted candidate name

```resume-dsl-invalid-syntax
CANDIDATE_PROFILE texto_sin_formato_ni_comillas
```

Captured `TextXSyntaxError` from textX:

```text
None:1:19: Expected STRING => 'E_PROFILE *texto_sin_'
```

### Semantic error: empty candidate name

This text parses because an empty quoted string matches `STRING`; semantic validation then rejects it.

```resume-dsl-invalid-semantic
CANDIDATE_PROFILE ""
TITLE: "Data Platform Engineer"
CONTACT
email= "rafaela.quintero@example.com"
EXPERIENCE:
EDUCATION:
SKILLS: "PYTHON"
EVALUATIONS:
"Data Engineer" : ACCEPTED
```

Captured `DSLValidationError`:

```text
El nombre del candidato no puede estar vacío.
```

### Semantic error: email without `@`

```resume-dsl-invalid-semantic
CANDIDATE_PROFILE "Rafaela Quintero"
TITLE: "Data Platform Engineer"
CONTACT
email= "rafaela-at-example.com"
EXPERIENCE:
EDUCATION:
SKILLS: "PYTHON"
EVALUATIONS:
"Data Engineer" : ACCEPTED
```

Captured `DSLValidationError`:

```text
El correo 'rafaela-at-example.com' no tiene un formato válido.
```

---

## 9. Limitations and Possible Extensions

- Profile names and skills are free strings; they are not checked against the profile or skill taxonomy.
- The email validator checks only for `@`, and experience years accept signed integers without a positivity check.
- Contact fields are limited to email, phone, GitHub, and LinkedIn. Portfolio and other metadata are not represented by this grammar.
- The serializer does not escape embedded quotes or backslashes in values, so some valid `STRING` values may not serialize back into valid DSL.
- Future extensions could use taxonomy-backed profile and skill types, stronger semantic checks, escaping in the serializer, and additional contact or resume fields.
