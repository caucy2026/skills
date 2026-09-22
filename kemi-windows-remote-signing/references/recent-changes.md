# Recent changes

## 2026-09-18 — Windows remote-signing workflow consolidation

The remote Windows Authenticode workflow is now exposed through one global entry: `$kemi-windows-remote-signing`. The former broad name `$kemi-remote-signing` was removed because it could be confused with macOS signing and notarization workflows.

### Signing trigger

The supported interactive chain is now explicit:

```text
VibeKits app_control in the active Windows session
  -> fixed GUI launcher EXE
  -> fixed BAT
  -> fixed PowerShell signing script
  -> SignTool
  -> hardware-token PIN dialog
```

SSH must not launch the BAT or SignTool directly. SSH is limited to inspection, fixed-file transfer, hashing, preparation, and report retrieval because it normally runs in Session 0 and cannot reliably expose the PIN dialog to the logged-in signer.

### PIN-dialog evidence

- A window title, PID, or `Visible=true` is no longer enough to ask for PIN entry.
- The controller must restore and foreground the PIN dialog, capture a fresh screenshot, visually inspect it, and show it to the signer.
- If the simulator screenshot is black, stale, or does not contain the dialog, a fixed Session 1 capture helper must create a PNG under the current `D:\KEMI-Test\results\signing\<RUN_ID>` directory. The controller downloads, inspects, and displays that PNG.
- If the protected desktop still cannot be captured, the run records `PIN_SCREENSHOT_UNAVAILABLE`; it must not claim the dialog is visible or enter unattended waiting.
- Screenshots are taken before input only. PIN values are never read, stored, pasted, scripted, or logged.

### Live completion tracking

After showing the screenshot and asking the signer to enter the PIN, the same task starts 2–3 second polling immediately. It does not create a scheduled task, end the turn, or require the signer to report completion. The run is followed through batch signing, full verification, and a new final `PASS` or `FAIL` report.

Success still requires the exact frozen manifest count, expected certificate thumbprint, trusted timestamp, `signtool verify /pa /all /v /tw`, independent main-executable verification, and post-sign SHA-256 values. Process exit or disappearance of the PIN window is not sufficient evidence.

### Documentation layout

- `SKILL.md` is the only invocation entry.
- `references/workflow.md` contains the VibeKits Session 1 execution procedure.
- `references/authenticode-signing.md` contains the shared Authenticode verification contract.
- This file records the current behavior change for reviewers and future maintainers.
