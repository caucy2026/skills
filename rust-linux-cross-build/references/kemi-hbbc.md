# KEMI HBBC verified example

Use this reference only when the target is the KEMI `hbbc` service. The generic skill does not replace `kemi-hbbc-release`; that skill remains authoritative for HBBC packaging and production deployment.

## Source and target

Locate rather than assume the developer's absolute path:

```text
server/hbbc/Cargo.toml
server/hbbc/Cargo.lock
server/hbbc/src/main.rs
server/deployment/kemi-rustdesk-hbbc.service
```

The maintained Linux target is:

```text
x86_64-unknown-linux-gnu.2.17
```

Expected artifact:

```text
<isolated-target>/x86_64-unknown-linux-gnu/release/hbbc
```

## Required command

Use the installed release skill's helper rather than rewriting its commands:

```bash
/path/to/kemi-hbbc-release/scripts/build_hbbc_linux.sh \
  --server-root /path/to/RustDesk/server \
  --target-dir /path/to/isolated-build-directory
```

The helper performs:

- formatting check;
- locked tests;
- strict locked Clippy;
- `cargo zigbuild --locked --release` for GLIBC 2.17;
- ELF x86-64 and GLIBC ceiling checks;
- version consistency and SHA-256 evidence.

Use network mode only if the offline attempt identifies a missing locked dependency. Keep target and Zig caches in the isolated build directory.

## HBBC boundaries

- Building HBBC does not authorize deployment.
- A normal HBBC release never rebuilds, replaces, stops, restarts, or reconfigures hbbs/hbbr.
- `BIN/server/hbbc` is the stable administrator release copy; compiler output is not automatically synchronized there.
- Production `/etc/kemi-rustdesk/hbbc.json`, SQLite data, payment/SMS keys, admin credentials, and TLS keys are never build inputs or Git artifacts.
- Production deployment must upload to a unique temporary path, validate against the existing config, use SQLite `.backup`, preserve the old binary, atomically replace only hbbc, and restart only `kemi-rustdesk-hbbc.service`.

## Expected handoff

Provide the hbbc version, source commit, fmt/test/Clippy outcomes, ELF/GLIBC evidence, artifact path/size/SHA-256, and clearly state whether `BIN/server` synchronization or production deployment has or has not occurred.
