# Prior-art search (Step 5)

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

Search before drafting the closest-prior-art comparison. Choose public patent databases and scholarly sources appropriate to the confirmed jurisdiction and technical subject. Do not assume a China-only search or equate an empty result with novelty. Use Google Patents, official patent-office records, DOI/publisher pages, and preprint records as applicable. An incomplete or unavailable search must be recorded honestly.

## Optional CNIPA published-patent route

For an explicitly requested Chinese jurisdiction or relevant Chinese prior art, the bundled `scripts/disclosure/cnipa_epub_search.py` searches `http://epub.cnipa.gov.cn/` through Playwright and parses the result HTML in memory. Install `scripts/disclosure/requirements-cnipa.txt` and Chromium only when this route is needed. Do not bypass access restrictions or a challenge the service requires a human to complete.

Form two to eight topic-relevant semantic search units. Keep meaningful technical terms together; avoid generic words, single characters, or an unsegmented long sentence. Run each intended unit as a separate bounded invocation, then merge results by `pub_number`, falling back to `link` or a stable title. The helper only splits whitespace; it does not segment Chinese prose automatically. CNIPA queries may use the source language when necessary, even though this skill's instructions and default disclosure are English.

A successful stdout record is one `EPUB_HITS_JSON:` line containing a JSON array. `EPUB_NOTE:`, `EPUB_MERGE:`, and `EPUB_HINT:` diagnostics go to stderr; they do not themselves mean failure. Use UTF-8 on Windows (`python -X utf8`) and keep streams distinct. If dependencies are missing, a call fails or times out, results are empty, or matches are irrelevant, use another appropriate public source and record the limitation. Never claim the unavailable route succeeded.

## Read and verify each source

For each relevant patent or paper, record its publication identifier, title, technical mechanism, application, demonstrated or stated limitations, and at least one verified public URL matching the record. Open the actual record before relying on it. Do not guess URLs or invent a mechanism from the title or number.

If a CNIPA result includes a nonempty `abstract`, read it fully before discussing its field, problem, modules, process, or effect. Summarize it in your own words and do not contradict it. If the abstract is absent, note this and inspect a detail page or another verifiable publication record before technical comparison. The same source discipline applies to all databases.

Prefer stable publication records (for example, a confirmed Google Patents publication page), publisher/DOI landing pages, and official preprint abstract pages over transient search-session URLs. Include the search date, actual queries, databases, and remaining coverage limits in search notes. Compare supported features, not marketing language, and distinguish technical differentiation from a legal patentability conclusion.

## Writing Chapter 1.1

The disclosure states the databases actually used, the substantive query concepts, the closest records, and the supported differences and limitations. Do not expose internal helper names, tool-routing details, or browser automation diagnostics in the technical narrative. End with a scoped search summary and the invention's supported difference; avoid wholesale copying of abstracts or claims.
