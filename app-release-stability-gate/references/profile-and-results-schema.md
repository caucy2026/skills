# Profile and results contract

## Product profile

`scripts/generate_test_plan.py` accepts JSON:

```json
{
  "product": "Example",
  "source_root": "/absolute/source/path",
  "source_revision": "git-commit",
  "platforms": [
    {"name": "android", "artifact_path": "/absolute/app.apk", "product_id": "com.example.app", "version": "1.2.3", "build": 123, "prior_stable_artifact": "/absolute/app-122.apk", "required_environments": ["real-device-android12"]},
    {"name": "windows", "artifact_path": "/absolute/app.exe", "product_id": "Example.App", "version": "1.2.3", "build": 123, "required_environments": ["windows11-x64-clean"]}
  ],
  "features": [{"id": "connect", "name": "Connect to a device", "priority": "P0", "platforms": ["android", "windows"], "preconditions": ["test peer online"], "steps": ["select peer", "connect"], "assertions": ["session reaches connected state"], "forbidden": ["duplicate connection process"]}],
  "historical_bugs": [{"id": "BUG-123", "family": "reconnect", "title": "Reconnect loop after network recovery", "priority": "P0", "platforms": ["android"], "preconditions": ["active session"], "steps": ["disable network", "restore network"], "assertions": ["session reconnects once"], "forbidden": ["repeated warnings"]}],
  "change_risks": [{"id": "CHANGE-1", "title": "Shared connection lifecycle changed", "priority": "P0", "platforms": ["android", "windows"], "steps": ["connect", "disconnect", "reconnect"], "assertions": ["one clean lifecycle"]}],
  "thresholds": {"idle_cpu_percent": 5, "memory_growth_mib": 50, "memory_growth_percent": 20, "soak_minutes": 60, "exploration_events": 10000, "seed": 154241},
  "delivery": {"enabled": true, "release_skill": "project-release-skill", "destinations": [{"name": "internal-market", "verify_customer_path": true}]}
}
```

Every path must be absolute. Secrets are forbidden; refer to environment or secret-store key names.

The generator deliberately marks each case as `automation.status=needs_implementation`. The agent must expand it into a detailed case and an executable record before running:

```json
{
  "id": "R-BUG-123-ANDROID",
  "preconditions": ["fixture peer online", "session connected"],
  "test_data": ["peer alias from KEMI_TEST_PEER"],
  "steps": ["disable test-device network", "wait for disconnected state", "restore network"],
  "assertions": ["exactly one session reaches connected within 30 seconds"],
  "forbidden": ["duplicate client process", "repeating warning more than once"],
  "cleanup": ["restore network", "disconnect fixture session"],
  "evidence_requirements": ["client log slice", "peer log slice", "process samples"],
  "timeout_seconds": 90,
  "retry_policy": "diagnostic-only; first failure remains a failure",
  "precondition_stabilization": {"required": true, "stable_reads": 2, "timeout_seconds": 30},
  "outcome_contract": {"product": "assertions and forbidden outcomes", "evidence": "complete trace tied to candidate", "environment": "declared fixture is ready"},
  "automation": {
    "status": "implemented",
    "argv": ["python3", "/absolute/tests/reconnect.py"],
    "cwd": "/absolute/source/path",
    "result_protocol": "app-release-case-result-v1",
    "test_proof": {"positive": "pass", "negative_control": "fail", "restored": "pass"}
  }
}
```

Run `validate_test_plan.py --require-executable` before `run_test_manifest.py`. The runner never invokes a shell; each command is an argument array. Test programs retrieve permitted secrets from the environment or secret store themselves and must not print them.

The runner sets `APP_RELEASE_CASE_RESULT` to an absolute JSON path. An adapter may write this result envelope:

```json
{"protocol":"app-release-case-result-v1","product_status":"pass","evidence_status":"pass","environment_status":"ready","failure_class":"none","reason":"destination received exact key edges","evidence":["/absolute/events.json"]}
```

Allowed dimensions are `product_status: pass|fail|blocked`, `evidence_status: pass|fail`, and `environment_status: ready|blocked`. Preserve every attempt. A retry may replace incomplete evidence after state restoration; it cannot erase a complete product failure.

## Execution results

`scripts/evaluate_release_gate.py` accepts JSON:

```json
{
  "candidate": {"artifacts": [{"platform": "android", "sha256": "hex", "product_id": "com.example.app", "version": "1.2.3", "build": 123}], "source_revision": "git-commit", "automation_revision": "git-commit"},
  "expected_candidate": {"artifacts": [{"platform": "android", "sha256": "hex", "product_id": "com.example.app", "version": "1.2.3", "build": 123}], "source_revision": "git-commit"},
  "cases": [{"id": "G1-ANDROID-CLEAN-INSTALL", "required": true, "status": "pass", "product_status":"pass", "evidence_status":"pass", "environment_status":"ready", "evidence": ["/absolute/log.txt"]}],
  "coverage": [{"id": "connect", "kind": "feature", "priority": "P0", "status": "covered", "case_ids": ["F-CONNECT-ANDROID"]}],
  "metrics": {"new_crashes": 0, "new_hangs": 0, "new_native_dumps": 0, "new_ooms": 0, "process_restarts": 0, "idle_cpu_percent": 2.1, "memory_growth_mib": 8.2, "memory_growth_percent": 4.4},
  "thresholds": {"idle_cpu_percent": 5, "memory_growth_mib": 50, "memory_growth_percent": 20}
}
```

Allowed case statuses: `pass`, `fail`, `blocked`, `not_run`. Allowed coverage statuses: `covered`, `blocked`, `not_automatable`, `unknown`. Evidence for a required passing case must contain at least one existing absolute path.
