# Test strategy

## Suite order

Before G0, validate the finalized executable plan and prove every new/changed test can fail under a controlled bad condition. Provision fixtures, test accounts, peers and services automatically from versioned setup scripts; record their identities and cleanup commands.

### G0 — source and artifact integrity

- Reproduce or verify the release build using locked dependencies and the intended configuration.
- Verify hash, signing/notarization, product identity, version/build number, architecture and production flags.
- Confirm the tested bytes are exactly the bytes intended for publication.

### G1 — installation, upgrade and startup

- Clean install and first launch on each required platform class.
- In-place upgrade from the currently published compatible version without clearing data.
- Assert retained accounts, settings, permissions and user data.
- Verify launch, relaunch, cold/warm start and platform security checks.

### G2 — deterministic product functions

- One positive end-to-end path for every P0/P1 function.
- Boundary, invalid-input, cancel, retry, concurrency and persistence paths where applicable.
- Verify outputs and durable state, not only visible navigation.
- Use controlled accounts, peers, servers, files and hardware fixtures.

### G3 — historical and change-impact regressions

- Execute every permanent historical regression on each affected platform.
- Recreate original timing, lifecycle, version, account, locale, permissions, network and hardware conditions.
- Execute direct and negative cases derived from each release diff.
- Assert both expected behavior and absence of original failure signatures.

### G4 — lifecycle, recovery and compatibility

- Background/foreground, close/reopen, process termination/restart, sleep/wake, display/rotation changes and reboot behavior where claimed.
- Offline, latency/loss, service interruption, reconnect, cancellation and retry.
- Permission denial/revocation/regrant and OS security prompts.
- Supported OS versions, architectures, displays, locale, font scale, theme and assistive technologies.
- Required peripherals and graphics/media behavior on real hardware.

### G5 — resource and performance stability

Measure a stabilized idle baseline, fixed core scenario, repeated-loop state and post-loop recovery:

- process and system CPU;
- private/working/PSS/RSS memory and platform-specific heaps;
- thread, handle/file-descriptor and child-process counts;
- startup, response latency and frame/jank metrics;
- network, wakeup, battery and thermal impact where relevant;
- crash, ANR/hang, OOM, watchdog, restart and dump deltas.

Run the same scenario on the prior published build when available. Resource comparison must use the same machine/device, environment, data and sampling schedule.

### G6 — soak, concurrency and bounded exploration

- Run the real core workflow continuously for the configured duration with periodic assertions and samples.
- Exercise repeated connect/disconnect, open/close, install/update, import/export or equivalent product loops.
- Use bounded state-model exploration or fuzzing with recorded seed after deterministic tests.
- Convert every reproducible fault into a deterministic permanent regression.

### G7 — final distributed bytes

- Recheck hashes, trust/signature/notarization and package metadata after signing or packaging.
- Install or upgrade using the exact distribution artifact and path customers receive.
- Repeat startup, critical smoke, updater/store detection and historical packaging regressions.
- Compare downloaded/public bytes with the frozen released hash when publication is requested.

## Evidence conventions

Use UTC or explicit timezone consistently. Take an environment snapshot before each suite and mark platform logs at suite start. A visual image proves appearance only; use accessibility, API, protocol, filesystem, database or process-state assertions for behavior. Preserve raw output and a normalized machine-readable result.
