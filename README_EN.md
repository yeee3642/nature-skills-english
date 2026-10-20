# Nature Skills — English Edition

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

Reusable research workflows for literature discovery, reading, writing, peer review,
statistics, data availability, scientific figures, and presentations.

![Skills](https://img.shields.io/badge/skills-22-0ea5e9)

## 1. About this edition

This is a local English adaptation of [Nature Skills](https://github.com/Yuan1z0825/nature-skills),
based on upstream commit `2a163b95255c608609ff815f3bbc6266591598e2`.
Existing English guidance is retained where applicable. Chinese-only guidance is
translated or condensed into English, and promotional material is omitted.
English is the default language for general deliverables; another language can
be selected explicitly. Language-specific parsing and optional jurisdiction-specific
backends remain available where required by a workflow.

The package contains 22 task skills and the `nature-shared` support package.
Scientific evidence, source attribution, uncertainty, shared references, runtime
scripts, and relevant assets remain part of the skills. Journal-style guidance
does not imply endorsement by Nature or Springer Nature.

## 2. Attribution and licensing

Original project: Yizhe Yuan and Nature Skills contributors. Upstream contributors
include Xin-Rui Ma, Bin Hu, Jiahao8595, and the authors named in individual files.
Keep the original [LICENSE](LICENSE), embedded attribution, and third-party notices.
Some individual skills declare their own licenses in their metadata.

See [EDITION-NOTICE.md](EDITION-NOTICE.md) for the adaptation scope and
`edition-manifest.json` for the per-file modification inventory.

## 3. Choosing a workflow

Start with the task rather than loading every skill. Reading uses `nature-reader`,
`nature-paper-card`, or `nature-paper-xray`; drafting uses `nature-writing`;
editing existing prose uses `nature-polishing`; simulated review uses
`nature-reviewer`; responding to an actual editorial decision uses `nature-response`.
Use specialist skills when the task calls for figures, statistics, data statements,
reference checking, or presentations.

## 4. Quick start

After installing the relevant complete skill directories, make a concrete request:

```text
Use nature-paper-card to analyse this paper in English. Separate the authors'
claims from the evidence and identify unsupported conclusions.
```

```text
Use nature-polishing to improve this paragraph in academic English. Preserve
all numerical values, terminology, evidence boundaries, and qualifications.
```

```text
Use nature-reviewer to evaluate this manuscript. Keep the reviewers independent
until their reports are complete, then synthesise their major concerns.
```

## 5. Local installation

Keep the complete folders under `skills/`, including their references, scripts,
templates, manifests, and assets. Keep `nature-shared` alongside skills that use it.
Do not copy only `SKILL.md`. The directory `nature-proposal-writer` retains the
compatible invocation name `researchwrite`; an installer may use that name.

On Windows, the bundled installer previews or copies this local edition:

```powershell
.\install-local.ps1 -Skill nature-reader,nature-polishing -WhatIf
.\install-local.ps1 -Skill nature-reader,nature-polishing
```

Omit `-Skill` to select the complete collection. Existing destination folders cause
the installer to stop before it copies anything. `-Destination` selects another
skills directory. The installer does not fetch upstream content, change hooks,
configure credentials, or install Python/Node dependencies.

Configure optional dependencies only for the workflows you actually use. API and
institutional-access routes require your own lawful access and local credentials.
Keep credentials outside the repository. Installation of instructions does not
prove that a browser, external provider, rendering tool, or MCP service is ready.

For other agents, reference or copy the same complete local skill directories;
see [the integration guide](docs/open-source-agent-frameworks_EN.md).

## 6. Skill index

| Skill | Purpose |
| --- | --- |
| [`nature-academic-search`](skills/nature-academic-search/README.md) | Multi-source literature search, citation management, and citation-impact audits. |
| [`nature-citation`](skills/nature-citation/README.md) | Find and verify claim-supporting literature within the requested journal scope. |
| [`nature-data`](skills/nature-data/README.md) | Data and Code Availability statements, access plans, and FAIR metadata. |
| [`nature-downloader`](skills/nature-downloader/README.md) | Lawful open-access, publisher-API, and authorized institutional retrieval. |
| [`nature-experiment-log`](skills/nature-experiment-log/README.md) | Evidence-grounded experiment logs from text, images, audio, and local files. |
| [`nature-figure`](skills/nature-figure/README.md) | Scientific figures, panel design, editable exports, and figure quality audits. |
| [`nature-image2ppt`](skills/nature-image2ppt/README.md) | Reconstruct slide images as object-level editable PowerPoint. |
| [`nature-literature-pipeline`](skills/nature-literature-pipeline/README.md) | Literature discovery, screening, close reading, and archival workflows. |
| [`nature-paper-card`](skills/nature-paper-card/README.md) | Structured paper cards with methods, evidence, limitations, and testable ideas. |
| [`nature-paper-to-patent`](skills/nature-paper-to-patent/README.md) | Evidence-grounded invention disclosures and jurisdiction-aware draft support. |
| [`nature-paper-trans`](skills/nature-paper-trans/README.md) | Translate PDF pages into a requested language while retaining page layout. |
| [`nature-paper-xray`](skills/nature-paper-xray/README.md) | Reconstruct a paper's reasoning, design choices, formulas, and evidence limits. |
| [`nature-paper2ppt`](skills/nature-paper2ppt/README.md) | Paper-based research presentations with source figures and speaker notes. |
| [`nature-polishing`](skills/nature-polishing/README.md) | Polish or translate existing academic prose without changing evidence or meaning. |
| [`nature-proposal-writer`](skills/nature-proposal-writer/README.md) | Research proposals, feasibility checks, and evidence-bounded planning. |
| [`nature-reader`](skills/nature-reader/README.md) | Source-grounded paper readers with aligned text, figures, equations, and locators. |
| [`nature-ref-verifier`](skills/nature-ref-verifier/README.md) | Field-by-field reference verification with explicit discrepancies and uncertainty. |
| [`nature-response`](skills/nature-response/README.md) | Reviewer replies, revision cover letters, and marked-manuscript packages. |
| [`nature-reviewer`](skills/nature-reviewer/README.md) | Independent mock peer review of significance, methods, evidence, and limitations. |
| [`nature-social-science`](skills/nature-social-science/README.md) | Research questions, literature maps, evidence routes, feasibility, and argument audits. |
| [`nature-statistics`](skills/nature-statistics/README.md) | Statistical-reporting audits covering units, replication, uncertainty, and tests. |
| [`nature-writing`](skills/nature-writing/README.md) | Manuscript arguments, section drafting, restructuring, and initial submissions. |

[`nature-shared`](skills/nature-shared/README.md) supplies shared reference modules
and is not a standalone task skill.

## 7. Validation and maintenance

Run structural validation with Python 3.11 or later from the package directory:

```text
python scripts/validate-repository.py
python scripts/validate-skill-metadata.py
python scripts/validate-readme-mirror.py
python scripts/validate-english-edition.py
```

The English-edition check audits text and path names for literal Han ideographs,
parses structured files, compiles Python syntax without executing workflows, and
checks literal local Markdown targets. Escaped Unicode used for input recognition
is retained as runtime data rather than prose.

This edition does not automatically track upstream. Review and reapply the English
adaptation before replacing it with a newer upstream version. Runtime smoke tests
and unconfigured external capabilities are described in `VALIDATION.md`.
