#!/usr/bin/env python3
"""Fail-closed evaluator for cross-platform application release results."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ZERO_METRICS = ("new_crashes", "new_hangs", "new_native_dumps", "new_ooms", "process_restarts")


def artifact_key(item: dict[str, Any]) -> tuple[Any, ...]:
    return item.get("platform"), item.get("product_id"), item.get("version"), item.get("build"), item.get("sha256")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("results", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.results.read_text(encoding="utf-8"))
    blockers: list[str] = []
    candidate = data.get("candidate", {})
    expected = data.get("expected_candidate", {})
    if expected.get("source_revision") and candidate.get("source_revision") != expected.get("source_revision"):
        blockers.append("source_revision mismatch")
    actual_artifacts = {artifact_key(x) for x in candidate.get("artifacts", [])}
    expected_artifacts = {artifact_key(x) for x in expected.get("artifacts", [])}
    if not expected_artifacts:
        blockers.append("expected artifact identity missing")
    elif actual_artifacts != expected_artifacts:
        blockers.append("candidate artifact identity set mismatch")
    if not candidate.get("automation_revision"):
        blockers.append("automation_revision missing")
    cases = data.get("cases", [])
    if not cases:
        blockers.append("no test case results")
    for item in cases:
        ident = item.get("id", "<missing-id>")
        if item.get("required", True) and item.get("product_status") != "pass":
            blockers.append(f"required case {ident} product_status is {item.get('product_status', 'missing')}")
        if item.get("required", True) and item.get("evidence_status") != "pass":
            blockers.append(f"required case {ident} evidence_status is {item.get('evidence_status', 'missing')}")
        if item.get("required", True) and item.get("environment_status") != "ready":
            blockers.append(f"required case {ident} environment_status is {item.get('environment_status', 'missing')}")
        if item.get("required", True) and item.get("status") != "pass":
            blockers.append(f"required case {ident} is {item.get('status', 'missing')}")
        if item.get("required", True) and item.get("status") == "pass":
            evidence = item.get("evidence", [])
            if not evidence:
                blockers.append(f"required case {ident} has no evidence")
            for evidence_path in evidence:
                p = Path(evidence_path)
                if not p.is_absolute() or not p.exists():
                    blockers.append(f"case {ident} evidence missing: {evidence_path}")
    coverage = data.get("coverage", [])
    if not coverage:
        blockers.append("coverage ledger missing")
    for item in coverage:
        if item.get("priority") in ("P0", "P1") and item.get("status") != "covered":
            blockers.append(f"{item.get('kind', 'coverage')} {item.get('id', '<missing-id>')} is {item.get('status', 'missing')}")
    metrics = data.get("metrics", {})
    thresholds = {"idle_cpu_percent": 5, "memory_growth_mib": 50, "memory_growth_percent": 20, **data.get("thresholds", {})}
    for name in ZERO_METRICS:
        if name not in metrics:
            blockers.append(f"metric {name} missing")
        elif metrics[name] != 0:
            blockers.append(f"metric {name} must be 0, got {metrics[name]}")
    for name in ("idle_cpu_percent", "memory_growth_mib", "memory_growth_percent"):
        if name not in metrics:
            blockers.append(f"metric {name} missing")
        elif metrics[name] > thresholds[name]:
            blockers.append(f"metric {name}={metrics[name]} exceeds {thresholds[name]}")
    report = {"decision": "PASS" if not blockers else "BLOCK", "candidate": candidate, "required_cases": sum(1 for c in cases if c.get("required", True)), "passed_required_cases": sum(1 for c in cases if c.get("required", True) and c.get("status") == "pass"), "blockers": blockers}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not blockers else 2


if __name__ == "__main__":
    raise SystemExit(main())
