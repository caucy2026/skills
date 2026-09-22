# Windows node, storage, and remote-control contract

Read this reference before connecting to or changing a Windows test machine.

## Host discovery and authentication

- Obtain the current host/IP, SSH user, port, expected host-key fingerprint, and controller public-key path from the active project's trusted documentation or from the user.
- IP addresses are not stable identity. Do not reuse an address from an old report without checking the current document and host fingerprint.
- Preflight in increasing order: local route/interface, ICMP when allowed, TCP 22, SSH key scan/fingerprint comparison, then public-key login.
- Do not use `StrictHostKeyChecking=no`, delete known-host entries blindly, or accept a changed key without user confirmation and an independent explanation.
- Use the project's intended key, commonly an existing `~/.ssh/id_ed25519`; never copy the private key to Windows.
- Do not expose passwords in command arguments. Prefer public-key auth and an allowlisted remote account.

Typical read-only controller checks:

```bash
route -n get WINDOWS_IP
nc -vz -w 3 WINDOWS_IP 22
ssh-keyscan -T 5 -t ed25519 WINDOWS_IP
ssh -o BatchMode=yes -o ConnectTimeout=8 WINDOWS_USER@WINDOWS_IP \
  'pwsh -NoProfile -Command "$PSVersionTable.PSVersion.ToString()"'
```

Compare the `ssh-keyscan` fingerprint with trusted project documentation before the final SSH command. Never treat scan output itself as trusted identity.

## Required Windows baseline

- Supported Windows 10/11 x64 with current security updates.
- Windows OpenSSH Server, automatic service start, LAN-only firewall scope.
- PowerShell 7 x64 callable as `pwsh`.
- A dedicated test account rather than a personal Microsoft account.
- A logged-in, unlocked interactive desktop account for UI testing.
- Recorded Windows build, CPU, RAM, GPU, display resolution, scale/DPI, locale, and free disk.
- Project-required build tools and runtimes installed or unpacked under `D:` unless Windows itself owns the component.

## D-drive invariant

All controllable data must remain under a fixed root such as `D:\KEMI-Test`:

```text
D:\KEMI-Test\
├─ source\                 commit-specific source/worktrees
├─ build\                  build directories
├─ tools\                  portable verified tools
├─ cache\                  compiler/package caches
├─ tmp\                    TEMP and TMP
├─ inbox\release\          incoming installers
├─ inbox\test-docs\        hash-verified corpora
├─ app\                    isolated installed/staged products
├─ agent\                  allowlisted interactive agent
├─ work\                   remote orchestration scripts
└─ results\
   ├─ logs\
   ├─ screenshots\
   ├─ traces\
   ├─ dumps\
   └─ vX.Y.Z\
```

Before work:

```powershell
$Root = 'D:\KEMI-Test'
if (-not (Test-Path 'D:\')) { throw 'D: drive is required.' }
$env:TEMP = "$Root\tmp"
$env:TMP = "$Root\tmp"
New-Item -ItemType Directory -Force -Path $env:TEMP | Out-Null
```

Also redirect project-specific NuGet, npm, Gradle, compiler, package-manager, DerivedData-equivalent, and download caches to `D:`. Do not install large SDKs or unpack archives into user profile/AppData or system TEMP by convenience.

Windows-owned registry, event log, service metadata, certificate stores, and unavoidable OS component records are exceptions. Project scripts must still avoid creating their own C-drive payloads.

## Transfer integrity

- Transfer only explicit paths via SFTP/SCP/rsync-over-SSH or Git.
- Place incoming artifacts in a versioned staging directory, not directly over a running installation.
- Compute SHA-256 on both controller and Windows after every material transfer.
- Keep test corpora read-only or copy them into a per-run work directory.
- Preserve Chinese names, spaces, long paths, and binary contents; use a small known binary round-trip during first node setup.

Example Windows check:

```powershell
Get-FileHash 'D:\KEMI-Test\inbox\release\package.exe' -Algorithm SHA256
```

## Destructive and privileged actions

The remote machine belongs to the user. Resolve exact targets before changing state.

- Read-only inventory, builds, tests, and writes inside the assigned versioned D-drive workspace are normally in scope.
- Ask before deleting material directories, uninstalling unrelated applications, resetting source changes, modifying firewall/security policy, importing certificates, installing system services, or rebooting.
- Prefer versioned side-by-side workspaces and isolated installs. Do not recursively delete `D:\`, `D:\KEMI-Test`, a user profile, or an unresolved variable.
- Stop only exact validated build processes. Never use broad `taskkill` patterns that can terminate unrelated work or the updater child process.

## Session boundary

SSH commands run in Session 0. They can compile, hash, inspect processes, install silently, and run headless algorithms, but cannot establish that visible UI is correct.

For UI work, use only a project-provided allowlisted desktop agent or an interactive scheduled task launched as the already logged-in desktop user. The bridge must:

- reject Session 0 when it is intended for desktop interaction;
- accept named allowlisted actions rather than arbitrary commands;
- keep request, heartbeat, logs, screenshots, and response JSON on `D:`;
- reject stale heartbeats and invalid paths;
- produce an explicit `interactive_required` result when no desktop token is available.

Do not enable general remote desktop automation or weaken Windows security merely to make a test pass.
