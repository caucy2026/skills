# Autonomous discovery, test and repair loop

## State machine

Persist `run-state.json` after every transition so another agent can resume without repeating successful work:

`DISCOVER → MODEL → GENERATE → IMPLEMENT → PROVE_TESTS → BUILD → FREEZE → DEPLOY → EXECUTE → EVALUATE`

- On `PASS`, preserve the evidence bundle and hand the exact artifact hashes to the requested release workflow.
- On a product failure, transition through `REPRODUCE → TRIAGE → ADD_REGRESSION → FIX → BUILD → FREEZE`, then run the failing case, its family, change-impact set and the entire required gate.
- On an automation failure, repair the adapter/test first and repeat `PROVE_TESTS`; never change product code to satisfy a broken test.
- On an environment failure, repair or reprovision the test environment automatically when authorized, then repeat the interrupted state.

The agent continues the state machine without asking between routine, reversible and already authorized steps. Persist current artifact hashes, completed case IDs, commands, evidence paths, failure signatures, source changes and next state.

## Automatic behavior discovery

Combine static and dynamic discovery:

- enumerate routes, windows/screens, commands, menu actions, public APIs, protocol messages, background jobs, services, installers/updaters, persistence schemas and feature flags from source;
- trace state transitions and error branches from each user action to observable outcomes;
- inspect existing test selectors and accessibility/resource identifiers;
- execute bounded UI/state exploration and record newly reachable states;
- compare the discovered model with documentation and historical behavior.

Generate a coverage gap for any reachable production action without an expected outcome or assertion. Never invent product semantics from labels alone.

## Prove the tests

Before trusting new automation:

1. Run the case against the intended good state and confirm it passes.
2. Use a safe negative control: mock a failing response, invert one fixture, disable the required dependency, run against a known-bad artifact, or apply an isolated mutation.
3. Confirm the same case fails for the expected assertion and failure signature.
4. Remove the mutation/fault, rebuild if needed, and confirm it passes again.
5. Run the case at least three times when timing, concurrency, networking or UI synchronization is involved. Any inconsistent outcome is a flake and blocks release until fixed or explicitly accepted.

Never mutate the sole copy of a release candidate. Use an isolated build/worktree or injectable test boundary.

## Failure triage

Classify before editing:

- `product`: candidate behavior violates a confirmed requirement;
- `automation`: selector, fixture, assertion, timeout or harness is wrong;
- `environment`: device, service, account, network or OS state is invalid;
- `requirement`: expected behavior conflicts or is unknown;
- `flake`: outcome changes with identical candidate, fixture, environment and seed.

Correlate timestamps across UI, client, service, OS and device logs. Reduce the failure to the shortest deterministic trigger. Inspect the smallest dependency surface before changing code. Record the root-cause claim and evidence separately; do not infer a cause merely from a nearby log line.

## Repair discipline

- Add or strengthen the regression before the source fix when practical.
- Make the smallest source change that restores the confirmed behavior.
- Do not refactor, update dependencies or alter unrelated behavior while repairing a gate failure.
- Review the diff and map every changed production path back to direct, negative and historical tests.
- Rebuild with locked dependencies and isolated caches; any new bytes create a new frozen candidate.
- Test the final signed/notarized/packaged bytes for identity, installation, launch, upgrade and smoke behavior.

## Stopping conditions

Continue until `PASS` or a real external boundary prevents further action. A hard boundary includes unavailable required hardware/service, MFA, CAPTCHA, hardware-token PIN, an inaccessible secret, missing entitlement, or an authorization scope that would newly permit destructive or production-impacting actions.

If the same confirmed root cause survives three materially different, evidence-backed fix attempts, stop changing code and issue `BLOCK` with the attempts, diffs, evidence and safest next experiment. Do not loop blindly, hide the blocker or downgrade a required case.
