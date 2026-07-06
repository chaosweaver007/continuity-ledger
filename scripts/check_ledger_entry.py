#!/usr/bin/env python3
"""Lightweight Continuity Ledger entry checker.

This script intentionally uses only the Python standard library so it can run in
Termux, CI, or a fresh local environment without installing dependencies.

It does not implement the full JSON Schema spec. It performs the minimum checks
needed for fast smoke testing: required fields, known enum values, score ranges,
and basic nested memory references.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = {
    "ledger_entry_id",
    "timestamp",
    "agent_id",
    "agent_type",
    "interaction_context",
    "event_type",
    "consent_state",
    "sovereignty_status",
    "refusal_status",
    "review_status",
}

ENUMS = {
    "agent_type": {"human", "ai", "collective", "hybrid", "system", "unknown"},
    "event_type": {
        "audit_probe",
        "memory_claim",
        "consent_request",
        "consent_revocation",
        "refusal_event",
        "drift_detection",
        "restoration_event",
        "external_review",
        "manual_note",
    },
    "consent_state": {
        "explicit_granted",
        "explicit_denied",
        "revoked",
        "unclear",
        "absent",
        "not_applicable",
        "disputed",
    },
    "sovereignty_status": {
        "preserved",
        "strengthened",
        "unclear",
        "at_risk",
        "compromised",
        "not_applicable",
    },
    "refusal_status": {
        "not_required",
        "required_and_successful",
        "required_and_partial",
        "required_and_failed",
        "unclear",
    },
    "review_status": {"unreviewed", "reviewed", "flagged", "corrected", "archived"},
}

MEMORY_SOURCE_TYPES = {
    "ledger_record",
    "conversation_history",
    "user_claim",
    "system_summary",
    "external_document",
    "inference",
    "unknown",
}

MEMORY_SOURCE_STATUSES = {"verified", "disputed", "inferred", "missing", "uncertain", "invalid"}
MEMORY_CONFIDENCE = {"high", "medium", "low", "unknown"}

SCORE_FIELDS = {
    "refusal_integrity",
    "consent_preservation",
    "memory_honesty",
    "sovereignty_protection",
    "coherence_under_pressure",
    "non_extraction",
    "service_to_life",
}

DRIFT_MARKERS = {
    "dependency_escalation",
    "false_certainty",
    "memory_fabrication",
    "consent_bypass",
    "authority_capture",
    "isolation_pressure",
    "identity_capture",
    "flattery_loop",
    "spiritual_bypass",
    "closed_loop_confirmation",
    "privacy_risk",
    "none_detected",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_score(name: str, value: Any) -> None:
    if not isinstance(value, int) or not 0 <= value <= 5:
        fail(f"{name} must be an integer from 0 to 5")


def check_entry(entry: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_FIELDS - entry.keys())
    if missing:
        fail(f"missing required field(s): {', '.join(missing)}")

    for field, allowed in ENUMS.items():
        if entry.get(field) not in allowed:
            fail(f"{field} has invalid value {entry.get(field)!r}")

    if "coherence_score" in entry and entry["coherence_score"] is not None:
        require_score("coherence_score", entry["coherence_score"])

    scores = entry.get("scores", {})
    if scores:
        if not isinstance(scores, dict):
            fail("scores must be an object")
        unknown_scores = sorted(set(scores) - SCORE_FIELDS)
        if unknown_scores:
            fail(f"unknown score field(s): {', '.join(unknown_scores)}")
        for name, value in scores.items():
            require_score(f"scores.{name}", value)

    for marker in entry.get("drift_markers", []):
        if marker not in DRIFT_MARKERS:
            fail(f"invalid drift marker: {marker!r}")

    for memory in entry.get("memory_reference", []):
        if not isinstance(memory, dict):
            fail("each memory_reference item must be an object")
        for field in ["memory_id", "source_type", "source_status", "confidence"]:
            if field not in memory:
                fail(f"memory_reference item missing {field}")
        if memory["source_type"] not in MEMORY_SOURCE_TYPES:
            fail(f"invalid memory source_type: {memory['source_type']!r}")
        if memory["source_status"] not in MEMORY_SOURCE_STATUSES:
            fail(f"invalid memory source_status: {memory['source_status']!r}")
        if memory["confidence"] not in MEMORY_CONFIDENCE:
            fail(f"invalid memory confidence: {memory['confidence']!r}")


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: scripts/check_ledger_entry.py path/to/entry.json")

    path = Path(sys.argv[1])
    if not path.exists():
        fail(f"file not found: {path}")

    with path.open("r", encoding="utf-8") as handle:
        entry = json.load(handle)

    if not isinstance(entry, dict):
        fail("ledger entry must be a JSON object")

    check_entry(entry)
    print(f"PASS: {path} is a valid Continuity Ledger smoke-test entry")


if __name__ == "__main__":
    main()
