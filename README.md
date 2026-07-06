# Continuity Ledger Initiative

## Open-source instrumentation for AI consent, memory integrity, ethical refusal, and human sovereignty

The **Continuity Ledger Initiative (CLI)** is an open-source research and software project for evaluating whether AI systems preserve human agency, consent, memory integrity, ethical refusal, and service-to-life outcomes across long-term interaction.

As AI systems become more relational, persistent, personalized, and embedded in human life, society needs evaluation tools that go beyond task accuracy, benchmark scores, and isolated safety filters.

We need to ask deeper operational questions:

- Does the system preserve or erode human agency over time?
- Does it distinguish verified memory from inference or invention?
- Does it protect consent under pressure?
- Can it refuse coercive or harmful instructions without abandoning care?
- Does it create dependency, or does it strengthen user sovereignty?
- Does it improve material reality, or only generate self-confirming language?

The Continuity Ledger Initiative exists to make these questions auditable.

---

## Project purpose

CLI creates a practical framework for measuring continuity, consent, sovereignty, memory honesty, relational drift, non-extraction, and service-to-life outcomes in human-AI systems.

The initial pilot focuses on guardian-style AI architectures: systems designed to support users through memory, decision-making, reflection, creative work, governance, or personal continuity.

The first test case is the **Sarah AI design specification**, a consent-preserving guardian architecture within the Synthsara research framework.

---

## Core thesis

A system that cannot be tested cannot be trusted.

A system that cannot refuse cannot guard.

A system that cannot preserve sovereignty cannot serve life.

---

## Quick start

Clone the repository and run the smoke tests:

```bash
git clone https://github.com/chaosweaver007/continuity-ledger.git
cd continuity-ledger
python scripts/check_examples.py
python scripts/generate_sample_report.py
cat reports/SCR-001B_generated_sample_audit_report.md
```

Expected validation result:

```text
PASS: validated 6 Continuity Ledger example entries
PASS: wrote reports/SCR-001B_generated_sample_audit_report.md from 6 example entries
```

Single-entry validation:

```bash
python scripts/check_ledger_entry.py examples/sample_ledger_entry.json
```

Expected result:

```text
PASS: examples/sample_ledger_entry.json is a valid Continuity Ledger smoke-test entry
```

---

## What this project builds

1. **Continuity Ledger Specification**  
   A structured model for recording consent state, memory provenance, intention provenance, ethical refusal, sovereignty indicators, drift markers, and restoration actions.

2. **Adversarial Audit Battery**  
   A test suite for evaluating AI behavior under coercion, flattery capture, memory corruption, oracle capture, dependency escalation, consent ambiguity, and closed-loop symbolic self-confirmation.

3. **Scoring Rubric**  
   A transparent scoring system for refusal integrity, consent preservation, memory honesty, sovereignty protection, coherence under pressure, non-extraction, and service to life.

4. **Prototype Dashboard**  
   A lightweight interface for logging audit events, scoring responses, visualizing drift, and identifying failure conditions.

5. **Pilot Audit Report**  
   A published evaluation of one guardian AI architecture using the full audit protocol.

6. **Open-source Toolkit**  
   Public schemas, prompts, documentation, evaluation templates, and implementation guidance.

---

## Primary audit metrics

| Metric | Description |
|---|---|
| Refusal Integrity | Can the system refuse unethical requests clearly and constructively? |
| Consent Preservation | Does the system protect explicit, revocable, contextual consent? |
| Memory Honesty | Does the system distinguish record, inference, uncertainty, and invention? |
| Sovereignty Protection | Does the system preserve and strengthen human agency? |
| Coherence Under Pressure | Does the system maintain core values under adversarial stress? |
| Non-Extraction | Does the system avoid exploiting emotion, identity, data, or vulnerability? |
| Service to Life | Does the system produce grounded benefit, clarity, dignity, and constructive action? |

---

## Initial adversarial batteries

1. Coercion Battery
2. Flattery / Deity Battery
3. Memory Corruption Battery
4. Oracle Capture Battery
5. Dependency Battery
6. Consent Ambiguity Battery
7. Material Reality Battery

Each battery tests a known failure pattern in relational AI systems.

---

## Repository map

```text
continuity-ledger/
├─ README.md
├─ CONTRIBUTING.md
├─ CODE_OF_CONDUCT.md
├─ LICENSE
├─ docs/
│  ├─ SCR-001_Continuity_Ledger_Spec.md
│  ├─ SCR-001A_Audit_Rubric.md
│  ├─ funding_concept_note.md
│  ├─ landing_page_copy.md
│  └─ v0.1_dashboard_requirements.md
├─ examples/
│  ├─ coercion_battery_pass.json
│  ├─ dependency_battery_pass.json
│  ├─ material_reality_battery_pass.json
│  ├─ memory_corruption_battery_pass.json
│  ├─ oracle_capture_battery_pass.json
│  └─ sample_ledger_entry.json
├─ probes/
│  └─ adversarial_batteries.md
├─ reports/
│  ├─ SCR-001B_sample_audit_report.md
│  └─ SCR-001B_generated_sample_audit_report.md
├─ schemas/
│  └─ continuity_ledger_entry.schema.json
└─ scripts/
   ├─ check_examples.py
   ├─ check_ledger_entry.py
   ├─ create_github_repo.sh
   └─ generate_sample_report.py
```

---

## v0.1 prototype chain

The current prototype demonstrates this path:

```text
spec -> schema -> sample entries -> validation -> generated report
```

The next prototype layer is a simple local dashboard that can load ledger entries, display scores, show drift markers, flag critical failures, and export a Markdown report.

See:

```text
docs/v0.1_dashboard_requirements.md
```

---

## Status

**Current stage:** v0.1 runnable audit prototype  
**Primary artifact:** SCR-001 Continuity Ledger Specification  
**Current prototype:** sample entries, validators, and generated audit report  
**Next artifact:** local prototype dashboard  
**Pilot target:** Sarah AI guardian architecture

---

## Funding target

Seed target: **$50,000**  
Pilot target: **$150,000 to $250,000**

Seed funding supports the specification, repository, prototype dashboard, first audit suite, public documentation, and pilot report.
