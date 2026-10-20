#!/usr/bin/env python3
"Append a revision record containing actual local and UTC times, user intent, delivered artifact names, and a merge or correction summary."
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LOG = "disclosure_revision_log.md"

FILE_HEADER = """# Disclosure revision log

> Appended by iteration_dialog_log.py or according to iteration_context.md. Each entry records actual times and revision intent. Preserve prior entries.

"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Append one revision dialog entry to case-dir log markdown"
    )
    parser.add_argument(
        "--case-dir",
        type=Path,
        required=True,
        help="Existing case output directory containing the disclosure",
    )
    parser.add_argument(
        "--kind",
        choices=("merge", "correct"),
        required=True,
        help="merge=incremental merge; correct=correction",
    )
    parser.add_argument(
        "--user",
        default="",
        help="User intent summary (one to eight sentences)",
    )
    parser.add_argument(
        "--summary",
        default="",
        help="Concise merge or correction summary",
    )
    parser.add_argument(
        "--artifacts",
        default="",
        help="Artifact filenames separated by commas",
    )
    parser.add_argument(
        "--log-name",
        default=DEFAULT_LOG,
        help=f"Log filename (default: {DEFAULT_LOG})",
    )
    args = parser.parse_args()

    case_dir = args.case_dir.expanduser().resolve()
    if not case_dir.is_dir():
        print(f"ERROR: Not an existing directory: {case_dir}", file=sys.stderr)
        return 2

    log_path = case_dir / args.log_name
    now_local = datetime.now().astimezone()
    now_utc = datetime.now(timezone.utc)
    kind_zh = "Merge" if args.kind == "merge" else "Correction"

    user_block = (args.user or "").strip() or "(No --user supplied; add the user intent summary to this entry.)"
    summary_block = (args.summary or "").strip() or "—"
    art = (args.artifacts or "").strip()
    if art:
        art_lines = "\n".join(f"- `{x.strip()}`" for x in art.split(",") if x.strip())
    else:
        art_lines = "—"

    entry = f"""## {now_local.strftime("%Y-%m-%d %H:%M:%S")} (local) · {now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")} (UTC)

**Kind**: {kind_zh}

**User intent**: 

{user_block}

**Delivered artifacts**: 

{art_lines}

**Change summary**: 

{summary_block}

---

"""

    if log_path.exists():
        prev = log_path.read_text(encoding="utf-8")
        if prev and not prev.endswith("\n"):
            prev += "\n"
        log_path.write_text(prev + "\n" + entry, encoding="utf-8")
    else:
        log_path.write_text(FILE_HEADER + "\n" + entry, encoding="utf-8")

    print(f"LOG_FILE={log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
