#!/usr/bin/env python3
"""Publish fixed KEMI client resources to the Newlink Common cloud."""

from __future__ import annotations

import argparse
import getpass
import hashlib
import http.cookiejar
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://www.newlinksz.cn/screensaver"
PUBLIC = BASE + "/api/plugData"
KEYCHAIN_SERVICE = "KEMI Newlink Common Publisher"
DEFAULT_ORDER = [
    "KEMI-PAD",
    "KEMI-macOS",
    "KEMI-Windows",
    "KEMI-Linux",
    "SHA256SUMS",
    "release-manifest",
]


def digest(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def request_json(opener, url: str, payload: dict | None = None) -> dict:
    body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode()
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, headers=headers)
    with opener.open(request, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def password_for(username: str) -> str:
    value = os.environ.get("NEWLINK_COMMON_PASSWORD", "")
    if value:
        return value
    if sys.platform == "darwin":
        result = subprocess.run(
            ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-a", username, "-w"],
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    if not sys.stdin.isatty():
        raise RuntimeError(
            "No credential available. Set NEWLINK_COMMON_PASSWORD or authorize a Keychain profile."
        )
    return getpass.getpass("Common后台密码（输入不显示）: ")


def qiniu_upload(token: str, key: str, path: Path, output: Path) -> dict:
    command = [
        "curl", "-fsS", "--retry", "5", "--retry-delay", "2", "-X", "POST",
        "https://upload-z2.qiniup.com",
        "-F", f"token={token}",
        "-F", f"key={key}",
        "-F", f"file=@{path}",
        "-o", str(output),
    ]
    subprocess.run(command, check=True)
    return load_json(output)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--release-dir", type=Path, required=True)
    parser.add_argument("--items", help="Comma-separated resource names; default is all six")
    parser.add_argument("--username", default=os.environ.get("NEWLINK_COMMON_USERNAME", "common"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verify-download", action="store_true")
    args = parser.parse_args()

    resources = load_json(Path(__file__).resolve().parents[1] / "references" / "resources.json")
    selected = DEFAULT_ORDER if not args.items else [x.strip() for x in args.items.split(",") if x.strip()]
    unknown = sorted(set(selected) - set(resources))
    if unknown:
        raise RuntimeError(f"Unknown resources: {', '.join(unknown)}")
    selected = [name for name in DEFAULT_ORDER if name in selected]
    if "release-manifest" in selected:
        selected = [name for name in selected if name != "release-manifest"] + ["release-manifest"]

    files = {}
    print(f"version={args.version}")
    for name in selected:
        path = (args.release_dir / resources[name]["filename"]).resolve()
        if not path.is_file():
            raise RuntimeError(f"Missing release file: {path}")
        md5 = digest(path, "md5")
        sha256 = digest(path, "sha256")
        files[name] = (path, md5, sha256)
        print(f"plan={name}\tfile={path}\tsize={path.stat().st_size}\tmd5={md5}\tsha256={sha256}")
    if args.dry_run:
        print("DRY_RUN=PASS")
        return 0

    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    password = password_for(args.username)
    try:
        login = request_json(opener, BASE + "/web/user/loginIn", {"name": args.username, "pwd": password})
    finally:
        password = ""
    if login.get("code") != 0:
        raise RuntimeError(f"Login failed: {login.get('msg', 'unknown error')}")

    config = request_json(opener, BASE + "/config/getWebConfig")
    if config.get("code") != 0 or config.get("fileSaveWay") != "qiniu":
        raise RuntimeError("Backend is not using the audited qiniu upload mode")
    token = config.get("uploadToken") or ""
    domain = (config.get("domain") or "").rstrip("/")
    if not token or not domain.startswith("https://cdn.newlink-sz.com"):
        raise RuntimeError("Invalid upload token or CDN domain")

    with tempfile.TemporaryDirectory(prefix="newlink-common-release-") as temp_name:
        temp = Path(temp_name)
        for index, name in enumerate(selected, start=1):
            record_id = resources[name]["id"]
            record_response = request_json(opener, BASE + "/web/configPlug/findOne", {"data": {"_id": record_id}})
            record = record_response.get("data") or {}
            if record_response.get("code") != 0 or record.get("name") != name or record.get("projectCode") != "Common":
                raise RuntimeError(f"Resource identity mismatch for {name}")

            path, local_md5, local_sha256 = files[name]
            remote_name = f"upgradefile{int(time.time() * 1000) + index}_{path.name}"
            remote_key = f"Common/{remote_name}"
            remote_url = f"{domain}/{remote_key}"
            print(f"uploading={name}\tversion={args.version}\tsize={path.stat().st_size}")
            result = qiniu_upload(token, remote_key, path, temp / f"qiniu-{index}.json")
            if result.get("key") != remote_key:
                raise RuntimeError(f"CDN upload failed for {name}")

            record.update({"version": args.version, "fileName": remote_name, "url": remote_url, "md5": local_md5})
            record.pop("file", None)
            update = request_json(opener, BASE + "/web/configPlug/uploadPlug", record)
            if update.get("code") != 0:
                raise RuntimeError(f"Backend update failed for {name}: {update.get('msg', 'unknown error')}")

            public = None
            for _ in range(20):
                query = urllib.parse.urlencode({"projectName": "Common", "name": name, "_t": int(time.time())})
                public_response = request_json(opener, PUBLIC + "?" + query)
                data = public_response.get("data") or []
                public = data[0] if data else None
                if public and public.get("version") == args.version and public.get("md5") == local_md5:
                    break
                time.sleep(1)
            else:
                raise RuntimeError(f"Public metadata did not converge for {name}")
            public_url = public.get("url", "")
            if not public_url.startswith("https://cdn.newlink-sz.com/Common/"):
                raise RuntimeError(f"Unexpected public URL for {name}: {public_url}")

            if args.verify_download:
                target = temp / f"download-{index}"
                urllib.request.urlretrieve(public_url, target)
                if digest(target, "md5") != local_md5 or digest(target, "sha256") != local_sha256:
                    raise RuntimeError(f"Downloaded bytes do not match local file for {name}")
            print(f"verified={name}\tversion={args.version}\tmd5={local_md5}\turl={public_url}")

    print(f"COMMON_RELEASE=PASS\tversion={args.version}\titems={len(selected)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, urllib.error.URLError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"COMMON_RELEASE=FAIL\t{error}", file=sys.stderr)
        raise SystemExit(1)
