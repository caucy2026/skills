# 成熟方法与失败分支

## 工具和连接

优先已提供 VibeKits MCP。缺直连工具时，已验证本机桥入口为 `vibekits-remote-simulator/scripts/invoke.rb TOOL_ID 'JSON'`；先读该技能的 tool-contract，使用工具实际 schema，不猜参数。桥凭据由脚本内部读取，禁止输出 token 或 tool-bridge.json。检查桥实际所属进程；共享桥有其他任务时不重启升级。

每台 Windows 的 SSH 工具调用串行，前一个句柄终态后再下一个；长构建不得挂在两分钟工具超时内。使用独立、唯一命名、LimitedInteractive 的构建/测试 worker，保存意图、PID/创建时间、资源采样、退出码和输出。查询终态不重复 launch。签名不使用该 ScheduledTask 路线。

Windows JSON 输出用基本 DTO；PowerShell 用 UTF16LE EncodedCommand，文件读取有界并转成简单字段，不递归输出大型 SDK 对象或敏感环境。默认 upload_file 可能落到 C 盘，D 盘约束时用已验证当前仿真载体 SFTP：严格主机指纹、现有 key 引用、回环载体端口、目标 D 路径、上传后哈希。不能启动旧脚本里硬编码的另一台设备事务。

断联先读原 worker/log/terminal，再查同机已授权远程桌面、焦点、浏览模式、权限、客户端日志、文件传输或可信管理入口。结果未知不重复安装、签名、删除。恢复后原 ID 实际工具调用和房间心跳都验一次。

## 源码、冻结和构建

先检查挂载/剩余空间及本机规则。产物和依赖缓存按项目/任务隔离到指定外盘；源码保留原位置。冻结 manifest 使用真实平台和 features 的 Cargo metadata resolve graph，再验证活跃本地 crate 的 include_bytes/include_str 文件；全 libs 扫描会把非活跃 portable 资源误判为门禁失败。生成绑定和外部依赖另列，跨平台生成文件差异不能直接当源码漂移。

Mac 双架构复用已验证真实 CMake 可执行文件，核版本而非路径名；外盘短 TMP，locked/offline，指定 deployment target，保留架构分别的日志及通用二进制证明。发布冻结副本改版本，不为了打包改共享工作树版本。

Harness runtime 的审批记忆必须绑定足够具体的调用身份；历史 session/tool/reason 记忆会错误复用。复用项目 rollback 脚本，验证旧形态、负碰撞、幂等和未知形态拒绝，再重建 UI。不要因为复制 qualified 旧 runtime 就假设已修。

HTTP 不可用采用单次有界调度、指数退避和抖动；429/503 Retry-After 含日期必须落实最低冷却，手动触发和并发成功不能消掉该冷却。stop 不应被迟到完成回调重启。保持 token、epoch、cache、outbox；单元测试还需负向故障注入确认断言有效。

## 包、签名和覆盖安装

Mac：完整 frozen 源码→原生双架构→Flutter→兼容性→所有自有 Mach-O 签名→notary Accepted→staple/validate→最终 ZIP→独立解压 codesign/Gatekeeper。对比旧新 App/Helper Bundle ID、Team、完整 designated requirement 和 entitlements；空 entitlement 可合法，不把解析 stdout/stderr 错误当不匹配。仍需真机覆盖与原功能，不以 notarization 代替。

Windows：真实 D 盘 native Release→输入及核心哈希→G0/权限协议→平台回归→fresh candidate→复用确证 CRT 版本/哈希和 Microsoft 签名→完整 PE 分类→签内层→打 Inno→签外层→签名回读→原 ID 覆盖升级。沿用同 AppId。静态 SHA 门禁变更要追到 canonical 当前输入及已有验证，不能为了通过任意放宽。

签名只在目标活动交互会话，沿用 GUI EXE→BAT→PS→SignTool 成熟封装。核真实证书、有效期与硬件；PIN 对话框截图展示后只请人输入 PIN，不读取/代填/存储。持续跟踪同一 run 至成功或失败；禁止同产物未知状态再签。厂商 PE 保持原字节和签名，自有 PE 包括 Inno 内部 setup/uninstaller，不漏签 .node 或被临时改扩展的 PE。

## 服务、任务与规模证据

hbbv 部署保留 serverId、私钥、授权/设备、customer/member 和持久业务数据；备份后沿原服务路线替换，不碰 hbbc/hbbs/hbbr。SQLite 关闭时后台任务/锁的生命周期与模态关闭 UI 分开验收。公开 service-info 是请求作用域，先核实际鉴权再解释 execution。

原任务记录中 publish/bid/allocation/claim/ack 每步均绑定 task/room/device 和唯一事务；先查已有结果和 lease，不新建替代原任务。Harness 真实执行和后台 API 合成 fixture 分开。原生 delegation proof 必须匹配当前连接代次和在线状态，撤销/退出后补拒绝用例。

规模记录区分设备数、逻辑会话数、网络位置、持续时长、采样/重启/断联恢复。已有 300 合成会话 loopback 60 分钟可以复用其范围，不冒充 WAN、100 台实体机器或 24/72 小时。

## 备份和交付

使用项目既定独立 GIT_INDEX_FILE backup helper：精确白名单、秘密筛查、最新 remote main 为 parent、三方合并冲突人工核验、正常 push、远端 tree/blob 读回、共享索引前后哈希不变。不要直接执行历史脚本顶层旧任务。源码/文档/skills 仓库分别记录 commit 与实际范围。

商城以目标正确、发布成功和公开下载哈希验证为准；只有上传成功不算完成。云端构建后依 cloud-build-cleanup 清自己的不用缓存和旧中间产物并读回，不能删除别人的任务、最新包、源码或签名材料。

## Windows 原生凭据测试宿主

普通 flutter test 没有 Windows Runner 的自有 MethodChannel，MissingPluginException 不能直接归为产品失败。先确认方法注册源码，再用真实原生宿主补验，不用 mock 或静默 skip 代替。Session0 实机曾返回1312（无登录会话），与缺插件、整机离线分开；须在原登录交互用户测试。

共享原应用不能停止时，可建立只供测试的 native project/AOT 投影：保留凭据读写和其他生产源、合格Flutter/plugin库，main仅隔离实例互斥名/测试窗口标题；独立obj/output，记录差异和源码哈希，绝不把投影宿主作为发布包。测试仅写随机前缀自己的键，finally逐键删除并经真实native读回缺失；失败与未清理项保留。使用固定GUI入口绑定活动session/user/PID与结果，再独立核原应用创建时间和真实存储结果。源码/构建通过仍不能算覆盖授权延续。

已上传长PowerShell脚本沿项目既定PowerShell7 -File入口执行，先核实际策略/GPO；2026-10-11目标7为RemoteSigned、5.1为默认Restricted，未修改策略。不要加ExecutionPolicy Bypass或更改全机策略掩盖问题。读取在途日志应有界且FileShare.ReadWrite；读锁错误不代表原事务失败，不重启未知作业。

## 硬件签名窗口的实际可见性

先完成冻结/入口编译/会话证书预检，再启动一次固定GUI签名链。提前准备本阶段的Session1截图辅助入口，避免PIN窗口出现后临时搭工具拖延。普通SSH截图可能全黑，不能据此判整机离线或重复签名。

同一SignTool PID+创建时间+Session1核验后，枚举它自己的窗口标题、HWND、可见性与矩形，不读输入控件。窗口可能被防火墙等弹窗遮挡；对已核实PIN HWND恢复/置前，必要时临时TOPMOST，而不是盲点未知确认。Windows150%DPI下GetWindowRect逻辑坐标与CopyFromScreen物理像素不一致；截图进程须先DPI-aware，不能改系统缩放。保存失败图及原因，取到完整PIN窗口、空输入框，下载SHA核验并视觉检查后才展示和提示人输入。

一旦展示并请求输入，禁止再次截图认证输入状态；用同一run的state/report/process跟踪2–3秒轮询，直到PASS/FAIL，未知结果不启动第二轮事务。第一轮内层结束后，外壳签名可能再次要求PIN，按新实际窗口的输入前证据处理，不能假设缓存仍有效。PIN只在目标硬件窗口由人输入，不能在聊天收取或自动化代填。

## 签名任务的当前平台工具集合

context的allowedTools必须与服务端required_tools一致：基础tools后接当前真实平台的platformTools，按原顺序去重。平台来自本地runtime，不从收到的context决定权限。遗漏平台专用app_signature会使真实claim后context绑定失败；保持完整签名/身份/epoch/fence/TTL和严格集合比较，不删平台条件或放宽验签。回归覆盖基础/macOS/Windows及签名有效但错误工具集合拒绝；单元通过后还需新包真实任务。已领取后失败先对账原instance/lease_uncertain，不再次分配未知事务。管理工具经最新mcp.catalog_list得到instanceId后使用mcp.tool_call，hbbv工具不是直接的VibeKits内建工具。

UI动作返回AX -25204后先对账目标：2026-10-12取消本任务误触发的Mac445命令行工具提示时，按原2497/PID创建时间和精确Bundle ID读树，点击明确取消按钮后API报错，但独立进程查询已确认目标消失、原VibeKits进程不变。窗口/应用随动作退出可使AX回执失败；先查同一目标进程与窗口，禁止直接重复点击或改按安装。

平台工具合同要核所有执行层：Dart ticket验证修好后，Node validateStart仍可能只查基础tools，提前用当前真实宿主OS的正控、外国平台工具负控及官方SDK/真实loopback endpoint补验，不把Dart绿当完整执行通过。Node平台来自process.platform，不由任务输入选。

保留推理选择时，描述的总输出token预算也可能包含推理消耗。620高推理/512出现真实max-tokens，不是充值证据；须保留失败与不可用状态、不盲重试，源码修复可用有界预算和更短描述（当前固定2048/300字），Provider/Model/Reasoning及零工具、输入输出界限、截止不改。仍以新整包一次真实复验为准。zsh中的path会绑定PATH，临时变量用bundle_part等专用名；命令尽量用已知绝对可执行路径。


## 远程桌面恢复责任与守护进程寿命

仿真断联时主动操作已登记同机桌面；核对精确远程ID/窗口、当前连接、焦点、控制而非浏览模式、键鼠权限和客户端日志。旧画面及无回执点击不能证明桌面不可用；一次AX错误也不能证明动作未执行。用实际进程、窗口变化或原ID工具调用核验结果。未查清这些层次不得把启动已安装应用等普通恢复交给用户。2026-10-12 Mac132由用户通过同机桌面启动后原ID恢复，说明此前恢复执行不足，不能归因于整机离线。

LaunchAgent包装脚本直接启动后台主进程时，脚本退出可能连带结束子进程；健康ACK之后仍须检查脚本终态后主进程持续存活和真实调用。Mac132第二次621诊断短暂通过但包装器退出后主进程消失，尚无信号日志证明原因，不能算持续运行通过。优先正常LaunchServices启动；诊断守护需设计独立主进程寿命，不重复安装、不清身份数据。

## 房间信息与设备列表

仿真信息窗口须按当前客户已批准房间显示名称，房间可展开设备列表，管理员单独标识；成员/角色/在线状态读真实服务，不将缓存标为当前。使用代理自身鉴权的房间roster接口，核owner与当前approved成员，不借管理令牌读其他客户。列表仅在展开且前台时刷新，关闭取消定时器；异步返回核配置generation和成员revision，失效清旧列表并禁用操作。分页不得把首100条冒充全房间。成员撤销后旧仿真票据拒绝，管理员降级不移除仍有效的普通成员权限；同房间通信不写永久手动白名单。必须区分诊断范围和完整仿真范围，分别记录真实原生双向调用证据。

### 成员票据与终态占用

管理员未配置时administratorPolicyRevision合法为0；Rust/Dart仅此字段允许0，其他成员/角色/consent修订号仍必须正。必须用服务端真实P256签名的0策略成员向量回归，并重新编译原生，不能只换Flutter或复用旧运行时。服务端maxConcurrent不能一直计已结束票据；只接受已领取票据的同一目标complete回执，控制端/未领取拒绝、完成幂等且旧票不可重用。目标Gate仅在actual cancelAndWait和工具Future都终态后发送，未知执行不提前完成；完成记录随原过期历史策略清理，不删审计和任务数据。客户端新增complete必须先部署匹配服务器再覆盖，否则执行后404会造成未知回执。


## 冻结Mac插件输入：627已证故障与修复

Mac候选不能仅因路径名为`macos/Flutter/ephemeral/.symlinks`就排除整个目录。626该目录实际为276个物化插件输入文件，冻结旧recipe的排除使627首轮链接缺`sherpa-onnx-c-api`，Xcode exit65。版本/Flutter声明资产检查不能证明这些原生插件输入齐全。复用最新合格基线实际输入，复制后逐文件哈希、检查实际xcframework库，再运行同一完整Xcode命令；保留首错log/XCResult和独立重试回执。不下载新依赖、不改签名身份，不复用失败产品。627恢复后完整命令45.026秒exit0，随后签前/后兼容与主/助手身份要求匹配通过。此经验不要求其他机器固定物化目录，只要求按实际插件布局保留输入。


## 无CLT目标Mac的只读核验（445现场）

已确认无Xcode/CLT的Mac不应因`/usr/bin/python3`存在就执行它；该路径可能是安装按需stub。627准备时误调用触发安装询问，未安装：通过实际bundleId `com.apple.dt.CommandLineTools.installondemand`的原授权UI检查、精确“取消”按钮恢复。AXPress返回-25204但新UI查询显示App退出，原VibeKits PID/版本/哈希不变；关闭窗口的动作须读回结果，不能因旧AX对象失效盲点第二次。后续沿内置PlistBuddy/ps/shasum/df做有界只读核验，不安装工具链。其他机器先沿各自已证环境判断，不将该Mac缺Python推成所有Mac都缺。


## 部署路径中的设备ID不是版本号

1321656264含626子串：对整个守护文本replace626→627会把设备ID和路径改错。627首次132守护实际exit127、未运行安装，旧626不变；按原label读取not-running/lastExit127，再保留首错、修正RID、核解码Plist ProgramArguments/输出路径与真实stage一致后重试成功。只替换明确版本字段，RID/主机指纹/路径中的设备身份独立固定；Bash语法和Plist lint不证明部署目标正确。

## 房间完整目录的真实证明边界

627两台真机在明确general room下各265工具连接；每方向1个bulk descriptor票、3个计算器/3个system.info，14票已领取并完成。工具目录存在不等于所有工具成功，计算器证明超出五诊断但不能替代文件/命令取消、角色撤销或全机队。保留room-members模式、所选roomId、目标实际PID、实际结果和服务审计，不改旧白名单。

客户端taskSessions的reconciling项不必然有在途工作；先核服务器实例终态/lease、SDK实际session/busy和pending结果。旧rejected+过期lease+无session/结果不能当运行任务，开关enabled也不是执行中；不删除历史或自动重放旧failed业务。


## HTTP等非进程资源也须登记取消

实际HTTP持续响应旧红控证明：CommandResourceScope只杀Process不能结束HttpClient的Future。把自有client登记为有限scope operation、cancel强制close、每chunk先consume、finally完成；gate仍需等原工具Future真正结束才complete票据。API无scope默认行为保持。32回归/166冻结候选通过只证明源修复，未装628前不要宣称627现场已修复。scope operation callback快照遍历防取消时集合变更，保4操作及原字节/时限。


## Same original simulator SFTP resume after a known failed transfer

确认原upload终态失败、源与残留前缀SHA一致后，可沿已登记VibeKitsloopback的原known_hosts/key引用执行sftpreput-a续传，不读privatekey内容、不新增授权。先核原hostFP及唯一当前port；路径含空格时复用已证quotedUserKnownHostsFile选项，保持StrictHostKeyChecking=yes。首quotes失误“Nohostkeyknown”未认证/写入，不绕过检查；修正真实文件路径后重核完整bytes/SHA才安装。未知在途不重传，不用resume掩盖不同前缀。628132实证207.6MBprefix→完整423.8MB。

## Mac bare launch before AppKit check-in and scoped recovery

采样显示新进程仍在AppKit/LS初始化、无Flutter/新crash且guard已回退时，核原事务与旧进程后，可以同一签名候选在独立stage仅改normalLaunchServicesopen启动。原ID/key/版本/实际MCP/rooms及guard卸载后同PID均复验，不重签、清用户数据或重置权限。628132已证该路线恢复；不能泛化为所有启动异常根因。


### Mac SSH/SFTP 受保护文件访问
按[远程仿真技能的 macOS 文件访问前置设置](../../vibekits-remote-simulator/SKILL.md#macos-远程文件访问前置设置)核对远程登录完整磁盘访问，保留允许用户名单，以原用户真实文件读回验收；它不代替App屏幕/辅助功能权限。


### 应用版本不能证明原生输入延续
冻结新客户端时，将实际原生输入绑定已审核的功能证据及保留输入的SHA/字节。640/641曾复用618原生，完整房间证据却绑定627/628；protocol_v3、签名、公证和组件通过不足以证明功能连续。项目verify_native_input_provenance.py提供哈希与证据字节门禁，旧输入/证据改动负控已过；真实最终包仍须另验。


## Mac冻结件的Flutter生成插件链接与RPC生命周期

643首轮Xcode在链接阶段exit65：冻结流程排除了macos/Flutter/ephemeral/.symlinks/plugins，导致Sherpa的xcframework路径缺失。Dart测试通过不证明这些链接存在。构建前核对已验证基线的全部插件链接：每个真实目标须与当前冻结package_config中的同名package root一致；库目录、实际库字节及目标架构可读，再恢复本候选的生成链接。只读复用既有插件包，不改锁文件或下载另一版；不覆盖共享源码的链接。原构建确认终态后，新结果目录/日志重试同命令。643恢复四个匹配链接后完整Universal构建exit0，原日志保留。

首次目录系统权限确认后的加载等待与模型可用是不同结果。132的642在首次Documents确认后读取未完成，取消重入才恢复并真实pwd确认QA目录；不能称首次无异常或旧TCC授权延续。先核设备、应用、系统请求的具体对象，按已有普通确认授权处理并读回；不清TCC、钥匙串或用户数据。

Safari15的应用适配层只对directoryPicker/list读请求设置30秒截止，写事务不新增超时或自动重放；预先和运行中取消均确定拒绝Promise，终态移除监听器，迟到响应不改结果。保留旧实现负控、三轮生命周期、JSON/二进制回归。准备运行时和完整预检必须执行生命周期测试，实际生成文件检查须拦截旧缓存；源码通过不代表已签旧包含修复。新包仍需同身份签名、公证、Intel实际选择目录和请求的完整证据。


## 运行时暂存备份不可进入签名载荷

重生成兼容前端时，先前版本的临时备份放在证据/任务缓存目录，不放native运行时或App资源目录。643中dist-macos12-before-lifetime被完整运行时复制带入已签App，实测5711619字节。核对两份自有备份完整清单、字节hash和无占用后删除，保留原公证容器/提交号及失败记录；重新签名和身份比较，通过后以不同容器/回执提交清理后的新字节。不能拿原提交票据验证修改后的App，也不能把重新签名说成原字节不变。打包前验证此类自有临时目录已不在签名载荷，修复的最终包另做完整验收。


## Mac停机时fork残留占用旧监听端口

644本机首次守护在替换前报OWNED_PROCESSES_DID_NOT_EXIT。不得仅凭同名新PID推断正常应用重启：残留7183父PID1、创建时间与停机一致、RSS约3MiB、无子进程，却持有原App多个监听端口；两秒sample显示唯一线程停在Dart ProcessStarter/FDUtils::ReadFromBlocking。原App磁盘仍643、未发生替换。以精确PID/出生时间/路径/旧main哈希和采样绑定后清理该自有停滞进程，正常LaunchServices恢复原643，实际MCP/原ID/实时入房再核，不能仅以open请求为恢复成功。

后续独立守护先核当前真正主PID/出生/哈希、SDK会话已完成、业务任务已过期或无在途；先SIGSTOP该主进程暂停Dart定时器，再快照并停止同一已核bundle的子进程，向该主进程发送SIGTERM和SIGCONT，检查全部自有进程确实退出后才原子替换。finally恢复暂停状态；替换前失败且旧App无运行主进程时正常恢复原App，已替换失败按原回退路线恢复。未证归属、PID变化或实际有业务工作时不泛杀。644此路线真实覆盖成功、反向原ID调用/主哈希/实时房间通过且守护退出；不意味着所有停机错误都可强制清理。


## 空闲性能修复先绑定线程热点，再独立复验

643五分钟CPU中位5.6%，644为8.6%，均未达5%；RSS各自通过不是CPU通过。不能用减少凭据读取的单元结果代替最终签名包性能。保留五分钟完整JSONL，分别跑CPU和RSS判定器，采样前核自有会话/事务结束，采样期间不操作App或改其监听目录，采样后查工具账本及主PID全程一致。短时sample只收线程函数，不读凭据/argv。

644热点实际落在RoomSimulationEnvelopeJournal.put→_expired→ECDSA。清理策略可先对结构、规范、作用域和到期保留期限做便宜拒绝，再对真正删除候选执行原公钥/原域签名验证；不能移除实际删除前的签名或权限检查，未知/篡改/其他scope/当前重试仍保留。非秘密观察回调只计验签启动次数，不替代验证结果。旧类负控4次验签、新类2次且伪造保留，原日志/委托安全14项通过。

同一生产类400条有效保留记录三轮计时旧中位1625.923ms、新32.103ms，写后401条保留；这是热点对照，不是整机CPU通过。新645包含该修复及之前凭据轮询修复，191联合回归通过；正式签名包仍需真实升级及五分钟门禁。源码版本变化、编译成功或包体变小都不能抹掉643/644首次FAIL。

### 凭据重复读取与异步回归的误通过

647 的五分钟 CPU 中位 10.7% 仍失败；10 秒 Time Profiler 中 ProcessStarter::Start 占 423/1224 ms，仅说明抽样热点，不证明唯一原因。记录子进程时只取 PID、父 PID 和可执行名称，不采集参数、环境或凭据。Xcode trace 的 TOC 可包含完整环境，保持私有，不直接输出或备份到 Git。

refreshLocalGrants 对不存在的本地授权记录原来每房间读取两次。只省掉没有同步、没有本地变更的第二次读取；下一次刷新仍读存储，已有记录的同步后复核和错误恢复保持。真实生产流程旧负控 Expected 1 / Actual 2，修后 agent/local-grant 共 27 项及三轮独立流程通过；不外推最终包 CPU 达标。

计数回归先等已启动的异步刷新结束，再记录基线并调用目标方法。第一次测试与现有刷新重叠，目标调用因 busy 返回却恰好计到一次读取，形成误通过；不能删负控或将此当正确产品行为。隔离 Flutter 测试须带 package_graph、声明资源，并把所有相对 package_config 根按原配置位置解析；测试代码和产品代码来自当前共享源码，所有生成输出放本机规定缓存目录，不改旧候选冻结件。

### 没有可授权设备时的工作区监视器

648 实测 CPU7.9%仍FAIL、RSS通过；采样61帧主PID一致，窗口内无记录的外部工具调用。热点包含工作区每秒读取记住设备的凭据。仅对“没有记住且connectionReady的设备”的观察复用最多五秒；成功save/forget跨同进程store实例立即失效，时钟倒退与错误不复用，存在可授权设备时每次新读。常规load及界面读取保持新鲜，不保存Key或复用实际权限，不改变原生检查或决定调用。跨进程新增无本地通知时最多等待该五秒观察期限，不能宣称零延迟。

旧读/filter路径五次读取负控失败；修后三轮空观察、截止和时钟回退，以及保存/忘记立即失效、实际记录逐次读取、失败不缓存通过。27配对/Host/界面相关回归通过，649冻结联合209项通过；这些不是最终包CPU证据。隔离Foundation启动对照三轮更慢且整轮CPU时间未改善，不据此替换生产启动路径；隔离elapsed/整轮rusage含初始化与子进程，不外推App唯一根因。

### 集群贡献对照和本地授权的空观察

649五分钟CPU7.2%仍FAIL。因果对照前确认原任务TASK_EXPIRED、关联会话不活跃、resultPending=false且自有模型已完成；只短暂关本机集群同步，保持仿真开启，finally恢复原开关，核原ID/live rooms。开启前14.3509%、关闭5.4587%、恢复15.2173%是短时主进程累计CPU时间占比，不是五分钟ps中位或发布PASS。

自动UI刷新对缺失本地授权记录最多复用五秒，最多128个完整上下文；上下文/成员修订或成功存储写入改变立即失效，时钟回退/错误不缓存。普通view主动清空旧缺失观察，approve/revoke/synchronize始终读存储，实际记录永不复用。只缓存非秘密的缺失时间与上下文，不缓存权限/Key。无本地通知的外部新增由截止后的下一次自动刷新发现，四秒轮询可达八秒；不能承诺外部变更零延迟。原房间成员/票据/撤销检查和模型凭据读取不改变。

旧实际view委托九房间两轮读取18次，负控Expected9/Actual18；修后三轮、截止/回退/显式/上下文、跨实例批准撤销、错误和外部变更显式观察共31相关回归通过。新650联合222项通过，仍须最终包真实CPU/RSS、授权和全设备验收，不以读取次数下降授予性能PASS。

### Windows：先核原成功执行器，再判断策略阻塞

58历史成功的原生628启动实际使用已装PowerShell7的绝对路径；误用系统PowerShell5.1执行后续.ps1时得到Restricted/UnauthorizedAccess。只读复查同机指纹后，7.6.6现行RemoteSigned，复用原7入口可正常启动Limited交互任务。没有修改策略、增加Bypass或绕过平台审批；旧“需改CurrentUser策略”问题因此不再是必要步骤。换机器先看自己的原成功argv和现行策略，不照搬本机C盘工具路径；所有新增受控输入/结果仍在D盘。

650源码准备先因旧基线一个将被新差异覆盖的测试文件hash变化停止，原基线未改。仅确认该路径的新冻结替换字节，核所有真正使用的旧输入和最终全量输入；不能泛免检。随后Python逐文件复制/重验在120与300秒截止，原PID/创建时间/终态先对账，部分源码不删除。原复制包含未声明的暂存/npm/旧Flutter编译缓存，排除精确根路径，保runtime完整闭包、NuGet输入、依赖图和hooks。复用原交付robocopy，/E /XJ /XC /XN /XO /R:0 /W:0及绝对根路径排除，不覆盖现有文件、不删除；新差异落盘前查已存在目标为原输入或新冻结字节，未知修改保留拒绝。最终2816输入全hash通过，46.68秒终态0。robocopy exit0自身不是源码或发布PASS。

整合已资格原生628的同一23176192B/20de87a00276ec0944feabafce56445a7fccad8f4ba05ba9af73ded9fdd4e31e，保27原生回归和来源清单回执，更新侧车而非继承旧二进制证明。隔离源码内替换不等于安装或仿真通过。完整Release沿619成熟入口，同镜像离线enforce-lockfile、D盘缓存/TEMP、CMake并发2和PID出生时间预算。650 Pub日志三条内容hash提示后实际lock SHA仍等于冻结de6843373f4019e71b8e544ec77851194ab1379b11508136bd18f6987b4ce719；先读实际字节，不因提示重写锁或变版本。


### macOS频繁只读查询的进程启动开销

先以同进程、相同触页堆、相同真实native只读命令做parent getrusage配对，再决定是否值得持久启动通道。持久通道只负责启动与生命周期，不缓存授权或状态；status/connections固定映射，身份与helper路径仍来自当前签名App，5–8秒原预算、队列/输入输出上限和关闭回收必须验证。任意命令/额外参数拒绝，写路径不转发。Dart多个并发IOSink.flush会绑定同一stream失败，必须串行写入；保留真实并发首失败，三轮实测复验。下降的parent CPU不能代替App五分钟CPU/RSS门禁。

准备runtime与App自有native/harness脚本hash不同，先比较当前已签名已运行App及原冻结来源。打包步骤可能覆盖这类自有脚本，因此raw准备目录不自动等于实际最终载荷；保留三方hash及旧字节，只在候选输入中对齐真正将打包的源，官方SDK不动，重跑完整helper/skills匹配。目标包要求按实际Node二进制格式判断，不能用控制机OS迫使Windows/ELF带Mac-only脚本。


### 2026-10-13 Mac132 桌面恢复与自动化输入模式

原651覆盖guard v1实读exit21/BLOCK_OLD_APP_TREE，旧643目录未被替换；不能把仿真离线写成整机离线，也不能重跑未知安装。登记办公372799163仍有实时桌面。逐层核对后，先结束本任务重新打开却停在T状态的旧版进程92620（已核精确App路径、state、启动时间），保留所有配置、用户数据、App及候选。Finder Caches内精确选择Vibekits 2，Quick Look实际版本1.9.0.643；办公键盘菜单选择传统模式后，通过实际Cmd+O打开原App，原1321656264重连、指纹G73...、265工具及system.info PID94393真实通过，roomsAreLive=true。恢复仅证明旧版可用，不证明651验收通过。

桌面自动化先核当前菜单和选择状态：1:1传输下CGEvent Unicode typeText可被远端当固定虚拟键，逐字符也可能只得到a；普通文字成功不能外推修饰键/命令准确。菜单会因模式增加行而改变坐标，必须每次观察当前菜单，不复用陈旧行坐标。已证成熟方式为当前会话切传统模式、核对精确目标、实际键盘动作与截图，再用原仿真ID真实只读工具确认。Mac办公窗口可用Dock精确AXDockItem→activate→Window菜单精确会话标题恢复前台，不关闭同事窗口或处理不属本任务的入站请求。鼠标移动/点击错位原因仍未独立证明，不将推断登记为修复。


### 2026-10-13 qualified overlay lessons
Reuse the signed bytes and verified full rollback. Windows watchdog requires install/backup/result paths to be distinct with neither nested in another;do not weaken that check. A stopped verification worker does not require recopy:33515 copied files were independently journaled and hash verified in v2. Persist per-file progress and monitor actual RAM/commit/CPU/handles/BOUND/dynamic range;unknown installer outcomes are reconciled, not replayed. Live log reads need explicit FileShare.ReadWrite, even in PowerShell7;use bounded streams rather than ReadAllText on writer-held logs. Success is guard committed plus original-ID real calls, signed core tuple, transfer hash and live rooms;then recheck the main after observer exits.
Deep macOS AX walks can exceed MCP budget:132 actual66.367s late success, not proof of a deadlock. Keep shallow/bounded queries and examine original tool trace before another action. Native typeText virtual key0 may become a in WebView;do not count requested character length as actual text. Cancel incorrect path and use verified directory rows;new651 picker was confirmed by actual pwd in the new workspace. Complete text/IME regression separately.

## 2026-10-13 Windows619 原位650覆盖升级终态

同一6192992780/xzl/zjc、既有无D盘C用户例外路径覆盖604→650/2650，安装退出0；新main4092/birth134363566853123894持续运行。guard7208 verified_committed/terminal0/observerEnded=true，Task Ready/result0且guardAlive=false。原ID重新连接、真实system.info4092、cluster.rooms实时connected恢复；09:28:20Z再次真实system.info仍4092。没有改执行策略、没有绕过被拒PS文件、没有清配置/Key/授权。

用既有签名Node及同版本Koffi的独立外置入口，Session1与原PID/birth/窗口所有者先核验，再正常WM_COMMAND41002退出；初两次探针因漏复制原Koffi可选win32-x64包失败，补齐匹配原字节五文件后v3通过。保留失败回执，不将其称平台拒绝。完整31105文件/1003774142字节604回退保留，manifest E67DC094BABACABACAEAE60322C12B474E561E096E08332FA432D9295ADB2DAD。

安装后独立核三件套：main A823C0999B90BD4236BBDB2051B71FC2491DB5EAFE7FA48AD8BB9740BD2F4886；flutter_windows.dll 1FDFC8FA063F29EC1CEE4343EF490110F582F313BDA046F8604569C0E54C4424；data/app.so 51232286107F649A0E6D7721AF1EBA488012A64CD237AD7F173C62B374E0FF89。与最终签名650对应字节一致；12逻辑核已读回。

控制器证据：cluster-app650-20261013-v1/windows619-install650-terminal.json、windows619-installed650-core.json、windows619-post650-health-commit.json。guard仅RAM/近似提交观察，不冒称完整CPU/网络五分钟资源通过。原Key模型、UI/历史与完整资源仍待验；商城未发布，G01–G10未完成。
