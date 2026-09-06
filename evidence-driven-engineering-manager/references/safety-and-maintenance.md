# Safety, Authorization, Release, and History

## Delegated approvals

Create an explicit project policy for what the manager may approve. When the owner has delegated approval for in-scope, reversible local actions, approve a waiting member immediately and state the exact action and boundary. Typical candidates are repository reads/edits, local builds, dependency installation, isolated tests, local development services, and necessary diagnostics.

Do not extrapolate that delegation to production or shared data, real/production credentials, payments, irreversible deletion, public communication, external publication, or scope expansion. Put those items in a user-attended queue.

Test credentials may appear in local commands, logs, or reports only when the project owner explicitly allows that practice. Do not create alarm solely from an explicitly authorized test credential, but keep production secrets and external publishing under the normal boundary.

## Release gate

Before any release action, identify the exact final artifact, source commit, version/build number, signature when applicable, hash, and location. Run every locally feasible build/install/unpack, cold-start, restart, critical-path, regression, configuration, cleanup, and rollback check against that exact artifact.

Debug builds, stale packages, temporary directories, source-code tests, and replacement artifacts cannot substitute for the proposed release artifact. If target hardware or environment is unavailable, record the precise exception, substitute checks, target validation plan, owner, and residual risk. “Locally unverified” is not “release ready.”

## Repository and backup checks

Periodically verify that each owned source/document/evidence directory is either tracked or intentionally excluded, the local repository has recoverable commits, and approved remotes contain the expected commits. Do not push merely because a remote exists; follow the project's publication authorization and sensitive-data rules. Report untracked or unpushed critical material with exact paths and recovery risk.

## Conversation-history threshold

Inspect history metadata every manager cycle. If one active history exceeds 300 MiB:

- do not modify it while the task is active, growing, ownership is unclear, or the format cannot be parsed reliably;
- only after the task stops or remains idle for two cycles and the file is stable, create a recoverable backup and verify its hash;
- preserve the most recent seven natural days of raw conversation in full;
- summarize and archive only content older than seven days, with time range, goals, decisions, completed work, evidence paths, unresolved issues, and next actions;
- rewrite through a temporary copy and atomic replacement only after validating format, time boundaries, ordering, readability, recoverability, and continued writes;
- if the active history still exceeds 300 MiB after archiving older content, stop and notify the user.

Never shorten the protected raw-history window to three days. Never delete recent raw history to meet the threshold.

