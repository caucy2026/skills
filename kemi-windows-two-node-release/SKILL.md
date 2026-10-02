---
name: kemi-windows-two-node-release
description: Build a KEMI Windows release on one VibeKits-simulated Windows machine, mount its artifact on a second simulated Windows signing machine without copying between them, sign inner and outer binaries with a hardware token, validate both machines, and publish from a Mac. Use for two-node Windows build/sign/release requests; not for a single-node build or unrelated stores.
---

# KEMI Windows two-node release

This skill joins three authorized roles: the Mac controls VibeKits simulation and publishes; Windows A builds; Windows B signs with its hardware token. It is a release gate, not a claim that successful compilation or a SignTool exit makes an app usable. Read [the verified 2026-09-24 procedure](references/rustdesk-2026-09-24.md) for the concrete RustDesk/KEMI Remote Office commands, paths, known failures, and restore sequence. For another product, retain the topology and gates but use that product's source, packaging, identity, and installer documentation.

## First use and document check

On first use in a task, locate this skill at `~/.codex/skills/kemi-windows-two-node-release/SKILL.md`, read this entrypoint and the linked case reference, then check its format with:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/kemi-windows-two-node-release
```

Run the same check after editing this skill. The validator requires Python's `PyYAML` module (`import yaml`); if it reports `ModuleNotFoundError: yaml`, check the active interpreter and install PyYAML into that interpreter's user environment, then rerun. Do not treat a missing validator dependency as a failed Windows build, and do not modify the project's Mac/Windows build environment to satisfy this documentation check.

## Required companion skills

Before touching a device, read `vibekits-remote-simulator` and its tool contract. Before a Windows build or run test, read `kemi-windows-device-lab` and the repository's `AGENTS.md`/Windows build instructions. Before signing, read `kemi-windows-remote-signing` including `references/workflow.md`; use its fixed GUI EXE → CMD → PowerShell → `Invoke-KemiAuthenticode.ps1` chain. Before uploading, read `kemi-market-publish`, `references/release-contract.md`, `references/signing-certification-closure.md`, and the current official market docs. The current user's explicit choice of a C: build directory on Windows A overrides the device-lab D: convention only for that machine and task.

## Route and boundaries

1. Connect to both user-authorized device IDs through VibeKits `simulator.connect`; compare each ID, host, user, transport, and SSH fingerprint against trusted node records. An ID alone is not permission to accept a changed host key. Do not use RustDesk remote-desktop UI to substitute for simulator tools.
2. Freeze the source commit, submodules, required patches, version name/code, output format, package identity, and destination store record before building. Build the full self-contained Release on Windows A. Do not combine newly built Flutter AOT data with an older executable or DLL directory.
   Transfer a frozen source snapshot or Git bundle from the Mac to a versioned source directory on A; verify the commit and required files there before compiling. Windows compilation must use A's toolchain and caches. Do not run Flutter/Xcode, `flutter pub get`, or dependency bootstrap in the Mac's shared source tree as a side effect of preparing the Windows release; these commands can rewrite generated Mac build state used by another worker.
3. Expose only the versioned output directory from A over a local-only file service. If B cannot reach A directly, create a host-key-verified, temporary **A → B reverse SSH forward** so B accesses A's loopback file service at B's own loopback address. Mount that remote tree on B. Verify a source hash from A equals the hash through the mount on B before signing. No build artifacts are copied from A to B.
4. Sign all required inner `.exe`/`.dll` on B **through the mounted path** in the active desktop session. The token PIN is entered only by the human on B; never handle or store it. Require a fresh `PASS` report, exact file count, intended embedded certificate, timestamp, SignTool verification, and post-sign hashes. Recheck at A that the physical files changed to those signed hashes.
5. Package the signed inner tree on A. Sign the resulting **outer** EXE/MSI on B through the same mount in a distinct versioned run. Require a second full `PASS`. Freeze final bytes and SHA-256 on A and B; they must match. An inner signature cannot stand in for the outer signature.
6. Test the exact final signed package on A and B. Confirm extraction/install yields the expected complete file set, main binary hash/version/signature, and an actual running process from the new path. Inspect crash and application logs. Existing installed instances can steal launch/IPC; preserve and restore them for an isolated test. A PID without a visible or otherwise verified UI does not prove UI acceptance. Compare with a known-good app using the same simulator mechanism before assigning blame to the new build.
7. Only after the product's required runtime gates pass, publish from the Mac to the existing KEMI market record. Use the official upload-token/complete flow or documented browser fallback, not a second app record. Verify final CDN bytes/hash, public detail with both exact size fields, unfiltered Windows list, old-code positive and current-code negative update checks, and actual storefront download/install. Never report “正式发布完成” before these checks.
8. Restore original user installations, services, and foreground state on both Windows nodes. Remove the temporary mount, reverse forward, file server, and access key only after no active signing/build/test depends on them. Keep versioned release evidence and the final signed artifact.

## Important failure decisions

- Remote SSH/PowerShell runs in Session 0. A successful SSH command cannot show a token PIN dialog. Launch signing via `vibekits.device.app_control` in Session 1, visually check the PIN window, and track the same run to its final report.
- If Windows execution policy blocks the fixed `.ps1` when called with `-File`, use the existing proven CMD wrapper that runs a UTF-16LE `-EncodedCommand` which loads the exact fixed script as a scriptblock. Do not change the machine's execution policy.
- If Cargo reports OS error 4551 for a generated `build-script-build.exe` or proc-macro DLL, first read the same-time `Microsoft-Windows-CodeIntegrity/Operational` 3033/3077 events and the exact Cargo log. This happened in both +310 and +315; it is distinct from the signing script execution-policy issue above. Follow the bounded evidence and retry procedure in [the 2026-09-25 case addendum](references/rustdesk-2026-09-24.md#2026-09-25-addendum-310-vs-315-build-recovery); do not change WDAC/Smart App Control, relocate build output to evade it, or claim a timed retry is guaranteed.
- Before Flutter Windows compilation, verify the versioned source tree contains both `flutter/lib/generated_bridge.dart` and `flutter/lib/generated_bridge.freezed.dart`, plus the generated plugin registrant and project-local junctions when needed. A missing ignored Freezed file can make `EventToUI_Rgba` / `EventToUI_Texture` look like source defects; use the same addendum to verify bridge-source identity before restoring generated output.
- If Flutter plugins fail because symlinks require Developer Mode, use verified **project-local** directory junctions for plugin paths; do not change global Developer Mode or retry a rejected elevation.
- Visual Studio `vcvars64.bat` may replace `VCPKG_ROOT`; set the intended vcpkg root **after** calling it, and use `set "NAME=value"` to avoid trailing spaces.
- Do not upload when signed bytes are correct but the expected GUI or full install has not been demonstrated. Record the precise pending gate and continue diagnosing; signature validity alone is insufficient.

For explicitly authorized signing of blocked compiler helper EXEs/proc-macro DLLs, read the 2026-09-27 addendum in [the case reference](references/rustdesk-2026-09-24.md). The +369 case verified both helper signatures and a successful retry of the original build; retain those same gates for each new run and do not confuse compiler-helper signing with final-product signing.
