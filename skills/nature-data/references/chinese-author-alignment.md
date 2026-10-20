# Author-Note Alignment

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

Use this reference for informal or multilingual Data Availability notes, or when
the user explicitly asks for bilingual wording. Translate the intended access route,
not the source syntax. English is the default output language.

## Core terminology

| Intended concept | Preferred English | Constraint |
|---|---|---|
| Availability heading | Data Availability | Use the journal's heading. |
| Data created by the study | data generated in this study | Give repository and identifier when public. |
| Unprocessed observations | raw data | Do not call processed tables raw data. |
| Transformed observations | processed data | State whether processing scripts are available. |
| Values underlying figures or tables | source data | Identify the corresponding displays. |
| Supporting files | Supplementary Information | Name exact files and tables. |
| Public database | public database / public repository | Name the resource and identifier. |
| Durable archive | data repository | Prefer repository over a vague platform label. |
| Repository-assigned identifier | accession number | Use only when assigned by the repository. |
| Permanent link | DOI / persistent URL | Prefer DOI when available. |
| Data subject to access limits | restricted data | State legal, ethical, consent, commercial, or third-party reasons. |
| Data with direct identifiers removed | de-identified data | Do not claim anonymity without addressing re-identification risk. |
| Access by request | reasonable request | Add route, eligibility, and conditions. |
| Author contact | corresponding author | Prefer an institutional access process when available. |
| Access agreement | data-use agreement | State when required. |
| Research authorization | ethics approval | Name the approval body or relevant requirement. |
| Software access heading | Code Availability | Keep separate when the journal does so. |

## Convert vague notes into traceable statements

- "All data are in the paper and supplement": name Source Data files,
  Supplementary Tables, or repository records. Flag absent raw data.
- "Available from the corresponding author on reasonable request": state why
  public sharing is impossible, who reviews requests, eligible requesters,
  approvals or agreements, and the access route.
- "Not public for privacy reasons": state the privacy, consent, or legal basis,
  public metadata, responsible access committee, and conditions.
- "Commercial data cannot be shared": name the provider or owner, request
  process, and whether derived or aggregate data can be shared.
- "Will upload after acceptance": record a deposit action before submission or
  arrange a private reviewer link when the repository supports one.
- "We used public datasets": include source, version or release, date accessed
  when relevant, and formal dataset citations.

## Intake questions

Ask only what is missing for the requested statement: which datasets support
main and supplementary displays and statistics; whether each has a repository,
DOI, accession, or reviewer link; what consent, privacy, commercial, third-party,
national, or institutional restrictions apply; who reviews requests and which
approvals or agreements are required; and whether code or a README documents
the path from raw observations to figure source data.

## Output

```text
Data Availability
[English statement for submission]

Author checks
- Intended meaning: [brief explanation when needed]
- Requires confirmation: [missing accession, repository, or ethics condition]
```

Keep explanatory notes outside the final statement. Add a second-language
explanation only when the user explicitly requests it and the journal permits
any bilingual text intended for submission.
