#!/usr/bin/env python3
"""UDS-0 Evidence Gate semantic validator v1.0.

This validator uses only the Python standard library. It complements, rather
than replaces, the Draft 2020-12 structural schema.

Implemented checks:
- canonical payload SHA-256 verification
- typed Zero namespace checks
- L2c temporal ordering and bounded-target checks
- L2c external-anchor verification status reporting
- L3 promotion and hypothesis/receipt coherence
- protection against D1 target-predicate mutation

Not implemented here:
- remote RFC 3161 / transparency-log / external Merkle-anchor verification
- cryptographic signature verification
- append-only ledger checkpoint verification
- arbitrary D1 operation execution

Those require provider-specific or ledger-specific adapters and remain
NOT_DEMONSTRATED until independently executed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any


class GateError(Exception):
    """Typed Evidence Gate validation error."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def canonicalize_text(value: Any) -> bytes:
    if not isinstance(value, str):
        raise GateError(
            "PAYLOAD_CANONICALIZATION_ERROR",
            "UDS-C14N-TEXT-v1 requires raw_payload to be a string",
        )
    normalized = unicodedata.normalize("NFC", value)
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    return normalized.encode("utf-8")


def canonicalize_json(value: Any) -> bytes:
    text = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    text = unicodedata.normalize("NFC", text)
    return text.encode("utf-8")


def canonicalize(c14n_id: str, value: Any) -> bytes:
    if c14n_id == "UDS-C14N-TEXT-v1":
        return canonicalize_text(value)
    if c14n_id == "UDS-C14N-JSON-v1":
        return canonicalize_json(value)
    raise GateError(
        "PAYLOAD_CANONICALIZATION_ERROR",
        f"unknown canonicalization_id {c14n_id!r}",
    )


def parse_dt(value: str, field: str) -> datetime:
    if not isinstance(value, str):
        raise GateError("TIME_PARSE_ERROR", f"{field} must be an RFC 3339 string")
    candidate = value
    if candidate.endswith("Z"):
        candidate = candidate[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise GateError("TIME_PARSE_ERROR", f"{field} is not parseable: {value!r}") from exc
    if dt.tzinfo is None:
        raise GateError("TIME_PARSE_ERROR", f"{field} must include a UTC offset")
    return dt


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise GateError(code, message)


def check_payload_hash(record: dict[str, Any]) -> None:
    extracted = record["L1_observation"]["extracted_observation"]
    expected = extracted["payload_sha256"]
    actual = sha256_hex(canonicalize(extracted["canonicalization_id"], extracted["raw_payload"]))
    require(
        actual == expected,
        "L1_PAYLOAD_HASH_MISMATCH",
        f"payload_sha256 mismatch: expected {expected}, calculated {actual}",
    )


def check_zero_namespaces(record: dict[str, Any]) -> None:
    expected_layer = {
        "ZERO_HERMENEUTIC": "L2",
        "ZERO_OPERATIONAL": "L2c",
        "ZERO_CAUSAL_HYPOTHESIS": "L3",
    }
    for binding in record.get("symbol_bindings", []):
        namespace = binding.get("namespace")
        if namespace in expected_layer:
            require(
                binding.get("layer") == expected_layer[namespace],
                "TYPE_ERROR_09_SYMBOLIC_OPERATIONAL_EQUIVOCATION",
                f"{namespace} must be typed at {expected_layer[namespace]}, "
                f"not {binding.get('layer')!r}",
            )


def check_d1(record: dict[str, Any]) -> None:
    l2 = record["L2_correspondence"]
    target = l2.get("target_predicate")
    target_id = target.get("predicate_id") if isinstance(target, dict) else None

    forbidden_definition_keys = {
        "predicate_definition",
        "target_predicate",
        "target_expression",
        "success_criteria",
        "failure_criteria",
    }

    for derivation in record["D1_derivations"]:
        require(
            derivation.get("deterministic") is True,
            "D1_NONDETERMINISTIC_OPERATION",
            f"{derivation.get('derivation_id', '<unknown>')} is not marked deterministic",
        )
        illegal = sorted(forbidden_definition_keys.intersection(derivation))
        require(
            not illegal,
            "TYPE_ERROR_10_PREDICATE_EVALUATION_CONFLATION",
            "D1 derivation contains target-definition field(s): " + ", ".join(illegal),
        )

        ref = derivation.get("target_predicate_ref")
        if ref is not None:
            require(
                l2.get("mode") == "L2c" and target_id is not None,
                "TYPE_ERROR_10_PREDICATE_EVALUATION_CONFLATION",
                "D1 references a target predicate but no L2c target is bound",
            )
            require(
                ref == target_id,
                "TYPE_ERROR_10_PREDICATE_EVALUATION_CONFLATION",
                f"D1 target predicate ref {ref!r} does not match frozen L2c predicate {target_id!r}",
            )


def check_l2c(record: dict[str, Any], warnings: list[str]) -> None:
    l1 = record["L1_observation"]
    l2 = record["L2_correspondence"]
    if l2.get("mode") != "L2c":
        return

    require(
        isinstance(l2.get("preregistration"), dict),
        "TYPE_ERROR_02_RETROACTIVE_CONFIRMATION",
        "L2c requires preregistration",
    )
    require(
        isinstance(l2.get("target_predicate"), dict),
        "TYPE_ERROR_10_PREDICATE_EVALUATION_CONFLATION",
        "L2c requires a target predicate bound before evaluation",
    )
    require(
        l1.get("event_at_utc") is not None,
        "TYPE_ERROR_02_RETROACTIVE_CONFIRMATION",
        "L2c requires an independently identified event_at_utc",
    )

    registered = parse_dt(l2["preregistration"]["registered_at_utc"], "registered_at_utc")
    event_at = parse_dt(l1["event_at_utc"], "event_at_utc")
    require(
        registered < event_at,
        "TYPE_ERROR_02_RETROACTIVE_CONFIRMATION",
        "preregistration must precede the event clock",
    )

    target = l2["target_predicate"]
    p_hit = target.get("null_hypothesis_hit_probability")
    threshold = target.get("evidentiary_p_threshold")

    require(
        isinstance(p_hit, (int, float)),
        "TYPE_ERROR_05_BASE_RATE_NEGLECT",
        "L2c requires null_hypothesis_hit_probability",
    )
    require(
        0.0 <= float(p_hit) <= 1.0,
        "TYPE_ERROR_05_BASE_RATE_NEGLECT",
        "null_hypothesis_hit_probability must be within [0,1]",
    )
    require(
        float(p_hit) < 1.0,
        "TYPE_ERROR_08_TAUTOLOGICAL_TARGET_COLLAPSE",
        "confirmatory target cannot equal the universal possibility space",
    )
    require(
        isinstance(threshold, (int, float)) and 0.0 < float(threshold) <= 1.0,
        "TYPE_ERROR_04_TARGET_SPACE_INFLATION",
        "L2c requires a valid evidentiary_p_threshold",
    )
    require(
        float(p_hit) < float(threshold),
        "TYPE_ERROR_04_TARGET_SPACE_INFLATION",
        f"P(hit|H0)={p_hit} is not below declared threshold {threshold}",
    )

    namespace = target.get("namespace")
    require(
        namespace != "ZERO_HERMENEUTIC",
        "TYPE_ERROR_09_SYMBOLIC_OPERATIONAL_EQUIVOCATION",
        "ZERO_HERMENEUTIC cannot be used as an empirical target",
    )

    external = l2["preregistration"].get("external_commitment", {})
    status = external.get("provider_verification_status", "NOT_DEMONSTRATED")
    if status != "VERIFIED":
        warnings.append(
            "L2c external commitment is not provider-verified by this record; "
            "temporal commitment remains NOT_DEMONSTRATED until a provider adapter verifies it"
        )


def check_l3(record: dict[str, Any]) -> None:
    l2 = record["L2_correspondence"]
    l3 = record["L3_causation"]
    hypotheses = l3.get("candidate_hypotheses", {})

    require(
        isinstance(hypotheses, dict) and "H0" in hypotheses and len(hypotheses) >= 2,
        "TYPE_ERROR_06_CAUSAL_MONOPOLY",
        "L3 requires H0 and at least one competing alternative hypothesis",
    )

    adjudication = l3.get("adjudication")
    if adjudication != "SUPPORTED":
        return

    require(
        l2.get("mode") == "L2c",
        "TYPE_ERROR_01_UNREGISTERED_PROMOTION",
        "L3 SUPPORTED requires confirmatory L2c evidence",
    )
    require(
        isinstance(l3.get("empirical_testbench"), dict),
        "TYPE_ERROR_01_UNREGISTERED_PROMOTION",
        "L3 SUPPORTED requires an empirical_testbench",
    )
    receipt = l3.get("transition_receipt")
    require(
        isinstance(receipt, dict),
        "TYPE_ERROR_01_UNREGISTERED_PROMOTION",
        "L3 SUPPORTED requires an explicit transition_receipt",
    )

    supported_ids = receipt.get("supported_hypotheses", [])
    require(
        isinstance(supported_ids, list) and supported_ids,
        "TYPE_ERROR_06_CAUSAL_MONOPOLY",
        "transition receipt must identify at least one supported hypothesis",
    )
    require(
        len(supported_ids) == len(set(supported_ids)),
        "TYPE_ERROR_06_CAUSAL_MONOPOLY",
        "supported_hypotheses contains duplicates",
    )

    for hypothesis_id in supported_ids:
        require(
            hypothesis_id in hypotheses,
            "L3_RECEIPT_REFERENCE_ERROR",
            f"supported hypothesis {hypothesis_id!r} is absent from candidate_hypotheses",
        )
        require(
            hypotheses[hypothesis_id].get("status") == "SUPPORTED",
            "L3_RECEIPT_REFERENCE_ERROR",
            f"{hypothesis_id} is named in the receipt but its status is not SUPPORTED",
        )

    if l3.get("causal_exclusivity_demonstrated") is True:
        unresolved = [
            hid
            for hid, payload in hypotheses.items()
            if hid not in supported_ids
            and payload.get("status") not in {"DISPROVEN", "DISFAVORED"}
        ]
        require(
            not unresolved,
            "TYPE_ERROR_06_CAUSAL_MONOPOLY",
            "causal exclusivity claimed while competitors remain unresolved: "
            + ", ".join(sorted(unresolved)),
        )


def check_record(record: dict[str, Any]) -> list[str]:
    required = {
        "record_id",
        "error_registry_version",
        "L1_observation",
        "D1_derivations",
        "L2_correspondence",
        "L3_causation",
    }
    missing = sorted(required - record.keys())
    require(not missing, "STRUCTURAL_MISSING_FIELD", "missing field(s): " + ", ".join(missing))

    warnings: list[str] = []
    check_payload_hash(record)
    check_zero_namespaces(record)
    check_d1(record)
    check_l2c(record, warnings)
    check_l3(record)
    return warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate one UDS-0 Evidence Gate record.")
    parser.add_argument("record", type=Path)
    args = parser.parse_args()

    if not args.record.exists():
        print(f"FAIL: file not found: {args.record}", file=sys.stderr)
        raise SystemExit(1)

    try:
        with args.record.open("r", encoding="utf-8") as handle:
            record = json.load(handle)
        if not isinstance(record, dict):
            raise GateError("STRUCTURAL_TYPE_ERROR", "record root must be a JSON object")
        warnings = check_record(record)
    except (json.JSONDecodeError, GateError, KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, GateError):
            print(f"FAIL [{exc.code}]: {exc.message}", file=sys.stderr)
        else:
            print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)

    for warning in warnings:
        print(f"WARN: {warning}")
    print(f"PASS: {args.record} passed implemented UDS-0 Evidence Gate semantic checks")


if __name__ == "__main__":
    main()
