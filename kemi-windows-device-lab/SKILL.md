---
name: kemi-windows-device-lab
description: Connect to a trusted LAN Windows test machine and perform D-drive-only source sync, native Release builds, Authenticode or hardware-token signing, installation, debugging, compatibility and performance tests, log collection, and closed-loop fixes. Use for KEMI Windows 真机编译、Windows 签名、远程调试、安装验收 or clean-machine compatibility; do not use for cloud-only CI or Android device work.
---

# KEMI Windows Device Lab

Use the Windows machine as a complete build, simulation, installation, and UI-validation node. The outcome is an evidence-backed Release candidate or a precise blocker, not merely a successful SSH command or compiler exit code.

## Load the applicable instructions

1. Read [references/node-security.md](references/node-security.md) before connecting, provisioning, transferring files, or changing the remote machine.
2. Read [references/build-test-loop.md](references/build-test-loop.md) before syncing source, building, installing, testing, or reporting results.
3. Read [references/authenticode-signing.md](references/authenticode-signing.md) before signing a Windows release, using iTrus/SafeNet, or automating `signtool.exe`.
   Use [scripts/Invoke-KemiAuthenticode.ps1](scripts/Invoke-KemiAuthenticode.ps1) for certificate-context inspection, deterministic thumbprint-selected signing, and fail-closed verification. Do not rewrite the signing command ad hoc.
4. In the target repository, search for `AGENTS.md` and Windows-specific docs/scripts. For KEMI OFFICE, prefer:
   - `docs/engineering/WINDOWS_LAN_DEVICE_TEST_NODE_SETUP.md`
   - `docs/engineering/WINDOWS_LOCAL_RELEASE_BUILD.md`
   - `docs/engineering/WINDOWS_X64_SINGLE_SCREEN_BUILD.md`
   - `scripts/windows/` and `scripts/windows/remote/`
   For KEMI Send, also read [references/kemi-send-node.md](references/kemi-send-node.md) and the repository's
   `docs/WINDOWS-LAN-DEVICE-LAB.md` plus `docs/RELEASE-AND-DEPLOYMENT-RUNBOOK.md`.
5. Project instructions override generic examples in the references. Never assume an old IP address, username, workspace, certificate, or version remains current.

## Working rules

- Resolve the host from current project documentation or user-provided data. Verify reachability and the recorded SSH host fingerprint before authentication. Never disable host-key checking to make a connection work.
- Use public-key authentication. Do not place passwords or private keys in scripts, logs, reports, or the remote workspace.
- Keep every KEMI-controlled component on the Windows `D:` drive: source, toolchains, SDKs, caches, TEMP/TMP, packages, test files, logs, screenshots, traces, dumps, and installed test copies. Abort if `D:` is unavailable.
- Do not run two builds against the same worktree/build directory. Resolve active PIDs/process groups before starting or stopping a build.
- Prefer the Windows node's local incremental build and existing verified cache. Use cloud CI only when the local toolchain genuinely cannot produce the target or the user requests cloud CI.
- Build Release unless the user explicitly asks for Debug diagnostics. Debug output cannot be promoted as a release artifact.
- Preserve unrelated remote files and dirty work. Use a versioned/commit-specific workspace and explicit target paths. Ask before uninstalling user software, deleting material data, or changing OS security settings.
- SSH is Session 0 and cannot prove interactive desktop UI behavior. Use the project's allowlisted desktop agent or a scheduled interactive task tied to the logged-in desktop account. Never report CLI conversion as UI acceptance.
- A certificate visible to iTrus/SafeNet in the logged-in desktop account may be absent from the SSH account's certificate store. Check the session and `Cert:\CurrentUser\My` before choosing automation. Never copy, log, guess, or embed a token PIN.
- Signing is an interactive-security-context operation unless the project explicitly proves that an approved software key is available to Session 0. SSH may stage, hash, and verify files, but `INTERACTIVE_SIGNING_REQUIRED` is a routing result, not a certificate failure. Do not repeatedly retry SignTool from SSH.
- A build change must be followed by the applicable tests. If a test fails, diagnose from logs, make an in-scope fix, rebuild incrementally, and rerun the same failing test plus the regression matrix.

## Required loop

1. Inventory the Mac/controller, Windows OS/build/CPU/RAM/GPU/display/DPI/free `D:` space, current user/session, SSH fingerprint, PowerShell, compiler, SDK, cache, and active builds.
2. Verify or prepare the fixed D-drive directory contract without installing arbitrary tools to `C:`.
3. Resolve the exact Git commit/submodules/patch sequence and sync reproducibly. Confirm source identity on both machines.
4. Run static source, dependency, decoder ownership, installer, and configuration gates before the expensive build.
5. Build the minimal valid target incrementally; collect start/end time, exit code, cache statistics, compiler errors, and artifact identity.
6. Stage a self-contained product and installer. Sign staged inner PE files first, build the final installer or portable EXE from those signed bytes, then sign and verify the exact outer `.exe` that will be uploaded. An inner signature never substitutes for the installer's outer signature. Verify versions, architecture, dependencies, signatures, exact bytes, and SHA-256.
7. Install into an isolated D-drive test location, then launch, close, relaunch, and confirm no developer PATH or third-party installation is required.
8. Run compatibility, malformed/protected-input, file association, drag/drop, return-home, exit, PDF/OCR, updater, and uninstall checks required by the project.
9. Run interactive UI and performance tests only on an idle logged-in desktop. Record cold and warm runs separately; capture screenshots/logs/traces and reject contaminated samples.
10. Compare against the previous accepted build using the same machine, files, display settings, and measurement definitions. Do not trade rendering correctness or layout for a faster number.
11. Copy the final accepted artifact and report to the project-prescribed location. Update release notes only after the final matrix passes.

## Completion boundary

Report separately:

- connection/node readiness;
- source identity and build result;
- self-contained packaging and signing;
- automated compatibility/algorithm tests;
- interactive desktop tests;
- cold/warm performance and regression comparison;
- installer/self-update lifecycle;
- remaining limitations.

Do not say “真机测试通过” when only SSH, compilation, headless conversion, or one document passed. If a desktop agent is offline, label UI checks `interactive_required` rather than passing or silently skipping them.


## Required debugging closeout

After debugging, clean up this task's own local and remote scene. First preserve the required evidence and record its location; inspect exact paths, process ownership and current use before removing anything. Clean only confirmed disposable temporary scripts, transfer duplicates, unused diagnostic copies and reproducible build/cache outputs created by this task. Close only its own debug processes and connections. Do not stop shared interfaces, coworkers' sessions or active builds.

Preserve source changes, credentials, authorization state, user data, the installed app, required crash evidence and rollback packages until their retention purpose is satisfied. Never upload a dump or user data merely to permit cleanup. Existing deletion authorization does not waive target checks or mandatory tool confirmations.

Verify the app and previously working services remain available after closeout. Report what was removed, reclaimed space when measured, and what remains with its reason and retention condition. If debugging is ongoing, identify the artifacts still needed rather than claiming cleanup complete.

For an app that crashes before its simulator starts, read [the remote-desktop startup-crash case](references/windows-startup-crash-388-20261003.md). It contains the actual reproduction, rollback, local dump analysis, controlled runtime recovery, lifecycle evidence and mandatory packaging prevention; do not treat it as a verified repair until its final evidence is added.

远程命令、日志读取或资源耗尽排查前，读[58提交内存事故与命令预算](references/windows-resource-exhaustion-58-20261006.md)，避免PowerShell5.1对象深度序列化和只在返回后截断。资源保护的部署及验收范围须以实际版本证明。

远程桌面确认和输入无响应时，读[目标核验与焦点恢复](references/remote-confirmation-focus-20261006.md)，在已有授权内完成普通确认，并保留平台拒绝、PIN及身份变化边界。
