# English Edition Validation

Validated locally on Windows on 2026-10-20. The upstream reference is commit
`2a163b95255c608609ff815f3bbc6266591598e2` of Yuan1z0825/nature-skills.

## Language and package integrity

The complete package has 22 task skills and one shared support package. All
UTF-8 source text and path names pass the literal-Han scan. English prose was
also reviewed for residual forced Chinese output, rather than relying only on
character counting. General workflows default to English; explicitly selected
translation, source-language parsing, and jurisdiction-specific routes remain.

The final scan covered 811 UTF-8 text files, including 221 Python files and
160 literal local Markdown targets, with zero issues. Node and shell syntax
checks passed for all 46 bundled MJS and shell files.

All skill frontmatter, interface metadata, manifest routes, README skill indices,
local Markdown targets, JSON/TOML files, and Python syntax were checked. Modified
source paths and SHA-256 hashes are recorded in `edition-manifest.json`. Runtime
and data files use that inventory for change notices without disturbing byte-based
runtime parity checks. Test caches are excluded from the archive and inventory.

Scientific PNG examples were reviewed in five contact sheets; their visible
labels appeared English. This was an overview inspection, not an OCR audit of
every tiny raster label. The three bundled PDF plots contain no extracted Han
text. Scientific figures and plots are retained unchanged.

## Existing tests and smoke checks

| Area | Observed result |
| --- | --- |
| Complete root tooling/content contracts, including the six social-science tests | 163 passed, 16 subtests passed |
| Citation, reviewer-response, and mock-review tests | 42 passed |
| Patent disclosure and validation tests | 19 passed |
| PDF translation attempt/review/publication workflow | 36 passed, 10 subtests passed |
| Shared consistency and presentation bounds | 14 passed |
| Proposal export/source-preservation tests | 12 passed |
| Downloader Node tests | 121 of 122 passed; one upstream Windows limitation below |
| Downloader Python tests | 18 of 19 passed; one upstream Windows limitation below |
| Image-to-PowerPoint distinct tests across full run and targeted reruns | 177 of 183 passed; six upstream renderer failures below |
| Explicit-provider downloader routing and CLI contracts | 17 of 17 passed, included in downloader evidence |

Reader mathematics checks, English and legacy translation-line handling,
English claim-reference and figure-description checks, tokenization equivalence,
and offline OCR-to-editable-PowerPoint conversion passed. English-edition
validator smoke checks cover encoded local paths, URL queries, email/external
links, malformed JSON, and Han detection. Installer checks cover preview mode,
PowerShell-relative destinations, complete-directory copying, hash equality,
and collision rejection before copying any selected folder.

These test groups overlap in places; their counts should not be summed into a
single claimed test total. Required dependencies were taken from existing local
runtimes or placed under the task's `work/` directory, without a global install.

## Observed environment limitations

Both downloader failures test POSIX owner-only permission bits. On this Windows
host the reported mode differs from POSIX `0600`; both failures reproduce on the
untouched upstream code. They are not reported as passing.

All six image-to-PowerPoint rendering failures also reproduce on the untouched
upstream subset. `PowerPoint.Application` is not registered (`0x80040154`,
`REGDB_E_CLASSNOTREG`), and LibreOffice is absent. File reconstruction and the
offline editable-PowerPoint path were exercised, but rendered visual evidence
requiring those applications could not be completed on this host. The upstream
doctor's readiness message does not establish a working renderer.

No live institutional login, paid provider, external MCP service, scheduled
delivery, journal submission, patent filing, was tested. Remote publication is verified separately from runtime capabilities.
This adaptation has not been installed into the user's active skills directory.

## Publication preparation

The inherited star-history workflow is manual-only in this repository. Its
periodic write schedule was removed before publication. The remaining CI
workflows are retained.
