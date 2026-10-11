# HBBC architecture and maintained context

## Product role

HBBC is a self-hosted multi-App service with independently usable modules:

```text
HTTP/HTTPS core
├─ configuration-driven download/static sites
├─ App/channel/published policy catalog
├─ phone/password authentication and device binding
├─ presence and usage accounting
├─ donation/payment entitlement
├─ administrator and operations UI
└─ read-only hbbs online monitor
```

It may run beside RustDesk hbbs/hbbr, but it is not their process, protocol, database, or lifecycle owner.

## Source map

- `hbbc/src/main.rs`: configuration, listeners, download routing, App catalog/publication, administrator sessions/API/UI, atomic JSON persistence, route dispatch, and integration document generation.
- `hbbc/src/account.rs`: SQLite schema/migrations, account registration/login/tokens, device identity/slots, presence, usage, donation orders/entitlements, operations queries, pagination, level and privilege administration.
- `hbbc/src/hbbs_monitor.rs`: bounded read-only hbbs registration/online inspection. Failure must not modify or restart hbbs.
- `hbbc/src/bin/payment_qr.rs`: payment QR support utility; it is not permission to expose or copy payment keys.
- `deployment/hbbc.example.json`: example only; never overwrite production configuration merely because it changes.
- `deployment/kemi-rustdesk-hbbc.service`: hbbc unit. Ordinary updates restart only this unit.
- `docs/HBBC-*.md` and `CHANGELOG.md`: public behavior, compatibility, migration, and release evidence.

## Data and generated-contract separation

Do not confuse:

1. process configuration for listeners, TLS paths, refresh and module file locations;
2. administrator App/channel/plan/resource catalog and published snapshots;
3. account SQLite data for users, tokens, devices, presence, usage, orders, entitlements and overrides;
4. generated client `integration.json`/Markdown, a read-only projection of published server data.

Clients consume the generated contract; operators maintain configuration/catalog; neither edits the account database manually.

## Maintained evolution baseline

The historical maintained source reached `1.4.10` in September 2026. Always re-read `Cargo.toml`, `Cargo.lock`, newest changelog, Git state, and production version.

- 1.3.x: App catalog, channels, levels/resources, authentication, usage, donation/payment, operations, App ID migration.
- 1.4.0–1.4.3: hardware/customer usage, real MAC, account-centric switching, same-MAC dedup and token revocation.
- 1.4.4: external static HTTPS sites.
- 1.4.5: independent server-side pagination.
- 1.4.6: one-year donation entitlement and renewal/expiry.
- 1.4.7–1.4.8: read-only hbbs online monitor and response fix.
- 1.4.9: per-App/per-user device-limit override, independent of level and privileges.
- 1.4.10: separate account/donation/usage pages, bounded pagination, visible save feedback.

## Private and public documentation

When present, protected `priv/hbbc` documents are organized by modules `00`–`08`; never copy its secrets/recovery assets into a skill or public repository. Public source/behavior docs belong with the server source. Historical `09-history` explains migrations but is not the default new-development contract.

Use the newest current module document first. Read older records only for migration/compatibility and record when live source differs.
