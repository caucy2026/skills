---
name: project-about-page
description: Design, implement, review, or migrate an application's About page, truthful product description, capability list, promotional carousel, offline fallback, and secure resource cache. Use when a project needs a 关于页、产品介绍、宣传图轮播 or reusable About-page specification; do not use for app-store listings or application self-update flows.
---

# Project About Page

Build the About experience from verified product facts, not from copied marketing text.

## Start with a product evidence profile

Before designing or changing UI, identify from the target project:

- official product name, icon, installation identity, version source, and design tokens;
- primary users, delivered value, and a two-line description grounded in current behavior;
- capability or supported-format manifest and the code/tests proving each claim;
- bundled offline content and, when present, the project's own HTTPS promotional-resource endpoint;
- platform constraints, navigation pattern, accessibility requirements, and existing self-update architecture.

Do not inherit another project's product name, slogans, format count, endpoint, cache location, virtual host, colors, or performance claims. Mark missing evidence as unresolved instead of inventing content. Claims such as offline, private, secure, fast, or support for N formats require test or source evidence.

## Route the work

Read [references/about-page-playbook.md](references/about-page-playbook.md) completely when implementing, migrating, or auditing the page. Use its KEMI OFFICE values only as a labeled worked example; replace every project-specific value before delivery.

For a design-only request, produce the product evidence profile, information architecture, state table, responsive interaction specification, and acceptance matrix. For implementation, also inspect the target repository and adapt to its existing UI, native bridge, storage, and capability sources rather than imposing a fixed framework.

## Required product behavior

- Keep product identity, version, truthful description, and actual capabilities readable without the network.
- Show cached or bundled content immediately. Background resource refresh must not delay app launch, document opening, or first meaningful paint.
- Model no-cache loading, ready cache, successful refresh, failed refresh, corrupt asset, and offline fallback explicitly; never leave a white screen or endless spinner.
- For remote collections, download into staging, validate the complete manifest and every asset, then atomically activate the entire set. Preserve the last known-good active and backup sets.
- Expose only validated content-addressed asset URLs to web UI. Do not expose arbitrary local paths, secrets, or raw service responses.
- Make carousel count, indicator count, selected state, keyboard behavior, timing cleanup, and 0/1/many-image behavior deterministic and accessible.
- Derive the displayed capability list from the same manifest used by open routing, drag-and-drop, file associations, or their validation tests.
- Keep About content separate from the application marketplace and from self-update state. Update failures and protocol errors do not belong on the About page.

## Completion gate

Do not call the work complete until evidence covers:

- identity, descriptions, versions, capability counts, and legal ownership;
- first-use online and offline behavior, cached offline behavior, set additions/removals/reordering, integrity failure, interrupted download, active corruption, and backup recovery;
- zero, one, several, and maximum supported images; click, keyboard, selected indicator, responsive layout, DPI, and repeated page entry/exit;
- no startup-path regression, bounded disk use, no hidden timers or UI-thread cleanup, and no mixed or partially activated resource set;
- source paths, test results, remaining limitations, and every project-specific replacement made from the worked example.

If implementation is requested, modify and test the project. If only a specification is requested, clearly distinguish proposed behavior from verified existing behavior.
