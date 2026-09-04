# Bundled specification snapshots

Source: VibeKits project revision `7d1759e3a85bd68c5ea2d2c544e94b667020194f`, packaged on 2026-09-04.

These files are bundled so a colleague can load and understand the skill without the author's D-drive checkout. They are supporting design/acceptance snapshots, not installed programs or proof of present node health. Repository-relative code paths and build commands inside the snapshots refer to the application source at the above revision; they do not imply those build tools are part of this skill. Obtain the application source separately only when actually building or modifying it.

Read only the documents relevant to the task, following the links in `common-contract.md`, `platform-adapters.md`, and `windows-58.md`.

## Safety and portability

- Existing hostnames, LAN addresses, account names, public keys and public fingerprints are registered deployment data, not reusable credentials or automatic authority to operate a node.
- Never execute setup, firewall, account, SSH or installation examples just to load or install the skill.
- `windows_node_local_ssh_smoke.ps1.txt` preserves the historical source for review. It mutates ACLs/ownership, authorized keys and SSH service state, and does not restore all prior ACL state. It is deliberately distributed as text, not as an executable helper. Do not run it automatically.
- No private keys, passwords, tokens, application binaries, SDKs, or package caches are included.
- If a live endpoint conflicts with a security/protocol contract, report the mismatch; do not weaken verification.
