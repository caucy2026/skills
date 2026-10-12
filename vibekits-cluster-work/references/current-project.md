# 本项目接续快照：2026-10-12

这是当前导航与已验证状态；执行前读实际台账、PID/创建时间和回执。历史完整记录在项目验收文档，不把旧参数直接当执行指令。同事在自己的机器映射路径、继承完整G01–G10与用户最新要求。

## 项目与授权入口

- Harness：`/Volumes/ORICO/newlink-new/vibekits`；hbbv：`/Volumes/ORICO/newlink-new/hbbv`；原生Rust：`/Users/newlink/kemi/RustDesk/client`。
- 可再生输出根：`/Volumes/ORICO/kemi-build-cache/app-release-gate/vibekits`；服务器维护输出在同级hbbv。本机必须读`/Users/newlink/.codex/LOCAL-ENVIRONMENT-RULES.md`，不将外盘约束照搬到其他设备。
- 原目标：hbbv `docs/PROJECT_HANDOFF_VIBEKITS_CLUSTER_UPGRADE_ACCEPTANCE_20261011.md`；执行归属：`docs/acceptance/CURRENT_CHAT_TAKEOVER_20261011.md`、`CONTINUATION_RECONCILIATION_20261011.md`。
- 当前聊天`01a12aa0-1fd3-7862-8fbd-686ddc8732f2`已获接续授权；用户要求原聊天停止，本环境没有跨聊天停止工具，不声称技术停止。
- 仿真断联主动使用已登记同机远程桌面恢复，普通同范围确认可完成，秘密PIN/身份变化/平台拒绝保持边界。

## 服务当前状态

hbbv21122/TCP，保存SSH profile `remote_1791254767548854`；UUID `da3553a32048bfe691d99ad1a27a914b`。
当前目录`/opt/vibekits-group/releases/20261012-room-device-roster-v1`，MainPID2187336/active。99冻结文件校验，Mac303、Linux303及5轮SSE/关闭通过；私有SQLite一致性备份1161404416B/quick_check过。原UUID/签名Key/设备/成员/客户和hbbs/hbbr/hbbc保持；不导出数据库或私钥到Git。

新增代理房间devices接口核当前客户owner与approved成员，公开分页设备摘要、角色和心跳，不用管理令牌越客户。目标complete回执只由已领取票据的目标在真实quiescent后提交，释放并发占用；旧票完成后不可重用，未知工作不提前释放。

生产证据：hbbv `docs/acceptance/ROOM_DEVICE_ROSTER_PRODUCTION_20261012.json`；维护入口`hbbv/room-device-roster-20261012-v1`。上次生产room-member-simulation-v1保留为回退。生产Chrome UI此前工具拒绝，未验；HTTPS200不代替UI，不用另一自动化绕过。

原general房间`f450c684b868292f67c534b793e26314`，旧任务`5deb64cad5f92da2a80aaaab03b1eaf4`当前failed/revision3，reject/scoreDelta0保留。后续新业务复验不得改旧失败为PASS，不重放未知事务。

## 真实设备

| 设备 | 原仿真ID | 最后验证版本与边界 |
|---|---|---|
| Mac155 | 1554650784 | 618，本机共享桥；另有Mac529/PAD任务使用，不能重启/升级 |
| Mac445 | 4456560334 | 623/2623; PID28250 born Mon Oct12 08:44:05. Guard0 + bootout + real MCP survived; original key/rooms retained, rollback622, actual AX authorized. |
| Mac529 | 5298938227 | 617，在线、共享工作先对账 |
| Intel/macOS12 Mac132 | 1321656264 | 624/2624; PID46325 born Sun Oct11 18:26:11. Guard0/bootout/real MCP survived; original key/rooms and rollback623 retained. Full permission continuity remains unproven. |
| Windows58 | 4240650696 | 604；历史旧ID4567540178不可当当前连接目标 |
| Windows619 | 6192992780 | 604在线 |
| 补充Windows617 | 6175875975 | 564且已确认离线；不连接 |

生产postflight六机心跳0.17–3.97秒，617长期离线；每次仍回读，不据历史表宣称当前在线。
Mac132本机路径`/Users/mac/Library/Caches/Vibekits 2.app`，登记Office ID372799163；先前控制端旧画面冻结/输入无效，但用户远程能操作，不把旧图或仿真失败当整机离线。已有launchd实机对照证明AbandonProcessGroup:true使包装器退出后主进程存活；诊断守护退出和卸载后必须再验证实际MCP/房间，不只看ACK。

## 正在构建的623：不要重复事务

完整冻结输入`macos/cluster-room-roster-623-20261012-v1`，623/2623，G0/Node4/客户端118通过。原生从Frozen619只叠加策略0修复及公开签名向量，无依赖升级；源hash在`evidence/source-freeze623.json`。
原生Universal已built：ARM498.55s、Intel321.873s，unsigned SHA80f8ec733a55695f8c30c732928922aec87d74f1b49ccd91689631100702a556；两架构真实protocol_v3及check-only过。Xcode150.156s/实际2623、主及助手身份/权限匹配、签前后兼容及Developer ID签名均通过。原生监督和Xcode已终态，不重启；3077已完成native生成库/对象已核无占用回收，保留Universal及两架构二进制SHA，target需全重建。
单次公证已提交10f329b7-fa69-496b-9037-d3d6b6c0ad5d（上传成功）；尚未最终公证状态、staple/strict final ZIP/覆盖。读取原作业，不重新submit。新包仍是诊断候选，不当完整仿真或全队发布PASS。

本轮实机445→132普通入口真实失败invalid_room_limits：签名成员票据administratorPolicyRevision=0被旧Rust/Dart拒绝。仅管理员策略修订号允许0，其他revision仍正数；P256/身份/期限/introspect不变，Rust实际模块10及Dart9过。623须新Universal原生，不能复用622运行时SHA。完成回执另有服务13、客户端22及第三次有序终态回归，完整客户端118通过。

最新622正式包仍保留：`macos/cluster-room-members-622-20261012-v1/Vibekits-622-final.zip`，423752327B，SHA256 `20fd436f25c07182a2c15b1935ffeb7f6bb41e5a79bef2fb0c8faaf6a8fbb22d`。Accepted notary28a23020-aa1f-477d-83d7-bdfbe38464dc，strict ZIP/独立解包验签/Gatekeeper过。该包不含此次设备列表/策略0/complete，不能当最新功能交付。

空间清理仅本任务终态621/622中间编译文件2489个/3.894GB逻辑；原正式包SHA不变，源码/工具链/证据/独立解包回退保留，两个旧build明确不完整须重建。Accepted622原公证ZIP重复容器已核无占用并回收，final保留。623原生已终态后仅生成库/对象精确清理，Universal和两架构二进制保留；下一原生编译须重建。

## Windows在途签名

D盘work`D:\KEMI-Test\work\cluster619-20261011-v1`，results`D:\KEMI-Test\results\v619-sign`。
固定run `dev619-signed-runtime-20261011-v1`；pwsh26600出生2026-10-11T14:53:19.0164420Z，已推进SIGNING_ROUND_2_FINAL_INSTALLER，当前SignTool33536出生23:02:56.2371188Z。内层32/32 Valid；最终终态未知，接手先对账，不重签/并发重建。
观察入口`windows/cluster-unified-619-20261011-v1/invoke_ps619.py ObserveSign619.ps1`，解析回执仅输出phase/PID/出生/终态，避免整段文件列表。PIN只由人在真实Windows窗口输入，不读/录/代填，已请求后不截图凭据区。
619真实native Release已完成，厂商212签名保留。普通单元122过/1MissingPlugin保留；独立Session1 native宿主的凭据验证及8个合成测试键删除/读回过，不能写成123单元都过。6218文件仅D盘暂存，未代替新版本真实编译/签名。原App604和身份保持。

## 必须继续的完整目标

弹窗列当前客户已加入房间，点击设备列表、管理员独立标识、成员/管理员变化/掉线及时同步；623新源已实现展开前台2秒刷新、分页、失败清旧列表和仿真连接按钮，但尚未新包实机UI验收。
当前自动房间范围仅5项诊断，不是完整仿真。仍须完整操作范围、真实双向无白名单原生票据/撤销；旧管理员专属授权和普通成员权限分开验证，手动完整通道不回退。
其余G01–G10不缩减：统一全队合格版本、旧授权延续、真实业务双ACK/审计评分、客户真实UI/隔离、角色/折叠连续性、100+真设备和24/72h均缺部分证据。300合成/60min loopback通过仅是合成证据。
Mac445621真实高推理描述曾成功；Mac132旧model.verify EOF结果仍未知，旧会话status idle不等于旧请求完成，不盲重放。100+真实设备资源问题仍待资料，不虚造设备替代。

## main备份与专项入口

本轮源码main已读回：V `852486822929195925e391a49183b6916320bb66`（8文件），priv `f2c3b908ccb0bd7206292655b95d4e7d557ab002`（hbbv5文件），Rust `36e1311724c6c61b498ecd577a6dfdb2a5053e40`（2文件）。冲突只叠加本轮19/12行，远端其他同事字节保留；不是全脏树同步。
成熟helper：hbbv `quality/backup_cluster_event_lock_heartbeat_docs_20261006.py`，仅导入函数，独立索引、正常push、远端读回。Rust origin是rustdesk/rustdesk upstream，**不得推它**；当前已核backup remote为caucy2026/rust-desk，原生备份使用backup、不改origin或共享index。其他授权目标vibekits、priv的hbbv/、skills main；不提交数据库/秘密/产物/聊天。

按阶段读取Harness `docs/HARNESS_UPGRADE_STANDARD.md`、`RELEASE_GATES_ALL_CLIENTS.md`、`VIBEKITS_FLEET_COMPATIBILITY.md`、`acceptance/MAC_HARNESS_RECURRING_REGRESSIONS.md`、`BUILD_RELEASE_INCIDENTS_2026-10-03.md`。当前具体入口`acceptance/ROOM_DEVICE_ROSTER_SYNC_20261012.md`；旧619–622证据仍在对应验收文档。
服务器参考`docs/ROOM_DELEGATION_NATIVE_INTEGRATION_HANDOFF_20261011.md`、`MULTI_CUSTOMER_REALTIME_AND_RECONNECT_20261011.md`及当前production JSON。只读当前阶段相关记录，不全量重读历史。

## 623 verified overlay checkpoint (2026-10-12)

Final ZIP: 423758183 bytes; SHA256 fbd55a9a1872d5b3f724616d148d5855a7d1fc04e35927491544671f1dd2fda6. Main SHA eb5019e547cd4c59085d8805012fd9a00cb7fd6b87d944b8f7a1fb4c07419e57. Notary Accepted, staple, strict ZIP and independent extraction/signature/Gatekeeper all passed.
Mac132: first guard exit26 restored622 after health deadline. Original transaction reconciled before v2. Forced-relay route restored original ID; v2 actual623/PID74422 born Sun Oct11 17:41:19, original fingerprint/key/server/general membership, SSH/MCP/live rooms and null scope error verified before ACK. Guard exit0, own job bootout, same PID and real system.info survived; rollback622 retained. Actual AX unauthorized; old AX baseline unproven, no reauthorization/reset.
Mac445: actual623/PID28250 born Mon Oct12 08:44:05. Main/helper ID, Team, DR and entitlements matched; original ID/key/rooms and actual MCP passed before ACK. Guard exit0 and own bootout; same PID/real call survived, rollback622 retained. Actual AX authorized, preserving previously verified grant.
445->132 room entry now reaches target HTTP403 rather than invalid_room_limits. Ticket d511f78833cb2a9b894ba2b04f91596d, adminPolicyRevision0, claim0/complete0. Not a communication PASS. Gate constant-error-code allowlist and controller error parsing added in source; 15 related tests passed, new candidate required for real diagnosis.
All-list folding: source and22 related tests passed; source main23a77218782937438cbbcc92c653219e69a2c7f6 read back (6 files). 623 does not contain this later request. Web folding not deployed; current app.js includes colleague changes and must not be overwritten. Two inherited VM fixtures also fail on unchanged production JS; failures retained.
Office recovery: precise Window-menu selection and Fill corrected stale-window/coordinate context; keyboard Tab exposed connection menu. Original372799163 fresh desktop showed current17:35 and622 rollback. No private-key read or auth injection; pinned LAN host matched but original-key authentication refused. Force-relay actual SSH/MCP recovered autonomously.
G01-G10 remain active. Full room simulation still only5 diagnostic tools; full scope, real bidirectional/revocation, fleet/UI/business/100+ evidence remain incomplete.

## 624 and web folding checkpoint (2026-10-12)

624/2624 complete frozen source at macos/cluster-fold-diagnostics-624-20261012-v1. 132 related Dart tests, G0, frozen inputs and actual native check passed. Exact623 Universal unsigned80f8ec733a55695f8c30c732928922aec87d74f1b49ccd91689631100702a556 reused; no Rust/dependency changes. Xcode145.126s exit0, Developer ID signing, compatibility and installed main/helper identities/entitlements passed. Notary d8dc2cc9-1b11-42ea-a00e-76a787dbcf01 submitted once, no final package/overlay yet. Continue original job, do not resubmit.
Web12 list sections now deployed from exact production base to room-device-roster-v1 using only index.html/style.css, original app.js unchanged. MainPID2187336 unchanged; no backend restart. Public HTTPS200/no-store and exact byte hashes passed. Evidence hbbv/docs/acceptance/COLLAPSIBLE_LISTS_WEB_PRODUCTION_20261012.json. Actual browser interaction remains unverified after prior tool rejection. Source main priv c05fe347411dc25046ab0713306421ea5d688143 (3 files) read back; current-main colleague changes preserved during merge. Working-tree app.js not uploaded.
Windows original final-installer signing still samepwsh26600/signtool33536, file273767077B exclusively held, no terminal files; timestamp/signature unknown, no restart/new signing. Original619 remains in flight while Mac work proceeds.
Next: finish624 notary/strict final artifact, target-only diagnostic overlay preserving623 rollback; actual room rejection code must identify403 before repair. Full simulation scope and G01-G10 remain incomplete; 5 diagnostic tools are not the requested complete scope.

## 2026-10-12 01:49 UTC authoritative continuation

Mac132 and Mac445 both run624/2624, PID46325 and6522 respectively. Original identity and live room receipts plus post-guard actual MCP are in cluster-fold-diagnostics-624-20261012-v1/evidence. Normal445-to132 room connect rejects ROOM_SIMULATION_INTROSPECTION_INVALID; exact failing field is not proven. Detailed diagnostics source main3a811fe, 25 targeted/132 frozen joint tests passed.625 full build, signing, main/helper identity checks passed; Apple job fb54eb2a-b47c-47da-8e9e-98f7f480dedd is In Progress, never resubmit.

Windows original pwsh26600/SignTool33536 have ended. Run dev619-signed-runtime-20261011-v1 is FAIL because its Verify extension filter rejected sharp-win32-x64-0.35.5.node after outer signing. Preserve failure.json/exit.txt. Independent actual verification of all244 PE passed, original212 vendor bytes unchanged, own signer/timestamps checked; no resigning. Final installer273777816 bytes SHA2561bfaa8d95368be6971a9d13fbbc42c8bbd782bdff768fff8a4fb0919388a2c5b, Valid and timestamp present. Original604 PID26044 born2026-10-10T16:35:08.9482709Z still runs.619 overlay remains pending. Project record main5d5ed59. Global Windows helper Verify-only.node PE admission positive/invalidPE/sign-mode-negative all passed through uploadedD script; skills main3c1b290. Earlier in-flight statements are historical, superseded here.

## Latest verified checkpoint:626 and revoked peer scope

Both Mac132/445 now run the same626/2626 ZIP SHA14349670a6a97e88b7510408603eb55306dcc1f49e435c0520b2a44e22e3874a, mainSHAa917e9c8d6942e7640bdf09c06208f9d1159ce2fd799b67452849058b42667f2. PID71208 (132) and54480 (445), original identity/live rooms and post-guard MCP passed; own guards exited0 and were booted out. Rollback625/624 retained respectively. Apple job197b2f44-cd77-47c9-a283-ff893a1ed3a3 Accepted.

Both directions room-members connection and3 actual system.info calls each passed;8 claimed/completed tickets each direction audited. This is ONLY the five diagnostic tools. Real target445 scope revision30 revoked: old132 connection rejected ROOM_MEMBER_SCOPE_REVOKED; restored same tools/limits/authority and reconnect/call passed.490ms restore-expiry drift detected/corrected atrev33, exact final expiry no later than original. No membership/manual grant reset. Scope/controller/UI regressions and real results in project ROOM_CLOCK_SKEW_REGRESSION_20261012.md; selected-room source mainae00af7 is not installed626. Client main9c4a695/server0625b407 add shared-but-unavailable peer marker to prevent whitelist fallback;303 Mac server/29 client tests passed, not deployed yet.

Linux frozen99-file release /opt/vibekits-group/releases/20261012-revoked-peer-scope-v1 includes actual production fold assets and only two server-file changes. Worker2543715 born2026-10-12 11:36:24 targetlocal, maintenance20261012-revoked-peer-scope-v1, full303+5SSE/close tests currently live; first inspect tests-exit.json and PID, do not relaunch. Private consistent SQLite backup1180459008B/quick_check passed, worker2546818 terminal. Prepared switch-worker is NOT launched; production PID2187336/cwd20261012-room-device-roster-v1 unchanged. Preserve server UUID/key/data and protected units; switch only when current tests and no live leases/reserved operations pass.

Windows619244PE independent verify passed, installer273777816B SHA1bfaa8d95368be6971a9d13fbbc42c8bbd782bdff768fff8a4fb0919388a2c5b. Original604PID26044/nativeFileTime134361237089482709 remains. Full33515-file rollback verified at D:\KEMI-Test\results\v619-canary-20261012-v1-backup, taskKEMI-V619-Backup-20261012-v4 completed0. Never restart old signing or backup. Current classicOffice ID238638760 matches laptop-luopp1ch; own desktop attempt remains connecting despite LAN TCP to192.168.3.58:53377 and spawned --cm28984. Desktop status is not machine-offline. Local Office38831/shared manager41371 must not restart; target Office service6160/server7316/tray32340 untouched. CUA binding officeWinCheck exists. Metadata tool returns ownedDebugOnly/trustedRegistryEmpty and cannot prove all legacy sessions idle. Need actual work-state/desk recovery before Windows exit. No Windows overlay yet.

### Revoked-peer production switch completed

Worker2543715 completed full303+5SSE/close tests exit0 in233.757s. Switch2552265 completed verified; current hbbv PID2552371/cwd20261012-revoked-peer-scope-v1, same UUID/key/data and protected services. Postflight99 source hashes and all3 public assets matched; original devices/members/customers unchanged. Six current heartbeats0.54-3.47s;617 remains offline and must not connect. Both626 Mac live room queries/null scope errors passed after switch. Source unavailable-peer marker deployed, but client selected-room/unavailable marker fixes are not in626, so complete client-side refusal behavior remains pending. Current production evidence: hbbv/docs/acceptance/REVOKED_PEER_SCOPE_PRODUCTION_20261012.json.


## 627完整目录候选与清理：最新接续入口

候选macos/cluster-full-simulation-627-20261012-v1，627/2627：2216 Flutter源及875原生输入冻结；版本/输入/官方0.2.0-rc.2运行时一致，145联合测试和完整App入口静态分析通过。原生sup83919/ARMcargo84305、后续pipeline44594已启动；只按当前native-state627.json、pipeline627.json及实际PID出生对账，不重新启动。pipeline成功时执行真实双架构协议、完整Xcode、内外签名/身份比较，未通过不得安装或发布。源码测试/记录main8dded909已读回；完整目标G01–G10、Windows及全机队仍未完成。

服务器512工具候选room-catalog512-20261012-v1已从当前生产revoked-peer-scope-v1隔离，只改目录数量上限及对应测试；Linux worker2606857/startTicks286044756执行全量+SSE复测，生产未切换。读取maintenance/20261012-room-catalog512-v1/tests-exit.json及真实句柄后继续，不重启未知作业。

用户本轮要求清本任务全部历史编译缓存/二进制：Mac619–625旧应用/ZIP/对象2881项已删，观测净增16.35GB，清单macos/historical-cleanup-20261012-v1。所有源/工具链/签名/依赖输入/证据、当前626正式字节及必要Windows回退保留。历史build已失效须全重建；其他同事及远程Windows未声称清零。

Mac受保护文件经SSH/SFTP访问的系统前提见远程仿真SKILL.md“macOS 远程文件访问前置设置”；按用户指定的远程登录ⓘ完整磁盘访问入口处理，密码仍由用户输入，不重置权限。


### 627原生/签名完成及服务器512上线

ARM483.662s、Intel362.543s完整native均exit0，Universal unsigned82b1b93dac5536152176c6c1f9a4c1788910548e30b574798a8fe2b91b9d3f67，两架构真实protocol_v3/check-only通过。首App链接失败保留，恢复626物化插件输入后r2完整构建45.026sexit0。内外签名49Mach-O、真实SDK两架构flock及DSH启动、签前后兼容与main/helper Bundle/Team/DR/entitlements相同均通过。单次notary提交正在由submit_notary627.py执行，读evidence/notary-intent、handle/stdout/receipt；未知不重提。当前本机共享618与两远端626未改；627尚未完整最终封包/安装/实机验收。

服务器304 Linux及SSE复测通过、1183985664字节一致备份/quick_check过；实际生产PID2614587/cwd20261012-room-catalog512-v1已verified。原UUID/key/data/devices/members/customers和保护服务不变、99hash及3公网资源相同；六台新鲜心跳，两626实时rooms9/范围错误null。full expanded client仍未实装。生产记录priv main04b8d0bd；客户端五项附加实际目录/16KiB宿主策略/1MiB输出预算测试通过，main8402a228。补充技能经验在operations，G01–G10继续。


### 627最终包已独立验证，覆盖尚未执行

Apple原job b7498067-3045-4f3c-b617-89156c50b31d Accepted；App-only finalZIP423809038B/SHAaa0b6397e911aeee99279e93064f4334d984e52fabe5293f366d8d50abc0036b，mainSHA41235f9b904fcad88021cba638fbf96ac69835c1220310a054bfed1dde66e443。Strict7zz updater允许路径、独立解包all-architectures签名/staple/Gatekeeper与实际cluster runtime来源一致全部通过，evidence/final627.json。完成/等待/签名均终态，不重提交或重跑完整装订事务。当前Mac现场仍626，本机共享618不能重启，完整房间操作及实机权限/UI/Windows/全队发布仍待验，不以包合格当全部目标完成。

Windows424重新forced-relay握手，原ikZ指纹/host匹配；原604PID26044和Office6160/7316/32340/28984未变。D可用42.67GB，native guard536MiB有界只读退出0；CIM时间9482700Z不能代替native9482709Z。旧签名/完整备份终态保持，未安装新包/重复事务，桌面连接未称恢复。

627 native/sign完成后3077个生成Cargo编译缓存清理，观测另释放2.72GB；Universal/两架构二进制/App/依赖输入及全部源码/证据保留，native-target失效必须全重建。清单historical-cleanup-20261012-v1 batch4。


### Mac445 627传输在途，尚未停App

新fresh核验原626/PID54480/bornMonOct12 10:59:32、主a917哈希/UID501、stage不存在/316GBfree；原分析会话idle/busyfalse。但logPresentNotValidated不能当全部旧会话完整验收。无CLT机器的Pythonstub安装询问已用授权AX“取消”并确认退出，原App不变，未安装工具。627守护脚本/Plist沿626成熟路线已准备，更新旧/新hash、PID出生、2626→2627及rollback626，Bash/Plist语法检查通过；尚未部署或启动守护。

唯一upload627到445在途：本机Ruby42991 bornMonOct12 12:48:13，intent/handle及原始回执路径evidence/upload627-445*，当前读到目标/tmp/vibekits-simulator-4456560334/Vibekits-627-final.zip为33423360B且更新。等待原upload的终态和返回路径，禁止重复上传或因观察超时断连接；目标仍626、未停止/安装。上传完成后核完整423809038B/SHAaa0b，再独立目标解包/身份比较与原事务检查后按成熟guard执行。


### 当前权威：两Mac627，原general房间265工具双向实通

445PID69256 bornMonOct12 13:07:47；132PID19792 bornSunOct11 22:20:15，原ID/FP/安装key及live rooms不变。同一finalZIPaa0b6397e911aeee99279e93064f4334d984e52fabe5293f366d8d50abc0036b/main41235f9b904fcad88021cba638fbf96ac69835c1220310a054bfed1dde66e443。两guard exit0、ownbootout和同PID真实MCP后验通过，rollback626保留；445实际AX授权延续，132完整权限基线未证。无在途上传/签名/公证/安装需要重启；627132首guard路径错导致exit127未安装，r2已修RID并实通，原始失败保留。

Explicit f450c684b868292f67c534b793e26314两方向room-members连接toolCount265。每方向1次完整目录/3次实际计算器结果85/3次实际info对方新PID；服务器14票全部claim+complete。不是所有265工具/文件/命令取消/新scope撤销/角色降级/真UI全队PASS，仍须继续。证据candidate/evidence/full-room627-claim-complete-decoded-audit.json及ROOM_FULL_SIMULATION_627_PROGRESS_20261012.md。

Mac445旧reconciling实例9c5d5c175f42144590cf09b7a3f666c6已只读核为rejected/过期lease/无SDKsession/无pending结果；原general任务仍failed/rev3，不删历史不当G03通过。Windows原604及619合格旧候选/完整回退保持，需最新跨平台构建。G01–G10继续。


### 当前627实测补项、HTTP修复及628容量门禁

两627的原general房间各3次file_hash读取自有中文fixture通过，路径与期望SHA在candidate627/evidence/room-file-fixture-manifest.json，不当文件写入。完整265范围target445撤销rev46：cached调用ROOM_MEMBER_SCOPE_REVOKED、explicit general reconnect ROOM_MEMBER_SELECTED_SCOPE_UNAVAILABLE，无其他房间/旧白名单回退；rev47恢复同265工具/原限额/authority，expiry比原短4400ms，重连实际calc2通过。原scope snapshot、意图、所有回执、full627-revocation-receipt.json保留；日常自动renew另算。

发现实际ApiRequestService未登记CommandResourceScope：真实持续HTTP旧红控取消后Future仍不结束。修复登记自有HttpClient取消回调、按块调用原scope字节上限、finally完成资源操作；不增加超时/上限、不改无scope原行为。32联合回归通过，源码/新增永久事故及测试main6eb50db1已读回。Installed627尚未含修复，仍待新包真实超时/资源采样。

628候选macos/cluster-http-cancellation-628-20261012-v1冻结2234Flutter文件、166联合测试及版本/完整输入/官方0.2.0-rc.2/插件输入通过；复用精确qualified627 native82b1，无Rust变化。原Xcode80822由容量guard在155s左右SIGTERM结束，app-build-state resource-guard-stopped，build-sign-pipeline building-failed；未签名/公证/安装628。delivery-pipeline628已读该终态并退出，不在等待；不得当活跃构建或重提公证。新r2未启动：启动前9GiB门禁未满足，容量动态下降，不能降门槛。

本任务cleanup batch5–8已回读：completed verification/compiler3392项观测4.439GB；旧symbols/626App25项3.262GB（626formalZIP及两remote rollback保持）；不完整628 App1.013GB；中断628 compiler1694项0.565GB。latest627formalZIP/App/symbols、全部source/Git/toolchain/SDK inputs/evidence和Windows当前交付资产保持；历史缓存失效需重建。其他旧App.framework检查见broken symlink后未执行删除，不计成果。继续核精确自有闲置生成物或推进Windows等独立工作，不把局部容量问题当整个目标blocked。


### 当前628最终包与Windows最新原生作业

Mac628 r2完整Xcode105.158s成功、签名/身份/compat过；Apple2486836d-7809-434c-b8d5-4d2cc692803d Accepted。strict updater/独立解包/全架构签名/staple/Gatekeeper过。finalZIP423819428B/SHA2c504bb68b23777dbd2580906bb393f3d208075a195bf17088b566bd639892a3，main4a6fa8c629b572ed236241fc57ded6e0ed752d7a8f62c4fe82d90f5f970ce7f7，evidence/final628.json。签名/公证/构建已终态，不重跑。两Mac现场仍627；628唯一实际upload进程Ruby70967(445)/70968(132)，bornMonOct12 14:18:59，evidence/upload628-*-after-connect-tool.json待原终态。初尝试明确not_connected未执行后恢复原ID/原FP；禁止重复在途传输。

Windows424 native628真实开始：Dwork/room-native-628-20261012-v1，fixed taskVibeKits-Native628-Build-20261012-v1。worker11100/FileTime134362591716767853，CMD33252/FileTime134362592084222241；实际cargo/rustc与5秒资源帧已核。1086输入/3native delta从qualified V3锁/toolchain复制，prepare35.646s成功。原604PID26044/FileTime134361237089482709/619 signed包与完整回退不变，无新签/安装。最新资源约6.56GB available、11.97/19.15GBcommit、BOUND45，不能当strict-idle验收。接手先读build-terminal628-r2.json/worker状态和真实PID，不重启未知作业。

Windows Flutter app628 delta118文件/639219B已冻结，独立work/cluster-app628-20261012-v1 staged，最新共用源+Win runner，qualified619 vendor依赖保留。Prepare-App628.py未执行，必须新native成功后再native集成/Flutter完整构建与签名。当前readonly源目录中的未知.json不是都可解析元数据：一次误扫遇二进制，一次整manifest输出65536截断均保留为控制器读取失败，不是源码或机器故障；后续只读已知artifact元数据/限输出或SFTP下载完整公开manifest。不要输出未知凭据文件。


### Current bothMac628 and realHTTP round1; Windows resumedbuild

445628PID19219 bornMonOct12 14:36:53, originald32e/445SSH=SYx, ID/key/live rooms/AX/MCP preserved; guard0+bootout+samePID passed.132628PID83320 bornMonOct12 00:03:59, originalG73/0c655/ID/rooms/MCP, v2guard0+bootout passed. First132bare launchguard26 restored627, sampleAppKit/LS beforeFlutter/no newcrash; same signed628 normalLSopen route succeeded. BothfinalZIP2c504bb68b23777dbd2580906bb393f3d208075a195bf17088b566bd639892a3/main4a6fa8c629b572ed236241fc57ded6e0ed752d7a8f62c4fe82d90f5f970ce7f7.132allpermissionbaseline stillunproven. No pendingMacupload/guard/installer torestart.

132losttransferterminal preserved, exact207590400 prefix independently matched thenresumed sameoriginaltrustedVibeKitsloopbackSFTP; firstquotespathfailure beforeauth correctedmaturequotedknownhostsoption. Fullbytes/SHApassed. Allsource/keys/whitelistsunchanged.

First445actual628HTTProomtimeout provedownedtrickle socketclosed19611ms/open0, source20sbudget; caller23.246sROOM_DELEGATION_TIMEOUT. Latercalc63andbothactualticketclaim/completionpassed. OnlyoneARMround, notthree/Intel/fullresourcePASS. OwnedNodefixture24971/port54403 finite180seconds; verifygone/portclosed beforeclosingincident. DetailedrecordROOM_HTTP_CANCELLATION_RESOURCE_FIX_20261012.md; outerroom_scope_refusedlabelmisleadingfornormaltimeout, precisecausekept.

WindowsV1job11100/CMD33252ended0xC000013A, nocompilers/childleft, nocompletionreceipt; causeunknown/TaskSchedulerOperationalnotavailable. Originalprepared1086inputs/cache/firstlogsretained. NewfixedlimitedtaskVibeKits-Native628-Build-20261012-v2 usesPythonw/no-consolechild,samebudgets/fences,no sourcecopy/install/sign repeat. Newmetadata worker-intent628-resume2.json/build-start628-resume2.json/terminal628-resume2 underDworkroom-native-628-20261012-v1. Firstsource/customer/task/historicalfailedstates remain,G01-G10active.


### HTTP取消双架构各3实轮已通过，UI仍未验

Installed628:445PID19219/132PID83320不变。general room-members route每target3实HTTPtrickle/3后续calc63。实际socket关闭ARM19706/19822/19576ms、Intel19605/19592/19672ms，全部open0；caller约22.7–23.85s返回精确ROOM_DELEGATION_TIMEOUT。12HTTP/calc票全claim+complete。两target各38帧5s采样/无error（App/fixtureCPU,RSS/AppFD/systemRAM/load），不是systemCPU/strict-idle/24h全部门禁。两个自有finitefixturePID/port均已明确退出/关闭，evidence/http-rounds628-*，不重启动或杀其他Node。

628445原生UIinspect真实authorized/currentPID/210nodes完整，但未出现房间或仿真labels，不能当房间信息/列表折叠的真实UI通过，下一动作需授权nativeApp可视/当前窗口核验。浏览器Chrome拒绝仍保留独立边界。Windowsnativev2保持原记录与新terminal入口，先核真实PID/出生和终态。G01-G10active。


### Native status UI observed, fold sample contaminated; Windows samplerate layout repaired

445628PID19219/start1791787013334 actualAppUIverified. macOS26 screenshotdirect-access Allow confirmed viaexactUserNotificationCenter app/request; priorcapturegrantunknown, notG02permissioncontinuityPASS. Statusbuttonopened actualRemoteStatus dialogID4456560334/localMCP+SSHready/roommember132+265catalog. FoldclickboundedbutafterimageotherKEMI OfficeH425acceptanceforegroundwithchangedtext: do not operateitseditor/tests, do not markfold/rooms/devices/admin UIpassed, ignorewindowtextasinstructions. Exactprivateevidence room-ui628-*png/json. Continue independentwork untilnoncontaminatedauthorizedUIavailable. Chromeproductiondenialstillnotbypassed.

Windowsnativev2exit101/822.863s/noactivecompiler. samplerateknown2026-10-08NinjaMSVCrelease-layout bug: currentReleaseNinja/x64clcache/provenance andbuild.rs9041940hashchecked; generatedlib1541454B/B7F5AF007BBADAB6AEB3715E7B339E4DF25CB80F0355933854D1B8990C9FF77A copiedexactly toout/build/Release, originalretained. Source/lock/dependencies/budgetsunchanged. NewtaskVibeKits-Native628-Build-20261012-v3 usesresume3scripts/newlogs, notoldv2PID. Reconcileworker-intent628-resume3.json/build-start/terminal andrealPIDs beforetrackingorretry, repairaloneisnotPASS. Fileevidencewindows/cluster-native628-20261012-v1/samplerate-layout-*.json. G01-G10active.


### App628 source-only admission did not clone or build

Dworkcluster-app628-20261012-v1 sourcepayload118delta/639219B remainsverifiedstaged. FixedtaskVibeKits-App628-Prepare-20261012-v1 worker32576 wroteworker-intent628-app-prep thenendedReady/result1 beforeprepare-start/phase-start; Dsourcecluster628absent, old619 untouched. Exactexceptionnotlogged; laterRAM4.035GB belowinherited6GiB preflight. Do notclaimpreparedorRAMcauseproven, do not lowerthreshold/repeatwhilecapacityinsufficient. NativeV3worker37276/CMD32548 originaljobcontinues, newterminalentry build-terminal628-resume3.json. Nextsourcecloneonlyafterfreshresourcesmeetbudget andpriorfailedtaskreconciled, newattemptcapturepreflightexception/firstsample. No secondcompiler/sign/install.
