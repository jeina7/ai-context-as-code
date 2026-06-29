#!/usr/bin/env python3
"""Generate repo-local agent entry files from forge source documents."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT_SOURCE_DIR = ROOT / "forge" / "_config" / "Agents"


OUTPUTS = {
    "AGENTS.md": ("agent.md", "common.md"),
    "CLAUDE.md": ("claude.md", "common.md"),
}


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text.strip()

    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("frontmatter start was found without a closing marker")

    return text[end + len("\n---\n") :].strip()


def read_source(name: str) -> str:
    path = AGENT_SOURCE_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"missing source file: {path.relative_to(ROOT)}")

    try:
        return strip_frontmatter(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: {exc}") from exc


def build_output(output_name: str, source_names: tuple[str, ...]) -> str:
    source_list = " + ".join(f"forge/_config/Agents/{name}" for name in source_names)
    header = "\n".join(
        [
            f"# {output_name} instructions",
            "",
            "<!-- GENERATED FILE. Do not edit directly. -->",
            f"<!-- Source: {source_list} -->",
            "<!-- Regenerate: python3 scripts/sync_agent_docs.py -->",
            "",
        ]
    )
    body = "\n\n".join(read_source(name) for name in source_names)
    return f"{header}\n{body}\n"


def main() -> int:
    for output_name, source_names in OUTPUTS.items():
        output_path = ROOT / output_name
        output_path.write_text(build_output(output_name, source_names), encoding="utf-8")
        print(f"wrote {output_path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
