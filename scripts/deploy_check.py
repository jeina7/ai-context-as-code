#!/usr/bin/env python3
"""Run the local checks that should pass before a Cloudflare Pages deployment."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    print(f"$ {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    try:
        run([sys.executable, "scripts/sync_agent_docs.py"])
        run([sys.executable, "scripts/build_trove.py"])
        run([sys.executable, "scripts/check_public_payload.py"])
        if shutil.which("node"):
            run(["node", "--check", "site/assets/app.js"])
        else:
            print("node not found; skipped JS syntax check")
    except subprocess.CalledProcessError as exc:
        return exc.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
