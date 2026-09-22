---
name: kemi-storage-cleanup
description: Safely inspect and reclaim storage from caches, temporary debugging artifacts, stale build outputs, duplicate packages, and old application backups on KEMI development Macs and attached volumes. Use when the user asks to clean disk space, identify removable files, remove old caches, or prune historical bin/build artifacts; do not use for deleting source projects or current release deliverables.
---

# KEMI Storage Cleanup

Reclaim space without losing source code, current releases, active build state, test reports, signing material, or Codex task history.

## First principle — never delete irreplaceable inputs

This rule overrides cleanup targets, disk pressure, age thresholds, filename patterns, and size considerations:

- Never delete source code, Git metadata needed to preserve work, uncommitted changes, handwritten scripts or configuration, documentation, test reports, user media, certificates, private keys, keystores, provisioning profiles, notarization/signing credentials, or other signing material. Small size is not a reason to delete them.
- Treat the following as a hard denylist, including files with uncommon or missing extensions: source and headers (`.c`, `.cc`, `.cpp`, `.h`, `.hpp`, `.m`, `.mm`, `.rs`, `.go`, `.java`, `.kt`, `.swift`, `.dart`, `.py`, `.js`, `.ts`, `.sh`); project manifests and handwritten configuration; documents (`.md`, `.txt`, `.pdf`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`); and signing material (`.pem`, `.key`, `.cer`, `.crt`, `.p12`, `.pfx`, `.jks`, `.keystore`, `.mobileprovision`). This list is illustrative, not exhaustive.
- Delete only outputs that are proven reproducible from source and retained tool/config inputs: compiled binaries, build trees, dependency/compiler caches, copied verification packages, generated debug logs, traces, and temporary screenshots.
- Before deleting a generated artifact, identify the retained source or formal artifact that makes it reproducible. If reproducibility is uncertain, do not delete it; preserve it or move it to a clearly named external quarantine.
- Age makes a reproducible output eligible for cleanup; age never makes protected inputs eligible.
- Never let a broad cleanup command cross this denylist. Directory names such as `tmp`, `build`, `bin`, `backup`, or `cache`, and extensions such as `.bin`, do not prove that every contained file is generated. Inspect mixed-content directories and delete only the individually verified reproducible outputs.

## Fast workflow

1. Capture the requested outcome before scanning: age threshold, whether it means last modification or last access, minimum GiB to reclaim, target free-space percentage, and any project that must keep running. When the user says only “超过 N 天”, use modification time; use access time only when they explicitly say “未访问”.
2. Run one parallel read-only inventory instead of repeated full scans:
   - `df` for the system data volume and requested external volumes;
   - `du -sk` for `/private/tmp`, user caches, developer caches, and known project/build roots;
   - top-level candidate sizes and timestamps under `/private/tmp`;
   - active Codex tasks plus process command lines that reference candidate paths;
   - Git status for every candidate worktree.
   Always request KiB output (`du -k` or `du -sk`) and convert with `GiB = KiB / 1048576`; macOS `du` without `-k` reports 512-byte blocks and must not be compared directly.
3. Rank candidates by reclaimable size and classify them before deleting:
   - Regenerable caches: application caches, Gradle caches, package-manager caches, analysis caches, browser caches.
   - Temporary debugging artifacts: `/private/tmp` build clones, candidate APK/app bundles, logcat files, screenshots, traces, extracted verification packages, test staging directories.
   - Historical build backups: paths named `backup`, `history`, `archive`, `candidates`, `before-*`, versioned release staging areas, and copied `bin`/`BIN` outputs.
   - Protected content: source repositories, Git state, handwritten scripts/configuration, current project `bin`, latest signed deliverables, signing keys/certificates/keystores/profiles, documentation, test reports, user media, Codex sessions, VS Code `workspaceStorage`, and any path used by a running process.
4. Freeze the exact candidate list, then check safety efficiently:
   - Prefer process command-line matching for the exact paths, followed by targeted `lsof`; do not run an unbounded all-files `lsof` scan.
   - Detect Git worktrees with `git -C <path> rev-parse --is-inside-work-tree`; `.git` may be a file, so testing only for a `.git` directory is insufficient.
   - Preserve any worktree with tracked, untracked, or ignored-but-important changes unless the user explicitly names that entire source project for deletion and separately acknowledges loss of those changes.
5. Respect the age threshold per file in mixed-age directories. Delete a whole top-level temporary directory only when the directory is inactive and its role is known. Keep same-day files when requested. Never infer that a name containing `final`, `ready`, `signed`, `notarized`, `archive`, `APK`, `DMG`, `PKG`, or `ZIP` is disposable; confirm that a formal copy exists elsewhere or move it to an external quarantine when freeing the system disk is the goal.
6. Resolve exact targets before destructive work. For any individual target above 10 GiB, identify and report its path and approximate size; check whether the user already authorized that same target, scope, and risk level. Seek explicit confirmation only when such authorization is absent or the target presents a materially new risk. Batch only already-inspected paths; do not delete through unresolved broad wildcards. Tool-mandated approval still applies, and a denied approval must not be bypassed.
7. Execute largest safe targets first and continue until the user's minimum reclaimed-space or free-percentage target is reached. Stop early when the target is achieved; if safe candidates are insufficient, report the remaining gap and the exact protected candidates rather than deleting them.
8. Verify with `df`, remaining target sizes, existence checks, and current process state. Report physical space reclaimed from `df`; explain differences from logical `du` savings caused by APFS clones, sparse files, open deleted files, snapshots, or purgeable storage.

## High-yield cleanup rules

- `/private/tmp`: inspect top-level entries once, protect active paths and Git changes, then prune old build trees, extracted verification copies, debug screenshots/logs/traces, and duplicate packages according to the user's threshold. Do not wipe `/private/tmp` wholesale.
- Build outputs: old `target`, `build`, `DerivedData`, Gradle homes, compiler caches, and copied verification trees are normally regenerable when inactive and their source/configuration still exists. A project `bin` is different: remove only age-qualified compiled backup/intermediate binaries; retain source-like scripts, manifests, documentation, certificates, signing material, and the newest formal artifact unless the user explicitly authorizes deleting all old reproducible binaries.
- VS Code: `workspaceStorage` can be several GiB and may contain active project state. Read `workspace.json`, check whether Code has an open window, stop an idle background Code process before clearing authorized workspace caches, and warn that indexing and extension state will rebuild.
- Codex: `logs_*.sqlite` is diagnostic data, while `sessions`, `thread_history_*.sqlite`, and state databases preserve tasks. Never remove or replace a live log database while Codex processes hold it; first identify holders and coordinate a restart. Do not delete task history when the user asks only for logs.
- System-pressure mode: when free space is critically low, prioritize large inactive system-disk caches and temporary build trees. If a possibly valuable deliverable blocks the target, prefer a verified move to a spacious external volume over deletion, but disclose the destination and preserve recoverability.

## KEMI-specific safeguards

- Recent projects may be compiling on the internal disk or ORICO. Do not delete files modified within the user-selected protection window.
- Keep current KEMI APK/IPA/DMG/PKG outputs in project `bin` directories. Remove duplicate packages from temporary verification and backup directories only within the confirmed age/scope.
- `.tmp` directories can contain full source clones and hundreds of GiB. Their name alone is not sufficient authorization: measure them, identify their purpose, check active use, and request explicit deletion approval.
- Never infer permission to delete an obsolete-looking project. Project deletion requires a separate explicit request naming that project.
- Cache cleanup may require dependency downloads or re-indexing later. State this tradeoff before deleting large Gradle, package-manager, Dart, Xcode, or IDE caches.

## Reporting

Provide a compact completion summary containing:

- exact categories and major paths cleaned;
- protection rules applied;
- system and external-volume free space before and after;
- actual physical space reclaimed;
- remaining large candidates that need separate authorization.
