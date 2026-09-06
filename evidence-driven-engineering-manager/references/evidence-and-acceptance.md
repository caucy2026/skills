# Evidence and Acceptance

## Evidence hierarchy

Use the strongest applicable evidence and label weaker evidence honestly:

1. final product used through the real user path;
2. target-environment or paired client/server runtime evidence;
3. protocol, persistence, replay, and restart evidence;
4. integration tests across real production code paths;
5. focused component tests;
6. successful build or static analysis;
7. code inspection or member claim.

Lower levels can prove intermediate work but cannot replace a required higher-level acceptance. Separate collection, static inference, component pass, protocol pass, final-product behavior, and overall completion.

## Acceptance record

Each acceptance candidate needs:

- requirement and exact scope;
- preconditions and artifact identity;
- expected result and measured actual result;
- executable steps or command;
- pass/fail/not-comparable/component-only/blocked verdict;
- logs, reports, screenshots, video, database state, protocol traces, hashes, or commit IDs;
- regression scope and result;
- unverified items and why they remain open.

A passing command without a checked result is not evidence. A generated file without provenance is not evidence. A screenshot proves only the visible frame unless runtime state and sequence are independently established.

## Hourly acceptance ledger

Every active member reports once per 60 minutes, then immediately continues working. If a necessary long command crosses the boundary, report the current phase, live evidence, and justified remaining estimate; do not wait for the command to finish before accounting for the hour.

Required fields:

- reporting window and end-state requirement;
- planned deliverables, actual completions, acceptance candidates, passes, failures, not-comparable cases, component-only cases, and blockers—each with counts and denominators;
- changed files and commits;
- commands/tests with passed/total and named failures;
- one row per acceptance candidate: ID, scenario, scope, criterion, expected, actual, verdict, evidence path, SHA-256;
- relevant end-to-end data flow and state transitions;
- reference media and final-artifact evidence when visual work is involved;
- generalization evidence and special-case scan when a reusable algorithm is required;
- newly excluded hypotheses and supporting evidence;
- same-route attempt count;
- one primary goal and one safe fallback for the next hour, each with acceptance criteria.

If zero items are acceptable, report `0/N` and the concrete evidence or hypotheses produced. Do not substitute “working,” “nearly done,” or a subjective percentage.

## Independent manager review

Do not accept the member's ledger at face value. Sample its commands, open its artifacts, inspect the cited images, check hashes when important, and compare the claim with the project contract. Mark unverifiable member statements as claims, not facts.

When a status summary conflicts with raw logs, files, builds, or running commands, prefer timestamped raw evidence. When evidence remains ambiguous, use `pending verification`; do not infer inactivity or issue an extreme low score.

## 100-point scoring

| Dimension | Points | What to judge |
|---|---:|---|
| User requirement execution | 35 | Correct goal, route, boundaries, and acceptance target |
| Effective output | 25 | Code, data, tests, artifacts, or new falsifiable conclusions |
| Acceptance closure | 20 | Build/run/real-use/regression/evidence completeness |
| Efficiency | 10 | Avoids idle time, blind repeats, and unnecessary reinvention |
| Risk and collaboration | 10 | Protects shared state, stays in scope, reports failures honestly |

100 means the relevant end state is fully and independently verified, not merely good progress. A reasonable failure with new evidence can score well. High activity that misses the user's target must lose requirement and closure points.

Scores below 60 require at least two independent negative evidence types. Scores below 20 require confirmation of at least three of: no raw event growth, no file change, no build/test, and no reasonable long task. Remind a low-scoring member only when the user has not intervened recently, the work is genuinely off-track, the reminder will not interrupt valid work, and the same reminder was not already sent.

## Facts and judgments

Every report distinguishes:

- confirmed facts;
- member statements not independently checked;
- manager judgments based on listed facts;
- unknowns that cannot support a negative inference.

If the manager made a wrong call, retract it promptly, show the corrected evidence and score, explain the cause and impact, and add a concrete prevention rule.

