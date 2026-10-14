---
name: vibekits-remote-simulator
description: "Use when the user gives a 6–16 digit VibeKits device ID and asks to debug that remote computer/device, especially Mac-to-Android-PAD remote ADB, or inspect apps, logs, system, transfers and software through 远程仿真. Also use for uploading and deploying applications to saved SSH/SFTP servers without VibeKits. Device simulation uses VibeKits P2P/relay; server deployment uses saved SSH/SFTP profiles, never a remote-desktop UI."
---

# VibeKits remote simulator

A device ID and an authorized remote-simulation endpoint are enough to start. The user need not name this skill or say “远程仿真”: “帮我调试远程设备 ID …” and equivalent requests should trigger it. Do not ask for its IP, SSH user, password, private key, relay address, or RustDesk password. The remote device must have enabled simulation and granted the required first-time consent; never bypass that or OS privacy controls.

## Inside VibeKits Harness

1. Use the registered VibeKits MCP tools directly. Call `vibekits.simulator.connect` with `{"routingId":"<ID>"}`. Do not launch RustDesk/KEMI remote desktop, a browser tunnel, an external SSH client, or a shell helper merely to connect.
2. Validate the structured result, not just tool transport success. Require `connected: true`, the requested routing ID, a verified device identity and `transport: p2p_or_relay`. Check `vibekits.simulator.connection_status` when needed. Treat an SSH host-key change or consent failure as a stop, not a reason to try another route.
3. When tool availability or arguments are unclear, call `vibekits.simulator.catalog` and follow the returned schemas. Use `vibekits.simulator.call` for the remote `vibekits.device.*` tools. Prefer purpose-built process, application, log, crash-report and UI-inspection tools to `vibekits.simulator.ssh_exec`.
4. For a read-only inventory, obtain installed apps with `vibekits.device.applications` using a bounded limit. Obtain OS/host details from connection metadata or a narrow read-only query when no dedicated tool exists. For a UI defect, compare the installed build, process state, bounded logs, target window/AX state and a diagnostic frame where permission allows; do not infer a cause merely from a successful connection.
5. Only perform the installation, removal, app control, UI action, transfer or settings change that the current request actually authorizes. An install result alone is not verification: check version, launch state and the reported behavior on the target. Keep the affected app's working functionality and rollback path in scope.
6. Call `vibekits.simulator.disconnect` on completion or a blocking error. Report what was actually observed, which route/identity was verified, what changed, and which claims remain unverified.

## macOS 远程文件访问前置设置

仿真客户端通过 macOS 的 SSH/SFTP 访问目标 Mac 文件时，如果身份验证已成功，但授权范围内的受保护目录仍出现 `Operation not permitted` 或文件访问拒绝，检查目标 Mac 的官方设置入口：**系统设置 → 通用 → 共享 → 远程登录旁的 ⓘ → 允许远程用户对磁盘进行完全访问**（部分版本表述为“允许远程用户完全访问磁盘”）。远程登录须开启，且当前连接账户应在允许访问的用户范围内；保持既有用户限制，不为排障改成“所有用户”。这是条件性前置设置，不是访问任意普通文件都必须开启。

先区分连接失败、SSH 认证失败、文件属主/权限不足和 macOS 隐私限制；该开关不能修复认证失败，也不能替代 VibeKits 应用本身的辅助功能、屏幕录制或其他隐私授权。根据实际 macOS 版本核对界面，旧版本可能位于“系统偏好设置 → 共享”。在已授权范围内可通过同机远程桌面检查设置；系统要求管理员密码时由设备所有者或获授权管理员完成，执行者不读取、记录或代填密码。不得以重置隐私数据库、关闭 SIP、清空用户数据或扩大访问对象来替代官方设置。

设置后沿原仿真 ID 和已验证身份的 SSH/SFTP 通道，对原先失败的、已授权路径做最小只读列目录或文件读取验证，并核对命令退出码和实际结果。只记录系统版本、设置状态、验证路径及结果，不保存文件敏感内容或认证截图；开关开启或连接成功本身不等于文件访问已通过。

官方依据：[Apple《允许远程电脑访问你的 Mac》](https://support.apple.com/guide/mac-help/allow-a-remote-computer-to-access-your-mac-mchlp1066/mac)（2026-10-12 核对，说明 Remote Login 使用 SSH/SFTP，并提供远程用户完全磁盘访问选项）。
新增安全敏感访问时遵守平台当次确认要求；已有有效、同范围授权不重复索取。


## Windows script execution

After the Windows device ID is connected and SSH is ready, use `vibekits.simulator.ssh_exec` for a short PowerShell script. Encode the script as UTF-16LE Base64 and pass one exact command: `powershell.exe -NoLogo -NoProfile -NonInteractive -EncodedCommand <base64>`. This avoids dependence on whether Windows OpenSSH starts `cmd.exe` or PowerShell and preserves Unicode and quoting. Check `ok`, `exitCode`, `stdout` and `stderr`; do not treat transport success as script success. For a longer `.ps1`, upload the exact file with `vibekits.simulator.upload_file`, execute that returned remote path with `powershell.exe -NoProfile -NonInteractive -File`, and verify the intended output. Do not change execution policy, bypass security prompts or open a desktop session.

Keep the whole workflow silent in the background and independent of Harness chat rendering. Never expose bridge tokens, credentials, private keys or authorization headers. Do not claim to have clicked a button when only a screenshot or source review was possible.

For an external macOS controller that lacks registered Harness MCP tools, read [references/tool-contract.md](references/tool-contract.md) and use the bundled `scripts/invoke.rb` against the local loopback VibeKits bridge. This fallback is not the Harness path and does not require the remote-desktop UI. For an Android PAD controlled from that Mac, follow the tested end-to-end [Mac → PAD remote ADB guide](references/mac-pad-remote-adb.md), including the dynamic local ADB serial, dual-screen targeting, reconnect after a host APK upgrade, and disconnect.

For a brand-new Mac and Android PAD, begin with the [first-install and remote ADB checklist](references/new-mac-pad-first-run.md). It identifies the public KEMI Market download pages, the cloud skill directory, the PAD release gate, and the exact handoff to the remote ADB guide. Do not treat an older market APK as having features that were added only in later device-tested candidates.

For a KEMI Market app upgrade on a remote device, follow [the simulator-based market update workflow](references/market-app-update.md). Check the installed integer build against the current same-platform market build before any download; if already current, report that no installation occurred.

When a device ID returns `Remote desktop is offline`, follow [the channel recovery guide](references/channel-recovery.md) before calling the physical computer offline. Record the failure and the verified recovery in that guide so subsequent colleagues can reproduce the diagnosis.

When online IDs cannot be called after a network or local App change, read [the network-switch incident recovery](references/network-switch-incident-20260930.md). Verify the current controller bridge before judging the remote device offline; a cluster heartbeat and a simulator connection are separate observations.

For uploading or deploying another application, including an SSH server without VibeKits, read [server file deployment](references/server-file-deployment.md). Use saved SSH/SFTP profile tools for that server; do not require a simulator ID or install VibeKits.

For SWDOL PAD acceptance on the user-assigned device 2315316040, read [the tested handoff](references/swdol-pad-acceptance-2315316040.md). It covers dynamic ADB identity, normal HOME return, input cancellation, animated transitions, frame-rate-independent timing and performance measurement boundaries; its historical samples do not authorize access or prove full acceptance.
