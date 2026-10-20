# Export and Archive

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

For a requested formal proposal package, create the agreed outputs, normally:

```text
exports/proposal_final.md     # archive / versioning / future reuse
exports/proposal_final.docx   # supervisor circulation or submission draft
```

A PDF is optional and should be generated only when requested. Honor a request
for Markdown or revised text without forcing a DOCX export.

## DOCX export

Use `scripts/build_proposal_docx.py` when its supplied formatting matches the
task. It parses Markdown into a formatted document using python-docx. The default
style is Times New Roman, with SimSun as the East Asian fallback; title 18 pt,
headings 16/14/12 pt in black and bold, body 12 pt at 1.5 line spacing, no first-line
indent, one-inch margins, Table Grid tables, and 9 pt Consolas code. Inspect the
actual script and final rendering rather than assuming a converter's default
styles are submission-ready. User or institutional format requirements take
precedence. Load document/PDF guidance only for the requested output formats.

## Pre-delivery checks

- No unresolved TODOs are hidden in a supposedly final document.
- Unsupported claims remain marked or removed rather than presented as facts.
- Citation placeholders are resolved or disclosed.
- Figure/table numbering and cross-references agree.
- Version name and date are clear.
- The target quality threshold is met, or remaining risks are reported.

## Archival

Keep external archival outside the default pipeline. Write to an external vault,
archive, or synced directory only within the user's requested scope. If that
destination has not been authorized, prepare the completed package locally and
ask specifically about the intended destination. Do not overwrite existing
archived versions implicitly.
