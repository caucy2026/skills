# KEMI known products and rejection lessons

These are September 2026 historical identities. Re-read the live ledger and portal because later submissions may supersede them.

## Publisher

- Microsoft account: `caucy2002@163.com`
- Organization: KEMI / Shenzhen NewLink Software Co., Ltd.
- Credential route: Chrome profile `niu` authenticated session or approved password-manager UI
- Reject unrelated cached account: `caucy2026@outlook.com`

Never record passwords, OTPs, cookies, recovery codes, certificate secrets, or PINs.

## KEMI Remote Office

- Product ID: `c759fbea-de94-45a5-981f-67cd1b2de329`
- Corrected Store build: `1.4.125+242`
- Artifact: `KEMI-Remote-Office-1.4.125+242-Microsoft-Store.exe`
- Size: `22,801,920` bytes
- SHA-256: `42626cde8378a1bee8062c6199f0cad3f04629305d495a79247b38d4d9262d05`
- Historical corrected submission ID: `1152921505701911851`

The earlier `+241` failed:

1. `10.2.7`: Add/Remove Programs name or publisher blank/unrelated.
2. `10.1.1.1`: Store name differed from installed `RustDesk` name.
3. `10.1.5`: Apps page promoted acquiring software outside Microsoft Store.

The `+242` flavor aligned executable/installer identity and publisher, and permanently removed Apps/marketplace navigation. Direct and internal-market builds stayed separate.

## KEMI Send

- Product ID: `5dc8e060-85ed-459f-8c2f-4ee0d87b5c59`
- Package record ID: `54612398`
- Rejected certification report: `fd930ec0-f881-48cc-be3e-58f43eb74a7d`
- Corrected source commit: `4cb34f9`
- Corrected Store build: `2.0.5+158`
- Artifact: `KEMI_Send-2.0.5+158-windows-x64-microsoft-store-setup.exe`
- Size: `22,359,896` bytes
- SHA-256: `50a7850ac41ed07405d734577d6e2812df19c227fca02c7715d0c08613cd3d6f`
- Historical immutable URL: `https://cdn.newlink-sz.com/Common/upgradefile1789740272014_KEMI_Send-2.0.5+158-windows-x64-microsoft-store-setup.exe`

The signed `+154` failed `10.1.5 Software Distribution` because `应用 -> 应用中心` exposed external acquisition. It could not be resubmitted unchanged. The `+158` flavor removed that entry, stamped correct outer metadata, signed and timestamped 19 inner PEs plus the outer installer, and matched after anonymous CDN download.

## Lessons

- Valid signing does not make a direct build Store-compliant.
- Signed inner files are insufficient if the downloaded outer installer is unsigned.
- A Store filename is not proof of a Store build; inspect the marker and UI.
- Partner Center must consume immutable bytes re-downloaded and hash-verified.
- A reused package link may land on Usage analytics; verify `/packages/<id>/edit`.
- Draft save and validation are not submission. Reopen the product after submission.
- `Review of application: 失败` requires the exact certification report, not more polling.
- The displayed SLA is not a guaranteed publication date; delay is not rejection.
- Work in the background and do not disturb another operator's browser or signing session.

