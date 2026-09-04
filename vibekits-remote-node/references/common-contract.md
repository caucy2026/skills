# Cross-Platform Remote Simulation Contract

## Operating model

A task has four separately verified identities:

- controller: the local Harness/agent initiating work;
- provider: the APP or node exposing tools;
- host: the physical or virtual OS instance;
- target: the build destination, desktop session, Android serial, or other controlled resource.

Do not infer one identity from another. An LMCP APP on a Mac can control a Windows build host, which can in turn reach an Android device.

## Discovery and capability selection

For VibeKits/LMCP work, use the repository's current LMCP/2 standard as authoritative. The expected baseline is:

- UDP multicast `239.255.42.99:47831`, multicast TTL 1;
- bind reuse suitable for multiple APPs sharing the discovery port;
- announcement every 4 seconds and offline TTL of 12 seconds;
- advertised HTTPS Streamable HTTP MCP endpoint, normally `POST /mcp`;
- `initialize`, then live `tools/list`, then schema-valid `tools/call`;
- stable `app.id`, privacy-preserving `hardwareCode`, `instanceId`, display name, certificate fingerprint, catalog revision, and catalog digest;
- signed caller identity, TLS fingerprint validation, replay protection, and persisted authorization scope.

The announcement is not a capability catalog. Refresh `tools/list` when a provider appears, its catalog revision/digest changes, a task begins and freshness matters, or a prior call reports stale/unknown capability. Validate arguments against the current JSON Schema and honor risk, cancellation, concurrency, timeout, and result metadata.

Read the bundled [LMCP/2 standard](specs/50_LMCP_APP_DEVICE_IDENTITY_AND_SWITCH_STANDARD.md) when implementing or diagnosing LMCP behavior. The installed skill has no dependency on the author's local checkout. Treat version numbers in the snapshot as historical; query the live provider for its current catalog.

## Transport selection

Prefer the narrowest authenticated transport that exposes the required capability:

1. LMCP/MCP for advertised application tools and agent coordination.
2. SSH for host build/shell administration when a registered host contract exists.
3. ADB for an Android device that is locally reachable or exposed through an authenticated tunnel.
4. RustDesk/VibeKits tunnel interfaces for a remote desktop-owned ADB or session capability.
5. Serial for independent device health observation or recovery evidence when configured.

Do not treat discovery as authorization, IP address as identity, a TCP connection as tool readiness, or a successful command as physical task completion.

## Preflight

Before mutation, capture:

- time, controller identity, target identity and intended scope;
- OS/version, architecture, shell, working root, free space and filesystem;
- transport endpoint and verified fingerprint/certificate/device serial;
- source revision and dirty state;
- current advertised catalog revision/digest and selected tool schema;
- compiler/runtime/package-manager versions needed by the requested task.

Preserve unrelated local changes. Resolve real paths before cleanup or destructive operations.

## Authorization behavior

Local Harness may call local tools within its configured authority without an extra remote-approval layer. A remote caller requires the provider-side pairing and persisted authorization scope. Once a remote caller is validly authorized for a tool, risk class, and resource scope, execute matching calls without a second blocking prompt; keep non-modal activity, audit, cancellation, revoke, and caller-block controls visible.

Require renewed authorization only when identity changes, scope expands, a certificate rotates, permission is revoked, or OS permission is lost. Network reconnects, APP restarts, or non-expanding catalog revisions do not by themselves invalidate persisted authorization.

## Long-running work

Prefer asynchronous tools returning a stable `taskId`. Require status/progress, final result, cancellation, last-result recovery, idempotency key behavior, bounded concurrency, and lease/heartbeat semantics where a resource must remain open. After reconnect, query task status before retrying. Never duplicate a destructive operation merely because a response was lost.

For repeated install/launch/stress loops, define before starting:

- exact iteration count;
- per-iteration phases and success evidence;
- heartbeat/watchdog sources (for example ADB plus serial);
- abort thresholds for crash, hang, overheating, storage exhaustion, or target loss;
- retry limit and whether a retry consumes an iteration;
- logs and artifacts retained after pass/fail.

## Evidence and handoff

Record timestamps, endpoint/identity fingerprints, source revision, resolved work paths, tool name and catalog revision, sanitized parameters, trace/task IDs, exit/error codes, artifact hashes, measured results, and cleanup state. Report every requested stage as pass/fail/blocked/skipped. Do not claim platform support based only on shared unit tests or another OS passing.
