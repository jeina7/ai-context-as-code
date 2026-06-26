#!/usr/bin/env python3
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DIR = ROOT / "notes"

PATTERNS = [
    ("possible email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("possible token", re.compile(r"\b(?:sk|ghp|gho|xoxb|xoxp)_[A-Za-z0-9_\-]{16,}\b")),
    ("local absolute path", re.compile(r"/Users/[A-Za-z0-9._\-]+")),
    ("private staging mention", re.compile(r"private-staging/.+\.md")),
    ("private visibility", re.compile(r"visibility:\s*private")),
]

BLOCKED_TERMS = [
    "PF MLS",
    "TossBank",
    "토스뱅크",
]


def main():
    findings = []
    for path in sorted(NOTES_DIR.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        for label, pattern in PATTERNS:
            if pattern.search(text):
                findings.append(f"{rel}: {label}")
        for term in BLOCKED_TERMS:
            if term in text:
                findings.append(f"{rel}: blocked term `{term}`")

    if findings:
        print("Publishable safety check failed:")
        for finding in findings:
            print(f"- {finding}")
        sys.exit(1)
    print("Publishable safety check passed.")


if __name__ == "__main__":
    main()

