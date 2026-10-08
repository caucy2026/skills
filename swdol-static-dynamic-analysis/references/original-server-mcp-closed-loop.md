# Original server injection → MCP client → candidate comparison

Use this procedure when unfinished SWDOL behavior is most efficiently resolved by observing the original server while the reconstructed client performs a normal action, then replaying the same action against the candidate server.

## Required result

```text
original binary/resource S0
→ exact original server PID + bounded probes
→ reconstructed fixed-path client performs one normal MCP action
→ original server D1 business events
→ client/server time-window correlation C1
→ typed formula/state/packet contract
→ candidate implementation and deterministic replay R1
→ same client/resource/input against candidate server E1
→ affected historical regression matrix
→ restore target health and fixed client package
```

Do not declare equivalence from `INJECT_OK`, heartbeats, static disassembly, component tests, screenshots, a candidate-server run, or a client-only trace. Each proves one layer only.

## Load project truth

Read, in order:

1. `/Users/kemi/coding/swdol2026/document/第一原则-任何修复不得破坏已验收功能.md`;
2. `/Users/kemi/coding/swdol2026/document/README.md`;
3. `/Users/kemi/coding/swdol2026/document/20260905-静态分析与双端动态分析全局工作规范.md`;
4. `/Users/kemi/coding/swdol2026/document/20260902-客户端整体研究统一总合同与文档纠错.md`;
5. the newest topic contract and evidence ledger;
6. the map/service-specific safe runbook and last successful attach record.

For Map04 use `/Users/kemi/coding/xyOnlie/tools/legacy-dynamic-trace/MAP04-SAFE-RUNBOOK.md`. Do not use a historical start-and-inject launcher when a healthy server already exists.

State one falsifiable question before the action. List competing explanations and the probe, packet field, register, state byte, or persistence read-back that separates them.

## Lock identities and rollback

Create a unique run directory and manifest. Record:

- original EXE SHA-256, function slice SHA-256, image base, map/Section and port;
- payload, attach-only executable, collector, analyzer and tracepoint SHA-256;
- fixed client executable, resource index, bundle identifier and build version;
- candidate server and relevant configuration/catalog SHA-256 values;
- account/role slot without storing its credential;
- authorization scope, allowed action, mutation policy and kill switch;
- the fixed-client rollback receipt when a temporary package is installed.

Resolve the listener owner instead of guessing a PID. Require exactly one owner, the expected executable name and expected command-line configuration. Record application health before injection; open ports alone are insufficient.

Before a global code change, record the shared owner, direct callers, indirect consumers, accepted cases and rollback file. Movement impact includes protocol decoding, authority position, AOI publication, prediction, body/equipment/name matrices, target/effect attachment, stop, transfer, collision, camera and persistence.

## Prepare one collector and one payload generation

Reuse a healthy collector when it owns the documented UDP port and output path. Otherwise start exactly one collector before injection and write to a fresh append-only trace.

For the original Pentium II/Windows target preserve:

```text
-march=pentium2 -mno-sse -mno-sse2 -mno-sse3
```

After each rebuild, run the opcode audit and revalidate every probe byte against the locked original binary. Any mismatch fails closed before installing a breakpoint.

The payload must accept only the intended map/service command line, install the smallest semantic boundary set, keep hot handlers bounded and allocation/I/O free, cap high-frequency events, restore original bytes when retiring, use a distinct addon name, and refuse a duplicate generation.

## Deliver and attach without changing the service

Prefer the last verified delivery path.

### Authenticated SMB/SCM

Use the project attach-only tool. Read the Windows credential only through a hidden runtime prompt or approved secret mechanism. Never put it in argv, source, logs or durable evidence. Upload only intended files, read them back, compare bytes/SHA, and run the short-lived attach-only executable through the documented SCM path.

### Existing UTM desktop HTTP/HTA

Use this only when the runbook records it and the current Administrator desktop is authorized.

1. Enable UTM input capture and verify its accessibility value becomes `1`.
2. Start guest `cmd.exe` and require visible command echo.
3. Stage only the intended HTA and DEBUG.EXE reconstruction texts in a unique temporary host directory.
4. Bind HTTP only to the private VM host address, never `0.0.0.0`.
5. Verify every URL returns 200 and each DEBUG text reconstructs the expected binary byte-for-byte before guest execution.
6. UI automation can drop `.`, `:`, `/` and `\`; type punctuation explicitly and verify the guest command or guest-address HTTP log.
7. The HTA may download, reconstruct and execute attach-only. It must not start, stop, restart, replace or reconfigure the original service or write its database.
8. Stop the HTTP server after delivery.

Host-side HTTP checks are not guest-download evidence. Require a GET from the guest address plus guest file/result evidence.

## Grade attachment readiness

Attachment is ready only when all are true:

1. result is `INJECT_OK` or `ALREADY_ACTIVE`;
2. recorded PID equals the unique listener owner;
3. payload log contains `PAYLOAD_LOADED`;
4. payload log contains the expected `PROBES_ACTIVE` count;
5. collector receives a new Ready event and fresh heartbeat from that PID;
6. original service health remains good.

Call this `INJECTED_READY_BUSINESS_ACTION_OPEN`. It is not D1 while requested business probes remain zero. When ready, reuse the same PID/generation rather than injecting again.

## Drive the original backend through MCP

Use the maintained MCP adapter and fixed formal app path. Never bypass product-identity, marker, resource, socket, evidence-directory or single-instance checks.

Before launch:

- identify and close only authorized or test-owned stale clients;
- preserve unrelated user-owned clients;
- verify fixed executable/resource SHA immediately before launch;
- verify the account belongs to the authorized snapshot;
- choose a role with a documented normal route to the target Section.

If a candidate must occupy the fixed path, use `/Users/kemi/coding/swdol2026/tools/install_client_acceptance_trial.py`. It must verify current/candidate SHA, signature, bundle ID, distinct build version, no running client and create a rollback receipt. This is temporary acceptance, never release approval. Restore using that receipt after the run.

Use only normal product actions: login, role selection, plot/item/spell transfer, movement, interaction, casting and inventory operations that pass through production validation and protocol encoding. Do not write client coordinates, forge packets, edit the original database or call server functions directly.

Defensive rejection branches can be unreachable from a healthy product client
because its own encoder, step clamp or state machine prevents the invalid input.
Prove that invariant first with static client ownership plus bounded dynamic
counterexamples. Then a minimal negative protocol D1 may reuse the real Master
authentication, role selection, map handshake and authoritative starting state,
changing only the one boundary field needed to reach the rejection. Label it
`D1_NEGATIVE_PROTOCOL`, preserve the normal MCP E1 separately, and never present
the negative probe as normal player behavior. One accepted lower boundary and one
rejected upper boundary only bracket the contract; do not guess an unseen dynamic
allowance or replace it with a fixed constant.

Capture a non-black initial frame before navigation/action. Reach the target map and require world readiness, connection, role projection and released input ownership. Preserve at least three seconds of quiet baseline. Perform one bounded action and stop it normally.

Record client wall/monotonic timestamps, session/world generation, controlled handle, Section, protocol counters, request/result fields, authority/render coordinates, input state and before/after captures. Stop/logout normally and close only the owned client.

## Correlate original server D1

Slice the server trace from before the action through bounded post-roll. Require the exact PID and stable identities. The usual movement chain is:

```text
263 request/position commit
→ 264 destination state
→ 265 state-FFFF fast path
   or 266 checked path → 267 collision result
→ 268 authoritative 0403 correction when rejected
```

Preserve raw records. Decode registers, stack and snapshots using the tracepoint-specific contract, locked original bytes and calling convention.

Correlate by host time window + exact server PID + client session/world generation + localObjectId/actor identity + opcode/request + Section/Act. A heartbeat, display name, adjacent line or same-source helper is not independent confirmation.

Separate results into:

- **Observed:** packets, probes, registers, state values and screenshots.
- **Derived:** signedness, scale, truncation, deltas, speed, timing and order.
- **Inferred:** the narrowest formula/state machine consistent with all observations.
- **Unknown/contradicted:** unhit branches, ambiguous ownership, drops and mismatches.

## Convert evidence into contract and replay

Bind the finding to original EXE and function-slice SHA. A numeric contract states units, widths, signedness, endian order, scale, float-to-integer rule, clamps/overflow, clocks, branch order, authority/publication/persistence side effects, refusal and rollback.

Preserve raw bytes separately from semantic fields. Add positive, negative, boundary, malformed-input, ordering, retry/disconnect, duplicate and persistence cases. The regression must fail against the prior incorrect implementation and pass against the corrected shared owner. Never encode the observed account, role, map, object, coordinate, PID or screenshot as product logic.

## Compare the candidate server

Use the same reconstructed client and resource index whenever possible. Start the candidate server in isolated temporary state with the same relevant catalogs/resources and record all hashes.

Repeat the same product action and compare:

- opcode, packet length, fields and order;
- accepted/refused branch and reason;
- authority coordinates, height, velocity and heading;
- AOI publication and observer output;
- stop/correction behavior;
- safe-logout/relogin persistence;
- render/action/attachment result;
- required failure, disconnect and retry behavior.

For multiplayer presentation use two normal clients on one clock. State thresholds before the run. A mean match does not excuse a burst, endpoint error, wrong stop or black screenshot.

Use `CORRELATED_PARTIAL` while original or candidate branches remain missing. `R1` requires deterministic replay. `E1` applies only to the exact external behavior tested.

## Run affected regressions on one artifact set

Use one client SHA, one server SHA and one resource-index SHA across the target and accepted cases. A global movement change includes cardinal/diagonal keyboard and joystick; wall, slope and multi-level ground; transfer and post-transfer height; observer interpolation, repeated endpoints and stop; camera/body/equipment/name/target/effect attachment; disconnect/relogin persistence; shared plot/status/magic/inventory cases; backend foundation and project full gates.

Report passed/total, failures, incomparables, component-only results, blockers, commands, paths and hashes. Any new historical failure keeps release blocked.

## Cleanup and restoration

1. Release input and log out the owned client normally.
2. Close only experiment-owned clients.
3. Restore the previous fixed app from the exact trial receipt.
4. Stop experiment-owned HTTP servers and recorders.
5. Keep collector/payload only when the runbook explicitly requires a resident observer; never duplicate them.
6. Recheck original service readiness and listener ownership.
7. Preserve raw traces, failed attempts, screenshots, manifests and SHA values.
8. Write derived reports separately without rewriting raw evidence.

## Guard initial-world evidence and parallel client identity

An encoder and a valid payload do not prove that an initial event can reach the
client. Check every gateway/session allowlist, initial-batch byte/count budget and
phase transition that the event must cross. Add a login-session regression for the
new opcode as well as the later active-world protocol test.

`worldReady` may become true before the tail of the bounded initial application
batch is consumed. When the claim depends on a specific initial event, wait for
that event's receipt counter and decoded authoritative state. Do not sample once
at Section readiness and treat zero as absence. Preserve the early sample as a
harness failure if it caused a false negative.

Hash the fixed client binary and resource index immediately before every original
and candidate action. Another authorized task can replace the fixed package after
an earlier receipt was created. If identity drift is detected, wait for its owned
client to close, create a fresh nested trial that backs up the new current package,
run the exact comparable artifact, and roll back using the newest matching receipt.
Never apply a stale receipt across an intervening package change.

## Failure routing

| Failure | Interpretation | Next action |
|---|---|---|
| TCP open, no application handshake | listener health is insufficient | capture bounded handshake before changing credentials/client |
| first challenge arrives, second does not | master handshake incomplete | preserve timing/bytes; do not send login early |
| both challenges arrive, authentication times out for multiple accounts | client build or master authentication mismatch | compare a last-known accepted fixed package through the trial tool |
| fixed app runs without an owned MCP socket | single-instance gate works | close only an authorized/test-owned exact process; never bypass it |
| guest URL is 404 | UI input may have dropped punctuation | verify guest command and host access log; type punctuation explicitly |
| host URL is 200 but guest has no file | host preflight is not delivery evidence | require guest-address GET and guest file/read-back |
| `INJECT_OK` without Ready/heartbeat | payload readiness is unproved | inspect byte checks/transport; do not trigger action |
| Ready/heartbeat with zero business probes | requested behavior is not D1 | perform one normal MCP action in a bounded window |
| unsafe event volume | hot hook is too broad | stop collection, retire current high-frequency points, verify recovery |
| three same-route attempts have no net evidence | method is exhausted | preserve all three and switch discriminator; no fourth blind retry |
| candidate matches one sample but regressions fail | shared contract is incomplete | keep release blocked and repair shared owner, not an ID/map constant |
| initial event encodes but map login disconnects | login/session initial-event gate rejected it | add the evidence-backed opcode to the proven initial set and test the full login phase |
| server trace proves initial event but MCP readiness shows zero receipts | readiness snapshot raced the initial batch tail | wait for the event receipt/decode deadline, then classify |
| fixed client SHA differs from the active trial receipt | another authorized task changed the package | preserve the new package with a fresh receipt; never force the stale rollback |

## Completion statement

```text
For original binary <SHA> / function <slice SHA>, reconstructed client <SHA>
performed <normal action> in Section <N>. Exact original server PID <PID>
produced <probe/packet sequence>. Observed <facts>; derived <formula/order>;
unknown <remaining branches>. Candidate server <SHA> reproduced <declared fields>
under the same input and client/resource identity. Replay <passed/total> and
affected regressions <passed/total>, with <new failure count> new failures.
Final scoped status: <D1/C1/R1/E1 or partial state>.
```

Do not say the feature, domain or release is complete while any required original business event, candidate comparison, persistence check, affected regression, package restoration or health check is missing.
