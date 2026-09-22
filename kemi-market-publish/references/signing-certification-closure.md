# Signing and certification closure

Read this reference for every formal macOS or Windows KEMI market publication. Signature work must preserve the product's stable bundle/package identity and existing entitlements.

## Shared invariants

- Freeze package name, bundle ID, executable name, version name/code, minimum OS, and intended architectures before signing.
- Sign only final build outputs. Any modification to nested code, resources, plist, entitlements, installer contents, or archive after signing invalidates downstream evidence.
- Use an intended organization certificate. Ad-hoc signing is never a formal release.
- Timestamp signatures where the platform supports it.
- Record certificate subject/team, artifact bytes, SHA-256, verification output, and signing/notarization identifiers without recording credentials.
- A failed or unavailable trust service is an invalid test environment until host validation proves otherwise.

## macOS full closure

### 1. Pre-sign inspection

Verify:

- the `.app` has the stable user-facing bundle name expected by previous releases;
- `CFBundleIdentifier`, `CFBundleShortVersionString`, `CFBundleVersion`, and `LSMinimumSystemVersion` match the release plan;
- the main executable contains every promised architecture, including `arm64` and `x86_64` for a Universal release;
- bundled frameworks, helpers, extensions, libraries, and executables are present;
- entitlements are intentional and compatible with the app's permission flows.

Do not rename the bundle to include a version when the installed product and updater require a fixed `/Applications/<Product>.app` path.

### 2. Developer ID signing

Use `Developer ID Application` with hardened runtime and secure timestamp. Sign nested code in dependency order when the build does not already produce a correctly signed bundle. Preserve required entitlements; do not add entitlements merely to silence a failure.

Immediately require:

```text
codesign --verify --deep --strict --verbose=2 <app>
codesign -dv --verbose=4 <app>
```

Inspect the final designated requirement, TeamIdentifier, Authority chain, timestamp, runtime flag, and entitlements. Run these checks on the real host.

### 3. Apple notarization

Create a notarization ZIP from the signed app, submit it with `xcrun notarytool` using an approved keychain profile, and wait for the terminal status. Record the submission ID. Require `Accepted`; `In Progress`, an upload interruption, or a missing record is not acceptance.

If rejected, retrieve the notarization log, fix the actual issue, rebuild/re-sign, and submit the new artifact. Do not staple or publish a rejected build.

### 4. Staple and final distribution archive

After acceptance:

1. staple the ticket to the `.app`;
2. validate the staple;
3. require Gatekeeper acceptance with source `Notarized Developer ID`;
4. recreate the final distribution ZIP from the stapled app;
5. compute the final ZIP byte count and SHA-256;
6. extract that exact ZIP and run `scripts/verify_macos_release.sh` outside the sandbox.

Never upload the pre-staple archive. Never sign the ZIP as a substitute for signing nested app code.

### 5. Real installation and launch

Install from the final distribution ZIP using the supported user path. Confirm:

- the bundle installs under its stable name;
- it launches on the current Apple Silicon machine;
- the app does not require a development toolchain or extra configuration;
- prior configuration and updater identity remain compatible;
- for a Universal release, the main executable reports both `arm64` and `x86_64` even when an Intel machine is not available.

Where the release claims an older macOS target, verify linked minimum OS metadata and avoid APIs unavailable on that target. State clearly when an actual older-OS or Intel launch remains untested.

### 6. Post-CDN validation

Download the public CDN object, require byte-for-byte SHA-256 equality, extract it, and repeat codesign, staple, Gatekeeper, architecture, fixed-name, install, and launch validation. Only the downloaded object proves what users receive.

## Windows full closure

### 1. Pre-sign inspection

Confirm package name, version, architecture, installer/executable format, embedded runtime dependencies, and clean-machine install requirements.

### 2. Authenticode signing

Sign the final `.exe`/`.msi` with the intended organization certificate, SHA-256 digest, and a trusted timestamp service. Sign nested binaries first when required by the packaging format.

On Windows, require `Get-AuthenticodeSignature` or SignTool verification to show `Valid` and the intended signer. A missing PE security directory, `NotSigned`, unknown signer, or invalid timestamp blocks formal publication.

### 3. Clean-machine validation

On the trusted Windows device lab, verify install, first launch, required runtimes, update flow, rollback/preservation on failure, and uninstall behavior. Compute bytes and SHA-256 for the exact signed package after all signing is complete.

### 4. Post-CDN validation

Download the store object on Windows, require bytes/SHA-256 equality, repeat Authenticode verification, install, launch, update discovery, and current-version no-loop check.

## Closure matrix

| Gate | macOS | Windows |
|---|---|---|
| Stable identity/version | required | required |
| Intended architecture | Universal evidence when claimed | intended PE architecture |
| Platform signature | Developer ID Application | Authenticode |
| Timestamp | required | required |
| Platform certification | Apple notarization Accepted + staple | trusted Authenticode chain |
| Host verification | codesign + stapler + spctl | SignTool/PowerShell |
| Clean install/launch | required | required |
| Final bytes/SHA-256 | required | required |
| CDN byte/hash equality | required | required |
| Downloaded artifact re-verification | required | required |
| Older version sees update | required | required |
| Current version sees no update | required | required |

Do not say “signed”, “certified”, or “formally published” when any required platform gate is missing. Report the exact completed gates and blocker instead.
