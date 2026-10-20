---
name: researchwrite
description: "Compose, revise, or audit research proposals, opening reports, and research plans from supporting evidence. Invoked as researchwrite for compatibility; use nature-writing for general manuscript sections."
license: MIT
metadata:
  hermes:
    tags: [research, writing, proposal, revision, qa, multi-agent]
    related_skills: [brainstorming, professor, avoid-ai-writing, docx]
---

# Researchwrite — Proposal-First Research Writing

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

## Contents

- [Principles](#principles)
- [Modes](#modes)
- [Project files](#project-files)
- [Reference index](#reference-index)
- [QA mode](#qa-mode)
- [Delivery](#delivery)


Use a stateful evidence-and-argument workflow for research proposals rather than
a generic paper-writing prompt. Write in English by default. The trigger name
`researchwrite` is retained for compatibility; the directory remains
`nature-proposal-writer`. Do not change the frontmatter name without a migration
plan. Read `manifest.yaml` before initializing templates or loading conditional
references, and load only resources needed by the task.

## Principles

Establish the research canon and evidence table before prose, the argument map
before sections, and section contracts before paragraphs. Each contract defines
purpose, allowed and forbidden claims, inputs, and validation. Lock the current
stage's scope before trying to make the document complete. Match specialist
review to the actual failure mode using `professor` when available; do not assume
a fixed expert pool or require an unavailable skill.

Repair scientific logic before polishing language. Never upgrade "may indicate"
to "proves" without evidence. Remove infeasible commitments from the main text;
record the reason where it is useful for review. A plateau, unresolved expert
conflict, or missing evidence can justify stopping instead of further polishing.

## Modes

| Input | Mode and reference |
|---|---|
| Topic, direction, rough idea | `compose`: `references/compose-mode.md` |
| Existing paragraph, section, or proposal | `revise`: `references/revise-mode.md` |
| Draft plus expansion or restructuring target | `hybrid`: `references/hybrid-mode.md` |

Infer the mode when clear. Ask only when the choice materially changes the work.
An instruction to keep receiving source material takes precedence over beginning
the state machine.

## Project files

Use the requested output directory, conventionally
`<outputs>/researchwrite/<project-slug>/`:

```text
00_scope.md              Current writing scope
01_research_canon.md     Hard facts and constraints
02_evidence_table.md     Claim-to-evidence mapping
03_argument_map.md       Argument architecture
04_section_contracts.md  Purpose, inputs, allowed/forbidden claims
05_style_guide.md        Terminology, style, and prohibited inflation
state.json               Mode, round, scores, technical debts
sources/                 Supplied materials and source records
drafts/                  Working sections
revision_briefs/         Targeted revision instructions
qa_logs/                 Diagnostics and review evidence
exports/                 Agreed final output formats
```

Use `templates/` through the manifest's conditional routing.
`references/worked-example-quaternary-proposal.md` demonstrates completed
foundation files in materials science.

## Reference index

| Reference | Load when |
|---|---|
| `references/compose-mode.md` | Building a new proposal with the nine-step compose process |
| `references/revise-mode.md` | Revising existing material with the nine-step revision process |
| `references/hybrid-mode.md` | Preserving a draft while adding missing modules |
| `references/evaluation-rubric.md` | Applying eight dimensions with anchored scores |
| `references/research-anti-slop.md` | Removing inflated or generic proposal language |
| `references/chinese-review-writing-style.md` | Writing evidence-led review prose; legacy filename retained |
| `references/stopping-rules.md` | Continuing, narrowing scope, or stopping |
| `references/professor-dispatch.md` | Dispatching relevant specialist review |
| `references/foundation-files.md` | Building or repairing the five foundation files |
| `references/project-structure.md` | Initializing the project or maintaining state |
| `references/export-archive.md` | Exporting agreed Markdown/DOCX files and archival |
| `references/partial-proposal-scope.md` | Preventing scope creep in staged drafting |
| `references/ref-renumbering-cascade.md` | Updating citations after additions/deletions |
| `references/review-paper-framework.md` | Designing a review's evidence and argument architecture |
| `references/review-critique-methodology.md` | Critical comparison and evidence-weighted synthesis |
| `references/validation-checklist.md` | Checking claims, citations, methods, numbering, and completeness |
| `references/gpt-handoff-revision-brief.md` | Preparing a self-contained editing handoff |
| `references/within-approved-proposal.md` | Deepening an approved project without changing its commitments |
| `references/worked-example-quaternary-proposal.md` | Checking expected foundation-file depth |
| `references/decommit-proposal-mode.md` | Calibrating overcommitted claims to insufficient evidence |

## QA mode

Use QA when the user asks to review, check, or run a draft through the pipeline.
The conventional thresholds are 7.0 for `paper` and `proposal`, 5.0 for `internal`,
and no numerical threshold for `quick`. Scores guide revision, not publication
or funding guarantees.

The order is content review (Gate 2), language detection/cleanup (Gate 1),
format/completeness validation (Gate 3), then anchored scoring (Gate 4). This
numbering is historical; content must come before language.

Select specialists by failure mode: methodology and domain for a paper,
feasibility and novelty for a proposal, coverage and critical depth for a review.
Use available tools or explicit manual checks when an external skill is absent.
Verify citations, reproducibility details, and numbering before scoring. Return
to the failed dimension for at most three rounds; apply stopping rules rather
than endlessly polishing. Quick review flags P0 issues without forcing every gate.

## Delivery

Return the current output or revised text, score/status, remaining risks, and one
useful next action when needed. Do not require a new user turn for work already
authorized. Learn the research background from supplied context and use it to
choose appropriate review expertise.
