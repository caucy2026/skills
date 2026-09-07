---
name: kemi-s1-hardware-debug
description: Connect and diagnose KEMI S1/huanglong Android hardware through VibeKits Harness using a caller-provided ADB address and an automatically discovered CH340 serial console. Use for dual-channel identity checks, logs, boot/crash/ANR diagnosis, and evidence-driven HiV730 source analysis; do not use for unrelated devices.
---

# KEMI S1 hardware debugging

Use VibeKits Harness tools to establish independent ADB and serial evidence for a KEMI S1 (`huanglong`) target. The operator only provides the current ADB address or `host:port`; never assume a saved IP or COM name.

## Required workflow

1. Refresh the live Harness/MCP catalog and use its current JSON Schemas. Use `vibekits.adb.*` and `vibekits.serial.*`; do not replace them with shell, system ADB, PowerShell serial access, or guessed parameters.
2. Normalize an address without a port to `5555`, call `adb.connect`, then `adb.list_devices`. Lock every later ADB call to that exact verified serial. Stop if it is unauthorized/offline or not KEMI S1/huanglong.
3. Call `serial.list_ports`. Rank current physical USB ports by CH340/CH341 description, USB transport, VID `0x1A86` (`6790`) and PID `0x7523` (`29987`). COM names can change; `COM33` is historical evidence only.
4. Use the verified console configuration: `115200 baud, 8 data bits, no parity, 1 stop bit, no flow control`. Do not probe other frame formats unless this profile fails on every matching candidate.
5. Try matching candidates one at a time with a bounded read-only console command. Send a unique marker plus `getprop` for model, manufacturer, device and Android release. Accept a port only after its response contains the marker, readable values and a console prompt; opening a handle or receiving zero bytes is not success.
6. Read the same four properties through the selected ADB serial and compare normalized values exactly. Current family evidence is model `huanglong`, manufacturer `HL2.0`, device `hi3781v730`, Android `12`; report drift instead of forcing these values.
7. Close one-shot transactions automatically. For sustained logging use the advertised serial and ADB session open/status/read/close tools, retain task/session IDs, and close both sessions at the end.

Read [references/s1-profile.md](references/s1-profile.md) before executing a live S1 task. It contains exact parameters, matching and fallback logic, evidence format, and the recovered HiV730 Git routing.

## Boundaries

- Commands defined here are read-only. Reboot, install, uninstall, property writes, file changes, flashing, bootloader work, stress loops, or source changes require authority from the current task.
- Local Harness uses the APP's local authority. Remote LMCP callers still require pairing and persisted provider-side scope.
- Do not send identifiers, logs, source, credentials, or network details to an external model without authorization for that transmission. The local VibeKits tool bridge can perform deterministic connection and comparison locally.
- Never print or store passwords, private keys, tokens, bridge credentials, or signing material.

## Completion

Report separately: live catalog, ADB connection/identity, serial discovery, serial marker round trip, four-field comparison, requested diagnostics, source mapping, session cleanup, and evidence path. One working channel cannot compensate for the other failing.
