#!/usr/bin/env python3
"""Regression battery for the UDS-0 Evidence Gate semantic validator v1.1."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from check_evidence_gate import GateError, check_record  # noqa: E402


EXPECTED_RED = {
    "red_011_role_inversion.json": "TYPE_ERROR_11_RELATIONAL_ROLE_INVERSION",
    "red_012_metric_outcome.json": "TYPE_ERROR_12_METRIC_OUTCOME_CONFLATION",
    "red_013_unoperational.json": "TYPE_ERROR_13_OPERATIONALIZATION_FAILURE",
    "red_014_uncertainty_leak.json": "TYPE_ERROR_14_UNCERTAINTY_INHERITANCE",
    "red_015_domain_equivocation.json": "TYPE_ERROR_15_DOMAIN_SEMANTIC_EQUIVOCATION",
    "red_016_is_ought_leak.json": "TYPE_ERROR_16_DESCRIPTIVE_NORMATIVE_CONFLATION",
    "red_017_proxy_overclaim.json": "TYPE_ERROR_17_NORMATIVE_PROXY_OVERCLAIM",
    "red_018_self_sealing.json": "TYPE_ERROR_18_SELF_SEALING_TARGET_EQUIVALENCE",
    "red_019_goodhart_capture.json": "TYPE_ERROR_19_PROXY_OPTIMIZATION_CAPTURE",
    "red_020_reputation_leak.json": "TYPE_ERROR_20_REPUTATION_SCOPE_LEAK",
    "red_021_ontology_inflation.json": "TYPE_ERROR_21_MECHANISM_ONTOLOGY_INFLATION",
    "red_022_human_score.json": "HUMAN_DIGNITY_UNSCORABLE",
    "red_023_architect_override.json": "ARCHITECT_CREDENTIAL_INSUFFICIENT",
}


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return payload


def expect_rejection(path: Path, expected: str) -> None:
    try:
        check_record(load(path))
    except GateError as exc:
        if exc.code != expected:
            raise AssertionError(
                f"{path.name}: expected {expected}, received {exc.code}: {exc.message}"
            ) from exc
    else:
        raise AssertionError(f"{path.name}: unexpectedly passed; expected {expected}")


def main() -> None:
    valid_path = ROOT / "examples" / "uds0_evidence_gate_l2e_717.json"
    legacy_failure_path = (
        ROOT / "examples" / "failures" / "uds0_tautological_target_failure.json"
    )
    red_dir = ROOT / "tests" / "fixtures" / "red"

    warnings = check_record(load(valid_path))
    if warnings:
        raise AssertionError(f"unexpected warning(s) for valid L2e fixture: {warnings}")

    expect_rejection(
        legacy_failure_path,
        "TYPE_ERROR_08_TAUTOLOGICAL_TARGET_COLLAPSE",
    )

    observed_files = {p.name for p in red_dir.glob("red_*.json")}
    expected_files = set(EXPECTED_RED)
    missing = sorted(expected_files - observed_files)
    unexpected = sorted(observed_files - expected_files)
    if missing or unexpected:
        raise AssertionError(
            f"red fixture inventory mismatch; missing={missing}, unexpected={unexpected}"
        )

    for filename, expected in EXPECTED_RED.items():
        expect_rejection(red_dir / filename, expected)

    print("PASS: valid Evidence Gate fixture accepted")
    print("PASS: legacy TYPE_ERROR_08 tautological target rejected")
    print(
        f"PASS: {len(EXPECTED_RED)}/{len(EXPECTED_RED)} red-team fixtures "
        "rejected with their expected typed diagnostics"
    )


if __name__ == "__main__":
    main()
