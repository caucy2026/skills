# Evidence and release ledger

Maintain one row for every `product + macOS + Apple App Store + version/build`. Never overwrite historical rows when a new build is created.

## Required fields

```text
product:
sourceCommit:
bundleId:
appleAppId:
marketingVersion:
buildNumber:
minimumMacOS:
architectures:
channelFlavor:
archivePath:
exportedPackagePath:
packageByteCount:
packageSHA256:
appleTeam:
signingIdentityLabel:
profileNameOrUUID:
uploadOrDeliveryId:
processedBuildId:
submissionId:
submittedAt:
lastCheckedAt:
state:
resolutionCenterIssue:
supportCaseId:
publicUrl:
evidencePaths:
blocker:
nextAction:
```

Do not record passwords, OTPs, recovery codes, cookies, tokens, API private keys, private signing keys, profile contents, or exported credentials.

## Evidence requirements

- Build evidence: source commit, archive/export log, entitlement/signature/provisioning inspection, architecture and deployment-target check, tests, final package byte count and SHA-256.
- Upload evidence: official delivery ID and the exact processed build visible in App Store Connect.
- Submission evidence: exact version page persistently showing queued/in-review state and submission ID after reload/reopen.
- Rejection evidence: exact current submission plus guideline/message and Resolution Center timestamp.
- Published evidence: signed-out/private anonymous product page, intended public version, install result, launch result, and a core workflow check.

Screenshots must visibly bind product, platform, version/build, and state. A cropped badge without product/version context is supporting evidence only. Use timestamps and descriptive names; redact unrelated personal information.

## Report format

Report the weakest state actually proved:

| Product | Version/build | Package SHA-256 | Processed build | Submission ID | Persistent state | Checked at | Evidence | Blocker/next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

If a required field is unknown, write `unknown` and explain how it affects confidence. Never fill it from memory when a live record is available.

