---
name: nature-ref-verifier
description: >-
  Cross-check academic references against multiple sources, compare authors,
  titles, publication years, volume/issue, pages, and DOIs, and produce an
  evidence-linked correction report. Supports single citations, whole
  bibliographies, BibTeX, and optional Zotero correction workflows.
---

# Academic Reference Verifier

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

## Contents

- [1. Parse the input](#1-parse-the-input)
- [2. Retrieve and cross-check sources](#2-retrieve-and-cross-check-sources)
- [3. Compare fields and classify differences](#3-compare-fields-and-classify-differences)
- [4. Record confidence](#4-record-confidence)
- [5. Deliver a correction report](#5-deliver-a-correction-report)
- [Optional Zotero updates](#optional-zotero-updates)
- [Limits and fallbacks](#limits-and-fallbacks)


Write reports in English by default. Load `references/common-patterns.md` when
handling repeated metadata errors, DOI/title conflicts, author-order differences,
pagination drift, or uncertainty wording. `manifest.yaml` records the same
on-demand routing; keep new resources discoverable from both places.

Use for pre-submission reference checks, reviewer-raised citation errors,
bibliography migrations, and library maintenance. Verification is distinct from
finding new references or choosing citations for a claim.

## 1. Parse the input

Accept a manuscript bibliography, an individual citation, a Zotero item key, or a
BibTeX file. Preserve original reference numbering and item keys. Extract the DOI
when present and parse author order, title, year, journal/proceedings, volume,
issue, pages or article number, and publication version.

## 2. Retrieve and cross-check sources

For a DOI-bearing item, begin with the available registry record, for example
`https://api.crossref.org/works/<DOI>`. Compare the returned title, authors, and
publication fields with the citation. A resolving DOI that identifies a different
paper is a substantive mismatch. A Crossref 404 alone does not prove the DOI is
invalid: registry coverage, publisher records, legacy identifiers, and the DOI
resolver must also be considered.

| Source | Use |
|---|---|
| Crossref or the relevant DOI registry | DOI metadata and identity checks |
| Publisher page or IEEE Xplore | Authoritative published-version metadata and legacy records |
| General academic/web search | Title-plus-author fallback and finding the authoritative source |
| Institutional repositories or national databases | Theses, regional publications, and non-DOI records |
| Configured Zotero library | Compare the user's stored metadata with verified records |

CNKI or Wanfang may be useful for explicitly requested Chinese-source references;
they are optional sources, not mandatory dependencies. Use only the available,
authorized integrations and report access gaps.

When useful, divide a large list into independent batches of about 10–15 items.
Keep reference IDs stable, deduplicate requests, and combine results only after
each batch identifies its sources and uncertainties. Do not promise a fixed
runtime or coverage percentage.

## 3. Compare fields and classify differences

| Severity | Examples and interpretation |
|---|---|
| Critical | A different paper under the cited DOI; wrong first author or author order; missing authors in an allegedly complete list; substantive title mismatch; wrong page range; article-number letters confused with digits |
| Warning | Online-first versus final metadata drift; issue missing; a small pagination difference; uncertain middle initials; historical publisher-name differences |
| Information | Harmless title case, supported journal abbreviations, punctuation, or equivalent formatting under the target style |

Use the actual meaning and source conflict to set severity. Page-count thresholds
are triage cues, not a reason to call an incorrect field harmless. An intentionally
abbreviated author list using `et al.` is not missing-author corruption.

Preserve distinct online-publication year, issue/volume year, and conference year
where applicable. Digits embedded in a DOI do not independently establish the
publication year. Prefer the official final record for the version being cited;
explain disagreements with a registry rather than automatically overwriting it.

## 4. Record confidence

| Status | Meaning |
|---|---|
| Verified | Authoritative evidence supports the record and available independent checks agree |
| Check suggested | A meaningful discrepancy remains or a field needs human judgment |
| Needs fix | Evidence supports a substantive correction |
| Unverifiable | Available sources do not support a reliable determination |

Keep access failure, absence from one index, and a demonstrated metadata error
separate. Never invent a replacement field for an unverifiable record.

## 5. Deliver a correction report

Include the checked-item count and status totals, followed by an evidence table:

| Reference | Field | Original | Verified value or uncertainty | Severity | Source |
|---|---|---|---|---|---|
| [N] | DOI/title/authors/etc. | Supplied value | Supported correction or unresolved issue | Critical/warning/info | Direct source link |

Provide a corrected BibTeX file or patch when requested. Preserve citation keys
unless a change is required and documented. Distinguish proposed corrections from
changes actually written to a library.

## Optional Zotero updates

Confirm that the items are present in the intended library before proposing or
performing updates. A bibliography may originate outside Zotero. Use the
configured supported interface and its actual capabilities; do not assume a local
HTTP wrapper permits updates. The local Zotero HTTP API may be read-only, while
an authenticated Web API integration such as pyzotero can support writes.

Library writes require the user's requested scope and suitable credentials. Never
print API keys. A connector endpoint that adds items is not an update mechanism
for existing records. Do not modify the live `zotero.sqlite` database as a routine
fallback. If an authorized correction cannot be applied safely, deliver a
reviewable patch and explain the limitation.

## Limits and fallbacks

Theses, internal reports, manuals, patents, and old proceedings may have incomplete
metadata. Verify the issuing organization, document/version identity, accessible
source, and available fields without claiming a complete metadata audit. Switch
search sources when coverage is poor. Optional tools include pyzotero, Zotero
connectors, academic search, and authenticated regional databases; ordinary web
search and publisher pages remain useful fallbacks.
