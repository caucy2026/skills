# hbbc source and skill backup

Use this after the hbbc source, tests, release artifact, deployment evidence, and documentation agree on one version.

## Keep repositories separate

- hbbc source and public release documentation belong to the server repository containing `hbbc/Cargo.toml`.
- the reusable `kemi-hbbc-release` skill belongs to its dedicated skills repository.
- production configuration, administrator credentials, SQLite data, SMS/payment keys, SSH control sockets, and customer records belong in neither repository.
- unrelated hbbs/hbbr or client working-tree changes must not be staged merely because they are adjacent.

## hbbc source backup gate

Before committing, record the branch, remote, dirty file list, final hbbc version, binary SHA-256, and deployed production version. Stage only reviewed hbbc files, deployment templates explicitly changed by the release, public docs, and intended `BIN/server` release metadata.

Inspect the staged diff and reject the backup when it contains:

- production JSON or secret files;
- account databases, WAL/SHM files, user exports, logs, tokens, passwords, private keys, or certificates;
- unrelated deletions or modifications already present in the shared worktree;
- a Cargo version that differs from the deployed binary or release documentation.

Commit with a versioned, behavior-oriented message. Push only after verifying the exact remote and branch. A local commit is not a cloud backup; report commit and push separately.

## Skill synchronization gate

When the release exposes a repeatable failure or changes the build/deploy/backup workflow, update the maintained skill source in the skills repository first. Validate it with the skill validator, inspect its staged diff, commit only that skill directory, push it, and then synchronize the validated directory into the local Codex skills installation.

The installed skill and GitHub copy must contain the same `SKILL.md`, references, scripts, and executable modes. Verify with a recursive diff after synchronization. Never copy secrets or production evidence into the skill.

## Completion evidence

Report these independently:

- server source commit and pushed remote branch;
- skill commit and pushed remote branch;
- installed-skill validation and repository/install diff result;
- release artifact version and SHA-256;
- production hbbc version and health;
- hbbs/hbbr unchanged evidence.
