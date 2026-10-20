# Literature Digest Format

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

Use this for an English digest prepared for the user's selected destination.
Feishu, Telegram, or another configured messaging integration is optional. A
completed draft does not itself authorize external delivery.

## Template

```markdown
Research Field Daily | {YYYY-MM-DD}

#{N} | {Title}
{Journal/Source}, {Year} | {Authors} | {Institution if verified}
Score: {score}/10 | Category: {agreed A-E identifier}
DOI: {verified DOI if present} | arXiv: {verified identifier if present}
Access: {Full text / Abstract only / Metadata only}

Takeaway: {Specific contribution and why it matters, or why it is deferred.}

Methods: {Experiment/simulation, system, conditions, material, measurement.}

Key results: {Concrete data or qualified conclusions with units and conditions.}

Assessment: {Value to the user's question, limitations, and whether to read in full.}

Source: {Best available DOI/publisher/arXiv/repository link}
```

Do not force a generic "connection to vault" field or low-information wiki links
into daily messages. Detailed project connections belong in archival notes.
Mention a tracked author or network naturally when it actually affects relevance.

## Field guidelines

The takeaway should let the reader judge relevance quickly without vague claims
of importance. Methods should identify the actual experimental or computational
approach and conditions. Results must state specific data or an explicit,
evidence-bounded conclusion. Assessment should explain practical relevance,
limitations, and the value of full-text reading.

The displayed 0–10 score is the validated 0–100 six-dimension total divided by ten.
Recalculate the total and enforce each dimension's cap. A score is a prioritization
aid, not proof of validity or quality.

## Synthetic example

All identifiers, dates, claims, and numerical results below are fictional.

```markdown
Research Field Daily | YYYY-MM-DD

#1 | Electrochemical monitoring of impurity X in compound A-B-C
Example Journal, 2026 | Example authors
Score: 9.2/10 | Category: A_core-research
DOI: <DOI> | Access: Full text

Takeaway: Method X reports a lower impurity-detection limit in system Y than the
comparison CV method; transfer to the user's system still needs verification.

Methods: SWV in molten chloride at 500 C, with a Pt working electrode, Ag/AgCl
reference, controlled Ar/H2O atmosphere, and titration cross-checks.

Key results: Reported detection limit 8 ppm O versus approximately 39 ppm for the
comparison method; R2 = 0.997 over 0–200 ppm; peak drift below 5 mV over 200 h.

Assessment: Relevant to a monitoring-control-validation workflow. Check reference
stability and calibration in the source before relying on the comparison.

Source: https://example.org/paper
```

## Delivery

Resolve the intended destination from the user and the configured integration.
Do not assume an imaginary `send_message` tool, infer an unknown chat ID, or send
to an arbitrary group. For a Feishu bot workflow, verify that the bot belongs to
the requested group and that the required permissions exist. If delivery is not
authorized or available, save or return the digest locally and report that status.
