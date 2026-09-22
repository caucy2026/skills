---
name: kemi-windows-remote-signing
description: Use when a KEMI Windows package must be Authenticode-signed through a VibeKits device ID or remote-simulation interface, especially when a hardware-token PIN dialog must be shown, screenshotted, and tracked through completion.
---

# KEMI Windows Remote Signing

Complete Windows Authenticode signing through VibeKits in the active logged-in desktop session. A device ID is enough to connect; do not ask for an IP address, SSH password, private key, RustDesk password, or token PIN.

Read and follow [references/workflow.md](references/workflow.md) for every signing run.

For the rationale and compatibility notes behind the current workflow, read [references/recent-changes.md](references/recent-changes.md).

## Trigger chain

Do not execute the BAT directly through SSH. SSH runs in Session 0 and normally cannot display the hardware-token PIN dialog to the signed-in user.

Use this fixed chain:

1. Connect with `vibekits.simulator.connect` using the authorized device ID and verify the returned identity.
2. Use SSH only to inspect state, upload fixed/versioned files, compute hashes, and read reports.
3. Call `vibekits.device.app_control` with `action: launch` to start a fixed GUI launcher EXE in the active Windows desktop session.
4. The GUI launcher starts one fixed BAT file with `UseShellExecute=true`.
5. The BAT runs one fixed PowerShell signing script and preserves its exit code.
6. Restore the token PIN window, capture a checked screenshot, and show that image to the signer before asking for PIN input.
7. Immediately poll the same run every 2–3 seconds until its new final report says `PASS` or `FAIL`.

```text
VibeKits app_control (Session 1)
  -> fixed Launch-Sign-<version>.exe
  -> fixed Run-Sign-<version>.bat
  -> fixed Sign-<version>.ps1
  -> signtool.exe
  -> hardware-token PIN dialog
```

The EXE, BAT, PowerShell script, input manifest, logs, screenshots, and reports must be versioned and stored under `D:\KEMI-Test`. Never accept an arbitrary command in the GUI launcher.

## Non-negotiable completion gates

- A window title or PID is not proof that the signer can see the PIN dialog. Show a visually checked screenshot first; follow the Session 1 fallback in the workflow if the simulator returns a black frame.
- Never read, paste, record, or automate the PIN.
- Keep the current task active after showing the screenshot. Do not create a scheduled task and do not wait for the signer to message again.
- Do not report success from process exit alone. Require the current run's final report, exact manifest count, certificate thumbprint match, timestamp, full SignTool verification, and signed-file hashes.
- Retry a vanished or cancelled PIN dialog at most once after proving the previous attempt has stopped.
