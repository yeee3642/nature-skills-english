# Core principles (reader)

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

Turn a research paper into a complete, source-grounded Markdown reading artifact. The default output is English, with intact source structure, figures, captions, equations, and source locations; it is not a summary dump.

- Preserve extractable prose, paragraph structure, section order, evidence, hedging, terminology, units, and citation markers.
- For English sources, retain the verified source text without adding a redundant translation. For other source languages, translate faithfully into English; preserve original text alongside the translation when the user requests bilingual or source-comparison output.
- A requested language or bilingual pair takes precedence. In bilingual mode use paragraph-level `**Original:**` and `**Translation:**` pairs and keep both original and translated captions.
- Extract figures/tables as assets and place them at the first substantive mention or interpretation point, with captions attached.
- Render equations as Markdown math with stable equation anchors. Never show bare LaTeX commands as prose or alter mathematical content when translating surrounding text.
- Preserve stable page and block anchors, and write complete `paper.md`, `source_map.json`, `translation_notes.md`, and necessary `assets/` by default.

This applies to papers, preprints, and conference proceedings across disciplines, not only Nature-family journals. An explicit question, summary, or excerpt request determines scope; do not expand it into full-paper processing. Citation-only searches belong to the citation workflow.

## Reader scope

When the user requests a reader, full-paper translation, source comparison, or invokes `nature-reader` without a narrower deliverable, process the full document. A bilingual reader is required only when requested; then align every available substantive paragraph and caption.

Do not substitute a summary, detached review, captions without figure/table crops, source-free key points, or only the abstract/introduction/highlights. If constraints prevent completion, produce an honest draft and record missing pages, assets, untranslated blocks, and uncertain OCR/crops in `translation_notes.md`.

Translate for meaning rather than style. Preserve paragraph prose unless the source itself uses lists or tables. Do not collapse methods into keyword bullets or slide notes.

## Equations and traceability

Give every display equation an `E001`, `E002`, ... anchor. Use `$...$` for inline math and `$$...$$` for display math. If transcription is uncertain, crop the original into `assets/equations/`, display it first, and mark any useful best-effort LaTeX as low confidence. Never guess missing symbols or leave commands such as `\frac` and `\sum` outside delimiters. Display each equation only once even in bilingual output.

Every substantive block retains a stable source pointer. In English-only mode, use the English source text or faithful English translation as the block's reading text. In requested bilingual mode:

```markdown
<a id="S001"></a>
**Source:** p.1 S001

**Original:** [source paragraph]

**Translation:** [faithful translation in the requested target language]
```

The reader must support movement between reading text, optional original/translation pairs, source locations, and figure/table evidence.

## Copyright caution

Keep chat quotations from publisher PDFs short and point to the local artifact. Include full local reading text only for user-provided or clearly lawful open-access sources; avoid reproducing large copyrighted text in chat.

## Quality bar

A reader should let the user read the whole available paper in the requested language, see where claims originate, inspect nearby figures/tables, read rendered equations or their original crops, and navigate without losing source traceability. Optional bilingual output must preserve full alignment rather than becoming a summary.
