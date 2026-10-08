# SWDOL project runbook

Use this reference for concrete static reconstruction and authorized runtime
instrumentation in the SWDOL repositories.

## Project roots and authorities

```text
SWDOL2026_ROOT=/Users/kemi/coding/swdol2026
XYONLINE_ROOT=/Users/kemi/coding/xyOnlie
KEMI_RD_ROOT=/Users/kemi/coding/kemi-rd
TRACE_ROOT=/Users/kemi/coding/xyOnlie/tools/legacy-dynamic-trace
```

`swdol2026` owns current product code and current contracts. `xyOnlie` contains
the original-client/server reverse-engineering archive and stable trace tooling.
`kemi-rd` contains mandatory development rules and authorized legacy environments.
Historical reports preserve evidence but do not outvote the current documentation
index and global contract.

## Static reconstruction

1. Write one falsifiable question and competing explanations.
2. Record SHA-256, architecture, ABI/calling convention, preferred/load base,
   target CPU, resource hashes, analyzer version, exact command, and output hash.
3. Establish width, endianness, signedness, alignment, count/index rules, and
   malformed-input behavior before assigning semantics. Keep unproved fields named
   `unknown_*`.
4. Recover all material callers and consumers, object creation/update/destruction,
   thread/queue/timer ownership, request/authority/persistence/publication order,
   and normal/refusal/timeout/disconnect/rollback paths.
5. Separate protocol record order from semantic fields. Selection-page equipment,
   world equipment, runtime handles, resource template IDs, account/role IDs, and
   display names are distinct domains.
6. For formulas, record units, signedness, truncation, random-consumption order,
   clamps, timers, side effects, transaction boundaries, and failure behavior.
7. Deliver a repeatable analyzer, hash-locked byte slices, typed JSON/fixture,
   boundary and corruption tests, and a list of facts still requiring runtime
   discrimination.

Relevant original data includes DBF, ACT, PLY, TEX, TSW, WLD, MBO, S3D, protocol
frames, and persistence records. A parser success proves addressability, not final
rendering or live behavior.

## Dynamic preflight

1. Confirm authorization and allowed mutation policy.
2. Allocate a unique `runId` and append-only evidence directory.
3. Resolve exact client/server PID, process start time, port, module base, binary
   hash, Section/Act, and the real readiness signal. Disambiguate multiple instances.
4. Capture pre-injection readiness, connection, and quiet-traffic baseline.
5. Hash injector, payload, collector, analyzer, configuration, and tracepoints.
6. Confirm one collector, one payload generation, and a documented kill switch.

The original client guest uses Pentium II 450MHz. Preserve the verified build
flags and run the opcode audit after every rebuild:

```text
-march=pentium2 -mno-sse -mno-sse2 -mno-sse3
```

Windows XP compatibility alone does not prove Pentium II compatibility.

## Stable launch and attach order

1. If the tool ISO changed, use
   `tools/legacy-dynamic-trace/mount_86box_client_iso.sh <ISO>`. Confirm the unique
   86Box process opened that absolute image and the virtual network link remains up.
2. Start exactly one host UDP collector on port `27667` with a fresh output path.
3. When protocol correlation is needed, start client/server pcap in the same host
   clock window.
4. Start legacy servers only through their already verified service workflow.
   `TRACE-INJECT-ONLY.BAT` attaches to running services; it must not start, stop, or
   reconfigure them.
5. Start the original client through the verified `GO.BAT` or
   `ONE-CLICK-LOGIN.BAT` resident-watcher flow. Do not invent another disc, launcher,
   or focus-stealing input path.
6. Require this sequence on each exact target:

```text
PAYLOAD_LOADED -> PROBES_ACTIVE -> target-PID heartbeat -> expected business probe
```

7. Recheck readiness, retain at least three seconds of quiet baseline, then request
   one minimal user action. When repeating, change one variable and use a new run.

## Probe and capture design

Prefer these semantic boundaries:

```text
protocol encode/decode -> dispatcher -> state owner -> authority calculation
-> transaction begin/commit/rollback -> publication -> client apply
-> final render/UI/audio decision
```

Each hot record contains wall-clock anchor, monotonic sequence, PID/TID, hook ID,
stable identities, bounded typed fields, and truncation/error flags. Do not allocate,
walk stacks, symbolize, format, compress, write files, take screenshots, or perform
network retries in a hot hook.

Discrete transitions such as request, target change, damage, status, death, loot,
purchase, transfer, and disconnect are event-driven. Per-frame draw/matrix probes
must have strict sample caps and retire by restoring original bytes. This prevents
the previously observed selection/world stalls caused by perpetual INT3 stepping.

For spell/effect visual work, reuse:

```text
$TRACE_ROOT/arm_spell_debug_session.sh
$TRACE_ROOT/record_86box_spell_session.sh <trace.jsonl>
```

Begin recording after map login or trace ready, before the click. Preserve 750ms
pre-roll and 1000ms after the last event. Use the host clock to align video and
trace. Returning to role selection, process exit, or bounded heartbeat loss stops
the session and its owned recorder/collector/watcher.

## Client/server correlation

Reconstruct the complete chain when applicable:

```text
user/client intent -> client validation -> outbound request -> server parse
-> authority/state transition -> persistence transaction -> outbound publication
-> client state application -> visible/audio result
```

Use shared host wall time and preserve monotonic ordering on each side. Correlate
with session/generation, `localObjectId` or actor handle, opcode/request ID,
Section/Act, Magic/Object/Plot ID, PID/TID, stack identity, and bounded time window.
Guest QPC values order one process only; they are not directly comparable across
guests. Missing events are findings, not permission to synthesize a bridge.

## Detach and recovery

Stop new records, flush the cold queue, and detach only the current experiment's
payload generation. Do not kill the target to simplify cleanup. Use standard client
logout, verify original service readiness, and check for leftover collectors,
recorders, watchers, ports, sockets, or character sessions. Preserve raw artifacts;
write summaries separately.

## Known failure signatures

| Symptom | First check |
|---|---|
| Injector exits with no log | SSE/SSE2 on Pentium II; payload entrypoint and opcode audit |
| `INJECT_OK` but no events | target Section/config whitelist, probe bytes, payload ready and target-PID heartbeat |
| Selection or map entry stalls | unbounded per-frame INT3 hooks or blocking hot-hook work |
| Failure after repeated attach | duplicate collector/payload generation or stale watcher |
| Client/server timeline mismatch | clock basis, reconnect generation, handle reuse, buffering and dropped counts |
| “Resource missing” during entry | first separate auth, role routing, map handshake, initial world, source read, decode and GPU stages |
| APP intermittently lacks `blobs.pack` | build/start race from rebuilding a user-visible release in place |
| Workspace becomes huge | distinguish one APP from repeated builds, trace/video evidence, dumps, and expanded intermediates |

## Resource and package boundary

Static extraction does not authorize permanent expanded assets in the product.
Keep content-addressed compressed source stores and compact indexes on disk. Let C++
read slices and decode only the current Section, visible instances, materials, and
actions. Bound CPU/GPU caches with ownership, LRU/refcounts, and GPU fences. Never
package screenshots, recordings, dumps, trace logs, build caches, or obsolete
expanded `.rgba/.bin` catalogs in the formal APP. Measure one formal APP against
the current package budget; do not report the whole build workspace as package size.
