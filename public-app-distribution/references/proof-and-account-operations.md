# Publication proof and publisher-account operations

Read this reference before using a live publisher account, monitoring a submission, or reporting release progress.

## Evidence ladder

Use the weakest state actually proved by fresh evidence:

| State | Required authoritative evidence | Evidence that is insufficient |
| --- | --- | --- |
| `not-started` | No matching product/platform record exists | A plan, prepared package, or account registration |
| `blocked` | Exact blocking page/message plus product/platform and checked-at time | A generic timeout or an assumption about credentials |
| `uploaded` | Exact file/version record showing accepted bytes, with size/hash when exposed | File picker selection, upload progress, or success toast |
| `processing` | Portal-side processing/scanning state tied to the exact file/version | A local build still running |
| `submitted` | Fresh application/version page showing it was explicitly sent, ideally with submission ID/time | Saved draft, onboarding email, or enabled Submit button |
| `in-review` | Exact product/platform/version page or dashboard row explicitly showing queued/under review | A different platform entry or old version under review |
| `rejected` | Exact reviewer issue/status tied to the submitted version | Search-engine absence or a long wait |
| `published` | Anonymous public product page plus intended version/build downloadable | Authenticated dashboard card, editorial acknowledgement, or upload receipt |

For channels with app-level and file-level states, record both without merging them. Example: an application can be `pending revision` while one exact file is `pending review`.

## Two-phase verification for every mutation

1. Before the action, capture `product + platform + version/build + artifact SHA-256` and the visible target account/team.
2. Perform only the authorized upload/save/submit action.
3. Treat any toast or progress bar as provisional.
4. Navigate away or reload, then re-open the exact application/version record.
5. Record the persistent backend state, application/listing ID, file/version ID, submission ID when available, checked-at timestamp/timezone, and a screenshot showing the identity and state together.
6. If the persistent state is absent or contradictory, mark the action `unverified`, preserve the draft, and troubleshoot. Do not claim success.
7. After publication, use a signed-out/private session or public HTTP fetch to prove anonymous visibility. Download the public artifact, verify version/size/hash or document a catalog repackaging difference, then install and launch it.

## Anti-stall progress watchdog

Maintain one row per `channel + product + platform`. Each poll must update `lastCheckedAt` from a fresh portal record, processing job, submission ID, or public URL.

- A changed backend state, completed gate, corrected submission, or new authoritative evidence is progress.
- A fresh poll of a live record with unchanged state is a verified wait.
- Repeating a cached status, plan, email receipt, screenshot, or local note is no progress.
- On the first no-progress cycle, refresh the authoritative record and inspect messages, required fields, agreements, export/privacy answers, and disabled controls.
- On the second consecutive no-progress cycle, take the next safe independent action: inspect the exact version detail, validate the artifact, prepare a support case, or switch to another unblocked channel.
- On the third consecutive cycle with the same genuine blocker, stop restating status. Escalate through official support when already authorized, or report the one specific user/portal action that is indispensable.
- When normal review time is exceeded, record the channel's published SLA/source, submission age, support case ID, and next follow-up time. Never invent an SLA or call delay a rejection.

## Background account operation

- Default to automation-first execution. Complete discovery, artifact validation, metadata preparation, field population, upload preparation, read-only status checks, rejection analysis, corrective builds, evidence capture, and release-record updates without asking the user to repeat known information.
- Keep a human-intervention budget per channel. Consolidate unavoidable human gates into the smallest possible number of foreground handoffs, normally one authentication/legal gate and one final action-time confirmation when the environment requires it. Do not request confirmation for read-only checks, reversible preparation, or information already available in the repository or portal.
- Before requesting human action, verify that the gate is currently visible and is truly indispensable. State exactly one action, where it is needed, and what will resume automatically afterward. Do not ask the user to navigate, search, copy routine metadata, or monitor review status on the agent's behalf.
- After the user completes a gate, resume from a fresh portal state automatically; do not ask whether to continue. Revalidate the identity lock, finish the remaining authorized workflow, restore/hide the browser, and keep monitoring until the requested terminal state.
- If a login session expires, first try the official session-resume flow and existing approved password manager. Never guess or brute-force credentials. Bring the login forward only when the portal actually requires CAPTCHA/MFA/account recovery.
- Use the publisher's existing authenticated browser session or approved credential manager. Do not scrape passwords, browser storage, cookies, keychains, or email tokens.
- Release records may contain the publisher account/team name, non-secret login identifier, portal URL, app/listing IDs, and the credential location label such as “browser password manager”; they must not contain the credential itself.
- Distinguish invalid credentials, expired session, CAPTCHA, MFA, missing role, unaccepted agreement, and legal attestation from the exact screen. Do not retry a password when CAPTCHA is the actual blocker.
- CAPTCHA, MFA, account recovery, legal ownership declarations, paid enrollment, tax/banking agreements, and license acceptance are human gates. Prepare all independent fields first, bring only the exact gate to the foreground, and hide the browser again immediately afterward.
- One operator owns a publisher portal at a time. Before switching a shared browser tab, record the active tab/window and confirm no file chooser or submission is in progress; restore the previous tab after a read-only check.
- File pickers are process-global. Immediately before confirming a file, re-read the selected absolute path and match it to the identity lock. Abort if it belongs to another product/platform.
- After each browser action, refresh the accessibility/DOM state and derive new controls. Never reuse stale element indices.
- Prefer read-only API/CLI status endpoints when officially supported, but do not bypass CAPTCHA/MFA or export live session credentials to create an unofficial API.

## Credential record format

Keep credential material separate from release evidence. The release ledger may record only:

```text
portal: <canonical publisher URL>
accountIdentifier: <non-secret email or username>
organizationOrTeam: <publisher organization/team>
credentialLocation: <existing browser profile or approved password-manager item label>
mfaMethod: <non-secret label such as account-holder device or mailbox>
lastAuthenticatedAt: <timestamp and timezone>
sessionState: authenticated | expired | captcha-required | mfa-required | recovery-required
```

Do not add a password field, OTP value, recovery code, cookie, token, keychain export, or signing-key material. If a user sends a password or code in chat, use it only for the authorized live gate when policy permits; never copy it into the skill, ledger, shell history, screenshots, reports, commits, or follow-up messages.

Use this recovery order when authentication fails:

1. Read the exact portal error and classify the gate.
2. Reuse an existing authenticated session if it is still valid.
3. Invoke the approved password manager through its normal UI when available.
4. Use an explicitly authorized mailbox connector only for that mailbox and only for a fresh verification message.
5. Otherwise foreground the exact CAPTCHA/MFA/recovery control for the account holder, without exposing other tabs or data.
6. After the gate, refresh the portal and verify the organization/team before resuming automatically.

Never loop password submissions. One retry after correcting the exact blocker is enough; subsequent failure requires reclassification or account recovery rather than guessing.

## Automation completion contract

The agent owns the workflow after a human gate. It must:

1. confirm the portal returned to the intended account/product/platform;
2. resume the exact pending step without a new “continue?” question;
3. verify the persistent backend state after every mutation;
4. schedule or perform fresh polling against a concrete record;
5. remediate rejected metadata or binaries within the authorized scope;
6. report only meaningful state changes, failures, or the next indispensable human gate;
7. keep the task incomplete until the requested public listing and downloadable artifact are independently verified.

Automation is not complete because a browser action ran, a form was filled, or an upload request returned. It is complete only when the channel's requested terminal state and post-publication checks are proved.

## Screenshot and release-record requirements

Screenshots support a claim only when they visibly include enough context to bind product, platform, version/build, and state. Name evidence files with channel, product, platform, version/build, state, and timestamp. Redact account email, personal names, IDs unrelated to the release, and secrets.

On macOS systems with multiple Spaces or browser profiles, an automation API reporting an active tab is not enough to prove that the visible captured window is the same tab. Before accepting a screenshot, verify that the captured image itself shows the intended portal, product, platform, version, and state. Discard screenshots of another Space, profile, tab, or application even when the browser API returned the expected URL.

For each status report, record:

- channel and authenticated/public URL;
- product, platform, version/build, artifact filename, byte count, and SHA-256;
- application/listing ID, file/version ID, and submission ID when available;
- separate application-level and file-level states;
- exact checked-at time and timezone;
- screenshot or machine-readable response path;
- blocker and the next concrete action/owner;
- whether the check was fresh, a verified wait, or no progress.

If any required identity field is missing, say so explicitly. Missing evidence lowers confidence; it never upgrades the state.
