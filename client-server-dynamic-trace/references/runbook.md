# Dynamic trace runbook

## 1. Preflight

- Confirm authorization, target environment, exact process/service ownership, and allowed mutations.
- Inventory architecture and compatibility constraints: OS, x86/x64, CPU instruction set, calling convention, privilege level, ASLR/module identity, and injector/payload hashes.
- Resolve current PIDs, ports, module bases, binary hashes, uptime, and readiness. If multiple candidates exist, stop and disambiguate.
- Read the last verified workflow. Reuse its build flags and delivery path; older CPUs may require explicitly disabling unsupported vector instructions.
- Allocate a fresh run ID and evidence directory. Record a pre-injection health snapshot.

## 2. Probe design

Start from the narrowest stable semantic boundary:

- protocol frame encode/decode;
- command dispatcher entry/exit;
- state transition owner;
- authoritative calculation input/output;
- persistence begin/commit/rollback;
- client state consumer and final presentation decision.

Each record should contain only what is needed to answer the question: wall-clock time, monotonic sequence, PID/TID, hook ID, relevant stable identities, bounded typed fields, and an explicit truncation/error flag. Avoid unbounded strings, heap allocation, filesystem access, symbol lookup, stack walking, or network I/O in a hot hook.

Sampling must preserve transitions. Periodic snapshots may be low frequency; discrete commands, state changes, damage, target changes, death, loot, purchase, and transfer events should be event-driven.

## 3. Build and isolated validation

- Build for the target ABI and oldest required CPU.
- Run parser, serializer, queue-overflow, attach/detach, and malformed-input tests outside the live service.
- Verify a harmless known hook in an isolated process before touching the target.
- Hash injector, payload, configuration, and analyzer. Do not deploy an untracked rebuild.

## 4. Collector-first launch

1. Start exactly one collector with a fresh append-only output.
2. Verify its readiness and destination.
3. Re-resolve the exact target PID and health.
4. Attach once. Confirm payload-ready and heartbeat from that PID, not merely injector exit code.
5. Recheck service readiness before asking for the stimulus.

When user interaction is required, provide one self-contained launch/attach script or one concise action. Do not make the user repeatedly alternate between injector and uninjection commands. The script must report target PID, payload generation, collector destination, and final attach status.

### Fast path for an installed resident observer

When a maintained project already installs a resident observer, the response to
“inject the client/server” begins with one bounded status lookup. Reuse its current
collector and compare the exact PID, payload generation, ready event, heartbeat,
and requested probe manifest. Return one of two results immediately:

- `READY_EXISTING_OBSERVER`: begin the bounded action window without redeployment;
- `NEW_PID_REQUIRED`: stage the complete audited observer artifact for the next
  process, then request only the project’s standard restart/relogin action.

Do not use screenshots, mouse/keyboard focus, an unrelated hypervisor control
script, an ad hoc web launcher, or an extra payload on the same PID as a fallback.
If the project’s last verified workflow names a specific VM or transport, verify
that transport’s real readiness signal before invoking any similarly named tool.

## 5. Stimulus and capture

- Mark `baseline-start`, perform one action, then mark `action-start` and `action-end`.
- Leave enough quiet time before and after the action to distinguish periodic behavior.
- For client/server work, capture both ends over the same time window and include connection lifecycle events.
- If the action must be repeated, change one variable only and assign a new run ID.

## 6. Detach and recovery

- Stop accepting new records, flush the cold queue, and detach only the current payload generation.
- Do not kill the target to simplify cleanup.
- Recheck the original readiness signal and compare it with baseline.
- Preserve raw trace immutable; create compact summaries as separate files.

## Failure signatures

- **Injector exits immediately with no log:** check target CPU instruction support and payload entrypoint before changing paths or credentials.
- **Attach reports success but no events:** require payload-ready plus target-PID heartbeat; verify hook address against the loaded module hash.
- **Service stalls after attach:** detach immediately; inspect hot-hook allocation, blocking I/O, recursion, event flood, and loader-lock work.
- **Repeated attach makes the map/service fail:** enumerate payload generations and collectors; remove only stale experiment-owned instances, return to one injector/one collector.
- **Trace volume explodes:** retain discrete transitions, lower periodic sampling, and move formatting off the target thread.
- **Client and server events do not align:** check clock basis, reconnect/session generation, runtime-handle reuse, buffering delay, and dropped-record counters.
- **A rerun contradicts the first result:** preserve both runs, identify the changed input/environment, and downgrade the conclusion rather than selecting the preferred trace.
