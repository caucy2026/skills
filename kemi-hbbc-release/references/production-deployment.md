# Production deployment and rollback

## Current production contract

Defaults for this KEMI installation:

| Item | Value |
|---|---|
| SSH/SFTP host | `119.96.24.110` |
| SSH/SFTP port | `39281` |
| SSH user | `root` |
| Public domain | `kemi-chat.newlinksz.com` |
| hbbc binary | `/opt/kemi-rustdesk-server/bin/hbbc` |
| hbbc configuration | `/etc/kemi-rustdesk/hbbc.json` |
| account database | `/var/lib/kemi-rustdesk-server/hbbc-accounts.sqlite3` |
| systemd unit | `kemi-rustdesk-hbbc.service` |
| HTTP | `21120/TCP` |
| HTTPS/admin/API | `21121/TCP` |

The SSH password is never documented. Let the administrator type it interactively, or use an already-authorized, separately protected SSH identity. Never print secret-file contents.

## Read-only preflight

Before upload, confirm:

```bash
ssh -p 39281 root@119.96.24.110 \
  '/opt/kemi-rustdesk-server/bin/hbbc --version; systemctl is-active kemi-rustdesk-hbbc.service kemi-rustdesk-hbbs.service kemi-rustdesk-hbbr.service'
```

Record current hbbc version and the before-state of all three services. If hbbs or hbbr is already unhealthy, report it; do not attempt to repair it under this skill.

## Standard binary-only deployment

After the user has authorized the exact production deployment, run:

```bash
/path/to/kemi-hbbc-release/scripts/deploy_hbbc.sh \
  --binary /path/to/hbbc \
  --host root@119.96.24.110 \
  --port 39281 \
  --confirm-hbbc-only
```

The script performs:

1. local ELF/x86-64 validation and SHA-256;
2. upload to a unique `/tmp/hbbc.<timestamp>.new` path;
3. remote `--version` and production `--check-config` as `kemi-rustdesk`;
4. SQLite `.backup` and existing-binary backup;
5. atomic binary install;
6. restart of only `kemi-rustdesk-hbbc.service`;
7. local HTTP health and version checks;
8. confirmation that hbbs and hbbr remain in their prior states;
9. automatic binary rollback if the new hbbc fails its health check.

The script intentionally does not upload `hbbc.json`, service files, keys, or databases.

## Configuration changes

Configuration deployment is a separate operation. Only do it when explicitly requested:

1. fetch or inspect the current production config without printing secret-file contents;
2. compare it with the proposed config;
3. preserve production-only paths, hosts, app catalog locations, TLS paths, SMS/payment secret-file paths, and static-site directories;
4. upload to a temporary path;
5. run the new binary’s `--check-config` as `kemi-rustdesk`;
6. back up the current config;
7. atomically install it;
8. restart only hbbc and execute the full validation matrix.

Do not use `install_bbc.sh` for a routine binary update because it also installs the packaged JSON. It is appropriate only for an initial/explicit package installation after reviewing its effects.

## Validation matrix

Require all relevant checks:

```text
Remote process version                 expected new version
systemctl is-active hbbc               active
systemctl is-active hbbs/hbbr          unchanged from preflight
http://127.0.0.1:21120/healthz         success and current hbbc version
http://kemi-chat.newlinksz.com:21120/  reachable
https://kemi-chat.newlinksz.com:21121/admin/login reachable with valid TLS
recent hbbc journal                     no startup loop/config/database/TLS errors
```

For account/admin changes, log in through the normal administrator page and verify the changed UI/API. Do not put an admin token in a URL. For download-site changes, verify discovery, page rendering, and representative redirects without downloading every large client unless requested.

## Rollback

Rollback replaces only the hbbc binary with the timestamped backup and restarts only hbbc. Keep the failed binary and logs long enough for diagnosis. Do not delete the account database or app catalog.

If a database schema change is not backward-compatible, binary rollback alone is insufficient. A release introducing such a migration must provide and test an explicit data rollback before production deployment. Ordinary additive SQLite indexes are backward-compatible and do not require removal.

## Stop conditions

Stop and report instead of forcing deployment when:

- SSH host identity changed unexpectedly;
- the target is not the expected server;
- the binary is not Linux x86-64 or exceeds GLIBC 2.17;
- production config validation fails;
- SQLite `.backup` cannot be completed;
- the exact hbbc service or binary path differs unexpectedly;
- deployment would require touching hbbs/hbbr;
- hbbc health fails and automatic rollback also fails.
