# Author-Note Alignment

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

Use this reference for informal or multilingual author notes, manuscript-change
summaries, and explicitly requested bilingual drafting.

## Default behavior

- Accept notes and reviewer summaries in their supplied languages.
- Draft the final point-by-point response in English unless another language is explicitly requested.
- Keep unresolved author actions in a short English `Author checks` section.
- Translate intent, not literal wording, and convert vague notes into evidence requirements.

## Common note conversions

| Author note | Problem | Better handling |
|---|---|---|
| "We fixed it" | Too vague | Ask what changed, where, and whether revised text is available |
| "Revised as requested" | No action mapping | Mark `AUTHOR_INPUT_NEEDED` until action and location are known |
| "We added experiments" | Missing evidence | Request experiment, conditions, replicate/sample details, result, and display location |
| "We added analyses" | Missing detail | Request method, data source, key result, statistical output, and location |
| "This issue is unimportant" | Defensive and unsupported | Explain scope, evidence, or claim boundaries only when justified |
| "No time to do it" | High-risk excuse | Use a study-design or scope explanation only if true; otherwise flag risk |
| "The reviewer misunderstood" | Accusatory | Treat it as a manuscript clarity issue and add clarification |
| "See main text" | Not traceable | Require section, page, line, figure, table, or supplement |
| "We think this is enough" | Unsupported sufficiency | Explain evidence addressing the concern or record the limitation |

## Confirmation section

```text
Author checks
- R1.1: Supply the validation result, sample or dataset size, and Fig. 5 location.
- R1.2: Confirm the test name, replication unit, sample size, and multiple-testing correction.
- R2.1: Animal validation is not documented; use a scope statement and Discussion limitation.
```

Preserve reviewer comments in their supplied language unless translation is
requested. Build the tracker with English action labels, draft polished English
responses, and add checks only for missing facts, decisions, and high-risk issues.
Provide a second-language explanation only on explicit request.

## Tone corrections

For an author note that the reviewer did not understand the method, the response
can acknowledge that the original Methods did not make the distinction clear,
then state the specific clarification and revised location. Do not claim the
revision was made without the revised text or other supplied evidence.

For an experiment outside the present design, explain what additional cohort,
system, or longitudinal design it would need. If supported by the actual
revision, describe the softened claim and added limitation with their locations.
Do not substitute an invented scientific reason for an unsupported author excuse.
