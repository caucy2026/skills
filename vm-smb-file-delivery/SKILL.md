---
name: vm-smb-file-delivery
description: Safely deliver files to authorized Windows virtual machines over SMB, configure or restore a guest mapped drive, and verify the transfer by read-back. Use for macOS/Linux host to Windows guest file delivery, legacy Windows SMB troubleshooting, shared-folder synchronization, or Z-drive recovery; do not use for offline virtual-disk mutation while a VM is running.
---

# VM SMB file delivery

Treat file delivery, folder synchronization, drive mapping, and payload execution as four separate operations. Passing one does not prove the others.

Before acting, identify the exact VM, guest OS, guest IP, SMB share, destination path, logged-in Windows user, and whether the requested result is a one-time upload or a continuously synchronized mapped drive. Read the target project's existing VM and deployment runbook first; preserve a proven route when one exists.

## Select the transport

- For a running Windows guest that exposes an authorized administrative or project share, prefer host-initiated SMB upload followed by SMB read-back. Read [references/direct-smb.md](references/direct-smb.md).
- For a Finder/host folder that must appear as `Z:` or another drive inside the guest, first determine whether the drive is a native VM shared-folder transport or a guest-local SMB share fed by a host synchronizer. Read [references/mapped-drive.md](references/mapped-drive.md).
- Use offline QCOW2/VHD/VMDK mounting only when the VM is fully shut down, the image is not attached elsewhere, and the user explicitly requested offline disk work. Never modify a live virtual disk to solve an ordinary delivery problem.

## Safety and correctness boundaries

- Begin with read-only reachability, service, share, path, and current-mapping checks.
- Keep credentials out of source, documentation, Git, shell history, process arguments, and durable logs when practical. Obtain them at runtime through a hidden prompt, approved secret store, or the project's established secure mechanism.
- Do not enable anonymous writable shares, expose TCP 445 to the public internet, or weaken the guest firewall beyond the trusted host/VM network.
- Default to uploading new uniquely named files. Before overwriting, read back the remote file and retain a recoverable copy unless the user explicitly declines.
- File delivery does not authorize execution. Do not start BAT/EXE files, restart services, kill processes, reboot the guest, or change VM resources unless separately requested.
- Drive mappings are scoped to a Windows logon session. A mapping created by SYSTEM or a background service does not prove that the interactive desktop user can see it.
- A host-side directory, VM configuration entry, open TCP port, or successful SMB command is not sufficient evidence by itself.

## Completion gate

Use [references/acceptance.md](references/acceptance.md) and report each layer independently:

1. transport reachable;
2. authenticated share access;
3. remote path resolved;
4. uploaded bytes read back and matched;
5. mapped drive visible in the intended interactive session, when requested;
6. both synchronization directions verified, when requested;
7. persistence after sign-out/sign-in or restart verified, only when requested;
8. payload execution and business effect verified separately, only when authorized.

State failed assumptions and remaining manual steps explicitly. Never convert a partial pass into “shared drive complete.”
