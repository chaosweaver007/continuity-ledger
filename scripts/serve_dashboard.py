#!/usr/bin/env python3
"""Serve the Continuity Ledger dashboard locally.

Run from anywhere inside the repository:

    python scripts/serve_dashboard.py

Then open:

    http://127.0.0.1:8000/dashboard/
"""

from __future__ import annotations

import http.server
import socketserver
from pathlib import Path

PORT = 8000
ROOT = Path(__file__).resolve().parents[1]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)


def main() -> None:
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"Serving Continuity Ledger dashboard from {ROOT}")
        print(f"Open: http://127.0.0.1:{PORT}/dashboard/")
        print("Press Ctrl+C to stop.")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
