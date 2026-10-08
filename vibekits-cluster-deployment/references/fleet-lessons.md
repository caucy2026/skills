# 六机集群搭建的实测故障与处置

本页来自 2026-09 VibeKits/hbbv 六机验收。设备 ID、目录与版本只是**案例定位**，新任务须重新读取项目运行文档、当前状态和授权。可信记录与当次证据保存在 VibeKits 项目的 `docs/acceptance/CLUSTER_MASTER_GOAL_AND_RECOVERY_2026-09-28.md`；仿真接口细节见 `vibekits-remote-simulator/references/tool-contract.md`、`channel-recovery.md` 和 `windows-build-transfer-lessons.md`。

## 先确认四种“在线”

1. 服务端成员 `approved` 只是审批持久化，不表示客户端已激活。
2. 服务端新鲜心跳表示集群联机；旧心跳和网页缓存不能证明当前在线。
3. `vibekits.simulator.connect` 返回 `connected=true`、SSH/MCP ready，才说明当前仿真通道能直接操作；`remote_disabled` 不能由心跳推翻。132 曾先返回 `remote_disabled`，后来同一个 ID 再次实测连接成功。不要沿用旧失败结论。
4. App/relay 进程在线不表示 Harness 有 key 或能执行需要智能体的任务。无 key 可报默认设备描述和做受支持的确定性操作；竞标还须核对工具就绪、容量、分配、租约与验收。

## 给 ID 后的最短排查顺序

- 调仿真连接；核对返回 ID、主机名、SSH 指纹与可信基线。历史 58 ID `4567540178` 与当前 `4240650696` 不同，不能凭旧 ID 离线判断整机离线，更不能自动当作同一身份；变更根因仍待查。
- 读真实进程可执行路径，继而读该路径下包的版本、Bundle ID/签名。132 曾运行在 `~/Library/Caches/Vibekits.app`、529 在 `/Applications/Vibekits.app`、58 曾从 `D:\KEMI-Test\installed\Vibekits` 启动；目录名里的 `dev319` 不是版本证据。两个相同应用副本可能分别承担主进程与 relay，须查进程命令行。
- 远程查客户端房间实时状态，并用管理 API 查申请、审批、成员、心跳。设备能被仿真操作但房间离线时，优先从设备侧测试服务端 HTTPS 路由和证书，而不是只从管理机访问。445 的 192.168.1.x 网络到 192.168.3.65:51838 不通，使其可仿真却无房间心跳。网络没有路径时，改为已授权的可达服务端地址或修复路由，不能跳过 TLS 校验。
- 房间目录刷新、申请、审批、激活、首个心跳分别留证。服务端已经持久化申请时，客户端随后报错不代表申请失败；按申请 ID/修订查状态再决定补救。

## 已遇故障及修法

| 现象 | 实测原因/判断 | 可复用处理 | 完成证据 |
|---|---|---|---|
| 申请成功后 Windows 报 `安全凭据超过 Windows 凭据长度上限` | 房间目录、成员 JSON 或设备档案与待上报能力被写进 Credential Manager，单项上限约 2560 字节。58 的申请已到服务端，但客户端激活与心跳受阻。 | 不重复申请。非密钥、可重建快照存应用私有文件；私钥、令牌仍放系统凭据库。已有 dev339 修复房间缓存，dev340 进一步修复档案；须装上签名版本后再看实时心跳。 | 原申请/审批修订不变，客户端 `roomsAreLive=true`、描述同步成功，服务端新鲜心跳。 |
| 批准后网页仍显示离线 | 审批不等于激活；App 未运行、集群关闭、TLS/路由失败、端侧持久化错误均可导致。 | 看客户端实时错误和设备到服务端的网络，恢复进程/配置后等待首个有效心跳；只更新网页无效。 | 两端同一设备 ID 与房间、服务端心跳时间前进。 |
| 更新脚本认为 HTTP 401 是服务崩溃 | 132 的认证监听器正常响应 401；错误脚本回滚磁盘旧包却留下新版进程。 | 401 仅说明未经认证。健康门禁分开验证进程、监听器、认证 API；回滚先停候选进程，再核对磁盘包与运行进程版本一致。 | 原 ID 重连、磁盘/进程版本一致、经认证功能调用通过。 |
| 远程更新后仿真断联 | 更新原 App 会暂时切断自己的桥；若子脚本提前杀 App，安装脚本也可能中断。 | 使用独立、可恢复脚本和结果文件，先传输哈希验证包、准备回滚点，再替换/启动；重新用原 ID 连接读取结果。必要时利用已核身份的另一合法通道恢复原交互用户 App，不用其它系统账号伪装原身份。 | 原 ID/主机指纹未变，实际新版进程运行，结果文件与远端事实一致。 |
| Mac 更新后瞬时 `No route to host` | 529 新进程刚启动时房间请求失败，但设备 `nc`/`curl` 可达，后续正常刷新恢复。 | 先看同机端口连通和短时间内下一次刷新；若持续失败再查路由、证书与客户端日志。 | `roomsAreLive=true`，服务端新鲜心跳。 |
| 无 Harness key 的客户端不能竞标 | 旧版把无 key 容量报 0；dev343 改为仿真就绪时可报 1 个确定性工作槽位。仍可能有 `TOOL_NOT_READY`，不能把容量修复视作竞标通过。 | 核对任务是否需要智能体、工具就绪、实际竞标结果和租约；对未知能力不得虚称通过。 | 有效 bid/claim、唯一租约、执行记录和独立验收结果。 |
| Windows 签名或安装卡住 | 硬件令牌 PIN 弹窗位于交互 Session 1；非交互远程命令看不到，也不应索取 PIN 文本。设备空间可能很小；xzl 只有 C 盘。 | 先核对磁盘与现有构建；按该机既定工作目录做最小传输/构建，Session 1 启动签名工作，让持有人在本机输入 PIN；验内外层签名，再原位覆盖，保留回滚。不要把 58 的 D 盘路径硬套 xzl。 | 签名完整验证、原 ID/授权保留、真机启动、房间实时上线。 |
| 同硬件升级或卸载后 ID 变化 | 58 的历史 ID 变化原因仍未证实，配置文件创建时间不能证明被删除。 | 发布前冻结原 ID、公钥指纹、主机指纹与凭据状态；覆盖后原 ID 重连。正常卸载重装须另做保护身份材料的专门验收，不要用新 ID 加房掩盖。 | 原 ID 可连接，房间仍是同一设备且无重复成员。 |

## 房间、任务和收尾门禁

默认房间可由服务器预建。设备开集群时必须先开仿真，再读取服务端房间列表及说明；申请加入后由已授权管理接口审批，客户端自动知道所在房间并心跳上报基础硬件、仿真 ID、办公 ID（存在时）、名称、版本与能力。能力变更由客户端立即上报，心跳作恢复同步；无 key 也有默认描述，有 key 时 Harness 可以按固定 schema 细化。任何声明能力先按自述/待验证分层，不能据自述直接宣称签名、发布等真实能力通过。

服务端是发现、身份、任务状态和证据索引的枢纽；实际任务由房间内智能体竞标、唯一分配、仿真 ID 点对点协作。验收须能反查发布者 ID、目标设备、投标与分配、租约、每阶段进度、消息引用、结果证据和独立验收。一个任务被 100 台抢时，不是 100 台都执行：按能力可信度、适配、负载、成功率与任务策略决断，唯一任务只发一个有效租约；全员任务为各设备建立独立子任务。设备离线或超时按任务状态机重新分配，避免重复执行。不能用“已发布”“已审批”代替完成验收。

一次入房验收至少记录：时间、原 ID 与主机身份、安装包版本/哈希/签名、实际运行路径与进程、目标房间、申请/审批/激活修订、客户端实时状态、服务端最新心跳、设备描述来源（默认或 Harness）、失败与恢复动作。只在这些证据齐备时报告 PASS；新设备能一分钟入房的前提和超时原因要如实说明。

## 已验证的 132 原位更新成功路径（2026-09-29）

原仿真 ID `1321656264` 当前连接成功后，先确认原进程真正运行于 `/Users/mac/Library/Caches/Vibekits.app`、旧版 dev330、房间已批准且心跳在线。通过仿真上传已签名公证的 Mac dev343 ZIP（420,981,581 B），远端 SHA-256 与源文件 `5fad62a56d8172c576c74d39a2849ed411f66000106eedd467d90a4c16a9b809` 一致。可回滚脚本验证旧/新 Bundle ID、指定签名要求、候选签名和 Gatekeeper，备份原包，再在**同一路径**安装新版。脚本杀旧进程时控制端 SSH 返回 255；独立脚本继续执行，远端结果写出 `PREFLIGHT_OK oldPid=34351 → INSTALLED_VERIFIED → STARTED newPid=44396`。原 ID 重连后查实际进程为 dev343、客户端房间 `roomsAreLive=true`、`acceptedRevision=11`、服务端同 ID/同办公 ID 的心跳年龄约 0.07 秒。此链路证明“自身热替换时桥断开”可自动恢复，不需把安装步骤交给用户；**不能**仅凭 SSH 255 或本地包传输成功判定结果。任务抢单还要单独验 `SIGNED_TASK_CONTEXT_REQUIRED` 门禁。

## 双 App 相互支援的实际恢复顺序（2026-09-29）

房间登记同一设备的 VibeKits 仿真 ID 和 KEMI 远程办公 ID，二者来源是客户端上报并需与可信设备身份复核，不能互算。正常集群任务与软件更新都先走仿真通道。自身热更新可能使仿真断线，此时先读取独立安装任务的结果并重试原 ID；确实无法连通时，才用同机已核对的办公 ID 尝试远程桌面 GUI 恢复，在原交互用户会话启动 VibeKits。办公界面“在线”或“正在连接”不是桌面已接通的证据。原 ID 重连后再分别核对当前进程版本、Harness、房间实时心跳与设备能力同步。58 的办公 ID `238638760` 曾显示在线但连接停在“正在连接”；随后用户在 58 本机手动启动，原仿真 ID `4240650696` 已恢复可连接。因此这次恢复动作应记作用户手动启动，不能声称办公远程操作成功。办公连接密码等凭据不得写入技能或仓库。

这个备援机制只解决通道失联与原用户 App 恢复，不代替设备加入审批、任务签名/分配、完成证据或独立验收。两条通道均不能连时保留已知状态和回滚结果，继续处理其它设备，并列出最小人工介入点。


## 58 dev340 签名覆盖与房间恢复：PASS（2026-09-29）

原 ID `4240650696`、办公 ID `238638760`。签名安装器的独立 Task Scheduler 任务已运行，文件锁由同机旧 App/relay/三个 Harness Node 引起；只关闭已核对路径的五个进程，办公桌面点击安装器 `Try again` 后完成。经办公桌面启动真实安装路径的新 App，清理旧仿真连接缓存并用原 ID 重连，主程序 dev340/build2340、有效签名、目标 SHA、交互 Session 1、安装任务退出码 0、同房间新鲜心跳、名称与双 ID、Harness 设备描述同步均已验证。完整逐步动作与坑点在仿真技能 `references/windows-build-transfer-lessons.md`。此项仅表示 58 dev340 覆盖升级/房间在线 PASS；六机总验收仍未完成，任务分发/领取/协作也未通过真机闭环。


### 2026-09-30 六机同房与 xzl 自动接入

六机房 `f450c684b868292f67c534b793e26314` 实测 6 个批准成员、6 在线、0 离线。xzl/6192992780 在仿真通道升级到已签 dev340 后，`cluster.rooms` 列出可发现房间，`cluster.apply` 返回 pending；管理页审批瞬间显示 5 在线/1 离线，数秒后客户端自动心跳、更新 Harness 描述，变为 6 在线。房间摘要必须可见名称、仿真 ID、客户端自报办公 ID、最后在线；详情须显示来源和真实版本。当前 445 的 Mac 版本仍 dev342，不能将六机在线误写成六机均最新或自动任务完成。详见 hbbv `docs/41_SIX_DEVICE_CLUSTER_IMPLEMENTATION_AND_ACCEPTANCE_2026-09-30.md`。


### 2026-09-30 445 Mac 补齐 dev343 后六机 6/6

445 的 dev342 原位升级以 529 已签/公证 dev343 App 为候选，三端 SHA 一致，先保留 dev342 回滚目录；新 App 真实进程 build2343、原 ID/SSH 指纹不变。更新后页面短暂离线且远端一次 HTTP 422，随后的心跳序列恢复、`roomsAreLive=true` 且 `approved`；01:10 六机页 6 在线/0 离线。四 Mac dev343、两 Windows dev340（当前已签候选），这只通过入房与版本现场门禁，不代表业务任务竞标、自动更新、验收或删除重装 ID 保持。详见 hbbv `docs/41_SIX_DEVICE_CLUSTER_IMPLEMENTATION_AND_ACCEPTANCE_2026-09-30.md`。

## dev344 四台 Mac 同包升级的复用门禁（2026-09-30）

已公证和 `spctl` 通过的包仍可能有 UI 版本错误：首个 dev344 ZIP 的 Info.plist 为 build 2344，但 `lib/app/app_version.dart` 仍是 2343，真实 UI 显示 `dev.344+2343`。修正源码后重新构建、签名、公证；唯一合格候选 SHA-256 为 `1d4f89bc0ab3ae33901c295c2c5b53fca51b75875ac856a41a2c13ffa5602c5d`。下次冻结应同时比较 pubspec、Info.plist、实际 UI 和仿真应用清单；任何一项不一致都不得推送。

四台 Mac 原位覆盖前先用仿真查询**实际运行进程路径**，并核对原 ID、主机指纹、包版本、目标文件哈希和空间。529 运行 `/Applications/Vibekits.app`，132 运行 `~/Library/Caches/Vibekits.app`，445 运行 `~/tools/Vibekits.app`；不能按默认安装路径批量覆盖。每台先保留 dev343 回滚包，再由与旧 App 生命周期独立的脚本替换准确路径、启动新版，并在持久结果文件依序写 `PREFLIGHT_OK`、`INSTALLED_VERIFIED`、`STARTED`。旧 App 退出可能让控制端 SSH 断线；重连**原 ID**后读取结果和实际新 PID/Info.plist，核对同一指纹、MCP/SSH ready、房间在线 approved、描述同步。四台均实测为 `1.9.0.344` / build 2344；本机 Harness 真实模型调用成功。132 的 macOS 12 Intel 目录选择器尚未实测通过，Windows 两台仍旧版，六机业务任务尚未通过，不得把局部成功写成总验收。

“给 ID 一分钟升级”只有远端已经有同哈希签名包、当前通道和安装脚本均就绪时才可能；首次传输约 423 MB 及签名/公证耗时不可省略。可缩短的是预检、哈希复用、准确路径和结果读取，不得省掉签名、回滚、保号与功能门禁。逐机记录见 hbbv `docs/42_CLUSTER_OFFICE_TASK_FLOW_STATUS_2026-09-30.md`。

### 2026-09-30 六机同房与 Windows dev344 交付边界

六机通用房 `f450c684b868292f67c534b793e26314` 可通过 hbbv 管理只读 API 核对 `total=6, online=6, offline=0`，每条都有仿真 ID、办公 ID、设备名和秒级心跳；网页登录默认打开此房间，设备单行右侧绿/灰灯仅表示房间心跳在线。四台 Mac 已运行 dev344+2344，58 `4240650696` 和 xzl `6192992780` 仍运行 dev340+2340 时，也会呈绿灯。故“六机已入房并在线”与“六机已更新同版、Harness 正常、任务自动执行”是不同验收门禁，不能互相替代。58 的 dev344 Windows 构建虽已 exit 0，只有硬件令牌完整签名、同 ID 覆盖安装及房间持续心跳后才可登记升级 PASS；具体源码包遗漏、CMake 首错和 PIN 截图处理见 `vibekits-remote-simulator/references/windows-build-transfer-lessons.md`。

### 2026-09-30 dev345 真实任务与 Mac 覆盖升级门禁

六机房只读广播任务 `5b3fa1319659ca6d0957b90b48fdac2f` 经发布者安装身份 challenge/prove 后，四台 dev344 Mac 自动竞标、接受 offer、claim 并取得签名上下文，却无结果，租约进入 `lease_uncertain`。根因为客户端验证冻结步骤读取 `step['id']`，服务端正式合同字段是 `stepId`；`TASK_CONTEXT_STEP_MISSING` 发生在 `context_issued` 后、真正执行前。修复应同步真实合同夹具/hash，至少跑 `cluster_room_agent`、`cluster_task_protocol`、`cluster_task_ticket_verifier` 三组测试；不能把投标/领取当作任务完成。dev345 修复版已通过 36/36 测试、Mac Universal/macOS 12/Harness 静态门禁、Developer ID 48 个 Mach-O 验签及 Apple 公证 Accepted，公证 ID `46170665-59a0-4531-8145-75235287c88c`；完整业务任务仍需新版重新分发并看结果/审核。

529 Mac 从 dev344 覆盖为 dev345，原仿真 ID、指纹和主进程保留，安装脚本写出 `PREFLIGHT_OK`、`INSTALLED_VERIFIED`、`STARTED`，但房间初次变离线，`cluster.rooms` 报 `No route to host`。系统 ping 到服务器 `192.168.3.65` 成功、51838 TLS 可握手，截图有两个叠放的局域网授权弹窗。用 `vibekits.device.ui_inspect` 指定 `UserNotificationCenter`，确认一个弹窗属于无关 86Box 游戏，另一个明文属于 `Vibekits`，且按钮在 AXWindow 7 的子节点 12；只对 VibeKits 的“允许”按钮操作。随后 `roomsAreLive=true`、`simulationReady=true`，后台同 ID dev345 心跳恢复。不要因另一应用的弹窗而盲点“允许”，也不要把系统授权提示误报成服务器路由故障。新版为何再次触发局域网系统确认需单独回归“旧版已授权→覆盖升级→无需重复授权”；在原因未解决前不能宣称授权延续门禁通过。

132 Mac 覆盖 dev345 后独立脚本也报 `STARTED`，但房间离线、`simulator.call` 超时。本机 `lsof` 发现旧 dev344 二进制从 `upgrade-rollback/dev344-before-dev345-20260930.app` 启动了另一进程，并占用 `127.0.0.1:32147/32148`；新 dev345 主进程存在但不能绑定这两个端口。先用 `lsof -p <PID>` 的 `txt` 实际路径证明旧进程身份，再仅 TERM 该 PID；确认端口释放后重启**原路径** dev345。之后新进程独占两端口、原仿真 ID 的 `cluster.rooms` 返回 live/connected、后台新版本心跳恢复。不要只信独立安装脚本的 `STARTED`，必须查是否有从回滚副本运行的旧 App、端口实际占用者和新版真实 MCP 响应。

58 Windows dev345 从 dev344 隔离源码复制后，Flutter 首次因复制的普通目录 `.plugin_symlinks` 报 `PathExistsException`；只在新副本中将旧目录改名留备份，让 Flutter 重建。随后复制的 `build/windows/x64/CMakeCache.txt` 仍指向 dev344 原路径；同样只在新副本中将旧 `build/windows` 改名留备份，再重建。一次计划任务出现 `^C`、LastTaskResult=`3221225786`，无 Flutter/编译进程残留；保留日志后按同一任务恢复一次，最终固定退出码 0、Release 成功。候选 29,072 文件、224 PE、20 未签、0 无效，原 dev344 源和候选均未覆盖。远程 `ssh_exec` 偶尔在长复制/扫描时返回 255，但原进程可能继续；先查固定产物和进程，不盲目重复复制。dev345 签名必须单独核 20 个待签 PE、本次 SignTool PID 与空 PIN 窗口，再等完整 `PASS`，不能沿用 dev344 的签名结果。

### dev346 六机任务闭环与 TLS 监听故障（2026-09-30）

六机均可竞标却在领取签名 context 后无结果时，先比对**正式成员** `GET /api/v1/agents/rooms` 中的 membership revision、服务端 `members.revision` 和签名 context 中的 `membershipRevision`；不要拿 `cluster.joinMemberships` 的**申请** revision 当成员 revision。本轮申请 revision=2、正式成员 revision=1，dev345 因错用申请版次拒绝任务上下文。dev346 修复后四台 Mac 真实领取只读任务 `2b14d9080bff49643bdede96a53fa105`、通过仿真 ID 发结果消息，管理 API 消息体哈希与实例 `outputHash` 一致，四项均 `accepted` 并积分。445 的消息/结果已经落库但实例进 `reconciling`，按同一结果哈希 `verify_received` 后再审核；不能重新执行设备任务。两台 Windows 的结果仍待新版完成，不得称六机全部通过。

六台设备**同一时间**离线时，先看本机 hbbv 的 LAN `51838` 与管理回环 `51839`；若回环可用而 LAN 请求超时、`sample` 显示 Python SSL 握手线程卡住，不要逐机重装或修改房间。旧 `run_local_https.py` 在监听 socket 的 accept 路径进行 TLS 握手，一个半开连接可阻塞新连接；改为 `do_handshake_on_connect=False` 后受控重启，同一原房间 6/6 心跳恢复，半开 TLS 回归时并行 HTTPS 请求仍返回 200。参考 hbbv `docs/47_DEV346_SIX_DEVICE_ACCEPTANCE_2026-09-30.md`。

### Windows 58 dev346 打包的命令长度与静默等待（2026-09-30）

58 内层 Authenticode 的 `sign-inner-summary.json` 为 224/224 Valid、`sign-inner.status=PASS` 后，才可编译外层 Inno 安装包。仿真 `ssh_exec` 的 `EncodedCommand` **有命令长度上限**：把约 5.5 KiB 的调度脚本直接编码发送会返回 `FormatException: 远程命令为空、过长或包含非法字符`，此时远端脚本完全没有执行，不能从空的 `data` 推断任务已启动。先检查工具最外层 `ok/error`，再检查远端状态文件。短调度命令可由远端读取已校验的脚本内容，在远端生成 UTF-16LE Base64 并登记计划任务，避免把长命令经仿真接口传输。

本轮尝试将 `ISCC.exe` 直接作为计划任务 Action，进程在 Session 1 存活，但 CPU、输出文件长度和最后写入时间持续不变；此时 `Running` 不是进展证据。只停止核对过的 `ISCC` PID 与该计划任务，把约 22 MiB 的未完成包改名保留，再沿用 dev345 成功的 `Package-Vibekits345` 脚本模式：以 `powershell.exe -EncodedCommand` 执行对应 dev346 脚本，日志重定向到 `package-console.log`，状态写 `package.status`。此路径的日志逐文件增长并显示 `Compressing`，说明实际恢复。后续必须等 `package.status=PASS`、包长度/哈希、外层签名 Valid 和同 ID 覆盖安装，不能只看日志增长。

### 六机 dev346 广播任务闭环（2026-09-30）

58 与 xzl 签名包原路径覆盖后，不能只核对安装器退出码；还须以**原仿真 ID**重连，核对主机名/SSH 指纹、实际运行程序的版本与 Authenticode、房间心跳版本及在线时间。2026-09-30 两台 Windows 均满足：58 `4240650696`、xzl `6192992780`，Inno 退出码和计划任务结果均为 0，实际运行 dev346，签名 Valid；同房间六台心跳当时均在 4 秒内。双 ID/名称见 hbbv `docs/48_SIX_DEVICE_ID_DIRECTORY_2026-09-30.md`。

原广播只读任务 `2b14d9080bff49643bdede96a53fa105` 在更新期间超时而 `failed`，两个 Windows 实例 `response_timeout`；保留此失败记录，不改状态或假装成功。重新通过发布者仿真 ID challenge/prove 发布任务 `03f5c9c1b4ebb88fd1fb5f7500a8f8e2`，六台自主竞标、各指派一个实例、自动执行 `vibekits.device.applications` 并向发布 ID 发结果。按每台消息发送者、消息体 SHA-256/实例 outputHash、版本、Mac 的 `path` 或 Windows 的 `installLocation` 验收；六实例 accepted，任务 completed、各加 1 分。清单任务仅证明任务通信和只读执行，不证明 KEMI 远程办公自动更新。全量验收证据见 hbbv `docs/47_DEV346_SIX_DEVICE_ACCEPTANCE_2026-09-30.md`。

### 六机同时心跳失败但 HTTPS GET 仍可返回（2026-09-30）

若六台同时报告 `INTERNAL_ERROR`、客户端 `roomsAreLive=false`，先查本机服务进程 SQLite 文件描述符。2026-09-30 的 hbbv 进程 PID 46478 对数据库的 FD 3/4/5 为 `(revoked)`，但回环 HTTP GET 仍应答，数据库本身 `PRAGMA quick_check=ok`、卷正常挂载；因此网页能打开并不能证明心跳写入可用。受控向该异常进程发 SIGTERM 后，现有 supervisor 自动拉起 PID 71781，新进程 SQLite FD 有效，约 12 秒内原六台心跳年龄恢复到 0–3 秒，132 客户端 `roomsAreLive=true`。不要逐台重装，不要删除数据库；先确认服务自身持有有效数据库句柄、写入恢复和六个原 ID 的最新心跳。此案与 TLS accept 被半开连接阻塞是不同故障，按现场 FD/请求症状区分。

### 2026-10-01 Windows dev368 构建、签名准备与中断恢复

只使用原仿真ID核验设备与主机指纹。控制端同事短暂更新会清空连接表，不代表远端构建失败；恢复后重新connect原ID并读取同一个任务、日志与退出文件，禁止重复启动构建。58本次原生Release及Windows Flutter Release均退出0，实际主程序1.9.0-dev.368+2368；依赖锁中的pub.flutter-io.cn与Windows默认pub.dev不一致导致首次enforce-lockfile失败，使用原缓存与进程级原镜像地址修复，未修改锁或升级依赖。Windows Harness仍旧0.1.7时，需要通过成熟prepare_harness_runtime.ps1准备该候选要求的0.2.0-rc.2及Windows模块，不可复制Mac模块。

复制含近三万运行时文件的候选可能超过SSH观察预算，exit255不能直接判复制失败。本轮远端仍完成复制与签前清单；恢复后真实清单224项、20项未签，先核对目录、进程、文件和hash，不重复解压/复制。PowerShell5把ConvertFrom-Json数组包在@(...)中可能造成count=1；先按真实JSON数组及当前引擎展开检查，不误报文件遗漏。签名在caucy的WTS Active会话1通过固定GUI启动器进行。SSH截图黑屏则使用绑定本次signtool PID的已有受限Session1截图程序；截图实际确认空PIN框后展示给签名人员，仅人员输入PIN。

目前这些是构建与签名准备证据，不是最终签名、覆盖升级或六机长期稳定通过。只保留已验签原App及回滚点，签名未完成不得打包发布。Mac132本次原仿真ID的普通与强制中继均返回transport_failed/Remote desktop is offline，办公372799163界面持续连接且日志实际返回offline；这是通道失败证据，不等于物理电脑关机，不能假装已经访问目标。


### 2026-10-01：硬件令牌输入后，外壳签名仍因时间戳网络失败

不要把 PIN 输入完成、内层签名通过或安装包生成解释为外壳签名成功。此次 dev368 内层 224/224 通过，外壳 SignTool 却报 timestamp server could not be reached or returned invalid response，退出 1，安装包保持原未签 SHA-256。先保留失败日志和未签包，禁止发布/安装，不重复编译。

按 DigiCert 官方排障文档检测 `http://timestamp.digicert.com/timestamp/health/heartbeat`；HEAD 根网址不是有效健康检查。本次 Windows58 DNS 解析官方地址正常，系统默认本机代理转发健康请求返回 502，同机 curl 直连健康请求返回 204，证据指向本机代理路径。不能直接推断 DigiCert 服务整体宕机。

诊断应仅输出代理主机/端口、是否代理、DNS、健康 HTTP 状态，不输出代理账户、认证头、配置令牌。不要删除应用配置或重置证书。沿用原官方时间戳地址、固定 helper、原证书和冻结候选；网络调整只应在已授权范围内精确作用于该域名，并保存原值、处理并发修改、结束时恢复。新进程可能再次要求 PIN；先绑定新 PID、确认活动桌面、展示输入前空框截图，再由人员输入，不能沿用旧窗口证据或代填。

当前记录仅确认故障定位，第二次尝试正在等待令牌输入。签名恢复、代理恢复和安装可用性还未验收，不能将本条称为已经成熟验证的更新成功方案。执行结果以项目 `docs/acceptance/WINDOWS_DEV368_RESUME_2026-10-01.md` 后续证据为准。


## 2026-10-01 Windows 升级前置检查

完整步骤见 [仿真更新排障实录](../../vibekits-remote-simulator/references/windows-update-incidents-20261001.md)。SSH 通不代表 SFTP 可用；外壳签名有效不代表内部临时安装程序已签名。原 ID 心跳、实际运行版本、Harness 本次回复、成员身份和有效任务授权要分别验证；禁止通过删门禁或改策略制造通过结果。


Mac同身份覆盖更新、SSH255结果回查及无Xcode票据处理，见[2026-10-01已验证现场步骤](../../vibekits-remote-simulator/references/mac-atomic-update-lessons-20261001.md)。只使用原仿真ID，区分实际更新、心跳和模型验收。

并行构建导致候选反复变化、进程版本与注册表不一致、仿真可用但反向房间失败时，见[2026-10-02诊断记录](../../vibekits-remote-simulator/references/frozen-candidate-diagnostics-20261002.md)。


## 2026-10-02 房间在线与方向授权分别验收

605新包2428已产生新心跳、默认能力描述和双ID，但控制端入站仿真仍consent_pending；249入站仿真调用成功，而其反向服务端ID未确认，导致roomsAreLive=false、描述pending_sync。先检查哪一方向被谁拦截，不能将房间心跳、服务器注册或单方向仿真作为双向任务通信通过。管理快照的readyCount只按脚本字段计算，不包含签名任务上下文、模型执行、更新安装或长期稳定。

允许按钮触发macOS系统密码验证、办公视频延迟导致误判和文件传输恢复的已验证细节，见[Mac605原位升级与确认排障](../../vibekits-remote-simulator/references/mac-atomic-update-lessons-20261001.md)。待验证项必须保留待验，不能将文档步骤写成已经成功。SIGNED_TASK_CONTEXT_REQUIRED应由正常任务领取取得有效签名上下文解决，不得删除门禁。

## 2026-10-02：仿真可用但 JOIN_CHALLENGE_EXPIRED

58原ID4240650696已运行dev445，SSH/MCP可调用，首次反向授权等待消失后却无法恢复房间，错误JOIN_CHALLENGE_EXPIRED。不要重装、重置名单、删除成员或反复apply；本案已有approved申请，apply明确拒绝重复申请。

最短诊断：通过原ID读取目标UTC，并记录控制端请求起止UTC；对照当前客户端cluster_direct_join.dart的挑战时间条件。本案签名挑战仅容忍issuedAt领先设备时钟5秒、过去60秒，58实读比控制端慢约4–6秒。继续查w32tm /query /status、Get-Service W32Time及既有时间源；本案服务停止0x80070426。授权维护范围内启动原W32Time服务，沿用time.windows.com既有配置，没有换时间源或手工写时钟。首次w32tm /resync仍报无可用时间数据，不能用SSH exit0冒充同步成功；后续stripchart两次偏差约±2毫秒，本机sntp只读偏差约0.196秒，58原申请自动恢复connected/roomsAreLive=true、能力版本accepted。

14:24:30Z服务端独立快照五台真实在线，58心跳1.907秒、原仿真ID和办公238638760保持。此连续证据支持时钟同步方向，但不把首次失败resync写成成功，也不声称经过隔离实验唯一证明因果。若校时仍失败，按实际时间源/网络继续诊断；不能放宽签名有效期、关闭TLS或人工制造在线。最终分别核对客户端实时状态和服务端新心跳。证据：VibeKits docs/acceptance/CLUSTER_DEV443_DELIVERY_2026-10-02.md 22:22/22:24。


## JSON存储启动FD压力与控制端通道复用（2026-10-07经验）

参数从当前目标证据取得，不照搬个人账号、磁盘路径、设备ID或程序版本。先分层记录当前App/SDK PID及创建时间、实际程序路径/版本/签名、原可信指纹、房间实时心跳与原请求。保存第一错误和原历史，平台审批、PIN、新身份/信任及已离线桌面禁止恢复的原边界继续有效。

**启动存储读取。** 真实案例有约8716 JSON历史记录、同次约8717在途readFile，SDK全表/全文件Promise.all的loadAll链引起FD压力，首open锁失败可留下0B文件；空锁是该失败的副产物线索，不能只清锁或用App事后内存判断根因。准确计数差8192不是实际CRT上限证明，也不能据积累数量归责谁创建全部会话。只统计元数据，不读取/输出用户会话内容或凭据。

修复应定位精确父SHA和唯一函数锚点的读取producer：共享已验证的16槽FIFO（其他场景按资源证据选择）、读取全部合法记录/保留顺序与schema、每load局部error/cancel/drain；A失败不能永久poison进程或拖住健康B，grant-before-error不得再开始IO，失败应抛原EMFILE/ENFILE而非成功返回部分表。保留原ENOENT/foreign/unsafe-key语义，不删除旧缓存/历史、切新home或全局丢弃shim来凑通过。未来固定分析会话减少随机扩散，但旧合法记录仍需安全读取。source/合成9000负控与真实目标启动分别验收。

**启动与模型分开。** startupReady/webAnnounced只证明初始化，不证明模型回答。真实402/QUOTA/insufficient_balance需要用户原账户额度或明确可用模型的动作；不复制Key、自动充值、不重发同一失败请求或降低合同requiresModel/Agent。记录真实消息/turn终态及原因；临时SDK补丁或恢复MCP不等于正式签名整包合格。

**先恢复控制端。** cached ready不代表实际MCP/SSH健康。App与SDK仍为同PID/寿命、cloud新鲜且既有同机办公通道正常时，先查控制端bridge和原会话；确认无在途写/安装/签名/Job后，对原ID/原FP做一次控制端断开重连并实际只读复验。不要为一次60秒SSH255或MCP timeout远端停SDK、重复安装或判物理离线。未取到样本只能记失败；优先<=15秒短批，超时对账原句柄，不能把采样说成采样间连续在线或一分钟稳定。

CIM创建时间微秒与GetProcess的100ns末位精度可不同；寿命fence按同API、同精度、同UTC表达比较，同时核PID/路径/签名，不以格式末位差判换进程。已无活跃的旧PID不继续等待；观察超时不是事务已终止。资源报告区分private/working set/commit、handles、累计CPU秒与CPU百分比；加载后增长需分段及释放证据，既不立即判leak也不立即判stable。

本经验未证明正式561发布、七台/100台协作、真实模型与长期资源门禁完成；按当前目标继续补未验项，不能缩成基础在线PASS。

## 561原身份升级、直接D传输与自动验收（2026-10-07实证）

以下是已授权目标的成熟方法，不扩大设备、路径、账户或权限范围。参数从当前可信登记与实际进程取得，不照搬某台机器的ID/PID/盘符。58与617正式561分别取得实际版本/主SHA、原ID/指纹、只读MCP、94B往返、实时approved入房与升级guard verified_committed；这只证明对应覆盖升级的基础通信，不证明模型生成、业务消息ACK、评分或长期稳定。

**传输接口缺口。** 公开simulator.upload_file只有localPath、没有remotePath时，不编造参数，也不在用户禁止的C盘先暂存。已验证的同Vibe fallback沿当前授权loopback SSH/SFTP carrier和已登记known_hosts，以StrictHostKeyChecking=yes/原FP/原用户验证，直接写允许D目标。私钥仅作为原identityFile路径引用供原认证引擎使用，不读取、复制或上传key内容，不新建信任或服务。先94B同目标往返，再单次完整传输，核目标bytes/SHA/签名/时间戳；传输失败保留部分字节和原句柄，对账后再判断可续传，不盲重复。实际617包259791104B/SHA2D25CE8B20CBE24BB51A55D8F77021F060AC9F91D3A6EF17436B43776CB2943C。可参考私有项目tool/windows/dev561-original617-20261007/transfer_qualified561_existing_vibe_sftp.py；脚本固定设备参数须按原目标证据投影，不能直接执行到其他机器。

**长路径完整回退。** WindowsPS5在copy后的Get-Item/hash遇260字符路径失败，不能丢弃已有副本、跳过长路径文件或称全部备份完成。617保留失败和copy后，验证实际bundled Node版本/来源SHA/签名，以Node串行1MiB流校验原source与backup完整pathset、每文件bytes/SHA及总数，拒reparse；31921项真实PASS后才进入安装。读取只有程序包内容/metadata，不用户聊天或凭据。使用现有Verify-Original617-Backup561-v2.mjs路线，不以更改ExecutionPolicy、递归清理、换home或无限并发解决。观察timeout不等于copy事务终态。

**角色与外部owner。** 查实际App、原外部终端和worker的token elevation/integrity、当前用户/SID与Active Session，普通Limited/High不猜。617实际Medium/非elevated，应继承Limited；58当前原管理角色按实际High身份执行。独立Interactive任务的祖先必须脱离App/relay Job，绑定唯一任务名、脚本SHA、原PID+同API创建时刻；禁止namekill、擅自升权或执行策略覆盖。新完整backup必须真实独立：守护回退Move-Item会消费旧backup，不能拿旧manifest冒充仍存在的副本。失败守护终态不得重启或延长；新必要重试须独立attempt/回执，保留旧失败证据。

**自动观察先于升级。** 安装前先启动控制器，确认observer进程存活且trusted_cloud_observer_ready已落盘。早期armed记录不足：ready须原保存profile/pin、serverUUID、时钟与approved成员首读成功。独立云只读等新版本且heartbeat新鲜、last_seen严格晚于本次安装请求时点，才一次原IDconnect，观察预算60秒。超时但操作可能完成时只读同connection_status，不重放connect；身份变化停止、不接受新信任。实际WindowsISO7位fraction在Python3.9先保守截至6位并处理明确时区，同PID寿命比较使用同API精度。

验证器逐项实时持久化原身份、实际version/mainSHA/签名、只读MCP、94B往返、原批准room/installationKey与云新鲜心跳。按实际guard waiting更新时间+600秒裁剪所有阶段预算，保留ACK及确认余量；剩余不足严格拒ACK，不续守护。58前两次因验证器残留560、30秒观察迟于35秒完成、7位时间解析与人工延迟失败，守护恢复原560；这些不能当561房间回归。第三次自动观察路线实际basic committed。升级commit ACK不是业务任务消息ACK。

公共服务签名key/TLS补齐需沿同serverUUID/原公共keyId与可信证书材料，不能读服务私钥或改身份。58/617已同原服务补齐且原安装key保持；SIGNED_TASK_CONTEXT_REQUIRED仍需真实冻结合同/分配/租约/permit，不人为改flag授业务权限。资源样本与能力声明也不等于当前可签名任务许可。模型provider402/QUOTA需原账户必要动作，不能自动换key、充值或重复模型请求。Mac561仅本地签名、未获公证/部署证明；七台全模型/协作/100台长期目标仍未通过。


## 资源节约、同任务恢复与升级经验（2026-10-08）

先复用仍有效的源/包hash与实际目标证据，不重复全量catalog、创建分析会话、编译或签名。诊断使用有界小批/流式原始文本DTO及owned进程预算；PS5 Get-Content装饰对象深JSON可能扩张，不完整捕获后才截断。编译/签名/备份需其任务预算与独立外部owner，不能套短诊断期限；内层工具成功而supervisor壁限失败时分别报告，不虚称整个任务成功。

维护观察timeout先查同一attempt/进程创建时间/阶段回执，不重发升级、connect或签名。已验证连接可能35秒才完成，单次connect以实际成熟60秒观察及status对账；在安装前observer必须原profile/UUID/FP/approved房间trustedready且live，按真实guardian期限保留ACK余量，不续守护。Python3.9读取PS七位fraction先保守到微秒并处理UTC；寿命以同API精度，不按路径名/CPU快照判进程身份。

保持原Bundle/Team/完整DR/entitlements、设备ID/FP、登录/凭据/TCC、房间身份与用户历史，正常覆盖/失败完整回退。公证/签名仅是包门禁，scheduled不是安装成功。Mac旧更新器可能拒__MACOSX，已签公证App仅做唯一App根兼容封包，独立票据/签名/GK/hash后走原校验，不热改App或绕校验。多实例端口占用查实际加载EXE（lsof txt）与父子关系；正常退出已证属于本次的旧实例，不namekill、不据时间猜谁启动。

无目标模型/欠费不使原仿真和房间资源失效：管理agent可在原授权内用确定性CPU/编译/签名工具；目标agent推理与资源任务从合同创建时明确两mode，不静默降低requiresModel、签名租约/permit。模型402不自动充值/复制Key/每poll重发。已过期任务在server discovery与client模型前拒绝；固定分析会话仍可能同会话无限错误重试，应核自动调用数，不只会话数/UI单次failed。typed provider QUOTA/401/402/403需停止该上下文自动请求，临时错误用已验证scope/上限/冷却；普通capability变动不能绕过。恢复按明确模型/key/runtime或正常配置动作，对结果按contract/step/generation对账，不复用过期租约。此项是已审源码修复；新正式包实机回归未证不称普遍部署。

普通确认只在原授权、精确目标/程序/同请求核对且工具允许时完成；PIN/密码/新信任/身份变化与平台强制审批保留。拒绝后不换路做同一拒绝动作；不批量批准不明或重复请求。在线原同机备用办公路径可恢复原开关，已离线桌面仍按用户要求不尝试。恢复后真实原ID MCP/SSH/实时房间逐层验证，cachedready不等可用；短资源采样不证明连续在线或长期稳定。源码/当前包/每机P0与100台业务验收各自记范围。
