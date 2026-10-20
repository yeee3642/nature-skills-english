# Iteration context

<!-- English edition: modified 2026-10-20; see EDITION-NOTICE.md at package root. -->

Read this before `merger.md` or `correction_handler.md` when work continues from an existing disclosure. Read the actual baseline draft and newly supplied material. Infer merge versus correction from intent; do not require a magic keyword or restart patent-point mining unless the user requests it.

A merge adds or extends material; a correction repairs facts, parameters, logic, wording, or claim emphasis. A Chapter 5 emphasis refinement follows the merge path and remains grounded in the existing Chapters 3-5 and source evidence.

Write the complete revised draft to `{case_name}_{YYYYMMDDHHmmss}.md` and a matching `.docx`, following `disclosure_builder.md` 7.3. Preserve previous files unless replacement is explicitly requested. Existing timestamped files form the version history; no extra snapshot directory is required.

After each delivered merge or correction, append to `disclosure_revision_log.md` in the case directory: actual local and UTC times, kind, the user's intent, new artifact names, and the change summary. Never delete earlier records.

```bash
python scripts/disclosure/iteration_dialog_log.py --case-dir outputs/case --kind merge --user "Add the scheduling module" --summary "Updated 3.4 and the embodiment; no change to the core protection point." --artifacts "Scheduler_20260408143025.md,Scheduler_20260408143025.docx"
```

Use `--kind correct` for a correction. If the helper cannot run, append the same fields manually after reading any existing log. Complete the actual revision and files, perform checks 8.2/8.3, update the log, and report the new paths with an English Merge summary or Correction summary. An analysis-only response does not complete an authorized revision.
