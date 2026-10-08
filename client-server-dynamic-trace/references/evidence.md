# Evidence and handoff contract

## Evidence levels

- **S0 — static:** binary/data/control-flow evidence only; no runtime observation.
- **D1 — dynamic:** observed in the real target with exact PID, binary hash, timestamps, and raw records.
- **C1 — correlated:** independent client and server records agree on the same action and stable identities.
- **R1 — replayed:** a deterministic test or replay reproduces the observed transition in the candidate implementation.
- **E1 — end to end:** the real client exercises the candidate server and matches the reference on the declared fields, order, results, and persistence boundary.

Higher levels do not erase their scope. One E1 purchase does not prove combat, and one D1 hook does not prove a formula for all objects.

## Required run manifest

Store a machine-readable manifest next to raw traces containing:

- run ID, question, hypothesis, expected discriminating observations;
- authorization/scope and mutation policy;
- host identifiers without secrets;
- target PIDs, process start times, ports, module/binary SHA-256;
- injector, payload, collector, analyzer hashes and configuration;
- wall-clock timezone plus monotonic start/end;
- action markers and stable identities used for correlation;
- event counts by hook, dropped/truncated counts, attach/detach status;
- preflight and postflight readiness results;
- paths and SHA-256 for raw and derived evidence.

## Analysis output

Separate four categories:

1. **Observed:** direct typed records and protocol bytes.
2. **Derived:** deterministic calculations from observed values, with formula/tool version.
3. **Inferred:** the smallest explanation consistent with observations.
4. **Unknown/contradicted:** missing variants, conflicts, and experiments still required.

For algorithms, list inputs, units, signedness, truncation/rounding, random draws and their order, clamps, timers, ordering, side effects, and failure/rollback behavior. A numerical match without matching random-consumption order or transaction boundary is not equivalent.

## Conversion into implementation

- Create a typed contract or fixture from the raw evidence; do not embed display names or one observed object ID as product logic.
- Add negative, boundary, ordering, retry, disconnect, and persistence tests.
- Run the candidate in an isolated environment with temporary state.
- Replay the same stimulus and compare event order and declared fields.
- State any remaining reference-only behavior that the candidate does not yet implement.

## Durable workflow record

When a method becomes stable, record prerequisites, exact commands and order, build flags, artifacts and hashes, target environment, success gates, common failures, rollback, date, and evidence paths in the project documentation. A future operator should be able to reproduce it without chat history or guessing.
