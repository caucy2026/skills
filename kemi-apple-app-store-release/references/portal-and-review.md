# App Store Connect operation and review handling

## Established browser route

On `/Users/newlink`, use Google Chrome profile `niu`. It is the field-verified route for the Apple publisher session, saved-login UI, build attachment, metadata, submission, and status checks. Use one task-owned tab per App. Do not switch to Safari during an active release unless Chrome is unavailable and the alternate session has been independently verified.

Try, in order: existing authenticated session; normal Chrome password-manager autofill; then the exact human gate Apple presents. Do not ask for passwords already available through the approved session, do not scrape credential databases, and do not retry guessed passwords. MFA, trusted-device approval, recovery, legal agreements, tax/banking, and license acceptance require the account holder.

While the user is entering a code or handling a human gate, do not click, type, refresh, hide, or switch that window. When the user finishes, fetch a fresh page state, verify team/App/version again, resume automatically, and return the portal to the background.

## Mutation verification

Before upload selection, build attachment, Save, Submit for Review, reply, or withdrawal, verify visible `product + macOS + version/build + Apple App ID`. After the action:

1. treat the toast as provisional;
2. navigate away or reload;
3. reopen the exact version/submission;
4. record persistent state, processed build, submission ID, time/timezone, and screenshot;
5. mark `unverified` when the backend record does not persist.

Do not withdraw, replace, or create a newer submission when the current exact version is healthy and waiting/in review unless Apple rejects it or a blocking defect makes it unsafe.

## Status interpretation

| Visible evidence | Record as | Meaning |
| --- | --- | --- |
| Build appears under TestFlight/processing | `processing` | Uploaded build is not yet eligible or not yet attached/submitted. |
| `准备提交` / Prepare for Submission | `uploaded` at most | Version draft exists; final submission did not happen. |
| Persistent `Waiting for Review` / `正在等待审核` with exact submission | `in-review` | Apple received it and queued it. |
| `In Review` | `in-review` | Active review. |
| Resolution Center/current submission explicitly rejected | `rejected` | Remediation is required. |
| Red exclamation badge only | inspect | It may be a current issue or historical message; do not classify from icon alone. |
| `Ready for Distribution` / `可分发` | approved/deliverable | Still verify public availability. |
| Anonymous product page with intended version | `published` after install check | Public distribution proved. |
| Lookup API `resultCount: 0` | not publicly visible | It says nothing about backend review/rejection. |

## Review delay

A long wait is a verified wait, not a rejection. Refresh the exact submission and inspect Resolution Center, agreements, export compliance, privacy answers, app-review messages, and required-action banners. Compare with Apple's current published review guidance; never invent an SLA.

If the normal window is exceeded and status inquiry is authorized, use Apple's official App Review Status contact path. Include App ID, platform, version, build, submission ID, submitted-at time, current state, and a concise request to confirm whether developer action is needed. A form error without a success page or case ID means the inquiry was not sent. Record the case ID only after the backend confirms it.

## Rejection patterns observed

- Unnecessary inbound-server entitlement: remove it when the App Store feature only initiates outbound connections; retain client networking and retest. This was the minimal correction used for a KEMI OFFICE App Store candidate.
- Missing/placeholder icon: validate AppIcon contents, target selection, 1024 icon, archive contents, and processed build before resubmitting.
- Invalid support or privacy URL: use public, product-specific pages that work without authentication.
- Reviewer cannot reach a feature: provide deterministic steps and test credentials only when required; do not rely on internal network state.
- Locale mismatch: every localized screenshot and text block must match its declared locale.
- Uploaded but never submitted: attach the processed build, complete all required fields, explicitly submit, and verify a persistent review state.
- Overbroad entitlements: remove unused capability, explain the remaining one in review notes, rebuild with a higher build number, and verify the exported package.

## Reviewer reply structure

Keep replies factual:

```text
App / platform / version / build / submission ID
Guideline or issue addressed
Exact code/configuration change
Exact user-visible behavior now
Navigation steps for reviewer
Permissions requested and why
Test account only if required
```

Do not promise behavior that is absent, argue from another channel, or call a fix complete before the corrected build is attached and resubmitted.

