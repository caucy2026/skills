# KEMI S1 / huanglong verified profile

## Input and discovery

The operator provides only `adbAddress`: an IPv4 address, hostname, or `host:port`. If no port is supplied, use `5555`. Never request or assume a COM port before discovery.

Always refresh the live catalog before calls. The names below are stable internal IDs; exported names and schemas come from the live provider.

1. `vibekits.adb.connect {"address":"<adbAddress>"}`
2. `vibekits.adb.list_devices {}`
3. `vibekits.serial.list_ports {}`
4. Rank current candidates using CH340/CH341 description, `transport=usb`, `vendorId=6790` (`0x1A86`) and `productId=29987` (`0x7523`).
5. Try each matching candidate with `vibekits.serial.transact`:

```json
{
  "port": "<discovered-port>",
  "baudRate": 115200,
  "dataBits": 8,
  "stopBits": 1,
  "parity": "none",
  "flowControl": "none",
  "mode": "text",
  "data": "echo <unique-marker>; getprop ro.product.model; getprop ro.product.manufacturer; getprop ro.product.device; getprop ro.build.version.release; echo <unique-end-marker>\r\n",
  "waitMs": 5000
}
```

Accept the port only when the delimited response contains four readable values and a console prompt. Continue to the next enumerated candidate on open failure, zero bytes, missing marker, undecodable output, or mismatched identity. Never scan invented COM names.

For the exact serial returned by ADB, call `vibekits.adb.command` four times with `arguments=["shell","getprop","<property>"]` for `ro.product.model`, `ro.product.manufacturer`, `ro.product.device`, and `ro.build.version.release`. Trim CR/LF and compare all four values.

`serial.auto_detect` can help with an unknown noisy console, but a quiet console can return zero bytes and zero confidence. For S1, the verified 115200/8-N-1/no-flow-control profile plus marker round trip is decisive.

## Verified evidence

On 2026-09-07, caller-supplied ADB `192.168.3.75:5555` and dynamically discovered `COM33`/CH340/`1A86:7523` both returned:

- model `huanglong`
- manufacturer `HL2.0`
- device `hi3781v730`
- Android `12`

The serial transaction sent 174 bytes and received 810 bytes with markers and `console:/ $`. These are identity expectations and historical evidence, not fixed IP or COM configuration.

## Diagnostics after identity passes

- Boot/reboot: serial continuous log plus ADB `boot_id`, boot reason, pstore/ramoops and bounded dmesg.
- Crash/ANR: ADB main/events/crash Logcat, ANR traces, tombstones and activity/process state, with serial tail.
- Black screen: SurfaceFlinger/display/HWC/GPU evidence plus serial/kernel tail.
- Install/launch stress: asynchronous task/session tools, explicit iterations, stage evidence, abort thresholds, cancellation and cleanup.

Never manufacture serial success from ADB-only data. Preserve bounded raw evidence and a normalized comparison.

## HiV730 source routing

Recovered historical project coordinates:

- SSH manifest: `ssh://172.21.16.194:29420/HiV730/manifest.git`
- Gerrit HTTP manifest: `http://172.21.16.194:8092/HiV730/manifest.git`
- historical master SHA: `7ed6ea64eb96ea379aacdcd3319eac38d2257e82`
- manifest: `default.xml`

These private-network coordinates do not prove current reachability or authorization. Refresh refs first. Preserve SSH host-key verification; the historical SSH attempt failed closed on an unknown host key. The HTTP endpoint previously supported read-only refs and manifest retrieval.

After collecting a real failure signature, use bounded VibeKits Git tools: `git.list_remote_refs`, then `git.read_remote_file`, map the failure to the smallest repository, and only then `git.clone_minimal` for that explicit repo/ref/depth. Never run an unbounded `repo sync` or clone the whole HiV730 tree by default.

## Evidence result

Return timestamp; controller/provider identity; input and verified ADB serial; discovered serial candidates and accepted USB identity; frame configuration and byte counts; four per-field comparisons; requested stages as pass/fail/blocked/skipped; task/session IDs; sanitized errors; evidence paths; and cleanup state.
