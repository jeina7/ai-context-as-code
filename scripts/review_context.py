#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD_STATS = ROOT / "_build" / "stats.json"

CHECKS = [
    ["python3", "scripts/check_publish_safety.py"],
    ["python3", "scripts/validate_notes.py"],
    ["python3", "scripts/build_meta.py"],
]


def run_check(command):
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return {
        "command": " ".join(command),
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def main():
    results = [run_check(command) for command in CHECKS]
    failed = [item for item in results if item["returncode"] != 0]
    for item in results:
        print(f"$ {item['command']}")
        if item["stdout"]:
            print(item["stdout"])
        if item["stderr"]:
            print(item["stderr"], file=sys.stderr)

    if BUILD_STATS.exists():
        stats = json.loads(BUILD_STATS.read_text(encoding="utf-8"))
        print(f"notes: {stats.get('note_count')}")
        print(f"broken_links: {stats.get('broken_link_count')}")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
