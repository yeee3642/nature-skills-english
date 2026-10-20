# Revision Handoff Brief

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

Use this when the user wants a standalone set of instructions for an external
editor such as GPT or Codex, or when a completed review needs a portable revision
brief. Prepare three aligned inputs: task summary, original draft, and revision
instructions. Writing a brief does not itself authorize sending it externally.

## Brief structure

```markdown
# Project — Revision Instructions
> Based on the review dated YYYY-MM-DD and the specified draft version.

## Core positioning change
[One sentence: previous positioning -> supported revised positioning.]

## Prioritized revisions
[P0, then P1, then P2. For each: issue -> required change -> exact draft location
-> evidence/constraints -> acceptance criterion.]

## Protected material
[Structure, text, data, terms, and commitments that must remain unchanged.]

## Final positioning paragraph
[Replacement text when the evidence and scope support a settled formulation.]
```

Give section numbers and the relevant original wording rather than making the
editor rediscover the location. Provide exact replacements for settled changes
and a constrained direction for unsettled ones. Keep P0 ahead of P1. Name the
file `revision_briefs/editor_instructions_YYYY-MM-DD.md`.

Before delivery, verify that the brief is self-contained, every P0/P1 item has a
location and acceptance criterion, and terminology and version identifiers agree
across the task summary, draft, and instructions.
