# Platform Adapters

Detect the target platform first. Use platform-native paths and lifecycle controls; do not translate commands mechanically between operating systems.

## Windows

- Use PowerShell with literal paths for filesystem operations.
- On registered build nodes, keep source, SDKs, package caches, temp, build output, APKs and logs on `D:`.
- Validate OpenSSH effective configuration, Windows account state, `authorized_keys` path/owner/ACL, firewall profile, and `sshd` service when diagnosing SSH.
- Never recursively delete or move a computed target before resolving and confirming it is within the intended D-drive work root.
- For the registered `.58` node, read [windows-58.md](windows-58.md).

## macOS

- Detect Apple Silicon versus Intel and whether a Universal binary is required.
- Use a configured non-system data/work volume for repository, Flutter/pub caches, temporary data and build output when the task has a non-system-volume requirement.
- Treat Keychain, Local Network permission, app sandbox entitlements, Hardened Runtime, Developer ID signing, notarization, stapling and Gatekeeper as distinct gates.
- LMCP listeners need network client/server entitlements; serial work needs the serial entitlement. Multiple discovery apps must coexist through socket address/port reuse.
- Validate the exact candidate `.app`, its embedded Harness/Node/ADB/Git/7-Zip runtimes, architectures and minimum OS. A Debug launch or `node --version` is not a Release/Harness acceptance result.
- Read the bundled [macOS platform specification](specs/11_MACOS_PLATFORM_SPEC.md), [feature parity](specs/54_MACOS_RECENT_WINDOWS_FEATURE_PARITY.md), and [self-contained acceptance](specs/56_MACOS_SELF_CONTAINED_HARNESS_ACCEPTANCE_2026-08-31.md) when relevant.

## Linux

- Detect distribution, init system, package/runtime availability, architecture, display/session type and container boundaries.
- Use POSIX permissions, an explicitly configured non-root work volume, and user services where possible; do not assume systemd, `/home`, `sudo`, X11, or root access without checking.
- For SSH, verify host keys, selected identities, file modes/ownership and effective daemon configuration. For LAN discovery, verify multicast route/interface and firewall without broadening beyond the private LAN.
- Linux support remains unverified until the requested build/runtime and LMCP behaviors pass on a real Linux target. Do not infer it from macOS POSIX similarity.

## Android

- Treat the ADB serial as target identity and lock every command to the selected serial. Never act on an implicit first device when multiple devices exist.
- Detect local ADB versus an authenticated RustDesk/VibeKits ADB tunnel. A tunnel endpoint is loopback plus a leased port, not a remote device identity.
- For install/launch/stress work, independently observe package state, foreground activity/process, crash/ANR, logcat, storage, temperature and serial telemetry when available.
- Clean install means uninstall/delete as specified, install the exact APK hash, launch the intended activity, verify readiness, then clean up according to the test contract.
- Tunnel leases require open/status/heartbeat/close, bind only to loopback, and expire or close when the authenticated desktop session changes.
- Read the bundled [Android stress requirements](specs/42_ANDROID_APK_STRESS_AGENT_REQUIREMENTS.md) and [RustDesk ADB tunnel contract](specs/51_RUSTDESK_REMOTE_ADB_TUNNEL_REQUIREMENTS.md). Historical acceptance is not proof that the current target passes; collect fresh evidence.

## Mixed-platform task planning

Model each boundary explicitly, for example:

```text
macOS Harness -> LMCP provider -> Windows SSH build node -> RustDesk ADB lease -> Android device
```

Verify and log identity, authorization, readiness, cancellation and result at every arrow. Failure at a downstream target must not be misreported as a controller or discovery failure.
