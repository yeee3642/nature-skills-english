---
name: nature-experiment-log
description: "Turn experiment images, audio transcripts, text, and local files into traceable Markdown lab logs with YAML frontmatter. Optional Feishu CLI and Obsidian integrations are supported."
license: MIT
metadata:
  author: Jiahao8595
  hermes:
    tags: [research, experiment, logging, feishu, obsidian, automation]
    related_skills: [nature-literature-pipeline, feishu-cli-integration, obsidian]
---

# Experiment Log

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

## Contents

- [Inputs and outputs](#inputs-and-outputs)
- [Workflow](#workflow)
- [Directory convention](#directory-convention)
- [Identifier rules](#identifier-rules)
- [Optional Obsidian integration](#optional-obsidian-integration)
- [Examples](#examples)
- [Optional Feishu CLI integration](#optional-feishu-cli-integration)
- [Customization](#customization)


Use this skill when the user supplies raw experimental records as images, audio,
transcripts, text, or local files. Write English logs by default; use another
language only when requested. The local Markdown workflow requires neither Feishu
nor Obsidian.

## Inputs and outputs

Read uploads or the local paths supplied by the user. Use available vision,
transcription, and text tools as appropriate; do not assume a named integration
exists. Retrieve Feishu group messages only when that optional source is requested
and configured. A Feishu bot must belong to the target group and have the relevant
`im:message`, `im:message.group_msg`, and `im:resource` permissions.

Save logs and copies of raw attachments under the user-specified local output
directory or Obsidian vault. If no directory is provided, return save-ready
Markdown rather than choosing a location on the user's behalf. Never invent
temperatures, sample identifiers, durations, instrument settings, or results.
Ask about ambiguous information or mark it `AUTHOR_INPUT_NEEDED`.

## Workflow

1. Read the supplied raw records and extract structured information.
2. Resolve missing or ambiguous facts needed to identify the experiment.
3. Establish the output directory, experiment ID, and sample/batch IDs.
4. Write `{OUTPUT_ROOT}/experiment-logs/{system}/{type}/{exp_id}.md`.
5. Archive copies of raw attachments under
   `{OUTPUT_ROOT}/raw/experiments/YYYY.MM.DD_description_EXPID/` and link them from
   the log. Preserve source files and record their provenance.
6. Update the experiment index if enabled; record anomalies separately with links
   to the affected experiment.
7. Report the exact generated-file and raw-material locations.

Separate observed results from interpretations and proposed next steps. Do not
convert an uncertain recollection into a confirmed condition.

## Directory convention

```text
{OUTPUT_ROOT}/
  raw/experiments/YYYY.MM.DD_description_EXPID/
    notes.md
    images/
    audio/
  experiment-logs/
    experiment-index.md
    anomaly-log.md
    {system}/{experiment-type}/{exp_id}.md
    common/equipment-tracking.md
```

Adapt this convention to an existing vault instead of moving its contents.

## Identifier rules

Experiment ID: `{SYSTEM}-{DEVICE}-YYMMDD-{SEQUENCE}`, with the daily sequence
starting at `001`. System codes are laboratory-defined, for example `CL`, `NO`,
`OX`, and `HY`.

Sample batch ID: `{SYSTEM}-{CANDIDATE}-B{SEQUENCE}`. Preserve the same `sample_batch`
value when one batch appears in several experiments. Existing salt-specific
examples use `salt_batch`; keep a laboratory's established schema consistent.

| Code | Device | Typical use |
|---|---|---|
| M | Muffle furnace | Heat treatment and immersion corrosion |
| T | Tube furnace | Atmosphere control, dehydration, thermal stability |
| E | Electrochemical workstation | CV, SWV, EIS |
| G | Glovebox | Preparation, weighing, sampling |
| F | Controlled-atmosphere furnace | Precise atmosphere control |
| B | General equipment | Drying, cleaning, specimen preparation |

Extend the codes for the actual laboratory rather than forcing this list.

## Optional Obsidian integration

Use plain Markdown and YAML frontmatter. If Dataview is available, copy the
following templates into the corresponding vault paths to enable queries:

| Target file | Template | Purpose |
|---|---|---|
| `experiment-logs/experiment-index.md` | `templates/experiment-index.md` | Experiment dashboard |
| `experiment-logs/anomaly-log.md` | `templates/anomaly-log.md` | Anomaly tracking |
| `experiment-logs/common/equipment-tracking.md` | `templates/equipment-tracking.md` | Equipment and reagent records |

Load these templates only when an index, anomaly record, or equipment tracker is
needed. Optional integrations must not block ordinary local logs.

## Examples

Load the matching example when a concrete field layout is useful. All data in
these examples are fictional and are not laboratory instructions or real results.

| Reference | Experiment type |
|---|---|
| `references/example-log.md` | Material immersion corrosion |
| `references/example-electrochemical.md` | CV window characterization |
| `references/example-thermal-stability.md` | Thermal-stability testing |

## Optional Feishu CLI integration

When requested, use the separately configured `feishu-cli-integration` skill.

```bash
lark-cli im +chat-messages-list --chat-id oc_*** --page-size 30 --sort asc
lark-cli im +messages-resources-download --message-id *** --file-key *** --type image --output <relative-path>
```

The resource-download `--output` argument accepts a relative path. First change
to the selected raw-material archive directory. Obtain group IDs and bot access
from the integration's configuration; do not infer them.

## Customization

System codes, experiment categories, YAML fields, device codes, and the output
root may follow the user's laboratory conventions. Preserve cross-record links
and identifiers when changing presentation.
