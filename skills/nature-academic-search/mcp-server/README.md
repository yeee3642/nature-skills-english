# Unified Academic Search MCP Server

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

This MCP server integrates CrossRef, PubMed, arXiv, Scopus, and ScienceDirect.

## Tools

| Tool | Function |
|---|---|
| `search_papers` | Search multiple sources concurrently |
| `get_paper_by_id` | Retrieve details by DOI, PMID, or arXiv ID |
| `get_citation` | Format citations in APA, Nature, IEEE, and other styles |
| `lookup_mesh` | Look up MeSH vocabulary |
| `search_scopus` | Run advanced Scopus searches |
| `get_scopus_abstract` | Retrieve Scopus abstracts and detailed metadata |
| `get_scopus_citation_overview` | Retrieve Scopus citation overviews |
| `search_scopus_authors` / `get_scopus_author` | Search and retrieve author records |
| `search_scopus_affiliations` / `get_scopus_affiliation` | Search and retrieve institution records |
| `search_scopus_serial_titles` / `get_scopus_serial_title` | Search journals and serial-title details |
| `get_scopus_plumx_metrics` | Retrieve PlumX metrics |
| `search_sciencedirect` | Search ScienceDirect |
| `get_sciencedirect_article_metadata` | Retrieve ScienceDirect article metadata |

## Configuration

- `PUBMED_EMAIL`: required by NCBI for PubMed use.
- `NCBI_API_KEY`: optional, for higher rate limits.
- Elsevier, Scopus, and ScienceDirect reuse the local `pybliometrics` configuration,
  normally `~/.config/pybliometrics.cfg`. Keep credentials out of repository files.

`search_papers` searches CrossRef, PubMed, and arXiv by default. Scopus and
ScienceDirect are optional providers. Elsevier APIs are called only when `sources`
explicitly includes `scopus` or `sciencedirect`, or when a dedicated tool is used.
This avoids unintentionally consuming Elsevier quotas. Missing local configuration
is reported for the relevant source in the returned JSON `errors` field.

Configuration file: `config.toml`.

## Usage

The plugin starts an isolated runtime in this form:

```bash
uv run --no-project --directory <mcp-server> --with ... python academic_search_server.py
```

The academic-search workflow invokes these tools.
