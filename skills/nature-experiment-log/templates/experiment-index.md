# Experiment Index

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

Optional Dataview dashboard for experiment logs.

```dataview
TABLE date, salt_system, exp_type, material, anomaly
FROM "experiment-logs"
WHERE exp_id
SORT date DESC
```

Place this file in the vault's `experiment-logs/` directory. Logs must contain
YAML frontmatter with fields such as `exp_id`, `date`, `salt_system`, and
`exp_type`. Open it in Obsidian with Dataview enabled.

Customize the fields for the laboratory. Example filters:

```dataview
WHERE salt_system = "chloride"
WHERE anomaly = true
WHERE date >= date(2026-01-01)
```

Use one appropriate filter or combine conditions in a valid Dataview query.
