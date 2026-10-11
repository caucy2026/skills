# HBBC operations, backup and continuation

## Diagnose before mutation

Read-only preflight records host role, hbbc version/hash/config/database, hbbc state/PID/time/journal, hbbs/hbbr state/PID/time, public health/admin TLS/API, and active build/deploy/backup jobs. Do not infer production from local source, `BIN`, an upload or an old report. Do not print secrets or user rows.

## Formal release/deployment

Use `$kemi-hbbc-release`. Its maintained scripts provide:

- `build_hbbc_linux.sh`: format, locked tests, Clippy, Linux x86-64/GLIBC/version/SHA gates;
- `sync_bin_server.sh`: align administrator release files without hbbs/hbbr changes;
- `deploy_hbbc.sh --confirm-hbbc-only`: config validation, SQLite `.backup`, binary backup, atomic install, hbbc-only restart, health, rollback and unchanged hbbs/hbbr proof.

Binary update does not authorize production-config overwrite. Configuration mutation is separately reviewed, backed up, validated, atomically installed and independently reversible.

## Post-deployment acceptance

Choose observable checks for the change: auth/device lifecycle, presence/usage, donation/payment idempotency, real admin browser flow, download/static discovery and redirects, or bounded read-only hbbs monitor behavior. Preserve old-client/old-route checks when compatibility is involved.

Keep prior binary and consistent database backup through the observation window. A browser-login blocker is pending UI acceptance, not complete release.

## Git and documentation

Stage only reviewed hbbc source, intended deployment templates, public docs and release metadata. Reject production configuration, database/WAL/SHM, user exports, logs, tokens, keys, certificates, adjacent client or hbbs/hbbr changes.

Local commit, Git push, release publication, production deployment and private-doc update are separate facts. Verify the exact remote tree after push. Never merge public source and protected operations material for convenience.

If the workflow changes, update/validate the maintained skill source and sync it to the global installation. Skills contain methods, not credentials or private evidence.

## Continuation package

Leave one entry with: full objective/revisions; source repo/branch/HEAD/dirty state/version; timed production version/hash/health; completed evidence; unresolved acceptance/first failure; next three executable actions; active jobs not to restart; protected data/config/identity/rollback; authorization boundaries; stable evidence paths.

The teammate revalidates live state and continues without replaying completed SMS, payment, migration or deployment operations.

When available, protected docs commonly route as `00-overview`, `01-core-operations`, `02-cloud-resource`, `03-app-catalog`, `04-auth-device`, `05-presence-usage`, `06-donation-payment`, `07-client-integration`, `08-security-recovery`; `09-history` is historical only. Never copy secret assets or recovery packages into source, client bundles, public cloud or skills.
