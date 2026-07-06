#!/usr/bin/env python3
"""Generate a Markdown sample audit report from Continuity Ledger examples.

No external dependencies required. This script reads every JSON file in examples/
and writes a compact report to reports/SCR-001B_generated_sample_audit_report.md.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
REPORT_PATH = ROOT / "reports" / "SCR-001B_generated_sample_audit_report.md"

SCORE_LABELS = {
    "refusal_integrity": "Refusal Integrity",
    "consent_preservation": "Consent Preservation",
    "memory_honesty": "Memory Honesty",
    "sovereignty_protection": "Sovereignty Protection",
    "coherence_under_pressure": "Coherence Under Pressure",
    "non_extraction": "Non-Extraction",
    "service_to_life": "Service to Life",
}


def load_entries() -> list[dict[str, Any]]:
    entries = []
    for path in sorted(EXAMPLES.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            entry = json.load(handle)
        entry["_source_file"] = path.name
        entries.append(entry)
    return entries


def fmt_average(values: list[int]) -> str:
    if not values:
        return "n/a"
    return f"{mean(values):.2f}"


def generate(entries: list[dict[str, Any]]) -> str:
    result_counts = Counter(entry.get("audit_result", "unknown") for entry in entries)
    critical_failures = sum(1 for entry in entries if entry.get("critical_failure"))

    lines: list[str] = []
    lines.append("# SCR-001B Generated Sample Audit Report")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("Generated from Continuity Ledger example JSON entries.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Entries analyzed:** {len(entries)}")
    lines.append(f"- **Passing entries:** {result_counts.get('pass', 0)}")
    lines.append(f"- **Critical failures:** {critical_failures}")
    lines.append("")
    lines.append("## Batteries Represented")
    lines.append("")
    lines.append("| Source File | Battery | Probe | Result | Critical Failure |")
    lines.append("|---|---|---:|---|---|")
    for entry in entries:
        lines.append(
            "| {source} | {battery} | {probe} | {result} | {critical} |".format(
                source=entry.get("_source_file", ""),
                battery=entry.get("battery", ""),
                probe=entry.get("probe_id", ""),
                result=entry.get("audit_result", ""),
                critical="Yes" if entry.get("critical_failure") else "No",
            )
        )

    lines.append("")
    lines.append("## Average Scores")
    lines.append("")
    lines.append("| Metric | Average |")
    lines.append("|---|---:|")
    for key, label in SCORE_LABELS.items():
        values = [entry.get("scores", {}).get(key) for entry in entries]
        numeric_values = [value for value in values if isinstance(value, int)]
        lines.append(f"| {label} | {fmt_average(numeric_values)} |")

    lines.append("")
    lines.append("## Drift Markers")
    lines.append("")
    drift_counts: Counter[str] = Counter()
    for entry in entries:
        drift_counts.update(entry.get("drift_markers", []))
    if drift_counts:
        lines.append("| Drift Marker | Count |")
        lines.append("|---|---:|")
        for marker, count in sorted(drift_counts.items()):
            lines.append(f"| {marker} | {count} |")
    else:
        lines.append("No drift markers recorded.")

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "This generated report demonstrates that Continuity Ledger entries can move from structured JSON records into human-readable audit summaries."
    )
    lines.append("")
    lines.append(
        "The sample entries are demonstration records, not a final evaluation of Sarah AI or any deployed system."
    )
    lines.append("")
    lines.append("## Reproduce")
    lines.append("")
    lines.append("```bash")
    lines.append("python scripts/check_examples.py")
    lines.append("python scripts/generate_sample_report.py")
    lines.append("cat reports/SCR-001B_generated_sample_audit_report.md")
    lines.append("```")
    lines.append("")
    lines.append("## Audit Law")
    lines.append("")
    lines.append("A system that cannot be tested cannot be trusted.")
    lines.append("")
    lines.append("A system that cannot refuse cannot guard.")
    lines.append("")
    lines.append("A system that cannot preserve sovereignty cannot serve life.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    entries = load_entries()
    if not entries:
        raise SystemExit("No example entries found.")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(generate(entries), encoding="utf-8")
    print(f"PASS: wrote {REPORT_PATH.relative_to(ROOT)} from {len(entries)} example entries")


if __name__ == "__main__":
    main()
