# VibeKits Windows one-minute operator path

Use this path for an already built, Authenticode-signed, timestamped, and Windows-verified VibeKits installer. “One minute” means operator interaction time; CDN transfer and server SHA-256 calculation depend on package size and network speed.

## Fixed identity and browser

- Existing KEMI market app: `app_id=54`.
- Package: `com.caucy.vibekits`; OS: `windows`; category: `工作`.
- Use installed system **Google Chrome**, profile `niu` / `niu minglei`, with page header `用户220738`.
- Do not use the Codex in-app browser, Safari, another Chrome profile, or create another app record.
- Fixed edit URL: `https://kemi.newlinksz.com/kd/console/apps/edit/54`.
- The form can briefly render Android defaults while loading. Wait until it shows the existing Windows record, `.exe / .msi / .zip`, package `com.caucy.vibekits`, and the current online version before touching the form.

## Pre-upload gate

Freeze and record the final installer absolute path, decimal byte count, and lowercase SHA-256. Require Windows Authenticode `Valid`, the intended embedded signer, trusted timestamp, and independent SignTool verification. The exact installer must already have passed the currently authorized Windows installation/launch gate. Never upload a partial controller download or a pre-outer-sign hash.

## Exact Chrome upload sequence

1. Open the fixed edit URL in the authenticated Chrome profile.
2. Locate the first `input[type=file]` whose `accept` is `.exe,.msi,.zip` or use the visible “拖入新安装包替换，或点击选择” button.
3. Start waiting for the Chrome `filechooser` event **before** clicking the upload control. Set the chooser to the frozen absolute installer path. Do not operate a native picker by row position when the chooser API works.
4. Keep the tab open through `直传 CDN 99%` and `正在计算 SHA-256`. The old URL/hash remain visible until completion; this is normal and is not an upload failure.
5. Completion is proved only when the upload button is enabled again and the page shows a new HTTPS CDN URL plus the exact local SHA-256.
6. If the chooser cannot set the file, enable “Allow access to file URLs” for the ChatGPT Chrome extension, then retry the same Chrome flow. A lost tab or chooser invalidates only the UI session; reopen the fixed URL and re-query server state before another upload.

## Exact form values

Preserve the existing name, package, category, icon, language, permissions, `在商城展示`, and `可取消` settings. Set:

- `版本号`: the verified release version, for example `1.9.0-dev.226`.
- `VersionCode`: the verified integer build code, for example `2226`. Element Plus number inputs may ignore `fill`; focus it, select all, type the number, press Tab, then read both `value` and `aria-valuenow`.
- `包大小`: the exact decimal byte string, never MB text.
- `更新说明`: only tested changes in the release.

Click `保存并发布` only after the displayed CDN SHA-256 equals the frozen local hash. Require navigation to the app detail page, `已上架`, the target version/code, and the success alert `已直接更新线上版本（免审）`.

## Mandatory post-release checks

1. Public detail: `/kd-api/api/store/apps/54?os=windows` has the target version/code, HTTPS URL, exact decimal `file_size`, and SHA-256.
2. Default list without category: `/kd-api/api/store/apps?page=1&pageSize=100&os=windows` contains app 54.
3. CDN `HEAD`: HTTP 200 and `Content-Length` equals local bytes.
4. Download the whole CDN object to the external build-cache artifact directory; require byte count and SHA-256 equality.
5. Update check with the previous code returns `has_update=true` and exact URL/size/hash; the released code returns `has_update=false`.
6. Complete any release-specific real update/install/launch verification that remains in scope. Keep that status separate from upload and storefront metadata success.

## Known failure: “缺少完整信息，已禁止安装”

The Windows client parses the public catalog `file_size_bytes ?? file_size` as an integer. If the public `file_size` is human-readable (for example `270.1MB`), it becomes zero and disables installation even when the HTTPS URL and SHA-256 are correct. The upload/edit form may show or save the formatted MB value; entering exact bytes once is not proof that the published field stayed numeric.

Before declaring success, compare the exact byte count against **both** `/kd-api/api/store/apps/54?os=windows` (`data.app.file_size`) and the app-54 entry in `/kd-api/api/store/apps?page=1&pageSize=100&os=windows` (`data.list[].file_size`). Require a decimal integer string equal to the signed installer’s bytes in both responses. Do not substitute the update-check response: it can report `file_size_bytes` correctly while the storefront remains blocked.

If the version, HTTPS URL, and SHA-256 are already correct but either public size is `MB`, blank, zero, or mismatched, perform a **metadata-only repair** on the existing app 54 in the authenticated Chrome profile: reopen the edit form, replace `包大小` with the verified exact decimal bytes, keep the same version and package URL, click `保存并发布`, and re-query both public endpoints. Do not reupload, rebuild, or resign the unchanged installer. The repair passes only when both public sizes match and the client download button is enabled.

## Immediate cleanup

After authoritative server and CDN checks are recorded, close the publication tab created or claimed for this release and release Chrome automation control. Dismiss any chooser or transient dialog. Leave unrelated user tabs/windows untouched and do not leave the market page in the foreground. Record app ID, version/code, URL, bytes, SHA-256, validation results, and any remaining device acceptance work in the release report.
