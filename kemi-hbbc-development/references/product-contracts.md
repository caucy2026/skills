# HBBC product and client contracts

## App, channel, policy and levels

- `app_id` is stable and administrator-chosen; changing it requires explicit migration.
- The server generates the first `channel_id`; clients never invent it. Display names do not establish identity.
- Catalog edits affect drafts. Clients use only a validated published snapshot and generated integration contract.
- Level `0` is guest. Logged-in baseline is commonly level `1`; names and permissions are App policy.
- A higher level replaces lower-level configured permissions unless policy explicitly says otherwise. Administrator extra privileges remain separate.
- Donation UI appears only after a real permission limit and when a higher eligible level exists. Highest level and trusted internal hardware do not show it.

## Authentication and device identity

- Registration: bot/human protection → phone/SMS → existing-account check → password entered twice → tokens → device binding.
- Password recovery uses verified phone/SMS and rate limits.
- `hardware_code` is stable device fingerprint; `hardware_mac` is normalized real MAC for production management/dedup. Report MAC during registration/binding, not every heartbeat.
- Same account plus same valid MAC reuses a slot. A changed hardware code revokes stale tokens and updates identity; uniqueness prevents duplicates.
- A replacement phone/device can log into the existing account and inherit current account permissions; records/tokens remain auditable.
- Device-slot override is keyed by `app_id + user_id`; maintained policy is default 3 and administrator extension 10. It does not change level, entitlement or extra privilege. Reducing the limit does not abruptly delete active records.
- Clients read `device.max_slots`/`bound_count` from the server rather than hard-code 3/10.

## Presence and usage

- Presence is lightweight and normally 60 seconds. It does not repeatedly upload real MAC or unrelated hardware inventory.
- HBBC unavailability must not freeze or crash the application's main function.
- Usage is server-time authoritative: start creates a lease, monotonic heartbeat renews it, finish closes it, and timeout prevents infinite charging.
- P2P/relay mode, duration/result/failure are separate. Presence online, usage permission and hbbs registration are different states.
- Client expiry enforcement uses current server responses and shows a clear limit message; permission description text alone is not enforcement.
- Retry transient transport/SQLite/5xx/timeout failures per current policy; explicit authentication, revocation or policy denial must not become an unlimited offline grant.

## Trusted KEMI hardware

Re-read the current client-specific hardware policy. The server never trusts a caller-provided `internal=true`; trusted status comes from registered installation/device evidence or explicit approval. Maintained KEMI hardware policy may grant broader P2P/relay usage and suppress donation UI while still requesting login for account services.

## Donation, payment and expiry

- Donation options, amount, target level and description are dynamic server data. Refresh after login and when opening the donation page.
- Order response is authoritative for amount; an existing unpaid order keeps its creation-time amount.
- Only verified idempotent server callback grants entitlement. Client buttons, screenshots or QR generation cannot.
- Donation history remains. Maintained entitlement duration is one year from confirmed payment; after all donation entitlement expires, a logged-in account returns to baseline, not guest/deleted.
- Allowed early renewal extends from existing expiry. Clients display server `level.expires_on` and stop using expired cached permission.

## Generated integration contract

Generated JSON/Markdown reflects the published App/channel/account policy: real IDs, endpoints, fields, heartbeat, permissions, device slots and rules. Do not hand-author a conflicting integration document or use example IDs from historical docs.
