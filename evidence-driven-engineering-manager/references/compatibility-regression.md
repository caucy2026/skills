# Compatibility and Regression Control

Read this reference when a change affects shared rendering, resource resolution, protocol handling, state machines, persistence, lifecycle ownership, common data structures, or multiple features. Its purpose is to prevent the oscillation where fixing case A breaks case B, and fixing B revives A.

## Declare the blast radius before editing

Record the shared entry point, state owner, direct callers, indirect consumers, format or protocol boundaries, affected feature families, previously accepted examples, and rollback point. If the blast radius is unknown, establish it with call-site search, static analysis, runtime tracing, or characterization tests before changing behavior.

When automated coverage is absent, capture a pre-change baseline for already accepted behavior. Preserve inputs, outputs, state transitions, timing, protocol evidence, screenshots or video when relevant, artifact identity, and hashes. A global change without a pre-change baseline cannot claim compatibility.

## Require a compatibility matrix

Every global change must test three groups:

1. the current failing case;
2. every previously accepted case in the affected feature families;
3. at least one materially different counterexample or boundary case.

Expand the matrix according to the blast radius. For a renderer, this may include geometry, models, equipment, movement, UI, different effect topologies, concurrent actors, and creation-to-destruction lifecycle. For a backend, it may include login, movement, combat, AI, persistence, replay/restart, inventory, story, and the affected real-client path. Shared client/server contracts must correlate request, authoritative mutation, persistence or audit, response, client state, and visible result under the same transaction identity.

Report exact passed/total counts, commands, expected and actual results, verdicts, evidence paths, and hashes. Passing only the new test while the affected historical suite is unexecuted is `current-case-pass / compatibility-open`, not completion.

## Turn every accepted fix into a permanent check

Each accepted defect fix must add a regression test, replay fixture, or stable acceptance probe that fails before the fix and passes after it. Add it to the normal affected-suite command so future changes run it automatically.

Do not delete, skip, weaken, or convert a strict assertion into a process-exit-only check merely to land a new change. If an old test is genuinely obsolete, require changed product requirements or stronger replacement evidence, impact analysis, and explicit review before removing it.

For visual behavior, retain the authoritative reference index and standardized final-artifact captures. Machine checks support but do not replace direct comparison of geometry, materials, alpha, attachments, animation, particle count and trajectory, timing, occlusion, UI, and interaction. A visible regression in a previously accepted condition fails compatibility.

## Stop A/B oscillation

When fixing A breaks B:

- on the first occurrence, put A and B into one command or matrix that must run after every subsequent edit;
- on the second occurrence, stop toggling local conditions and investigate the shared invariant, state owner, transaction identity, lifecycle, authoritative data source, or missing abstraction;
- on the third occurrence without net improvement, apply the three-attempt fuse: forbid another similar patch, preserve the three diffs and results, ask for focused help, and switch to a different method such as a minimal reproduction, invariant-based redesign, or state isolation.

Net improvement means the total failure count decreases without reviving an accepted case. Moving the failure from A to B is not new evidence and must not reset the attempt counter.

## Merge, push, and release gate

A global change may be accepted, merged, pushed, or released only when:

- blast radius and pre-change baseline are recorded;
- the current case, affected historical cases, counterexamples, and required full suite pass;
- the intended final artifact passes every feasible real-path check;
- the compatibility matrix has zero newly introduced failures;
- forbidden sample-specific branches are absent;
- code, tests, documentation, evidence, denominators, hashes, and rollback point agree.

For collaborative repositories, also verify that the change set does not include another member's unrelated work. If any gate fails, repair and rerun the same matrix before moving to the next feature.

## Required ledger fields

For global changes, add these fields to the acceptance ledger:

- blast radius;
- pre-change baseline;
- compatibility matrix passed/total;
- newly introduced historical failures;
- A/B oscillation count;
- final-artifact real-path status;
- rollback point.

Missing fields keep the change at `compatibility-open`.
