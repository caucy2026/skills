#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 --server-root PATH [--target-dir PATH] [--allow-network]" >&2
  exit 2
}

server_root=""
target_dir=""
offline="--offline"
while [ "$#" -gt 0 ]; do
  case "$1" in
    --server-root) [ "$#" -ge 2 ] || usage; server_root="$2"; shift 2 ;;
    --target-dir) [ "$#" -ge 2 ] || usage; target_dir="$2"; shift 2 ;;
    --allow-network) offline=""; shift ;;
    *) usage ;;
  esac
done

[ -n "$server_root" ] || usage
server_root="$(CDPATH= cd -- "$server_root" && pwd)"
manifest="$server_root/hbbc/Cargo.toml"
lockfile="$server_root/hbbc/Cargo.lock"
[ -f "$manifest" ] || { echo "Missing $manifest" >&2; exit 1; }
[ -f "$lockfile" ] || { echo "Missing $lockfile" >&2; exit 1; }
command -v cargo >/dev/null || { echo "cargo is required" >&2; exit 1; }
command -v file >/dev/null || { echo "file is required" >&2; exit 1; }
command -v strings >/dev/null || { echo "strings is required" >&2; exit 1; }
command -v shasum >/dev/null || { echo "shasum is required" >&2; exit 1; }
command -v cargo-zigbuild >/dev/null || { echo "cargo-zigbuild is required" >&2; exit 1; }

version="$(awk -F '"' '/^version = "/ { print $2; exit }' "$manifest")"
[ -n "$version" ] || { echo "Cannot read hbbc version" >&2; exit 1; }
lock_version="$(awk '/^\[\[package\]\]/{inside=0} /^name = "hbbc"$/{inside=1;next} inside && /^version = "/{split($0,part,"\"");print part[2];exit}' "$lockfile")"
[ "$version" = "$lock_version" ] || { echo "Cargo.toml version $version != Cargo.lock $lock_version" >&2; exit 1; }

if [ -z "$target_dir" ]; then
  target_dir="${TMPDIR:-/tmp}/kemi-hbbc-linux-$version"
fi
mkdir -p "$target_dir"
# Zig 的共享缓存出现过“索引仍在、对象文件已丢失”的并发损坏。正式构建必须
# 将全局/本地 Zig 缓存都固定到本次 hbbc 独立目标目录，不能复用 ~/.cache/zig。
export ZIG_GLOBAL_CACHE_DIR="$target_dir/.zig-global-cache"
export ZIG_LOCAL_CACHE_DIR="$target_dir/.zig-local-cache"
mkdir -p "$ZIG_GLOBAL_CACHE_DIR" "$ZIG_LOCAL_CACHE_DIR"

cd "$server_root"
echo "[1/6] format"
cargo fmt --manifest-path "$manifest" -- --check
echo "[2/6] tests"
cargo test --locked ${offline:+$offline} --manifest-path "$manifest" --target-dir "$target_dir"
echo "[3/6] clippy"
cargo clippy --locked ${offline:+$offline} --manifest-path "$manifest" --target-dir "$target_dir" --all-targets -- -D warnings
echo "[4/6] Linux release"
cargo zigbuild --locked ${offline:+$offline} --manifest-path "$manifest" --release \
  --target x86_64-unknown-linux-gnu.2.17 --target-dir "$target_dir"

binary="$target_dir/x86_64-unknown-linux-gnu/release/hbbc"
[ -x "$binary" ] || { echo "Missing release binary: $binary" >&2; exit 1; }
description="$(file "$binary")"
case "$description" in
  *"ELF 64-bit"*"x86-64"*) ;;
  *) echo "Unexpected binary: $description" >&2; exit 1 ;;
esac
glibc="$(strings "$binary" | sed -n 's/.*\(GLIBC_[0-9][0-9.]*\).*/\1/p' | sort -Vu | tail -n 1)"
if [ -n "$glibc" ] && [ "$(printf '%s\n%s\n' "$glibc" GLIBC_2.17 | sort -V | tail -n 1)" != "GLIBC_2.17" ]; then
  echo "GLIBC requirement too new: $glibc" >&2
  exit 1
fi

echo "[5/6] artifact"
echo "$description"
echo "max_glibc=${glibc:-none}"
shasum -a 256 "$binary"
echo "[6/6] complete"
echo "version=$version"
echo "binary=$binary"
