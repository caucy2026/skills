# Host validation and interrupted-release recovery

Read this reference when validating a macOS package, investigating contradictory signature results, or resuming a KEMI market upload after a browser/agent restart.

## 2026-09-05 failure pattern and root cause

During a KEMI Remote Office publication, a restricted execution environment reported the release ZIP and unrelated known-good applications as invalid. The same environment also reported that no keychain was available. Rechecking the identical ZIP in the real macOS host produced all expected results:

- `codesign --verify --deep --strict`: valid on disk and satisfies its designated requirement;
- `xcrun stapler validate`: valid ticket;
- `spctl -a -vv -t exec`: accepted, source `Notarized Developer ID`;
- Developer ID identity visible in the host keychain.

The package had not changed. The failure was inability of the restricted environment to reach the host keychain and trust services. Rebuilding or re-signing would have changed a valid artifact and wasted the notarization evidence.

The browser was then restarted while a create form and file chooser were in progress. The form returned to a new tab. This was a session-state loss, not an upload, package, or signing failure.

## macOS validation procedure

1. Freeze the final post-staple archive path.
2. Record exact bytes and SHA-256.
3. Run `scripts/verify_macos_release.sh` in the real host environment.
4. Preserve its output in the release report. The script verifies the extracted app, signature, staple, Gatekeeper result, executable architectures, and fixed bundle name.
5. Perform the project-required real install/launch test from the distribution archive. Confirm the installed bundle retains the stable product name expected by previous versions and configuration paths.
6. Recompute bytes and SHA-256 after any archive change. Any change creates a new artifact identity and invalidates earlier upload/hash evidence.

### Invalid test-environment signals

Stop interpreting signature output when any of these occurs:

- `security` says no keychain is available;
- `spctl` rejects multiple known-good signed applications in the same session;
- the Developer ID identity is absent only inside the restricted environment but visible on the host;
- trust-service communication errors occur.

Rerun the unchanged artifact outside the sandbox. Do not disable Gatekeeper, remove quarantine as a release fix, ad-hoc sign, or reconstruct the ZIP.

## Existing browser login versus CLI credentials

A failed CLI password login does not invalidate an authenticated browser session. Inspect the official console before asking the user to log in again. If tab control times out, inspect the same session through the available native browser UI instead of repeatedly creating blank tabs. When API credentials are unavailable, use the official existing-app form: select the frozen archive, require its displayed SHA-256 to match, fill the real version/code and exact byte size, submit, then verify through the public detail/CDN/update APIs. Recover a file-chooser clipboard timeout by inspecting the current dialog and setting its path field directly.

Do not attribute sandbox signature errors to archive damage, Finder merging, or provenance metadata without host evidence. Unchanged bytes and successful host verification invalidate those explanations.

## Publication state machine

Use server state rather than browser appearance as the source of truth:

```text
LOCAL_VALIDATED
  -> SERVER_LOOKUP
  -> PACKAGE_UPLOADED_AND_COMPLETED
  -> APP_CREATED_OR_UPDATED
  -> DEVELOPER_RECORD_VERIFIED
  -> PUBLIC_DETAIL_VERIFIED
  -> CDN_VERIFIED
  -> UPDATE_POSITIVE_AND_NEGATIVE_VERIFIED
  -> REAL_DOWNLOAD_INSTALL_VERIFIED
```

For every transition, record non-secret evidence. If interrupted, query the server and resume from the earliest transition without evidence.

### Recovery decisions

- Browser/tab/file-chooser lost: reopen/login, re-query `(package_name, os_type)`, and resume. Do not rebuild.
- Upload response ambiguous: query developer record and public detail. If the target hash is absent, request a fresh upload token and upload once.
- Target version and SHA-256 already online: skip upload and app mutation; perform verification only.
- Older online version: update the existing app ID; never create a replacement record.
- Same version but different hash: stop and audit; do not silently overwrite or bump a version merely to bypass the conflict.
- CDN mismatch: stop publication, preserve evidence, and do not announce completion.

## Minimal release evidence

Record these fields in the project release report:

- timestamp and Git commit;
- artifact absolute path, bytes, SHA-256;
- package name, OS, version name/code, architecture;
- macOS signer, codesign result, notarization submission/status, staple result, Gatekeeper result;
- developer app ID and create/update action;
- upload-complete URL/bytes/SHA-256;
- developer record, public detail, unfiltered list, CDN, update-positive and update-negative results;
- real downloaded-package install and launch result;
- remaining blockers, especially unsigned Windows artifacts or missing self-update support.

Never record passwords, bearer tokens, upload tokens, cookies, or authorization headers.
