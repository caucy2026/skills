# Linux 桌面常见错误：按当前症状取用

这是一组真实案例提炼的决策依据，不是每次都要执行的额外清单。项目原命令、目标系统与当前授权优先；已解决历史项不盲重跑。

| 症状/曾发生的错误 | 正确定位与最小处理 | 验收不能混淆 |
|---|---|---|
| x64 Flutter主机直接当ARM编译器；执行错架构工具 | 核ELF/SDK/engine真实架构；复用已验证对应架构原生环境。原工具链缺ARM支持时才做有证据的隔离适配 | 文件名arm64、设置--target不等于产物架构正确 |
| 新Dart配旧插件/原生/SDK，或只换AOT | 冻结原生生成器、输入和完整运行时，重建正确整包；组件复用须有相同输入与最终哈希证明 | 编译/启动不等于SDK、原功能和最终包通过 |
| 新外壳版本夹带旧version.json | 同步pubspec、AppVersion及生成资源，验最终包与实际运行路径 | CLI --build-number不能替代其他版本字段 |
| 安装了依赖仍pkg-config失败 | 用**同阶段真实环境**验证搜索路径；保留原PKG_CONFIG_PATH、CC/CXX、LIBCLANG_PATH。字体454控制器曾漏传已验证libyuv路径，ambient失败、原qualified环境成功 | dpkg installed不证明pkg-config能发现；不先升级系统包 |
| Cargo误用默认缓存/联网重装原工具 | 复用原CARGO_HOME/RUSTUP_HOME、固定工具链、offline locked metadata；先本地试原工具再决定安装 | 网络超时不是源码断言失败，不删原SDK解决 |
| Pub认为合法Git缓存损坏并删除 | 检查PUB_CACHE是否为symlink；使用已验证物理路径pwd-P，避免复制整套缓存 | 不改下载校验、锁或全局Git配置掩盖问题 |
| dpkg状态多行误报缺包 | 逐行匹配目标架构或all及install ok installed | 不把多架构输出拼接后当单值比较 |
| 桥接/协议摘要不符 | 在原正式入口的相同临时版本/协议准备状态核验；入口退出还原的canonical源不能直接与生成前摘要混比 | 不能跳过协议生产器、补假stamp或复制不明桥接 |
| SDK更新导致DialogTheme等类型变化 | 核真实版本API；只在对应隔离构建源做最小适配并锁依赖，保其他平台原API/锁 | 不因ARM SDK较新就全局改坏Mac/Windows旧SDK |
| 原生target错位或库名字不对 | 核实际Cargo产物、CMake引用、target symlink及所有权一致 | 同一版本名不能证明core/AOT同源 |
| 中文首次方框/升级回退 | 按fonts-and-windows定位系统/包/主题/加载/SDK，各层分开 | 不把fc-match成功、TTF存在或locale中文当实际显示成功 |
| 黑色圆角/透明API在旧SDK不存在 | 核Gtk visual、GL alpha和FlView底面；按实际接口可用性兼容，正常/最大化/恢复分开看 | 不把整窗opacity调低；RGB丢alpha不代表窗口真的黑角 |
| 硬编开关开但实际软编/加载失败 | 区分软件x264/x265和硬件后端；核GLIBC/GLIBCXX及依赖、设备驱动、实际关键帧/会话 | H264/H265、/dev节点、注册名、低CPU均不能单独证明硬编 |
| GLIBC过新，目标旧系统加载不了 | 检查完整依赖链的version-needs；用匹配基线重建或经用户允许验证独立运行时/codec进程，记录支持范围 | 不盲换系统libc、不伪改ELF版本；基线允许调整时也不能固守旧门槛停工 |
| 同名库被直接套用另一份SDK头文件/ABI | 核实际导出、版本、调用约定与匹配头文件，再试编译；文件名libavcodec.so不能替代这些验证 | 加载成功不证明全部FFmpeg API/结构布局或编码器可用 |
| 按CPU核数开j16后OOM/磁盘边界 | 先核同机RAM/swap/IO/空间与原预算；区分memory-boundary/disk-boundary。保首败、准备足够环境后完整重试，真实标j4/j8等 | 失败轮不是编译提速数据；不除以8掩盖CPU占用 |
| 秒表100Hz整页刷新或后台仍跑 | 真实单调计时＋vsync/局部通知；静态表盘缓存；隐藏停绘、返回更新、失焦仍可见则继续 | GUI不宜为“多线程”创建8个刷新Timer；重计算用有界worker |
| Widget测试误走Android、平台变量清理失败 | Flutter测试默认可为Android；用官方TargetPlatformVariant定位目标分支。保原失败，按实际控件模型/语义断言 | fixture错误不是产品故障；测试断言过了但框架结束报错仍不能报整套PASS |
| Type=oneshot看似超时/SSH观察断开 | 使用合适TimeoutStartSec及内部阶段时限；需要立即回执时--no-block；核同一单元/PID/出生/真实子进程与结果 | RuntimeMaxSec对oneshot可能不生效；观察超时不是终态，更不能重启未知事务 |
| 上传后按原文件名找不到 | 使用返回的实际remotePath（可能有时间前缀），完整SHA/bytes后才解包/执行 | No such file是路径/业务错误，不一定是权限拒绝 |
| Mac归档UID501导致Linux信任拒绝 | GNU tar --no-same-owner，禁Mac xattrs；核任务目录目标UID/模式，只修本任务错误元数据 | 不放宽GUI身份门禁、不换运行账户或重置允许库 |
| 正常点允许却一直pending | 沿GUI→原生handler→平台cfg→IPC allowlist→身份/nonce/CAS完整链检查 | Dart能显示、用户点击、目录有条目均不证明Linux原生处理编进去了；不代写grant |
| 工具只返回泛化tool_rejected | 查原结构化错误和必要代码：参数校验、invalid bundle、无文件与安全审查拒绝分开 | 真安全拒绝不能换工具绕过；Linux appName/PID/出生可能才是正确目标字段，不能改App ID凑参数 |
| 主桥ECONNREFUSED或仿真离线 | 核当前实例数据根、连接文件PID、loopback监听；再对账目标原进程/已登记备用通道 | 旧bridge文件失效不等于整机离线；不新启多实例抢同事 |
| 脚本bash\r/解析首败 | 核实际上传字节、CRLF及shell；只修本任务生成脚本，保持原SHA与首败证据 | 不用全局文本替换版本号，把0755误改成0756 |
| Git部分克隆提交准备突然拉大量无关blob | 保真实main父提交和树；仅在未修改对象引用来自可信原树、改动blob齐全时可用write-tree --missing-ok，逐路径核差异；正常快进推送 | 不能构造假父提交/树、force或动同事HEAD/index；未知推送先回读，不重复 |
| 本机模型设置/原SDK功能回退 | 保本机/访客/远端不同身份元数据、原业务接口与配置镜像；真实点击原设置/推理/停止 | 后端302绿测、MCP ready、组件或签名PASS不代替原UI功能 |

## 对照报告最小字段

来源commit＋Linux增量；目标架构/系统/SDK和阶段环境；精确产物bytes/SHA；实际进程/出生/映射；旧失败负控、新组件与真实功能证据；资源口径和失败样本；剩余项；现场恢复和实测空间。不要把本表、一次脚本执行或云端上传当交付。

## 项目证据入口

- VibeKits：`docs/development/COMPILATION_DEPLOYMENT_RULES_20261023.md`、`docs/acceptance/LINUX101_RECENT_ISSUES_ACCEPTANCE_20261026.md`及`vibekits-linux-release/references/linux-incidents.md`。
- 远程办公：`kemi-remote-office-release/references/linux-native-market-20261016.md`，及RustDesk main `9d2a0ced...`的`client/kemi-docs/LINUX454_FONT_CORNERS_ACCEPTANCE_20261026.md`。
- 这些是案例入口；版本、设备、PID、账号和路径必须现场核验，不复制为全局默认值。用户允许调整基线后，已用官方签名Ubuntu包构建独立2.35运行时：同一个实际ARM编译helper在系统2.31加载厂商库失败，在独立2.35可加载VENC及媒体库，系统仍2.31。这个真实负/正对照证明加载方案可行，仍不代表H264/H265硬编关键帧或整包兼容通过，不能泛化为所有机器都应升级或都能使用该方案。
