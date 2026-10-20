# Literature Note Template

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

## Contents

- [Standardized frontmatter](#standardized-frontmatter)
- [Body structure](#body-structure)
- [File naming](#file-naming)
- [Directory discipline](#directory-discipline)
- [Bulk standardization](#bulk-standardization)

Use this template for new literature notes. Write notes, classifications, tags,
and filenames in English by default. Another language is an explicit user choice,
not a requirement of the archive format. Preserve the original source title and
author names where needed for accurate identification.

## Standardized frontmatter

```yaml
---
title: "Original Article Title"
authors: "Last1, F.; Last2, F."
year: 2024
journal: "Full Journal Name"
doi: "10.xxxx/example"
classification: "A_core-research"
tags: [corrosion, nitrate, oxide-ion, review]
date_read: 2026-06-03
---
```

| Field | Rule |
|---|---|
| `title` | Verified original title, quoted |
| `authors` | Consistent `Last, F.; Last, F.` form; abbreviation only when appropriate |
| `year` | Four-digit publication year, distinct from the reading date |
| `journal` | Verified venue name or report identifier |
| `doi` | Verified DOI when present; leave absent/null rather than inventing one |
| `classification` | One of the agreed full category identifiers below |
| `tags` | Three to five specific English keywords by default |
| `date_read` | ISO date of the actual reading |

Default categories:

- `A_core-research`: directly addresses the main research question.
- `B_section-support`: supports a particular thesis or review section.
- `C_engineering-background`: supplies application or engineering context.
- `D_method-transfer`: offers a potentially transferable method.
- `E_deferred`: lower-priority material retained for possible later use.

Keep classification IDs consistent across configuration, directories, and
frontmatter. If an existing archive uses another schema, map it explicitly and
preserve rollback information instead of silently renaming its contents.

Avoid duplicating the publication year in a generic `date` field or the reading
date in an additional `note_date` field. Add provenance fields only when they
serve a real traceability need; this template is not a ban on source links.

## Body structure

```markdown
## Core claim
[One to three sentences. Distinguish established evidence, broad agreement,
disputed interpretation, and speculation. Do not label consensus without support.]

## Methods
[Key methods, conditions, advantages, and limitations.]

## Key findings
[Concrete data, units, comparisons, and source locations.]

## Critical assessment
[Strengths, weaknesses, relevance gaps, alternative explanations, and reliability.]

## Connection to research
[Specific relevance to the user's question, system, measurement, or design.
Keep reported findings separate from proposed transfer.]

## Next steps
[Which section might cite this, which reference to follow, what to verify,
or which experiment the evidence motivates.]
```

The frontmatter `title` serves as the note title; avoid a duplicate H1 in the body
unless the user's renderer requires it. Label whether the note rests on full
text, an abstract, or metadata.

## File naming

Use `{FirstAuthorLast}{Year}_{specific_keywords}.md`. Preserve meaningful hyphens
and name spelling, place the four-digit year immediately after the surname, and
choose two to four contribution-specific English keywords joined by underscores.

| Good | Avoid |
|---|---|
| `Goods2004_nitrates_304_316_long-term-corrosion.md` | A compressed entire title without separators |
| `Author2018_topic_method.md` | `paper.md` |
| `Kruizenga2011_316SS_failure_oxide-coverage.md` | A generic keyword such as `literature` |

## Directory discipline

Use the established full category paths, for example
`A_core-research/notes/`, `B_section-support/notes/`,
`C_engineering-background/notes/`, `D_method-transfer/notes/`, and
`E_deferred/notes/`. Verify that delegated outputs use the same IDs and paths.
Do not alter a pre-existing archive without the user's requested scope.

## Bulk standardization

Inventory Markdown files, parse existing frontmatter, and extract only supported
values from the source record or note body. Publication years may be recognized
with `(19|20)\d{2}`, but a number in a filename is only a candidate and should be
checked. Preserve original titles and authors instead of guessing missing
metadata. Normalize the agreed category ID, derive specific tags, and generate a
collision-safe filename. Remove redundant body titles only after preserving their
content. Before an authorized rename, save a mapping CSV for rollback and check
links and duplicate paths. A missing field is a request for evidence, not a reason
to invent a plausible value.
