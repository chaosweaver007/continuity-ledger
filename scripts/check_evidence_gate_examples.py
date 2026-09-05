#!/usr/bin/env python3
"""Smoke tests for the UDS-0 Evidence Gate semantic validator."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from check_evidence_gate import GateError, check_record  # noqa: E402


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return payload


def main() -> None:
    valid_path = ROOT / "examples" / "uds0_evidence_gate_l2e_717.json"
    failure_path = ROOT / "examples" / "failures" / "uds0_tautological_target_failure.json"

    warnings = check_record(load(valid_path))
    if warnings:
        raise AssertionError(f"unexpected warning(s) for valid L2e fixture: {warnings}")

    try:
        check_record(load(failure_path))
    except GateError as exc:
        expected = "TYPE_ERROR_08_TAUTOLOGICAL_TARGET_COLLAPSE"
        if exc.code != expected:
            raise AssertionError(
                f"expected {expected}, received {exc.code}: {exc.message}"
            ) from exc
    else:
        raise AssertionError("tautological-target fixture unexpectedly passed")

    print("PASS: valid Evidence Gate fixture accepted")
    print("PASS: tautological target rejected with TYPE_ERROR_08")


if __name__ == "__main__":
    main()
