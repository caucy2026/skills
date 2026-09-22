# End-to-end Mac App Store workflow

Read this file for every KEMI macOS App Store release. Apple documentation and the live portal remain authoritative when fields or policies change.

## 1. Preflight and isolation

- Read the project release scripts and prior App Store handoff. Reuse the existing build path; do not create a parallel ad-hoc pipeline just because the portal is urgent.
- Fetch/sync only through the project's documented Git route. Preserve user changes and record the exact source commit.
- Use a separate App Store worktree and separate build/cache directories. On this workstation put regenerable Xcode/Flutter/Rust/temporary outputs under `/Volumes/ORICO/kemi-build-cache/<project>-app-store/` when ORICO is mounted and writable. Do not silently fall back to filling the system disk.
- Keep marketing version and build number distinct. Every changed binary needs a new monotonically increasing build number even when the marketing version is unchanged.
- Confirm Apple App ID, bundle ID, team, roles, agreements, certificates, provisioning profiles, listing record, and next build number before compiling.
- Freeze supported languages. Screenshot language must match its locale. Chinese UI screenshots do not belong in an English (United States) metadata block.

## 2. Store capability design

Create a permanent App Store flavor. Do not change the normal/internal flavor.

- Enable App Sandbox and only entitlements used by shipped App Store code.
- Prefer `com.apple.security.network.client` when the app initiates outbound connections. Keep `com.apple.security.network.server` only if the reviewed feature truly listens for inbound connections and reviewer notes explain why, where the user triggers it, what data is exchanged, and how it is disabled.
- Treat Downloads access, user-selected file access, accessibility, screen recording, input monitoring, background services, remote control, login items, camera, microphone, Bluetooth, USB, and local-network behavior as review-sensitive. Remove unused capabilities rather than merely hiding their UI.
- Do not advertise or link to prohibited external payment/donation/software-acquisition routes in the App Store binary when Apple policy disallows them.
- Keep About, privacy, support, version, and contact information reachable without login.
- Remote-control software is not automatically impossible on macOS, but permissions, consent, disclosure, sandbox compatibility, reviewer access, and privacy behavior must match the actual implementation. If the product fundamentally needs capabilities incompatible with the Mac App Store, keep that capability in the Developer ID distribution instead of disguising it.

## 3. Signing and archive inspection

Use Apple Distribution and the correct App Store provisioning profile. Developer ID notarization is a separate direct-distribution flow.

Inspect at least:

- `CFBundleIdentifier`, `CFBundleShortVersionString`, `CFBundleVersion`, display name, and minimum macOS;
- main binary and every nested executable for required `arm64`/`x86_64` slices;
- signature authority, designated requirement, Team ID, hardened/runtime settings as applicable;
- embedded provisioning profile and entitlement agreement between profile and code;
- App Sandbox and target-specific entitlements for app, extensions, XPC, helpers, frameworks, login items, and plugins;
- App Groups and keychain groups shared only where required;
- privacy manifests and required-reason API declarations;
- no development/ad-hoc signatures and no unsigned nested code;
- no stale direct-distribution updater, store selector, donation link, debug menu, private framework, or dormant restricted capability in the App Store target.

Do not apply the main target's entitlements indiscriminately to Pods, packages, helpers, or frameworks. Each target gets only its own entitlements.

## 4. Icon and presentation gate

Before archive/export:

- validate `Assets.xcassets/AppIcon.appiconset/Contents.json` and every referenced file;
- include the required 1024×1024 marketing icon and valid lower sizes without alpha when Apple requires it;
- ensure the App Store build target actually selects that asset catalog and `AppIcon` set;
- inspect the archive/exported product, not only source files;
- treat an App Store Connect placeholder/grid icon as a build or asset-processing defect until the processed build proves otherwise.

For screenshots, use truthful current UI, the exact locale, Apple-supported dimensions, and no invented controls or misleading device frames.

## 5. Test gate

Run project automation plus native smoke checks proportional to functionality:

- clean install or locally testable equivalent;
- first launch, relaunch, update/migration when relevant;
- primary workflows and failure paths;
- sandbox file open/save/import/export paths;
- network unavailable, permission denied, malformed data, and service unavailable paths;
- light/dark appearance and every declared locale's critical screens;
- close-window, quit, background/menu-bar behavior as documented;
- CPU/memory idle behavior and no crash loop;
- Intel/macOS 12 support only when deployment target and every executable slice are actually verified.

Record a limitation when the exported App Store package cannot be locally installed exactly as delivered; do not replace package inspection with an unrelated development build and call it equivalent.

## 6. Export and upload

- Export with the project's established App Store export options.
- Preserve export logs/summary, package absolute path, byte count, and SHA-256.
- Upload using Xcode Organizer or Apple's current official command-line transport.
- Record delivery/upload identifier and response. An accepted upload is `uploaded` or `processing`, not `submitted`.
- Wait for processing and inspect any processing warning/error. Never attach a different build merely because it appeared first.

## 7. App Store Connect completion

On the exact version page:

- attach the exact processed build number;
- provide localized name/subtitle/description/keywords/promotional text as applicable;
- provide truthful localized screenshots and icon processing result;
- answer privacy/nutrition labels from actual code/data flows, including third-party SDKs;
- answer encryption/export compliance truthfully;
- provide product-specific public Support URL and Privacy Policy URL;
- provide reviewer contact, deterministic review steps, notes for unusual capabilities, and demo credentials only when required;
- complete age rating, availability, pricing, category, copyright, and agreements.

Save, reload, and prove persistence. Then explicitly choose Submit for Review. Upload, processing, build selection, and draft save are not submission.

## 8. Resubmission

When Apple rejects:

1. Open Resolution Center and bind the message to App, platform, version/build, and submission ID.
2. Quote or summarize the exact guideline and requested action in the release ledger.
3. Classify as binary, entitlement, metadata, privacy, business model, reviewer access, or account/agreement.
4. Fix the smallest permanent App Store-only scope. Preserve direct/internal behavior.
5. Increment build if bytes change; rebuild cleanly and repeat signature, entitlement, sandbox, icon, test, and package gates.
6. Upload, attach the new processed build, update notes/metadata, reply with exact changes and navigation steps, and explicitly resubmit.
7. Reopen the exact submission and capture the new persistent state.

Never rename and re-upload rejected bytes, mask a prohibited feature, or unlock it after review.

