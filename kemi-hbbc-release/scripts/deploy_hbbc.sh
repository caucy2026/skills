#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 --binary PATH [--host USER@HOST] [--port PORT] --confirm-hbbc-only" >&2
  exit 2
}

binary=""
host="root@119.96.24.110"
port="39281"
confirmed="false"
while [ "$#" -gt 0 ]; do
  case "$1" in
    --binary) [ "$#" -ge 2 ] || usage; binary="$2"; shift 2 ;;
    --host) [ "$#" -ge 2 ] || usage; host="$2"; shift 2 ;;
    --port) [ "$#" -ge 2 ] || usage; port="$2"; shift 2 ;;
    --confirm-hbbc-only) confirmed="true"; shift ;;
    *) usage ;;
  esac
done

[ -n "$binary" ] || usage
[ "$confirmed" = "true" ] || { echo "Explicit --confirm-hbbc-only is required" >&2; exit 2; }
binary="$(CDPATH= cd -- "$(dirname -- "$binary")" && pwd)/$(basename -- "$binary")"
[ -x "$binary" ] || { echo "Binary is missing or not executable: $binary" >&2; exit 1; }
case "$(file "$binary")" in
  *"ELF 64-bit"*"x86-64"*) ;;
  *) echo "Refusing non-Linux-x86_64 binary" >&2; exit 1 ;;
esac
glibc="$(strings "$binary" | sed -n 's/.*\(GLIBC_[0-9][0-9.]*\).*/\1/p' | sort -Vu | tail -n 1)"
if [ -n "$glibc" ] && [ "$(printf '%s\n%s\n' "$glibc" GLIBC_2.17 | sort -V | tail -n 1)" != "GLIBC_2.17" ]; then
  echo "GLIBC requirement too new: $glibc" >&2
  exit 1
fi

stamp="$(date +%Y%m%d-%H%M%S)"
remote_tmp="/tmp/hbbc.$stamp.new"
local_sha="$(shasum -a 256 "$binary" | awk '{print $1}')"
echo "local_sha256=$local_sha"

preflight="$(ssh -p "$port" "$host" '
  printf "version="; /opt/kemi-rustdesk-server/bin/hbbc --version
  printf "hbbc="; systemctl is-active kemi-rustdesk-hbbc.service
  printf "hbbs="; systemctl is-active kemi-rustdesk-hbbs.service
  printf "hbbr="; systemctl is-active kemi-rustdesk-hbbr.service
')"
printf '%s\n' "$preflight"
before_hbbs="$(printf '%s\n' "$preflight" | awk -F= '$1=="hbbs"{print $2;exit}')"
before_hbbr="$(printf '%s\n' "$preflight" | awk -F= '$1=="hbbr"{print $2;exit}')"
[ -n "$before_hbbs" ] && [ -n "$before_hbbr" ] || { echo "Cannot read hbbs/hbbr preflight state" >&2; exit 1; }
scp -P "$port" "$binary" "$host:$remote_tmp"

ssh -p "$port" "$host" bash -s -- "$remote_tmp" "$stamp" "$local_sha" "$before_hbbs" "$before_hbbr" <<'REMOTE'
set -euo pipefail
incoming="$1"
stamp="$2"
expected_sha="$3"
before_hbbs="$4"
before_hbbr="$5"
binary="/opt/kemi-rustdesk-server/bin/hbbc"
config="/etc/kemi-rustdesk/hbbc.json"
database="/var/lib/kemi-rustdesk-server/hbbc-accounts.sqlite3"
service="kemi-rustdesk-hbbc.service"
backup="$binary.before-$stamp"
db_backup="$database.before-$stamp"

[ -f "$binary" ] && [ -f "$config" ] && [ -f "$database" ]
actual_sha="$(sha256sum "$incoming" | awk '{print $1}')"
[ "$actual_sha" = "$expected_sha" ] || { echo "Uploaded SHA-256 mismatch" >&2; exit 1; }
chmod 0755 "$incoming"
"$incoming" --version
runuser -u kemi-rustdesk -- "$incoming" --config "$config" --check-config
command -v sqlite3 >/dev/null || { echo "sqlite3 is required for a consistent online backup" >&2; exit 1; }
sqlite3 "$database" ".backup '$db_backup'"
test -s "$db_backup"
cp -p "$binary" "$backup"
install -o root -g root -m 0755 "$incoming" "$binary.next"
mv "$binary.next" "$binary"

rollback() {
  echo "New hbbc failed; rolling back binary" >&2
  install -o root -g root -m 0755 "$backup" "$binary"
  systemctl restart "$service"
}

if ! systemctl restart "$service"; then
  rollback
  exit 1
fi
healthy="false"
for unused_attempt in $(seq 1 20); do
  if systemctl is-active --quiet "$service" && curl -fsS http://127.0.0.1:21120/healthz >/dev/null; then
    healthy="true"
    break
  fi
  sleep 1
done
if [ "$healthy" != "true" ]; then
  journalctl -u "$service" -n 100 --no-pager >&2 || true
  rollback
  exit 1
fi

"$binary" --version
curl -fsS http://127.0.0.1:21120/healthz
printf '\nservice_states:\n'
systemctl is-active "$service" kemi-rustdesk-hbbs.service kemi-rustdesk-hbbr.service
after_hbbs="$(systemctl is-active kemi-rustdesk-hbbs.service)"
after_hbbr="$(systemctl is-active kemi-rustdesk-hbbr.service)"
[ "$after_hbbs" = "$before_hbbs" ] || { echo "hbbs state changed unexpectedly: $before_hbbs -> $after_hbbs" >&2; exit 1; }
[ "$after_hbbr" = "$before_hbbr" ] || { echo "hbbr state changed unexpectedly: $before_hbbr -> $after_hbbr" >&2; exit 1; }
rm -f "$incoming"
echo "binary_backup=$backup"
echo "database_backup=$db_backup"
REMOTE

curl -fsS "http://kemi-chat.newlinksz.com:21120/healthz"
curl -fsSI "https://kemi-chat.newlinksz.com:21121/admin/login" | sed -n '1,8p'
echo "deployment_complete=true"
