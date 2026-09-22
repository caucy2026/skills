# Mac-to-Mac tunnel debugging runbook

## 1. Principle and data path

The initiating Mac (A) opens a loopback listener such as `127.0.0.1:22022`. KEMI/RustDesk carries that TCP stream over its authenticated connection to the target Mac (B), where it connects to `127.0.0.1:22`. A then runs ordinary OpenSSH against its own loopback port:

```text
Mac A ssh client
  -> 127.0.0.1:<LOCAL_PORT>
  -> KEMI/RustDesk authenticated TCP tunnel
  -> Mac B 127.0.0.1:<SSH_PORT>
  -> Mac B sshd
```

This avoids router port forwarding and does not expose the target SSH port publicly. KEMI and SSH remain separate security layers.

## 2. Information to obtain

- Exact KEMI device ID and device name of Mac B.
- Mac B system account name; do not ask for or record its password.
- Actual SSH port, normally `22`.
- A unique unused local port for Mac B, normally above 1024.
- Mac B Ed25519 host fingerprint, obtained independently on Mac B:

```bash
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub -E sha256
```

Use a stable port per target to avoid `known_hosts` ambiguity.

## 3. Target preparation

With the owner's approval on Mac B:

1. Enable **System Settings → General → Sharing → Remote Login** only for the required user.
2. Enable **KEMI/RustDesk → Settings → Security → Permissions → TCP tunneling**.
3. Verify SSH locally:

```bash
nc -vz 127.0.0.1 22
```

Read-only identity checks:

```bash
hostname
sw_vers
uname -m
id
```

## 4. Create and validate the tunnel

On Mac A, open the target device's **TCP tunnel** panel and add:

```text
Local port:  <LOCAL_PORT>
Remote host: 127.0.0.1
Remote port: <SSH_PORT>
```

Keep the tunnel session alive. Confirm the listener is loopback-only:

```bash
lsof -nP -iTCP:<LOCAL_PORT> -sTCP:LISTEN
```

Connect without disabling host-key checks:

```bash
ssh -o ServerAliveInterval=15 -o ServerAliveCountMax=3 \
  -p <LOCAL_PORT> <SSH_USER>@127.0.0.1
```

Compare the displayed fingerprint with the independently supplied fingerprint. If it differs, stop. A changed key may mean a reused port, a rebuilt target, or the wrong device. After independently verifying a legitimate change, remove only that target-port entry:

```bash
ssh-keygen -R "[127.0.0.1]:<LOCAL_PORT>"
```

Immediately after login, prove target identity:

```bash
hostname
id
sw_vers
uname -m
```

## 5. Read-only baseline

Record a timestamp on both machines. On Mac B collect only what the issue needs:

```bash
date '+%Y-%m-%d %H:%M:%S %z'
pgrep -afil 'KEMI|远程办公|rustdesk'
lsof -nP -iTCP -sTCP:LISTEN
ps -axo pid,ppid,lstart,%cpu,rss,command
```

For an installed KEMI app, verify the fixed path and metadata:

```bash
/usr/libexec/PlistBuddy -c 'Print :CFBundleIdentifier' '/Applications/KEMI远程办公.app/Contents/Info.plist'
/usr/libexec/PlistBuddy -c 'Print :CFBundleShortVersionString' '/Applications/KEMI远程办公.app/Contents/Info.plist'
/usr/libexec/PlistBuddy -c 'Print :CFBundleVersion' '/Applications/KEMI远程办公.app/Contents/Info.plist'
codesign -dv --verbose=4 '/Applications/KEMI远程办公.app' 2>&1
spctl -a -vv -t exec '/Applications/KEMI远程办公.app'
```

Use narrow log windows. Start a timestamp immediately before reproduction and query only matching processes/categories afterward. Avoid unrestricted dumps containing user data.

## 6. Reproduction discipline

1. State one exact action sequence and acceptance condition.
2. Start simultaneous resource/process/socket sampling on Mac B.
3. Have the operator perform the action once and announce the exact time.
4. Correlate Mac B logs with the initiator/client logs using time, connection ID, session ID, peer hash, process PID, and window ID where available.
5. Repeat enough times to distinguish a deterministic bug from noise; preserve the first failure evidence.
6. If logs are insufficient, add one bounded diagnostic point that can answer the unresolved question. Do not flood video/input hot paths with per-frame logging.

For lifecycle or duplicate-process bugs, compare before/after counts:

```bash
pgrep -afil 'KEMI|远程办公|rustdesk'
ps -axo pid,ppid,state,lstart,command | rg 'KEMI|远程办公|rustdesk'
lsof -nP -p <PID>
```

For memory investigations, sample the same PID and distinguish RSS, physical footprint, heap growth, mapped media buffers, and file-descriptor growth. A larger cache plateau is not automatically a leak; monotonic retained growth under repeated identical cycles is the stronger signal.

## 7. Transfer and candidate deployment

SSH/SFTP/SCP reuse the same tunnel:

```bash
scp -P <LOCAL_PORT> <LOCAL_FILE> <SSH_USER>@127.0.0.1:<REMOTE_STAGING_PATH>
sftp -P <LOCAL_PORT> <SSH_USER>@127.0.0.1
```

Before replacing an app, obtain explicit deployment approval. Stage outside `/Applications`, verify SHA-256, signing, notarization/staple, architecture, minimum macOS version, bundle ID, and fixed bundle name. Preserve the current installation as a timestamped recoverable backup; never delete it first.

After installation, launch from `/Applications/KEMI远程办公.app`, then verify:

- Process executable path points to `/Applications`, not App Translocation or a mounted archive.
- Version/build and hash match the candidate.
- Existing configuration and user-set password remain intact.
- Screen Recording and Accessibility permission identity remain tied to the fixed bundle ID/path.
- Both required architectures are present for a Universal release.

## 8. Post-change validation

Repeat the original action sequence, not a substitute smoke test. Compare:

- success/failure count and latency;
- process and child-process count;
- window/Dock item behavior;
- open sockets and file descriptors;
- CPU, RSS/footprint, retained heap trend;
- logs for crash, ANR-equivalent stalls, connection resets, decoder failure, or unrecovered state;
- old configuration, permanent password, permissions, and upgrade behavior.

If the gate fails, collect the new evidence and restore the preserved installation/configuration. Do not publish the candidate.

## 9. Close cleanly

1. Exit SSH.
2. Remove the forwarding record in KEMI/RustDesk.
3. Verify the local port is no longer listening:

```bash
lsof -nP -iTCP:<LOCAL_PORT> -sTCP:LISTEN
```

4. Ask the owner whether temporary Remote Login/TCP-tunneling permissions should be disabled.
5. Record whether the candidate remained installed or rollback completed.

## 10. Common failures

- `No permission of IP tunneling`: target has not authorized TCP tunneling.
- Local port not listening: tunnel window/session closed, wrong device, or port collision.
- `Connection refused` after the tunnel reaches B: `sshd` is not listening on the configured target port.
- SSH authentication failure: KEMI authentication succeeded, but the Mac account/key/password did not.
- `REMOTE HOST IDENTIFICATION HAS CHANGED`: stop and reverify target fingerprint; never suppress the check.
- Tunnel drops during a long test: use task-side checkpointing or an authorized persistent test harness; SSH keepalive only detects failure and cannot fix target sleep or KEMI disconnects.
