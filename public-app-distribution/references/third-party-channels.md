# Third-party public channels

## Uptodown

Create or claim the app, complete product/platform metadata, upload the exact signed artifact, submit it, and verify listing state after processing. CAPTCHA and MFA require the account owner. A successful login or upload does not mean review started. Record listing ID, filename, checksum, scan state, submission state, and public URL.

If password login fails, distinguish invalid credentials from unsolved CAPTCHA using the actual portal message and field state. Do not repeatedly retry credentials or bypass CAPTCHA. OAuth may request third-party scopes; inspect them before authorization.

The top-level application state can lag or use wording such as `pending revision` while an exact uploaded file already shows `pending review`. Record both, but use the file/version detail as evidence for the binary and the application page as evidence for the listing. Do not collapse these two scopes into one invented state.

## Softonic and editorial catalogs

Prefer the publisher submission route and canonical vendor URL. Provide a signed stable build, version, OS support, screenshots, description, privacy/support URLs, and publisher identity. Record whether the request is received, queued, accepted, or publicly listed. Search-engine absence alone is not proof of rejection.

Preflight the package type shown by the exact platform form before building or uploading; for example, a macOS form may accept DMG/PKG while rejecting ZIP. Verify the platform selector before file selection, again before `Save`/`Create`, and on the dashboard after creation. A Windows draft created while attempting macOS does not satisfy the macOS submission. Do not reuse, modify, or delete unrelated product/platform drafts merely because they are visible in the same account.

If a legal ownership or distribution-rights declaration is unchecked, prepare every other field and bring that declaration to the account owner for explicit confirmation. Do not silently make the legal attestation.

## SourceForge and vendor-listing catalogs

Distinguish open-source project hosting from commercial/business software listings. Proprietary desktop binaries should use the current official vendor-listing route or another explicitly accepted commercial route; do not create a misleading open-source project. A delivered email or support request is `submitted` only for the onboarding request, not `published` for either application. Record the recipient/form endpoint, request ID or delivery evidence, included product/platforms, reply state, and public product URL once created.

## GitHub Releases

Use an identified commit/tag. Upload platform-labelled signed artifacts, checksums, release notes, minimum OS/architecture, install instructions, known limitations, and security/privacy links. Verify public asset headers and hashes. Never publish secrets, sensitive symbol bundles, or unsigned artifacts under a stable tag.

## Homebrew Cask

Use a notarized immutable versioned URL and SHA-256. Confirm bundle identifier, app name, uninstall/zap behavior, and minimum macOS. Submit to the appropriate tap only after the canonical release is public and immutable.

## Microsoft Store

Use Partner Center and the currently accepted package type. Validate identity, architectures, capabilities, privacy/support URLs, screenshots, rating, clean-machine install, upgrade, launch, uninstall, and certification. Record submission/certification IDs and exact package version.

## Feature policy

Some catalogs permit variants, but undisclosed delayed activation is never a default tactic. If staged availability is explicitly permitted, document the rule and test pre/post activation. Apple review builds must not contain dormant functionality intended to appear only after review.
