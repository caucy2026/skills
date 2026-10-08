# Safety, Authorization, Release, and History

## Delegated approvals

Create an explicit project policy for what the manager may approve. When the owner has delegated approval for in-scope, reversible local actions, approve a waiting member immediately and state the exact action and boundary. Typical candidates are repository reads/edits, local builds, dependency installation, isolated tests, local development services, and necessary diagnostics.

An explicit instruction such as “approve for me when approval is needed” establishes standing delegation within the owner's existing project scope. Record it in the project handoff and existing monitoring automation so it survives context compaction. Do not require the owner to repeat that approval during unattended work. This is conditional on the owner's delegation; the skill itself grants no permissions in other projects.

### Approval completion workflow

1. Identify the exact member, pending request, command or operation, target paths/endpoints, and side effects. An `awaiting approval` label alone is insufficient to approve an unknown action.
2. Match it against the standing delegation and any existing narrow authorization. Approve only covered actions. Preserve explicit release/compatibility gates even when the destination was previously authorized.
3. Use a callable approval API or permitted application control when available. If the workflow is conversational, send a precise scoped approval. Do not describe a chat response as application-level approval unless the tool actually accepted it.
4. Verify both the approval result and a new execution event or command outcome. Record detection time, action taken, approval outcome, resumed-work evidence and unresolved next step in the scoring ledger.
5. If the requested result was already obtained independently, pass the verified result to the member to avoid duplicate work; do not inject a forged tool response or assume its pending call has disappeared.
6. If approval capability is unavailable, a tool explicitly refuses access, or human confirmation is mandatory, keep the request blocked. Do not route around a refusal via another UI tool, shell automation, application database edits or global approval-setting changes. Explain the exact capability restriction rather than asking for the same project authorization again.
7. Notify the owner once with the concrete blocked request and necessary human action. Continue safe independent work where possible; recheck recovery on the next cycle. Do not repeatedly notify unchanged blockers or repeatedly send “agree” into the same suspended call. A changed request or newly actionable failure may warrant a new notice.

The manager's responsibility is timely detection, correct scoped approval, verified recovery and truthful escalation. It is not a promise to override system safeguards. Never claim “approved and resumed” when only a message was sent.

Do not extrapolate that delegation to production or shared data, real/production credentials, payments, irreversible deletion, public communication, external publication, or scope expansion. Put those items in a user-attended queue.

Test credentials may appear in local commands, logs, or reports only when the project owner explicitly allows that practice. Do not create alarm solely from an explicitly authorized test credential, but keep production secrets and external publishing under the normal boundary.

## Release gate

Before any release action, identify the exact final artifact, source commit, version/build number, signature when applicable, hash, and location. Run every locally feasible build/install/unpack, cold-start, restart, critical-path, regression, configuration, cleanup, and rollback check against that exact artifact.

Debug builds, stale packages, temporary directories, source-code tests, and replacement artifacts cannot substitute for the proposed release artifact. If target hardware or environment is unavailable, record the precise exception, substitute checks, target validation plan, owner, and residual risk. “Locally unverified” is not “release ready.”

## Repository and backup checks

Periodically verify that each owned source/document/evidence directory is either tracked or intentionally excluded, the local repository has recoverable commits, and approved remotes contain the expected commits. Do not push merely because a remote exists; follow the project's publication authorization and sensitive-data rules. Report untracked or unpushed critical material with exact paths and recovery risk.

## Conversation-history threshold

Inspect history metadata every manager cycle. If one active history exceeds 300 MiB:

- treat the size only as a storage-maintenance signal, never as a model-context or token measurement;
- do not edit, truncate, replace, or delete Codex-managed session or rollout files to simulate context compaction;
- do not parse, synthesize, or depend on opaque/native compacted items;
- do not modify any active or growing history;
- create a recoverable external backup only when the owner requested archival and the task is stopped; verify the decompressed hash;
- write a separate handoff containing goals, decisions, completed work, evidence paths, unresolved issues, next actions, permissions, and release gates;
- use only the product's supported native compaction mechanism to reduce model context;
- if native compaction fails, apply the three-attempt fuse and request explicit authorization to create a new task from the handoff rather than repeatedly retrying or rewriting internal files;
- prove recovery with a new turn that reads the handoff and produces a real execution event. File size, valid JSON, a preserved last record, or a backup hash cannot prove task recovery.

Preservation windows such as seven days govern external archival policy only. They do not authorize mutation of the product's active internal session store.
