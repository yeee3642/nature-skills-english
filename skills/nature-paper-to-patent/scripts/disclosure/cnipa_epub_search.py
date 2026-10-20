# -*- coding: utf-8 -*-
"Search CNIPA and parse results in memory. stdout emits one EPUB_HITS_JSON record; ASCII diagnostics use stderr. Split argv on whitespace, query each semantic unit, and merge by publication number. Source-language terms are accepted; no automatic Chinese word segmentation is performed."
from __future__ import annotations

import json
import os
import sys

_MAX_TERMS = 8


def _ensure_utf8_stdio() -> None:
    "Ensure utf8 stdio."
    for stream in (sys.stdout, sys.stderr):
        try:
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError, TypeError):
            pass


def _terms_from_argv(argv: list[str]) -> list[str]:
    "Terms from argv."
    terms: list[str] = []
    for a in argv:
        for part in (a or "").split():
            p = part.strip()
            if p:
                terms.append(p)
    return terms


def _dedupe_hits(hits_lists: list) -> list:
    from cnipa_epub_parse import EpubSearchHit

    seen: set[str] = set()
    out: list[EpubSearchHit] = []
    for hits in hits_lists:
        for h in hits:
            key = h.pub_number or h.link or (h.title or "")[:120]
            if key in seen:
                continue
            seen.add(key)
            out.append(h)
    return out


def _usage() -> None:
    print("usage: python scripts/disclosure/cnipa_epub_search.py <term> [more terms...]", file=sys.stderr)
    print(
        "whitespace splits to multiple terms; one Playwright run per term; merge by pub_number.",
        file=sys.stderr,
    )
    print('example: python scripts/disclosure/cnipa_epub_search.py "scheduler"', file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    _ensure_utf8_stdio()
    argv = argv if argv is not None else sys.argv[1:]
    terms = _terms_from_argv(argv)
    if not terms:
        _usage()
        return 2
    if len(terms) > _MAX_TERMS:
        print(
            "ERROR: too many terms after split (%d > %d); shorten or run in batches."
            % (len(terms), _MAX_TERMS),
            file=sys.stderr,
        )
        return 2

    os.environ.setdefault("EPUB_WAF_MAX_WAIT_SEC", "180")

    try:
        import playwright  # noqa: F401
    except ImportError:
        print(
            "ERROR: pip install -r scripts/disclosure/requirements-cnipa.txt && python -m playwright install chromium",
            file=sys.stderr,
        )
        return 1

    from cnipa_epub_crawler import search_epub_keyword
    from cnipa_epub_parse import hits_to_jsonable

    multi = len(terms) > 1
    last_html = ""
    all_batches: list = []

    try:
        for kw in terms:
            html, hits = search_epub_keyword(kw)
            last_html = html
            all_batches.append(hits)
    except Exception as e:
        print("CNIPA_EPUB_ERROR:", e, file=sys.stderr)
        return 1

    if multi:
        hits = _dedupe_hits(all_batches)
        print(
            "EPUB_MERGE: terms=%d merged_hits=%d" % (len(terms), len(hits)),
            file=sys.stderr,
            flush=True,
        )
    else:
        hits = all_batches[0]

    if not hits and last_html and len(last_html) < 20_000:
        if multi:
            print(
                "EPUB_HINT: 0 hits after multi-term run; try broader terms or WebSearch (prior_art_search.md)",
                file=sys.stderr,
                flush=True,
            )
        else:
            print(
                "EPUB_HINT: 0 hits; try more terms (space-separated) or WebSearch",
                file=sys.stderr,
                flush=True,
            )

    print(
        "EPUB_NOTE: html_bytes=%d disk=0" % len(last_html),
        file=sys.stderr,
        flush=True,
    )
    # stdout，/Agent （，）
    print(
        "EPUB_HITS_JSON:",
        json.dumps(hits_to_jsonable(hits), ensure_ascii=False),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
