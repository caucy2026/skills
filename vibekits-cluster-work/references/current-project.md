# 本项目接续快照：2026-10-12

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
- Mac 最终 ZIP 在 `macos/cluster-unified-619-20261011-v1/Vibekits-619-final.zip`，423710323 字节，SHA256 `168d504c6b06c8ea019aa0bb91ee405edffac2a47acbbc5a3b56ccbafe887f1c`。Mac445已覆盖升级通过，其他机及商城发布仍未完成。本机 App618 是共享桥，其他任务正在用，不能为了619随意重启。
- Windows58 上新源码619真实 Release 已成功，核心版本2619；原合格615native复用须保持限定证据。619签名事务在途，尚无签名终态、未安装/发布。见 `docs/acceptance/WINDOWS619_RELEASE_BUILD_20261011.md`。
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

2026-10-12业务追加：Mac445619单次显式模型复验真实完成，管理MCP候选eligibleNow=true；原任务唯一offer、自动claim/fence1、context_issued真实发生，随后TASK_TICKET_BINDING，sessionId=null，进入reconciling。原事务不重发。已定位客户端漏合并当前platformTools，修后30项通过（含签名错误集合拒绝），尚未重建/实机复验。619暂不扩散覆盖/发布；Mac132同SHA已传输、独立解压codesign/build2619通过，仍保持原615运行。入口Harness docs/acceptance/CLUSTER619_PLATFORM_CONTEXT_BINDING_20261012.md。

2026-10-12候选追加：620/2620仅将619合格冻结目录的当前平台工具集合修复及测试叠加，再改隔离版本；2173文件测试后SHA未变。Mac完整Release145.16秒exit0、实际Universal/build2620、49Mach-O签名、签后兼容/NodeJIT/DSH/flock及原DR/entitlements匹配通过。原完整857非跳过用例覆盖（首轮5目录缺失，25项复测保留失败），另30协议通过。公证47db456e-ed55-401d-8e77-2aaf50af9d1e在途，尚未final ZIP/覆盖/发布；入口Harness docs/acceptance/CLUSTER620_PLATFORM_CONTEXT_CANDIDATE_20261012.md。Windows620四文件payload已独立D盘暂存，尚未展开/构建；619硬件签名事务不重启。已精确清理619终态native-target的3909生成库/对象，保源码/工具链/证据/正式ZIP/实际runtime，target需重建。

620最终包追加：公证Accepted、staple/validate、Gatekeeper、严格单App根及独立解压验签均通过，final ZIP423709844B/SHAa44515fd6eab711b7eccfc2d170295e1363a20940d285d9a1077dc3ce48274e1。主程序SHA3d0e5bfd…cc278f9c，2620。当前正向Mac445传输，尚未覆盖。原5deb已逾期，停止结果已按证据失败审核reject/scoreDelta0，保留原历史；新的业务复验不能冒称原失败通过，也不能重发未知事务。Mac445本任务CLI工具安装提示已按取消控件操作后核进程消失；没有安装工具链。

Mac445620覆盖终态：主PID52126创建02:55:00，原路径实际2620/mainSHA3d0e…78f9c、原指纹/安装Key/批准general房间/真实MCP与新鲜620服务心跳核验后ACK，守护exit0；AX授权仍true，619回退保留。一次模型复验实际MODEL_OUTPUT_BUDGET_EXHAUSTED，model-ready未置真且不重复请求。另发现Node start也漏平台工具，旧负控红/修后绿、完整runtime/官方SDK工具层/真实loopback endpoint门禁均过；描述预算已源修为固定2048并限300字，保留原provider/model/high及零工具/截止/失败门禁。尚未重建新包/实机复验，620仍有该Node缺项，勿扩散为业务PASS。入口Harness docs/acceptance/CLUSTER_RUNTIME_PLATFORM_AND_DESCRIPTION_BUDGET_20261012.md；ORICO约4.4GiB，下一轮先核本任务已终态可再生输出恢复构建空间。

2026-10-12 621准备追加：在cluster-runtime-621-20261012-v1以完整620输入隔离冻结621/2621，源模块及实际Node runtime同步，版本G0及平台合同正负控通过，尚未构建。只清本任务终态旧编译/检查输出2772生成二进制，保来源/工具链/证据/618final-v2/619final/620final/完整620解压副本；旧编译及619解压目录标不完整，不直接复用其验签路径。实际可用1.56GB→8.60GB，仍不满足Xcode10GiB持续保留，后续继续精确容量恢复及全Goal；入口Harness docs/acceptance/CLUSTER621_FROZEN_SOURCE_AND_CAPACITY_20261012.md。

621构建追加：容量恢复15.04GB后，四Node门禁、版本G0、2163输入SHA通过；完整Universal Xcode150.201秒exit0、实际2621，实际runtime SHA5bf22d8d…a39ccc58匹配修复源。49Mach-O签名、原DR/entitlements、签后兼容及JIT/DSH/flock通过。单次公证73878ff9-a3e4-4726-b7b0-d65c2900978a在途，尚未final/覆盖/真实模型重验；Windows6218文件已独立D盘暂存，不替代真实构建。

621final追加：公证73878ff9-a3e4-4726-b7b0-d65c2900978a Accepted，票据、严格ZIP单App根、独立解压验签/票据/Gatekeeper和实际runtime模块SHA均通过；final ZIP423709865B/SHAae2c49a3afdf93270c32ece70a044ea5b6344c5885f54020f8fa911c45783837，mainSHA54be36b2…f79c879b，2621。同一ZIP正在向445/132暂存，尚未新覆盖；先对账原upload意图及句柄，不重传未知结果。Mac445620的原固定会话即时idle，后续仍须覆盖/原Key/真实模型/任务实测。

621实机状态追加：Mac445620→621原身份健康提交，PID52231/03:54:35、实际2621+mainSHA54be…c879b、MCP及新鲜房间心跳通过后ACK/guard0，620回退保留；首次预算修后真实模型描述19:56:47Z成功reported。Mac132同包覆盖未通过：新621两PID94064/94082、无新心跳，独立守护exit26回退615；原ID/G73及615新鲜心跳恢复，当前主94554/13:11:55。旧图Office备用372799163虽匹配标题但无可验证输入/原生连接，未据此称恢复；仿真恢复后白盒查原失败，无621 Harness启动事件，native CLI可运行/无确定CrashReport，不定根因。失败包/日志保留，后续须修Intel/macOS12早期启动，不重复旧安装。100+设备资源清单问题已异步发出、等待资料，不替换既有七台目标。
