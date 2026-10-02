# 六机集群换网事故分析与突发处理

日期：2026-09-30。范围：四台Mac、两台Windows；房间 f450c684b868292f67c534b793e26314。本文记录已验证事实、原因和待研发项，不能作为全量验收通过证明。

## 结论与实际影响

最后一次六机并行实测，1321656264、1554650784、4456560334、5298938227、4240650696、6192992780 全部 connect成功并完成 cluster.rooms实际调用。只有本机和605的 roomsAreLive=true，其余四台的集群接入失败。故“全部设备离线”不成立；集群网页心跳失联也不能表示仿真不可用。

软件安装不依赖设备固定IP：本次58仍可经4240650696上传UI检查脚本、启动只读登录桌面检查任务、取回截图。xzl也已通过6192992780处理普通结果提示。仿真ID应是远程操作入口。

## 原因一：集群数据通道没有继承仿真ID路由能力

当前cluster_room_agent.dart用HttpClient.openUrl直接请求配置的HTTPS origin。仿真经P2P/relay按ID连接，两者是独立通道。仿真成功不会自动让目标设备访问位于另一私有网段的HTTPS服务器。当前产品尚未实现集群经服务设备ID自动建立认证传输或可验证的地址发现，不能将设想描述成现成功能。

本机实际地址从192.168.3.65变成192.168.1.140，旧192.168.3.65已不在本机接口。132到新地址的路由仍经192.168.3.1；605经192.168.1.1访问旧地址超时。此证据证明旧接入地址失效及网段变化，尚不能单独确认路由器ACL或具体丢包设备，不应臆断“防火墙坏了”。

## 原因二：服务绑定失败后的清理死锁

run_local_https.py先构造127.0.0.1监听，再构造固定旧LAN地址监听，全部绑定完成后才启动serve_forever。旧LAN地址不存在时第二绑定抛OSError Errno49；finally却对未启动serve_forever的第一个Server调用shutdown。shutdown等待服务循环退出，因此留下仅本机端口监听、实际不处理请求的假象。

实际旧进程PID1251仅监听51839，无51838。已修复为记录started_servers，只对已启动服务shutdown，未启动监听仅close。保持原数据库、签名密钥、CA、TLS私钥；重载专用服务后，本机与新LAN HTTPS返回200且证书严格验证通过。该修复解决清理死锁，不等于实现自动换网恢复。

## 原因三：我的临时DNS替代方案验收不充分

我将客户端配置改为newlinkdemac-mini.local，并补同CA的DNS/IP SAN证书，原设备与服务密钥未变化。605能解析、TCP可达；但只验证605不足以推广到所有平台和网段。后续真实结果：58/xzl返回Failed host lookup(errno11001)，132/445请求超时。`.local`依赖局域网名称发现，不能当公网跨网统一入口。

初次请求还返回HOST_INVALID，因为服务Host白名单未包含新DNS authority。已加精确--public-host白名单并部署；没有去掉Host验证、接受任意Host或忽略TLS。随后本机与605实时入房恢复，其余四机尚未恢复。不得通过写hosts文件、关闭证书验证或伪造在线掩盖问题。

## 原因四：控制端旧桥文件与当前候选进程不一致

invoke.rb默认读取正式数据目录下tool-bridge.json。同事运行的候选使用隔离VIBEKITS_DATA_HOME，正式目录桥文件可能指向已退出PID及旧loopback端口。本次50077、61942等返回ECONNREFUSED；当前候选另有实际监听，核验当前PID、隔离数据根、桥processId与监听后调用成功。候选再次退出时该桥也随之失效。

这与远端网络及远端授权是不同问题。修复时不能停止同事候选、输出完整环境或token。尝试加入显式桥路径支持曾实测成功，但共享invoke.rb后被另一写入恢复为原默认实现；当前不能宣称它仍支持该参数。必须检查当前源码和实际进程。不得将旧桥失败报告为六台设备都不在线。

## 已完成与待完成

### 后续代码修正与复核

正式技能脚本invoke.rb现通过simulator_bridge_locator.rb发现当前进程拥有的live loopback桥：核验文件属主/权限、App进程PID、桥processId、loopback URL、token存在与实际监听。默认桥失效后仅从当前App显式数据根寻找；APFS的Mcp/mcp按inode去重；多个不同live桥明确报控制端歧义，不称远端离线。不会在请求可能已执行后重复副作用。代码副本保存于VibeKits tool目录。

用修复后的正式脚本，无临时端口脚本，六个原ID全部connect成功、可信指纹一致，并完成device.applications实际查询。此结果证实本机旧桥误用已修复。

另外，harness_simulator_controller.dart将连接超时误归target_offline，现改为transport_timeout，并对连接阶段超时自动一次forceRelay重试；授权/身份失败及已经forceRelay的失败不重复重试。增加真实假传输回归验证失败隧道清理和中继成功。该客户端源码变化尚未编译、签名或分发，不能宣称六机已装这个修复。

已完成：六个原ID实际仿真调用；绑定失败清理修复；保留原数据库和密钥恢复HTTPS；精确Host白名单；605与本机实时房间；两Windows传书主界面证据；排障流程写入技能。

待完成：六机统一可达的服务入口；服务换网自动恢复；工具桥运行实例发现与共享变更协调；所有设备最新版一致性与授权延续；智能体远程办公自更新、双向沟通、完整账本与独立验收。官方市场当前Mac383、Windows384，六机对应已装相同build，不能用重装或降级伪称新版升级。

## 后续突发处理流程

1. 冻结原六机ID、服务ID、房间、安装身份与既有任务；不重建数据库、不换ID、不批量重装。
2. 检查发起端桥：当前主进程、其数据根、桥文件processId、实际loopback监听；只打印脱敏必要字段。若旧桥失效，先恢复/定位当前桥，不能判远端离线。
3. 每台经原ID connect并验证可信指纹，再做一个只读实际调用。分别记录simulationConnected、remoteCallSucceeded、clusterConnected、heartbeatFresh、agentReady，禁止合并成一个在线布尔值。
4. 仿真可用但集群失败：通过ID读取cluster状态、HTTPS错误、必要路由与服务日志；设备IP只是诊断数据，不成为操作地址。
5. 服务端检查真实监听及请求响应；端口LISTEN不足以证明健康。绑定失败要完整close，快速失败让监督进程可重试；网络变更后要重新选择有效监听并匹配TLS/Host白名单。
6. 优先采用所有设备可验证访问的稳定HTTPS服务域名；本地验收若采用服务设备ID隧道/发现，则必须实现认证、原服务密钥校验及端口/生命周期管理后再使用。两种方案不能仅靠修改文档假称上线。
7. 服务地址变化通过原仿真ID同步到客户端，保留原身份、CA/签名信任、房间及配置；逐平台先验证，禁止未测Windows就全量迁移。
8. 客户端房间实时读取与服务端新鲜心跳双向核验，再对账任务合同、租约fence、操作回执与消息ACK；失联期间不得重复副作用。
9. 仍无法通信时，用已核验属于同机的办公ID作备用检查；不把备用通道可见当仿真或集群已恢复。
10. 最终截图/接口回执确认实际可用，记录恢复时间和未验证事项，才进入任务验收。

## 必须新增的换网验收

- A网络正常运行 → 服务电脑切B网络 → 六台仍通过原仿真ID调用；集群应自动恢复或明确进入降级并提供可执行恢复路径，禁止假在线。
- LAN绑定失败：无残留假健康监听、无shutdown死锁，监督进程可恢复。
- Mac/Windows、同网/跨网分别验证解析、TLS、Host、认证及心跳；稳定名称需实测全部目标，不凭单机成功推广。
- 正式App/隔离候选切换：定位当前桥、旧文件不误用；不打断并行开发。
- 换网期间已有任务不重复领取/执行；恢复后消息去重、租约对账、完整记录可查。
- 保留原设备ID、公钥、房间、办公ID与原授权；不能将重建身份当恢复。

这些门槛尚未全部通过，需逐项补研发与真实故障注入验收。


## 原生构建必须复现成熟参数（2026-09-30）

本次集群 HTTPS 仿真载体的独立冻结源码构建，先因缺少 CMake 路径、继而因 CMake 4 旧源码策略兼容、最终因遗漏 `CARGO_PROFILE_RELEASE_PANIC=unwind` 而失败。准确错误由 `kemi_p2p_portmap.rs` 的编译保护给出。应核对原项目 `res/build-kemi-developer-id-macos.sh`，使用现有 `res/kemi-cmake-compat.sh` 包装器和 unwind 参数；不能安装另一工具链、删保护或凭一次失败放弃成熟路线。

补齐参数后 ARM release 构建成功，实际无参数入口返回缺少命令及退出码 2，未启动或替换运行客户端。Intel 同源码构建仍进行中。单架构编译成功不等于 Universal 整包、签名、授权延续、ID 载体实测或六机实时入房通过。按现有 `prepare_rustdesk_harness_relay_macos.sh` 双架构与协议门禁验证后再更新设备。

构建有活跃句柄或编译进程时继续观察；观察超时不能视作终止。只有明确退出码及具体错误才能修正重试。共享源码与同事改动保留，冻结编译目录独立，保留原身份及认证。


## 签名候选并行验收与公证配置（2026-10-01）

实际 dev357 候选验证：原 Developer ID Team26T5WV4GLP签名通过44个Mach-O；Universal macOS12+资源检查通过；隔离工具桥通过仿真ID5298938227连接并执行远端只读应用查询，内外层ok均成功。不是六机更新或集群任务验收通过。

1. 独立候选复制排除源码根目录 `.tmp`、`.runtime-cache`、`.codex-artifacts`、`bin`、`dist`、构建和Git目录；保留npm包内实际需要的build/dist资源，不能全局同名排除。只清理本任务误复制的候选副本，不删正式包、共享缓存或同事目录。
2. 使用原正常CocoaPods环境；额外缩窄GEM_HOME/GEM_PATH会造成Flutter误报CocoaPods broken。先直接核验原pod版本，本次1.17.0正常，撤掉错误覆盖即进入编译，不重装依赖。
3. `VIBEKITS_LOCAL_ACCEPTANCE=1`和独立DATA_HOME用于并行启动，仍可能同机32148端口被原App占用。不得把工具桥可用当作仿真目标成功，不为候选测试擅自退出原App。
4. 状态IPC从TMPDIR生成vkh/v1.sock，macOS路径必须少于104字节。DATA_HOME短不代表TMPDIR短；本次短外盘TMPDIR解决路径错误，实际socket权限0600。只退出并重启自己的已核验候选PID，不改正式实例。
5. 公证旧文档profile vibekits-notary不存在，现有成功恢复记录明确正确配置KEMI_NOTARY。只读history验证成功后复用，不索取或输出秘密。使用同一固定签名归档submit并等待；无最终输出但句柄活跃不能重复提交，也不能宣称Accepted。Accepted后仍须staple/validate、Gatekeeper、最终归档及覆盖后原ID/权限/心跳验证。

### 2026-10-01 Mac605 升级后的实时与 Harness 复验

通过原仿真 ID 5298938227 再次连接，connected/transportReady/sshReady/mcpReady 均 true，主机及既有 SSH 指纹一致。客户端 cluster.rooms 内外层均成功，roomsAreLive/connected/simulationReady/clusterAvailable 均 true；六机通用房 membership=approved，办公 ID 415501605，profileRevision=acceptedRevision=5，默认描述显示 dev357 且 reported。此项证明该设备升级后身份、仿真和房间读取保持；不等于六机全部通过。

进一步使用原工具合同提交零工具只读响应指令，requestId=cluster-upgrade-605-dev357-readonly-20261001，真实会话 session-864b3641-edf5-4b4b-b1d0-ec3723ab3769 返回 accepted，随后 session_status=failed。增量历史确认具体失败为 MISSING_CREDENTIAL：当前 deepseek-official/deepseek-flash 路由没有可用 API key。未读取、复制或重置任何密钥，尚未证明这是升级造成凭据丢失；需要对照旧版原有模型选择和凭据服务的可用状态。accepted 回执、Node 进程和工具服务可用不能作为大模型可用证据。无有效模型时默认描述是正确降级，不能声称详细 Harness 描述已完成；intelligentDescriptionPending=true 也不是模型验证成功。

本机实际运行的是 dev357-archived-menu-20260930/resigned-candidate，PID 52473。其签名后 relay SHA-256 为 29142e531956e74c94fa0aeea0002b8e00a1865ac1ba924bcce90e11b5b8ed49；本任务 dev357-cluster-id-route 候选签名后 relay 为 bb379e8e2445bdfe6e8b81800b9789f5e1ef9d3b3dd2cf768b412566f40064ef。两者不能仅凭同一 dev357 版本号当作相同产物，也不能由哈希不同直接断言协议不支持。接收端固定 51839 能力仍需真实 ID 路由验收；不得覆盖正在被同事使用的候选或宣称路由已经通过。

### 首次 ID 路由超时与恢复（2026-10-01）

对 Mac605 保留同一 HTTPS origin 后设置 serverSimulationId=1554650784。省略公开 CA/签名公钥时回执意外报告两个 has 字段均 false，未按预期保留信任；具体原因尚未确定，不应擅自归因凭据丢失。立即使用本服务已有公开 CA 和从既有签名身份导出的公共键恢复；公共键 DER SHA-256 与此前 serverKeyId 3e20c4cb72f38873d078e82ea46f76891ebbce2203b2d2e740663b4d03c866a5 一致，未生成新密钥或修改设备身份。

显式提供原公开信任后 ID 路由首次实测失败：HTTP openUrl 外层 6 秒先超时，roomsAreLive/connected=false，而仿真仍 ready。源码显示内部 connect 允许 direct/relay 各45秒，随后固定51839隧道 direct/relay各20秒，现有6秒外层无法覆盖首次建立阶段。只修改共享源码 cluster_room_agent.dart 的首次 ID HTTP 建立预算为150秒；已有隧道和直接 HTTPS 保持6秒，未放宽TLS/Host/任务认证或增加任意端口。此修正尚未重新打包和部署，不能宣称 ID 接入已成功。

测试后将 Mac605 恢复 serverSimulationId 空值及原公开信任。实际再次 cluster.rooms 内外层成功，roomsAreLive/connected/simulationReady=true。后续接收端载体与新超时包需一并真实验收；本次失败不能仅归因远端离线或接收端旧版。

### 同源增量构建与 Windows 准备复用（2026-10-01）

共享源码有新改动时，不以旧载体已有签名推断同源。按保留的1070项原生哈希清单核验；六项不同先保存旧输入，再同步当前差异到本任务冻结构建目录，原manifest不覆盖。保持已成功的CMake兼容包装器、panic=unwind、离线锁文件、VCPKG及独立target参数，ARM/Intel本次分别2m57s/2m38s完成，合并bfdb856b4a23e20119baa94844ad01c2ce4afe20c154a6d88eb33d12476cf768。1070项再次对照无差异后，保存共享旧载体，运行原prepare脚本同步共享打包输入。此动作不重启运行中的App；真正接收端仍须部署验收。

Mac候选冻结复用APFS克隆和根锚定rsync排除项，保留旧Accepted包，不重复探索工具链。构建签名保持正常HOME，隔离DATA_HOME及短TMPDIR。dev360完整构建、44个Mach-O签名、Universal/macOS12+兼容、实际内置技能及私有工具桥只读调用通过，但并行正式App占32148时隔离候选仿真目标会报端口占用；不能拿工具桥ready代替接收端ready，更不能杀同事实例抢端口。

58原ID可连接时，先只读核验原指纹、D容量、活动构建和成熟wrapper内容。本次原路径Build-Vibekits346-20260930.cmd使用Flutter3.41.9-clean、D盘Pub/TEMP和既有source\vibekits-dev345-six-device-20260930\source缓存；保持Release --no-pub及完整输出组装/内层→外层签名顺序。源目录名字不代表编译版本。读取PowerShell Get-Content输出时先[string]::Join成普通字符串再ConvertTo-Json，避免带ETS扩展属性的字符串展开大量FileSystem元数据。只修序列化，不因此执行或重做脚本。

本次约20.6MB/940文件源码包向58的仿真上传被自动审批明确拒绝，需要具体源码外发授权。传输未发生，已向用户请求指定文件与目标ID的最小授权；不能经另一通道/Git拉取规避同一拒绝，不能把普通安装授权伪称已满足具体审核。Mac构建等不受影响部分继续。该约束属于现场工具审批，不是设备离线或仿真协议失败。

空间不足时先冻结本任务精确可再生缓存清单并核验cargo/rustc均结束、源清单和新旧产物留存；本次仅删除2934个本任务.rlib/.rmeta，实际回收2.69GiB。不得按目录名删除源码、测试报告、正式包或其他人的target；后续重编会重建这些缓存。


### 已公证候选归档与传输等待（2026-10-01）

dev360同一公证提交最终Accepted，票据staple/validate与Gatekeeper通过后再用原ditto归档。正式ZIP SHA256 `27ba60e839fa2ec6cd7cf5488291ba2809c91bf8ece1ad2189e33efe6461a531`，412044122字节。通过Mac605原ID5298938227上传时，控制端句柄10211存活，远端目标文件长度117242880字节，原App PID83164仍运行；这证明传输正在进行，不能重启上传，也不能当作已安装。独立handoff沿用dev357成功脚本，仅冻结现场旧build2357/PID83164、新build2360及单独回滚目录；新脚本SHA256 `d1a26eda6a876a8c405952047d6b76c4110b13fe48b9db49c6492b53c200e75b`，bash语法核验通过。传完后先三端哈希和签名、空间、独立任务、旧进程精确核验，再原位替换、原ID重连、真实进程版本与房间心跳检查。


### Mac605实际dev360升级复核

独立LaunchAgent运行一次exit0，STARTED PID91828/build2360。覆盖前保存旧2357回滚，后重新连接原ID5298938227、原SSH指纹一致、SSH/MCP ready。实际/Applications/Vibekits.app新版进程，已签原生载体hash与发布包相同。客户端roomsAreLive/connected/simulationReady均true、六机房approved、名称/办公ID415501605未变；后台版本dev360/profileRevision5，默认描述已实时同步。不能把默认描述或通信成功当作模型key/智能任务通过。

准备命令SSH255时核实真实目录/进程，解压已完整，分步验签与Gatekeeper成功后继续；禁止盲目重复上传。launchctl正确系统路径是/bin/launchctl，错误/usr/bin/launchctl返回127时任务根本未启动；只在明确未执行后修正同一任务。独立脚本准确冻结旧PID、版本、路径及回滚目录；安装后断开旧缓存连接，再用原ID重建并取真实进程、客户端和数据库三方证据。


### Mac445旧relay移至废纸篓后仍存活（2026-10-01，恢复未完成）

升级后App56359/dev360已运行，但仿真ready=false、集群暂停。pgrep旧relay PID28005命令行仍/Users/mac/Downloads/Vibekits.app，lsof实际txt则/Users/mac/.Trash/Vibekits 15.01.47.app/Contents/MacOS/vibekits-harness-relay，原Downloads包已不存在；32147/32148由新App占用。原生connections返回simulatorAccessEnabled=false，使用既定setter1仍false，不能只凭ok=true认定门禁设置成功。以原成熟LaunchAgent方式启动一次独立恢复：验当前签名、精确核旧PID实际txt路径、TERM该PID、启动当前包的relay并记录日志。启动后原ID返回offline，未重复任务；对照Mac605仍可连接，控制端dev360本机自身也ready=false。Mac445恢复日志暂无法从仿真取得，故不能填恢复PASS。按已授权同机办公ID24955106尝试备援，界面操作尚未取得正确目标桌面，未操作任何未核实远端。后续必须读独立relay-recovery.log、核对真实服务注册ID及原指纹，再完成原ID和集群恢复。


### 控制桥冷启动间隙的多任务冲突（2026-10-01）

同事追溯PAD调试任务在冷启动桥间隙open正式/Applications/Vibekits.app，PID32992启动02:55:56；dev360候选PID33396启动02:56:10。lsof32147/32148均属于32992，不能仅看候选App存在就判定候选仿真门禁通过。成熟project simulator_invoke/locator只定位live bridge，没有自动拉起App代码，不能误归因调用器。跨任务需在安全边界协调正常退出，不能杀另任务正在用的服务。临时明确 VIBEKITS_TOOL_BRIDGE_FILE=/Volumes/ORICO/kemi-build-cache/v354qa/mcp/tool-bridge.json 定位候选桥；这只避免控制HTTP桥混用，不证明固定MCP端口冲突已修好。通过候选桥445仍offline，529可连，尚需目标独立恢复日志。

远程办公備援界面字段正确显示24955106，但窗口反复显示415501605，未核实正确桌面前不得在远端操作。自动审核拒绝过期AX索引及未核实坐标，先重新读完整AX再操作已确认控件；仍不能建立正确桌面时不得绕过审批或声称点击成功。已请求目标机提供不含凭据的relay-recovery.log末尾状态，以定位剩余卡点；源码、旧包和恢复结果保留。


### 源码门禁假成功修复与27项回归（2026-10-01）

现场SetSimulatorAccess(true)曾返回ok=true却simulatorAccessEnabled=false。RustDeskHarnessShareService.setSimulatorAccess原先只检ok，现已新增：响应含simulatorAccessEnabled时必须与请求enabled严格一致，否则SIMULATOR_GATE_UPDATE_NOT_APPLIED；旧版本缺字段保留已有兼容路径，不开启新权限。新增回归同时验证开启返回false、关闭返回true均拒绝。首轮夹具缺state/connections，被正式解析器拒绝；仅补齐真实合同字段，不放宽解析器。沿用独立tests目录、共享源码symlink和原缓存运行同一rustdesk_harness_share_service_test，27/27 PASS，退出0。此改动在共享源码，尚未进入已签dev360，不得将单元回归写成远端恢复。

当前候选本机phase=error，32148 Address already in use，lsof固定端口属于旧/Applications PID32992，候选33396，未强停其他调试任务。明确桥路径仅避免管理桥混用，不解决固定端口争用。Mac445恢复与真实六机任务仍未通过。


### 2026-10-01 现场续验：控制端切换、Windows输入和Mac445备援

本机旧App与候选同时运行时，固定32147/32148属于旧实例；只指定QA桥并不能证明入站载体更新。安全边界协调退出旧实例后，dev360单独监听，仍需恢复旧IPC relay。精确停止获批后，原ID1554650784 ready，132独立反向connect与runtime.status实际成功。切换会清掉其他ID连接缓存：58下一次not_connected须重新connect；重新原ID4240650696实测成功、指纹不变，不要把缓存丢失报成设备离线。

58 dev360冻结940项Flutter/Harness输入和1070项原生输入已分别传输，原生逐项SHA校验通过且含127.0.0.1:51839。Flutter输入包不含Windows原生载体，不能只编译界面便填全部PASS。历史默认RustDesk源码及dev336-fresh缓存已清理不存在；现场应查成熟wrapper和实际目录。本次查到独立dev336 rustdesk-client输入与dev332缓存，正在运行的另一个cargo属于Office Store，不得中断或覆盖。低于6GB空闲内存的原生启动门禁确实阻止了启动；未改阈值冒险并发。

58默认PowerShell Restricted拒绝已核验准备PS1，原源码未覆盖。保留错误和脚本SHA；不使用Bypass、Invoke-Expression或其它手段绕过同一拒绝。已请求仅当前构建进程RemoteSigned的具体决定，未获决定前不执行该脚本。源码同步脚本每项输入先验SHA、相对路径拒绝穿越、旧文件先备份并验SHA，产物与原始版本独立记录。

Mac445原仿真通道不可达时，使用已记录同机办公ID24955106备援。CUA完整AX、实际路径绑定、取消悬挂Window菜单后，主页输入字段的当前值确认24955106，再点击连接；最终窗口标题24955106@macdemac-mini.local且实际桌面dev360可见，才算建立正确目标。不能把旧605窗口当目标。备援桌面发现新vibekits-harness本地网络权限弹窗；尚未确认允许或验收原ID恢复。跨App数据访问属于额外能力，不因任务更新默认扩大。新权限必须与原有授权延续验收分开，记录归因与实际后果，不能把安装版本正确写成可直接使用PASS。

## 2026-10-01：仿真正常但集群 ID 服务通道超时

先查询原仿真ID注册状态和真实工具结果，不把房间超时误报设备离线。此次132的SSH/MCP正常，集群51839在20秒超时。原生转发只在本地客户端连接后启动远端握手；集群先等ready再连接端口造成互等。共享源码已改为先建立无负载本地bootstrap socket，再等待native-ready，finally关闭探测socket，真实HTTPS仍校验原域名/CA/Host。真实本地Socket测试和28项隧道、10项控制器回归通过；尚未签名分发和六机实测，不可宣称已恢复。后续同事须核对运行包包含修复。

58本次原生任务终止101，libsamplerate-sys 0.1.12在MSVC查找out\build\Release，Ninja却输出out\build\samplerate.lib。读取build.rs和实际输出确认后，将本次生成库复制至声明目录，前后SHA256均b51025de5ed5284a58f6531bc5d6720c1678b9da2a0d8ef33da2384ca64570bc；保留失败日志、确认无Cargo再重启原任务。当前Cargo11704实际运行，不能将旧101结果文件或调度Running当本轮测试结论。不替换依赖版本，不用历史二进制冒充新产物。

### 132真实验证补证（2026-10-01）

用当前包内Node/native helper和只读tool/cluster_id_https_demand_probe.js按“先local socket需求、再native-ready、再真实TLS”执行。仅连接服务仿真ID1554650784的固定127.0.0.1:51839，原公开CA、SNI newlinkdemac-mini.local及Host保留，132返回tlsAuthorized=true、HTTP/1.0 200 OK、退出0；无固定设备IP、无证书绕过、无认证凭据。探测会回收仅自己创建的socket/native进程。证明载体和TLS服务可用，仍不能替代安装修复包后的房间实时心跳。诊断脚本SHA256 549de910b2ebb71d722733c879d1684121724d10fdb3fea9ec18ed329f911bb6。

## 2026-10-01：大文件传输中断必须查实，不重复安装

605经原ID5298938227上传395751136字节正式365 ZIP，出现sftp_upload_failed/remote host closed，随后not_connected。控制端App12789及桥PID未变，目标旧360 PID91828仍存活，目标部分文件33945600字节，无安装副作用。对方同事确认未切控制端或disconnect529，根因尚未证实，不能归责、称设备关机或宣称已修复。按原ID重连、核对同指纹和旧包，创建deep-strict通过的APFS回滚副本；等待其他传输结束和明确切换窗口后才重传，完整大小/hash前不换包。共享会话不能因临时调用的finally关闭其他调用正在用的会话；该并发风险仍需真实调用日志或回归证明，不把猜测写成事故根因。

58原生11项实际10pass/1fail：授权门禁测试未显式打开默认false开关，且其他并行测试改同一个AtomicBool。仅cfg(test)加状态互斥、明确开关前置及关闭负例，与冻结输入比较生产部分逐字节相同；保留首次失败后重跑同一任务，尚待真实终态。不要删断言迎合失败，也不要默认已有10pass代表全组通过。


## 2026-10-01：门禁测试通过与共享会话删除入口的边界

58原仿真ID4240650696的同一Native构建任务第三轮测试实际11/11通过，native-test.exit.txt新结果为0；随后Cargo进入Release编译。应分别核验测试退出码、构建退出码、签名与安装后的运行版本，不能把测试通过当作升级完成。前一轮测试失败的修复仅为cfg(test)初始化授权开关及互斥隔离，生产门禁未放宽。

排查Mac传输后not_connected时，先区分远端进程退出与本机controller会话被移除。源码controller.disconnect会移除同ID会话并关闭SSH/MCP；官方界面每10秒做心跳查询，8秒超时或失败会调用该入口，连接自检失败也会调用；临时publisherChallenge另有finally关闭自己首次建立连接的分支。这些是可核对的删除入口，不是本次故障已证实原因。查同requestId/peerId的实际活动记录、调用方和时间再归因，不把同事另一个ID的操作当证据。

特别注意：_connectOnce对已有SSH的Mac/Windows会话立即返回snapshot；其刷新MCP失败后disconnect分支用于无SSH的PAD路径，不可拿该分支解释Mac断连。未取得拒绝报文、进程退出或会话删除证据时，保留网络/连接未知状态，不能声称对端主动拒绝或物理离线。


## 2026-10-01：codesign空权限声明导致升级前置检查误失败

132的升级前置命令把codesign成功返回的空entitlements输出交给plutil，导致NULL/zero-length解析失败，安装尚未执行。605旧App及最终365候选也独立实测codesign exit0、声明stdout为空，stderr仅Executable诊断。正确比较：先核对每条codesign独立退出码；两侧均空记录均无声明；仅一侧为空拒绝；两侧非空才解析并比较。不能忽略命令失败，也不能凭空给App增加权限来修复比较。

同Bundle、Team、designated requirement、deep strict、Gatekeeper与真实嵌套Node运行门禁仍要保持，主App无声明不等于Node没有JIT声明。605 handoff源码已修正、bash-n通过，尚未远端执行；实际上传后核对修订hash再触发一次性交接，不把源码改好当作升级通过。


## 2026-10-01：605最终365经原ID更新的实证路线

原ID5298938227完整上传最终签名公证ZIP：395751136字节、SHA620ac9ab1fcebdfb8d46bc9de92942ffefb82850cac878ab822c940b9ae472dd。控制端最终ZIP PID60022保持运行；传输期间同一ID短只读查询及另一Windows ID构建查询成功，不能据此宣称100台并发已验收。此前33MB断连原因仍未知，此次完成也不证明旧根因已定位。

复用步骤：先核验当前活桥/原ID/指纹与旧PID；完整上传并核hash；私有解压、同Bundle/Team/requirements与权限声明、deep strict及Gatekeeper；保留已验签旧版本APFS回滚；独立gui/501 LaunchAgent一次性交接（不要让退出旧App终止安装脚本）；记录实际runs1/exit0后bootout并归档plist；清理自己的旧连接缓存后按原ID新握手；实际MCP调用、客户端目标房approved、描述修订已上报与服务端新心跳分别验证。605实际新PID2456/build2365，原ID/指纹保持，description默认ready/reported且修订7，智能描述仍pending，不冒充模型生成描述完成。

本轮源脚本tool/cluster_mac605_dev365_handoff.sh（3327字节，SHAbeb8bbc5f85a9f708d82041a48ef23ee0fe6384c9a024ca0829725901ede8ad6）与同名plist（716字节，SHAc8dee08465b8d84bf55820914d7b8e59397c430aebeb8d996133e067279cf447）是该现场实证，不应把其中kemi用户、旧PID91828、gui/501、旧/新2360/2365盲套另一台设备。下一位同事先核对实际用户、旧运行路径/PID与版本，最小调整这些参数，保护原ID/配置与回滚。传输耗时取决于实际包大小和中继带宽，不承诺任意包一分钟完成。


## 2026-10-01：Windows已编译原生组件必须进入新整包

58同一任务11/11测试及Release编译均退出0，实际未签x64原生EXE21982208字节/SHA717c8eacedfd88c551d56d42e4223323f6f0a5bc7e7f3a7b27899bc999120dc8，独立冻结在D:\KEMI-Test\results\v360-native-inputs\native-artifact。该次命令使用host target，正确取件路径是cache根release目录，不是旧x86_64-pc-windows-msvc/release。签名之后hash会变化，应另记录签后报告，不把签前hash硬套已签文件。

本轮365的940冻结源码输入不包含生成的native Windows runtime。直接仅同步源码后使用已有runtime，会把旧helper装进新UI；CMake读取项目native/rustdesk/windows/runtime目录中的EXE、provenance及AGPL许可。因此整包准备须保留旧runtime三文件、植入本轮经过门禁/hash核验的新helper，按既有prepare格式产生provenance，再按成熟Flutter缓存路径编译。原生组件成功不等于365整包已编译、签名或安装。

PS1静态Parser在执行前捕获新脚本一处括号错误，旧稿已保存、修订后PS1及CMD守卫均0解析错误。5844字节PS1/SHA6934fb3b38135683599cca8b565af67650b9c890bc7d40bf95252f5ecd73dfa1与1404字节CMD/SHAc373e47bf4b1a75a16352241a90e1c27fb729098f1ca9d29afeb86682c1e15f3只是本轮已静态核验稿；尚未执行、未改执行策略，不能当作客户端构建证据。

## Windows房间过期但仿真可用：2026-10-01实测

58（4240650696）和xzl（6192992780）均以原ID连接成功，SSH/MCP就绪、可信主机与指纹匹配；实际cluster.rooms均返回simulationReady=true，但roomsAreLive=false、connected=false，错误为newlinkdemac-mini.local名称解析失败11001。两者Harness能力描述ready但pending_sync，不能当后台已收到。58运行时describe_tool确认dev346的cluster.configure不含serverSimulationId且additionalProperties=false；不得把新版参数硬塞旧工具，也不能把旧房间记录称实时在线。采用已完成原生测试/构建的新版整包升级路线，之后以原ID核对服务载体、真实房间和新鲜心跳。业务执行另有DEVELOPMENT_TRUST_CONFIRMATION_REQUIRED，需保留其门禁，不以仿真可用推导业务已获准。

## 2026-10-01：605管理API上下线与后台实测

605原仿真ID5298938227、dev365、原办公ID415501605，关闭集群前管理APIonline=true；关闭16秒后online=false，后续观察lastSeenAt固定1790810887.8214111，实际仿真runtime.status仍成功；恢复集群后lastSeenAt变为1790810912.746357并online=true。房间memberCount始终6，onlineCount随真实其他设备状态变化，不能把总人数当在线人数。原始净化证据：/Volumes/ORICO/kemi-build-cache/vibekits-cluster-validation-20260930/mac605-dev365-api-presence-20261001.json。只证明该台本轮API/心跳/仿真独立性，不替代全部平台开关和任务执行验收。

复用quality/room_fleet_snapshot.py的正式API模式（X-Hbbv-Client: api，accessToken仅进程内）可生成双ID/名称/版本/描述/approved/online快照；普通网页登录使用HttpOnly Cookie，不要错误期待JSON中token。六机快照另存six-device-management-snapshot-dev365-20261001.json：六台均approved，双ID/名称齐全；当时2台满足dev365实时画像快照，132心跳间隔偶尔超过12秒，随后恢复。已交负责132的同事结合AX耗时核验，不推断仿真离线。

网页实际登录后默认选通用六机房；标题显示总数6及动态在线数，单行列表显示名称/双ID/最后在线并在线优先，展开605后可见默认描述、未配置模型、连续在线/最后离线、任务历史/验收/积分。发现原详情把response_timeout实例误计当前待处理2项且直接显示accepted/completed代码；web/app.js仅展示修订后，实际刷新详情显示当前/待处理0项、已验收/已完成/响应超时及中文验收记录和积分原因。数据库与协议未改，JS语法检查退出0。旧只读任务不等于真实软件更新任务。

## 2026-10-01 后台详情阅读位置事故

实际网页在任务详情scrollTop937时经一次4秒刷新回到0，不能靠截图或暂停实时刷新掩盖。根因web/app.js renderDevices每次replaceChildren销毁整个滚动列表，loadDeviceDetail先清空已展开内容又使高度塌缩。修复按deviceId复用原节点、更新单行摘要并按在线顺序移动必要节点，异步详情加载期间保留已有内容，保持展开行阅读锚点。真实复验scrollTop986经9秒两轮刷新仍986，在线数据继续更新。中文任务状态/积分原因同步修正，旧response_timeout和总任务failed不再算当前任务。报告hbbv/docs/acceptance/BACKEND_LIVE_VERIFICATION_2026-10-01.md，JS语法0/页面无console error；这只证明网页和605单台相关项目，不等于六机任务完成。


## 2026-10-01 Mac249：旧路径与本机桥退出

设备 macdeMac-mini.local，仿真4456560334，办公24955106。原ID连接已恢复，SSH/MCP ready，原主机指纹保持。此前恢复日志直接记录 helper 从废纸篓旧App运行，切换后 registered/callable；当前实际App/helper却来自缓存dev308/2308，另有tools目录dev360/2360未运行。由此证明安装路径与运行路径不一致，但不证明这是全部失联的唯一根因。

更新前须核对实际App/helper PID、可执行路径和版本；升级当前实例，保留回退副本、配置、同签名要求与权限。不能只替换另一目录的App或按旧脚本硬编码PID终止进程。安装后必须验证两组件均为目标版本、原ID重连、新工具可调用和房间新心跳。

此次已验证新ZIP通过原ID上传：412066932字节，SHA256 0dfa9200fcd49b33c696a4e678699fd80b986c8fb99d0ca844065ad76713b9fc。回退副本签名验证通过。解压/签名检查回包EOF时，本机桥记录PID88877而真实进程已不存在；这是本机控制桥失效证据，不能报远端离线。远端命令结果未知，恢复桥后先只读查现场，禁止直接重跑上传/解压/安装。与桥所有者协调，只有在途任务结束或明确交接后才切换控制端App。

当前仅上传和回退准备通过；安装、授权延续及六机任务未通过。完整项目证据：vibekits/docs/acceptance/MAC249_RUNTIME_PATH_INCIDENT_2026-10-01.md。远端没有rg时改用系统grep；复合诊断应核对stderr及各子命令，最后一个命令exit0不代表前面的查询成功。


## 2026-10-01 持续资源与覆盖更新门禁

真实现场旧dev360 relay持续606%至657% CPU；保存精确PID、路径、占用后仅停止该旧helper，高占用消失。后续300秒采样终态exit0，旧进程未复活，当前helper中位0.6%/峰值2.1%。但当时有两个同候选App实例，新按generation合并在途就绪探测的源码也未进入运行包；因此仅算止损，不算根因修复或单实例发布通过。

SIGBUS同时段存在内核外盘media not present与重新挂载记录。时间关联支持排查存储映射故障，不足以认定外盘物理掉线原因；不可将签名验证成功当作运行稳定性。恢复桥之前先枚举同包实际进程、数据目录及服务归属，不能只看到旧桥PID消失就启动第二实例。未知同事实例不得盲目关闭。

新增集群源码将持久消息重试移出心跳同步；真实本地HTTP回归证明消息Future挂起时下一轮心跳完成、重试不重叠、关闭后不再调度，13项通过。设备成品仍待验。源码中的仿真探测合并也已有17项回归，仅证明在途合并和完成后重新探测，不证明忙循环根因。部署前应核验单实例、旧helper退出、空闲CPU、实际仿真与持续心跳，并区分源码、成品、止损三类证据。

## 2026-10-01 仿真在线但集群服务载体超时

Mac605原ID 5298938227可调用runtime.status，但通过服务端仿真ID的HTTPS载体持续运行时报告内部5秒连接超时，真实心跳年龄38.92秒。分别核验仿真通道、HTTPS载体和房间心跳，首次连接成功不能证明持续稳定，更不能据此判远端关机。

源码已对齐ID模式内部150秒与既有外层上限，普通直连仍5秒；传输超时后清理HTTP和载体供下一轮重建，保留TLS验证、凭据、epoch和outbox。实际本地HTTP回归在载体建立延迟5.2秒后请求成功，共14项通过。新源码尚未进入设备签名包，持续真机与故障重建未通过。

605恢复原HTTPS配置后roomsAreLive、connected、simulationReady均true，acceptedRevision=7。仅在原地址可达并保留既有TLS信任时恢复原配置；不改固定IP、不忽略证书、不重置授权、不放宽离线阈值。签名包验收还须覆盖持续心跳、原ID重建和任务不重复执行。

## 2026-10-01 消息重试批次饥饿

若后台镜像已存在、部分同事一直pending，检查重试是否总取前20条。固定前缀会阻止后续消息进入批次，不应据此判后续设备离线。cluster_task_protocol已改按房间上批最后key轮转，身份/journalScope变化清游标，仍用原messageId、镜像全文和ACK去重。21条回归中前20持续不可达，第21在第二批收到；协议16项通过。源码测试不等于六机成品已支持，使用前核对安装包。不得新建消息ID制造重试、直接改后台received或跳过成员/执行门禁。
