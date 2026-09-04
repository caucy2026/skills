# Registered Windows Node: 192.168.3.58

## Canonical identity

| Field | Value |
|---|---|
| Host | `192.168.3.58` |
| SSH port | `22` |
| SSH user | `kemi-test` |
| Host key algorithm | `ssh-ed25519` |
| Expected host fingerprint | `SHA256:ikZ6NXAH3VFBGooSCeKW0JY9+h0cIcQOzib4fxmvz6M` |
| Registered client public-key fingerprint | `SHA256:hpYI+CFcXcCgdLNnllblFfemUcT+SpAk5m8uwFYh+ww` |
| Registered client public key | `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILcqFlN1LmEBeT/VV60kSRreDnbetudiE0xfBf6A8UXR` |
| Device label | `mac-1047146775` |
| Device ID | `bULd71j7WNXHkRZS90qHj7Jd` |
| Allowed LAN | `192.168.3.0/24` |

The private key is not part of this contract. Locate it only through authorized local SSH configuration or an explicit user-provided path.

## Paths and services

- Remote root: `D:\KEMI-Test`
- Working tree: `D:\KEMI-Test\work`
- Temporary directory: `D:\KEMI-Test\tmp`
- Authorized keys: `C:\Users\kemi-test\.ssh\authorized_keys`
- Account: enabled, non-administrator `kemi-test`
- Service: OpenSSH `sshd`, running with automatic startup and listening on port 22
- Expected user override:

```text
Match User kemi-test
AuthorizedKeysFile C:/Users/kemi-test/.ssh/authorized_keys
Match all
```

The key file should have protected inheritance and full-control entries limited to `kemi-test`, `Administrators`, and `SYSTEM`. Inspect actual ownership and ACLs before repair.

## Connection and rejection diagnosis

Check port 22, obtain the ED25519 host key, compare the exact fingerprint, select the intended private key explicitly, verify its public fingerprint, and connect with batch mode, `IdentitiesOnly=yes`, and strict checking through a narrowly scoped known-hosts file. Stop on host mismatch.

For `Permission denied (publickey,...)`, inspect verbose SSH evidence and distinguish: wrong/no offered key; missing/malformed key line; wrong effective `AuthorizedKeysFile`; rejected owner/ACL; disabled account; or stale service configuration. Never overwrite the whole key file or disable authentication/host checking. After an authorized repair, reload only what changed and repeat strict authentication.

## Build workflow

Before builds, confirm all project, package cache, SDK download, temp and output paths resolve beneath `D:\KEMI-Test` or another explicitly approved D-drive directory. Preserve dirty source state. Run and record the requested stages separately: revision/sync, incremental Release build, self-contained bundle verification, install/deploy, launch, LMCP discovery/call, compatibility, performance, stress count, and self-upgrade/rollback.

Bundled reference snapshots (paths and identities describe this node, not all colleagues' machines):

- [Mac-to-Windows guide](specs/30_MAC_WINDOWS_NODE_CALL_GUIDE.md)
- [58 onboarding](specs/MAC_TO_WINDOWS_NODE_192.168.3.58.md)
- [Node tool requirements](specs/28_AGENT_WINDOWS_NODE_TOOL_REQUIREMENTS.md)
- [Secure integration](specs/27_SECURE_WINDOWS_NODE_INTEGRATION_GUIDE.md)
- [Node tool API](specs/29_AGENT_WINDOWS_NODE_TOOL_API.md)
- [Historical SSH smoke source](specs/windows_node_local_ssh_smoke.ps1.txt) is reference-only. It changes ACLs/ownership, key files and service state; it is not a read-only diagnostic, does not restore all prior ACL state, and must not be automatically executed. Prefer read-only diagnosis and separately authorized, narrowly scoped repairs.
