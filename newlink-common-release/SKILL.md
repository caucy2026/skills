---
name: newlink-common-release
description: Publish or update the six fixed KEMI client resources in the Newlink Common cloud, including single-platform hotfixes, manifest-last ordering, and public version/MD5 verification. Use for www.newlinksz.cn Common client releases; do not use for the separate KEMI application market.
---

# Newlink Common Release

Use the deterministic background publisher in `scripts/publish_common.py`. Do not automate the web form unless the official API flow is unavailable.

Before publishing, read [references/release-contract.md](references/release-contract.md). It defines the six fixed resources, safe ordering, hotfix scope, and completion gate.

## Choose a mode

Use the fast path when the requested release files are already staged and verified, the exact Common upload is authorized in the current request, and the Keychain credential is available. This is the normal KEMI hotfix/re-release path and should normally finish without opening or focusing a browser.

Use the audited path for a first release, suspicious/stale artifacts, changed signing inputs, previous partial failure, or when the user explicitly asks for full CDN byte verification.

## Fast path (target: one minute after artifacts are ready)

1. Read [references/release-contract.md](references/release-contract.md) and identify full release vs platform hotfix.
2. Confirm the formal artifact gate is already recorded. For macOS this means fixed internal bundle name, Developer ID signature, Apple notarization/stapling, Gatekeeper acceptance, and launch of the exact extracted ZIP.
3. Check the Keychain item without printing the secret:

```bash
security find-generic-password -a common -s 'KEMI Newlink Common Publisher' >/dev/null 2>&1
```

4. If the current request authorizes these exact files and destination, run the publisher once. It computes and prints every file's size, MD5 and SHA-256 before login or upload, validates resource identity, forces manifest last, and verifies public version/MD5 after each update. Do not run a redundant separate dry-run in this mode.

```bash
python3 scripts/publish_common.py --version <version> --release-dir /Users/newlink/kemi/RustDesk/BIN/release --items KEMI-macOS,SHA256SUMS,release-manifest --username common
```

For a full six-resource release, omit `--items`. For a PAD, Windows, Linux, or macOS hotfix, select only that binary plus `SHA256SUMS,release-manifest` in that order. The script normalizes the final ordering.

5. Report completion only on `COMMON_RELEASE=PASS`. Include the exact version and verified public MD5 values.

If the Keychain item is missing, stop before upload and open one visible terminal prompt to save it. Never switch to repeated browser automation. Credential storage and the external upload remain separate authorizations.

## Audited path

1. Inspect the local release directory and determine whether this is a full six-file release or a platform hotfix.
2. Run `--dry-run` first. Confirm the requested version, selected resources, file paths, sizes, and MD5 values.
3. Obtain explicit authorization immediately before the external upload if the current user request has not already authorized these exact files and destination.
4. Run the publisher with `--verify-download`. It uses the backend's official login/config/upload/update APIs, re-downloads CDN bytes, and does not open or focus Chrome.
5. Report success only when every selected public `plugData` endpoint returns the requested version and the same MD5 as the local file.

Examples:

```bash
python3 scripts/publish_common.py --version 1.4.113 --release-dir /Users/newlink/kemi/RustDesk/BIN/release --items KEMI-macOS,SHA256SUMS,release-manifest --dry-run
python3 scripts/publish_common.py --version 1.4.113 --release-dir /Users/newlink/kemi/RustDesk/BIN/release --items KEMI-macOS,SHA256SUMS,release-manifest --verify-download
```

For a full release, omit `--items`; all six resources are selected and `release-manifest` is forced last.

Credentials are never stored in the skill or repository. The publisher uses `NEWLINK_COMMON_PASSWORD`, then the macOS Keychain service `KEMI Newlink Common Publisher`, then an interactive hidden prompt. Saving a credential to Keychain requires separate explicit user authorization. Once saved, reuse the Keychain item and do not ask the user to log in again unless authentication actually fails.

If the script stops, do not advance the manifest manually. Preserve the already published binaries, diagnose the exact failed item, and resume only after reconciling local and public metadata.
