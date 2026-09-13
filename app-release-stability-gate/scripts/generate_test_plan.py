#!/usr/bin/env python3
"""Generate a stable cross-platform application release test plan."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


DEFAULT_THRESHOLDS = {
    "idle_cpu_percent": 5,
    "memory_growth_mib": 50,
    "memory_growth_percent": 20,
    "soak_minutes": 60,
    "exploration_events": 10000,
    "seed": 154241,
}


def slug(value: str) -> str:
    text = "".join(ch if ch.isalnum() else "-" for ch in value.upper())
    return "-".join(p for p in text.split("-") if p)


def make_case(case_id: str, title: str, group: str, priority: str = "P1", **extra: Any) -> dict[str, Any]:
    result = {
        "id": case_id,
        "title": title,
        "group": group,
        "priority": priority,
        "required": True,
        "platforms": [],
        "preconditions": [],
        "test_data": [],
        "steps": [],
        "assertions": [],
        "forbidden": [],
        "cleanup": [],
        "evidence_requirements": ["timestamped command output", "candidate identity"],
        "timeout_seconds": 300,
        "retry_policy": "diagnostic-only; first failure remains a failure",
        "automation": {"status": "needs_implementation"},
    }
    result.update(extra)
    return result


BASE_GATE_DETAILS = {
    "IDENTITY": (["compute bytes and SHA-256", "read platform identity, version, architecture and trust metadata"], ["all values equal the frozen candidate record", "required signature or trust policy passes"]),
    "CLEAN-INSTALL": (["prepare an isolated clean target", "install the frozen artifact", "launch once and collect platform logs"], ["installation succeeds from the frozen bytes", "first launch reaches the expected ready state", "no new crash, hang or permission loop occurs"]),
    "STARTUP": (["measure cold launch", "close normally", "measure warm relaunch"], ["cold and warm launches reach ready state within the case timeout", "close releases the expected process state", "relaunch does not create duplicate application instances"]),
    "UPGRADE": (["install the supplied prior stable artifact", "capture identity, settings and permission state", "upgrade with the frozen candidate", "relaunch and compare preserved state"], ["the candidate version replaces the prior version", "identity, user data, settings and compatible permission grants are preserved", "no update loop occurs"]),
    "LIFECYCLE": (["launch the app", "exercise background, foreground, close and relaunch transitions", "simulate an owned process termination and recover"], ["each transition reaches one deterministic state", "recovery creates no duplicate process or stale session"]),
    "NETWORK": (["establish a controlled session", "remove network connectivity", "restore connectivity", "observe bounded reconnect behavior"], ["offline state is reported", "exactly one usable session recovers within timeout", "retry activity is bounded"]),
    "PERMISSIONS": (["exercise denied permission state", "grant the permission through the platform flow", "revoke it and retry"], ["denial is controlled and actionable", "grant enables only the intended capability", "revocation does not crash or corrupt state"]),
    "RESOURCES": (["stabilize the app in the declared state", "sample CPU, memory, threads, handles and process identity", "repeat the core loop and sample again"], ["resource samples belong to the frozen candidate and declared state", "configured CPU and memory limits are met", "no unexplained restart or monotonic leak occurs"]),
    "SOAK": (["run the deterministic core flow for the configured duration", "continuously collect crashes, hangs and resource samples"], ["the full duration completes", "all iterations pass", "no crash, hang, OOM, restart or resource-limit violation occurs"]),
    "EXPLORE": (["run bounded model exploration using the recorded seed and event budget", "preserve every action and discovered state"], ["the event budget completes or a reproducible defect is recorded", "all reached states satisfy safety and lifecycle invariants"]),
}


def platform_gate_case(case_id: str, title: str, group: str, gate: str, platform: str, priority: str = "P1", **extra: Any) -> dict[str, Any]:
    steps, assertions = BASE_GATE_DETAILS[gate]
    return make_case(case_id, title, group, priority, platforms=[platform], steps=steps, assertions=assertions,
                     forbidden=["candidate identity drift", "unexplained crash, hang, data loss or duplicate process"],
                     cleanup=["restore changed network, permission and application state", "preserve evidence"],
                     evidence_requirements=["timestamped command output", "candidate identity", "platform logs and state assertions"], **extra)


def read_profile(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in ("product", "platforms"):
        if not data.get(key):
            raise SystemExit(f"missing required profile field: {key}")
    if not isinstance(data["platforms"], list):
        raise SystemExit("platforms must be a list")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    profile = read_profile(args.profile)
    thresholds = {**DEFAULT_THRESHOLDS, **profile.get("thresholds", {})}
    platform_records = []
    cases: list[dict[str, Any]] = []
    coverage: list[dict[str, Any]] = []
    platform_names = set()
    for platform in profile["platforms"]:
        for key in ("name", "artifact_path", "product_id", "version", "build"):
            if platform.get(key) in (None, ""):
                raise SystemExit(f"platform missing required field: {key}")
        name = str(platform["name"]).lower()
        if name in platform_names:
            raise SystemExit(f"duplicate platform: {name}")
        platform_names.add(name)
        artifact = Path(platform["artifact_path"])
        if not artifact.is_absolute() or not artifact.is_file():
            raise SystemExit(f"artifact_path must be an existing absolute file: {artifact}")
        digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
        platform_records.append({**platform, "name": name, "artifact_path": str(artifact), "bytes": artifact.stat().st_size, "sha256": digest})
        p = slug(name)
        common = [
            platform_gate_case(f"G0-{p}-IDENTITY", f"Verify {name} artifact identity, version and trust", "integrity", "IDENTITY", name, "P0"),
            platform_gate_case(f"G1-{p}-CLEAN-INSTALL", f"Clean install and first launch on {name}", "install", "CLEAN-INSTALL", name, "P0"),
            platform_gate_case(f"G1-{p}-STARTUP", f"Cold/warm start, close and relaunch on {name}", "startup", "STARTUP", name, "P0"),
            platform_gate_case(f"G1-{p}-UPGRADE", f"Upgrade published build on {name} without data loss", "upgrade", "UPGRADE", name, "P0", required=bool(platform.get("prior_stable_artifact"))),
            platform_gate_case(f"G4-{p}-LIFECYCLE", f"Lifecycle, process death and recovery on {name}", "resilience", "LIFECYCLE", name),
            platform_gate_case(f"G4-{p}-NETWORK", f"Offline, restore, reconnect and retry on {name}", "resilience", "NETWORK", name),
            platform_gate_case(f"G4-{p}-PERMISSIONS", f"Permission denial, revocation and regrant on {name}", "resilience", "PERMISSIONS", name),
            platform_gate_case(f"G5-{p}-RESOURCES", f"CPU, memory, handles/threads and restart stability on {name}", "resources", "RESOURCES", name, "P0"),
            platform_gate_case(f"G6-{p}-SOAK", f"Core-flow soak for {thresholds['soak_minutes']} minutes on {name}", "endurance", "SOAK", name, "P0"),
            platform_gate_case(f"G6-{p}-EXPLORE", f"Bounded exploration with seed {thresholds['seed']} on {name}", "exploration", "EXPLORE", name, seed=thresholds["seed"], events=thresholds["exploration_events"]),
        ]
        cases.extend(common)
    for group_name, source_key, prefix, kind in (("function", "features", "F", "feature"), ("historical-regression", "historical_bugs", "R", "historical_bug"), ("change-impact", "change_risks", "C", "change_risk")):
        for item in profile.get(source_key, []):
            item_id = str(item.get("id", "")).strip()
            if not item_id:
                raise SystemExit(f"every {source_key} item requires id")
            targets = [str(x).lower() for x in item.get("platforms", sorted(platform_names))]
            unknown = sorted(set(targets) - platform_names)
            if unknown:
                raise SystemExit(f"{item_id} references unknown platforms: {unknown}")
            generated_ids = []
            for target in targets:
                cid = f"{prefix}-{slug(item_id)}-{slug(target)}"
                cases.append(make_case(cid, item.get("title", item.get("name", item_id)), group_name, item.get("priority", "P0" if kind == "historical_bug" else "P1"), platforms=[target], family=item.get("family"), preconditions=item.get("preconditions", []), test_data=item.get("test_data", []), steps=item.get("steps", []), assertions=item.get("assertions", []), forbidden=item.get("forbidden", []), cleanup=item.get("cleanup", []), evidence_requirements=item.get("evidence_requirements", ["timestamped command output", "candidate identity"])))
                generated_ids.append(cid)
            coverage.append({"id": item_id, "kind": kind, "priority": item.get("priority", "P0" if kind == "historical_bug" else "P1"), "platforms": targets, "case_ids": generated_ids})
    plan = {"schema_version": 1, "product": profile["product"], "source_root": profile.get("source_root"), "source_revision": profile.get("source_revision"), "platforms": platform_records, "thresholds": thresholds, "cases": cases, "coverage_contract": coverage}
    canonical = json.dumps(plan, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    plan["automation_revision"] = profile.get("automation_revision") or f"generated-plan:{hashlib.sha256(canonical).hexdigest()}"
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "test-plan.json"
    md_path = args.output_dir / "test-plan.md"
    json_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [f"# {profile['product']} release test plan", "", "| ID | Priority | Group | Platform | Required | Title |", "|---|---|---|---|---:|---|"]
    lines += [f"| {c['id']} | {c['priority']} | {c['group']} | {','.join(c.get('platforms', []))} | {'yes' if c['required'] else 'no'} | {c['title']} |" for c in cases]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"plan": str(json_path.resolve()), "summary": str(md_path.resolve()), "cases": len(cases), "platforms": len(platform_records)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
