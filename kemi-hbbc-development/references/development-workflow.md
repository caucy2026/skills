# HBBC development workflow

## Establish the change surface

Before editing, answer from code and current docs:

- Which route receives the request?
- Which App/channel/user/device identity scopes it?
- Which persisted object or SQLite transaction is authoritative?
- Which generated integration field or admin page exposes it?
- Which old client/database behavior must remain?
- What proves rollback preserves accepted writes?

Inspect the exact worktree/staged state. Adjacent dirty server files may belong to others; stage only intended hbbc files.

## Storage and migration rules

- Catalog JSON writes keep validation and atomic replacement; do not introduce partial multi-file publication.
- Account SQLite/WAL migrations are additive, idempotent on repeated startup, and tested from an old database.
- Live backup uses SQLite `.backup`, never a raw WAL copy advertised as consistent.
- Preserve accounts, password hashes, tokens, devices, real MAC, orders, entitlements, usage and audit data.
- New uniqueness rules deduplicate/migrate before creating the unique index.
- Never use production data as a development fixture or print private rows as evidence.

## API and authorization rules

- Validate App/channel/target ownership, session/token, device identity, request size, and enum/query allowlists at the boundary.
- Administrator browser sessions, administrator automation tokens, and user tokens are separate. Do not put an admin token in a URL.
- User tokens are App-scoped. A phone number used in two Apps does not merge accounts or entitlement.
- Public configuration/integration endpoints expose policy, not secrets.
- Payment callbacks require signature, server-side order/App/user/amount checks, replay-safe idempotency and durable audit.
- Preserve client-visible error meanings; add optional fields rather than repurposing old ones.

## Admin UI and scale

Accounts, donations, devices and usage are independent server-paginated pages rather than unbounded nested arrays. Require bounded page size, whitelisted query field, pagination metadata, previous/next and direct jump, loading/empty/error states, stable save feedback including idempotent saves, and narrow/mobile validation.

Verify the real authenticated browser click path and resulting API state. HTML compilation, string search or HTTP 200 alone is insufficient UI acceptance.

## Test layers

Run the narrow failing test, then affected module tests, then the formal source gate:

```text
cargo fmt --check
cargo test --locked
cargo clippy --locked --all-targets -- -D warnings
```

Use the maintained release skill for the Linux artifact. Keep caches/targets in the machine's required project-specific build directory.

Tests should cover positive/negative auth, cross-App isolation, old client missing optional fields, old database migration/repeated startup, idempotency, expiry/time boundaries, pagination limits, relevant concurrency, and module-failure isolation.

## Documentation and versioning

Do not bump a version for diagnosis alone. When released behavior changes, align `Cargo.toml`, lock entry, build info, changelog, docs, release directory, binary `--version`, and production report.

Record exact suite and revision. A targeted suite does not prove unrelated payment, authentication or download behavior.
