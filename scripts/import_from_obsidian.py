#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING_DIR = ROOT / "private-staging"
REPORT_JSON = STAGING_DIR / "import-report.json"
REPORT_MD = STAGING_DIR / "import-report.md"

RISK_PATTERNS = [
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("local_path", re.compile(r"/Users/[A-Za-z0-9._\-]+")),
    ("token_like", re.compile(r"\b(?:sk|ghp|gho|xoxb|xoxp)_[A-Za-z0-9_\-]{16,}\b")),
    ("internal_company_term", re.compile(r"\b(?:PF MLS|TossBank|토스뱅크)\b")),
    ("daily_private_context", re.compile(r"\b(?:일기|가족|재무|건강|관계|Daily/|Strategy/CURRENT)\b")),
]

ROUTE_RULES = [
    ("principle", re.compile(r"\b(?:principle|원칙|expertise|전문성)\b", re.IGNORECASE), "notes/10-principles/"),
    ("pattern", re.compile(r"\b(?:pattern|workflow|loop|방법)\b", re.IGNORECASE), "notes/30-workflows/"),
    ("research", re.compile(r"\b(?:research|리서치|source|출처|trend|용어)\b", re.IGNORECASE), "notes/60-research/"),
    ("decision", re.compile(r"\b(?:decision|결정|why|tradeoff|ADR)\b", re.IGNORECASE), "notes/50-decisions/"),
    ("project", re.compile(r"\b(?:project|design|architecture|plan|설계)\b", re.IGNORECASE), "notes/40-projects/"),
    ("reference", re.compile(r"\b(?:context|knowledge as code|concept|개념)\b", re.IGNORECASE), "notes/20-concepts/"),
]


def classify(text):
    for note_type, pattern, destination in ROUTE_RULES:
        if pattern.search(text):
            return note_type, destination
    return "reference", "notes/20-concepts/"


def risk_findings(text):
    findings = []
    for label, pattern in RISK_PATTERNS:
        if pattern.search(text):
            findings.append(label)
    return findings


def summarize_text(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return " ".join(lines[:3])[:500]


def analyze_file(path):
    text = path.read_text(encoding="utf-8")
    note_type, destination = classify(f"{path.name}\n{text[:4000]}")
    risks = risk_findings(text)
    return {
        "source_path": str(path),
        "file_name": path.name,
        "note_type": note_type,
        "recommended_destination": destination,
        "risk_findings": risks,
        "requires_rewrite": True,
        "eligible_for_direct_import": False,
        "summary_hint": summarize_text(text),
    }


def write_reports(results):
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "dry-run",
        "results": results,
    }
    REPORT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Obsidian Import Dry Run",
        "",
        "This report is generated from private source material. Do not publish it directly.",
        "",
        "| Source | Type | Destination | Risks | Direct Import |",
        "|---|---|---|---|---|",
    ]
    for item in results:
        risks = ", ".join(item["risk_findings"]) if item["risk_findings"] else "none detected"
        lines.append(
            f"| `{item['file_name']}` | {item['note_type']} | `{item['recommended_destination']}` | {risks} | no |"
        )
    lines.append("")
    lines.append("## Rule")
    lines.append("")
    lines.append("All imported material must be rewritten into publishable notes before entering `notes/`.")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Dry-run import analysis for private Obsidian notes.")
    parser.add_argument("paths", nargs="+", help="Markdown files to analyze.")
    args = parser.parse_args()

    results = []
    for raw_path in args.paths:
        path = Path(raw_path).expanduser().resolve()
        if path.suffix.lower() != ".md":
            raise SystemExit(f"Only markdown files are supported: {path}")
        if not path.exists():
            raise SystemExit(f"File not found: {path}")
        results.append(analyze_file(path))

    write_reports(results)
    print(f"Wrote {REPORT_JSON.relative_to(ROOT)} and {REPORT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
