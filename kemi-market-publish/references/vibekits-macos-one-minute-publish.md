# Vibekits macOS one-minute publish path

Use this reference only for publishing a prepared Vibekits macOS release to the existing KEMI market record. “One minute” means the operator path is deterministic and begins when the final post-staple ZIP already exists. Apple notarization, a 400+ MB transfer, CDN hashing, and full download verification take their real service and network time; never fake, skip, or report those gates early.

## Frozen identity

- Developer record: app ID `53`.
- Package: `com.caucy.vibekits`.
- OS: `macos`.
- Edit URL: `https://kemi.newlinksz.com/kd/console/apps/edit/53`.
- Public detail: `https://kemi.newlinksz.com/kd-api/api/store/apps/53?os=macos`.
- Artifact convention: `/private/tmp/Vibekits-<version>+<code>-macos-universal-notarized-clean.zip`.
- Keep category `工作`, storefront visibility enabled, and update cancellable unless the user explicitly changes them.
- Update app 53. Never create another Vibekits record.

## Start with the artifact, not the browser

1. Check whether the target version and SHA-256 are already online. If yes, skip upload and continue verification.
2. Require the ZIP to be created after stapling. Run `scripts/verify_macos_release.sh` on the real macOS host.
3. Freeze its absolute path, exact decimal byte count, and SHA-256. The form's package size must be the decimal byte count, never `401.0MB` or another display value.
4. Do not upload an archive produced before `xcrun stapler staple`.

If the signing script says another Vibekits instance is running, read the bridge PID from `~/Library/Application Support/com.caucy.vibekits/Vibekits/Mcp/tool-bridge.json`, confirm its executable path with `lsof`, and close only that release/test instance. A directly launched app can remain registered as a dynamic `launchd` job and restart after SIGTERM. Resolve its exact label with `launchctl list` and boot out `gui/<uid>/<label>` before retrying. Do not repeatedly re-sign while the same registered instance is the only blocker.

For a real launch of an extracted CDN app, close the prior exact-bundle instance and use `open -n /absolute/path/Vibekits.app`. Directly executing `Contents/MacOS/Vibekits` can activate an older LaunchServices registration with the same bundle ID, making the new package appear to exit. Verify the bridge PID belongs to the extracted app path.

## Browser selection is fixed

Use the installed system **Google Chrome**, not the Codex in-app browser, Safari, or another Chrome profile.

- Expected authenticated Chrome user/profile evidence: Chrome profile shown as `niu`/`niu minglei`, and the KEMI page header shows `用户220738`.
- Prefer the purpose-built authenticated API when credentials are available. Otherwise use the existing Chrome session.
- When browser-extension tab control fails with a request-header-policy or timeout error, do not retry indefinitely and do not switch to the Codex browser. Bind the native `Google Chrome` app, focus its address bar, and navigate the existing release tab to the fixed edit URL.
- Keep browser work in the background. Do not open the Codex in-app browser for publication.
- Reusing a blank/login-helper Chrome tab is allowed. Close only the publication tab after verification; keep unrelated user tabs and windows.

## Exact Chrome form sequence

1. Open the fixed edit URL and verify all three identity signals before upload: `Vibekits`, `com.caucy.vibekits`, and current online version.
2. Activate the installation-package chooser.
3. The macOS chooser normally opens at `/private/tmp`. Select the row whose full filename exactly equals the frozen artifact name. Do not select `VibekitsHarness-*` or any folder.
4. Confirm the selected row URL points to the exact ZIP, its kind is ZIP archive, and the `打开` button is enabled. Then click `打开` once.
5. Wait through both phases: CDN upload and local/server SHA-256 calculation. At 99% the page can remain on `正在计算 SHA-256` for several minutes. Preserve the tab; do not refresh, choose the file again, or start a second upload.
6. Continue only after the form replaces the old SHA-256 with the exact local SHA-256.
7. Set version name, integer VersionCode, exact decimal byte size, and release notes. Preserve other metadata.
8. macOS accessibility may expose VersionCode as a stepper. If direct value assignment does not change it, focus the stepper, press `super+a`, type the complete code, press Tab, and reread the displayed value. Never use the increment button after a failed assignment; it can reset the value to `1`.
9. Reread version, VersionCode, byte size, SHA-256, storefront visibility, and force-update choice immediately before `保存并发布`.
10. Click `保存并发布` once. Success requires navigation to app detail, status `已上架`, the new version/code, and the message `已直接更新线上版本（免审）`.

An old `查看安装包` URL can remain visible while a new upload is in progress. The authoritative upload completion signal is the new SHA-256 shown by the form, followed by the public API after publication.

## Mandatory post-release checks

Query and compare against the frozen evidence:

- public detail for app 53;
- unfiltered macOS list with no category parameter;
- update check from the immediately older VersionCode: `has_update=true`;
- update check from the released VersionCode: `has_update=false`;
- HTTPS CDN URL, HTTP 200, exact `Content-Length`, full downloaded SHA-256;
- `scripts/verify_macos_release.sh` on the downloaded ZIP;
- extract the downloaded ZIP, launch its `Vibekits.app` with `open -n`, and verify its Harness bridge PID belongs to that extracted path.

The public detail endpoint may expose only decimal `file_size`; the update endpoint must expose both `file_size` and integer `file_size_bytes`. Treat the combined public contracts as passing only when both equal the frozen byte count.

## Source record and GitHub transport recovery

Update the release report with version/code, artifact identity, signer, notarization submission ID and `Accepted` status, staple/Gatekeeper result, app ID, CDN URL, API results, and real downloaded-package launch. Do not include credentials.

If `git push` over SSH is closed at port 22 and the bundled GitHub CLI reports an authenticated account with `repo` scope:

1. Preserve the configured remote and the user's global rewrite rules.
2. Copy `~/.gitconfig` to a mode-safe temporary file.
3. Remove only `url.git@github.com:.insteadof` from that temporary config.
4. Run the one push/fetch with `GIT_CONFIG_GLOBAL=<temporary-config>` and the HTTPS repository URL.
5. Delete the temporary config and verify local `HEAD` equals `refs/remotes/origin/main`.

Do not print tokens or embed them in a URL.
