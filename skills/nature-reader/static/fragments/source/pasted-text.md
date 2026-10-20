# Source: pasted text or notes

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

The user pasted prose or notes directly, with no retrievable original layout or page images.

- Treat the pasted text as the source of truth. Build the source map and bilingual pairs from it.
- Page numbers may be unknown. Use sequential block IDs (`S001`, `S002`, ...) and, where the paste shows section headings, use section-level anchors instead of page anchors. Note in `translation_notes.md` that page anchors are unavailable.
- There are usually no figure/table images. Do not invent crops. If the text references figures/tables, keep the references and captions as text blocks and note that the visual assets were not provided.
- If the paste is clearly partial (for example abstract and intro only), build the reader for what was given and label it draft mode; do not backfill missing sections from memory.
- Preserve any citation markers, equations, and symbols exactly as pasted. Keep valid existing math delimiters; normalize unmistakable raw LaTeX into `$...$` or `$$...$$`, but mark ambiguous or incomplete expressions instead of guessing missing delimiters or symbols.
- Keep the requested reader format, including aligned pairs when bilingual output is requested; do not collapse pasted prose into a summary just because layout metadata is missing.
