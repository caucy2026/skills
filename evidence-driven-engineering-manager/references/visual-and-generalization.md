# Visual Truth and Generalization

Read this reference when the project includes visual parity, screenshots, UI, 3D rendering, animation, media, simulation, or a requirement for a general algorithm rather than patches.

## Establish visual truth

Classify every image before using it:

- authoritative user/reference capture;
- indexed historical evidence;
- candidate final-product capture;
- debug or component capture;
- generated concept/mockup;
- raw asset/icon/texture.

Only project-authorized reference captures are visual truth. Raw assets, mockups, web previews, debug output, and the current product must not silently become their own acceptance baseline.

Build a reference matrix with source, path, date, hash, scenario, role/object, equipment/state, map/location, camera, resolution/scaling, action/skill, target, frame phase, and known limitations.

## Comparable-capture rule

Before comparing, align the material conditions that affect the picture. If role, equipment, location, camera, scale, state, action phase, target, lighting, or UI layout differs materially, mark the pair `not comparable` and obtain a comparable capture. Do not use subjective resemblance to pass it.

Inspect reference and candidate images directly. Record, as applicable:

- geometry, composition, projection, camera, and object placement;
- model identity, animation frame, pose, equipment, and attachment anchors;
- texture/material, color, alpha, lighting, fog, shadows, and occlusion;
- particle count, emitter position, trajectory, scale curve, blend mode, timing, and lifetime;
- state icons, damage text, menus, panels, typography, hit areas, and interaction feedback;
- temporal order across video or multiple frames.

Use side-by-side views first; use registered overlays or difference images when they answer a specific question. Pixel metrics are supporting measurements, not a replacement for checking semantic and temporal correctness.

The candidate must come from the intended final artifact. Record its binary/package hash, source commit, runtime environment, and capture path. A replay, web preview, old build, debug executable, historical screenshot, or single still cannot prove a required dynamic final-product behavior.

## General algorithm gate

A general solution must explain where behavior comes from and reproduce a class of examples without sample-specific branches.

Require:

- authoritative data source and transformation chain;
- algorithm entry points and shared state/lifecycle ownership;
- explicit behavior for unknown or malformed input;
- no branches keyed to individual sample IDs, names, screenshots, or hand-tuned constants unless the source format itself defines them;
- tests across multiple representative examples and at least one counterexample;
- regression outside the originally failing sample;
- a scan or review for forbidden hard-coded special cases;
- evidence that fixing one case did not degrade previously accepted cases.

An implementation that makes one screenshot look closer but cannot explain the data path is a patch, not an accepted algorithm. Keep the sample `FAIL` or `component-only` until the generalization gate passes.

## End-to-end visual closure

For systems where a backend drives a renderer, require the full chain:

```text
real user/client action
→ protocol request
→ backend algorithm and authoritative state
→ persistence/audit when applicable
→ protocol response/event
→ client state machine
→ resource resolution and general rendering algorithm
→ final-product visual/interaction result
→ reference comparison and cross-example regression
```

Backend-only or client-only evidence can close a component, not the whole chain.

