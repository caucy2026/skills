# 本项目接续快照：2026-10-11

这是定位资料，易变状态须现场复核，不是可以直接执行的旧事务参数。技能可以复制给同事；本地原始证据和专项技能访问权限仍须具备。

## 本机资源入口

- Harness：`/Volumes/ORICO/newlink-new/vibekits`
- 服务：`/Volumes/ORICO/newlink-new/hbbv`
- 产物根：`/Volumes/ORICO/kemi-build-cache/app-release-gate/vibekits`
- 全局技能：`/Users/newlink/.codex/skills`
- 环境规则：`/Users/newlink/.codex/LOCAL-ENVIRONMENT-RULES.md`，以及任务路径适用 AGENTS。
- 主交接：hbbv `docs/PROJECT_HANDOFF_VIBEKITS_CLUSTER_UPGRADE_ACCEPTANCE_20261011.md`
- 执行归属及完整目标：hbbv `docs/acceptance/CURRENT_CHAT_TAKEOVER_20261011.md`、`CONTINUATION_RECONCILIATION_20261011.md`。当前聊天 `01a12aa0-1fd3-7862-8fbd-686ddc8732f2` 承接；用户要求原接续聊天停止，但本环境没有跨聊天停止工具，不能声称已技术停止。

## 原设备与服务定位

Mac155 `1554650784`，Mac445 `4456560334`，Mac529 `5298938227`，Mac132 `1321656264`；Windows58 `4240650696`（历史旧号4567540178），Windows619 `6192992780`；补充 Windows617 `6175875975`。先按登记身份核验，不因显示名相近换对象。

服务器沿已保存 SSH profile `remote_1791254767548854`，hbbv21122；原 serverId `da3553a32048bfe691d99ad1a27a914b`。不保存密码或导出私钥。原 general room `f450c684b868292f67c534b793e26314`，task `5deb64cad5f92da2a80aaaab03b1eaf4`；查原状态再续，不重发未知事务。

## 当前已验证与待续

- 重连有界退避源代码/24 项测试及负向故障注入通过，见 Harness `docs/acceptance/CLUSTER_RECONNECT_BACKOFF_20261011.md`；尚不能因此宣称规模真机全部通过。
- Mac619 已完整 frozen 源码、双架构原生、857 测试通过（1 Windows-only skip）、Developer ID、notary Accepted、staple 和独立解压验证。见 `docs/acceptance/UNIFIED619_SOURCE_NATIVE_PREFLIGHT_20261011.md`。
- Mac 最终 ZIP 在 `macos/cluster-unified-619-20261011-v1/Vibekits-619-final.zip`，423710323 字节，SHA256 `168d504c6b06c8ea019aa0bb91ee405edffac2a47acbbc5a3b56ccbafe887f1c`。未覆盖安装/商城发布。本机 App618 是共享桥，其他任务正在用，不能为了619随意重启。
- Windows58 上新源码619真实 Release 已成功，核心版本2619；原合格615native复用须保持限定证据。619尚未签名/安装/发布。见 `docs/acceptance/WINDOWS619_RELEASE_BUILD_20261011.md`。
- Windows11文件123用例第一轮122通过、1因测试缺 Flutter binding 失败；仅补 ensureInitialized 后第二轮独立测试任务已启动，第二轮已终态：122通过、1因普通 flutter test 无原生 windows_credential_read 插件失败；不能当产品凭据失败，也不能算真机凭据通过。须使用真实原生宿主补验。作业名 `VibeKits-Cluster619-Test-20261011-binding-r2`；D盘 `D:\KEMI-Test\work\cluster619-20261011-v1` 中 `regression-terminal619-binding-r2.json` 与 driver/resources；输出在同名 results 目录。不得重启未知结果。
- 服务 customer modal/SQLite关闭恢复后后台297Mac+297Linux+5SSE通过，见 hbbv `docs/acceptance/CUSTOMER_DIALOG_CLOSE_RECOVERY_PRODUCTION_20261011.json`。真实生产浏览器UI仍缺；此前 Chrome 自动审核拒绝不可换自动化规避。
- 300合成会话、60min真实loopback HTTP长跑已通过，见 hbbv `docs/acceptance/scale.md`。100+真设备、24/72hr、WAN/Harness范围仍缺。
- 六机覆盖升级、原任务业务闭环、多客户真实UI、角色/折叠连续性、实时委托原生门禁仍按G01–G10补证据，不能把当前包装阶段当全部完成。

## 下一阶段可执行入口

1. 保留 Windows binding-r2 的122通过/1 MissingPluginException回执；沿真实原生宿主补凭据用例，该缺项已用独立Session1 native宿主补验PASS；保留单元失败与补验范围，不能改写为123单元通过。
2. 在 Windows D 盘复核空间、原native proof及当前619 core，619 fresh candidate 已暂存到 D:\KEMI-Test\results\v619-sign\candidate：244 PE，32待签/212厂商签名，CRT和源证明已通过；交互native凭据探针已PASS，8个测试键已真实清理、原App未变；下一步独立签名预检和固定GUI内外签名。不得重签旧615或用其版本名冒充619。
3. 保留共享桥，不安装本机Mac619直至能证明不干扰其他任务；独立补其他设备/业务目标的现有可执行缺项。

Windows辅助入口：Harness `tool/windows/dev561-original617-20261007/transfer_qualified561_existing_vibe_sftp.py` 只复用 carrier/scp 函数和当前核验参数，不运行硬编码旧 main。构建/观测脚本在产物根 `windows/cluster-unified-619-20261011-v1`，先读意图/回执再用。

备份成熟 helper：hbbv `quality/backup_cluster_event_lock_heartbeat_docs_20261006.py`；只提取通用函数，不运行历史顶层。授权目标分别 vibekits.git、priv.git 的 hbbv/、skills.git，核精确 remote 与 main，不推 RustDesk upstream。最新备份提交和范围见各验收文档；本快照不会保证后来远端仍同一HEAD。

## 进入对应阶段才读的项目记录

Harness `docs/HARNESS_UPGRADE_STANDARD.md`、`docs/RELEASE_GATES_ALL_CLIENTS.md`、`docs/VIBEKITS_FLEET_COMPATIBILITY.md`、`docs/acceptance/MAC_HARNESS_RECURRING_REGRESSIONS.md`、`docs/acceptance/BUILD_RELEASE_INCIDENTS_2026-10-03.md`。

hbbv `docs/ROOM_DELEGATION_NATIVE_INTEGRATION_HANDOFF_20261011.md`、`docs/MULTI_CUSTOMER_REALTIME_AND_RECONNECT_20261011.md`，以及项目 CUSTOMER_ID_DEVICE_ENROLLMENT、CLUSTER_MODEL_READINESS_EXPLICIT_VERIFY、ROOM_DELEGATED_MCP_GATE、ROOM_DELEGATION_ONE_USE_CLAIM、ROOM_MESSAGES_AND_COLLAPSIBLE_ROOMS 记录。按当前动作搜索，不全量重读所有历史。

当前追加（2026-10-11）：同次619 Runner/独立AOT在Session0返回1312且0键写入；交互测试投影仅main互斥名/窗口标题变化，独立build86.154s exit0，固定GUI入口已由真实MCP运行：原用户/Session1、native PASS、8键删除并读回缺失、exit0、原App未变。详见项目Windows619台账；不覆盖首轮失败。

22:43追加：Windows619已另存READY_FOR_SIGNATURE_ONLY收据（SHA778324E6…38B9245）；活动Session1签名Inspect exit0、原B828…7E82证书有效至2027-09-12、x64 SignTool可用。未签名/安装/发布。第一619固定GUI签名脚本在同名控制端产物目录准备，启动前对账intent/原进程及文件哈希，PIN只在实际窗口由人输入。

在途签名追加：619第一签名runId dev619-signed-runtime-20261011-v1，D results\v619-sign\installer-signed-runtime-20261011-attempt1；原Session1 pwsh26600、首轮signtool31088生命周期见项目Windows619台账。已按实际HWND460074解决遮挡与150%DPI截图，已向用户展示空PIN窗并请其仅在Windows输入；只跟踪同一run报告，不重启未知事务、不在输入后截图。尚无最终PASS。

2026-10-12追加：Mac445已原路径615/2615→619/2619覆盖，原指纹SYx46…ETVs、安装Key d32e…6fda和原general房间保持；真实SSH/MCP/rooms live、新鲜619云心跳核验后才ACK，独立守护exit0。当前主PID70551创建00:05:15，615回退包保留。证据入口Harness docs/acceptance/MAC445_619_ORIGINAL_ID_UPGRADE_20261012.md。Windows619首轮签名仍在Session1等待实际PIN，原run不重启。
