---
name: kemi-apple-app-store-release
description: Build, sign, upload, submit, remediate, monitor, and verify KEMI macOS applications in Apple App Store Connect using isolated App Store variants and the established KEMI publisher Mac. Use for KEMI Send, VibeKits, KEMI OFFICE, or another authorized KEMI Mac App Store release; do not use for Developer ID direct downloads, notarized ZIP/DMG distribution, or the KEMI internal market.
---

# KEMI Apple App Store release

Deliver a truthful App Sandbox build to the exact App Store Connect record and prove its persistent state. An archive, uploaded package, processed build, selected build, saved draft, yellow badge, or success toast is not a submission or publication by itself.

## Required reading

1. Read the repository `AGENTS.md`, project release instructions, and current release ledger before acting.
2. Read [references/end-to-end.md](references/end-to-end.md) for every new submission or corrected build.
3. Read [references/portal-and-review.md](references/portal-and-review.md) before using App Store Connect, interpreting status, contacting Apple, or handling rejection.
4. Read [references/kemi-products-and-cases.md](references/kemi-products-and-cases.md) only for established KEMI product IDs and historical evidence. Re-check every mutable state live.
5. Read [references/evidence-ledger.md](references/evidence-ledger.md) before reporting progress.
6. Also apply `public-app-distribution` for shared public-store evidence and account-operation rules. This skill is the KEMI/Apple specialization.

## Identity lock

Before building, uploading, attaching, submitting, replying to review, or replacing a build, record and verify:

```text
product:
platform: macOS
channel: Apple App Store
sourceCommit:
bundleId:
appleAppId:
marketingVersion:
buildNumber:
minimumMacOS:
architectures:
archivePath:
exportedPackagePath:
packageByteCount:
packageSHA256:
appleTeam:
processedBuildId:
submissionId:
```

Abort on a mismatch. Never use a KEMI Send build for VibeKits, a direct-distribution package for App Store, or a current dashboard badge to infer the state of a different version.

## Store-only variant

Keep the normal KEMI/internal/direct build intact. Build an explicit App Store-only variant in the project's existing release workflow, using an isolated worktree and cache directory. The App Store variant may permanently remove capabilities that violate policy, but must not hide them temporarily and reveal them later by launch count, elapsed time, remote flag, geography, reviewer detection, or post-review activation.

App Sandbox is mandatory. Retain only capabilities used by reachable App Store functionality. Audit the main app, frameworks, helpers, login items, extensions, XPC services, and plugins independently. A capability inherited accidentally by nested code is still a release defect.

## Release contract

Follow this order:

1. Freeze source, version/build, release notes, supported languages, minimum macOS, and architectures.
2. Create the isolated App Store flavor without weakening or overwriting direct/internal variants.
3. Build an Xcode archive with Apple Distribution signing, the correct team/profile, App Sandbox, and target-specific entitlements.
4. Inspect the archive and exported App Store package for bundle IDs, version/build, architecture slices, deployment target, provisioning, signatures, sandbox, App Groups, nested executables, privacy manifests, and icon resources.
5. Install or launch a locally testable equivalent and exercise first launch, core workflow, permissions, offline/error paths, quit/background behavior, and localization. Record any App Store package limitation separately.
6. Export the App Store package, calculate final byte count and SHA-256, and preserve it immutably with the export summary and test evidence.
7. Upload through Apple's official Xcode transport. Record delivery/upload ID and wait for processing.
8. In App Store Connect, use Google Chrome profile `niu`, open the exact App/version, select the exact processed build, and complete metadata, screenshots, privacy, export compliance, review notes, contact, support URL, and demo credentials when required.
9. Explicitly submit the version for review. Then leave the transient page, reopen the exact version/submission, and record the persistent state and submission ID.
10. On rejection, bind the issue to the exact submission, make the smallest permanent App Store-only correction, increment build when bytes change, repeat every applicable gate, reply precisely, and resubmit.
11. Mark `published` only after an anonymous Apple product page exposes the intended version and a public install/launch/core-workflow check succeeds when available.

## Browser and credential route

On the established publisher Mac, use Google Chrome profile `niu` for App Store Connect. Reuse its authenticated Apple session or normal password-manager autofill; do not inspect browser databases, cookies, Keychain records, or stored secrets. Do not switch to Safari merely because a session expired.

Apple passwords, app-specific passwords, OTPs, trusted-device codes, recovery codes, API private keys, certificates, private keys, and provisioning files never belong in this skill, chat output, screenshots, shell history, repositories, or release ledgers. CAPTCHA, MFA, account recovery, agreements, tax/banking, legal attestations, and other platform-required human gates remain human actions. Prepare everything else first, foreground only the exact gate, then resume automatically from a fresh portal state.

Developer ID plus notarization is the direct-distribution path, not the Mac App Store path. Do not substitute the known `Developer ID Application` identity or `KEMI_NOTARY` profile for Apple Distribution signing and App Store provisioning.

## Truthful states

Use only `not-started`, `blocked`, `uploaded`, `processing`, `submitted`, `in-review`, `rejected`, or `published`.

- `准备提交` means the build/version is not submitted.
- `正在等待审核` or `Waiting for Review` means Apple received the submission and it is queued.
- A red exclamation badge may point to a current issue or an historical message; open the exact submission and Resolution Center before classifying it.
- A long wait is not a rejection. Do not withdraw a healthy submission merely to upload newer code.
- `可分发`/Ready for Distribution is stronger than approval but publication still requires an anonymous public page and the intended version.
- Apple Lookup `resultCount: 0` proves only that no anonymous public listing is visible; it does not prove rejection.

## Completion

Return the exact App, version/build, package hash, processed build, submission ID, persistent state, checked-at timestamp/timezone, current blocker, next action, and evidence path. Never claim success from a dashboard summary, old screenshot, email alone, or memory. Keep the release active until the user's requested terminal state is proved.

