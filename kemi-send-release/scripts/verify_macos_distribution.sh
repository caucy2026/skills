#!/bin/bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "usage: $0 /absolute/path/package.zip [repository-root]" >&2
  exit 64
fi

archive=$1
repo_root=${2:-$PWD}
if [[ $archive != /* || ! -f $archive || $archive != *.zip ]]; then
  echo "error: supply an existing absolute .zip path" >&2
  exit 64
fi
if [[ ! -d $repo_root/.tools ]]; then
  echo "error: repository root must contain .tools: $repo_root" >&2
  exit 64
fi

if unzip -Z1 "$archive" | grep -E '(^|/)\._|^__MACOSX/' >/dev/null; then
  echo "error: archive contains AppleDouble metadata" >&2
  exit 65
fi

work_dir=$(mktemp -d "$repo_root/.tools/macos-distribution-verify.XXXXXX")
unpacked="$work_dir/unpacked"
mkdir -p "$unpacked"
/usr/bin/unzip -q "$archive" -d "$unpacked"

apps=()
while IFS= read -r -d '' app; do
  apps+=("$app")
done < <(find "$unpacked" -mindepth 1 -maxdepth 2 -type d -name '*.app' -print0)
if [[ ${#apps[@]} -ne 1 ]]; then
  echo "error: expected exactly one top-level .app, found ${#apps[@]}" >&2
  exit 66
fi

app=${apps[0]}
plist="$app/Contents/Info.plist"
bundle_id=$(/usr/libexec/PlistBuddy -c 'Print :CFBundleIdentifier' "$plist")
version=$(/usr/libexec/PlistBuddy -c 'Print :CFBundleShortVersionString' "$plist")
build=$(/usr/libexec/PlistBuddy -c 'Print :CFBundleVersion' "$plist")
executable=$(/usr/libexec/PlistBuddy -c 'Print :CFBundleExecutable' "$plist")
binary="$app/Contents/MacOS/$executable"

[[ $bundle_id == org.kemi.send ]] || { echo "error: unexpected bundle id: $bundle_id" >&2; exit 67; }
[[ -x $binary ]] || { echo "error: missing executable: $binary" >&2; exit 68; }

/usr/bin/codesign --verify --deep --strict --verbose=2 "$app"
/usr/bin/xcrun stapler validate "$app"
/usr/sbin/spctl -a -vv -t exec "$app"
architectures=$(/usr/bin/lipo -archs "$binary")
[[ " $architectures " == *" x86_64 "* && " $architectures " == *" arm64 "* ]] || {
  echo "error: expected x86_64 and arm64, got: $architectures" >&2
  exit 69
}

bytes=$(stat -f '%z' "$archive")
sha256=$(shasum -a 256 "$archive" | awk '{print $1}')
printf 'archive=%s\nbytes=%s\nsha256=%s\napp=%s\nbundle_id=%s\nversion=%s\nbuild=%s\narchitectures=%s\nwork_dir=%s\nresult=PASS\n' \
  "$archive" "$bytes" "$sha256" "$app" "$bundle_id" "$version" "$build" "$architectures" "$work_dir"
