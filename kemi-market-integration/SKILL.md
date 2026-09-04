---
name: kemi-market-integration
description: Integrate, implement, audit, or test KEMI application-market browsing, platform-filtered downloads and installation, and secure in-app self-update across Android, Windows, and macOS. Use when an app needs to 接入 KEMI 商场 or fix its marketplace/update client; use kemi-market-publish instead for an upload-only release task.
---

# KEMI Market Integration

Implement the market as three isolated trust boundaries: public browsing, public self-update, and privileged publishing.

## Read the current contract

Read [references/cross-platform-integration-standard.md](references/cross-platform-integration-standard.md) completely before implementation, migration, security review, or release acceptance. Recheck the live official documentation linked there because production contracts can change. If live documentation conflicts with the bundled reference, stop mutation, follow the live contract, and report the drift.

## Establish the product/platform manifest

Derive rather than invent:

- stable package name and real version source;
- target OS, architecture, minimum OS, directly installable package format, and platform identity/signing policy;
- existing app-center UI, HTTP layer, download storage, native installer bridge, update state, and rollback path;
- final artifact evidence: exact bytes, SHA-256, signature, installability, and tested upgrade origin.

Keep `version_code` as the strictly increasing comparison value and `version_name` as display text. A shared cross-platform package name is allowed, but every lookup and update check must include the current OS.

## Implement the three isolated paths

### Store browsing and installation

- Use only public store endpoints and show only the current platform's records.
- Normalize forward-compatible responses, but reject missing or conflicting platform identity.
- Permit viewing incomplete metadata while disabling installation with a clear reason.
- Download only after explicit user action. Stream to a partial file and validate final HTTPS URL, platform, extension, exact size, SHA-256, and platform signature before installation.
- Launch installers with structured argument APIs, never shell-string concatenation. Preserve a usable current version on cancellation or failure.

### This application's self-update

- Check asynchronously with stable package name, current integer version code, and explicit OS; never block startup or offline use.
- Require both HTTP success and a valid business envelope. A server/schema failure is not “no update.”
- Show a global update prompt only when a verified higher version exists. Keep no-update and background failure out of About and app-center pages.
- Use a persistent, cancellable state machine with bounded retries, atomic partial-file handling, independent updater behavior where required, health checks, and rollback.

### Administrator publishing

Client binaries must never contain administrator credentials, bearer/upload tokens, or signing secrets. Production create/update/upload operations require explicit authorization and a controlled release environment. When the task is to publish signed packages rather than implement the client integration, use `$kemi-market-publish` and its release contract.

## Platform gates

- Android: release keystore, verified APK identity/version/signature, `FileProvider`, system install confirmation, and real permission-denial tests.
- Windows: self-contained signed installer, valid Authenticode, UAC-respecting launch, and a detached signed updater for self-replacement and rollback.
- macOS: correct architectures and minimum OS, nested signing, Hardened Runtime, Apple notarization acceptance, staple validation, Gatekeeper acceptance, and a final archive created after stapling.

Do not claim support for an untested platform, architecture, or minimum OS.

## Diagnose before changing clients

For update failures, compare the real package, a known-nonexistent package, same-platform list, and app detail. If both package checks fail before filtering with the same schema/SQL category while list/detail work, classify it as a backend contract failure and block release closure. Do not delete `os`, rename parameters, ignore business status, or hardcode no-update as a workaround.

## Completion gate

Require evidence for:

- platform mapping/filtering, response compatibility, URL encoding, validation failures, cancellation, retry, partial-file cleanup, and installer argument handling;
- public category/list/detail, old-version positive update, current-version negative update, nonexistent package, and no cross-platform package selection;
- CDN full-download byte/SHA equality and platform signature identity;
- target-device first install, launch, upgrade, cancel/permission denial, corrupt artifact rejection, failure recovery, uninstall where applicable, and old-version preservation;
- no duplicated `(package_name, os_type)` record, no credential leakage, and a report linking source revision, build, artifact, tests, and limitations.

A UI screenshot, successful build, upload response, or HTTP 200 alone is not completion. If implementation is requested, modify and test the target project; if only a design or audit is requested, distinguish verified facts from recommendations.
