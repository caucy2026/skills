# Windows startup crash through an existing remote desktop: 2026-10-03 case

## Scope and current result

Device 388630819 was reachable through KEMI Remote Office while VibeKits failed at startup. This is a remote-desktop ID, not a proven VibeKits simulator ID. Use the existing authorized desktop connection when the crashing app cannot provide its own simulation interface. No host-security changes are needed for that route.

Current status: the controlled app-local CRT comparison recovered startup and interactive workspace selection. Restart persistence, same-location overwrite upgrade, credentials, model/MCP, simulation and final-package acceptance remain unverified. This is a successful diagnostic comparison, not a fully accepted release recipe.

## Observed sequence

1. Verify the window is `388630819@laptop-rqnvq34m`; confirm Windows 10 build 19045.6466 and D-drive availability. Inventory the installed executable and Application Error / WER records. The original dev232 and signed dev445 both failed with access violation in MSVCP140 14.34.31938.0, RVA 0x13028.
2. Transfer the exact signed candidate through the existing remote desktop file-transfer interface. Check transfer completion, then independently verify target size, SHA256 and Authenticode; transfer success alone is not installation or acceptance.
3. Before replacement, create a complete old-install manifest and backup on D:. The observed backup contained 30349 files; copy errors and mismatches were zero. Preserve configuration and authorization identifiers.
4. Perform the authorized guarded installation, launch once and correlate the new process and timestamps with new crash events. Dev445 exited after approximately three seconds. Keep the failed complete candidate and restore the old complete directory. The restored old build also crashes; report rollback achieved but health unproven.
5. Use official Microsoft Sysinternals ProcDump, verify its signature and SHA256. Obtain action-time consent for its EULA and a single local dump. Capture one unhandled exception only; do not repeat the capture without the required authorization. The actual dump was 344506682 bytes and remained on target D:. Do not upload dumps or print arbitrary memory, environment strings or user data.
6. The standard cdb paths were absent. A bounds-checked PowerShell MINIDUMP parser ran locally on the target instead: it reported a null-address READ and RIP in MSVCP140 + 0x13028. It did not unwind the call stack; scanning 128 stack words yielded no module-address candidates. These facts do not prove a particular source function.
7. A bounds-checked PE export parser reported nearby `_Thrd_yield` (0x12F70) and `_Mtx_clear_owner` (0x13170). Nearby exports do not prove the faulting function's extent.
8. Query the live builder through its trusted simulator route. The current dev445 source build reports MSVC 14.44.35207, compiler 19.44.35228.0. Its unsigned executable differs from the signed failing executable, so current CMake metadata is not a complete historical build receipt for the exact signed binary.
9. Inspect the complete official x64 CRT directory, not one selected DLL. Actual builder path: `D:\VSBuildTools\VC\Redist\MSVC\14.44.35112\x64\Microsoft.VC143.CRT`. All 10 DLLs were version 14.44.35211.0 with Valid Microsoft signatures. A diagnostic ZIP was prepared and downloaded with matching SHA256 `993C7EB4DAA5C10C9DA9683861EC31297CB47588F2255994AAC3C0D99D6A6222`, 721587 bytes. The archive was transferred to the verified active 388 file-transfer tab. Full-clone preparation subsequently completed without changing System32 or the signed main executable.

## Reliable remote input and transfer details

- Before every file action, verify the target title. The file-transfer action sometimes focused an existing 415501605 Mac transfer window instead of 388. Never transfer to that window by assumption; select or establish the exact 388 transfer destination first.
- Direct remote typing corrupted special PowerShell characters. The tested route was a local TextEdit file containing one exact command, Select All / Copy, then the remote desktop toolbar's Send Clipboard Keys action. Wait until the complete command is visible before pressing Return once. Do not repeat Return while asynchronous typing is unfinished.
- Long scripts used gzip/base64 payloads, decoded-script SHA256 verification and PowerShell Parser validation before execution. Short simulator SSH commands used UTF-16LE EncodedCommand. Neither route changed execution policy.
- Treat display lag or an observation timeout as incomplete observation, not command failure. Reinspect the existing process or terminal marker before retrying.

## Remaining controlled repair comparison

Inspect CRT files already present in the failed package. Clone the complete package into a new D-drive diagnostic directory and add the complete same-version official x64 CRT group. Keep the signed executable bytes unchanged. Launch once, prove the actual loaded CRT paths and versions, and inspect fresh crash events. Do not modify System32 or blindly add compiler macros.

If startup recovers, verify workspace selection, Harness model/MCP behavior, original authorization continuity, close/relaunch and the required compatibility/performance gates. Only then integrate deterministic CRT packaging and package validation, sign the final complete artifact and repeat the same failure on the final signed installed bytes. Record the exact before/after hashes, loaded modules and outcomes. If the comparison still crashes, retain the result and continue diagnosis; do not assert runtime mismatch as the root cause.

## Packaging prevention and closeout

The reviewed CMake packaging did not explicitly deploy the MSVC CRT; existing signature checks did not establish a minimum runtime version. This is a packaging gap to investigate, not proof that every actual package omits CRT. Verify the actual artifact and make runtime provenance, architecture, completeness and minimum-version checks executable before promotion.

After debugging, preserve the required sanitized evidence and rollback package, then clean only this task's confirmed unused temporary files, transfer duplicates and diagnostic processes. Protect installed software, user data, credentials, shared services and coworkers' sessions. Record what remains and why; do not delete the only failure evidence to make the disk look clean.

## Primary references

- https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist
- https://learn.microsoft.com/en-us/cpp/windows/redistributing-visual-cpp-files
- https://github.com/microsoft/STL/issues/4730 (a related runtime compatibility mechanism; not proof of this crash)

Detailed project evidence: `docs/acceptance/WINDOWS_388630819_REMOTE_DEBUG_2026-10-03.md` and `tool/windows/dev445-388-20261003/` in the authoritative VibeKits source repository. Preserve the case's unproven boundaries when reusing it.

## Mandatory prevention checks for the next desktop upgrade

1. Record and pin the compiler, SDK, architecture, runtime and native-plugin inputs of the actual final artifact. Do not silently upgrade the toolchain during an unrelated product fix. Changes require a targeted compatibility comparison.
2. Audit actual packaged PE dependencies. Verify the complete applicable CRT group from one official redistributable source, its architecture, minimum version, hashes and signatures, or verify the installer's official redistributable prerequisite path. Do not rely on the development machine's installed CRT or PATH. Other dependencies such as WebView2 and native helpers must follow their existing project deployment contracts. Do not redistribute Windows system DLLs by guessing.
3. Test the final signed installed bytes on a machine without the compiler/developer PATH and with an older runtime baseline. Record actual loaded module paths and versions. Main EXE signing and successful compilation are insufficient.
4. Run both fresh-install and previously-authorized old-version overwrite-upgrade flows. Verify startup, workspace selection, Harness model/MCP and remote simulation, close/relaunch, CPU/resource release, device identity and credentials without resetting user data or authorization.
5. Include the project's six-device fleet, extra 9509249133 regression target and crash-prone Windows 388 in the applicable release matrix. An unreachable required device is unverified, never PASS. Preserve existing project Mac Intel/minimum-system and Apple Silicon gates.
6. Maintain a fault-specific regression for the 388 startup crash, with artifact hashes, fresh event-log time bounds and process/module evidence. A changed error message or a brief surviving process is not a passed application test.
7. Packaging/compatibility gates must fail closed on missing evidence or dependencies. Reuse still-valid evidence only for unchanged artifacts and the scope it proves. Publish only after the required final-package gates pass; retain the complete previous package and deployment rollback. Diagnose controlled comparison failures instead of repeatedly reinstalling unchanged bytes.
8. Finish with the required debugging closeout: preserve evidence first, clean task-owned disposable material, confirm working services remain available, and report retained artifacts and reasons.

These checks reduce recurrence; they do not claim compatibility with every unspecified operating system or hardware configuration. Keep an explicit supported OS/architecture baseline and test the actual supported fleet.

## Actual comparison outcome and prevention boundary

The complete diagnostic clone at `D:\vibekits-debug-388-20261003\crt-comparison-14.44-1358\app` retained the signed main SHA256 `768013B7F1772395CED2B719836D8F03D3F976F185627DA811E17712705D67EC`. Preparation returned CRT_COMPARISON_PREPARED. The single observer returned CRT_OBSERVATION_DONE; its visible sample showed app-local MSVCP140/VCRUNTIME140/VCRUNTIME140_1 14.44.35211.0 and no crash events in that bounded interval. The app remained visible and the native directory picker selected the task-owned D-drive workspace, which then appeared in Harness. Retrieve full target JSON before relying on unshown fields. Cumulative CPU time does not establish idle CPU acceptance.

A firewall prompt for the diagnostic path was cancelled; no new permission was granted. API-key onboarding was deferred without accessing or entering credentials. The original installation was unchanged by this comparison. These facts support runtime compatibility as an important cause but do not identify the source function or prove complete repair. The earlier pending-comparison paragraphs are historical instructions; the remaining required steps are restart/upgrade/function acceptance and deterministic final-package CRT checks.

For recurrence prevention, attach compiler/runtime provenance and actual loaded-module evidence to the final signed installed package's existing acceptance report. Reject missing dependency evidence rather than assuming the developer machine represents the customer machine. A temporary diagnostic clone must never be substituted for final-package acceptance. Preserve authorization and identity across overwrite upgrades, run the supported fleet and specific 388 regression, and complete task-owned cleanup after evidence and rollback are secured.


## Verified follow-up and executable gate

Full prepare-result.json and observe-once.json were retrieved and inspected in the project evidence directory WINDOWS388_CRT_COMPARISON_20261003. They confirm 31910 cloned files verified, unchanged signed main, ten added CRT files, unchanged System32, twelve five-second observations and no crash events in that interval. Title-bar close and subsequent restore retained the workspace with the same PID. This was hide-to-tray continuity, not a cold restart. Original-location upgrade, model/MCP, simulation and idle-resource acceptance remain unverified.

The shared tool/verify_windows_crt.ps1 now gates Release through tool/verify_windows_bundle.ps1. It checks ten applicable CRT files, a minimum version, consistent versions, Microsoft signatures and AMD64 PE headers. Actual dev446 candidate passed all ten; missing-file and deliberately higher minimum-version tests failed as expected. The full bundle verifier and final installed-package acceptance were not established by these helper runs. Reuse the script and case evidence; do not substitute helper PASS or a diagnostic clone for final signed-package regression.


## Prevent false acceptance when reusing this case

The retrieved 300-second CPU JSON contains 60 samples over 300.8309608 seconds. Main-process median is 7.7956% one-core equivalent, or 0.9744% after division by eight logical cores. Status is MEASURED_NOT_ACCEPTED: strict host idle and the complete helper process family were not established. Preserve both definitions; never use normalized CPU to evade the project's existing process-sum threshold.

The lifecycle inventory identified the diagnostic main PID 7620 and its relay, Node and WebView descendants with creation times. Revalidate current ownership before acting. Title-bar X hides VibeKits; use its verified tray “退出并停止后台服务” action for actual exit, verify owned descendants release, then establish a new main PID and preserved workspace/credentials. Do not stop the remote-office connection or unrelated helpers.

Before promotion, bind the full Release bundle verifier, signatures, final installer hash and actual installed bytes to one candidate. Run the previously failing device path on those exact bytes; a repaired diagnostic clone, helper checker PASS or no new event-log entry is insufficient. Record missing checks as BLOCK, retain first failures, and complete authorized evidence backup and task-owned cleanup only after rollback and evidence needs are secured. The project incident document is the maintained release checklist; do not recreate the procedure from chat each upgrade.


## Native payload manifest prevention and current lifecycle evidence

The dev446 full bundle check rejected the relay manifest. The earlier Stage-Native441.ps1 replaced only the EXE, leaving the dev368 provenance JSON behind; the mismatch already existed before signing. Treat a native payload and its source manifest as one staged, validated and recoverable unit. Verify the pre-sign hash against actual build evidence before signing, preserve its relationship to the final signed hash, and recheck the final package before deployment. Never refresh a hash to conceal stale source provenance. The project's verify_windows_relay_signed_manifest.ps1 rejected the unrelated manifest; its mutation branch has not been accepted and must not be promoted as a proven repair.

388 subsequently used the verified tray exit: the exact main count became zero and all inventoried owned PIDs disappeared. A new main PID 12920 then started from the diagnostic path and the workspace remained present. This proves diagnostic exit/cold-start continuity, not credential continuity or final-package acceptance. Final model/MCP, simulation, overwrite-upgrade and complete-family idle-resource gates remain outstanding. Maintain current results in the project incident/device reports and reuse unchanged valid evidence instead of repeating the investigation.
