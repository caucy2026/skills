# Apple App Store workflow

Use current Apple Developer and App Store Connect documentation as the authority; portal fields and policy wording evolve.

## Preflight

1. Confirm the bundle ID, team, App Store record, agreements, roles, certificates, provisioning profiles, and next build number.
2. Audit entitlements against actual code paths. Retain only required capabilities and prepare plain-language reviewer explanations for unusual access such as incoming network listeners, Downloads read/write, accessibility, screen capture, background services, or remote control.
3. Use an App Store-specific build configuration. Remove prohibited external purchase/donation links from that binary when Apple IAP rules apply; do not alter unrelated direct-download variants.
4. Ensure Support URL and Privacy Policy URL are public, functional, product-specific, and contain contact/privacy information.
5. Do not hide a feature during review and unlock it later by time, launch count, server flag, reviewer account, or geography. Permanently omit it from the App Store target or disclose and make it compliant.

## Build and upload

- Build an Xcode Archive with Apple Distribution signing and the correct App Store profile. Do not apply the app target's entitlements globally to Pods, Swift packages, helpers, or extensions; each target needs its own valid signing configuration.
- Validate archive bundle IDs, nested code, architectures, minimum OS, entitlements, privacy manifests, version/build, and export compliance.
- Upload with Xcode Organizer or current Apple transport tooling. Record the delivery/upload identifier and wait for processing.
- Attach the processed build to the correct version, complete privacy/nutrition labels, encryption declaration, screenshots, review notes, contact details, and demo credentials when required.
- The final “Submit for Review” action is distinct from upload. Verify the version state in App Store Connect after submission.

## Reviewer notes

Explain why sensitive entitlements are necessary, where the user triggers them, what data is accessed, whether access is local or remote, how consent is obtained, and how it can be disabled. Provide a deterministic review path and test account only when needed.

## Rejection loop

Classify each issue as binary, entitlement, metadata, privacy, business model, or reviewer-access. Fix only the affected channel variant, increment the build number, reproduce the correction, upload, attach the new build, reply with precise changes and navigation steps, and explicitly resubmit. Preserve the rejection ID and submission ID in the release report.

Common failures:

- uploaded but never submitted;
- invalid/nonfunctional support page;
- external donation/payment links;
- unnecessary or unexplained entitlements;
- signing one target's entitlements onto every dependency;
- promising Intel/minimum-OS support without validating Mach-O slices and deployment targets;
- reporting “in review” based on an old version instead of the exact submitted build.
