---
name: kemi-hbbc-development
description: Continue, implement, diagnose, test, document, hand off, or operate the KEMI HBBC multi-app download, account, device, presence, usage, donation, payment, admin, and read-only hbbs-monitor backend. Use for current hbbc work or legacy “dhhc” requests; use kemi-hbbc-release for the formal binary release/deployment gate and never treat hbbs/hbbr as part of an ordinary hbbc change.
---

# KEMI HBBC continuous development

Carry HBBC work forward from authoritative source and evidence. Do not reconstruct the project from chat memory or reduce it to the latest bug.

## Start from the maintained state

1. Read the applicable `AGENTS.md` and sibling `LOCAL-ENVIRONMENT-RULES.md` before acting.
2. Locate the maintained project by finding `hbbc/Cargo.toml`, `hbbc/src/main.rs`, `hbbc/src/account.rs`, `hbbc/src/hbbs_monitor.rs`, and `deployment/kemi-rustdesk-hbbc.service`. Do not assume another machine has the author's paths.
3. Record the repository/branch/HEAD, dirty files, hbbc package version, current docs, active processes/builds, and requested scope. Preserve unrelated changes.
4. Read [architecture and context](references/architecture-and-context.md). Treat its version examples as historical context; the live source, production readback, and newest acceptance record are authoritative.
5. Route only to the references needed now:
   - implementation, schema, tests, or UI: [development workflow](references/development-workflow.md);
   - App/account/device/presence/usage/donation/client semantics: [product contracts](references/product-contracts.md);
   - production diagnosis, documentation, backup, or teammate continuation: [operations and handoff](references/operations-and-handoff.md).

## Preserve the product invariants

- `hbbc` is independent from RustDesk `hbbs` and `hbbr`. An hbbc change does not authorize modifying, reinstalling, restarting, or releasing them. The hbbs monitor is read-only observation, not hbbs ownership.
- `dhhc` is a retired prototype name. Confirm the current hbbc source/service before reusing historical DHHC designs; there is no fourth DHHC production service.
- Every business record and policy is isolated by stable `app_id`; channel-sensitive data also uses `channel_id`. Display names never establish identity or authorization.
- Level `0` is the guest. Higher level names, permissions, donation amount, expiry, usage limits, P2P/relay rules, and resources come from the published server policy. Clients must not hard-code them.
- Server responses are authoritative for account level, effective permissions, entitlement expiry, device slots, payment state, online state, and usage decisions. A client cache may improve UX but cannot grant access.
- Account/device limits, account level, donation entitlement, and administrator extra privileges are separate controls. Changing one must not silently change another.
- Keep old clients and old routes working when adding optional fields, tables, indexes, filters, or pages. Use additive SQLite migrations and safe defaults unless the user explicitly authorizes a breaking change and migration.
- Authentication, SMS, payment, administrator, TLS, signing, and database secrets stay in protected server files or encrypted recovery storage. Never print or copy them into source, skills, logs, prompts, release packages, or public Git.

## Work to an evidence-backed result

1. Convert the request into explicit behavior, compatibility, data, UI, security, and rollback assertions. Separate already proven facts from proposed behavior.
2. Trace the complete path before editing: route in `main.rs` → account/storage logic in `account.rs` or monitor logic in `hbbs_monitor.rs` → generated integration contract/admin UI → client consumer if in scope.
3. Implement the smallest change that reaches the requested result. Keep module failure isolated so download pages, authentication, payment, presence, and monitoring do not unnecessarily take each other down.
4. Add regression tests at the authoritative layer. For migrations, test an old database, repeated startup, preserved rows/tokens/orders, and binary rollback compatibility. For admin UI, test API authorization, pagination/search, save feedback, empty/error state, and responsive behavior.
5. Run format, locked tests, and strict Clippy using the project/local environment rules. A source test is not production evidence; a successful HTTP response is not UI acceptance.
6. Update the nearest maintained change document with version, exact behavior, compatibility, tests, artifact identity when built, deployment boundary, rollback, and known gaps. Do not rewrite history to make an incomplete feature look complete.
7. If formal packaging or production mutation is requested, invoke `$kemi-hbbc-release` and follow its references/scripts. Do not duplicate an ad-hoc deployment route in this skill.
8. If cloud compilation is used, run `$cloud-build-cleanup` after the latest complete artifact is verified and retrievable.

## Completion boundary

Report separately: source state, implemented behavior, automated tests, data migration, client contract, admin UI, artifact/build, production deployment, public checks, rollback evidence, source backup, skill backup, and hbbs/hbbr unchanged evidence. Mark only observed stages complete.

For a handoff, leave one self-contained entry that lists the full objective, current version/source, completed evidence, missing acceptance, next three executable actions, active jobs, protected resources, authorization boundary, and stable evidence paths. A new teammate must be able to continue without rereading the old conversation.
