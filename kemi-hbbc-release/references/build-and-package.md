# Build and package hbbc

## Locate and inspect

The current KEMI layout normally looks like:

```text
RustDesk/
├── server/
│   ├── hbbc/Cargo.toml
│   ├── hbbc/Cargo.lock
│   ├── hbbc/src/main.rs
│   ├── deployment/hbbc.example.json
│   └── deployment/kemi-rustdesk-hbbc.service
└── BIN/server/
    ├── hbbc
    ├── BUILD-INFO.md
    ├── README-HBBC-配置与部署.md
    └── SHA256SUMS.txt
```

Do not confuse:

- `server/hbbc`: maintained Rust source;
- `server/hbbc/target` or an isolated target directory: compiler output;
- `BIN/server/hbbc`: stable release copy for administrators;
- `/opt/kemi-rustdesk-server/bin/hbbc`: production binary;
- hbbs/hbbr: separate RustDesk signaling and relay services.

Before edits, inspect repository instructions, `git status`, the hbbc package version, relevant docs, and existing release checksums. Preserve unrelated working-tree changes.

## Version consistency

The package version is authoritative:

```text
hbbc/Cargo.toml  -> [package].version
hbbc/Cargo.lock  -> package name="hbbc", matching version
```

When a requested release requires a version bump, update both through a normal Cargo-compatible edit and verify the compiled program reports the same version with `hbbc --version` on Linux. Cross-compiled Linux binaries cannot execute on macOS; use the remote preflight or a matching Linux runner for that check.

## Formal build sequence

Use the bundled build script:

```bash
/path/to/kemi-hbbc-release/scripts/build_hbbc_linux.sh \
  --server-root /path/to/RustDesk/server
```

Default target directory:

```text
/private/tmp/kemi-hbbc-linux-<version>
```

Override with `--target-dir`. Use `--allow-network` only after an offline run proves a locked dependency is missing and network access is authorized.

The sequence is:

```bash
cargo fmt --manifest-path hbbc/Cargo.toml -- --check
cargo test --locked --offline --manifest-path hbbc/Cargo.toml --target-dir <target>
cargo clippy --locked --offline --manifest-path hbbc/Cargo.toml --target-dir <target> --all-targets -- -D warnings
cargo zigbuild --locked --offline --manifest-path hbbc/Cargo.toml --release \
  --target x86_64-unknown-linux-gnu.2.17 --target-dir <target>
```

The online mode removes only `--offline`; it retains `--locked`.

## Artifact acceptance

Expected output:

```text
<target>/x86_64-unknown-linux-gnu/release/hbbc
```

Accept only when:

- `file` identifies an ELF 64-bit x86-64 executable;
- the maximum referenced `GLIBC_*` symbol is no newer than `GLIBC_2.17`;
- the file is non-empty and executable;
- SHA-256 is recorded;
- tests and strict Clippy passed from the same source tree;
- no secrets or production database were embedded or copied.

The Zig linker may emit a known deprecated optimization-setting warning. Record it, but do not misreport it as a failed build when the command exits successfully. Any Rust warning under the strict Clippy gate is a failure.

## Synchronize BIN/server

First update the versioned release notes and `BUILD-INFO.md`. Then run:

```bash
/path/to/kemi-hbbc-release/scripts/sync_bin_server.sh \
  --server-root /path/to/RustDesk/server \
  --bin-server /path/to/RustDesk/BIN/server \
  --binary <target>/x86_64-unknown-linux-gnu/release/hbbc
```

The script:

1. validates the source version and Linux binary;
2. saves the prior stable binary under `BIN/server/candidates/hbbc-<version>-<timestamp>/`;
3. installs the new binary as stable `BIN/server/hbbc`;
4. regenerates `SHA256SUMS.txt` for top-level release files;
5. verifies every checksum.

It does not copy or modify hbbs/hbbr. If documentation names a different hbbc version, fix the documentation before declaring the directory aligned.

## Source backup

Commit only reviewed hbbc-related source, deployment templates, public docs, and release metadata. Keep local/private credentials and production data outside Git. Before pushing, show the exact branch, remote, commit, and file list; do not bundle unrelated client or server changes merely because they share a parent directory.
