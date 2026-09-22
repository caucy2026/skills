# KEMI Send Windows node profile

Read this reference only for KEMI Send Windows native builds and acceptance on the configured LAN node.

## Trusted node identity

- Host: `192.168.3.58`, port `22`, user `kemi-test`.
- Expected ED25519 host fingerprint: `SHA256:ikZ6NXAH3VFBGooSCeKW0JY9+h0cIcQOzib4fxmvz6M`.
- Controller identity: `/Users/newlink/.ssh/id_ed25519`; expected public-key fingerprint
  `SHA256:hpYI+CFcXcCgdLNnllblFfemUcT+SpAk5m8uwFYh+ww`.
- Remote root: `D:\KEMI-Test`.

Always rescan the public host key and compare its SHA-256 to the trusted value before login. Connect with
`BatchMode=yes`, `IdentitiesOnly=yes`, and `StrictHostKeyChecking=yes`. Use a task-local known-hosts file after the
comparison when the controller's default known-hosts file does not contain the node. Never disable host-key checking,
try passwords, or reuse an unrelated deployment key.

Prefer uploading a reviewed `.ps1` to `D:\KEMI-Test\work` and invoking it with `pwsh -NoProfile -File`. Nested
PowerShell in an SSH command is fragile: local-shell quoting can remove `$env:` assignments and corrupt paths with
spaces while the command still partially succeeds.

## Storage and toolchain facts

All KEMI-controlled source, tools, caches, TEMP/TMP, build output, test installations, logs, screenshots, traces, and
dumps stay under `D:\KEMI-Test`. Set `GIT_CONFIG_GLOBAL`, `PUB_CACHE`, `CARGO_HOME`, and `RUSTUP_HOME` to D-drive
paths per process; do not modify system-wide TEMP/TMP or Git configuration.

The 2026-09-04 baseline found:

- Windows 10 Home China 22H2 build 19045, zh-CN, Intel i7-10510U, 8 logical processors;
- PowerShell 7.6.5 and Windows SDK 10.0.26100.0;
- MSVC/MSBuild/CMake/Ninja under `D:\VSBuildTools`;
- Inno Setup under `D:\KEMI-Test\tools\inno-setup`;
- shared Flutter under `D:\tools\flutter`, but it was 3.47.0 and owned by Administrators;
- no Rust executable discovered in the KEMI D-drive tool roots;
- the node could not reach `github.com:443` during provisioning.

Treat these as discovery hints, not timeless facts. Recheck them each run. KEMI Send pins Flutter 3.41.9 in `.fvmrc`;
do not build a Release with the shared 3.47.0 SDK. Do not alter the shared SDK. Provision the pinned Windows SDK beside
it under `D:\KEMI-Test\tools`, or transfer a hash-verified archive from the controller when the node has no internet.
Likewise, keep Rust under the D-drive contract.

The 2026-09-04 initial Release build reached native MSBuild and proved that the existing Build Tools instance omitted ATL:
`flutter_secure_storage_windows_plugin.cpp` failed with C1083 for `atlstr.h`. Before building, verify
`D:\VSBuildTools\VC\Tools\MSVC\<version>\atlmfc\include\atlstr.h`. If absent, stop the build and have an administrator
add `Microsoft.VisualStudio.Component.VC.ATL` to the existing `D:\VSBuildTools` instance. The SSH account is a standard
user and must not claim that a silent installer succeeded; the acceptance check is the header's presence followed by a
zero-exit Release build. For KEMI Send itself, commit `25165abc9` removes this optional machine prerequisite by vendoring
upstream `flutter_secure_storage_windows` 3.1.2 and replacing only ATL string conversions with Win32 UTF-8 conversion
APIs. Do not install ATL or mutate Build Tools when building that commit or later. Preserve the first failure log and
perform only one incremental retry after the prerequisite or project fix is present.

Known-good pinned tool facts from that run were Flutter 3.41.9, Dart 3.11.5, engine
`42d3d75a56efe1a2e9902f52dc8006099c45d937`, and Rust/Cargo 1.98.1. The clean Flutter clone was kept at
`D:\KEMI-Test\tools\flutter-3.41.9-clean`. When the node cannot reach upstream storage, transfer official artifacts from
the controller only after recording byte count plus SHA-256, then recompute SHA-256 on Windows. Never treat a copied,
dirty Flutter SDK as a clean pinned checkout.

The ATL-free Release compiled successfully on the node. Its verified source archive SHA-256 was
`9d8385bc0560fc05555495d206600be41256e9ddc7ab7998e38860cfc6feb645`. It passed three Session-0 launch/terminate
cycles at the five-second probe (about 96–101 MB working set), five app-center updater catalog tests, and fourteen
download/clipboard/shared-desktop tests. These are build and headless compatibility evidence only, not interactive UI
or genuine old-version self-update acceptance.

The standard `kemi-test` account may be denied CIM/WMI and may not expose `quser` in PATH. Do not elevate merely for
inventory. Use ordinary-user-readable OS/registry/process data and mark unavailable GPU, RAM, display, DPI, or desktop
session evidence `interactive_required`.

## Source synchronization caveat

Use the exact controller commit and a versioned path such as `D:\KEMI-Test\source\kemi-send-<short-commit>`.
`packages/device_apps` and `packages/pasteboard_override` are ordinary tracked trees in the root commit. Build from the
committed contents; do not include unrelated untracked upstream README, example, or Gradle-wrapper files. Verify the
uploaded source archive hash on both sides and do not describe an opaque dirty working-tree copy as a clean checkout.

## Acceptance scope

Follow the repository runbook and `docs/WINDOWS-LAN-DEVICE-LAB.md`. Build x64 Release, stage a self-contained package,
install side by side on D, launch/close/relaunch, run app-specific compatibility and malformed-input checks, measure at
least three eligible cold and warm runs, and test self-update from a genuine older version plus current-version and
download-failure negatives.

SSH Session 0 cannot prove UI behavior. Use the project's allowlisted logged-in desktop agent when available; otherwise
report interactive checks as `interactive_required`. Only a candidate that passes the required matrix may be copied to
`bin/release` or passed to Common publishing.
