---
name: vibekits-fleet-compatibility
description: Gate VibeKits Harness desktop upgrades against the project's real Mac and Windows compatibility fleet, preserving device identity, authorization, workspace access and existing functions before release.
---

# VibeKits fleet compatibility

Use this skill when changing, building, signing, upgrading, or publishing VibeKits Harness desktop clients. Read the current project's `docs/HARNESS_UPGRADE_STANDARD.md`, `docs/acceptance/MAC_HARNESS_RECURRING_REGRESSIONS.md`, and `docs/RELEASE_GATES_ALL_CLIENTS.md` before selecting a candidate or target. The project documents own the current device IDs and exact test matrix; do not carry a stale device list between repositories or releases.

Freeze one candidate with its source/lock, runtime version, app version, architectures, bundle identity, signing requirement, hash and rollback identity. Keep build intermediates on the machine's configured build volume. A source edit or new signature creates a new candidate; repeat affected checks on its exact final bytes.

Use a short task-specific temporary directory on that build volume for macOS Unix sockets; a deeply nested `TMPDIR` can fail the IPC tests at the platform path-length limit. Preserve the first failure log, then rerun the exact failed cases and full preflight under the corrected path. Keep the dependency lock unchanged when an offline Pub cache copy rewrites only content-hash metadata. For Universal Mac and Windows builds, verify the same native relay source supports the existing `--vibekits-harness-protocol` probe and current simulator gate response before signing either client.

Before updating another device, install and exercise the final signed candidate on the build Mac. Test Harness first launch, workspace selection, actual model request, MCP tool listing and a read-only call, session operations, prior regressions, and unchanged authorization. Build success, a green status light, and a successful simulator connection are different observations; none proves the others.

For each device in the project's approved fleet, record the actual running app path and version, OS/CPU, current simulation ID and transport, prior authorization, and a recoverable pre-upgrade copy. Compare bundle ID, Team ID, designated requirement and relevant entitlements before a same-identity overlay. After upgrade, reconnect by the same ID and verify launch, workspace selection, Harness request, MCP read-only call, existing session/data, and permission continuity. Intel/macOS 12 must use its Safari 15 compatibility frontend; run the directory-picker regression and reject missing `Response.headers` or raw `f.headers.get` errors. Use Windows-specific native build/signature tests for Windows devices. Do not infer target compatibility from another machine.

After any relay-helper replacement or restart, disconnect and reconnect from a separate machine by the original simulator ID, then call a read-only tool. The relay's volatile simulation gate can reset while the UI or heartbeat still says ready; `registered/callable`, a green indicator, and process liveness do not prove remote access. Treat `remote_disabled` as a regression and restore existing authorized access before continuing. In installer health checks, an HTTP 401 from the protected DSH root means the service responded; if rollback is needed, stop the new process and confirm the old disk package and old running process match.

On a recoverable authorized test device for every platform, also verify ordinary App removal followed by same-signature reinstall while preserving user configuration, Keychain and device-identity material. The original simulation ID, authorization, room membership and remote interaction must survive. An overlay install does not prove this case; mark it BLOCK when it has not been run. Never delete identity or user data to manufacture a clean-install pass.

Record PASS/BLOCK per required device and regression with logs and candidate hash. Offline, untested, changed-ID, lost authorization, or still-running-old-version devices remain BLOCK. Do not publish or claim the fleet works until every required gate in the project documents is proved on the same candidate. Preserve failed logs and rollback packages; do not reset user data or credentials to make a test pass.
