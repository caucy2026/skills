# Apple, Uptodown, Softonic, and SourceForge field lessons

Read this reference when operating these four public-distribution channels. It captures failure modes that are easy to misread and the checks that prevent false progress.

## Shared operating pattern

Create one ledger row for every `product + platform + channel`. Before opening a portal, freeze the exact product, platform, marketing version, build number, artifact filename, byte count, SHA-256, signing/notarization result, source commit, and intended account/team. Never allow one product's browser tab or file picker to supply another row.

For each portal mutation:

1. Re-read the visible product and platform.
2. Select the already verified artifact by absolute path.
3. Re-read the selected filename and visible version before confirming.
4. Perform the authorized mutation once.
5. Treat the immediate toast or error as provisional.
6. Leave the form, reopen the dashboard or exact version record, and use that persistent state as the result.
7. Capture a screenshot or machine-readable response containing product, platform, version, and state together.

Do not retry blindly after a generic error. A portal may commit the mutation and then fail while refreshing the form. First inspect the dashboard for a new record or state transition; otherwise a retry can create duplicates.

## Account, password, CAPTCHA, and verification-code handling

- Use an existing authenticated browser profile or the approved password manager. Store only the non-secret account identifier, publisher/team name, portal URL, and credential-location label in the ledger.
- Never put a password, OTP, recovery code, session cookie, API key, signing private key, or browser-storage value in this skill, a repository, a release report, a screenshot, a command, or chat output.
- Do not infer that a remembered password is current. Distinguish `invalid password`, `CAPTCHA incomplete`, `MFA required`, `session expired`, `account locked`, `missing role`, and `agreement pending` from the exact portal message.
- If a page says both “complete CAPTCHA” and “valid username/password,” solve neither by repeated password retries. Stop at the CAPTCHA or account-recovery gate and preserve the rest of the prepared workflow.
- If an authorized mailbox connector is already installed and the user explicitly placed that mailbox in scope, it may be used to find a fresh verification message. Otherwise bring the code field to the foreground for the account holder. Never scrape mail, browser storage, Keychain, or cookies to obtain a code.
- While the user is typing a CAPTCHA, password, OTP, or account-recovery answer, do not click, type, refresh, hide, or switch the same window. Resume only after the user says the gate is complete, then fetch a fresh portal state.
- Do not save a password into the browser or create a persistent credential without the action-time authorization required by the environment. Existing saved credentials may be used through the normal password-manager UI.
- On successful login, verify the publisher organization/team before editing any app. A valid login to the wrong team is not progress.
- CAPTCHA, MFA, legal ownership attestations, paid enrollment, banking/tax forms, and account recovery remain human gates. Consolidate them into the smallest foreground handoff; all other preparation, submission, polling, and evidence work stays automated.

## Apple App Store Connect

### Browser route on the KEMI publisher Mac

- Use Google Chrome profile `niu` as the established App Store Connect route for login, saved credentials, build attachment, metadata, submission, and status inspection. Preserve one tab per App.
- Do not begin with Safari or switch browsers during an active submission unless the user explicitly requests it or Chrome is unavailable and an authenticated Safari session has already been verified. Authentication trouble is a session gate, not a reason to change the proven release route.
- Keep binary delivery separate from portal operation: upload the Apple Distribution-signed App Store package with Apple's official Xcode/command-line transport, then use Chrome `niu` to attach the processed build and submit the exact version.

### Submission identity

Record App ID, bundle ID, platform, marketing version, build number, processed-build identity, and submission ID separately. An uploaded build is not the submitted version; a selected build is not an in-review submission.

### Store-specific binary rules

- Use an isolated App Store flavor. Restricted capabilities must be permanently absent from that flavor, not hidden by launch count, date, reviewer detection, remote flag, or post-review activation.
- Verify every helper, login item, extension, and embedded executable for App Sandbox, provisioning, App Groups, minimum macOS, architectures, and distribution signing.
- Inspect the exported App Store package, not only the development-signed archive. Record the export summary and the exact package hash.
- After upload, wait for processing, select that exact build, finish export-compliance/privacy/metadata fields, submit the version, then reopen the version page and verify `Waiting for Review`, `In Review`, or the channel's current equivalent.

### Status interpretation

- Apple Lookup API `resultCount: 0` proves only that no anonymous public listing is available. It does not prove rejection or describe the App Store Connect review state.
- A long `Waiting for Review` state is not rejection. Do not withdraw or replace an otherwise valid submission merely to upload newer code; withdrawal restarts the queue.
- If the published normal review window is exceeded, inspect Resolution Center, agreements, export compliance, privacy answers, and unresolved banners. Submit an official status inquiry only when authorized, and require a success page or case ID. A generic support-form error with no case ID means the inquiry was not sent.
- If a submitted version is already in review, prefer waiting over replacing it unless Apple rejects it or a blocking defect makes the submitted binary unsafe.

## Uptodown

### Browser requirement on the KEMI publisher Mac

- Use Google Chrome profile `niu` for Uptodown login, CAPTCHA, and publisher-console work. Safari authentication has repeatedly failed on this workstation, so do not open or retry the Uptodown authentication flow in Safari.
- When human CAPTCHA input is required, foreground only the Chrome Uptodown tab, stop all automation on that window, and resume from a fresh authenticated state after the account holder says the gate is complete.

### Two-scope state model

Always record both:

- application/listing state, such as `PENDING REVISION`;
- exact file state, such as `PENDING REVIEW`, together with file ID, size, version, hash, and flags such as `published`, `rejected`, or `readyToReview` when exposed.

Do not merge them. A listing can remain `PENDING REVISION` while its exact binary is already accepted into editorial review. A disabled `SUBMIT FOR REVIEW` button plus a pending exact-file record can mean the platform is processing the submission, not that the operator forgot to click.

### Verification and failure handling

- Reopen Information, Descriptions, Screenshots, and Files. Record which screenshots say `Pending approval`, which descriptions are present, and the exact file state.
- Check portal notifications for hidden rejection or required-action messages before declaring a verified wait.
- Public-page absence, timeout, or search-engine absence proves only “not publicly reachable.” It does not prove rejection.
- When the login error mentions CAPTCHA, do not keep changing or retrying the password. Complete the CAPTCHA through the human gate, then retry once and verify the authenticated app identity.
- Never count a different application ID or similarly named product as evidence for the intended product.

## Softonic Publishing Center

### Browser and locale lock on the KEMI publisher Mac

- Use Google Chrome profile `niu` and verify the exact Mac product card before editing.
- The declared locale and every screenshot in that locale must match. English (United States) metadata requires English UI screenshots; put Chinese UI screenshots only in a Chinese locale block. A locale mismatch is a rejection that requires corrected screenshots and resubmission, not passive waiting.

### macOS package preparation

- Confirm the form's package requirement before upload. A signed and notarized ZIP may still be rejected as “invalid file” or “must be executable”; for macOS, prepare the accepted DMG or PKG format when the portal requires it.
- For a DMG, sign the contained app and the DMG as required, notarize the final distributable, staple the ticket, run Gatekeeper assessment, and calculate the final SHA-256 after stapling because stapling changes bytes.
- If the portal taxonomy offers only `Mac OS X`, use that platform label but state the truthful minimum supported version, architectures, and requirements in the description and release record.
- If screenshots require a larger canvas, resize or letterbox a truthful product screenshot without inventing controls or functionality. Record the transformation and retain the source image.

### Draft and submission behavior

- Softonic may show multiple entries with the same product name for Windows and Mac. The platform label on the dashboard is part of the identity lock; a Windows `UNDER REVIEW` card never proves the Mac submission.
- Save the draft and reopen it before final submission to prove the metadata and binary persisted.
- A final submit action may return a generic “error while saving changes” even though the backend accepted the submission. Before retrying, return to `My Apps` and inspect the product/platform card. If it persistently shows `UNDER REVIEW`, record the submission as `in-review` and do not create or submit a duplicate.
- Conversely, a disabled Submit button on a still-loading form is not proof of review. Only the dashboard or exact version record can advance the state.
- Record application UUID and version UUID from the canonical URL when exposed.

## SourceForge Business Software

### Correct route

Distinguish the Business Software vendor-listing request from open-source project hosting. A proprietary application must not be misrepresented as an open-source project just to obtain a download page.

On the KEMI publisher Mac, use Chrome profile `niu`. Do not create a SourceForge open-source project as a workaround when the Business Software onboarding is incomplete or blocked.

### Initial request semantics

- The vendor form can request a commercial/business listing without accepting the binary during the first step. Fill truthful company contact, website, product title, square logo, product description, audience, the most specific category, starting price, free/support/training options, and platform.
- Category examples: an AI developer toolkit can use `AI Development`; a local transfer utility can use `File Sharing` when those exact catalog choices exist.
- The final checkbox may combine Terms of Use, Privacy Policy, and consent to receive communications. Treat it as a legal/communications gate according to the active environment and obtain the required action-time authorization.
- After Submit, an invisible reCAPTCHA notice can appear without a puzzle. Wait for navigation, then verify the canonical success URL and text.
- `/software/vendors/new_submitted` with `Request Received` and `THANKS!` proves the listing request was received. It does not prove a product page, binary upload, or public distribution. Until SourceForge creates/approves the listing, record `submitted` or `in-review` at the onboarding-request scope, never `published`.
- If no request ID is provided, keep the checked-at timestamp, success URL, product/platform payload summary, and screenshot. Later email or product-page creation must be tied back to that row.

## Preventing false progress

The following are not terminal success:

- login completed;
- form opened or fully populated;
- file selected in a native picker;
- upload progress reached 100%;
- draft saved;
- transient success toast;
- onboarding email delivered;
- authenticated dashboard card without a public page;
- similarly named third-party result found in search;
- public URL timing out;
- status copied from an earlier screenshot.

For public distribution, the terminal gate remains: anonymous product page, intended version available, public artifact downloaded, identity/hash or documented catalog-repackaging difference verified, clean install completed, app launched, and a core workflow exercised. Keep the row active and continue polling until this gate is met or the user explicitly changes the target.

## Browser ownership and cleanup

- Use one tab per `product + platform + channel`, with one operator at a time.
- Fetch fresh accessibility/DOM state after every interaction because field indices can shift after validation, autofill buttons, uploads, or dynamic counters appear.
- Native file dialogs are process-global. Never batch file-picker operations across products; re-read the selected absolute path immediately before confirming Upload/Open.
- Keep portal work in the background except during an unavoidable human gate. When the user begins interacting, stop automation on that window.
- Close only task-created tabs that are no longer required. Preserve pre-existing user tabs and keep a dashboard tab only when it is the active monitoring anchor.
- Stop task-created test processes/tunnels and archive or delete only disposable artifacts under the project's cleanup policy. Record what remained open and why.
