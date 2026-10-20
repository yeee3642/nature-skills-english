# Literature Gap Analysis Methodology

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

## When to use

Use when the user asks whether a topic has been studied, whether an apparent gap
is real, or which related systems already have evidence.

## 1. Multi-source search

Search the exact topic and relevant synonyms across multiple available sources.
Combine exact system names, broader component queries, and adjacent application
or mechanism terms. For example, search an exact quaternary salt system as well
as relevant ternary and binary systems. Record the source, query, date, filters,
and observed hit counts. Search-engine result counts are approximate and do not
measure the number of relevant studies.

## 2. Decompose and classify

If the direct search finds no relevant result, decompose the system into
subsystems and search naming variants. For a four-component system, examine the
four three-component combinations and other scientifically relevant subsets.

| Tier | Meaning | Action |
|---|---|---|
| Direct | Same system and research question | Assess actual overlap and evidence |
| Adjacent | Relevant subsystem, method, or related condition | Extract transferable evidence and its limits |
| Unrelated | Does not address the question | Exclude with a brief reason when useful |

Zero direct hits means "not located within the documented search", not a
confirmed global absence. A one-component paper may still be methodologically
relevant; classify by the question rather than component count alone.

## 3. Extract adjacent evidence

For each useful adjacent paper, record the verified citation, composition or
system, method, relevant finding, possible transfer to the user's work, and the
condition that limits that transfer. Mark abstract-only or metadata-only access.
Do not silently skip inaccessible evidence or infer an unreported mechanism.

## 4. Deliver a bounded gap report

Use the requested output directory, conventionally
`outputs/literature/<topic>_gap_report.md`, and cover:

1. The main conclusion: found overlap, partial overlap, or no direct evidence
   located within the search scope.
2. A subsystem/evidence map with representative sources.
3. Details from the most informative adjacent studies.
4. What remains unresolved and why answering it would matter; do not invent a
   reason that previous researchers did not study it.
5. A source-supported, qualified gap statement suitable for an introduction.
6. Concrete experimental or computational next steps.
7. Reproducible search methods, queries, filters, counts, and access limitations.

## Cost control

Start with a small batch of independent queries, then adapt to coverage gaps.
Read a few high-information sources rather than extracting every hit. Use the
available search/fetch tools, report access limits, and stop when further search
would not materially change the supported conclusion. Do not impose a fixed call
budget that prevents an adequate search.
