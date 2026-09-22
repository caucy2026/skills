# Microsoft Store evidence record

Maintain one monotonic entry per product and attempt.

```markdown
## <product> Microsoft Store <version+build> — <checked-at CST>

- publisherAccount: caucy2002@163.com
- organization: KEMI / Shenzhen NewLink Software Co., Ltd.
- productId:
- packageRecordId:
- submissionId:
- certificationReportId:
- sourceCommit:
- channelFlavor: microsoft-store
- artifactFilename:
- artifactAbsolutePath:
- artifactBytes:
- artifactSHA256:
- innerPECount:
- innerSignatureResult:
- outerSignatureResult:
- timestampResult:
- cdnURL:
- anonymousDownloadBytes:
- anonymousDownloadSHA256:
- installTest:
- launchTest:
- coreWorkflowTest:
- uninstallTest:
- portalState:
- reviewState:
- publicStoreURL:
- evidencePaths:
- blocker:
- nextAction:
```

Keep CDN state, package validation state, and application review state separate. `uploaded` must name its scope. `in-review` requires the reopened product record. `rejected` requires the exact certification report. `published` requires an anonymous listing plus public installation and launch verification.

For a retry also record previous submission/hash, rule number, exact reviewer finding, permanent correction, new source/build/hash, regression evidence, and new submission ID. This prevents renaming and resubmitting rejected bytes.

Screenshots must visibly identify product and state. Redact unrelated accounts/tabs and never capture passwords, OTPs, cookies, certificate secrets, or identification documents.
