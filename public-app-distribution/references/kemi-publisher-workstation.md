# KEMI macOS publisher workstation

Use this reference only when publishing from the existing KEMI Mac under `/Users/newlink`. It tells another operator where the approved identities and authenticated sessions are managed without copying secrets into source code or documentation.

## Handoff contract

This Mac is the publishing workstation. There is no shared plaintext "password file" to find or copy. Existing release credentials are already kept in macOS Keychain, the browsers' password managers, and authenticated browser sessions. An operator who receives this skill should use those protected stores through their normal UI or named keychain profile, not ask the user to repeat known passwords and not inspect the underlying credential databases.

The stored credentials are reusable only for accounts, teams, and channels that the current release is authorized to use. A new App still needs its own bundle ID/listing record, channel-compatible package, metadata, and an available role on the publisher account. Credential availability does not prove that those product-level prerequisites exist.

### First five minutes for another App

1. Read this file plus the channel reference linked from `SKILL.md`; do not start by asking for passwords.
2. Identify `product + platform + version/build + artifact SHA-256`, the source commit, bundle/package ID, and intended publisher organization.
3. Check the existing authenticated portal session. If signed out, invoke autofill from the protected location in the table below.
4. For direct-download macOS packages, verify the named Developer ID identity and `KEMI_NOTARY` profile before building. For Mac App Store packages, verify the Apple team, App record, Apple Distribution signing, and provisioning separately.
5. Upload or submit only after the portal identity matches the release identity. Reopen the exact backend record afterward and save the persistent state/ID as evidence.
6. If CAPTCHA, MFA, trusted-device approval, legal acceptance, paid enrollment, or account recovery appears, prepare everything else first and foreground only that one human gate. Resume automatically after it is completed.

## Ready-to-use credential locations

| Purpose | Approved location on this Mac | How to use it |
| --- | --- | --- |
| Apple Developer ID signing | Current macOS user's **login Keychain**; identity label `Developer ID Application: zhen ji (26T5WV4GLP)` | Confirm with the normal code-signing identity check, then reference the identity label in the signing command. Never export the private key for routine local releases. |
| Apple notarization | Current macOS user's **login Keychain**; `notarytool` profile `KEMI_NOTARY` | Use `xcrun notarytool history --keychain-profile KEMI_NOTARY` as the non-mutating credential check, then submit with the same profile. Do not request or print the Apple app-specific password. |
| App Store Connect | Google Chrome profile `niu`; reuse its authenticated Apple publisher tab/session or Chrome Password Manager | On this workstation Chrome `niu` is the field-verified primary route for App Store Connect. Open the exact App record, verify the publisher team and App ID, and use the browser's saved-login UI if the session expired. Do not switch to Safari during an active release merely because authentication needs refreshing. Apple MFA or account recovery stays with the account holder. |
| Uptodown publisher portal | Google Chrome profile `niu`; reuse its authenticated publisher tab/session or Chrome Password Manager | Open the canonical Uptodown admin page in the `niu` profile. Uptodown login/CAPTCHA must be completed in Google Chrome on this workstation; Safari has repeatedly failed authentication and must not be used for this portal. If signed out, use the saved-login UI. A CAPTCHA message is not a password failure. |
| Softonic Publishing Center | Google Chrome profile `niu`; reuse its authenticated publisher tab/session or Chrome Password Manager | Open Publishing Center, then verify organization `KEMI` and the product/platform card before editing. Do not reuse a Windows card for a Mac submission. |
| SourceForge Business Software | Initial vendor-listing request does not require a publisher login; follow-up account onboarding arrives through the submitted company contact | Use the official Business Software vendor route. After approval, use the account link delivered by SourceForge and save any new credential only through the approved browser password manager. |
| Verification mailbox | Existing authenticated webmail session on this Mac, only when that mailbox is explicitly authorized for the current release | Search only for the fresh portal verification or review message. Do not copy mailbox passwords or session data. If the mailbox session is unavailable, foreground only the OTP field for the account holder. |
| Microsoft Partner Center for the current KEMI Windows products | Microsoft account `caucy2002@163.com` only | Reject Chrome autofill or cached sessions for `caucy2026@outlook.com`; sign out of the incorrect Live session and restart with the 163 account before opening either product record. Never request or use the old account's recovery/MFA code for this release. |
| Signing/notarization operating guide | `/Users/newlink/kemi/priv/MACOS-DEVELOPER-ID-SIGNING-NOTARIZATION-GUIDE.md` | Read before signing or notarizing. It is the authoritative local handoff for certificate, Team ID, `KEMI_NOTARY`, packaging, Gatekeeper, and renewal checks. |

The publisher contact used for the current vendor submissions is `jince.ji@newlink-sz.com`, with company `Shenzhen NewLink Software Co., Ltd.` and website `https://www.newlinksz.cn/`. Treat this as non-secret listing metadata, not as proof that a login exists for every portal.

## Browser password-manager paths

Use the browser UI; never read or copy browser credential databases.

- Chrome: select profile `niu` → Password Manager → search the exact portal domain. Use the offered credential through autofill; do not reveal it in chat or paste it into notes.
- Safari: use only when the user explicitly requests it or Chrome is unavailable and a currently authenticated Safari session has already been verified. Do not use Safari as a speculative fallback during an active release.
- Apple account: prefer the existing App Store Connect session. If Apple requests a trusted-device code, pause automation on that window until the owner finishes the code.

Do not treat the existence of a Chrome/Safari profile as proof that a current credential is stored. First try the existing authenticated session, then the official password-manager prompt. If neither works, classify the exact login gate instead of guessing.

### Portal-to-store lookup

| Portal | Start here on this Mac | Credential lookup |
| --- | --- | --- |
| App Store Connect / Apple Developer | Chrome profile `niu` first and by default; keep the same authenticated Chrome tab for build attachment, metadata, submission, and status checks | Chrome Password Manager entry for the exact Apple domain, or the already authenticated Apple session. Safari is not the default route on this workstation. |
| Uptodown Developers Console | Chrome profile `niu` only; do not use Safari for authentication | Chrome Password Manager entry for the exact Uptodown domain |
| Softonic Publishing Center | Chrome profile `niu` | Chrome Password Manager entry for the exact Softonic domain |
| SourceForge onboarding | Existing company-contact email/session after SourceForge approves the vendor request | Use only the official onboarding link; save any newly created login in the approved browser password manager |
| Verification/review email | Existing explicitly authorized webmail session | Search only for the fresh message belonging to the active portal and App |

Never copy a masked password out of autofill merely to learn it. Successful autofill and a verified authenticated account/team are sufficient. If the browser does not offer a saved credential, record `credential unavailable` and follow the portal's official recovery flow rather than trying passwords from chat history.

On this workstation, the verified Uptodown recovery path is Chrome profile `niu` → `https://www.uptodown.dev/` → use the browser-offered saved Google account to continue. When that account chooser is already available and the release is authorized, complete it directly without asking the owner to re-enter a password. Success is proved only after the portal opens the exact intended application record; the account chooser or login page is not submission evidence.

## New-App fast start

Another operator can begin a new public App release on this Mac as follows:

1. Read the project release instructions and freeze the source commit, platform, channel flavor, marketing version, build number, and minimum OS.
2. Create a ledger row for each `product + platform + channel`, including the intended artifact path and SHA-256.
3. For macOS direct-download catalogs, confirm the Developer ID identity in the login Keychain, build a Universal `arm64 + x86_64` candidate when required, sign all nested code, notarize with `KEMI_NOTARY`, staple, run Gatekeeper assessment, and calculate the final hash after stapling.
4. For Mac App Store, use the isolated App Store flavor, Apple Distribution/profile flow, App Sandbox, and the product's existing App Store Connect record. Do not substitute the Developer ID direct-download package.
5. Open the requested portal in the existing authenticated browser profile and verify account/team, product, platform, version/build, and artifact hash before upload.
6. Complete metadata and upload the exact artifact. Obtain the required action-time confirmation for submission/legal gates when the environment requires it.
7. Leave the transient result page and reopen the dashboard or exact version record. Only the persistent backend state advances the ledger.
8. Continue hourly checks across all channels. On rejection, record the exact reason, make the smallest channel-specific correction in an isolated branch/flavor, retest, and resubmit.
9. Mark `published` only after an anonymous product page exposes the intended version and the public download passes hash/identity, installation, launch, and core-workflow checks.

## What must not be copied

The following already live in protected stores on this Mac and must stay there:

- Apple ID password and app-specific password;
- Uptodown, Softonic, SourceForge, email, or other portal passwords;
- MFA/OTP/recovery codes;
- Chrome/Safari cookies, Login Data databases, or exported sessions;
- Developer ID private key, exported P12 password, App Store Connect API private key;
- `KEMI_NOTARY` underlying credentials.

Skills and release ledgers store only the labels and locations above. If a colleague moves the workflow to another Mac, invite their Apple account to the correct team and transfer signing material through the organization's controlled process; do not copy this workstation's password or browser database.

## Session-expiry recovery

1. Reopen the exact portal using the previously verified browser route: Chrome profile `niu` for Apple, Uptodown, and Softonic; Chrome `niu` for SourceForge once vendor onboarding supplies an account.
2. If the session expired, invoke the saved-login prompt for that portal domain.
3. If the portal shows CAPTCHA, MFA, trusted-device approval, legal acceptance, or account recovery, bring only that gate forward and wait for the owner.
4. Once completed, fetch a fresh page state, verify organization/team and product/platform, then resume automatically without asking for another “continue.”
5. If authentication still fails, stop password retries and document the exact error, timestamp, portal domain, and next recovery action.

## Verified route inheritance

Treat the browser, package type, account profile, and state-verification method below as release parameters, not suggestions. Reuse them on later runs unless the portal or workstation has materially changed and the alternative is independently proven.

| Channel | Fixed workstation route | Accepted release input and proof |
| --- | --- | --- |
| Apple App Store | Build/export/upload with Apple's official Xcode command-line transport; use Chrome profile `niu` for App Store Connect | Apple Distribution-signed App Store PKG, processed build attached to the exact version, then persistent `Waiting for Review`/`In Review`/published state on the exact App record |
| Uptodown | Chrome profile `niu` only | Developer ID-signed, Apple-notarized Universal ZIP; verify exact file ID/version/SHA-256 and both listing-level and file-level states |
| Softonic | Chrome profile `niu` | Signed, notarized, stapled DMG or PKG when the Mac form rejects ZIP; verify the exact Mac application/version record after saving or submitting |
| SourceForge | Chrome profile `niu`, Business Software vendor-listing route only | `Request Received` proves onboarding submission only; publication requires the later product record and anonymous public page |
| Chocolatey (KEMI Windows) | Build a normal Chocolatey `.nupkg`, but embed the final signed EXE or complete signed payload under `tools/`; never use an external application-download URL in new KEMI package versions | Verify Authenticode and timestamp before packing, reopen the `.nupkg` to prove the payload is physically present and byte-identical, then run offline install/launch/uninstall before submission and repeat the inner-payload hash check after anonymous public download |

Do not repeat a failed browser experiment or change package format merely because a session expired. Restore the verified session or classify the precise gate. A different route is allowed only after a concrete environment change or a fresh authoritative portal requirement, and its success must be written back here after independent verification.
