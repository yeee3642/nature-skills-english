# Disclosure tools

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

Run commands from this skill directory or use absolute script paths. On native Windows use `python -X utf8`; in other environments use the configured Python interpreter. Install only the dependencies needed for the requested workflow, in an appropriate environment. Do not store API keys in repository files.

## Office sources to Markdown

`docx_to_md.py` converts `.docx` using mammoth; `pptx_to_md.py` converts `.pptx`/`.ppsx` using python-pptx. Both extract embedded images into a sibling `{output_stem}_media/` directory and use relative Markdown references.

```bash
python scripts/disclosure/docx_to_md.py -i source/design.docx -o work/design.md
python scripts/disclosure/pptx_to_md.py -i source/review.pptx -o work/review.md
```

Use `--media-dir` for a custom image directory. Legacy `.doc`/`.ppt` need conversion to OOXML first. Word conversion may simplify complex layout or unsupported vector pictures. PowerPoint conversion retains ordinary text, tables, image shapes, and speaker notes, but does not rasterize every chart, SmartArt, or OLE object. Shape traversal can differ from visual reading order. Inspect important missing content against the source rather than treating absence in converted text as absence in the document.

## Mermaid diagrams and matching Word output

The helper discovers a local `node_modules/.bin/mmdc`, PATH `mmdc`, or Node/npx, in that order. The optional local Mermaid CLI dependency is declared in `scripts/disclosure/package.json`; run `npm install` there only when the requested workflow needs it. Rendering uses argument arrays so Windows paths with spaces remain intact.

```bash
python scripts/disclosure/mermaid_render.py -i work/draft.md -o "outputs/Adaptive_scheduler_20260408143025.md"
python scripts/disclosure/mermaid_render.py -i work/draft.md -o outputs/version.md --docx outputs/version.docx
python scripts/disclosure/mermaid_render.py -i work/draft.md -o work/preview.md --no-docx
python scripts/disclosure/mermaid_render.py -i work/draft.md -o work/preview.md --mmdc-scale 3 --mmdc-width 1600 --mmdc-height 1200
```

The delivery filename follows `disclosure_builder.md` 7.3 even though intermediate filenames may differ. `--assets-dir` controls the PNG subdirectory. Mermaid source remains fenced in Markdown, followed by a hidden image comment; Word embeds the PNG rather than the code. Existing generated comments prevent duplicate processing. Failed diagrams retain their source and emit diagnostics. Do not describe a failed rendering as successful. If automatic Word generation fails, follow its printed manual command.

## Equations and Markdown-to-Word conversion

```bash
python scripts/disclosure/math_render.py -i work/draft.md -o work/with-equations.md
python scripts/disclosure/md_to_docx.py -i work/draft.md -o outputs/disclosure.docx --base-dir work
python scripts/disclosure/md_to_docx.py -i work/draft.md -o outputs/disclosure.docx --image-max-width-inches 6 --image-max-height-inches 9
```

Generic disclosure rendering uses matplotlib equation PNGs and preserves LaTeX source on failure. It retains inline/display delimiters and uses hidden image comments. Use `--no-math` in `mermaid_render.py` or the corresponding Markdown converter option when rendering is intentionally skipped. Do not claim these PNG equations are editable Office Math: the separate structured formal-application renderer provides native Office Math.

The Markdown converter handles headings, ordinary paragraphs, inline bold/code, lists, fenced code, simple GFM tables, quotations, rules, and images constrained proportionally by width and height. Consecutive nonblank source lines become separate Word paragraphs. Complex layout may need a real document template and visual review. Source Markdown must never be overwritten by Word output.

## Revision log

```bash
python scripts/disclosure/iteration_dialog_log.py --case-dir outputs/case --kind merge --user "Add the scheduling module" --summary "Updated process and embodiment." --artifacts "Scheduler_20260408143025.md,Scheduler_20260408143025.docx"
```

`--kind` is `merge` or `correct`; `--log-name` defaults to `disclosure_revision_log.md`. Each appended record contains actual local and UTC times. Read and append manually if the helper is unavailable; preserve existing entries.

## Optional CNIPA source search

Use this provider only when the confirmed jurisdiction or prior-art scope calls for it; see `prior_art_search.md`. It requires Playwright and Chromium. Its machine-readable stdout contains one `EPUB_HITS_JSON:` record; ASCII diagnostics remain on stderr. Preserve UTF-8 and inspect the actual JSON before treating a call as empty. `cnipa_epub_parse.py` can parse an existing result HTML file without browsing. `cnipa_epub_crawler.py` is a separate debugging/export entrypoint that can save HTML; the normal search wrapper keeps result HTML in memory. Respect service access restrictions and human challenges.
