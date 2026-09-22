#!/bin/bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 /absolute/path/package.zip" >&2
  exit 64
fi

archive=$1
if [[ $archive != /* || ! -f $archive || $archive != *.zip ]]; then
  echo "error: supply an existing absolute .zip path" >&2
  exit 64
fi

work_dir=$(mktemp -d /tmp/kemi-market-verify.XXXXXX)
cleanup() {
  rm -rf "$work_dir"
}
trap cleanup EXIT

bytes=$(stat -f '%z' "$archive")
sha256=$(shasum -a 256 "$archive" | awk '{print $1}')
ditto -x -k "$archive" "$work_dir/unpacked"

apps=()
while IFS= read -r -d '' app; do
  apps+=("$app")
done < <(find "$work_dir/unpacked" -mindepth 1 -maxdepth 1 -type d -name '*.app' -print0)

if [[ ${#apps[@]} -ne 1 ]]; then
  echo "error: expected exactly one top-level .app in archive, found ${#apps[@]}" >&2
  exit 65
fi

app=${apps[0]}
app_name=$(basename "$app")
executable=$(plutil -extract CFBundleExecutable raw "$app/Contents/Info.plist")
binary="$app/Contents/MacOS/$executable"

if [[ ! -x $binary ]]; then
  echo "error: bundle executable is missing or not executable: $binary" >&2
  exit 66
fi

codesign --verify --deep --strict --verbose=2 "$app"
xcrun stapler validate "$app"
spctl -a -vv -t exec "$app"
architectures=$(lipo -archs "$binary")

printf 'archive=%s\n' "$archive"
printf 'bytes=%s\n' "$bytes"
printf 'sha256=%s\n' "$sha256"
printf 'bundle=%s\n' "$app_name"
printf 'executable=%s\n' "$executable"
printf 'architectures=%s\n' "$architectures"
printf 'result=PASS\n'
