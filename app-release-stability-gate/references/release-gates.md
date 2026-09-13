# Release gates

The evaluator produces `PASS` only when all required evidence is present. Any hard failure produces `BLOCK`.

## Hard blockers

- Candidate artifact hash, package/bundle/product ID, version/build, source revision or signing identity differs from the frozen input.
- Any required case is `fail`, `blocked`, `not_run` or missing.
- Any P0/P1 feature, change-risk item or historical regression lacks a mapped passing automated case.
- Any required new/changed test lacks passing positive control, failing negative control and passing restored control.
- Any new crash, ANR/hang, native dump, OOM, data loss, security/privacy failure, update failure or startup failure occurs.
- Clean installation or in-place upgrade fails on a required platform.
- A required supported platform/device/architecture class is absent.
- Resource evidence is missing, belongs to another candidate/environment or violates a configured limit.
- Evidence was overwritten or cannot be tied to the candidate hash and automation revision.
- A discovered failure was fixed without a permanent regression, root-cause evidence and a full-gate rerun on the rebuilt bytes.

## Default resource guards

Stricter product limits take precedence:

- New crashes, hangs/ANRs, native dumps, OOMs and unexplained process restarts: 0.
- Required-case pass rate and historical-regression pass rate: 100%.
- Idle CPU median after stabilization: at most 5% of one core unless documented product behavior and the stable-build baseline justify another limit.
- Memory growth after the configured repeated core loop: no more than both 50 MiB and 20% from stabilized baseline; no monotonic growth over the final half of samples.
- Candidate regressions versus the prior stable build: at most 15% for startup, steady CPU, peak memory and frame-jank unless a stricter limit is defined.

If a metric is not meaningful or cannot be collected reliably, the profile must say why and provide an alternative assertion. Missing evidence never passes silently.

## Flakes

A failing first run remains a failure even if a retry passes. Quarantine requires a defect ID, owner, reproducible evidence, expiry and explicit acceptance for that release. A retry is diagnosis, not deletion of evidence.

## Candidate immutability

Signing or repackaging usually changes bytes. Freeze and report both the tested pre-sign artifact and final distributed artifact when the platform requires staged checks. Run signature/install/smoke/update checks again on the final distributed bytes; never transfer a PASS from a different hash.
