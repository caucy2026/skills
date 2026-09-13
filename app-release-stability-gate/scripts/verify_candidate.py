#!/usr/bin/env python3
"""Verify artifact bytes and optional Git source revision against a frozen plan."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    errors: list[str] = []
    checked = []
    for item in plan.get("platforms", []):
        path = Path(item.get("artifact_path", ""))
        if not path.is_absolute() or not path.is_file():
            errors.append(f"artifact missing: {path}")
            continue
        actual = {"bytes": path.stat().st_size, "sha256": sha256(path)}
        if actual["bytes"] != item.get("bytes") or actual["sha256"] != item.get("sha256"):
            errors.append(f"artifact drift: {path}")
        checked.append({"path": str(path), **actual})
    source_root = plan.get("source_root")
    source_revision = plan.get("source_revision")
    if source_root and source_revision:
        root = Path(source_root)
        if not root.is_absolute() or not root.exists():
            errors.append(f"source root missing: {source_root}")
        else:
            head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True, check=False)
            if head.returncode != 0 or head.stdout.strip() != source_revision:
                errors.append("source_revision drift")
    report = {"valid": not errors, "artifacts": checked, "source_revision": source_revision, "errors": errors}
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
