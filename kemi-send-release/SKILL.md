---
name: kemi-send-release
description: Build, sign/notarize, package, real-launch test, and publish KEMI传书 clients to Newlink Common and the KEMI application market. Use for KEMI Send release or hotfix work; never touch KEMI远程办公 resources.
---

# KEMI Send Release

Deliver a traceable KEMI传书 release, not merely a successful build or upload.

## Product boundary

- Work only on KEMI传书 / KEMI Send (`org.kemi.send`) and its repository.
- Common mutations are limited to `KEMI-SEND-ANDROID`, `KEMI-SEND-MACOS`, `KEMI-SEND-WINDOWS`, and `KEMI-SEND-LINUX`.
- Never modify `KEMI-PAD`, `KEMI-macOS`, `KEMI-Windows`, `KEMI-Linux`, `SHA256SUMS`, `release-manifest`, or any KEMI远程办公 application record.
- Keep source, SDK caches, build output, extraction directories, downloads, and verification evidence inside the KEMI Send repository. System compilers and security tools may be executed read-only; do not use system temporary directories for controlled build artifacts.

## Required workflow

1. Locate the repository, read its `AGENTS.md` and `docs/RELEASE-AND-DEPLOYMENT-RUNBOOK.md` completely, and inspect the live Git/build state before any mutation. If the runbook and live environment differ, update the runbook before continuing.
2. Define the requested platforms and release version. Keep the Flutter version/build number and any platform-specific version files consistent. Preserve unrelated worktree changes.
3. Build with the repository-pinned toolchain and project-local caches. Use the platform path mandated by the runbook; do not substitute an old package when a target cannot be built.
4. Validate the immutable artifact identity `(absolute path, byte count, SHA-256)` and every platform gate in [references/release-checklist.md](references/release-checklist.md).
5. For macOS, use the repository signing/notarization script and run `scripts/verify_macos_distribution.sh` in the full host security context. The final ZIP must be created after stapling and must contain no `._*` or `__MACOSX/` AppleDouble entries. Ordinary `unzip` extraction—not only `ditto`—is mandatory because AppleDouble materialization can invalidate an otherwise notarized app.
6. Before publication, start the exact final artifact or an ordinary-unzip copy. Confirm a real application window and a live process after a meaningful wait; a launch command returning successfully is not evidence. For a public macOS package, also download the CDN object, extract it normally, pass Gatekeeper's ordinary first-open flow, and confirm the downloaded App stays running.
7. Obtain explicit authorization immediately before external mutations. Publish Common through the installed `kemi-send-common-release` workflow and the KEMI market through `kemi-market-publish`. Query existing state first and update existing records; do not create duplicates or repeat an upload whose exact version and hash are already online.
8. Re-download every changed CDN object and compare byte count and SHA-256/MD5 with the immutable local artifact. Verify storefront visibility without a category filter, download/install availability, old-version positive update response, current-version negative update response, and `force_update=false` unless explicitly required.
9. Record non-secret evidence in the repository release notes: commit, version, platforms, artifact identity, signing/notarization, real launch, Common resource IDs/URLs, market app IDs/URLs, update checks, unchanged platforms, and blockers. Remove password, bearer-token, upload-token, and temporary authenticated-session files.
10. Commit only the intended source and documentation files. Push only when the user authorizes the exact remote/branch and the environment permits it. Never claim Git backup, publication, signing, or launch completion unless its observable check passed.

## macOS damaged-app gate

The packaging command must suppress resource forks and extended attributes:

```bash
COPYFILE_DISABLE=1 ditto --norsrc --noextattr -c -k --keepParent "KEMI传书.app" package.zip
```

After both the notary ZIP and final ZIP are produced, enumerate the complete archive without an early-exit `grep -q`. Under `set -o pipefail`, `grep -q` can make `unzip` terminate with SIGPIPE and hide a real match. Reject the archive if any AppleDouble entry exists.

Run trust checks on the macOS host. If the sandbox cannot access the login keychain or rejects known-good signed applications, classify that as an invalid test environment and rerun the unchanged artifact on the host; do not rebuild or resign based on a sandbox false negative.

## Completion

Use “正式发布完成” only when build, signature where required, notarization where required, exact final archive, ordinary extraction, real launch, Common/store metadata, CDN byte equality, update behavior, release report, and credential cleanup all pass. Otherwise state completed facts and the precise remaining blocker separately.
