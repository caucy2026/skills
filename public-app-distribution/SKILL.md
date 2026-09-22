---
name: public-app-distribution
description: Prepare, submit, update, and verify desktop or mobile apps across public application stores and high-reach download catalogs. Use for Apple App Store, Microsoft Store, Uptodown, Softonic, GitHub Releases, Homebrew, or similar external distribution; use project-specific internal-market skills for private company stores.
---

# Public application distribution

Ship a truthful, installable release and leave an auditable record. Treat a successful upload as an intermediate state: completion requires storefront/review status, downloadable artifact integrity, and an install/launch smoke test when the platform permits it.

## Route the work

1. Inventory the app, target platforms, source branch, current public versions, signing assets, support/privacy URLs, and authorized publisher accounts.
2. Select channels by platform, audience, cost, review constraints, and packaging support. Read [references/channel-selection.md](references/channel-selection.md).
3. Apply the common release gates in [references/release-gates.md](references/release-gates.md).
4. For Apple submission or rejection remediation, read [references/apple-app-store.md](references/apple-app-store.md).
5. For Uptodown, Softonic, GitHub Releases, Homebrew, Microsoft Store, or other catalogs, read [references/third-party-channels.md](references/third-party-channels.md).
6. For failures or stalled reviews, use [references/troubleshooting.md](references/troubleshooting.md).
7. Before operating an authenticated publisher account or reporting progress, read [references/proof-and-account-operations.md](references/proof-and-account-operations.md).
8. When publishing through Apple, Uptodown, Softonic, or SourceForge, read the field-tested failure patterns in [references/four-channel-field-lessons.md](references/four-channel-field-lessons.md).
9. When operating on the KEMI macOS publisher workstation, read [references/kemi-publisher-workstation.md](references/kemi-publisher-workstation.md) before asking for credentials or opening a portal.
10. Record every channel using [references/release-record-template.md](references/release-record-template.md).

On the KEMI publisher workstation, previously verified browser profiles, package formats, account routes, and backend proof checks are release parameters. Reuse them exactly; do not re-explore an earlier failed route unless the environment or portal requirement has materially changed. When a new route is independently proven, update the workstation reference so the next operator inherits it.

Use these exact states: `not-started`, `blocked`, `uploaded`, `processing`, `submitted`, `in-review`, `rejected`, or `published`. Never report `published` from an upload receipt alone.

## Proof before progress

Every progress claim must name the exact product, platform, version/build, artifact SHA-256, state scope, checked-at time, and authoritative evidence. A plan, opened page, login, populated form, saved draft, email delivery, upload percentage, toast, or stale screenshot is activity—not progress—unless a fresh backend or public-page check proves a state transition.

After any mutation, leave the transient success screen, re-open the application/version record, and read the resulting state. If that independent check is missing, report the action as `unverified`; never promote it to `uploaded`, `submitted`, `in-review`, or `published`.

Polling must track a concrete portal record, submission ID, processing job, or public URL. Repeating the last known status without a fresh authoritative check is not a verified wait. When a state exceeds the channel's normal window, inspect hidden banners/messages/agreements and take the next safe action; do not keep saying “waiting” indefinitely.

## Closed-loop operating cadence

Publishing work always has priority over documentation. Repeat this loop until the requested terminal state is reached: read the authoritative backend state, take every currently available action, independently re-open and verify the resulting record, then use unavoidable processing or review time to update evidence and lessons learned. Documentation, screenshots, or reports must never pause an actionable upload, metadata fix, build selection, review submission, or rejection remediation.

Maintain a monotonic ledger for every product/channel row: source commit, channel flavor, marketing version, build number, artifact SHA-256, upload/delivery ID, portal record ID, last verified state, checked-at time, blocker, and exact next action. A duplicate-build response is not a generic failure: query the existing build and reuse it only when the product, platform, version/build, eligibility, and intended source identity are proven; otherwise increment the build number and rebuild.

For Flutter desktop products, use separate worktrees and separate build/cache directories for store and direct variants. Perform a clean build whenever compile-time distribution flags change. After building, inspect the produced binary or manifest for the intended channel marker so stale incremental output cannot silently ship the wrong feature policy.

For Apple macOS, distinguish the development-signed archive from the exported App Store package. Verify the export summary and every embedded executable, helper, login item, and extension for architectures, sandbox entitlements, App Groups, provisioning, bundle identifiers, minimum OS, and distribution signing. Missing helper dSYMs are recorded separately from blocking validation errors. A successful binary upload still requires selecting that exact processed build on the version, completing metadata/compliance, and explicitly submitting the version for review.

For browser portals, verify that automation controls the authenticated browser profile before acting. If the automation path fails, immediately continue all CLI/API/build work and expose only the smallest unavoidable login, CAPTCHA, MFA, or legal gate; do not mislabel an automation outage as a channel outage. After submission, navigate away from the success toast and re-open the version record before advancing its state.

## Execution order

1. Freeze an identified source commit and preserve unrelated local changes.
2. Build channel-specific variants without weakening the ordinary/direct build.
3. Run automated tests, platform-native install/launch tests, and signature/package inspection.
4. Create immutable artifacts, SHA-256 files, screenshots, release notes, and rollback copies.
5. Upload the exact approved artifact; record the upload/delivery ID immediately.
6. Complete all listing metadata and explicitly submit for review.
7. Re-open the portal and verify the exact app/version/build state.
8. After publication, download from the public listing, verify its hash/version, install it, launch it, and exercise the core workflow.

## Portal identity lock

Treat every browser form and upload as a four-part identity: `product + platform + version/build + artifact SHA-256`. Write those four values into the release record before opening a portal. Immediately before selecting a file, saving a draft, submitting for review, or publishing, re-read the visible form and verify all four parts. After the action, return to the dashboard or version detail page and verify the same product and platform together with the resulting state. Abort on any mismatch; a listing created for the wrong platform is not progress for the requested target.

Use one clearly named browser tab per product/platform and only one active operator per publisher portal. A shared browser profile, native file picker, or mutable tab must not be driven concurrently by another task. If another task owns the portal, coordinate and wait or do non-browser work. After every browser interaction, refresh the page state and derive new element targets; never reuse stale indices or assume a toast changed the backend state.

## Non-negotiable invariants

- Never weaken, overwrite, or silently alter the normal internal/direct build to satisfy an external store. Isolate channel-specific behavior behind explicit build flavors or compile-time flags and test both variants.
- Preserve truthful functionality. Do not use dates, launch counts, remote flags, geofencing, or reviewer detection to reveal undisclosed features after review. For a restricted feature, disclose it, permanently omit it from that channel, or satisfy the channel policy.
- Keep About, support, privacy, terms, version, and contact information reachable without login unless the channel explicitly permits otherwise.
- Do not expose passwords, tokens, signing keys, session cookies, provisioning profiles, or verification codes in logs, commits, screenshots, or reports.
- CAPTCHA, MFA, legal attestations, paid enrollment, tax/banking agreements, and license acceptance remain human gates. Bring the exact prompt to the foreground and continue all independent work before asking.
- Browser actions that submit a listing, upload a binary, send a reviewer message, accept terms, or publish are external mutations; obtain action-time authorization when required by the active environment.
- Never replace an existing public binary until version monotonicity, platform/architecture, signature, hash, and rollback artifact have been verified.
- Never make up download counts, review progress, submission IDs, signing status, or publication results. Re-check the exact portal/listing and timestamp every report.
- Never count an unintended platform draft, a support request, an editorial acknowledgement, or a private dashboard card as a successful submission for another product/platform.
- Never store or repeat plaintext passwords, OTPs, recovery codes, session cookies, API keys, or signing secrets in skills, repositories, screenshots, shell history, or release reports. Record only the non-secret account/team identifier and where the approved credential is managed.
- Never call a channel complete while its evidence row has an empty public URL, mismatched product/platform/version, missing artifact identity, or a state weaker than the user's requested terminal state.

## Definition of done

Return a channel matrix with listing URL, app/version/build, artifact hash, signing/notarization result, upload/submission ID, state scope, review status and timestamp, blockers, next action, and evidence path. A channel is complete only when its requested terminal state is actually reached. For public distribution, `published` additionally requires an anonymous public listing, the intended downloadable version, and a post-publication download/install/launch check when the channel permits it.

## Operator cleanup

Track every browser tab, temporary browser session, foreground application, test process, tunnel, and temporary artifact created by the distribution run. Keep publisher pages in the background except while an unavoidable human gate is active. After each portal action, close only the task-owned tab when it is no longer needed; never close pre-existing user tabs. At the end of a run, stop task-owned test processes and tunnels, remove or archive only disposable temporary artifacts according to the project policy, restore any application temporarily stopped for validation, and record the cleanup result. A successful upload or submission does not waive this cleanup gate.
