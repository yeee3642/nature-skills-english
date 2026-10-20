#!/usr/bin/env python3
"""Run deterministic claim-structure checks, retaining legacy Chinese antecedent checks."""

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


CLAIM_START = re.compile(r"(?m)^\s*(\d+)\s*[.、．]\s*")
REFERENCE = re.compile(
    "\u6743\u5229\u8981\u6c42\\s*(\\d+)(?:\\s*[-\u2014~\uff5e\u81f3]\\s*(\\d+))?|\u6743\u5229\u8981\u6c42\\s*(\\d+)\\s*(?:\u6216|\u3001)\\s*(\\d+)"
)
TERM_INTRO = re.compile("(?:\u6240\u8ff0|\u8be5)([\\u4e00-\\u9fffA-Za-z][\\u4e00-\\u9fffA-Za-z0-9_-]{1,20})")
PLACEHOLDER = re.compile("\\[(?:TO CONFIRM|\u5f85\u786e\u8ba4)[^\\]]*\\]", re.IGNORECASE)


@dataclass
class Finding:
    level: str
    claim: int | None
    code: str
    message: str


def split_claims(text: str) -> list[tuple[int, str]]:
    matches = list(CLAIM_START.finditer(text))
    claims = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        claims.append((int(match.group(1)), text[match.end() : end].strip()))
    return claims


def references(body: str) -> list[int]:
    result = []
    for match in REFERENCE.finditer(body):
        if match.group(1):
            start = int(match.group(1))
            finish = int(match.group(2) or start)
            result.extend(range(start, finish + 1))
        else:
            result.extend((int(match.group(3)), int(match.group(4))))
    for match in re.finditer(r"\bclaims?\s+(\d+)(?:\s*(?:-|to)\s*(\d+))?", body, re.IGNORECASE):
        start = int(match.group(1))
        finish = int(match.group(2) or start)
        result.extend(range(start, finish + 1))
    return sorted(set(result))


def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text)


def term_is_introduced(term: str, basis: str, claim: str) -> bool:
    "Check whether a captured term or its substantive prefix has an earlier antecedent."
    for end in range(2, len(term) + 1):
        prefix = term[:end]
        if prefix in basis or re.search(rf"(?<!" "\u6240" rf"" "\u8ff0" rf")(?<!" "\u8be5" rf"){re.escape(prefix)}", claim):
            return True
    return False


def audit(text: str) -> list[Finding]:
    claims = split_claims(text)
    findings = []
    if not claims:
        return [Finding("ERROR", None, "NO_CLAIMS", "No numbered claims beginning with \"1.\" were recognized.")]

    numbers = [number for number, _ in claims]
    expected = list(range(1, len(claims) + 1))
    if numbers != expected:
        findings.append(
            Finding("ERROR", None, "NUMBER_SEQUENCE", f"Claim numbers must be consecutive: expected {expected}, found {numbers}.")
        )

    previous_text = ""
    claim_map = {}
    for number, body in claims:
        compact = normalize(body)
        claim_map[number] = compact
        refs = references(body)

        if not body:
            findings.append(Finding("ERROR", number, "EMPTY", "Claim text is empty."))
            continue
        if PLACEHOLDER.search(body):
            findings.append(
                Finding("ERROR", number, "PLACEHOLDER", "Formal claims still contain confirmation placeholders.")
            )
        if number == 1 and refs:
            findings.append(
                Finding("ERROR", number, "INDEPENDENT_REFERENCE", "Claim 1 must not reference another claim.")
            )
        if number > 1 and not refs:
            findings.append(
                Finding("WARNING", number, "NO_REFERENCE", "No dependency reference detected; check whether this is an independent claim.")
            )
        for ref in refs:
            if ref >= number:
                findings.append(
                    Finding("ERROR", number, "FORWARD_REFERENCE", f"References a claim that is not earlier: {ref}.")
                )
            if ref not in claim_map:
                findings.append(
                    Finding("ERROR", number, "MISSING_REFERENCE", f"Referenced claim {ref} does not exist.")
                )

        if "\u5176\u7279\u5f81\u5728\u4e8e" not in compact and not re.search(r"\b(?:comprising|wherein|consisting\s+of|characteri[sz]ed)\b", body, re.IGNORECASE):
            findings.append(
                Finding("WARNING", number, "TRANSITION", "No recognized claim transition was detected.")
            )
        if len(compact) < 25:
            findings.append(
                Finding("WARNING", number, "TOO_SHORT", "Short claim: check that the technical solution is fully defined.")
            )
        if re.search("(\u6548\u679c\u66f4\u597d|\u6027\u80fd\u4f18\u5f02|\u663e\u8457\u63d0\u9ad8|\u5927\u5927\u63d0\u9ad8|\u6700\u4f73|\u6700\u4f18)", compact):
            findings.append(
                Finding("WARNING", number, "RESULT_LANGUAGE", "Contains effect-only or promotional wording; consider a supported technical limitation.")
            )

        searchable_basis = previous_text + "".join(
            claim_map.get(ref, "") for ref in refs
        )
        # "1" captures ""; drop the  so the generic head noun is skipped.
        terms = {found[1:] if found.startswith("\u7684") else found for found in TERM_INTRO.findall(body)}
        for term in sorted(terms):
            if len(term) < 2 or term in {"\u65b9\u6cd5", "\u88c5\u7f6e", "\u8bbe\u5907", "\u7cfb\u7edf", "\u6b65\u9aa4", "\u7a0b\u5e8f"}:
                continue
            if not term_is_introduced(term, searchable_basis, compact):
                findings.append(
                    Finding(
                        "WARNING",
                        number,
                        "ANTECEDENT_BASIS",
                        f"Term \"{term}\" may lack a clear antecedent.",
                    )
                )
        previous_text += compact

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("claims", type=Path, help="UTF-8 claims text file")
    parser.add_argument("--json", action="store_true", help="Output findings as JSON")
    args = parser.parse_args()

    text = args.claims.read_text(encoding="utf-8")
    findings = audit(text)
    if args.json:
        print(json.dumps([finding.__dict__ for finding in findings], ensure_ascii=False, indent=2))
    elif not findings:
        print("PASS: No structural issues found.")
    else:
        for finding in findings:
            location = f"Claim {finding.claim}" if finding.claim else "Overall"
            print(f"{finding.level}\t{location}\t{finding.code}\t{finding.message}")
        errors = sum(finding.level == "ERROR" for finding in findings)
        warnings = sum(finding.level == "WARNING" for finding in findings)
        print(f"\nSummary: {errors} errors, {warnings} warnings")

    return 1 if any(finding.level == "ERROR" for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
