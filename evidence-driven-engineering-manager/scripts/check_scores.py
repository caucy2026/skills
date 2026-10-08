#!/usr/bin/env python3
"""Check review roster and arithmetic; cannot certify evidence truth."""
import argparse
import json
from pathlib import Path

WEIGHTS = {"requirements": 35, "output": 25, "closure": 20,
           "efficiency": 10, "boundaries": 10}


def check(data):
    errors = []
    members = data.get("members", [])
    exempt = data.get("exempt", {})
    if not isinstance(members, list) or not all(isinstance(x, str) for x in members):
        return ["members must be a list of names"]
    if len(set(members)) != len(members) or "Manager" in members:
        errors.append("duplicate members or Manager included in member roster")
    if not isinstance(exempt, dict) or any(not isinstance(v, str) or not v.strip() for v in exempt.values()):
        return errors + ["exempt must map member names to nonempty reasons"]
    if set(exempt) - set(members):
        errors.append("exemption outside member roster")
    expected = (set(members) - set(exempt)) | {"Manager"}
    seen = set()
    if not data.get("window"):
        errors.append("missing review window")
    rows = data.get("assessments", [])
    if not isinstance(rows, list):
        return errors + ["assessments must be a list"]
    for row in rows:
        if not isinstance(row, dict):
            errors.append("assessment must be an object")
            continue
        name = row.get("member")
        if not isinstance(name, str):
            errors.append("missing member name")
            continue
        if name in seen:
            errors.append(f"{name}: duplicate assessment")
        seen.add(name)
        if row.get("status") == "incomplete":
            errors.append(f"{name}: incomplete evidence; do not rank or treat as completed review")
            continue
        parts = row.get("components", {})
        if not isinstance(parts, dict) or set(parts) != set(WEIGHTS):
            errors.append(f"{name}: all five components required")
            continue
        valid = all(type(parts[k]) is int and 0 <= parts[k] <= cap for k, cap in WEIGHTS.items())
        if not valid:
            errors.append(f"{name}: component out of range")
            continue
        score = row.get("score")
        if type(score) is not int or score != sum(parts.values()):
            errors.append(f"{name}: total does not equal component sum")
        evidence = row.get("evidence")
        if not isinstance(evidence, list) or not evidence or any(not isinstance(x, str) or not x.strip() for x in evidence):
            errors.append(f"{name}: evidence references required")
        if not isinstance(row.get("deductions"), str) or not row["deductions"].strip():
            errors.append(f"{name}: deduction explanation required (or justified none)")
        if type(score) is int and score < 60:
            negative = row.get("negative_evidence_types", [])
            if not isinstance(negative, list) or not all(isinstance(x, str) and x.strip() for x in negative) or len(set(negative)) < 2:
                errors.append(f"{name}: low rating needs two independent negative evidence types")
    if seen != expected:
        errors.append(f"roster mismatch: missing={sorted(expected-seen)}, extra={sorted(seen-expected)}")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.review.read_text())
        failures = check(data) if isinstance(data, dict) else ["review must be an object"]
    except (ValueError, OSError) as exc:
        failures = [str(exc)]
    print(json.dumps({"valid": not failures, "errors": failures,
                      "scope": "structure and arithmetic only; human evidence review still required"}, ensure_ascii=False))
    raise SystemExit(bool(failures))
