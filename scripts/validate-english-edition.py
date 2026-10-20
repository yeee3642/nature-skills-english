#!/usr/bin/env python3
"""Audit this local English adaptation without executing any research workflows."""
from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import sys
import tomllib
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
HAN = re.compile('[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\U00020000-\U000323af]')
LINK = re.compile(r'!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+"[^"\n]*")?\)')
BINARY = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.pdf', '.woff', '.woff2', '.ttf', '.zip', '.pyc'}


def audit(root: Path = ROOT) -> tuple[list[str], dict[str, int]]:
    issues: list[str] = []
    counts = {'text_files': 0, 'python_files': 0, 'structured_files': 0, 'local_links': 0}
    for path in sorted(root.rglob('*')):
        if any(part in {'.git', '__pycache__', '.pytest_cache', '.codebase-memory'} for part in path.relative_to(root).parts):
            continue
        rel = path.relative_to(root).as_posix()
        if HAN.search(rel):
            issues.append(f'{rel}: Han ideographs in path name')
        if not path.is_file() or path.suffix.lower() in BINARY:
            continue
        try:
            text = path.read_text('utf-8-sig')
        except UnicodeDecodeError:
            issues.append(f'{rel}: unexpected non-UTF-8 text')
            continue
        counts['text_files'] += 1
        match = HAN.search(text)
        if match:
            line = text.count('\n', 0, match.start()) + 1
            issues.append(f'{rel}:{line}: literal Han ideographs in source text')
        try:
            if path.suffix == '.py':
                ast.parse(text, filename=rel)
                counts['python_files'] += 1
            elif path.suffix == '.json':
                json.loads(text)
                counts['structured_files'] += 1
            elif path.suffix == '.toml':
                tomllib.loads(text)
                counts['structured_files'] += 1
        except (SyntaxError, ValueError) as exc:
            issues.append(f'{rel}: parse failure: {exc}')
        if path.suffix != '.md':
            continue
        prose = re.sub(r'(?ms)^\s*(```|~~~).*?^\s*\1[^\n]*\n?', '', text)
        prose = re.sub(r'`[^`\n]*`', '', prose)
        for match in LINK.finditer(prose):
            raw_target = match.group(1).strip('<>')
            target_url = urlsplit(raw_target)
            target = unquote(target_url.path)
            if not target or target_url.scheme or target_url.netloc:
                continue
            if target.startswith(('/', '~', '$')) or any(mark in target for mark in ('<', '>', '*', '{', '}')):
                continue
            resolved = path.parent / target
            counts['local_links'] += 1
            if not resolved.exists():
                issues.append(f'{rel}: missing local Markdown target: {target}')
    return issues, counts


def main() -> int:
    issues, counts = audit()
    print(json.dumps({'checks': counts, 'issues': issues}, indent=2, ensure_ascii=True))
    return bool(issues)


if __name__ == '__main__':
    sys.exit(main())
