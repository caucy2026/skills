---
name: kemi-market-publish
description: Publish or update signed application packages in the KEMI application market and verify storefront metadata, CDN integrity, and in-app update behavior. Use when a user asks to 上架、发布、更新、补全信息 or verify an app on kemi.newlinksz.com; do not use for unrelated app stores.
---

# KEMI Market Publish

Complete the release as a production loop, not as an upload-only task.

## Non-negotiable execution environment

- Run macOS signature, notarization, Gatekeeper, architecture, and launch checks in the real macOS host environment. A restricted agent sandbox may be unable to access the login keychain, `trustd`, or `securityd` and can falsely report every signed app as invalid.
- If `security` reports that no keychain is available, or the same environment also rejects known-good Apple/Developer ID apps, classify the result as **invalid test environment**, not an invalid package. Rerun the unchanged artifact on the host; never rebuild, redownload, resign, or re-notarize because of that result.
- Treat `(absolute artifact path, exact byte count, SHA-256)` as the immutable artifact identity. Once host validation passes, reuse that evidence while the identity remains unchanged.
- For macOS ZIP releases, run `scripts/verify_macos_release.sh /absolute/path/package.zip` outside the restricted sandbox. Read [references/host-validation-and-session-recovery.md](references/host-validation-and-session-recovery.md) before diagnosing a signature failure or resuming an interrupted publication.
- For any signing, notarization, or signature audit, read [references/signing-certification-closure.md](references/signing-certification-closure.md) and complete its platform gate before upload.

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
   For KEMI传书 (`org.kemi.send`), use the public storefront category `探索` on every platform; never publish it as the restricted `开发工具` category (even when that category's slug is `工具`). Confirm `探索` exists and is enabled in the authenticated category API before mutating an app record.
2. Validate the artifact before upload. macOS requires Developer ID signing, an `Accepted` Apple notarization, staple validation, Gatekeeper acceptance, and a final archive created after stapling. Windows requires a valid intended Authenticode result and a self-contained clean-machine install when the project requires it.
3. Compute the exact byte count and SHA-256 locally. Human-readable values such as `385.7MB` are invalid release metadata: before final publish, require `file_size` to be the exact decimal byte string from the final post-staple archive and `file_size_bytes` to be the same integer. Re-query public detail after publish and stop if either field is missing, non-numeric, or differs from the local byte count.
4. Query by `(package_name, os_type)`. Update the existing app when present; create only when absent. Never create a duplicate to avoid an update problem.
5. Upload through the documented package-token/CDN/package-complete flow. Require the server URL, exact size, and SHA-256 to equal local evidence.
6. Create or update the app with all desktop compatibility fields. In particular, send both `file_size` as the exact decimal byte string and `file_size_bytes` as the integer.
7. Verify the developer record, public storefront detail, unfiltered public platform list, CDN headers, old-version positive update check, current-version negative update check, and the visible download/install path. The platform list check must omit `category`; a published KEMI传书 record must appear in this default “全部” result.
8. Confirm the client contains the platform-specific self-update path before claiming completion.
9. Write or update the project release report and changelog without secrets.
10. Delete temporary authentication and upload credentials.
11. After every requested platform has completed its post-release verification, close the publication workspace: dismiss any open file chooser or transient dialog, close only the publish/form/detail tabs created or claimed for this release, and release browser automation control. Do not close the user's pre-existing browser windows or unrelated tabs. If the workflow must pause for user input, mark only the necessary tab for handoff and close it after the release resumes and completes.

For macOS, validation of the pre-staple app does not validate the distributed ZIP. The release identity is always the final archive recreated after stapling. Extract and validate that exact archive before upload, then download the CDN object and validate it again before completion. Require exactly one top-level `.app`; signed helper applications nested inside that bundle are valid when `codesign --verify --deep --strict` validates the complete top-level bundle.

## Stable publication and recovery

For an already signed, notarized, stapled, and verified Vibekits macOS ZIP, read and follow the deterministic [Vibekits macOS one-minute publish path](references/vibekits-macos-one-minute-publish.md). It records the exact app identity, Chrome choice, file-picker behavior, field values, recovery decisions, post-release checks, and GitHub transport fallback. Do not rediscover these details or open another browser.

## Regression lessons from the 2026-09-21 Windows release

## Host-dependent component publishing

- QEMU and Mihomo runtime packages are VibeKits **components**, not standalone applications. Every market record must include `artifact_type: component`, `host_package_name: com.caucy.vibekits`, a stable `component_id` (`virtual_machine` or `network_proxy`), `standalone: false`, explicit `os_type`, and architecture.
- The storefront description must state: `VibeKits 功能组件，依赖 VibeKits 主程序，不能单独运行，不创建独立应用入口。` Never expose an `Open` action or claim the component is independently usable.
- A direct component download must check that the host package `com.caucy.vibekits` is installed. If it is absent, stop and direct the user to install VibeKits first. If present, install only into the host's managed component directory after HTTPS, exact byte count, SHA-256, platform signature, architecture, and manifest validation.
- Windows components belong under `%LOCALAPPDATA%\\Vibekits\\components\\<component_id>\\<version>\\`; macOS components belong under `~/Library/Application Support/Vibekits/components/<component_id>/<version>/`. Never write downloaded components into a signed macOS `.app` bundle.
- QEMU and Mihomo are independent optional components. Do not make one depend on the other, and do not include them in the core package's mandatory startup gate. The host must show `missing/installing/installed/outdated/invalid/failed` states and enable the feature only after the component manifest and signature validate.

- Never assemble a Windows release by copying only `data\\app.so` or another newly built payload into an older signed directory. The Flutter AOT payload, `flutter_windows.dll`, `vibekits.exe`, and all bundled runtime files must come from the same full Release build. A valid Authenticode signature does not prove runtime compatibility: the mixed bundle passed signature checks but crashed immediately in `flutter_windows.dll` with `0xc0000005`.
- Before signing and publishing, compare the hashes and sizes of `vibekits.exe`, `flutter_windows.dll`, and `data\\app.so` between the staging directory and the single full Release output. Then launch the exact staging tree on the Windows test machine and check that the process remains alive and no new crash dump appears.
- For KEMI desktop metadata, `file_size` is a decimal byte string, never `250.2MB` or another human-readable value. Also send `file_size_bytes` as the same integer. The public catalog may otherwise expose a non-numeric size; the client parses that as zero and reports the misleading error that HTTPS/size/SHA-256 verification is missing even when `download_url` is HTTPS and the hash is correct.
- Treat URL and enum casing as contract data: use `https://kemi.newlinksz.com/kd-api`, the CDN hostname `cdn.newlink-sz.com`, `os=windows` for the check request, and compare the returned `os_type` after lowercasing. Verify the public `/api/store/apps?os=windows` record, not only the authenticated form, before calling the release complete.
- A market update can retain the same version only for a metadata-only repair when the server confirms the online record changed. For a new binary, require a strictly higher `version_code`; for a metadata repair, re-query the public record and confirm exact bytes, URL, and SHA-256.

- Prefer the documented authenticated API flow over browser form automation. Use browser UI only when the live documentation requires it or the API is unavailable.
- Fast-path for the established Vibekits macOS release: use the linked one-minute publish reference. Its fixed identity is app `53`, package `com.caucy.vibekits`, OS `macos`. Do not improvise browser, profile, app record, chooser target, metadata format, or transport recovery.
- Before any upload or after any interruption, query `(package_name, os_type)` and compare the online version, bytes, SHA-256, and URL with the immutable local evidence.
  - Exact target version and hash already online: do not upload again; continue post-release verification.
  - Existing app with an older version: update that app ID.
  - No app: create only after a second lookup confirms absence.
  - Conflicting or duplicate records: stop before mutation.
- A browser restart, lost tab, expired form, or failed file chooser invalidates only the UI session. It does not invalidate the artifact. Restore the session, re-query server state, and resume from the first unverified server step.
- Never keep a partially completed form as the only release state. Record non-secret evidence in the project release report: package/OS, version/code, bytes, SHA-256, host validation result, upload completion, app ID, CDN URL, and verification results.
- Use one upload attempt at a time. After an ambiguous response, query server state before retrying. Do not create a second app or rebuild the same artifact as a recovery mechanism.

## Decision rules

- A successful build is not a release.
- A successful CDN upload is not a release.
- A successful create/update response is not a release.
- Do not report completion while the storefront download button is disabled, public metadata is incomplete, the CDN length differs, the current version loops updates, or a required signature/notarization check is missing.
- For `.zip`, infer no OS from the suffix alone. Resolve the platform from the build and package contents.
- For non-Android clients, always pass the explicit `os` value to the public update check.
- Preserve the existing app identity and package name during updates. A new version code must be greater than the online value. A metadata-only repair may retain the version only if the API explicitly confirms the online record was updated.
- Treat category as a storefront visibility field, not decorative metadata. For KEMI传书, use the enabled public `探索` category. Do not substitute the restricted `开发工具` category or its `工具` slug, because that can exclude the app from the public default list.
- Do not invent ratings, download counts, developer level, or capabilities. These are system-managed or must reflect tested product behavior.
- If credentials lack release permission, stop and report the permission issue; do not seek a bypass.
- Do not confuse a test-environment failure with an artifact failure. A signature conclusion is valid only when the checking environment can access normal macOS trust services.
- Do not repeat completed gates when the artifact identity is unchanged. Recheck only the failed or unverified release stage.
- Publication cleanup is part of completion. Do not leave an upload form, file picker, temporary release tab, or browser-control session open after verification has finished. Cleanup must never discard an unsubmitted form or interrupt an upload; perform it only after the authoritative server state has been re-read and the release is either verified complete or recorded as blocked.

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
