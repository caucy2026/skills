#!/usr/bin/env python3
"""Execute implemented test cases without invoking a shell and preserve raw evidence."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
from pathlib import Path


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def output_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--case", action="append", dest="selected")
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    args.evidence_dir.mkdir(parents=True, exist_ok=True)
    selected = set(args.selected or [])
    results = []
    for case in plan.get("cases", []):
        if selected and case.get("id") not in selected:
            continue
        ident = case.get("id", "missing-id")
        automation = case.get("automation", {})
        started = now()
        status = "blocked"
        reason = "automation not implemented"
        exit_code = None
        stdout_path = args.evidence_dir / f"{ident}.stdout.log"
        stderr_path = args.evidence_dir / f"{ident}.stderr.log"
        if automation.get("status") == "implemented" and isinstance(automation.get("argv"), list):
            env = os.environ.copy()
            for key, value in automation.get("env", {}).items():
                if not isinstance(key, str) or not isinstance(value, str):
                    raise SystemExit(f"{ident}: automation env keys and values must be strings")
                env[key] = value
            try:
                completed = subprocess.run(
                    automation["argv"],
                    cwd=automation.get("cwd"),
                    env=env,
                    shell=False,
                    text=True,
                    capture_output=True,
                    timeout=int(case.get("timeout_seconds", 300)),
                    check=False,
                )
                stdout_path.write_text(completed.stdout, encoding="utf-8")
                stderr_path.write_text(completed.stderr, encoding="utf-8")
                exit_code = completed.returncode
                status = {0: "pass", 3: "blocked", 4: "not_run"}.get(completed.returncode, "fail")
                reason = {0: "exit code 0", 3: "environment or external dependency unavailable", 4: "case intentionally not run"}.get(completed.returncode, f"exit code {completed.returncode}")
            except subprocess.TimeoutExpired as exc:
                stdout_path.write_text(output_text(exc.stdout), encoding="utf-8")
                stderr_path.write_text(output_text(exc.stderr), encoding="utf-8")
                status = "fail"
                reason = "timeout"
        evidence = [str(stdout_path.resolve()), str(stderr_path.resolve())] if stdout_path.exists() else []
        results.append({"id": ident, "required": case.get("required", True), "status": status, "reason": reason, "exit_code": exit_code, "started_at": started, "finished_at": now(), "evidence": evidence})
    artifacts = [{"platform": item.get("platform", item.get("name")), **{key: item.get(key) for key in ("product_id", "version", "build", "sha256")}} for item in plan.get("platforms", [])]
    status_by_id = {item["id"]: item["status"] for item in results}
    coverage = []
    for item in plan.get("coverage_contract", []):
        mapped = item.get("case_ids", [])
        coverage.append({**item, "status": "covered" if mapped and all(status_by_id.get(case_id) == "pass" for case_id in mapped) else "blocked"})
    output = {
        "schema_version": 1,
        "plan": str(args.plan.resolve()),
        "candidate": {"artifacts": artifacts, "source_revision": plan.get("source_revision"), "automation_revision": plan.get("automation_revision")},
        "expected_candidate": {"artifacts": artifacts, "source_revision": plan.get("source_revision")},
        "cases": results,
        "coverage": coverage,
        "thresholds": plan.get("thresholds", {}),
    }
    args.results.parent.mkdir(parents=True, exist_ok=True)
    args.results.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"results": str(args.results.resolve()), "passed": sum(x["status"] == "pass" for x in results), "failed": sum(x["status"] == "fail" for x in results), "blocked": sum(x["status"] == "blocked" for x in results)}, ensure_ascii=False))
    return 0 if results and all(x["status"] == "pass" or not x["required"] for x in results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
