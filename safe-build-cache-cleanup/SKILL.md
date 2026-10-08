---
name: safe-build-cache-cleanup
description: Safely reclaim disk space by inventorying storage and deleting only stale, reproducible build outputs, compiler caches, temporary binaries, and downloadable caches older than a user-selected age. Use for disk-full and developer-cache cleanup; never use it to delete source code, documents, user data, Git history, release archives, VM disks, or ambiguous mixed-content folders.
---

# Safe build and cache cleanup

Reclaim meaningful space without treating every large directory as disposable. A successful cleanup leaves source, documentation, data, history, and deliverables intact and reports the measured space actually recovered.

## Hard preservation boundary

Never delete or modify:

- source files, project assets, documentation, reports, screenshots, evidence, databases, or user media;
- `.git`, Git objects, Codex sessions, Codex worktrees, archived task history, or repository metadata;
- release archives, signed packages, deployment bundles, backups, or artifacts whose reproducibility is not proven;
- virtual-machine disks, emulator state, device images, lab snapshots, or container volumes merely because they are large;
- a directory that mixes generated files with source, documentation, configuration, or collected evidence;
- system-protected caches by bypassing privacy controls or using elevated privileges to defeat an OS denial.

If classification is uncertain, preserve the item and report it as a large non-cache consumer.

## Authorized deletion scope

Only delete items that satisfy every condition:

1. The user authorized cleanup on the exact machine or remote device.
2. The item is a cache, compiler intermediate, temporary binary, generated application bundle, or test runtime that can be reproduced from retained inputs.
3. Its last modification is older than the requested cutoff.
4. No running process is executing from or actively using the target.
5. The target is resolved to a narrow absolute path and is not a symlink traversal, filesystem root, home directory, workspace root, or unresolved glob.
6. If the target is inside a Git worktree, every candidate path has been checked against the repository index and tracked files are excluded, even when they live under a directory named `build`.

Typical eligible locations include a project's top-level `build`, `target`, `.dart_tool`, `.cxx`, or disposable Gradle cache; Xcode `DerivedData`; package-download caches; and clearly named temporary acceptance/build runs. A folder named `build` inside SDK source, dependency source, a Python package, documentation, or another mixed tree is not eligible based on name alone.

## Workflow

### 1. Establish the boundary and baseline

- Resolve whether the user means the local machine or a specific remote device.
- Record the requested age threshold; do not silently reduce it.
- Capture free space before cleanup with the platform's disk-usage tool.
- Inventory top-level consumers before deleting anything. Separate project trees, caches, VM/lab data, Git storage, app data, and temporary storage.

### 2. Attribute large consumers

Use bounded, read-only size scans, starting broad and drilling into only the largest directories. Report large preserved consumers as well as deletion candidates so the user understands why disk usage remains high.

Classify each candidate as one of:

- **rebuildable cache/output** — eligible after age and process checks;
- **mixed or unknown** — preserve;
- **source/history/document/data** — prohibited;
- **release/backup/VM** — preserve unless the user separately and explicitly authorizes that category.

Do not infer disposability from size, extension, or a convenient folder name alone.

### 3. Apply the age cutoff correctly

Prefer file-level timestamps, such as `! -newermt '<N> days ago'`, rather than relying only on the parent directory timestamp.

Deleting a whole temporary directory is allowed only when:

- its name and location identify it as a disposable generated run;
- inspection shows only generated artifacts;
- no contained file is newer than the cutoff; and
- it contains no source, documents, reports, screenshots, databases, or collected evidence.

For mixed build directories, delete only old generated files and later remove empty subdirectories. Recent output must remain.

### 4. Check live use

Before mutation, inspect running process command lines for executables whose command begins inside each proposed target. Do not stop a process merely to make cleanup possible. Exclude any active target and report it.

Avoid loose regular expressions that match a target path only in process arguments. Match the executable path or verify open files precisely.

### 5. Protect repository-tracked files

Before any deletion inside a Git worktree:

- resolve the repository root and inspect tracked files under every proposed target;
- treat every tracked file as source, configuration, resource, or intentional repository content and preserve it;
- do not assume a `build` directory is disposable: packaging templates, icons, import libraries, test fixtures, and checked-in binaries may be tracked there;
- capture repository status before mutation and compare it after cleanup.

If a safe deletion mechanism cannot exclude tracked paths deterministically, skip that target.

### 6. Delete narrowly

- Use explicit absolute roots and an exact age predicate.
- Delete regular files and generated symlinks first, then only empty directories.
- For whole-directory deletion, revalidate content and recency immediately before deletion.
- Never use `/`, a home directory, a workspace root, `$HOME`, `~`, an unvalidated variable, or an unresolved wildcard as a destructive target.
- Do not delete an entire cache ecosystem when only stale files meet the request.
- Treat deletion as permanent unless a recoverable trash operation would still achieve the required disk recovery.

### 7. Verify and report

After cleanup:

- measure free space again and report the actual difference, not just the logical candidate sum;
- verify that targeted old files are gone and recent files remain;
- check repository status where relevant to demonstrate that tracked source and documents were not modified;
- list protected or ambiguous large consumers that were intentionally preserved;
- state that permanent deletions are not recoverable from Trash when applicable.

## Failure and stopping rules

- If the OS returns a privacy or protection error, skip that location; do not escalate around the protection.
- If a target changes during validation, contains unexpected files, or appears active, stop cleaning that target.
- If the safe candidates do not meet a requested free-space goal, report the remaining gap. Do not expand into source, documents, user data, Git history, releases, backups, or VM disks without a separate explicit decision from the user.
- Preserve unrelated existing changes in every repository.
