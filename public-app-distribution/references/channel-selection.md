# Channel selection

Choose channels deliberately; do not create accounts everywhere without confirming the app type and package are accepted.

| Channel | Best fit | Typical package | Primary gate |
|---|---|---|---|
| Apple App Store | Native macOS/iOS discovery and managed updates | signed archive uploaded through Apple tooling | paid Apple Developer membership, App Review, sandbox/entitlements |
| Microsoft Store | Windows discovery and managed updates | MSIX/EXE depending current policy | Partner Center identity, package identity, certification |
| Uptodown | Broad cross-platform download catalog | signed/notarized installer or archive | developer account, CAPTCHA/MFA, malware scan, editorial review |
| Softonic | Editorial/download discovery | canonical vendor download or uploaded package | submission/editorial acceptance and reputation checks |
| GitHub Releases | Open-source and developer audience | signed installers plus checksums | public repository and durable release notes |
| Homebrew Cask | Technical macOS audience | notarized stable URL artifact | public versioned URL, checksum, cask review |

Check current official publisher documentation at execution time because accepted package types, fees, review fields, and regional requirements change.

Prefer the smallest channel set that reaches the requested audience. Use the vendor's own website as the canonical support/privacy/update source even when mirrors are added.

Do not confuse states:

- `uploaded`: bytes accepted by a portal.
- `processing`: portal is scanning or extracting metadata.
- `submitted`: listing/binary was explicitly sent for review.
- `in-review`: reviewer has begun or queued review.
- `published`: public listing is reachable and the intended build is downloadable.
