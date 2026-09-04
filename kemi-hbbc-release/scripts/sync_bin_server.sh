#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 --server-root PATH --bin-server PATH --binary PATH" >&2
  exit 2
}

server_root=""
bin_server=""
binary=""
while [ "$#" -gt 0 ]; do
  case "$1" in
    --server-root) [ "$#" -ge 2 ] || usage; server_root="$2"; shift 2 ;;
    --bin-server) [ "$#" -ge 2 ] || usage; bin_server="$2"; shift 2 ;;
    --binary) [ "$#" -ge 2 ] || usage; binary="$2"; shift 2 ;;
    *) usage ;;
  esac
done

[ -n "$server_root" ] && [ -n "$bin_server" ] && [ -n "$binary" ] || usage
server_root="$(CDPATH= cd -- "$server_root" && pwd)"
bin_server="$(CDPATH= cd -- "$bin_server" && pwd)"
binary="$(CDPATH= cd -- "$(dirname -- "$binary")" && pwd)/$(basename -- "$binary")"
[ -f "$server_root/hbbc/Cargo.toml" ] || { echo "Invalid server root" >&2; exit 1; }
[ -x "$binary" ] || { echo "Binary is missing or not executable: $binary" >&2; exit 1; }
[ -f "$bin_server/SHA256SUMS.txt" ] || { echo "Missing release checksum manifest" >&2; exit 1; }
case "$(file "$binary")" in
  *"ELF 64-bit"*"x86-64"*) ;;
  *) echo "Refusing non-Linux-x86_64 binary" >&2; exit 1 ;;
esac

version="$(awk -F '"' '/^version = "/ { print $2; exit }' "$server_root/hbbc/Cargo.toml")"
stamp="$(date +%Y%m%d-%H%M%S)"
backup_dir="$bin_server/candidates/hbbc-$version-$stamp"
mkdir -p "$backup_dir"
if [ -f "$bin_server/hbbc" ]; then
  cp -p "$bin_server/hbbc" "$backup_dir/hbbc-before-$version"
fi
install -m 0755 "$binary" "$bin_server/hbbc"

manifest_tmp="$(mktemp "${TMPDIR:-/tmp}/kemi-hbbc-sha.XXXXXX")"
trap 'rm -f "$manifest_tmp"' EXIT
find "$bin_server" -maxdepth 1 -type f ! -name 'SHA256SUMS.txt' ! -name '.DS_Store' -print0 \
  | sort -z \
  | while IFS= read -r -d '' file_path; do
      hash="$(shasum -a 256 "$file_path" | awk '{print $1}')"
      printf '%s  %s\n' "$hash" "$(basename -- "$file_path")"
    done > "$manifest_tmp"
install -m 0644 "$manifest_tmp" "$bin_server/SHA256SUMS.txt"
(cd "$bin_server" && shasum -a 256 -c SHA256SUMS.txt)
echo "version=$version"
echo "release_binary=$bin_server/hbbc"
echo "backup=$backup_dir"
