# Evidence, implementation, and handoff contract

Read this reference when planning an experiment, grading evidence, converting a
finding into product code, or handing the work to another contributor.

## Evidence grades

- **S0 — static:** hash-locked binary/data/control-flow evidence; no runtime claim.
- **D1 — dynamic:** exact real PID, binary hash, timestamps, and raw runtime records.
- **C1 — correlated:** independent client/server records agree on one action and
  stable identities.
- **R1 — replayed:** a deterministic candidate test reproduces the declared
  transition and ordering.
- **E1 — end to end:** a real client drives the candidate server, or the candidate
  client drives the real server, and matches the declared external behavior.

Evidence grades are scoped. One E1 purchase does not prove combat; one D1 actor
does not prove every actor, action, Section, camera, latency, or failure branch.

## Required run layout

```text
run-<date>-<topic>-<sequence>/
  session-manifest.json
  client-trace.jsonl
  server-trace.jsonl
  network.pcapng
  client-payload.log
  server-payload.log
  recording/
  dumps/
  analysis/
    compact.json
    report.md
```

Raw traces are append-only within a run. Do not overwrite a successful baseline.
Compact reports are derived artifacts and must cite raw paths and SHA-256.

## Manifest fields

Record at minimum:

```json
{
  "runId": "YYYYMMDD-topic-NN",
  "question": "one falsifiable question",
  "hypotheses": [],
  "expectedDiscriminators": [],
  "authorization": "read-only unless explicitly stated",
  "timezone": "Asia/Shanghai",
  "targets": [
    {"side": "client", "pid": 0, "startedAt": "", "sha256": ""},
    {"side": "server", "pid": 0, "startedAt": "", "sha256": "", "section": 0}
  ],
  "tools": {
    "injectorSha256": "",
    "payloadSha256": "",
    "collectorSha256": "",
    "analyzerSha256": ""
  },
  "markers": {"baselineStart": "", "actionStart": "", "actionEnd": ""},
  "correlation": {
    "sessionGeneration": 0,
    "localObjectId": 0,
    "opcode": "0x0000"
  },
  "counts": {"events": 0, "dropped": 0, "truncated": 0},
  "attach": {"status": "", "payloadGeneration": ""},
  "health": {"before": "", "after": ""},
  "artifacts": []
}
```

Do not store credentials, tokens, unnecessary packet bodies, or personally
identifying account details in durable evidence.

## Analysis report

Separate every conclusion into:

1. **Observed:** typed records, protocol bytes, register/stack/object bytes, and
   actual video frames.
2. **Derived:** deterministic calculations from observed values, including formula
   and tool version.
3. **Inferred:** the narrowest explanation consistent with current observations.
4. **Unknown or contradicted:** missing variants, dropped events, conflicting runs,
   and the exact next discriminating experiment.

For numeric algorithms, state units, signedness, rounding/truncation, random draws
and their order, clamps, timers, ordering, side effects, and rollback. Numerical
agreement without random-consumption order or transaction-boundary agreement is not
equivalence.

## Converting evidence into code

1. Create a typed contract or fixture from raw evidence. Preserve original bytes
   and source identity separately from semantic projection.
2. Implement one shared algorithm at the actual ownership boundary. Do not embed a
   sampled name, account, ObjectID, Section, coordinate, angle, or screenshot.
3. Add positive, negative, boundary, malformed-input, ordering, retry, disconnect,
   duplicate, handle-reuse, persistence, and rollback tests as applicable.
4. Replay the original stimulus in isolated temporary state and compare declared
   fields plus event order.
5. Build the formal artifact atomically, verify hashes/signing/resource indexes and
   package-size gates, then repeat the external action in the real environment.
6. Update the current topic contract, global contract when affected, tests, source
   comments, evidence index, and status in the same change.

## Completion and status language

Use one of these explicit states when the full chain is not complete:

- `STATIC_ONLY`
- `DYNAMIC_PARTIAL`
- `CORRELATED_PARTIAL`
- `REPLAY_PASS_E1_OPEN`
- `CONTRADICTED`

Use “complete” only when the target remained healthy or was restored, the action
has bounded timestamped evidence, hashes and exact commands are retained, claims
are graded, a deterministic regression exists, the formal candidate passed the
same external behavior, and no requested work remains.

## Handoff summary template

```text
Question:
Scope and evidence grade:
Exact binaries/resources and hashes:
Observed:
Derived:
Inferred:
Unknown/contradicted:
Candidate implementation and owner:
Regression/replay result:
Formal artifact and E1 result:
Health/cleanup result:
Evidence paths:
Next smallest discriminating action (only if still open):
```
