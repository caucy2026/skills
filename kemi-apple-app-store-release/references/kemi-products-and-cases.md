# KEMI Apple product and case ledger

These are historical, non-secret identifiers and observed states from the September 2026 release work. They accelerate identity checks but do not replace a fresh App Store Connect read. Mutable states below are explicitly historical.

## KEMI Send / KEMI传书

- Apple App ID: `6810529561`.
- Historical reviewed version: macOS `2.0.5`.
- Verified outcome from the session: the App later reached `可分发`, and an anonymous public page was observed at `https://apps.apple.com/cn/app/kemi%E4%BC%A0%E4%B9%A6/id6810529561?mt=12`.
- This is a verified successful route, not a promise that the current version remains public. Re-check the anonymous page and exact public version on every new run.

## VibeKits

- Apple App ID: `6809822607`.
- Historical submission: macOS `1.9.162`, build `2169`.
- Historical submission ID: `9ada6dbb-0712-49bc-9082-9dc79e808d57`.
- Historical state: `Waiting for Review` from 2026-09-10 13:34 CST during repeated checks.
- Historical support case: `102968433295`, recorded after an official status inquiry on 2026-09-19.
- This case was not verified as published in the captured session. Treat it as historical `in-review`/support-follow-up evidence only. Do not withdraw or replace it merely to ship newer code unless the live state or safety requires that action.

## KEMI OFFICE

- Apple App ID: `6813291300`.
- Historical candidate: macOS `1.0.137`, build `10138`.
- Historical submission ID: `e7bfba9e-a838-49e6-b75d-8d81afd0b141`.
- Historical correction: remove unnecessary `com.apple.security.network.server`; retain `com.apple.security.network.client` for outbound-only network behavior, then rebuild and resubmit.
- Historical resubmission time: 2026-09-19 05:24 CST.
- Last captured state was `Waiting for Review`, not published. A red badge was not sufficient by itself to classify a new rejection; the exact submission/Resolution Center record had to be opened.

## What these cases proved

- Chrome profile `niu` can carry the authenticated App Store Connect workflow on the KEMI publisher Mac.
- Official Xcode transport plus the exact processed-build attachment and explicit Submit for Review is the correct route.
- A direct Developer ID/notarized artifact is not interchangeable with a Mac App Store package.
- Removing an unused entitlement is preferable to writing a broad reviewer justification for functionality the App Store build does not expose.
- Exact version/build/submission state must be checked; summary cards, TestFlight `准备提交`, old red badges, and anonymous search absence can all be misleading.
- The session did not prove that VibeKits or KEMI OFFICE had become public. Keep that uncertainty visible until fresh anonymous evidence exists.

