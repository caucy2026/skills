---
name: kemi-send-common-release
description: Publish or update only the four KEMI Send client packages in the Newlink Common cloud. Use for KEMI传书/KEMI Send Common releases; never use it for KEMI远程办公 resources.
---

# KEMI Send Common Release

Publish only these exact Common resources:

- `KEMI-SEND-ANDROID`
- `KEMI-SEND-MACOS`
- `KEMI-SEND-WINDOWS`
- `KEMI-SEND-LINUX`

This skill is separate from `newlink-common-release`. Never update `KEMI-PAD`, `KEMI-macOS`, `KEMI-Windows`, `KEMI-Linux`, `SHA256SUMS`, or `release-manifest`; those belong to KEMI远程办公.

## Required workflow

1. Work in the KEMI Send repository and read its `docs/RELEASE-AND-DEPLOYMENT-RUNBOOK.md` completely before building, packaging, or publishing.
2. Confirm the current `app/pubspec.yaml` version and build number. Do not publish mixed builds under one release.
3. Keep all build, extraction, download, and verification files inside the repository (normally `bin/release/` and `.tools/`).
4. Validate each selected artifact before mutation:
   - Android: release APK, expected application ID/version, approved certificate, and APK signature schemes.
   - macOS: final ZIP extracts cleanly; in a full macOS security context, Developer ID signature, notarization ticket, Gatekeeper, supported architectures, and minimum OS all pass.
   - Windows: archive integrity, expected version/architecture, clean-machine launch test, and the signing requirement stated by the repository runbook.
   - Linux: archive integrity, expected ELF architecture/version, and a Linux launch/smoke test. Build it on the approved Linux runner rather than substituting an older package.
5. Run `scripts/publish_kemi_send_common.py` first with `--dry-run`. Review the four exact resource names, IDs, file paths, sizes, MD5, and SHA-256.
6. Obtain explicit authorization immediately before live upload. A prior request to prepare or inspect a release is not authorization to mutate Common.
7. Run the publisher without `--dry-run` and with `--verify-download`. Partial platform updates are allowed only when the user explicitly requests them; unselected resources remain unchanged.
8. Report each updated resource's version, MD5, SHA-256, and public CDN URL. Explicitly list platforms left unchanged and any unmet formal-release gate.

The publisher logs in with `NEWLINK_COMMON_PASSWORD` or macOS Keychain service `KEMI Newlink Common Publisher`; never print or persist the password. It checks each fixed record ID, exact resource name, and `projectCode=Common` before upload, then waits for public metadata convergence and optionally downloads the published bytes for digest comparison.

