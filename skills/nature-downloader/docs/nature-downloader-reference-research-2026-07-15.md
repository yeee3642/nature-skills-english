# Nature Downloader: upstream implementation notes

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

Historical source review dated 2026-07-15. This document summarizes two pinned upstream implementations; it does not certify the current downloader or current provider behavior.

## Sources and scope

`ShZhao27208/Aut_Sci_Download` at `5e0de4cf68ab48dce8763fe7ca76a6f29874afc2` (2026-06-29, MIT) was reviewed for CNKI institutional access. `kermitt2/article_dataset_builder` at `920fe298a81061e8a26d55d13829ccb6deb6501c` (2023-10-03, package 0.2.6, Apache-2.0) was reviewed for open-access discovery, state, downloads, and outputs. Preserve their original licenses when adapting actual code.

The useful architectural seams are an institution-specific access adapter and a source-independent OA candidate pipeline. Neither repository should be copied wholesale into this interactive skill.

## Institutional access observations

Aut_Sci_Download separates FSSO access from WebVPN transport. Users authenticate themselves; subsequent requests reuse their authorization. Its source exports cookies into local JSON and, for one WebVPN implementation, rewrites provider URLs. Those are historical observations, not instructions to export credentials or a claim of universal institution support. This edition uses the user's authorized browser session and does not export cookies or collect institution passwords.

Keep transport and provider differences inside adapters. Validate authorization explicitly: HTTP 200 plus a provider keyword can still be an anonymous page or an error. Vendor-specific proxy URL formats must not be treated as a universal protocol. Sensitive session material requires appropriate local protection; ordinary plaintext configuration is not a credential-storage design.

CNKI search results include title, authors, source, year, detail URL, `filename`, and `dbcode`. Prefer strong provider identifiers over a title alone. A fallback parser may recover only a URL and must flag missing metadata. Internal query fields, selectors, and URL formats belong in a tested provider adapter. The assumption that a `v` query parameter is a reliable filename was not established by this review. Resolve ambiguous title/author/year matches before choosing a document.

The source tries newer and older detail pages, prefers PDF over CAJ, and checks for login pages, file signatures, and a minimum size. Retain the distinction between transport success and valid content. The reviewed implementation could accept sufficiently large content without a recognized PDF/CAJ signature, so its success result cannot be adopted uncritically. A cache hit needs content validation and metadata, rather than a filename and size alone. Write downloads to temporary files and publish them atomically after validation. Return provider, access mode, actual format, bytes, final path, and a typed failure.

## Open-access observations

article_dataset_builder is a batch dataset harvester for DOI, PMID, PMCID, or CORD-19 records. It aggregates metadata, resolves OA files, and optionally runs TEI conversion, thumbnail generation, and S3 output. It is not an institution-authenticated browser or a publisher subscription API.

Normalize DOI prefixes, whitespace, and case. Map strong identifiers onto one record and track metadata resolution, OA candidates, validated PDF, structured full text, and supplementary material separately. Metadata sources answer which article is intended; PMC, Unpaywall, and lawful repositories answer where an accessible copy may exist. Preserve failed and incomplete stages for resumable, idempotent work.

The source uses biblio-glutton and Crossref, UUID records, and LMDB identifier mappings. Its documented metadata fallback and implementation do not always agree. The reviewed identifier-reuse path also exposed a bytes/string assumption. Treat the architecture as a useful idea while independently testing fallback and resume behavior; biblio-glutton and LMDB are not mandatory dependencies for this skill.

Its historical candidate waterfall checks a special-purpose local mapping, existing files, PMC OA archives, Unpaywall locations, and metadata OA links. Use current article-level OA evidence rather than publisher names or DOI prefixes to infer accessibility. Preserve all lawful candidates with repository, version, license, PDF-link status, and selection reason. A PMC archive may contain PDF, JATS/NXML, and attachments; model it as a resource bundle.

Handle absent `best_oa_location` values explicitly. Distinguish personal access, OA status, and redistribution permission; one does not prove the others. The reviewed implementation selected a first suitable URL and did not preserve all provenance, so this edition should retain richer candidate records.

The source separates URL selection from multiple transfer implementations and validates MIME rather than trusting an extension. Keep that separation and validation. Do not inherit disabled TLS verification, shell-interpolated download commands, swallowed exceptions, unrestricted retries, or challenge-bypass assumptions. Respect provider limits and route cases needing a real user session to authorized browser access.

## Unified design principles

The request router normalizes identifiers and selects an appropriate provider. CNKI-specific page interpretation remains optional provider logic. The OA subsystem resolves lawful candidate locations. Publisher APIs and institutional Web Access retain their own credentials, entitlement checks, and provenance. Supporting Information enters the pipeline only after the user chooses it.

Each document manifest should retain the original request, normalized DOI/PMID/PMCID/provider identifiers, language, OA assessment and timestamp, candidate and final URLs, selected provider and access mode, SHA-256, MIME, byte count, actual file format, source-supplied license/version, SI choice and attachment outcomes, typed errors, and the next useful action. Remove secret values from all persisted or displayed records.

Useful failure distinctions include `credentials_missing`, `session_expired`, `not_entitled`, `oa_not_found`, `metadata_ambiguous`, `download_link_changed`, `challenge_required`, `invalid_content`, `rate_limited`, and `si_not_requested`. A missing OA copy does not mean an article does not exist; a valid login does not establish entitlement; HTTP success does not establish a valid PDF.

For interactive use, begin with a lightweight manifest rather than importing an entire LMDB/S3/GROBID dataset stack. Consider a queue or SQLite only when batch requirements justify them. Preserve limited concurrency and explicit retry state.

## Pinned evidence links

These links are retained from the historical source review and have not been revalidated against current provider behavior.

- [Pinned source 1](https://github.com/ShZhao27208/Aut_Sci_Download/tree/5e0de4cf68ab48dce8763fe7ca76a6f29874afc2)
- [Pinned source 2](https://github.com/ShZhao27208/Aut_Sci_Download/blob/5e0de4cf68ab48dce8763fe7ca76a6f29874afc2/pyproject.toml#L1-L12)
- [Pinned source 3](https://github.com/ShZhao27208/Aut_Sci_Download/blob/5e0de4cf68ab48dce8763fe7ca76a6f29874afc2/LICENSE#L1-L20)
- [Pinned source 4](https://github.com/kermitt2/article_dataset_builder/tree/920fe298a81061e8a26d55d13829ccb6deb6501c)
- [Pinned source 5](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/setup.py#L3-L28)
- [Pinned source 6](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/LICENSE#L1-L12)
- [Pinned source 7](https://github.com/ShZhao27208/Aut_Sci_Download/blob/5e0de4cf68ab48dce8763fe7ca76a6f29874afc2/README.md#L135-L142)
- [Pinned source 8](https://github.com/ShZhao27208/Aut_Sci_Download/blob/5e0de4cf68ab48dce8763fe7ca76a6f29874afc2/scripts/cnki_download.py#L70-L102)
- [Pinned source 9](https://github.com/ShZhao27208/Aut_Sci_Download/blob/5e0de4cf68ab48dce8763fe7ca76a6f29874afc2/scripts/webvpn_crypto.py#L14-L58)
- [Pinned source 10](https://github.com/ShZhao27208/Aut_Sci_Download/blob/5e0de4cf68ab48dce8763fe7ca76a6f29874afc2/scripts/cnki_download.py#L105-L116)
- [Pinned source 11](https://github.com/ShZhao27208/Aut_Sci_Download/blob/5e0de4cf68ab48dce8763fe7ca76a6f29874afc2/scripts/cnki_download.py#L119-L142)
- [Pinned source 12](https://github.com/ShZhao27208/Aut_Sci_Download/blob/5e0de4cf68ab48dce8763fe7ca76a6f29874afc2/scripts/cnki_download.py#L145-L222)
- [Pinned source 13](https://github.com/ShZhao27208/Aut_Sci_Download/blob/5e0de4cf68ab48dce8763fe7ca76a6f29874afc2/scripts/cnki_download.py#L245-L335)
- [Pinned source 14](https://github.com/ShZhao27208/Aut_Sci_Download/blob/5e0de4cf68ab48dce8763fe7ca76a6f29874afc2/scripts/cnki_download.py#L317-L335)
- [Pinned source 15](https://github.com/ShZhao27208/Aut_Sci_Download/blob/5e0de4cf68ab48dce8763fe7ca76a6f29874afc2/scripts/cnki_download.py#L338-L403)
- [Pinned source 16](https://github.com/ShZhao27208/Aut_Sci_Download/blob/5e0de4cf68ab48dce8763fe7ca76a6f29874afc2/scripts/cnki_download.py#L406-L459)
- [Pinned source 17](https://github.com/ShZhao27208/Aut_Sci_Download/blob/5e0de4cf68ab48dce8763fe7ca76a6f29874afc2/scripts/cnki_download.py#L462-L501)
- [Pinned source 18](https://github.com/ShZhao27208/Aut_Sci_Download/blob/5e0de4cf68ab48dce8763fe7ca76a6f29874afc2/scripts/config.py#L16-L18)
- [Pinned source 19](https://github.com/ShZhao27208/Aut_Sci_Download/blob/5e0de4cf68ab48dce8763fe7ca76a6f29874afc2/pyproject.toml#L7-L12)
- [Pinned source 20](https://github.com/ShZhao27208/Aut_Sci_Download/blob/5e0de4cf68ab48dce8763fe7ca76a6f29874afc2/scripts/config.py#L85-L143)
- [Pinned source 21](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/Readme.md#L4-L38)
- [Pinned source 22](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/Readme.md#L8-L13)
- [Pinned source 23](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/config.json)
- [Pinned source 24](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L1368-L1373)
- [Pinned source 25](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L286-L336)
- [Pinned source 26](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L737-L804)
- [Pinned source 27](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L1441-L1453)
- [Pinned source 28](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/Readme.md#L94-L108)
- [Pinned source 29](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L558-L567)
- [Pinned source 30](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L1133-L1140)
- [Pinned source 31](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L889-L945)
- [Pinned source 32](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L207-L234)
- [Pinned source 33](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L157-L205)
- [Pinned source 34](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/Readme.md#L15-L15)
- [Pinned source 35](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L1468-L1492)
- [Pinned source 36](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L1425-L1439)
- [Pinned source 37](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L1617-L1675)
- [Pinned source 38](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L1328-L1359)
- [Pinned source 39](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L1530-L1583)
- [Pinned source 40](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L1494-L1528)
- [Pinned source 41](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L530-L575)
- [Pinned source 42](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/Readme.md#L110-L110)
- [Pinned source 43](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L1024-L1038)
- [Pinned source 44](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L1041-L1131)
- [Pinned source 45](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/article_dataset_builder/harvest.py#L396-L437)
- [Pinned source 46](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/setup.py#L14-L28)
- [Pinned source 47](https://github.com/kermitt2/article_dataset_builder/blob/920fe298a81061e8a26d55d13829ccb6deb6501c/Readme.md#L40-L57)
