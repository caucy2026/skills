# KEMI S1 integration

Read the target repository's current README, architecture, build, install, release, and validation documents before editing. Fetch the remote state and compare it with the working tree; preserve local changes and do not overwrite a newer cloud revision.

## Verified format and invariants

- Logical master: 1920x2560, D2 at y=0..1279 and D0 at y=1280..2559.
- Hardware-friendly stored video: clockwise-rotated 2560x1920 HEVC Main, yuv420p, hvc1, no audio.
- Each live wallpaper window: 1920x1280.
- Video rendering: one MediaPlayer, one SurfaceTexture, one GL context/thread, one `updateTexImage()` per frame, then submit the same texture timestamp to D2 and D0.
- Static and video themes use stable IDs; preserve default theme 03 unless the user changes it.
- UI and service are separate APKs. Preserve the formal platform certificate and never print signing secrets.
- The selector's Exit action must leave the wallpaper service running.

## Device verification

Resolve the actual ADB target supplied by the user. On the common lab device, display ID 0 is the lower display and physical screencap index 0 captures it; display ID 2 is the upper display and physical screencap index 1 captures it. Re-check this mapping because firmware can change it.

The upper launcher may contain large widgets or another foreground activity. Separate normal launcher/app overlays from wallpaper borders by inspecting the wallpaper Window frames and Surface size. Do not stop or manipulate unrelated apps merely to manufacture a clean screenshot.

For synchronization evidence, retain log samples containing a single theme/frame/PTS followed by `targets=D2 D0`. A screenshot pair taken sequentially cannot by itself prove same-frame rendering.

Before rotation tests, record `wm user-rotation -d <id>` and `wm fixed-to-user-rotation -d <id>` for each display. Restore those exact values afterward. A screenshot dimension check proves surface orientation and edge coverage; it does not prove that a character was recomposed upright for portrait use.

## Release record

Record source and resolved URLs, input digest, model and weight digest, native and delivery dimensions, crop, frame count, frame rate, duration, codec, audio count, black-frame result, seam measurement, APK hashes, certificate digest, installed versions, screenshots, same-frame logs, rotation restoration, selector cleanup persistence, CPU/memory snapshots, and any unverified limits.

