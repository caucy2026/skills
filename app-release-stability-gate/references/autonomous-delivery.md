# Autonomous delivery loop

Use this reference only when the user requested a release, publication, upload or other delivered artifact.

## Delivery state machine

Persist these states in `run-state.json`:

`PASS → SIGN/PACKAGE → REFREEZE → FINAL-SMOKE → UPLOAD → DESTINATION-READBACK → CLIENT-UPDATE/INSTALL → OPEN → RECEIPT`

Any byte-changing step returns to `REFREEZE`. Run the identity, trust, install/upgrade, startup and critical historical packaging cases on the final bytes. Never upload an unsigned or pre-notarization hash merely because an earlier build passed.

## Automatic execution

Select and read the matching project/platform release skill. Reuse previously authorized destination, account, application record, signing route and release channel when scope and risk are unchanged. Prefer updating the existing application record over creating a duplicate. Continue through ordinary retries without asking the user to click, copy files or collect logs when an authorized tool path exists.

External boundaries such as MFA, CAPTCHA, hardware-token touch/PIN, unavailable entitlement or a legally required declaration remain `BLOCK`. Complete every independent build, metadata, package and validation step before surfacing that blocker.

## Destination assertions

Require all applicable evidence:

- destination application/record ID and channel;
- uploaded file byte count and SHA-256;
- server/store/CDN readback byte count and SHA-256;
- visible semantic version and platform build/version code;
- update comparison from the previous production build;
- install or in-place upgrade from the customer-visible path;
- application open and critical smoke after delivery;
- rollback artifact identity and a tested or documented rollback command/path.

A successful HTTP response, portal toast, processing state or file listing is an intermediate result. Delivery is complete only when the destination preserves the intended record and the customer path resolves to the frozen bytes. Store review queues may end in `SUBMITTED/IN_REVIEW` rather than `PUBLISHED`; report the exact state without upgrading its meaning.

## Failure behavior

- Metadata or upload rejection: correct the smallest confirmed cause and retry the same record.
- Destination bytes differ: stop rollout, preserve both hashes, restore the prior manifest/record when the release skill permits safe rollback, then diagnose.
- Store compares only a platform build number: verify both user-facing version and platform build/version code; a higher marketing version alone is insufficient.
- Delivered app fails install, upgrade or open: mark release `BLOCK`, roll back when authorized and safe, add a permanent regression, repair, rebuild and repeat the full final-byte gate.

## Delivery receipt

Write JSON and Markdown receipts tied to the gate decision. Include the candidate, test decision, delivery states, timestamps, destination evidence, post-delivery client result and remaining review/external blockers. The receipt must make it possible for another agent to resume without repeating completed uploads or guessing which record was changed.
