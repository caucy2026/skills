# History and change mining

The plan must be derived from evidence, not a generic checklist.

## Build the history corpus

Read available task/chat summaries and turns, issue records, support reports, release notes, test reports, crash records and Git history. Inspect the actual diffs for the candidate range, including dependency and build-system changes. Treat titles and chat text as leads; confirm expected behavior from source, tests or an explicit product requirement before writing assertions.

Normalize each failure into:

- stable family ID and original bug/commit/task references;
- affected platforms, versions, device classes and accounts;
- pre-state and test data;
- precise trigger and timing;
- expected state transition or output;
- forbidden outcome and log signature;
- components and dependencies involved;
- automation layer best able to observe it;
- last known failing and passing artifact hashes.

Cluster records when they share the same user-visible failure or root subsystem. Keep variants for lifecycle, platform, input mode, permissions, installation state and timing. A later fix to the same family is evidence that the earlier regression gate was incomplete; strengthen that family instead of creating a disconnected one-off check.

## Change-impact cases

For every changed production file, map callers, state owners, platform conditionals, persistence/schema, IPC/protocol contracts, packaging and update paths. Generate:

1. a direct behavior case for the changed outcome;
2. a negative case proving unrelated supported behavior still works;
3. every historical regression family touching that dependency surface;
4. cross-platform cases wherever shared code or data formats changed;
5. install/upgrade/signature cases wherever packaging or version metadata changed.

Documentation-only changes need identity and consistency checks, not unrelated product retesting. Build-tool changes require reproducible build and artifact-equivalence checks. Do not expand into unrelated features without a dependency path.

## Permanent regression ledger

Store the ledger in the project test tree or release-quality directory and commit it with the automation. Never rely only on a chat transcript. Each release appends the candidate hash and result to existing IDs. A family can be retired only when the feature is removed, with source evidence and replacement behavior recorded.
