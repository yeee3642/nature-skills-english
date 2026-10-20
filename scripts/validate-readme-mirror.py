#!/usr/bin/env python3
"""Validate English README compatibility copies in the local English edition.

Modified 2026-10-20: README.md and README_EN.md now both contain English.
The upstream requirement for Chinese language-switch links no longer applies.
"""
from __future__ import annotations
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
HAN = re.compile('[\u3400-\u9fff]')

def main() -> int:
    errors = []
    skills = sorted(path for path in (ROOT / 'skills').iterdir() if path.is_dir())
    for skill in skills:
        texts = []
        for name in ('README.md', 'README_EN.md'):
            path = skill / name
            if not path.is_file():
                errors.append(f'{skill.name}: missing {name}')
                continue
            text = path.read_text('utf-8')
            texts.append(text)
            if HAN.search(text):
                errors.append(f'{skill.name}/{name}: non-English Han text')
            if not re.search(r'^#\s+\S', text, flags=re.M):
                errors.append(f'{skill.name}/{name}: missing title')
        titles = [re.search(r'^#\s+(.+)', text, flags=re.M).group(1) for text in texts if re.search(r'^#\s+(.+)', text, flags=re.M)]
        if len(titles) == 2 and titles[0] != titles[1]:
            errors.append(f'{skill.name}: README titles differ')
        if skill.name == 'nature-shared' and not all('support package' in text.lower() for text in texts):
            errors.append('nature-shared: support-package role is missing')
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'English README validation passed: {len(skills)} skill directories.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
