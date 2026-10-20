# Anomaly Log

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

Record observed anomalies for quality control and troubleshooting.

```markdown
---
date: YYYY-MM-DD
related_exp: EXP-ID
anomaly_type: equipment-failure / handling-error / unexpected-result / safety-event
severity: low / medium / high
status: pending / resolved / recheck-needed
---

## Description

[Objective description of what was observed.]

## Impact

[Known or uncertain effects on the experiment.]

## Response

[Actions actually taken.]

## Follow-up

[Proposed checks, responsible person, and status.]
```

Check for anomalies after each experiment, add a linked record when relevant,
and periodically revisit unresolved items.
