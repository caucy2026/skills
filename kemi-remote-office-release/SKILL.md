---
name: kemi-remote-office-release
description: Build, sign, notarize, validate, and release all four KEMI Remote Office clients (Android PAD, Universal macOS, Windows x64, Linux AppImage) to Newlink Common and the KEMI application market. Use for KEMI 远程办公 four-platform releases, platform hotfixes, signing/notarization, release handoff and upgrade verification; not KEMI Send, VibeKits, Apple App Store or Microsoft Store releases.
---

# KEMI 远程办公四端发布

先完整读取适用的 `AGENTS.md`、同目录 `LOCAL-ENVIRONMENT-RULES.md`、仓库 `client/AGENTS.md`，再读 [四端完整操作手册](references/four-platform-release.md)。手册覆盖源码冻结、四端编译、签名、公证、Common 六资源、商场及更新验收；按当前平台读取其中链接的详细参考，不从头探索已经验证的路线。

完整发布顺序：冻结可追溯源码与版本 → 四端完整 Release → PAD 平台证书、Mac Developer ID＋公证、Windows 内层与外层 Authenticode → 最终包真机与旧版覆盖更新验收 → 同一最终字节发布 Common 和商场 → 回下载、更新检查、应用内商场更新与授权延续验收。

必须保持：

- 主分支以当前 `client/AGENTS.md` 的 `main` 为准；历史参考中的 `master`、旧 SDK、旧版本和设备 ID 不能照抄。
- 正式候选来自冻结源码；`KEMI_ALLOW_DIRTY=1` 只适用于已标记的测试包。旧包改版本号、旧 Rust 核心搭配新 AOT、历史签名报告套用新哈希都不能发布。
- PAD 固定 `com.newlinksz.kemi.remote` 和 Huanglong 平台证书；Mac 固定 Bundle ID、Team、顶层 `KEMI远程办公.app`。更新保留配置、设备身份、登录、录屏/辅助功能等既有授权，不卸载或清数据解决问题。
- Mac 正式入口 `res/build-kemi-macos-universal.sh`。单架构候选不冒充 Universal；公证 Accepted 后装订 App，再重打 ZIP 并核验最终 ZIP。
- Windows 用完整同源 Release，先签全部需签内层 PE，再打包，再签外层 EXE。硬件令牌 PIN 由签名人员输入；Session 0 不能替代交互桌面。
- Linux 使用固定 CI 的真实 AppImage，实机启动后独立判定；现有路线没有 Windows Authenticode 或 Apple 公证，哈希不等于代码签名。
- Common 四端二进制先传、完整 SHA256SUMS 次之、manifest 最后；商场按 `(package_name, os_type)` 更新现有记录，保留完整元数据及精确字节数、SHA-256。

配套执行技能：`vibekits-remote-simulator`、`kemi-windows-two-node-release`、`kemi-windows-remote-signing`、`newlink-common-release`、`kemi-market-publish`；产品验收按 `app-release-stability-gate` 及当前已约定的项目用例。复用已有证据，优先白盒检查，只做必要测试；没有证据的平台标记未完成，不把构建或上传成功写成发布完成。

更新本技能后运行 `python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ~/.codex/skills/kemi-remote-office-release`，并核对全部相对引用存在。文档校验不会重新编译、签名或发布四端。
