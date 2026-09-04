---
name: kemi-hbbc-release
description: Build, package, deploy, verify, or roll back the KEMI hbbc HTTP/HTTPS, account, presence, usage, and payment service. Use for hbbc or legacy-spelled dhhc release work; do not use to modify, restart, or release RustDesk hbbs/hbbr.
---

# KEMI HBBC Release

Use this skill for the complete hbbc release path from source verification to production evidence. Treat “dhhc” as the historical/prototype spelling only after confirming the target source is the current `hbbc` crate.

## Route the task

1. Locate the repository by finding `hbbc/Cargo.toml`, `hbbc/src/main.rs`, and `deployment/kemi-rustdesk-hbbc.service`. Do not assume the author’s absolute local path on another machine.
2. Read [references/build-and-package.md](references/build-and-package.md) before compiling, versioning, or synchronizing a release directory.
3. Read [references/production-deployment.md](references/production-deployment.md) before any remote inspection, upload, deployment, restart, rollback, or production validation.
4. Use `scripts/build_hbbc_linux.sh` for a repeatable release build and `scripts/sync_bin_server.sh` when aligning the repository’s `BIN/server` package.
5. Use `scripts/deploy_hbbc.sh` only after the exact production target and hbbc-only deployment are authorized. Never place a password, private key, administrator token, SMS key, payment key, database, or user record in arguments, logs, release files, or Git.

## Preserve these invariants

- hbbc is independent from RustDesk `hbbs` and `hbbr`. Never replace, stop, restart, reconfigure, or reinstall hbbs/hbbr as part of hbbc work.
- Do not run the three-service/full-server installer for an ordinary hbbc update. Update the hbbc binary independently.
- Preserve the live `/etc/kemi-rustdesk/hbbc.json` unless the user explicitly requests a reviewed configuration change. A new binary release is not permission to overwrite production configuration.
- Upload to a unique temporary path, verify version and production-config compatibility, back up the SQLite database and current binary, then atomically install and restart only `kemi-rustdesk-hbbc.service`.
- Use SQLite’s `.backup` for the live account database. Do not make a raw copy of a live WAL database and call it a verified backup.
- Build with `--locked`. Prefer the repository’s toolchain/configuration and an isolated target directory. Try cached/offline dependencies first; if a locked dependency is missing, request network access and download only what the lockfile requires.
- The Linux release target is `x86_64-unknown-linux-gnu.2.17`. Reject a non-ELF, wrong-architecture, debug, or newer-than-GLIBC-2.17 artifact.
- Keep `hbbc/Cargo.toml` and the hbbc entry in `hbbc/Cargo.lock` on the same version. Do not silently invent or bump a version when the task is only diagnostic.
- Release documentation and checksum manifests are part of the artifact. Recompute hashes after the final binary and documentation are in place; never edit an existing hash to match an unverified file.
- Public skill/source repositories must contain no secrets. Hostnames, service names, ports, and public URLs are configuration, not credentials.

## Required local quality gate

For a formal release, the outcome is not “Cargo finished.” Require all of the following:

- formatting check;
- locked unit/integration tests;
- Clippy for all targets with warnings denied;
- optimized Linux cross-build;
- ELF x86-64 and GLIBC ceiling inspection;
- binary SHA-256;
- version consistency;
- release-directory checksum verification when `BIN/server` is in scope.

Run:

```bash
scripts/build_hbbc_linux.sh --server-root /path/to/RustDesk/server
```

The script prints the final binary path and evidence. It does not deploy or mutate `BIN/server`.

## Completion standard

Report each stage separately: source/version, tests, Clippy, Linux build, binary format/GLIBC, BIN synchronization, remote backup, production config check, hbbc restart, local health, public HTTP/HTTPS checks, and hbbs/hbbr unchanged. State the first causal failure and the exact next prerequisite. Do not call a release complete merely because upload or restart succeeded.
