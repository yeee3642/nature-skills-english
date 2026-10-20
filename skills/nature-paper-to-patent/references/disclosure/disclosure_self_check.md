# Internal disclosure checks (Step 8)

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

Use these checks to repair the draft before delivery. Keep the checklist separate from the technical disclosure unless the user asks for an audit report.

## 8.1 Technical logic

Confirm a complete path from input through processing to concrete output, clear dependencies between modules, handling of disclosed branches and low-confidence cases, and sources for learned prototypes or thresholds. Chapter 5 summarizes protection points supported by Chapter 3; it must not introduce a second technical solution.

## 8.2 Equations and parameters

Where formulas appear, confirm that 3.4.1 defines every symbol, index, unit, and range before use. Use resource subscripts (`b_{i,\mathrm{cpu}}`) rather than field-name superscripts. Check symbol identity across the main equations, parameter table, embodiments, and process explanation. Do not reuse one letter for unrelated quantities.

Check formula correctness, not merely formatting: operators, parentheses, exponents, denominators, missing terms, inequalities, sign conventions, dimensions, and value ranges. Verify that each formula corresponds to a stated module or process step. Review applicable empty-set, single-node, zero-denominator, absent-measurement, and boundary-value cases. Revise all affected sections together. If the source cannot establish the correct formula, isolate the uncertainty and ask a specific inventor question instead of guessing.

## 8.3 Files and references

Check versioned filenames and preservation of the previous draft, actual Markdown/Word generation, diagram rendering, and valid chapter cross-references. Every prior-art item needs an accessible matching public source. Read retrieved abstracts or public text before summarizing mechanisms or limitations. The disclosure names the databases and substantive queries used, not internal script names or browser implementation details.

For an iteration, append the local/UTC timestamp, user intent, new artifact names, and change summary to `disclosure_revision_log.md`. The delivery message records a Merge summary or Correction summary and any material unresolved issue. Keep repository footnotes, fictional-example labels, tool chatter, and internal audit tables outside the document. Any suggested claim emphasis must follow from its existing evidence.

Repair supported errors directly; do not merely tell the user to fix them. When required technical facts are unavailable, preserve a specific unresolved question and label the draft incomplete.
