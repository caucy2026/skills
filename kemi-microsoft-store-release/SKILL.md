---
name: kemi-microsoft-store-release
description: Build, sign, submit, remediate, monitor, and verify KEMI Windows desktop applications in Microsoft Store Partner Center using isolated Store-only variants and the established KEMI publisher workstation. Use for KEMI Remote Office or KEMI Send Microsoft Store releases; do not use for Common, the KEMI internal market, Chocolatey, Uptodown, or Softonic.
---

# KEMI Microsoft Store release

Deliver a signed, policy-compliant KEMI Windows Store-only build to Microsoft Partner Center and prove its persistent review or publication state. A package upload, saved draft, validation run, or success toast is not completion.

## Required reading and routing

1. Read the repository `AGENTS.md` and current release ledger before acting.
2. Read [references/end-to-end.md](references/end-to-end.md) for every release or rejection correction.
3. Read [references/kemi-known-products.md](references/kemi-known-products.md) only for the existing KEMI Remote Office and KEMI Send records, known failures, and verified artifacts.
4. Read [references/evidence-record.md](references/evidence-record.md) before reporting progress or updating the ledger.
5. Use `kemi-windows-device-lab` for Windows native build, install testing, and local Authenticode inspection. Use `kemi-windows-remote-signing` only when hardware-token signing must be driven through the established remote simulator.
6. Use `public-app-distribution` for shared public-store proof rules. This skill supplies the KEMI Microsoft Store specialization.

## Non-negotiable identity lock

Before build selection, CDN upload, Partner Center package editing, or submission, write and verify:

```text
product:
platform: Windows
channel: Microsoft Store
sourceCommit:
marketingVersion:
buildNumber:
artifactAbsolutePath:
artifactByteCount:
artifactSHA256:
partnerProductId:
partnerPackageRecordId:
publisherAccount: caucy2002@163.com
```

Abort on any mismatch. Reject cached Microsoft sessions and autofill for `caucy2026@outlook.com`; the authorized publisher identity for these products is `caucy2002@163.com`.

## Store-only flavor rule

Keep the ordinary/direct application intact. Build a permanent, explicit Store-only flavor in an isolated worktree and cache directory. The Store flavor may permanently remove or alter features that violate Store policy, but must never hide them temporarily for review or enable them later by date, launch count, remote flag, geography, or reviewer detection.

For the current products, Store policy requires the installed product identity and publisher to match the listing and forbids in-app promotion of acquiring software outside Microsoft Store. Confirm the Store artifact contains the intended distribution marker and does not expose the removed app-market navigation before signing.

## Release contract

Follow this order without skipping gates:

1. Freeze source and create an isolated Store-only version/build.
2. Build on the trusted Windows node using the D-drive-only paths defined by the device-lab skill.
3. Verify file/product metadata, Add/Remove Programs identity, architecture, silent install arguments, and Store-only feature policy.
4. Sign every embedded PE and the final outer installer in the interactive hardware-token session. Verify certificate identity, trust, timestamp, and `Valid` status for every PE.
5. Run clean installation, launch, core-workflow, upgrade where applicable, and uninstall checks on Windows. Do not upload an artifact that has only passed signature inspection.
6. Preserve the final artifact, byte count, SHA-256, source commit, signing report, test evidence, and rollback copy.
7. Upload only that exact immutable Store-only artifact to a separate CDN object. Do not modify Common or KEMI internal-market resource records.
8. Download the CDN URL anonymously and prove byte count and SHA-256 match the signed local artifact.
9. In Partner Center, verify account, product ID, package record ID, version/build, architecture, installer type, URL, and silent arguments before saving.
10. Save the package draft, run package validation, complete listings/ratings/availability/policy fields, and submit.
11. Leave the submission surface, reopen the exact product overview, and verify a persistent state such as `正在审核` plus `Review of application: 正在进行`. Record the submission ID when exposed.
12. After publication, open the anonymous Store listing, install from the public route, launch, and exercise the core workflow before declaring `published`.

## Rejection remediation

Open the exact certification report and bind every issue to the rejected submission. Make the smallest permanent Store-only correction, increase the build number whenever bytes change, repeat all gates, and submit the corrected artifact. Never resubmit the rejected bytes under a renamed file.

Common KEMI findings:

- `10.1.1.1`: listing name and installed display name differ. Align executable metadata, installer identity, Add/Remove Programs name, and every localized listing.
- `10.2.7`: Add/Remove Programs name or publisher is blank or unrelated. Fix installer registry metadata and verify it after a real install.
- `10.1.5 Software Distribution`: the application links to or promotes acquiring apps outside Microsoft Store. Permanently remove that navigation/link in the Store flavor and verify the compiled result.

## Browser and collaboration discipline

Use background/read-only checks whenever possible. Do not occupy the foreground while another colleague owns the browser or Windows desktop. Use one task-owned Partner Center tab per product, avoid shared file-picker races, refresh the accessibility state after every action, and close only task-created pages after recording evidence. Bring the browser forward only for a currently visible login, MFA, CAPTCHA, legal gate, file selection, or submission step.

## Truthful states

Use only `not-started`, `blocked`, `uploaded`, `processing`, `submitted`, `in-review`, `rejected`, or `published`. A prepared build, successful signature, CDN upload, draft save, validation run, or reviewer email is not `in-review`. Publication requires an anonymous Store page and public installation verification.
