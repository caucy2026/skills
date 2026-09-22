# End-to-end Microsoft Store procedure

## 1. Establish the release row

Read the latest monotonic ledger entries. Capture the last submitted version/build, certification report, product ID, package record ID, source commit, artifact hash, and blocker. Verify that another task is not using the worktree, publisher portal, native file picker, or Windows signing desktop.

Choose a higher build number for every byte-changing correction. Give the artifact a Store-specific filename such as `Product-Version+Build-Microsoft-Store.exe`.

## 2. Isolate and build the Store flavor

Create or reuse a dedicated worktree from the frozen commit. Use independent caches and build outputs. On the KEMI Windows node, source and build work stays on `D:`.

Implement policy through a permanent compile-time flavor. Verify both builds:

- Store: prohibited external-app acquisition navigation is absent; installed name, publisher, and version match the listing.
- Direct: ordinary functionality remains intact and has not been overwritten.

Inspect the output for the Store marker so stale incremental output cannot ship. Use a clean build when distribution flags change.

## 3. Pre-signing inspection

Enumerate every staged PE and record the expected count and paths. Inspect x64 architecture, supported Windows versions, `ProductName`, `FileDescription`, `CompanyName`, `FileVersion`, `ProductVersion`, installer display name, publisher, AppId, uninstall entry, silent switches, support/privacy/About access, and absence of prohibited navigation.

An unsigned installer preflight may prove the recipe and metadata. Its hash is disposable and must never be reported as the signed release artifact.

## 4. Hardware-token signing

Read the current Windows signing skills and their VibeKits Authenticode reference. Signing must run in the logged-in interactive Windows session that can show the token PIN. SSH Session 0 may stage, hash, package already signed inner files, and verify signatures; it cannot substitute for the interactive token session.

1. Sign all inner PE files with the intended certificate and RFC 3161 timestamp.
2. Persist an inner report with file count, valid count, certificate identity, timestamp, SignTool exit codes, and session ID.
3. Package the signed payload without modifying inner PE files.
4. Sign the final outer installer interactively.
5. Persist an outer report and terminal `signed-valid` state.
6. Independently verify every inner signature and the outer signature.
7. Copy the final artifact to the formal candidate location and compare SHA-256.

A PIN prompt, wrapper launch, `inner-signed` state, command window, or outer-file existence does not prove completion. Require outer `Valid`, intended certificate, timestamp, byte count, and final hash.

## 5. Windows acceptance gate

Protect unrelated running KEMI sessions. Install using the documented silent command. Verify no prompts, Add/Remove Programs name/publisher/version/uninstall data, install location, installed launch, Store-specific UI policy, core workflow, and silent uninstall. Test upgrade where applicable. Restore temporarily stopped processes.

If the shared Windows desktop is busy, do not disrupt it. Continue independent work, but do not waive this gate.

## 6. Immutable CDN object

Partner Center Win32 packages consume a version-controlled HTTPS EXE/MSI URL. Create a new immutable Store-only object whose filename includes product, version/build, architecture, and `microsoft-store`. Never replace a Common client resource, KEMI internal-market package, or direct-build URL.

After upload, anonymously download the complete file and verify exact byte count and SHA-256. Record this as CDN `uploaded-and-anonymously-verified`, not Store submission.

## 7. Partner Center package editor

Use `caucy2002@163.com`; reject cached `caucy2026@outlook.com`. Verify KEMI organization and the exact product. Open `/packages/<record-id>/edit`; reused links can incorrectly land on Usage analytics.

Verify installer type, x64 architecture, immutable URL, version, silent install/uninstall commands, expected return codes, and acceptance-test equivalence. Save the package draft and the whole submission. Run validation and resolve errors. Read warnings; override only understood, truthful warnings within the authorized submission.

## 8. Listing and submission

Complete availability, age ratings, properties, support/privacy URLs, and every requested language. Screenshots must match their declared language. Listing identity must match the installed Store build.

Immediately before submission, recheck product ID, package record, version/build, CDN URL, artifact hash, and completed sections. Submit the exact correction.

## 9. Independent proof

Leave the submission surface and reopen the exact product overview. `in-review` evidence should bind the product to persistent text such as `正在审核`, `应用设置: 正在审核`, `你的应用提交已完成`, and `Review of application: 正在进行`. Record submission ID when exposed, timestamp/timezone, IDs, hash, and screenshot.

If it returns to draft or shows `Review of application: 失败`, open the exact certification report immediately.

## 10. Publication closure

After `In the Store` or Store ID appears, open the public listing signed out, confirm name/version/publisher, install through the public route, launch, and exercise the core workflow. Only then record `published`.

