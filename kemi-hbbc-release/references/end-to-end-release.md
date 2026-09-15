# End-to-end hbbc release

Use this workflow for a complete maintained-source-to-production release. `dhhc` is a legacy spelling; first confirm the executable and service are actually `hbbc`.

## 1. Freeze scope and evidence

- Record the repository, branch, dirty files, hbbc version, intended production host, and exact requested change.
- Preserve unrelated local changes. Do not silently include or revert them.
- State explicitly that hbbs/hbbr binaries, configuration, services, and databases are out of scope.
- A release request authorizes hbbc deployment only; it does not authorize publishing source or overwriting production configuration.

## 2. Build from the maintained source

Read `build-and-package.md`, then run `scripts/build_hbbc_linux.sh` with an isolated target directory. Accept the artifact only when formatting, locked tests, strict Clippy, Linux release build, ELF architecture, GLIBC ceiling, version, and SHA-256 all pass.

If the final source changes after the build—even for UI text or style—rebuild and replace the candidate. Never deploy an earlier artifact while reporting a later source state.

## 3. Establish a protected connection

Prefer an authorized SSH identity. When a password is required, open a visible SSH master session and let the administrator type the password; never receive or store it in chat, command arguments, files, logs, or skill content. Reuse the temporary control socket for preflight, upload, and deployment.

## 4. Read-only production preflight

Before upload, record:

- current production hbbc version;
- active state, PID, and activation timestamp of hbbc, hbbs, and hbbr;
- expected hbbc binary/config/database paths;
- whether hbbs/hbbr are already unhealthy.

Stop if host identity, paths, service names, or server role differ from the reviewed production contract.

## 5. Upload and validate before replacement

Upload to a unique `/tmp/hbbc.<timestamp>.new` path. On the server verify SHA-256, ELF/version, and run the incoming binary's `--check-config` against the existing production config as the service user. Do not upload a replacement JSON merely because the example config changed.

## 6. Back up and deploy only hbbc

Use `scripts/deploy_hbbc.sh --confirm-hbbc-only`. It must:

1. create a consistent SQLite `.backup` of the live hbbc account database;
2. preserve the current hbbc binary under a timestamped name;
3. atomically install the incoming binary;
4. restart only `kemi-rustdesk-hbbc.service`;
5. roll back the binary automatically if local health does not recover;
6. prove hbbs/hbbr state, PID, and activation timestamp did not change.

Never run a full three-service installer for a normal hbbc upgrade.

## 7. Validate observable behavior

- Confirm remote binary version and local HTTP health.
- Confirm public HTTP and HTTPS endpoints with certificate validation enabled.
- Inspect the new hbbc journal for startup loops, config, SQLite, TLS, SMS, or payment errors.
- For admin/UI work, log in normally and verify the actual page, click path, API result, empty/error state, and responsive layout.
- For large admin datasets, require independent server-side pagination for accounts, donations, devices, and usage records. Verify query, previous/next page, direct page jump, and a fixed visible success/failure notice after every save; do not accept a UI that embeds an unbounded or unrelated record list inside another page.
- For compatibility-sensitive work, exercise at least one unchanged old-client or old-route path. New optional configuration must have safe defaults.

## 8. Report and retain rollback data

Report build evidence, deployed SHA-256, backup paths, hbbc PID/version, public checks, and unchanged hbbs/hbbr evidence separately. If browser validation still requires administrator login, say that the binary is deployed but UI acceptance remains pending.

Keep the prior binary and database backup until the release has passed the agreed observation window. Do not call upload, compilation, or HTTP 200 alone a completed release.
