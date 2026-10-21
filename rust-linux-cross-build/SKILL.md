---
name: rust-linux-cross-build
description: Build a release Rust executable on a developer machine for a specified Linux architecture and GLIBC baseline, then verify tests, lint, ELF format, dynamic dependencies, version, and SHA-256 before handing it to deployment. Use for “本地编译Linux能跑的程序”, macOS-to-Linux Rust cross-builds, or reproducible Linux server binary preparation; do not use to deploy, restart services, or build Flutter/Linux desktop bundles.
---

# Rust Linux Cross-Build

Produce one traceable Linux release binary from reviewed Rust source. Compilation success alone is insufficient: the artifact must match the target CPU, libc baseline, package version, and current source.

## Route the task

1. Locate the maintained Rust manifest and repository instructions. Record the source commit, dirty files, package name/version, target server architecture, libc family/version, and expected executable name.
2. Prefer a project-provided build script when it already fixes the target, linker, caches, tests, and acceptance checks. Inspect it before running; do not invent a parallel build path merely because Cargo can compile directly.
3. For selecting native Linux versus local cross-build, or diagnosing linker/runtime compatibility, read [references/build-workflow.md](references/build-workflow.md).
4. For KEMI HBBC, read [references/kemi-hbbc.md](references/kemi-hbbc.md) and use the existing `kemi-hbbc-release` build helper. Do not modify or restart hbbs/hbbr.
5. Stop after producing and verifying the artifact unless the user separately requested deployment. Deployment authorization does not follow automatically from a build request.

## Required build discipline

- Preserve unrelated source changes. Freeze the exact source state used by the binary; any source or build-input change invalidates the prior artifact.
- Use `cargo build/test/clippy --locked`. Do not update dependencies during a release build.
- Use an isolated target/cache directory. Respect the machine's local environment rules for build storage; do not hard-code another developer's disk path.
- Try the project's cached/offline route first when it is established. Enable network only for missing locked dependencies, without changing the lockfile.
- On macOS or a mismatched Linux host, prefer `cargo-zigbuild` with an explicit target such as `x86_64-unknown-linux-gnu.2.17`. A plain `cargo build --target ...` is acceptable only when the required cross linker and native libraries are already configured and verified.
- Do not claim a musl binary and a glibc binary are interchangeable. Match the server contract.
- Never copy production secrets, databases, private keys, tokens, or host configuration into the build context or artifact package.

## Quality gate

Unless the project has a stricter gate, require from the same frozen source:

1. `cargo fmt --check`.
2. Locked unit/integration tests for the relevant workspace/package.
3. Locked Clippy for relevant targets with warnings denied.
4. Optimized release build for the explicit Linux target.
5. `file` reports the requested Linux ELF class and architecture.
6. The highest referenced `GLIBC_*` symbol is no newer than the agreed server baseline, or the artifact is intentionally static/musl and verified as such.
7. Dynamic dependencies are expected and resolvable; reject accidental host-specific paths or missing libraries.
8. The binary reports the intended version on a compatible Linux environment when it supports `--version`.
9. Record size and SHA-256.
10. Keep command logs and a short build-evidence record without secrets.

If the developer host cannot execute the cross-built ELF, use a matching Linux runner, container, or the target server for read-only `--version`/smoke verification. Do not treat “cannot execute on macOS” as a build failure, and do not skip ELF/GLIBC inspection.

## Handoff

Report separately:

- source repository, branch, full commit, and dirty inputs;
- package/version and exact build command or project script;
- host and target triples;
- fmt, test, and Clippy results;
- ELF architecture, libc baseline, and dynamic-dependency result;
- artifact absolute path, byte size, and SHA-256;
- runtime smoke-test environment and result;
- anything not yet built, signed, deployed, or verified.

Do not label an upload, service restart, or HTTP 200 as part of this skill's success. Those belong to the target project's deployment/release skill.
