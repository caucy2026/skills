# Platform automation adapters

Choose only adapters needed by the product. Prefer the repository's existing framework and stable semantic selectors.

## Android

- Inspect: `apkanalyzer`, `aapt2`, `apksigner`; freeze package/version/signature/SDK/ABI.
- Drive: AndroidX instrumentation/Espresso for source-aware UI, UIAutomator for system UI, Maestro or Appium for black-box flows, ADB for lifecycle and device state.
- Observe: logcat, DropBox, tombstones/ANR where authorized, `dumpsys meminfo`, CPU/process stats, gfxinfo/frame timeline, batterystats and thermal state.
- Exercise clean install and `adb install -r` upgrade without clearing data. Use package-scoped Monkey with a fixed seed only after deterministic flows.

## Windows

- Inspect: Authenticode/SignTool, PE architecture/version, MSI/MSIX/AppInstaller identity and hashes.
- Drive: project tests plus WinAppDriver/Appium Windows, UI Automation/PowerShell, protocol/API tests and Windows Sandbox or a clean test VM.
- Observe: Windows Event Log, WER/crash dumps, application logs, process handles/threads/private bytes/working set/CPU, installer exit codes and service/task state.
- Test clean install, upgrade over the published version, repair/uninstall, launch/relaunch, service/user-session boundaries, sleep/wake and signed update behavior as applicable.

## macOS

- Inspect: `codesign`, `spctl`, `stapler`, bundle identifiers/versions, architectures and notarization ticket.
- Before any upgrade test or delivery, compare the currently installed production app and the exact candidate with `codesign -dv --verbose=4`, `codesign -dr -`, and extracted entitlements. Require the same bundle identifier, `TeamIdentifier`, Apple signing class, full designated requirement and permission-relevant entitlements. An ad-hoc signature has no stable team identity and is forbidden for an upgrade candidate even when it is a Release build. Quarantine the artifact and return `BLOCK` before installation if any identity field differs.
- Drive: XCTest/XCUITest, accessibility automation, CLI/API/protocol tests and clean user accounts or disposable machines.
- Observe: unified logs, crash/spin reports, process CPU/memory, energy diagnostics and application logs.
- Test first launch/Gatekeeper, upgrade preserving container/keychain/permissions, Dock reopen, window lifecycle, sleep/wake and helper/service identity where applicable. The upgrade case must install over the current production version without clearing or resetting TCC, then assert required permissions remain authorized and functional. A renewed Screen Recording, Accessibility, Input Monitoring or Automation prompt is a product failure, not a manual setup step. Record the installed and candidate designated requirements as evidence.

## iOS/iPadOS

- Inspect archive/export identity, entitlements, provisioning, bundle/version and architecture.
- Drive XCTest/XCUITest on real devices plus simulators for matrix breadth.
- Observe device logs, MetricKit/test metrics, crashes, hangs, memory warnings, launch and UI performance.
- Exercise install/update through the authorized distribution path; include permission revocation, background/foreground and state restoration.

## Linux and other desktop systems

- Inspect package manager metadata, signatures, dependencies, architectures and desktop/service entries.
- Drive project tests plus accessibility/UI automation appropriate to the desktop environment.
- Observe journal/core dumps, process CPU/RSS/FD/thread counts and service state.
- Test clean install, upgrade, uninstall, desktop integration, session/reboot behavior and package integrity.

## Shared services and protocols

Use deterministic API/protocol fixtures for authentication, reconnect, retries, cancellation, concurrency and backward compatibility. When two clients interact, freeze both endpoint versions and record evidence from both sides. UI success cannot substitute for protocol-state assertions.
