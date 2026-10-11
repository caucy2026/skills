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
