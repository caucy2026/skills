#!/usr/bin/env python3
"""Validate completeness and executable status of a generated release test plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = (
    "id", "title", "group", "priority", "required", "platforms",
    "preconditions", "test_data", "steps", "assertions", "forbidden",
    "cleanup", "evidence_requirements", "timeout_seconds", "retry_policy", "automation",
    "precondition_stabilization", "outcome_contract",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--require-executable", action="store_true")
    args = parser.parse_args()
    data = json.loads(args.plan.read_text(encoding="utf-8"))
    errors = []
    seen = set()
    cases = data.get("cases", [])
    delivery = data.get("delivery", {})
    if not isinstance(delivery, dict) or not isinstance(delivery.get("destinations", []), list):
        errors.append("delivery must be an object with a destinations array")
    if delivery.get("enabled") and not delivery.get("destinations"):
        errors.append("delivery is enabled but has no destinations")
    if not cases:
        errors.append("plan has no cases")
    for index, case in enumerate(cases):
        ident = case.get("id", f"index-{index}")
        missing = [field for field in REQUIRED_FIELDS if field not in case]
        if missing:
            errors.append(f"{ident}: missing fields {','.join(missing)}")
        if ident in seen:
            errors.append(f"{ident}: duplicate id")
        seen.add(ident)
        if case.get("required", True) and case.get("priority") in ("P0", "P1"):
            for field in ("steps", "assertions", "evidence_requirements"):
                if not case.get(field):
                    errors.append(f"{ident}: required {field} is empty")
        automation = case.get("automation", {})
        contract = case.get("outcome_contract", {})
        if not all(contract.get(key) for key in ("product_status", "evidence_status", "environment_status")):
            errors.append(f"{ident}: outcome_contract is incomplete")
        if args.require_executable and case.get("required", True):
            if automation.get("status") != "implemented":
                errors.append(f"{ident}: automation is not implemented")
            argv = automation.get("argv")
            if not isinstance(argv, list) or not argv or not all(isinstance(x, str) and x for x in argv):
                errors.append(f"{ident}: automation.argv must be a non-empty string array")
            cwd = automation.get("cwd")
            if not isinstance(cwd, str) or not Path(cwd).is_absolute():
                errors.append(f"{ident}: automation.cwd must be absolute")
            proof = automation.get("test_proof", {})
            if proof.get("positive") != "pass" or proof.get("negative_control") != "fail" or proof.get("restored") != "pass":
                errors.append(f"{ident}: positive/negative/restored test proof incomplete")
    report = {"valid": not errors, "cases": len(cases), "errors": errors}
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
