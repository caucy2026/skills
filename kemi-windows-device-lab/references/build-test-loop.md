# Windows local build, debugging, and acceptance loop

Read this reference before syncing source, building, installing, testing, or reporting a Windows result.

## 1. Establish a reproducible run identity

Record before mutation:

- controller repository path and Git commit;
- remote repository/worktree path and Git commit;
- submodule commits and applied product patch sequence;
- product/version name, integer version/build number, architecture, configuration;
- Windows build, CPU/RAM/GPU, display/DPI, free `D:` space, locale;
- compiler/SDK/CMake/Ninja/MSBuild/Inno/cache versions;
- active build and test processes;
- fixed corpus manifest and SHA-256 values.

Do not compile a dirty source tree without identifying which changes are intentional. Never discard remote edits merely to make it match the controller.

## 2. Preflight before expensive compilation

Prefer repository-provided verification scripts. At minimum validate:

- expected source and submodule commits;
- generated patch/application order;
- target architecture/configuration;
- dependency provenance and app-local packaging plan;
- file format/decoder ownership invariants;
- installer inputs and version resources;
- required portable tools under `D:`;
- TEMP/TMP/cache destinations;
- adequate free space;
- no competing build writing the same workdir.

Fail fast on missing SDKs, ATL headers/libs, WebView2 package, qpdf/OCR assets, signing inputs, or stale generated Makefiles. Do not wait for a multi-hour build to rediscover an input error.

## 3. Source synchronization

Use a commit-specific directory such as:

```text
D:\KEMI-Test\source\product-<short-commit>
```

Preferred order:

1. fetch the intended Git commit on Windows;
2. verify submodules and source hashes;
3. apply the repository's deterministic patch/preparation entrypoint;
4. compare generated/source parity with the controller;
5. sync only unavailable local artifacts by SFTP and rehash them on Windows.

Do not copy an opaque prebuilt directory over source and then describe it as a reproducible build.

## 4. Efficient Release build

- Use `Release`/`x64` unless explicitly diagnosing Debug behavior.
- Reuse the verified build directory and compiler cache only when source/toolchain identities match.
- Prefer the smallest valid incremental target (for example app-only) after a localized change.
- Refresh generated entry Makefiles/project files when repository scripts require it; stale copies can silently run old targets.
- Capture command, working directory, environment summary, start/end timestamps, exit code, and log path.
- Preserve the first compiler/linker failure with surrounding context. Do not repeatedly rerun an unchanged failing command.
- Never start another build until the previous PID/process group is verified complete.

Cache metrics are evidence, not correctness. After enabling ccache/sccache or changing MSBuild task granularity, compare cold and warm build time and rerun product tests from the same output.

## 5. Stage and package a self-contained product

From the final Release output:

- stage all product binaries/resources into a clean versioned directory;
- audit imported DLLs and runtime search paths;
- require business tools/runtimes to be bundled as designed;
- prevent test success through developer PATH, installed Python, Office, WPS, qpdf, OCR, or build-tool directories;
- validate main EXE file/product version, company, description, icon, architecture, and package version;
- build the installer using a verified compiler/toolchain from `D:`;
- verify Authenticode status where signing is required;
- record installer exact bytes and SHA-256.

“The EXE exists” is insufficient. Start every bundled helper from the staged/installed environment and audit missing non-system DLLs.

## 6. Isolated installation lifecycle

Install into a versioned D-drive test location whenever the installer supports it. Record install time and process tree.

Required lifecycle:

1. confirm the product is not running;
2. install without launching automatically unless testing that behavior;
3. verify installed file manifest, versions, hashes, dependencies, shortcuts, and associations;
4. launch from the installed path with a clean environment;
5. close normally and verify process release;
6. launch a second time to expose first-run-only assumptions;
7. open files by dialog, drag/drop, command line, and registered association as required;
8. return from a document to the home page without terminating the whole app when that is product behavior;
9. uninstall and verify only owned files/registrations are removed.

Do not rely on a developer machine's preinstalled runtimes to claim “works on every computer.” A clean or isolated acceptance environment is mandatory for release statements.

## 7. Compatibility matrix

Use the repository's fixed corpus and add hash-recorded fixtures only when coverage is missing. Cover at least:

- Word: DOC/DOCX, small/large, images, tables, fonts, malformed/protected;
- PowerPoint: PPT/PPTX, image-heavy, complex layout, empty/hidden slides, malformed/protected;
- Excel: XLS/XLSX, multiple sheets, wide/long tables, formulas, malformed/protected;
- PDF: normal, image-heavy, many-page, encrypted/damaged, and product PDF tools;
- OpenDocument and every advertised text/structured/image/legacy format;
- Chinese names, spaces, long paths, uppercase/misleading extensions;
- zero-byte, truncated, corrupt, unsupported, and resource-exhaustion inputs.

For each file record route, open/controlled rejection, first visible state, first clear state, scroll/interaction, close/return, process release, errors, screenshots, and logs. A protected or malformed file may pass through a controlled non-crashing rejection; white pages, permanent blur, silent missing pages, hangs, or crashes fail.

## 8. Interactive UI tests

Run in the actual logged-in desktop session through the allowlisted desktop agent. Validate:

- window appears on the intended display with correct title/icon/version;
- minimize, maximize, restore, move, resize, close, and return-home behavior;
- file picker cancellation does not reopen in a loop;
- drag/drop opens supported files instead of downloading them;
- file associations and “Open with” registration;
- loading/progress overlays, menus, dialogs, fonts, localization, DPI, and keyboard focus;
- PDF/OCR/toolbox controls and any update UI;
- nonblank screenshots and no hidden modal blocking interaction.

Headless conversion output and UI Automation element presence support the test but do not replace visual inspection.

## 9. Performance measurement

Before measuring, assert the host is idle and no build, antivirus scan, updater, or competing test is consuming material CPU/storage. Mark contaminated runs ineligible; do not hide them.

Measure cold and warm separately, with at least three valid repetitions where practical:

- click/open request to loading feedback;
- request to first visible content;
- request to first clear content;
- page/slide/sheet readiness progression;
- scroll FPS, jank, P95/P99 frame time and long frames;
- CPU, GPU, working set/peak memory, disk I/O;
- exit time and residual process/resource release.

Compare old and new on the same machine, corpus, display/DPI, idle policy, and metric definitions. Keep screenshots to prove layout/rendering stayed correct. A faster blurry or incomplete result is a regression.

## 10. Debugging loop

On failure:

1. preserve the exact input, command/action, timestamps, logs, screenshot, process state, and dump/trace;
2. classify the failing layer: routing, import/decoder, layout, rendering/GPU, UI thread, packaging/dependency, installer, updater, session bridge, or environment;
3. reproduce with the smallest fixture that retains the mechanism, while keeping the original document for final regression;
4. fix the shared mechanism rather than special-casing one filename;
5. rebuild the minimal affected target;
6. rerun the same failure, same-format family, core Word/PPT/Excel/PDF smoke tests, and the full matrix required by risk;
7. compare against the last accepted build and revert experiments that worsen correctness or performance.

Never claim a bug fixed solely because logs changed or one synthetic test passed.

## 11. Installer self-update

Test from a genuinely older installed version to the new installer:

- update discovery and version comparison;
- visible prompt/progress/cancel/error states;
- exact download size and SHA-256 verification;
- main process exit and detached installer survival;
- replacement of locked files without recursively killing the installer child;
- new version on disk and on relaunch;
- failed-update rollback/preservation of the old working version;
- current version negative check to prevent an update loop.

Use the repository's process-tree negative test where provided, then complete the visible UI path in the interactive session.

## 12. KEMI OFFICE repository mapping

When present, prefer these maintained entrypoints instead of improvising equivalents:

```text
docs/engineering/WINDOWS_LAN_DEVICE_TEST_NODE_SETUP.md
docs/engineering/WINDOWS_LOCAL_RELEASE_BUILD.md
docs/engineering/WINDOWS_X64_SINGLE_SCREEN_BUILD.md
scripts/verify-windows-source-parity.sh
scripts/windows/prepare-koffice-local-release.ps1
scripts/windows/prepare-koffice-packaging-tools.ps1
scripts/windows/compile-koffice-installer.ps1
scripts/windows/remote/Measure-KemiOfficeFirstPage.ps1
scripts/windows/remote/Invoke-KemiSelfUpdateProcessTreeSmoke.ps1
scripts/windows/remote/Install-KemiDesktopAgent.ps1
scripts/windows/remote/Start-KemiDesktopAgent.ps1
scripts/windows/remote/Submit-KemiDesktopAgentRequest.ps1
```

Discover current names with `rg --files`; scripts can be renamed as the project evolves. Read each selected script and its project documentation before execution.

For KEMI OFFICE, all source, toolchains, caches, TEMP/TMP, installers, applications, corpora, logs, screenshots, traces, and dumps remain under `D:\KEMI-Test`. The SSH account and interactive desktop account may differ; if the desktop agent heartbeat is missing or stale, report `interactive_required` rather than fabricating UI results.

## 13. Acceptance report

Record:

```markdown
# Windows Release <version> acceptance

- Controller/remote host identity and SSH fingerprint:
- Windows build, hardware, display/DPI, locale:
- D-drive free space and workspace:
- Git/submodule/patch identity:
- Toolchain and cache versions:
- Build command/configuration/start/end/elapsed/exit/cache stats:
- Product/installer paths, versions, bytes, SHA-256, signatures:
- App-local dependency audit:
- Isolated install/launch/close/relaunch/uninstall:
- Compatibility matrix pass/fail/controlled rejection:
- Word/PPT/Excel/PDF results:
- Added-format results:
- UI/session-agent evidence and screenshots:
- Cold/warm performance and old/new comparison:
- Updater positive/negative/process-tree/rollback results:
- Crash/hang/dump/event-log findings:
- Remaining blockers and risks:
- Final status: candidate only / accepted Release / blocked
```

Only an accepted Release may be copied to the product `bin` directory or passed to a publishing workflow.
