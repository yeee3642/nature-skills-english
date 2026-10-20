# Project-document scan (Step 2)

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

Adapt the search paths to the actual project. Inspect patent-point analyses and existing disclosures first, then detailed designs, complete workflows and comparison documents, core implementation code, and system architecture. In a large repository, locate likely evidence before reading whole modules. Record stable file and section locators so technical statements can be traced without exposing internal names in the final disclosure.

Include Office documents in the source inventory. Convert OOXML `.docx` and `.pptx` files before reading their content; do not omit them merely because Markdown is easier to inspect. Legacy `.doc` and `.ppt` need an explicit conversion to a supported format first.

```bash
python scripts/disclosure/docx_to_md.py -i source/design.docx -o work/design.md
python scripts/disclosure/pptx_to_md.py -i source/review.pptx -o work/review.md
```

Run from the skill directory or use absolute script paths. Converted Markdown and its sibling `_media/` directory form one evidence unit. Inspect tables, numbered lists, slide titles and text, speaker notes, and relevant embedded figures. Preserve the original source files. Conversion may omit complex objects or alter reading order, so check the source when an important point is missing or ambiguous.

Do not OCR every standalone raster asset by default. Inspect a separate image when the user identifies it or it is critical and absent from converted Office material. Treat source-supported facts as evidence; implementation ideas inferred during analysis remain proposals requiring inventor confirmation.
