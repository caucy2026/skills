#!/usr/bin/env python3
"""Run implemented cases, preserve evidence, and safely resume an unchanged candidate."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def output_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence_exists(item: dict[str, Any]) -> bool:
    evidence = item.get("evidence", [])
    return bool(evidence) and all(Path(p).is_absolute() and Path(p).exists() for p in evidence)


def reusable(item: dict[str, Any]) -> bool:
    return item.get("status") == "pass" and item.get("product_status") == "pass" and item.get("evidence_status") == "pass" and item.get("environment_status") == "ready" and evidence_exists(item)


def read_envelope(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("adapter result envelope must be a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--case", action="append", dest="selected")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    plan_digest = digest(args.plan)
    args.evidence_dir.mkdir(parents=True, exist_ok=True)
    selected = set(args.selected or [])
    previous: dict[str, Any] = {}
    if args.resume and args.results.exists():
        old = json.loads(args.results.read_text(encoding="utf-8"))
        if old.get("plan_sha256") == plan_digest:
            previous = {x.get("id"): x for x in old.get("cases", []) if x.get("id")}
    results: list[dict[str, Any]] = []
    metrics: dict[str, Any] = {}
    for case in plan.get("cases", []):
        if selected and case.get("id") not in selected:
            continue
        ident = case.get("id", "missing-id")
        prior = previous.get(ident)
        if prior and reusable(prior):
            results.append({**prior, "resumed": True})
            metrics.update(prior.get("metrics", {}))
            continue
        automation = case.get("automation", {})
        started = now()
        status, reason, exit_code = "blocked", "automation not implemented", None
        product_status, evidence_status, environment_status = "blocked", "fail", "blocked"
        failure_class = "automation_missing"
        stdout_path = args.evidence_dir / f"{ident}.stdout.log"
        stderr_path = args.evidence_dir / f"{ident}.stderr.log"
        envelope_path = args.evidence_dir / f"{ident}.result.json"
        if envelope_path.exists():
            envelope_path.unlink()
        envelope: dict[str, Any] = {}
        if automation.get("status") == "implemented" and isinstance(automation.get("argv"), list):
            env = os.environ.copy()
            env["APP_RELEASE_CASE_ID"] = ident
            env["APP_RELEASE_CASE_RESULT"] = str(envelope_path.resolve())
            for key, value in automation.get("env", {}).items():
                if not isinstance(key, str) or not isinstance(value, str):
                    raise SystemExit(f"{ident}: automation env keys and values must be strings")
                env[key] = value
            try:
                completed = subprocess.run(automation["argv"], cwd=automation.get("cwd"), env=env, shell=False, text=True, capture_output=True, timeout=int(case.get("timeout_seconds", 300)), check=False)
                stdout_path.write_text(completed.stdout, encoding="utf-8")
                stderr_path.write_text(completed.stderr, encoding="utf-8")
                exit_code = completed.returncode
                envelope = read_envelope(envelope_path)
                if automation.get("result_protocol") == "app-release-case-result-v1" and not envelope:
                    raise ValueError("adapter did not write the required result envelope")
                fallback = {0: ("pass", "pass", "ready"), 3: ("blocked", "fail", "blocked"), 4: ("blocked", "fail", "blocked")}.get(completed.returncode, ("fail", "fail", "ready"))
                product_status = envelope.get("product_status", fallback[0])
                evidence_status = envelope.get("evidence_status", fallback[1])
                environment_status = envelope.get("environment_status", fallback[2])
                failure_class = envelope.get("failure_class", "none" if completed.returncode == 0 else "adapter_failure")
                dimensions_pass = product_status == "pass" and evidence_status == "pass" and environment_status == "ready"
                status = "pass" if completed.returncode == 0 and dimensions_pass else ("blocked" if environment_status == "blocked" else "fail")
                reason = envelope.get("reason") or ({0: "adapter passed", 3: "environment or external dependency unavailable", 4: "case intentionally not run"}.get(completed.returncode, f"exit code {completed.returncode}"))
            except (subprocess.TimeoutExpired, ValueError, json.JSONDecodeError) as exc:
                if isinstance(exc, subprocess.TimeoutExpired):
                    stdout_path.write_text(output_text(exc.stdout), encoding="utf-8")
                    stderr_path.write_text(output_text(exc.stderr), encoding="utf-8")
                    reason, failure_class = "timeout", "timeout"
                else:
                    stderr_path.write_text(str(exc), encoding="utf-8")
                    reason, failure_class = str(exc), "invalid_result_envelope"
                status, product_status, evidence_status, environment_status = "fail", "fail", "fail", "ready"
        evidence = [str(p.resolve()) for p in (stdout_path, stderr_path, envelope_path) if p.exists()]
        for value in envelope.get("evidence", []):
            p = Path(value)
            if p.is_absolute() and p.exists() and str(p) not in evidence:
                evidence.append(str(p))
        if status == "pass" and not evidence:
            status, evidence_status, reason, failure_class = "fail", "fail", "adapter passed without evidence", "evidence_missing"
        case_metrics = envelope.get("metrics", {}) if isinstance(envelope.get("metrics", {}), dict) else {}
        metrics.update(case_metrics)
        results.append({"id": ident, "required": case.get("required", True), "status": status, "product_status": product_status, "evidence_status": evidence_status, "environment_status": environment_status, "failure_class": failure_class, "reason": reason, "exit_code": exit_code, "started_at": started, "finished_at": now(), "attempt": int(prior.get("attempt", 0) if prior else 0) + 1, "evidence": evidence, "metrics": case_metrics, "resumed": False})
    artifacts = [{"platform": item.get("platform", item.get("name")), **{key: item.get(key) for key in ("product_id", "version", "build", "sha256")}} for item in plan.get("platforms", [])]
    status_by_id = {item["id"]: item["status"] for item in results}
    coverage = [{**item, "status": "covered" if item.get("case_ids") and all(status_by_id.get(case_id) == "pass" for case_id in item["case_ids"]) else "blocked"} for item in plan.get("coverage_contract", [])]
    output = {"schema_version": 2, "plan": str(args.plan.resolve()), "plan_sha256": plan_digest, "candidate": {"artifacts": artifacts, "source_revision": plan.get("source_revision"), "automation_revision": plan.get("automation_revision")}, "expected_candidate": {"artifacts": artifacts, "source_revision": plan.get("source_revision")}, "cases": results, "coverage": coverage, "thresholds": plan.get("thresholds", {}), "metrics": metrics}
    args.results.parent.mkdir(parents=True, exist_ok=True)
    args.results.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"results": str(args.results.resolve()), "passed": sum(x["status"] == "pass" for x in results), "failed": sum(x["status"] == "fail" for x in results), "blocked": sum(x["status"] == "blocked" for x in results), "resumed": sum(x.get("resumed", False) for x in results)}, ensure_ascii=False))
    return 0 if results and all(x["status"] == "pass" or not x["required"] for x in results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
