# Newlink Common release contract

## Destination

- Admin site: `https://www.newlinksz.cn/screensaver/main/configPlug/Common`
- Public metadata: `https://www.newlinksz.cn/screensaver/api/plugData?projectName=Common&name=<resource>`
- Project: `Common`

This cloud is the fixed-resource update channel used by the PAD client. It is not the KEMI application market at `kemi.newlinksz.com`.

## Fixed resources

| Resource | Local filename | Record ID |
|---|---|---|
| KEMI-PAD | KEMI-PAD.apk | 6a6d81c09cb89f166dac208c |
| KEMI-macOS | KEMI-macOS.zip | 6a6d81709cb89f166dac208a |
| KEMI-Windows | KEMI-Windows.exe | 6a6d81f89cb89f166dac208e |
| KEMI-Linux | KEMI-Linux.AppImage | 6a6d7358c557f530ffec567f |
| SHA256SUMS | SHA256SUMS.txt | 6a6d74e5c557f530ffec5685 |
| release-manifest | release-manifest.json | 6a6d82359cb89f166dac2093 |

The script validates each ID against the returned resource name and `projectCode=Common` before uploading.

## Ordering

Full release:

1. Four client binaries.
2. `SHA256SUMS`.
3. `release-manifest` last.

Single-platform hotfix:

1. Changed platform binary.
2. `SHA256SUMS` containing the complete four-client checksum set.
3. `release-manifest` last.

Never publish the manifest before its referenced files. The manifest is the client-visible switch to the new batch.

## Completion gate

For every selected resource, require all of the following:

- backend update response succeeds;
- public `plugData` version equals the requested version;
- public MD5 equals the local file MD5;
- public URL is HTTPS and points to `cdn.newlink-sz.com/Common/`.

Large CDN re-download is optional for routine repeat releases and enabled with `--verify-download`. Formal macOS release validation—Developer ID signature, notarization, stapling, Gatekeeper and local launch—must be completed before this upload skill is invoked.

## Failure handling

- Authentication or token failure: publish nothing; request a valid credential path.
- Resource ID/name mismatch: stop before upload.
- Binary succeeds but checksum fails: do not publish manifest.
- Checksum succeeds but manifest fails: clients remain on the previous complete batch; fix and republish only the manifest after verifying referenced files.
- Public version/MD5 mismatch: do not report completion, even if the admin page displayed success.
