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
    ("principle", re.compile(r"\b(?:principle|원칙|expertise|전문성)\b", re.IGNORECASE), "notes/principles/"),
    ("pattern", re.compile(r"\b(?:pattern|workflow|loop|방법)\b", re.IGNORECASE), "notes/workflows/"),
    ("research", re.compile(r"\b(?:research|리서치|source|출처|trend|용어)\b", re.IGNORECASE), "notes/research/"),
    ("decision", re.compile(r"\b(?:decision|결정|why|tradeoff|ADR)\b", re.IGNORECASE), "notes/decisions/"),
    ("project", re.compile(r"\b(?:project|design|architecture|plan|설계)\b", re.IGNORECASE), "notes/projects/"),
    ("reference", re.compile(r"\b(?:context|knowledge as code|concept|개념)\b", re.IGNORECASE), "notes/concepts/"),
]


HIGH_RISK_LABELS = {"token_like", "internal_company_term", "email"}
MEDIUM_RISK_LABELS = {"local_path", "daily_private_context"}


def classify(text):
    for note_type, pattern, destination in ROUTE_RULES:
        if pattern.search(text):
            return note_type, destination
    return "reference", "notes/concepts/"


def risk_findings(text):
    findings = []
    for label, pattern in RISK_PATTERNS:
        if pattern.search(text):
            findings.append(label)
    return findings


def summarize_text(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return " ".join(lines[:3])[:500]


def candidate_title(path, text):
    heading = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    if heading:
        return heading.group(1).strip()
    return path.stem.replace("-", " ").replace("_", " ").title()


def risk_level(risks):
    if any(label in HIGH_RISK_LABELS for label in risks):
        return "high"
    if any(label in MEDIUM_RISK_LABELS for label in risks):
        return "medium"
    return "low"


def recommendation_for(risks):
    level = risk_level(risks)
    if level == "high":
        return "rewrite-from-scratch"
    if level == "medium":
        return "extract-and-redact"
    return "rewrite-for-standalone-context"


def rewrite_checklist(risks):
    checklist = [
        "write a standalone note that does not depend on the private source file",
        "keep only durable context, decisions, or reusable procedures",
        "add wikilinks to existing notes after the rewritten note exists",
    ]
    if "internal_company_term" in risks:
        checklist.append("remove company, team, project, and role-specific details")
    if "daily_private_context" in risks:
        checklist.append("remove personal journal, finance, health, family, or strategy context")
    if "email" in risks or "token_like" in risks or "local_path" in risks:
        checklist.append("remove identifiers, credentials, local paths, and account-specific strings")
    return checklist


def analyze_file(path):
    text = path.read_text(encoding="utf-8")
    note_type, destination = classify(f"{path.name}\n{text[:4000]}")
    risks = risk_findings(text)
    title = candidate_title(path, text)
    return {
        "source_path": str(path),
        "file_name": path.name,
        "candidate_title": title,
        "note_type": note_type,
        "recommended_destination": destination,
        "risk_findings": risks,
        "risk_level": risk_level(risks),
        "recommendation": recommendation_for(risks),
        "rewrite_checklist": rewrite_checklist(risks),
        "requires_rewrite": True,
        "eligible_for_direct_import": False,
        "summary_hint": summarize_text(text),
        "rewrite_prompt": (
            f"Rewrite `{title}` as a standalone {note_type} note under `{destination}`. "
            "Do not copy private wording. Keep only the reusable idea, decision, or workflow."
        ),
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
        "| Source | Type | Destination | Risk | Recommendation |",
        "|---|---|---|---|---|",
    ]
    for item in results:
        risks = ", ".join(item["risk_findings"]) if item["risk_findings"] else "none detected"
        lines.append(
            f"| `{item['file_name']}` | {item['note_type']} | `{item['recommended_destination']}` | {item['risk_level']}: {risks} | {item['recommendation']} |"
        )
    lines.append("")
    lines.append("## Candidate Notes")
    lines.append("")
    for item in results:
        lines.extend([
            f"### {item['candidate_title']}",
            "",
            f"- Source: `{item['file_name']}`",
            f"- Destination: `{item['recommended_destination']}`",
            f"- Recommendation: {item['recommendation']}",
            f"- Summary hint: {item['summary_hint'] or 'none'}",
            f"- Rewrite prompt: {item['rewrite_prompt']}",
            "- Rewrite checklist:",
        ])
        lines.extend([f"  - {entry}" for entry in item["rewrite_checklist"]])
        lines.append("")
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
