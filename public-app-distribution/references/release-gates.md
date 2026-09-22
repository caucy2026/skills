# Common release gates

## Source and variant isolation

- Start from a clean, identified commit. Preserve unrelated working-tree changes.
- Pull/rebase according to the project policy and record the full commit SHA.
- Channel-only changes belong in a named flavor, target, configuration, or compile-time define. Build and test the ordinary distribution variant too, proving it did not change.
- Avoid review-evasion behavior. A feature that is not allowed in one store must be permanently absent from that store's binary or fully disclosed and compliant.

## Product metadata

Prepare a stable product name, short/long description, category, age rating, languages, screenshots, icon, support URL, privacy URL, terms URL, copyright, contact email, and release notes. URLs must return useful public content without authentication, not merely HTTP 200 or a repository landing page.

Descriptions and screenshots must match the submitted binary. Mention network listeners, downloads-folder access, background operation, remote-control capabilities, user-generated content, cryptography, and account requirements when relevant.

## Build and artifact validation

For every platform record:

- semantic version and monotonically increasing build/version code;
- source commit and build command/configuration;
- architecture(s), minimum OS, package identifier, and artifact size;
- SHA-256 (and MD5 only when a legacy service explicitly requires it);
- signature chain, timestamp, notarization/stapling where applicable;
- dependency/runtime inventory and license notices;
- fresh install, upgrade from previous public version, launch, core workflow, close/background behavior, uninstall, and rollback checks.

Use the project's documented canonical unpacker and verifier for the channel artifact. A failure produced only by a different archive extractor, quarantine context, or ad-hoc verification path is not proof that the artifact is damaged. Reproduce the result with the canonical command and the intended host security context before rebuilding, re-signing, or replacing an already identified artifact; record both results when they disagree.

macOS public download artifacts should normally be Universal (`arm64` + `x86_64`) when Intel support is promised, have the promised minimum deployment target, pass strict `codesign` verification, Gatekeeper assessment, notarization, and stapling. App Store archives require Apple Distribution signing and an App Store provisioning profile; Developer ID signing is for distribution outside the Mac App Store.

Windows release validation should occur on a representative clean Windows machine, not only by cross-compilation. Verify installer/UI architecture, input/clipboard, update behavior, antivirus reputation impact, and clean-machine runtime dependencies.

## Submission and verification

- Capture upload/submission IDs and portal timestamps.
- Re-open the portal after submission and verify the state changed; do not trust a transient toast alone.
- When published, retrieve the public artifact or HEAD metadata, compare version, size, and checksum to the approved candidate, then install/launch it.
- If rejected, quote only the relevant issue identifiers, map each to code/metadata evidence, fix the smallest compliant scope, retest every affected variant, and send a concise reviewer reply.

## Release report template

For each channel record: `channel`, `listing URL`, `platform`, `version/build`, `commit`, `artifact`, `SHA-256`, `signature/notarization`, `upload/submission ID`, `status`, `checked at`, `evidence`, `blocker`, and `next action`.
