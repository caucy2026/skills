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

## 14:12 后复发核验

重新检查发现全局技能 invoke.rb 再次被覆盖为固定默认桥路径版本，项目 tool 中的已验证 locator 修复仍在。恢复两份脚本后，六个原仿真 ID 全部 connect.connected=true，device.applications 调用外层 ok=true；58另核对内层结果。此次未修改远端身份、未改IP、未重装。说明修复还必须纳入共享技能交付，不能仅临时复制后假定永久生效。

客户端 transport_timeout 自动转一次中继的源码修复仍存在，两个针对性回归测试已通过；尚未签名分发，不能宣称新客户端已部署。后续验收必须包含技能升级后脚本仍使用 locator、正式/候选实例切换、直连超时后中继恢复、内外层远端返回均成功。
## 2026-10-01：集群专用载体的需求驱动死锁

普通仿真SSH/MCP可用而房间HTTPS超时，不等于设备离线。原生端口转发在本地client被accept后才启动远端握手；集群先等native-ready、HTTP拿到lease后才连接端口，会互等。修复使用 `waitUntilConnectedWithLocalDemand`：先打开无负载本地socket，再等native-ready，成功或失败均回收探测socket；真实HTTP仍保留原CA、SNI和Host。隧道29项（含拒绝错误透传和socket关闭）、控制器10项回归通过。

132真实只读验证用当前包内Node/native helper，通过服务仿真ID1554650784的固定127.0.0.1:51839、原公开CA/SNI/Host，得到tlsAuthorized=true、HTTP/1.0 200 OK；不使用设备固定IP，不关闭TLS验证，不传认证凭据。成熟诊断源为共享项目 `tool/cluster_id_https_demand_probe.js`，SHA256为549de910b2ebb71d722733c879d1684121724d10fdb3fea9ec18ed329f911bb6，回收仅自己创建的socket和子进程。该验证证明载体/TLS可用；必须另核对安装包含修复、cluster.rooms实时和后台新鲜心跳，不能据此宣布六机完成。

Windows原生samplerate失败案例：libsamplerate-sys 0.1.12在MSVC声明out/build/Release，Ninja实际生成out/build/samplerate.lib。先读取实际build.rs/输出、确认原任务终止和无Cargo，保留失败日志，再将本次生成库复制到声明目录并核对SHA一致后重启原任务。不用历史库冒充、不升级依赖。调度Running或旧exit文件不是本轮通过；应看当前PID、CPU进展、新结果时间及测试/构建真实终态。

下一版允许名单/黑名单与明确拒绝报文仍属于待实现需求。不能把未知结果编成拒绝，不能绕过明确拒绝，不能把拟定协议错误码当作当前已上线功能。

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
