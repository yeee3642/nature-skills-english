# Technical disclosure builder (Step 7)

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

Use `template_reference.md` for chapter examples. Draft in English unless the user explicitly requests a different language or a jurisdiction-specific formal application.

## 7.1 Chapter structure

Use: document notes; Chapter 1 background and closest prior art, with 1.1 source-by-source comparison and 1.2 limitations; Chapter 2 technical problem; Chapter 3 detailed solution, with 3.1 context, 3.2 system diagram, 3.3 module functions and relationships, 3.4 process diagram and explanation, 3.4.1 symbols and equations when applicable, and 3.5 technical parameters; Chapter 4 supported advantages; Chapter 5 technical features and proposed protection points; Chapter 6 embodiments, technical effects, and parameter examples.

Every patent or paper in 1.1 needs a verified public URL matching its bibliographic record. Understand the full retrieved abstract or public text before describing the technical solution, application, or limitations. Never invent content from a title. Summarize sources in your own words.

Keep internal checklists, evidence IDs, scores, repository notes, and tool implementation details outside the delivered disclosure body. Its technical chapters must stand on their own. State material limitations and review requirements separately when delivering the files.

## 7.2 Document header

Use the working invention title, technical contact fields supplied by the user, and intended patent category. Unknown contact fields remain `[TO CONFIRM]`. Explain the technical background and solution completely enough for an inventor and patent professional to assess implementation; do not claim legal enablement merely because the template is complete.

## 7.3 Output filenames and versions

Extract the case name from the document, remove placeholder text, replace Windows-invalid characters (`\ / : * ? " < > |`) and newlines, and keep a meaningful stem of roughly 80 characters or fewer. Deliver both `{case_name}_{YYYYMMDDHHmmss}.md` and a matching `.docx`. Use the actual local write time. The same naming rule applies to the first draft, incremental merges, and corrections. Preserve previous versions unless the user explicitly requests replacement. Honor a user-specified filename.

```bash
python scripts/disclosure/mermaid_render.py -i work/draft.md -o "outputs/Adaptive_scheduler_20260408143025.md"
```

The default Word output uses the same stem. Keep generated figures with the corresponding document and report the actual deliverable paths.

## 7.4 System and process diagrams

Use fenced Mermaid source for system and process diagrams, with brief English operation labels and ordinary step numbers. Render locally with `mmdc`; embed the resulting PNG in Word. Retain the Mermaid source and generated image comment in Markdown. An ASCII box diagram is not a substitute for the diagram. Explain how each step corresponds to the claimed operation and concrete domain output.

## 7.5 Sensitive material

Remove confidential company, product, customer, and category names when the user requires anonymization. Replace them with consistent functional descriptions. Preserve technical meaning and supported quantitative facts needed for assessment; do not silently convert evidence into invented ranges or vague claims. Distinguish a deliberately anonymized value from an unknown value.

## 7.7 Symbols and equations

Define symbols before equations in 3.4.1. State meanings, index meanings, units, and ranges. Keep a symbol's form and meaning identical in the equation text, 3.5 parameter table, and Chapter 6 examples. Do not reuse one letter for different physical quantities.

Use upright resource/type subscripts, such as `b_{i,\mathrm{cpu}}` and `a_{j,\mathrm{mem}}`; do not use `^{cpu}` or `^{mem}` as field labels. Reserve superscripts for powers, transposes, sequence indices, or related mathematical notation. Use one inline delimiter convention (`\(...\)` or `$...$`) and one display convention (`\[...\]` or `$$...$$`) throughout. Prefer `\leq` and `\geq`. Keep display formulas on one source line when practical, choose one numbering convention, and write logical conjunctions in prose or as `\land`/`\lor` rather than complex textual commands.

Check operators, parentheses, missing terms, sign and inequality direction, units, and declared ranges. Map each scoring, scheduling, constraint, or aggregation operation to the process and module description. Address applicable boundaries such as empty sets, missing measurements, and zero denominators. Update dependent prose and examples whenever notation or a formula changes.

## Final Markdown and Word delivery

Deliver both files with matching version stems. The Markdown preserves fenced Mermaid and hidden image references; Word embeds the generated diagram. The generic disclosure helper renders equations as PNG when possible and preserves unrenderable source. This is different from the structured formal-application renderer, which requires native editable Office Math. Do not claim generic disclosure equations are editable Office Math.

## 7.6 Optional claim emphasis

When useful, explain separately that Chapter 5 can be refined toward a method, system, or apparatus emphasis already supported by this draft. Do not invent alternative industries, mechanisms, or protection points merely to offer choices. A later requested refinement follows `iteration_context.md` and `merger.md`, creates a new timestamped version, and updates `disclosure_revision_log.md`.
