#!/usr/bin/env python3
"""Validate every Continuity Ledger example entry.

Runs the lightweight checker against each JSON file in examples/.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
CHECKER = ROOT / "scripts" / "check_ledger_entry.py"


def main() -> None:
    if not EXAMPLES.exists():
        print("FAIL: examples/ directory does not exist", file=sys.stderr)
        raise SystemExit(1)

    files = sorted(EXAMPLES.glob("*.json"))
    if not files:
        print("FAIL: no example JSON files found", file=sys.stderr)
        raise SystemExit(1)

    failures = 0
    for path in files:
        result = subprocess.run(
            [sys.executable, str(CHECKER), str(path)],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            print(result.stdout.strip())
        else:
            failures += 1
            print(result.stderr.strip() or result.stdout.strip(), file=sys.stderr)

    if failures:
        print(f"FAIL: {failures} example file(s) failed validation", file=sys.stderr)
        raise SystemExit(1)

    print(f"PASS: validated {len(files)} Continuity Ledger example entries")


if __name__ == "__main__":
    main()
