# KEMI market release contract and verification reference

Read this reference when preparing or auditing a KEMI market release. Recheck the live official docs before using these examples because production fields can change.

## Endpoints

```text
UC=https://kemi.newlinksz.com/usercenter
KD=https://kemi.newlinksz.com/kd-api
```

| Purpose | Method and path |
|---|---|
| Login | `POST {UC}/api/auth/login` |
| Categories | `GET {KD}/api/apps/categories` |
| Duplicate lookup | `GET {KD}/api/apps/list?os_type={os}&keyword={package}&page=1&pageSize=20` |
| Desktop upload token | `POST {KD}/api/upload/package-token` |
| Desktop upload completion | `POST {KD}/api/upload/package-complete` |
| Create app | `POST {KD}/api/apps/create` |
| Update app | `POST {KD}/api/apps/update` |
| Public detail | `GET {KD}/api/store/apps/{app_id}?os={os}` |
| Public update check | `GET {KD}/api/store/update/check?package_name={package}&version_code={code}&os={os}` |

Authenticated KD calls use `Authorization: Bearer {token}`. Obtain the token with the official administrator flow. Never print it.

## OS and upload category

| Package | `os_type` | upload category |
|---|---|---|
| `.exe`, `.msi` | `windows` | `winpkg` |
| `.dmg`, `.pkg`, verified Mac `.zip` | `macos` | `macpkg` |
| `.apk` | `android` | use `apk-token` and `apk-complete` |
| `.AppImage`, `.deb`, `.rpm` | `linux` | `linuxpkg` |
| `.ipa` | `ios` | `iospkg` |

## Login body

```json
{
  "account": "administrator account",
  "password": "secret supplied at runtime",
  "device_id": "kemi-release-cli",
  "device_name": "KEMI Release CLI"
}
```

Use a protected temporary directory. Interactive password input should not echo. Delete login request/response, bearer token, OAuth code, upload token, and payload files after the run.

## Duplicate lookup

The identity key is `(package_name, os_type)`:

- exactly one match: update its `app_id`;
- no match: create;
- more than one match: stop and audit duplicates;
- never change the package name or OS to work around an update rejection.

Before an ordinary version update, require `new_version_code > online_version_code`.

## Desktop package upload

Request a token:

```json
{
  "category": "winpkg or macpkg",
  "filename": "final artifact filename",
  "size": 285183449
}
```

POST the returned `token`, `key`, and package file as multipart form data to `data.upload_url`. For large packages use bounded retries, but do not start multiple competing uploads of the same package.

Complete the upload:

```json
{
  "key": "returned key",
  "filename": "final artifact filename",
  "size": 285183449
}
```

Require all of the following before continuing:

```text
status == 200
data.url starts with https://
data.size == local exact bytes
data.sha256 == local SHA-256
```

Desktop upload completion may not parse package identity or versions. Do not copy empty package/version fields from that response.

## Create/update payload

Create omits `app_id`; update includes the existing `app_id`. Submit the complete current record so metadata is not accidentally cleared.

Before creating or updating, read the authenticated category list and resolve the exact enabled category. Category names and slugs that look similar can have different storefront visibility. KEMI传书 (`org.kemi.send`) must use the enabled public category `探索` for every published platform; do not use the restricted `开发工具` category or its `工具` slug. After publishing, verify the app is present in the platform's default public list with `category` omitted.

```json
{
  "app_id": 51,
  "app_name": "Product Name",
  "package_name": "com.company.product",
  "os_type": "macos",
  "category": "工作",
  "version_name": "1.0.127",
  "version_code": 10127,
  "download_url": "https://cdn.example/product.zip",
  "icon": "https://cdn.example/icon.png",
  "apk_sha256": "64 lowercase hexadecimal characters",
  "file_size": "285183449",
  "file_size_bytes": 285183449,
  "short_desc": "Accurate short description",
  "long_desc": "Accurate tested capabilities",
  "release_notes": "Changes in this release",
  "languages": ["中文"],
  "permissions_list": [],
  "screenshots": [],
  "promo_image": "",
  "list_in_store": 1,
  "force_update": 0
}
```

### Critical size compatibility invariant

Always send both:

- `file_size_bytes`: exact integer bytes;
- `file_size`: the same number as a decimal string.

The update API can be correct while the storefront detail remains unusable if only `file_size_bytes` is populated. A blank public `file_size` can disable download with a combined “missing HTTPS, size, or SHA-256” message.

## macOS release gate

Required order:

1. Release build.
2. Developer ID Application signing, including nested code.
3. `codesign --verify --deep --strict`.
4. Create notarization archive.
5. Submit with `xcrun notarytool`; require `Accepted`.
6. Staple the `.app`; validate the staple.
7. Require `spctl` to report `accepted` and `Notarized Developer ID`.
8. Recreate the final distribution archive after staple.
9. Recompute final bytes and SHA-256.
10. Upload only that post-staple archive.

An `In Progress` record after an interrupted multipart upload is not proof that the package reached Apple. Query the submission ID. If the client explicitly reports incomplete upload and no final acceptance arrives, resubmit the same signed notarization archive rather than rebuilding the app.

## Windows release gate

- Verify the intended Authenticode signer and status on Windows.
- Verify exact bytes and SHA-256.
- Confirm the installer contains app-local dependencies required by the product.
- Install on a clean or isolated Windows environment and start without relying on an existing developer toolchain.
- Verify file associations and uninstall behavior when they are release requirements.

## Four-layer post-release verification

### 1. Developer record

Requery `/api/apps/list` and assert:

- one matching record;
- correct app ID, package, OS, version, and status;
- `list_in_store=true` when intended;
- HTTPS URL;
- both size fields;
- correct SHA-256;
- no unintended draft or duplicate.

### 2. Public storefront detail

Requery `/api/store/apps/{app_id}?os={os}` and assert:

```text
data.app.file_size == exact byte string
data.app.download_url starts with https://
data.app.apk_sha256 == local SHA-256
data.app.version_code == released code
```

This endpoint is the storefront download-button contract. Do not substitute the developer list or update-check response.

Also query the unfiltered platform list:

```http
GET /api/store/apps?page=1&pageSize=100&os={os}
```

Do not send `category` for this “全部” check. Require the released app to be present in `data.list`. For KEMI传书, verify the returned category is `探索`; a record categorized as the restricted `开发工具` fails storefront visibility acceptance even when its detail endpoint remains readable.

### 3. CDN

Require HTTP 200 and `Content-Length == local bytes`. For first release, high-risk changes, or any prior integrity incident, download the whole object, recompute SHA-256, and install that downloaded artifact.

### 4. Update checks

- Query with the immediately older code: `has_update=true`; verify target code, URL, bytes, SHA-256, package, and OS.
- Query with the released code: `has_update=false`.
- Explicitly pass `os` for Windows/macOS/Linux/iOS to avoid selecting another platform sharing the package name.

Finally inspect the visible storefront and perform the actual download/install path. A machine-readable pass does not replace a disabled-button or installer-error check.

## Client self-update gate

The client must:

- query the correct package, OS, and integer local version;
- expose a comprehensible update state and progress;
- stream downloads without unbounded memory use;
- verify exact bytes and SHA-256 before execution/opening;
- never install an incomplete or mismatched package;
- avoid replacing a running Windows executable directly; use a detached updater/installer;
- on macOS, either open the verified notarized distribution for a user-guided replacement or use a separately signed and audited helper;
- preserve the current working version if installation fails.

## Stop conditions

Do not claim completion if any of these remains:

- signature or notarization is missing;
- upload completion does not match local bytes/hash;
- duplicate identity exists;
- public detail has blank size, non-HTTPS URL, or missing hash;
- CDN length differs;
- old version cannot discover the release;
- current version continues to discover itself;
- visible storefront cannot download;
- clean installation or launch fails;
- temporary credentials remain.

## Report fields

Record per OS: time, actor, Git commit, build environment, artifact path, package/OS/app ID, create vs update, versions, bytes, SHA-256, signature evidence, notarization ID/status where relevant, upload completion, developer record, public detail, CDN, positive and negative update checks, visible storefront result, clean install result, self-update result, and remaining limitations.
