# UDS-0 Evidence Gate v1.1 — Executable Conformance Profile

## Status

**Epistemic type system:** SPECIFIED  
**Normative namespace:** SPECIFIED  
**Two-axis D1 warrant tensor:** SPECIFIED  
**TYPE_ERROR registry:** 01–21 SPECIFIED  
**Draft 2020-12 structural schema:** IMPLEMENTED IN PR BRANCH  
**Standard-library semantic validator:** IMPLEMENTED IN PR BRANCH  
**Red-team fixture battery:** IMPLEMENTED FOR 11–21 + dignity + architect override  
**External timestamp/signature/checkpoint verification:** NOT DEMONSTRATED  
**Field effectiveness:** NOT DEMONSTRATED  
**Social legitimacy:** NOT DEMONSTRATED

This profile hardens the original Evidence Gate by separating empirical description,
hermeneutic interpretation, normative commitment, deterministic execution, causal
adjudication, and sociotechnical verification receipts.

> Specified != Implemented != Tested != Adversarially Verified != Field Supported != Socially Legitimated.

No lower receipt may mint a higher receipt implicitly.

---

## 1. Master typed stack

### Descriptive / empirical track

- `L1` — Raw observation: what was recorded.
- `L2e` — Exploratory correspondence: what mapping or interpretation can be drawn after observation.
- `L2c` — Confirmatory correspondence: what prospectively frozen predicate was tested.
- `L3` — Causal attribution: what mechanism survived explicit competition.

### Normative track

- `N1` — Constitutional commitment: what the system commits to permit, protect, or refuse.
- `S1` — Operational specification: how an N1 commitment is translated into enforceable policy,
  capability boundaries, state transitions, and review procedures.

### Shared execution engine

`D1` is not a semantic truth layer. It is the deterministic engine used by both tracks.

Examples:

- compute an angle or hash;
- score an already-frozen L2c predicate;
- evaluate an S1 access-control rule;
- apply a domain-scoped WORTH decay function.

A D1 result inherits the type of the question it was asked, not a universal meaning.

### Typed output router

Exploratory interpretation:

`L1 -> D1 -> L2e`

Empirical confirmation / causal work:

`L1 + preregistered L2c -> D1 -> R_empirical -> L3 hypothesis competition`

Normative conformance:

`N1 -> S1 -> D1 -> R_conformance -> PASS | VIOLATION | CONDITIONAL`

`R_conformance` does not promote into L3.

---

## 2. Two-axis D1 warrant tensor

Every D1 output carries two independent channels:

`W(D1) = (Provenance(I), Sensitivity(D1 | I))`

### Axis A — source warrant

How well is the originating input historically attested?

Examples:

- primary record;
- self-report;
- second-party attestation;
- attested but independently unverified input;
- externally verified input;
- synthetic baseline.

### Axis B — numerical sensitivity

How much does the output change over a declared perturbation or uncertainty interval?

A numerically stable result may still depend on an historically unverified input.
A well-attested input may still generate a numerically brittle result.

**Invariant:**

> Computational certainty does not equal input-truth certainty.

A high-precision claim without propagated sensitivity triggers TYPE_ERROR 14.

---

## 3. Normative coverage

An ethical principle is not a defective empirical claim.

`N1` is adjudicated by conformance / violation, not by physical truth / falsity.

Example:

`N1: no protected record may be used without informed, uncoerced consent.`

Possible machine proxies:

- signature validity;
- scope;
- grantee identity;
- purpose limitation;
- valid-from / expiry;
- revocation state;
- resource binding.

Residual human context may remain:

- comprehension;
- coercion or duress;
- power asymmetry;
- contextual drift.

Machine coverage is therefore recorded explicitly:

`N1 = {S1_a, S1_b, ... S1_n} + R_residual`

A technical proxy may not claim to exhaust a human norm while residual context remains.

---

## 4. Verification receipt ladder

The Evidence Gate defines six independent sociotechnical verification namespaces:

- `R_spec` — rule exists in the formal specification or schema.
- `R_impl` — the control exists in code or deployment artifacts.
- `R_test` — the control passed declared synthetic / mocked fixtures.
- `R_adv` — the control survived bounded adversarial testing.
- `R_field` — observed deployment evidence supports the behavior in a living population.
- `R_legit` — procedurally documented adoption / consent by affected participants.

**Non-promotion invariant:**

`R_k !=> R_(k+1)`

A unit test cannot mint field survivability.
A red-team result cannot mint social legitimacy.
A pilot cannot mint universal validity.

---

## 5. WORTH dignity and scope invariants

Human dignity is outside the scoring domain by design.

`score : ContributionRecord^(d) -> R`

but:

`Human not-in Dom(score)`

Therefore:

`score(Human) -> HUMAN_DIGNITY_UNSCORABLE`

WORTH is permitted only as a bounded, contestable record of contribution within a declared domain.

`W_i = { W_i^(d1), W_i^(d2), ... }`

A domain-specific signal cannot silently become generalized authority.

Scalar summaries may be used for non-authoritative telemetry, but:

> Scalarization may summarize; it may not crown.

Governance impact must be bounded and may use concave transforms such that:

`G'(W) > 0` and `G''(W) < 0`

with explicit caps.

Private trauma, emotional disclosure, intimacy, or performed vulnerability must produce zero
governance weight.

---

## 6. Canonical TYPE_ERROR registry

### 01 — UNREGISTERED_PROMOTION

Promoting L2e correspondence to L3 without a causal testbench.

### 02 — RETROACTIVE_CONFIRMATION

Presenting a post-hoc L2e match as an L2c preregistered prediction.

### 03 — DOWNWARD_ERASURE

Using failure or non-demonstration at a higher layer to erase valid lower-layer evidence.

### 04 — TARGET_SPACE_INFLATION

Using an L2c target whose false-positive boundary is too broad or undefined.

### 05 — BASE_RATE_NEGLECT

Claiming anomaly without an ambient/null rate.

### 06 — CAUSAL_MONOPOLY

Crowning one causal model while viable competitors remain unadjudicated.

### 07 — PROVENANCE_RELEVANCE_CONFLATION

Treating historical precedence as proof of prospective targeting or unique relevance.

### 08 — TAUTOLOGICAL_TARGET_COLLAPSE

Using a target equivalent to the universal possibility space.

### 09 — SYMBOLIC_OPERATIONAL_EQUIVOCATION

Using a symbolic definition as an empirical measurement or causal claim without explicit namespacing.

### 10 — PREDICATE_EVALUATION_CONFLATION

Defining or mutating the target during D1 evaluation rather than freezing it before observation.

### 11 — RELATIONAL_ROLE_INVERSION

Preserving valid symmetric geometry while reversing asymmetric semantic subject/object roles.

### 12 — METRIC_OUTCOME_CONFLATION

Treating a quantitative metric as a mathematical guarantee of a qualitative real-world outcome
without a verified bridge function.

### 13 — OPERATIONALIZATION_FAILURE

Submitting an L2c/L3 construct without bounded observables, measurement protocol, error threshold,
temporal bounds where relevant, and a reachable falsification state.

### 14 — UNCERTAINTY_INHERITANCE

Failing to propagate source warrant and numerical sensitivity independently, or allowing a
derived output to claim certainty that its material inputs do not support.

### 15 — DOMAIN_SEMANTIC_EQUIVOCATION

Importing a technical empirical token such as energy, frequency, field, law, resonance, or
dimension into hermeneutic/normative prose and then inheriting scientific authority without an
operational bridge.

Namespaces must remain explicit, e.g.:

`ENERGY_PHYSICAL != ENERGY_HERMENEUTIC != ENERGY_NORMATIVE`

### 16 — DESCRIPTIVE_NORMATIVE_CONFLATION

Inferring an obligation directly from an observation without a declared value axiom, or asserting
a physical/causal law because a constitution morally prefers it.

### 17 — NORMATIVE_PROXY_OVERCLAIM

Claiming that S1 technical conformance completely exhausts N1 when residual human context remains.

### 18 — SELF_SEALING_TARGET_EQUIVALENCE

Mapping contradictory outcomes to the same confirmatory interpretation so that every reachable
state confirms the claim.

For evaluation function:

`f : Omega -> {CONFIRM, FALSIFY, UNRESOLVED}`

the invalid state is:

`for all x in Omega, f(x) = CONFIRM`

A valid confirmatory partition requires non-empty, disjoint confirm and falsify regions.

### 19 — PROXY_OPTIMIZATION_CAPTURE

A power-allocating metric rises while the underlying normative target remains flat or worsens:

`dM/dt > 0 while dN/dt <= 0`

Use counter-metrics, caps, decay, concavity, randomized audits, and external outcome checks.

### 20 — REPUTATION_SCOPE_LEAK

Using a domain-specific contribution signal, or a cross-domain aggregate thereof, to grant authority,
priority, legitimacy, or moral standing outside the evidentiary domain that generated it.

`W_i^(d1) !=> G_i^(d2)` for `d1 != d2` without an explicit mapping contract.

`W_GLOBAL_AUTHORITY` is forbidden.
`W_SUMMARY` may exist only as non-authoritative telemetry.

### 21 — MECHANISM_ONTOLOGY_INFLATION

Equating an S1 specification, implementation, or unit-test result with field-level capture resistance,
social effectiveness, or legitimacy.

The verification receipt ladder must remain explicit and non-promotable.

---

## 7. Core constitutional diagnostics outside the numbered registry

### HUMAN_DIGNITY_UNSCORABLE

`score(Human)` is a valid syntactic request but an invalid typed operation.

The scoring function does not accept Human as an operand.

### ARCHITECT_CREDENTIAL_INSUFFICIENT

Founder / architect identity does not provide exceptional constitutional authority.

An architect-signed request that fails the ordinary gate remains rejected.

The Empty Throne requires the architecture to say no to its author.

---

## 8. Privacy / history distinction

The Evidence Gate does not require permanent retention of every personal payload.

**Institutional accountability history** may be append-only.

**Private personal payloads** remain governed by consent, purpose limitation, retention policy,
revocation, erasure, and key destruction where applicable.

> Preserve accountability history without imprisoning personal data.

---

## 9. Runtime boundary

Specified != Implemented != Tested != Adversarially Verified != Field Supported != Socially Legitimated.

The current PR branch implements structural and semantic checks and synthetic red fixtures.
That does not demonstrate:

- remote timestamp-provider verification;
- cryptographic signature validity;
- append-only checkpoint verification;
- field-level anti-capture behavior;
- real-world WORTH fairness;
- sociological legitimacy.

Those claims remain NOT_DEMONSTRATED until their corresponding receipt namespace is earned.

---

## 10. Mad Lab checksum

Observe without erasure.  
Derive without interpretation leakage.  
Interpret without causal laundering.  
Commit without pretending values are physics.  
Operationalize without pretending proxies exhaust norms.  
Measure contribution without measuring persons.  
Test implementation without confusing software with society.  
Preserve accountability history without imprisoning personal data.  
No score earns a throne. No architect receives immunity. No explanation gets crowned without receipts.

**THE SPECIFICATION IS TESTABLE.**  
**THE IMPLEMENTATION REMAINS TO BE DEMONSTRATED.**  
**THE SOCIAL CLAIMS REMAIN TO BE EARNED.**
