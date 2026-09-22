# KEMI传书发布证据清单

Read this reference before validating or publishing a release.

## Shared evidence

- Git commit and clean/known worktree state
- version name and integer build/version code
- absolute artifact path, modification time, exact bytes, SHA-256, and format integrity
- build toolchain and target architecture
- real start time, PID, window/process evidence, crash result, and a short idle CPU/RSS sample
- release report path and rollback artifact/version

Do not reuse a check after the artifact bytes change. A matching path or filename is insufficient.

## Android/PAD

- `org.kemi.send`, expected version name/code, ARM64 target when required
- approved project certificate fingerprint and APK v2/v3 verification
- install/update succeeds on the designated PAD and the installed package stays running
- KEMI's embedded shared-desktop Activity/native libraries exist when that feature is shipped; no second remote-control APK is installed or launched as a substitute

## macOS

- final ZIP was recreated after stapling using `COPYFILE_DISABLE=1 ditto --norsrc --noextattr`
- archive listing contains no `._*` and no `__MACOSX/`
- ordinary `/usr/bin/unzip` extraction succeeds inside the repository
- exactly one top-level `KEMI传书.app`; nested helpers are allowed
- bundle ID `org.kemi.send`, expected version/build, and supported minimum macOS
- main executable and required native helpers contain both `x86_64` and `arm64` when Universal is promised
- `codesign --verify --deep --strict`, `stapler validate`, and `spctl --assess --type execute` pass in a full host context
- notarization submission is `Accepted`; Gatekeeper reports `Notarized Developer ID`
- exact final ZIP starts with a real window; the CDN-downloaded copy also passes ordinary first-open and remains running

An archive that works only when extracted with `ditto` fails this gate.

## Windows

- archive/installer integrity, expected x64 binaries and version
- Authenticode result matches the current runbook and release policy; never call an unsigned binary signed
- install and launch on the configured clean Windows test device
- application window/process, basic feature smoke test, self-update result, CPU/RSS, and uninstall/rollback evidence as applicable

## Linux

- expected x86-64 format/version and archive integrity
- required dynamic dependencies are present on the approved Linux runner
- application stays running in a real or documented headless smoke environment

## Common post-publication

For only the requested `KEMI-SEND-*` resources, verify record ID/name/project, version, MD5, public URL, downloaded MD5, and downloaded SHA-256. List all unselected KEMI Send platforms as unchanged.

## KEMI market post-publication

For each `(package_name=org.kemi.send, os_type)` record, verify uniqueness, app ID, version, exact byte fields, SHA-256, HTTPS URL, enabled `探索` category, unfiltered storefront visibility, real download/install, old-version `has_update=true`, current-version `has_update=false`, and intended force-update policy. Remove all authentication and upload-token files after verification.
