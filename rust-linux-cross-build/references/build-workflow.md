# Rust Linux binary build workflow

## 1. Discover the target contract

Before choosing a command, determine:

```text
manifest/package          Which Cargo.toml and package produce the executable?
binary name               Which [[bin]] or src/main.rs output is expected?
CPU architecture          x86_64, aarch64, armv7, etc.
libc                      glibc/gnu or musl?
minimum runtime           e.g. GLIBC 2.17, Ubuntu 20.04, Debian 12
native dependencies       OpenSSL, SQLite, ALSA, GTK, C/C++ libraries, protoc, etc.
release features          default, no-default-features, explicit feature list
version source            Cargo.toml, generated file, Git tag, or build metadata
```
Read the project's build scripts, CI workflow, lockfile, toolchain file, `.cargo/config*`, and recent successful build record. Reuse the established route when it matches the current target.

## 2. Choose the build environment

### Native Linux

Use when the host distribution and architecture are equal to or older than the deployment baseline. Native builds are simplest, but building on a newer distro may introduce a GLIBC requirement the older server cannot satisfy.

### macOS/Windows cross-build with Zig

Use `cargo-zigbuild` when a gnu Linux executable must be produced locally and the project supports it. The target's libc suffix establishes the maximum baseline:

```bash
cargo zigbuild --locked --release \
  --target x86_64-unknown-linux-gnu.2.17 \
  --manifest-path path/to/Cargo.toml \
  --target-dir /path/to/isolated-target
```

Do not omit the `.2.17` suffix when GLIBC 2.17 compatibility is an actual requirement. Keep Zig global/local caches isolated if the project has experienced stale shared-cache failures.

### musl

Choose a `*-unknown-linux-musl` target only when the project and its native dependencies support it and the deployment contract permits it. Static linking can simplify portability, but it changes DNS, TLS, allocator, plugin, and native-library behavior; it is not an automatic replacement for a gnu build.

### Container or CI runner

Use when the developer machine cannot supply a reliable linker/native dependency set. A container or runner is a build environment, not the production server. Preserve the same frozen source, lockfile, target, evidence, and artifact checks.

## 3. Recommended gate commands

Adapt package/workspace flags to the project:

```bash
cargo fmt --manifest-path path/to/Cargo.toml -- --check

cargo test --locked \
  --manifest-path path/to/Cargo.toml \
  --target-dir /path/to/isolated-target

cargo clippy --locked \
  --manifest-path path/to/Cargo.toml \
  --target-dir /path/to/isolated-target \
  --all-targets -- -D warnings

cargo zigbuild --locked --release \
  --manifest-path path/to/Cargo.toml \
  --target x86_64-unknown-linux-gnu.2.17 \
  --target-dir /path/to/isolated-target
```

If tests cannot run for the cross target on the developer host, run tests natively with the same source and locked dependencies, then cross-build the release artifact. Record this distinction.

## 4. Artifact verification

Example inspection on macOS/Linux with GNU-compatible tools available:

```bash
file /path/to/binary
sha256sum /path/to/binary      # Linux
shasum -a 256 /path/to/binary  # macOS
```

Inspect the highest GLIBC symbol using an available ELF reader, for example:

```bash
readelf --version-info /path/to/binary \
  | grep -o 'GLIBC_[0-9.]*' \
  | sort -V -u \
  | tail -1
```

Also inspect the interpreter and dependencies with `readelf -l/-d`, `objdump -p`, or `ldd` on a matching Linux environment. Never execute `ldd` on an untrusted binary; release artifacts must originate from the reviewed build.

Typical rejection cases:

- Mach-O, PE, wrong ELF class, or wrong CPU architecture;
- debug profile or missing expected optimization/build flags;
- `GLIBC_*` newer than the server baseline;
- missing dynamic library or accidental dependency on a developer-only absolute path;
- version mismatch between Cargo metadata, binary output, and release notes;
- artifact generated before the final source change;
- lockfile changed unexpectedly during the build.

## 5. Runtime smoke test

On a compatible disposable Linux environment or through a read-only target-server check:

```bash
/path/to/binary --version
/path/to/binary --help
```

For a service, prefer its config-validation or dry-run mode. Do not bind production ports, modify the live database, replace the running executable, or restart services under a build-only request.

## 6. Evidence record

Record at minimum:

```text
timestamp/timezone
source repo + branch + full commit
dirty file list included/excluded
package and version
host OS/architecture
Rust/Cargo/Zig/cargo-zigbuild versions
exact build command
test and Clippy result
target triple and libc baseline
artifact path, bytes, SHA-256
file/readelf/dependency result
runtime smoke result and environment
```
