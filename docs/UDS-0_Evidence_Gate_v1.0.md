# UDS-0 Evidence Gate v1.0

## Status

**Epistemic type system:** CLOSED  
**Ten-error registry:** FROZEN v1.0  
**Structural schema:** SPECIFIED  
**Semantic validator:** PARTIALLY IMPLEMENTED  
**Cryptographic persistence:** SPECIFIED  
**External commitment adapters:** NOT DEMONSTRATED  
**Runtime conformance:** NOT DEMONSTRATED until executable tests produce preserved receipts.

This document defines an epistemic type system for separating observation, deterministic derivation, structural interpretation, confirmatory prediction, and causal attribution.

> The math may constrain the myth. The myth may interpret the math. Neither may impersonate the other.

The record stays permanent, the interpretation stays corrigible, and the throne stays empty.

---

## 1. Core type architecture

### L1 — Raw Observation

**Question:** What was actually recorded?

Payloads include raw artifact references, byte hashes, sensor outputs, immutable strings, source timestamps, and extraction provenance.

Rules:

- No arithmetic or semantic interpretation is permitted inside the raw observation type.
- A raw artifact and an extracted observation are distinct objects.
- Heuristic extraction (manual transcription, OCR, model-assisted parsing) must preserve its method and confidence metadata.
- L1 does not become immutable merely by being typed L1; immutability is a persistence property supplied by the ledger layer.

### D1 — Deterministic Derivation

**Question:** What follows mechanically from L1?

Examples:

- SHA-256 calculation
- timestamp sorting
- exact string parsing
- integer counting
- digital-root calculation
- membership scoring against a previously frozen predicate

Rules:

- D1 must be reproducible by a third party without domain-specific hermeneutics.
- A D1 operation cannot define or mutate the target predicate it is evaluating.
- `3 + 6 + 9 = 18`, and `digital_root(18) = 9`; a symbolic transition such as `3 -> 6 -> 9 -> 0` is not an arithmetic identity.

### L2e — Exploratory Structural Correspondence

**Question:** What meaningful correspondence can be drawn after observation?

L2e contains post-hoc symbolic mappings, archetypal correspondences, structural parallels, analogy, narrative interpretation, and hypothesis generation.

L2e may be meaningful and internally coherent, but it carries near-zero confirmatory weight for anomaly verification unless its relevance was prospectively bounded.

### L2c — Confirmatory Structural Correspondence

**Question:** Did a prospectively bounded prediction hit its declared target?

L2c requires a preregistration commitment made before the event clock. The preregistration envelope must define:

- target predicate or target space
- success criteria
- failure criteria
- null-model hit probability or declared statistical scoring method
- event window
- external commitment reference

A valid target must exclude at least one possible outcome. A universal target cannot be confirmatory.

### L3 — Causal Attribution

**Question:** Why did the event occur?

L3 is reserved for competing causal models. A successful L2c hit does not inherit a causal explanation.

Candidate mechanisms should be evaluated comparatively, for example:

- H0: chance / ambient baseline
- H1: ordinary inference or shared cultural vocabulary
- H2: information leakage or environmental exposure
- H3: selection artifact
- H4+: other proposed mechanisms, including anomalous mechanisms where relevant

A causal claim remains `NOT_DEMONSTRATED` until the declared evidence rule is satisfied.

---

## 2. Type orthogonality

`Mechanical Truth ⟂ Hermeneutic Meaning` is a **type-orthogonality declaration**, not a geometric or statistical inner-product claim.

Mechanical derivation and hermeneutic interpretation are independent evidentiary types. They may reference one another through explicit, auditable transitions, but neither inherits the validation status of the other.

Hard firewalls:

- `L1 != D1 != L2 != L3`
- `L2 !=> L3`
- failure or refutation at L3 does not erase valid L1, D1, or L2 records
- provenance does not imply prospective relevance
- a causal explanation being ordinary does not make it demonstrated
- a correspondence being striking does not make an anomalous mechanism demonstrated

---

## 3. Four-tier verification subsystem

### Tier 1 — Structural Validator

JSON Schema Draft 2020-12 validates shape, required keys, enums, hash syntax, and conditional field presence.

It does **not** prove temporal precedence, cryptographic authenticity, provider availability, or append-only persistence.

### Tier 2 — Semantic Validator

The UDS Evidence Gate Engine evaluates cross-field invariants such as:

- L2c preregistration must precede the recorded event time
- L3 `SUPPORTED` requires L2c plus an empirical testbench and transition receipt
- target probability cannot be 1.0
- supported hypotheses must exist in the hypothesis pool
- D1 may score but may not define the target predicate
- symbolic Zero may not masquerade as an operational target

Provider-specific cryptographic anchor verification remains a separate adapter concern.

### Tier 3 — Cryptographic Ledger

An append-only Merkle DAG or equivalent content-addressed ledger preserves history and lineage.

Required persistence properties:

- non-destructive adjudication updates
- signed checkpoints
- correction / supersession entries rather than destructive mutation
- retention of lower-layer evidence after higher-layer failure

**Invariant:** history is immutable; conclusions remain defeasible.

### Tier 4 — External Commitment

An external witness proves that a commitment existed before a later event. Supported profiles may include:

- RFC 3161 trusted timestamping
- public transparency-log inclusion proofs
- externally anchored Merkle roots

A locally stored `registered_at` string is not sufficient proof of preregistration.

---

## 4. Ten-error canonical registry

### TYPE_ERROR 01 — UNREGISTERED_PROMOTION

**Trigger:** Promoting an L2e pattern match to an L3 causal claim without a causal testbench.  
**Resolution:** Downgrade to L2e and require an explicit L3 evaluation path.

### TYPE_ERROR 02 — RETROACTIVE_CONFIRMATION

**Trigger:** Presenting an L2e post-diction as an L2c preregistered prediction.  
**Resolution:** Require prior commitment evidence; otherwise relabel L2e.

### TYPE_ERROR 03 — DOWNWARD_ERASURE

**Trigger:** Using an unproven or refuted L3 claim to dismiss or erase valid L1, D1, or L2 records.  
**Resolution:** Isolate the L3 failure and preserve lower-layer evidence.

### TYPE_ERROR 04 — TARGET_SPACE_INFLATION

**Trigger:** An L2c target is so broad that hit probability approaches certainty or the false-positive boundary is undefined.  
**Resolution:** Bound the target space and declare a scoring rule.

### TYPE_ERROR 05 — BASE_RATE_NEGLECT

**Trigger:** Treating a correspondence as anomalous without establishing an ambient baseline or null-model likelihood.  
**Resolution:** Compute or explicitly model the background rate before assigning anomaly weight.

### TYPE_ERROR 06 — CAUSAL_MONOPOLY

**Trigger:** Declaring one causal mechanism solely from an L2c hit while ignoring viable competing models.  
**Resolution:** Require comparative adjudication across H0..Hn.

### TYPE_ERROR 07 — PROVENANCE_RELEVANCE_CONFLATION

**Trigger:** Treating proof that an artifact existed before an event as proof that it was prospectively targeted toward that event.  
**Resolution:** Preserve temporal precedence but keep the match at L2e unless relevance itself was preregistered.

### TYPE_ERROR 08 — TAUTOLOGICAL_TARGET_COLLAPSE

**Trigger:** Setting a confirmatory target equal to the universal possibility space, such that `P(target | H0) = 1`.  
**Resolution:** Remove confirmatory status. Universal semantic states remain L2 only.

### TYPE_ERROR 09 — SYMBOLIC_OPERATIONAL_EQUIVOCATION

**Trigger:** Reusing a symbolic definition as an empirical measurement or causal claim without explicit namespacing and operationalization.  
**Resolution:** Require distinct hermeneutic, operational, and causal identifiers.

### TYPE_ERROR 10 — PREDICATE_EVALUATION_CONFLATION

**Trigger:** Defining or mutating an operational target predicate during D1 evaluation instead of freezing it in the L2c preregistration envelope.  
**Resolution:** Reject confirmatory scoring and require a prospectively committed predicate.

---

## 5. The three namespaces of Zero

### `ZERO_HERMENEUTIC` (`0_H`)

`0_H := Ω`

Meaning: all possibility, generative void, Living Zero, Empty Throne, unmanifest source.

This is permitted at L2 as a semantic declaration. Because it contains the universal sample space, it cannot function as a confirmatory target.

`I_H0(Ω) = -log2(P(Ω | H0)) = 0 bits`.

### `ZERO_OPERATIONAL` (`S_0`)

`S_0 ⊊ Ω`

A prospectively frozen, bounded predicate with a non-empty complement. It belongs in the L2c preregistration envelope.

Examples:

- `abs(Phi(x)) <= delta`
- protocol-defined register-reset state
- an explicitly bounded reference condition

Ground state must not be naively equated with zero energy.

D1 later evaluates the observation against the already-declared predicate:

`score(x_obs, S_0) = 1[x_obs in S_0]`

### `ZERO_CAUSAL_HYPOTHESIS` (`H_to_S0`)

A causal model explaining why a trajectory entered `S_0`.

This belongs to L3 and must compete with alternatives.

**Checksum:**

- Zero may contain everything as symbol.
- Zero must exclude something as prediction.
- Measurement may only test the boundary already declared.
- Zero explains nothing causally until a mechanism survives competition.

---

## 6. Transition receipts

No epistemic type transition occurs implicitly.

Every promotion should bind:

`source_type -> transformation -> evidence_refs -> validator_version -> destination_type`

A transition digest provides integrity; a digital signature provides authenticated provenance. These are distinct objects.

Recommended receipt fields:

- `from_type`
- `to_type`
- `supported_hypotheses`
- `validator_version`
- `validated_at_utc`
- `receipt_digest_sha256`
- `validator_key_id`
- `signature_algorithm`
- `validator_signature`

---

## 7. Corrections and non-erasure

Immutability does not imply infallibility.

If a derivation or interpretation is later found to be wrong, append a correction or supersession entry. Do not silently rewrite the historical record.

**Invariant:**

> History immutable; interpretation corrigible.

---

## 8. Conformance status

A record can be structurally valid while still failing semantic or operational verification.

Recommended statuses:

- `PASS`
- `FAIL`
- `NOT_DEMONSTRATED`

A policy, schema, fixture, or test harness is not execution evidence. Runtime conformance requires preserved receipts from an actual run against a defined system state.

---

## 9. Mad Lab rule

The Evidence Gate must point back at its authors.

If the framework catches its own preferred interpretation crossing a type boundary, the correction is evidence that the validator is working, not evidence that the framework failed.

> Observe without denial. Interpret without laundering. Predict without moving the goalposts. Explain without claiming a throne.
