#!/usr/bin/env python3
"""Publish only fixed KEMI Send resources to Newlink Common."""

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
ORDER = ["KEMI-SEND-ANDROID", "KEMI-SEND-MACOS", "KEMI-SEND-WINDOWS", "KEMI-SEND-LINUX"]
ARGUMENTS = {
    "KEMI-SEND-ANDROID": "android",
    "KEMI-SEND-MACOS": "macos",
    "KEMI-SEND-WINDOWS": "windows",
    "KEMI-SEND-LINUX": "linux",
}


def digest(path: Path, algorithm: str) -> str:
    value = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def request_json(opener, url: str, payload: dict | None = None) -> dict:
    body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode()
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, headers=headers)
    with opener.open(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def password_for(username: str) -> str:
    value = os.environ.get("NEWLINK_COMMON_PASSWORD", "")
    if value:
        return value
    if sys.platform == "darwin":
        result = subprocess.run(
            ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-a", username, "-w"],
            text=True, capture_output=True, check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    if not sys.stdin.isatty():
        raise RuntimeError("No Common credential available")
    return getpass.getpass("Common后台密码（输入不显示）: ")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    for argument in ARGUMENTS.values():
        parser.add_argument(f"--{argument}", type=Path)
    parser.add_argument("--username", default=os.environ.get("NEWLINK_COMMON_USERNAME", "common"))
    parser.add_argument("--work-dir", type=Path, required=True, help="Repository-local temporary directory")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verify-download", action="store_true")
    args = parser.parse_args()

    root = Path.cwd().resolve()
    work_dir = args.work_dir.resolve()
    if root not in work_dir.parents:
        raise RuntimeError("--work-dir must be inside the current repository")
    resources = json.loads((Path(__file__).resolve().parents[1] / "references" / "resources.json").read_text(encoding="utf-8"))

    files: dict[str, tuple[Path, str, str]] = {}
    for name in ORDER:
        path = getattr(args, ARGUMENTS[name])
        if path is None:
            continue
        path = path.resolve()
        if root not in path.parents or not path.is_file():
            raise RuntimeError(f"Artifact must be a repository-local file: {path}")
        files[name] = (path, digest(path, "md5"), digest(path, "sha256"))
        print(f"plan={name}\tid={resources[name]}\tfile={path}\tsize={path.stat().st_size}\tmd5={files[name][1]}\tsha256={files[name][2]}")
    if not files:
        raise RuntimeError("No KEMI Send artifacts selected")
    if args.dry_run:
        print(f"KEMI_SEND_COMMON_DRY_RUN=PASS\tversion={args.version}\titems={len(files)}")
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
    token = config.get("uploadToken") or ""
    domain = (config.get("domain") or "").rstrip("/")
    if config.get("code") != 0 or config.get("fileSaveWay") != "qiniu" or not token or not domain.startswith("https://cdn.newlink-sz.com"):
        raise RuntimeError("Backend is not using the audited qiniu upload mode")

    work_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="kemi-send-common-", dir=work_dir) as temp_name:
        temp = Path(temp_name)
        for index, name in enumerate([item for item in ORDER if item in files], start=1):
            response = request_json(opener, BASE + "/web/configPlug/findOne", {"data": {"_id": resources[name]}})
            record = response.get("data") or {}
            if response.get("code") != 0 or record.get("name") != name or record.get("projectCode") != "Common":
                raise RuntimeError(f"Resource identity mismatch for {name}; refusing mutation")

            path, local_md5, local_sha256 = files[name]
            remote_name = f"upgradefile{int(time.time() * 1000) + index}_{path.name}"
            remote_key = f"Common/{remote_name}"
            output = temp / f"qiniu-{index}.json"
            subprocess.run([
                "curl", "-fsS", "--retry", "5", "--retry-delay", "2", "-X", "POST", "https://upload-z2.qiniup.com",
                "-F", f"token={token}", "-F", f"key={remote_key}", "-F", f"file=@{path}", "-o", str(output),
            ], check=True)
            result = json.loads(output.read_text(encoding="utf-8"))
            if result.get("key") != remote_key:
                raise RuntimeError(f"CDN upload failed for {name}")

            public_url = f"{domain}/{remote_key}"
            record.update({"version": args.version, "fileName": remote_name, "url": public_url, "md5": local_md5})
            record.pop("file", None)
            update = request_json(opener, BASE + "/web/configPlug/uploadPlug", record)
            if update.get("code") != 0:
                raise RuntimeError(f"Backend update failed for {name}: {update.get('msg', 'unknown error')}")

            public = None
            for _ in range(30):
                query = urllib.parse.urlencode({"projectName": "Common", "name": name, "_t": int(time.time())})
                candidates = request_json(opener, PUBLIC + "?" + query).get("data") or []
                public = next((item for item in candidates if item.get("name") == name), None)
                if public and public.get("version") == args.version and public.get("md5") == local_md5:
                    break
                time.sleep(1)
            else:
                raise RuntimeError(f"Public metadata did not converge for {name}")

            if args.verify_download:
                target = temp / f"download-{index}"
                urllib.request.urlretrieve(public["url"], target)
                if digest(target, "md5") != local_md5 or digest(target, "sha256") != local_sha256:
                    raise RuntimeError(f"Downloaded bytes do not match local file for {name}")
            print(f"verified={name}\tversion={args.version}\tmd5={local_md5}\tsha256={local_sha256}\turl={public['url']}")

    print(f"KEMI_SEND_COMMON_RELEASE=PASS\tversion={args.version}\titems={len(files)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, urllib.error.URLError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"KEMI_SEND_COMMON_RELEASE=FAIL\t{error}", file=sys.stderr)
        raise SystemExit(1)
