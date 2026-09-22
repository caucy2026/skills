# Submission troubleshooting

## Portal and authentication

- Read the exact error before changing credentials. CAPTCHA incomplete, invalid password, expired session, missing role, and unaccepted agreement are different blockers.
- Retry only after correcting the identified cause. Avoid lockouts and never attempt CAPTCHA bypass.
- If the session is authenticated but a button does nothing, inspect required fields, browser validation messages, network response, and portal status; do not assume submission succeeded.
- If a submit action shows a generic save/network error, do not immediately resubmit. Navigate to the dashboard or exact version record and check whether the backend state nevertheless changed. Record the persistent state; retry only when no matching mutation exists.
- If a form returns a success page without a request ID, preserve the canonical success URL, timestamp, product/platform payload summary, and screenshot. Keep its state scoped to the request or onboarding record, not the final public product.
- If the wrong platform or file appears, stop before saving. Re-check which task owns the browser, close or release any native file picker, obtain a fresh page state, and restart from the intended product/platform record. Never repair the mistake by overwriting an unrelated live listing.

## Shared-browser failures

- Only one task may operate a given publisher portal at a time. Name the browser task and coordinate ownership before opening a file chooser.
- Native file choosers are process-global enough to receive input from the wrong task. Select and verify the filename within the same controlled flow; after upload, verify the visible filename, version, platform, size, and hash where the portal exposes them.
- Re-fetch the accessibility/DOM state after every action. Reusing element indices after navigation, validation, or another task's interaction can target a different control.
- If browser control repeatedly times out, preserve current drafts, release the portal, and continue only read-only/public checks or local artifact preparation. Do not claim the pending browser step completed.

## Package rejection

- Signing: confirm identity type, trust chain, timestamp, nested code, profiles, bundle IDs, and capability match.
- Version: confirm public/current version and monotonically increasing platform build number.
- Architecture/OS: inspect the package, not just project settings.
- Malware/reputation: reproduce on a clean machine and submit false-positive evidence through the vendor process; do not disable security controls.
- Metadata: verify product-specific support/privacy URLs, screenshots, description, contact data, and category.
- Policy: isolate the smallest compliant channel change, then regression-test direct/internal builds.

## Stalled states

If a status remains unchanged, compare against the channel's current normal processing/review window, verify there is no hidden action banner, unread message, agreement, or missing export-compliance/privacy response, and capture the checked timestamp. Escalate through official support with app ID, version/build, submission ID, and screenshots. Do not claim rejection from delay alone.

Do not treat an automation heartbeat as proof that the portal was checked. A verified wait requires a fresh read of a concrete portal record, job handle, submission ID, or public URL. Apply the anti-stall watchdog in [proof-and-account-operations.md](proof-and-account-operations.md); after repeated no-progress cycles, take the next safe action or surface the single genuine blocker instead of recycling the same status text.

## Safe retries

Never overwrite the last known-good artifact. Increment the build number for a changed Apple binary. Recompute checksums after any byte change. Link every retry to its source commit, previous failure, correction, tests, and new submission ID.
