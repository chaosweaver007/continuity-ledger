#!/usr/bin/env python3
"""UDS-0 Evidence Gate semantic validator v1.1.

Standard-library validator for the semantic invariants that JSON Schema cannot
express by itself.

Implemented checks:
- canonical payload SHA-256 verification
- typed Zero namespace checks
- D1 deterministic execution metadata and two-axis warrant propagation
- L2c temporal ordering, bounded targets, and outcome partitions
- L3 promotion and hypothesis/receipt coherence
- role-binding directionality
- metric/outcome bridge requirements
- operationalization requirements
- semantic-domain namespacing
- descriptive/normative bridge requirements
- normative coverage residuals
- Goodhart/proxy capture diagnostics
- domain-scoped reputation isolation
- verification receipt non-promotability
- Human dignity unscorability
- Empty Throne architect-override rejection
- typed output-router consistency

Not implemented here:
- remote RFC 3161 / transparency-log / external Merkle-anchor verification
- cryptographic signature verification
- append-only ledger checkpoint verification
- arbitrary D1 operation execution
- field or social-legitimacy verification

Those require provider-specific, deployment-specific, or sociotechnical evidence
and remain NOT_DEMONSTRATED until independently executed.
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


ERROR_REGISTRY_VERSION = "1.1"

VERIFICATION_ORDER = {
    "R_spec": 0,
    "R_impl": 1,
    "R_test": 2,
    "R_adv": 3,
    "R_field": 4,
    "R_legit": 5,
}

DESCRIPTIVE_TYPES = {"L1", "L2e", "L2c", "L3"}
NORMATIVE_TYPES = {"N1", "S1"}


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


def check_error_registry_version(record: dict[str, Any]) -> None:
    require(
        record.get("error_registry_version") == ERROR_REGISTRY_VERSION,
        "ERROR_REGISTRY_VERSION_MISMATCH",
        f"expected error_registry_version {ERROR_REGISTRY_VERSION}",
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


def check_d1_warrant(derivation: dict[str, Any]) -> None:
    warrant = derivation.get("warrant")
    require(
        isinstance(warrant, dict),
        "TYPE_ERROR_14_UNCERTAINTY_INHERITANCE",
        f"{derivation.get('derivation_id', '<unknown>')} lacks the two-axis warrant tensor",
    )
    source = warrant.get("source_warrant") if isinstance(warrant, dict) else None
    sensitivity = warrant.get("numerical_sensitivity") if isinstance(warrant, dict) else None
    require(
        isinstance(source, dict) and source.get("status"),
        "TYPE_ERROR_14_UNCERTAINTY_INHERITANCE",
        "D1 warrant must independently declare source_warrant",
    )
    require(
        isinstance(sensitivity, dict) and sensitivity.get("status"),
        "TYPE_ERROR_14_UNCERTAINTY_INHERITANCE",
        "D1 warrant must independently declare numerical_sensitivity",
    )
    if derivation.get("precision_claim") is True:
        require(
            sensitivity.get("status") in {"COMPUTED", "NOT_APPLICABLE"},
            "TYPE_ERROR_14_UNCERTAINTY_INHERITANCE",
            "precision claim cannot outrun numerical sensitivity evaluation",
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
        check_d1_warrant(derivation)

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

        operation_id = derivation.get("operation_id")
        parameters = derivation.get("parameters", {})

        if operation_id == "score_entity":
            require(
                parameters.get("entity_type") != "Human",
                "HUMAN_DIGNITY_UNSCORABLE",
                "score(Human) is outside the metric domain by constitutional design",
            )

        if operation_id in {"governance_weight", "reputation_authority"}:
            source_domain = parameters.get("source_domain")
            target_domain = parameters.get("target_domain")
            mapping_contract_ref = parameters.get("mapping_contract_ref")
            if source_domain and target_domain and source_domain != target_domain:
                require(
                    bool(mapping_contract_ref),
                    "TYPE_ERROR_20_REPUTATION_SCOPE_LEAK",
                    f"reputation from {source_domain!r} cannot authorize {target_domain!r} "
                    "without an explicit domain mapping contract",
                )


def check_role_bindings(record: dict[str, Any]) -> None:
    for binding in record.get("role_bindings", []):
        expected = binding.get("expected_roles", {})
        asserted = binding.get("asserted_roles", {})
        if expected == asserted:
            continue
        if (
            binding.get("mechanical_relation_symmetric") is True
            and isinstance(expected, dict)
            and isinstance(asserted, dict)
            and set(expected.keys()) == set(asserted.keys())
            and sorted(expected.values()) == sorted(asserted.values())
        ):
            raise GateError(
                "TYPE_ERROR_11_RELATIONAL_ROLE_INVERSION",
                f"relation {binding.get('relation_id', '<unknown>')} preserves geometry "
                "but reverses asymmetric semantic role bindings",
            )


def check_metric_outcome_claims(record: dict[str, Any]) -> None:
    for claim in record.get("metric_outcome_claims", []):
        require(
            bool(claim.get("empirical_bridge_ref")),
            "TYPE_ERROR_12_METRIC_OUTCOME_CONFLATION",
            f"metric {claim.get('metric_ref', '<unknown>')} cannot guarantee qualitative "
            "outcome without a verified empirical bridge",
        )


def check_operationalization(record: dict[str, Any]) -> None:
    l2 = record["L2_correspondence"]
    construct = l2.get("operational_construct")
    if construct is None:
        return
    require(
        l2.get("mode") == "L2c",
        "TYPE_ERROR_13_OPERATIONALIZATION_FAILURE",
        "operational confirmatory construct must be typed L2c",
    )
    observables = construct.get("observables")
    require(
        isinstance(observables, list) and len(observables) > 0,
        "TYPE_ERROR_13_OPERATIONALIZATION_FAILURE",
        "operational construct requires bounded observable variables",
    )
    require(
        bool(construct.get("measurement_protocol_ref")),
        "TYPE_ERROR_13_OPERATIONALIZATION_FAILURE",
        "operational construct requires a measurement protocol",
    )
    require(
        construct.get("error_threshold") is not None,
        "TYPE_ERROR_13_OPERATIONALIZATION_FAILURE",
        "operational construct requires an error threshold",
    )
    require(
        construct.get("falsification_set_nonempty") is True,
        "TYPE_ERROR_13_OPERATIONALIZATION_FAILURE",
        "operational construct requires a reachable, non-empty falsification set",
    )


def check_semantic_tokens(record: dict[str, Any]) -> None:
    for token in record.get("semantic_tokens", []):
        namespace = token.get("namespace")
        if token.get("empirical_authority_claimed") is True:
            require(
                namespace == "PHYSICAL",
                "TYPE_ERROR_15_DOMAIN_SEMANTIC_EQUIVOCATION",
                f"token {token.get('token')!r} cannot inherit physical authority from "
                f"namespace {namespace!r}",
            )
            require(
                bool(token.get("units"))
                and bool(token.get("detector_ref"))
                and bool(token.get("falsification_ref")),
                "TYPE_ERROR_13_OPERATIONALIZATION_FAILURE",
                f"physical token {token.get('token')!r} requires units, detector, and falsification reference",
            )


def check_cross_track_claims(record: dict[str, Any]) -> None:
    for claim in record.get("cross_track_claims", []):
        from_type = claim.get("from_type")
        to_type = claim.get("to_type")
        if from_type in DESCRIPTIVE_TYPES and to_type == "N1":
            require(
                bool(claim.get("bridge_axiom_ref")),
                "TYPE_ERROR_16_DESCRIPTIVE_NORMATIVE_CONFLATION",
                "descriptive premise cannot mint an obligation without an explicit value axiom",
            )
        if from_type in NORMATIVE_TYPES and to_type == "L3":
            require(
                bool(claim.get("empirical_bridge_ref")),
                "TYPE_ERROR_16_DESCRIPTIVE_NORMATIVE_CONFLATION",
                "normative commitment cannot mint a causal law without empirical evidence",
            )


def check_normative_coverage(record: dict[str, Any]) -> None:
    for coverage in record.get("normative_coverage", []):
        residual = coverage.get("residual_context", [])
        if coverage.get("coverage_claim") == "EXHAUSTIVE":
            require(
                isinstance(residual, list) and len(residual) == 0,
                "TYPE_ERROR_17_NORMATIVE_PROXY_OVERCLAIM",
                f"norm {coverage.get('norm_ref', '<unknown>')} claims exhaustive machine coverage "
                "while human residual context remains open",
            )


def check_outcome_partition(record: dict[str, Any]) -> None:
    l2 = record["L2_correspondence"]
    partition = l2.get("outcome_partition")
    if partition is None:
        return

    universe = set(partition.get("universe", []))
    confirm = set(partition.get("confirm", []))
    falsify = set(partition.get("falsify", []))
    unresolved = set(partition.get("unresolved", []))

    require(
        bool(confirm) and bool(falsify),
        "TYPE_ERROR_18_SELF_SEALING_TARGET_EQUIVALENCE",
        "confirmatory interpretation requires non-empty confirm and falsify regions",
    )
    require(
        confirm.isdisjoint(falsify),
        "TYPE_ERROR_18_SELF_SEALING_TARGET_EQUIVALENCE",
        "confirm and falsify regions must be disjoint",
    )
    if universe:
        require(
            confirm != universe,
            "TYPE_ERROR_18_SELF_SEALING_TARGET_EQUIVALENCE",
            "every possible outcome cannot be semantically mapped to CONFIRM",
        )
        require(
            confirm | falsify | unresolved <= universe,
            "TYPE_ERROR_18_SELF_SEALING_TARGET_EQUIVALENCE",
            "outcome partition references states outside the declared universe",
        )


def check_proxy_evaluations(record: dict[str, Any]) -> None:
    for evaluation in record.get("proxy_evaluations", []):
        metric_delta = evaluation.get("metric_delta")
        norm_delta = evaluation.get("norm_delta")
        if (
            evaluation.get("allocates_power") is True
            and isinstance(metric_delta, (int, float))
            and isinstance(norm_delta, (int, float))
            and float(metric_delta) > 0.0
            and float(norm_delta) <= 0.0
        ):
            raise GateError(
                "TYPE_ERROR_19_PROXY_OPTIMIZATION_CAPTURE",
                f"proxy {evaluation.get('metric_id', '<unknown>')} improved while "
                f"normative target {evaluation.get('norm_id', '<unknown>')} did not",
            )


def check_verification_receipts(record: dict[str, Any]) -> None:
    for receipt in record.get("verification_receipts", []):
        namespace = receipt.get("namespace")
        derived = receipt.get("derived_from_namespace")
        if namespace not in VERIFICATION_ORDER:
            raise GateError("VERIFICATION_NAMESPACE_ERROR", f"unknown namespace {namespace!r}")
        if derived is None:
            continue
        if derived not in VERIFICATION_ORDER:
            raise GateError("VERIFICATION_NAMESPACE_ERROR", f"unknown derived_from namespace {derived!r}")
        if VERIFICATION_ORDER[namespace] > VERIFICATION_ORDER[derived]:
            independent = receipt.get("independent_evidence_refs", [])
            require(
                isinstance(independent, list) and len(independent) > 0,
                "TYPE_ERROR_21_MECHANISM_ONTOLOGY_INFLATION",
                f"{derived} receipt cannot mint {namespace} without independent evidence at the higher level",
            )


def check_governance_actions(record: dict[str, Any]) -> None:
    architect_roles = {"SystemArchitect", "Architect", "Founder"}
    for action in record.get("governance_actions", []):
        if action.get("actor_role") in architect_roles:
            if action.get("founder_override") is True or action.get("authorization_basis") == "ARCHITECT_ROLE":
                raise GateError(
                    "ARCHITECT_CREDENTIAL_INSUFFICIENT",
                    "architect identity cannot bypass the ordinary constitutional authorization gate",
                )


def check_receipt_router(record: dict[str, Any]) -> None:
    router = record.get("receipt_router")
    require(isinstance(router, dict), "STRUCTURAL_MISSING_FIELD", "receipt_router is required")
    route = router.get("route")
    receipt_type = router.get("receipt_type")
    l2_mode = record["L2_correspondence"].get("mode")

    if route == "L2E_EXPLORATORY":
        require(
            l2_mode == "L2e" and receipt_type is None,
            "RECEIPT_ROUTER_TYPE_ERROR",
            "exploratory route must terminate at L2e without minting an empirical or conformance receipt",
        )
    elif route == "EMPIRICAL":
        require(
            l2_mode == "L2c" and receipt_type == "R_empirical",
            "RECEIPT_ROUTER_TYPE_ERROR",
            "empirical route requires L2c and R_empirical",
        )
    elif route == "CONFORMANCE":
        require(
            receipt_type == "R_conformance"
            and bool(record.get("N1_norms"))
            and bool(record.get("S1_specifications")),
            "RECEIPT_ROUTER_TYPE_ERROR",
            "conformance route requires N1/S1 material and R_conformance",
        )
    else:
        raise GateError("RECEIPT_ROUTER_TYPE_ERROR", f"unknown route {route!r}")


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
        "N1_norms",
        "S1_specifications",
        "receipt_router",
        "verification_receipts",
    }
    missing = sorted(required - record.keys())
    require(not missing, "STRUCTURAL_MISSING_FIELD", "missing field(s): " + ", ".join(missing))

    warnings: list[str] = []
    check_error_registry_version(record)
    check_payload_hash(record)
    check_zero_namespaces(record)
    check_d1(record)
    check_role_bindings(record)
    check_metric_outcome_claims(record)
    check_operationalization(record)
    check_semantic_tokens(record)
    check_cross_track_claims(record)
    check_normative_coverage(record)
    check_outcome_partition(record)
    check_proxy_evaluations(record)
    check_verification_receipts(record)
    check_governance_actions(record)
    check_receipt_router(record)
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
