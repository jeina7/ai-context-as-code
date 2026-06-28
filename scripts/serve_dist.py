#!/usr/bin/env python3
"""Serve dist/ locally with the same app-shell fallback used by Workers static assets."""

from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "dist"


class AppShellHandler(SimpleHTTPRequestHandler):
    def send_head(self):  # noqa: N802 - stdlib method name
        requested = self.translate_path(self.path)
        if not Path(requested).exists() and (
            self.path.startswith("/trove/") or self.path.startswith("/search")
        ):
            self.path = "/index.html"
        return super().send_head()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=4173)
    args = parser.parse_args()

    if not DIST_DIR.exists():
        raise SystemExit("dist/ is missing. Run python3 scripts/build_trove.py first.")

    handler = partial(AppShellHandler, directory=str(DIST_DIR))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Serving ACAC dist at http://{args.host}:{args.port}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
