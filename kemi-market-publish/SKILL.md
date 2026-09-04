---
name: kemi-market-publish
description: Publish or update signed application packages in the KEMI application market and verify storefront metadata, CDN integrity, and in-app update behavior. Use when a user asks to 上架、发布、更新、补全信息 or verify an app on kemi.newlinksz.com; do not use for unrelated app stores.
---

# KEMI Market Publish

Complete the release as a production loop, not as an upload-only task.

## Authority and current documentation

- Treat uploads, app creation, and app updates as external production mutations. Obtain explicit authorization in the current task before the first mutation. Read-only lookups and local validation may proceed without it.
- Never store account passwords, bearer tokens, OAuth codes, or upload tokens in source control, reports, chat output, or durable scripts. Use mode-600 temporary files and remove them at the end.
- Before publishing, read the current official documentation at:
  - `https://kemi.newlinksz.com/kd/docs/ai-publish`
  - `https://kemi.newlinksz.com/kd/docs/app-upload`
  - `https://kemi.newlinksz.com/kd/docs/store-api`
  - the target OS page under `https://kemi.newlinksz.com/kd/docs/app-self-update/`
- If the live documentation conflicts with this skill, stop before mutation and follow the live contract. Update this skill only when the user asks or the task includes maintaining it.
- Read [references/release-contract.md](references/release-contract.md) before constructing upload or app payloads.

## Required outcome

For every requested platform:

1. Identify the final artifact, package name, OS, semantic version, integer version code, architecture, icon, category, descriptions, and release notes from project evidence.
2. Validate the artifact before upload. macOS requires Developer ID signing, an `Accepted` Apple notarization, staple validation, Gatekeeper acceptance, and a final archive created after stapling. Windows requires a valid intended Authenticode result and a self-contained clean-machine install when the project requires it.
3. Compute the exact byte count and SHA-256 locally.
4. Query by `(package_name, os_type)`. Update the existing app when present; create only when absent. Never create a duplicate to avoid an update problem.
5. Upload through the documented package-token/CDN/package-complete flow. Require the server URL, exact size, and SHA-256 to equal local evidence.
6. Create or update the app with all desktop compatibility fields. In particular, send both `file_size` as the exact decimal byte string and `file_size_bytes` as the integer.
7. Verify the developer record, public storefront detail, CDN headers, old-version positive update check, current-version negative update check, and the visible download/install path.
8. Confirm the client contains the platform-specific self-update path before claiming completion.
9. Write or update the project release report and changelog without secrets.
10. Delete temporary authentication and upload credentials.

## Decision rules

- A successful build is not a release.
- A successful CDN upload is not a release.
- A successful create/update response is not a release.
- Do not report completion while the storefront download button is disabled, public metadata is incomplete, the CDN length differs, the current version loops updates, or a required signature/notarization check is missing.
- For `.zip`, infer no OS from the suffix alone. Resolve the platform from the build and package contents.
- For non-Android clients, always pass the explicit `os` value to the public update check.
- Preserve the existing app identity and package name during updates. A new version code must be greater than the online value. A metadata-only repair may retain the version only if the API explicitly confirms the online record was updated.
- Do not invent ratings, download counts, developer level, or capabilities. These are system-managed or must reflect tested product behavior.
- If credentials lack release permission, stop and report the permission issue; do not seek a bypass.

## Completion report

Report each platform separately with:

- app ID and whether it was created or updated;
- package name, OS, version name, and version code;
- artifact path, bytes, and SHA-256;
- signature/notarization evidence where applicable;
- developer-record, storefront-detail, CDN, positive-update, negative-update, and real install results;
- self-update implementation status;
- source/report paths and commit ID when committed;
- any remaining limitation stated plainly.

Say “正式发布完成” only when all mandatory checks pass. Otherwise state the precise blocker and keep completed facts separate from pending work.
