# Android real-input and multi-display automation

Use this adapter when release behavior depends on an Android input method, simultaneous touches, physical-style key edges, a remote-input proxy or more than one logical display.

## Prove the path under test

- `adb input keyevent`, `input keycombination` and direct calls into a mapping function bypass an IME's touch handling. They can be isolation controls, but they cannot prove that a visible key or chord works.
- Inject one `MotionEvent` stream containing all pointers through a test-only instrumentation package using `UiAutomation.injectInputEvent`. Preserve pointer IDs and send `DOWN`, ordered `POINTER_DOWN`, optional `MOVE`, reverse `POINTER_UP`, then final `UP`.
- Keep the injector in a package separate from the receiving test Activity. Starting instrumentation can stop or restart its target package; an injector that targets the receiver invalidates focus and event assertions.
- Use a test-only receiver with a real `InputConnection`. Record only action, key code, meta state, repeat count and `sendKeyEvent` result. Do not record user text or install a broad key monitor.
- Assert exact edge order, the main key, required meta bits, balanced modifier release and forbidden `commitText`. A visible pressed state or a modifier log without the main key is a failure.

## Calibrate before the suite

1. Freeze device serial, API/ABI, physical and logical display IDs, resolution, rotation, package versions and installed APK hashes.
2. Launch the receiver on the intended logical display and assert it is the served view in `dumpsys input_method`.
3. Restore the keyboard mode and size. Capture a screenshot or bounds map and reject stale coordinates when resolution, rotation or layout differs.
4. Inject one unmodified key and require its `DOWN/UP` pair. This is the coordinate and focus positive control.
5. Determine the ordinary tap duration from both the device sampling window and the product gesture threshold. Reject ultra-short injections that the device does not recognize. Keep the positive press safely below long-press activation, then run an unmodified duration above the threshold as the negative control. Record both. For a modifier chord, also test a realistic hold and a long hold when the shortcut is expected to remain valid; the long-press action must not swallow the main key.
6. After injection, wait on a bounded event/state condition or allow a small measured settling interval before reading asynchronous logs.

Treat evidence quality separately from product behavior. An empty event set, a sequence beginning with `UP`, or a sequence ending with `DOWN` is an incomplete injection/capture and may be retried a small bounded number of times after restoring focus. A balanced modifier `DOWN/UP` sequence that omits the expected main key is complete evidence of a product failure and must never be retried into a pass. Store retry counts and the discarded incomplete captures.

Keys that normally fire their click on touch-up and also own a long-press action need special chord coverage. If the framework can release or cancel modifier view state before the main-key click, dispatch the shortcut main key on that key's touch-down while the modifier is known to be held, consume the later click, and suppress the key's unrelated long-press action for that chord. Verify that unmodified tap and unmodified long-press semantics remain unchanged.

## Required chord evidence

For a modifier plus main key, require `modifier DOWN`, `main DOWN`, `main UP`, `modifier UP`. For multiple modifiers, require modifiers to go down in pointer order and up in reverse order, with every main-key edge carrying the expected combined meta mask. Repeat representative chords enough times to catch stuck modifiers and dropped pointers; record per-round events and failure indexes.

Include at least:

- one unmodified printable key positive control;
- one two-pointer chord containing a printable key;
- Space or another key with a long-press action, with short/long duration controls;
- one three-pointer chord;
- one chord containing all supported desktop modifiers when the product exposes them;
- cancellation or lifecycle cleanup that proves held modifiers are released;
- resource samples before and after the repeated run;
- crash, ANR and input-timeout deltas without clearing log buffers.

When the input is forwarded to a remote machine, first prove the IME output with the independent receiver, then run the same chord through the real remote connection and assert a destination-side effect or exact destination event. This separates IME loss from transport or host injection loss.
