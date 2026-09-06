# Operating Cycle

## Default cadence

- Run a complete manager cycle every 30 minutes.
- Require each working member to publish a quantified acceptance ledger every 60 minutes.
- Treat completion, stopping, approval requests, failures, and requests for help as event-driven triggers; handle them without waiting for the next scheduled cycle.
- Treat two consecutive 30-minute windows without material evidence as stalled or falsely active only after checking raw evidence and reasonable long-running work.

Cadence is configurable, but a project-specific change must preserve the distinction between observation frequency and the threshold for declaring a stall.

## One complete 30-minute cycle

1. Reload the final goal, user requirements, member boundaries, current plan, previous review, and applicable project rules.
2. For each member, inspect the last 60 minutes and isolate the last 30-minute window:
   - raw messages and timestamps;
   - tool calls and command state;
   - file additions, edits, and deletions;
   - commits and working-tree changes;
   - build, test, runtime, protocol, database, screenshot, video, and artifact evidence;
   - session-file size and modification time;
   - blockers, approval requests, user intervention, and reasonable long-running jobs.
3. Classify the state using the table below.
4. Validate any completion claim against the end-state acceptance criteria.
5. Check same-route failure count and apply the three-attempt fuse.
6. Check whether the hourly acceptance ledger is due and valid.
7. Assign work only when intervention is justified.
8. Record decisions, evidence, open risks, daytime experiments, and the next-cycle focus.
9. Deliver the user-requested report. Routine notifications should remain quiet unless the user explicitly requested periodic reports.

## State classification

| State | Evidence standard | Manager action |
|---|---|---|
| `in_progress` | Material code, test, log, conclusion, or tool progress within two windows | Do not interrupt |
| `long_running` | Necessary command is still running and has credible progress/log evidence | Do not interrupt; inspect again next cycle |
| `stalled` | Two windows without evidence, after raw-log/file/process checks | Identify the gap and assign a changed, verifiable action |
| `idle_incomplete` | Member stopped while acceptance remains open | Immediately assign the best safe next task |
| `awaiting_acceptance` | Completion claimed but evidence is incomplete or unreviewed | Independently inspect or run acceptance |
| `verified_complete` | Every relevant criterion passed with reproducible evidence | Update the plan and assign the next goal or release the member |
| `blocked_external` | Requires unavailable user input, external state, or authority | Add a minimal daytime experiment; switch to independent work |
| `approval_blocked` | Waiting on an in-scope delegated approval | Approve within the configured boundary and require continuation |
| `release_blocked` | Final artifact identity or required validation is missing/failing | Prevent release until repaired and revalidated |

Only `verified_complete` means complete.

## Stop handling

When a member stops, resolve these questions from evidence or ask them once in a single message:

1. Is the end-state goal complete?
2. Where are the build, run, acceptance, regression, and artifact-identity records?
3. Is there truly no safe, authorized work left?
4. What action most directly advances the end state?
5. Why has that action not already started?

If incomplete work remains, issue one concrete assignment containing goal, scope, inputs, acceptance, evidence location, stop condition, and help route. Do not send generic “continue” or “status?” messages.

## Three-attempt fuse

An attempt has a hypothesis, an action, and an observable result. Repeating a command, changing wording, or producing no new evidence remains the same route.

After the third no-result attempt:

1. stop that route;
2. record all three hypotheses, actions, and results;
3. identify the remaining unknown;
4. request the smallest useful input from the most relevant person;
5. put user-dependent work into the daytime experiment queue;
6. switch immediately to the highest-priority independent task;
7. reopen only after new evidence or a materially different method appears.

## Unattended operation

When the user is absent, continue safe and reversible implementation, local builds, tests, static checks, offline evidence analysis, documentation, fixtures, diagnostics, and isolated experiments. Do not expand permissions or wait idly on a blocked item while independent work exists.

