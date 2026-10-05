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

## VibeKits macOS prepublication device gate

Before publishing a new VibeKits macOS binary, use the **same final signed and stapled candidate** on every reachable device in the release's named regression fleet. For the 2026-09-25 fleet, check `1321656264` (Intel macOS 12), `4456560334`, `5298938227`, and `9509249133`; also test the local publisher Mac. Connect through VibeKits remote simulation, record each device's OS/architecture, candidate version and actual process path, fresh P2P/relay connection, Harness launch, interactive UI/ready state, and relevant logs. On macOS 12, verify ordinary launch without an injected compatibility environment variable and confirm the legacy WebKit frontend is selected. Preserve the previous app as a rollback until acceptance. An unreachable device must be recorded as untested with the exact transport evidence; do not count an ID, green presence indicator, package install, or process start as a functional pass. Fix any reachable-device failure and repeat the affected gate before storefront mutation. If a named device is unreachable, explicitly state the coverage gap and obtain the user's release decision only if the requested scope requires that device's pass.

The prepublication test must precede package upload and storefront version mutation. A new binary changes the artifact identity and requires the device gate again. After publication, verify the downloaded CDN artifact and the installed version separately; record per-device pass/fail/untested outcomes in the project release report.

## Required outcome

For every requested platform:

1. Identify the final artifact, package name, OS, semantic version, integer version code, architecture, icon, category, descriptions, and release notes from project evidence.
   For KEMI传书 (`org.kemi.send`), use the public storefront category `探索` on every platform; never publish it as the restricted `开发工具` category (even when that category's slug is `工具`). Confirm `探索` exists and is enabled in the authenticated category API before mutating an app record.
2. Validate the artifact before upload. macOS requires Developer ID signing, an `Accepted` Apple notarization, staple validation, Gatekeeper acceptance, and a final archive created after stapling. Windows requires a valid intended Authenticode result and a self-contained clean-machine install when the project requires it.
   For Android PAD packages that embed separately installed system components, unpack the **final signed APK** and compare every embedded component version with the host's actual minimum runtime requirement; verify host and component package IDs and signing certificate. Test both an existing-device overlay upgrade and first authorization on a device without a previously upgraded component. A host signed with a bundled component below its required version blocks publication even when it works on an older test device. VibeKits PAD: run `python3 tool/check_pad_embedded_helper.py <final-apk> --source <frozen-source>`; the dev458/v5 versus required v9 incident is recorded in `docs/acceptance/PAD_DEV458_EMBEDDED_HELPER_INCIDENT_2026-10-03.md`.
3. Compute the exact byte count and SHA-256 locally. Human-readable values such as `385.7MB` are invalid release metadata: before final publish, require `file_size` to be the exact decimal byte string from the final post-staple archive and `file_size_bytes` to be the same integer. Re-query public detail after publish and stop if either field is missing, non-numeric, or differs from the local byte count.
4. Query by `(package_name, os_type)`. Update the existing app when present; create only when absent. Never create a duplicate to avoid an update problem.
5. Upload through the documented package-token/CDN/package-complete flow. Require the server URL, exact size, and SHA-256 to equal local evidence.
6. Create or update the app with all desktop compatibility fields. In particular, send both `file_size` as the exact decimal byte string and `file_size_bytes` as the integer.
7. Verify the developer record, public storefront detail, unfiltered public platform list, CDN headers, old-version positive update check, current-version negative update check, and the visible download/install path. The platform list check must omit `category`; a published KEMI传书 record must appear in this default “全部” result.
8. Confirm the client contains the platform-specific self-update path before claiming completion.
9. Write or update the project release report and changelog without secrets.
10. Delete temporary authentication and upload credentials. After publication and real installation are verified, remove only the exact disposable upload/download ZIPs and extraction directories created for this release on the publisher and updated clients. Check path, ownership, expected artifact identity and active use first; retain signed final deliverables, rollback copies, logs and release evidence. Record what was removed and what was intentionally retained. Do not delete user downloads or general app caches by directory name alone.
11. After every requested platform has completed its post-release verification, clean and close the publication workspace before reporting completion: dismiss file choosers and transient dialogs, close the publish/form/detail/document tabs created or claimed for this release, and release browser automation control. If this release created a dedicated browser window and all its tabs belong to this release, close that window too; when reusing an existing window, close only this release's tabs. Never quit or kill the shared browser process, close the user's pre-existing windows, or disturb another colleague's tabs. Re-read the browser/app inventory and verify that the owned tabs/window and dialogs are gone; a close command alone is not proof of cleanup. Record the closure result alongside the release verification. If user input is genuinely required, retain only the necessary handoff tab and finish this cleanup immediately after the release resumes. Do not discard an unsubmitted form or interrupt an active upload.

For macOS, validation of the pre-staple app does not validate the distributed ZIP. The release identity is always the final archive recreated after stapling. Extract and validate that exact archive before upload, then download the CDN object and validate it again before completion. Require exactly one top-level `.app`; signed helper applications nested inside that bundle are valid when `codesign --verify --deep --strict` validates the complete top-level bundle.

## Stable publication and recovery

For an already signed, notarized, stapled, and verified Vibekits macOS ZIP, read and follow the deterministic [Vibekits macOS one-minute publish path](references/vibekits-macos-one-minute-publish.md). It records the exact app identity, Chrome choice, file-picker behavior, field values, recovery decisions, post-release checks, and GitHub transport fallback. Do not rediscover these details or open another browser.

For a signed VibeKits Windows installer update, read and follow the deterministic [VibeKits Windows one-minute operator path](references/vibekits-windows-one-minute-publish.md). It fixes the Chrome profile, existing app identity, upload chooser sequence, exact metadata, public verification, and cleanup steps. Do not use the Codex in-app browser for this flow.
For Windows, also follow that reference’s “缺少完整信息” recovery: compare exact decimal bytes in both public detail and unfiltered list after saving. A correct update-check size alone does not prove the in-app storefront can install. If only the size is wrong, repair app 54 metadata in place and verify again without reuploading the unchanged signed package.

## Regression lessons from the 2026-09-21 Windows release

## Host-dependent component publishing

### VibeKits Android PAD components

- Publish all VibeKits/VibePads Android PAD host-dependent components under the enabled public **`组件`** category, never the default `探索`. Resolve its current `name`, `slug`, `category_id`, and visibility from authenticated `/api/apps/categories` before mutation; verified on 2026-10-05: name `组件`, slug `component`, ID `9`, enabled and public. Do not hard-code the ID as a permanent contract.
- Determine PAD ownership from Android OS, component manifest and dependency on host **`com.vibekits.vibekits`**, not package prefix alone. The legacy Android proxy package `com.caucy.vibekits.component.network_proxy` is a PAD component; it must not be confused with desktop components whose host is `com.caucy.vibekits`. The PAD host application itself is not a component and its category is not changed by this rule.
- Keep the component contract in the package manifest and supported catalog fields: `artifact_type: component`, `host_package_name: com.vibekits.vibekits`, stable `component_id`, `standalone: false`, Android platform/device compatibility and actual architecture. The description states the host dependency, purpose, and inability to run independently. If the live API does not persist these fields, do not claim that it does; retain the manifest contract and truthful description.
- Inventory authenticated Android records including hidden/self-update records and drafts, then update existing PAD component records in place. For a category-only repair, preserve package/OS, version/code, HTTPS URL, exact byte count, SHA-256, icon, descriptions, platforms, visibility and force-update setting; do not reupload or create duplicates. Re-read the authenticated record and verify that only category and the server timestamp changed. Check public detail, the `category=组件` list and default Android list without a category filter for records intended for public display.

### Desktop components

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
- After the package-upload completion response is received and the server URL, byte count, and SHA-256 have been recorded, immediately dismiss any file chooser/transient dialog, close the temporary upload form or release tab when it is no longer needed, and release browser control so the user's foreground is available again. Preserve the recorded upload evidence and resume later from server state for app-record mutation and post-release verification; never leave the upload page in front while waiting on later checks.

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
