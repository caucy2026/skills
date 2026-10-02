# 通过 VibeKits 仿真 ID 更新目标机的 KEMI 商场应用

## 热更新与失败回滚验收（2026-10-01）

HTTPS、商城下载和编译机产物只是包来源，落地后的升级事务必须使用同一套身份、哈希、签名、备份、启动与回滚校验。每台先记录实际运行路径、版本、双 ID、可信指纹和有效授权；按当前平台选择已验证的安装事务，不能按固定盘符套用其他机器。

- macOS：完整备份当前 App，并验证备份签名。候选单独解压，检查版本、Bundle ID、Team ID、指定要求、权限声明、Gatekeeper及票据。禁止 ditto 合并到现有 App：本次实际出现旧资源残留导致 sealed resource missing/invalid，完整目录替换后恢复。停止精确旧实例后同路径完整换包；移动、换包后验签、open 或启动健康检查任一失败，恢复旧完整目录并启动。不能仅对 open 失败回滚，而遗漏换包后 codesign 失败。
- Windows：先区分 MSI、Inno 与便携事务，保留原安装身份、配置和签名校验。升级执行者必须独立于即将关闭的 App，使用已授权、已验证的交互会话任务；旧 App 退出不能把安装执行者一起结束。回滚须恢复精确旧文件与原配置，并验证实际进程、原 ID 和有效授权。未知格式不能盲传静默参数，不能修改执行策略绕过门禁。
- 通道中断：SSH EOF/255 或桥失联不表示升级失败，也不证明成功。先恢复本机真实桥，再按原 ID 只读查实际版本、进程和事务日志；未知结果禁止重复安装。仿真确实不可达时，同机办公 ID 可作已授权备用诊断渠道；首次仿真同意仍必须由对方人员确认，不能自己点授权。

本次 Mac249 已实际完成 dev308→dev366、原 ID 重连及新工具调用；dev367 的605回退脚本只通过语法检查，失败分支尚未真机演练。Windows dev346历史更新成功不等于当前所有便携包回滚已验收。不得把这些不同证据合并成“六机热更新全部通过”。

持续运行验收使用同一签名候选逐台核验：原双 ID、Harness实际调用、房间新鲜心跳、双向消息及 ACK。同时记录客户端/后台时间、进程退出、CPU、内存和连接重建；覆盖持续正常网络及断网恢复、服务重启、App重启，恢复后保留凭据、任务租约和消息去重。短时在线截图不算长时间稳定，不能放宽在线阈值掩盖心跳间断。持续时长和允许资源阈值按项目验收文档执行；未满足则记录失败并修复，不能保证“有网络必定永不故障”。

适用：用户给出已授权的 VibeKits 仿真 ID，要求把该设备上的 KEMI 远程办公或其他商场应用升级。此流程是**单机仿真维护**；要声称“房间智能体自主领任务并更新”，还须另验集群合同、唯一租约、外部操作许可、消息与独立审核，不能把控制端代操作算成客户端自主完成。

## 最短现场流程

1. 用 `vibekits.simulator.connect` 连接指定 ID，核对 `connected`、原 ID、主机名、已知 SSH 指纹和仿真许可。优先查目标工具的 `vibekits.simulator.catalog` Schema。远端应用版本用 `vibekits.simulator.call` → `vibekits.device.applications` 读取；macOS 记录 Bundle ID、`build`、路径，Windows 登记的 `DisplayVersion` 可能只到 `1.4.127`，必要时用一条短、只读的 `ssh_exec` PowerShell 从**实际运行的 EXE**读取 `ProductVersion/FileVersion` 和 Authenticode。不要从应用展示名、目录名或旧文档猜 build。
2. 从 KEMI 商场公开列表/详情读取当前平台的稳定包名、整数 `version_code`、下载 URL、精确字节数和 SHA-256；例：`GET https://kemi.newlinksz.com/kd-api/api/store/apps?os=windows|macos&keyword=...`，详情对象可能在 `data.app`。只比较同包名、同 OS 的真实本机 build 与商场整数码。**同版或本机更高即结案“已是最新/拒绝降级”**，零下载、零安装；本机 build 不明则先查清，不把未知当旧版。可用仿真单帧截图补充应用中心“已是最新版本”的 UI 证据，但截图不代替版本读取。
3. 确有更高版本时，先核对目标包为当前平台可安装格式、可信 HTTPS、大小、SHA-256 和官方签名。由目标机已注册的 `vibekits.network.download` 下载，设置 `expectedSha256`、`maxBytes`，复核返回的本机绝对路径、实际字节数和摘要。控制端传包只作经授权的备用渠道，落地后仍由目标机重算哈希/验签；大包 SFTP 失败时参考 `channel-recovery.md` 的一次性 TLS 单文件方法，不重编、不盲重试。
4. 只有当前目标工具 Schema、用户授权和签名任务执行范围都允许时，才调用 `vibekits.device.app_install`，传入目标机**已下载的绝对路径**、`sha256`、`expectedIdentity`；Windows 还按实际安装形态传精确 `expectedRegistryKey` 或经过证明的便携事务参数。macOS 的现有安装桥仅接受单 `.app` 签名 ZIP，要求 Gatekeeper 通过、新旧 designated requirement 相同且新版本更高。Windows MSI/Inno/便携是不同执行合同：不能把 `.exe` 扩展名或同证书当作可安全覆盖的证据；未知便携包、服务/安装目录迁移、未完成授权备份与回滚门禁时停止，报告具体阻断。应用中心 `downloadAndOpen` 只证明安装器被打开，**不是**静默安装完成回执。
5. 安装动作可能关闭当前 VibeKits 或办公通道；先保留原路径、安装身份、办公 ID、有效授权和回滚材料。断线后优先用原仿真 ID 回连；仿真确实离线时按 `channel-recovery.md` 检查，办公 ID 是同机备用通道，不能由仿真 ID 推算。最终从目标机实际运行文件核对新 build、签名、原办公 ID/授权、应用启动与房间心跳。安装器退出码、下载成功、网页“最新版”均不能单独证明更新完成。把版本前后、哈希、签名、原双 ID、失败/回滚和真实结果写进验收记录。

## 已验证的分支与边界（2026-09-30）

六机通用房的四台 Mac 远程办公均为商城 build 383，两台 Windows 均为商城 build 384；4456560334 的仿真截图里应用中心显示“已是最新版本”。因此本轮**没有发生远程办公安装**，正确处置是同版结案，不能复述为“一分钟升级成功”。这也没有验收未来新版本出现时的六机自主更新。Windows 非交互 SSH 里 `RustDesk.exe --get-id` 返回空时，只能记“此读取方法未取得 ID”，不能据此判定办公 ID 丢失；需经原办公应用通道另验。

先前 Windows 58 的 **VibeKits 自身** dev346 覆盖升级是另一项已完成的仿真操作：内外层 Authenticode Valid、独立交互会话计划任务安装返回码 0、原仿真 ID 4240650696 回连并上报 dev346；xzl 6192992780 使用相同签名包、经受限 TLS 转送后原路径升级和回连通过。它证明仿真渠道能做已验证包的更新，不能据此推定 KEMI 远程办公当前便携包的覆盖事务已经通过。具体日志与 SHA-256 见 hbbv `docs/47_DEV346_SIX_DEVICE_ACCEPTANCE_2026-09-30.md`。

## 六机现场分流与同事操作（2026-09-30）

项目源码的 `tool/fleet_remote_office_update.py` 将六个冻结仿真 ID、主机名和 SSH 指纹一起核对；默认只读，`--apply` 仅在商场整数 build 严格高于目标机实际 build 时才进入下载安装。外部控制端须先确认本机 VibeKits 回环桥接正在运行；覆盖本机 App 时端口可能改变或暂时 `ECONNREFUSED`，待原 ID 和桥接恢复后再运行同一命令，不能把瞬时断连当成六台设备离线。操作脚本与实测记录在 VibeKits `tool/fleet_remote_office_update.py`、`docs/acceptance/SIX_DEVICE_SIMULATOR_MARKET_UPDATE_2026-09-30.md`，云端备份在 hbbv `tools/`、`docs/49_...md`。

Mac `1321656264` 的 `vibekits.device.ui_inspect` 返回 `macOS Accessibility authorized=false`，这只阻断读取/点击原生控件；`vibekits.device.applications`、`vibekits.network.download`、`vibekits.device.app_install` 是独立的仿真工具，不需要先用控件点击安装按钮。Windows 没有 Mac 原生控件接口，也同样使用这些独立工具。六台分别用不存在的包路径调用 `app_install`，均从目标机返回“安装包必须是目标机上已下载的绝对文件路径”，证明安装门禁可达且未执行安装；这不是有效签名新包的成功覆盖验收。若任务确实必须操作 Mac 原生界面，辅助功能授权仍应由设备持有人通过系统设置完成，不编辑 TCC 或伪造点击。

Windows 当前公开的远程办公 `+384` 包经 SHA-256 核对是 RustDesk 便携包装器，而已安装的两台使用 `...\\Uninstall\\RustDesk` 登记身份。当前 `app_install` 对 Windows 的通用执行合同仅覆盖已签 MSI、Inno `_is1`，另有一个固定旧便携包 `+369` 的专用签名任务事务；不能把未来新便携 `.exe` 直接作为 Inno 安装器运行。遇此组合先返回 `installer_format_unverified`，记录包格式、实际旧/目标 build、原办公 ID、旧授权、停机与回滚证据，由开发者补齐并真机验收便携事务后再重试。不要用 `--silent-install`、`--update` 或 SSH 脚本绕过安装门禁。实际同版时六台直接报告 `current`，不下载、不安装。

Windows `+384` 商城包的只读格式核验还发现入口名大小写差异：数据段文件记录是 `rustdesk.exe`，尾部入口是 `RustDesk.exe`。在 Windows 语义下按不区分大小写匹配、返回归一文件记录路径后，95 个文件可完整解压并逐项核对 MD5（69,122,720 B）。这只修复解析，不是安装桥支持新包；未来包仍须逐包验签、哈希、停机与回滚。若解析器测试在 macOS 默认 `/tmp` 报 `REPARSE_OR_SYMLINK_PATH`，先按本机环境规则选一个非符号链接的真实临时目录设置 `TMPDIR` 后重跑，不能移除产品的符号链接拒绝逻辑。
# 回滚现场补充（2026-10-01）

旧进程已经停止后，即使只在候选目录换名阶段失败，恢复旧目录也必须重新启动旧App。目录恢复不等于服务恢复。605/249的独立交接脚本已补这一分支，隔离真实文件系统故障测试验证了候选目录不存在时旧内容完整恢复并调用旧App启动；该测试不代表正式设备已完成故障回滚验收。

检查每个平台的实际安装执行器，而非只看事务类或测试数：Windows OfficeUpdateTransaction当前只有日志核心，无生产执行Host，不能声称支持真实自动回滚。Mac内置更新器需同时检测打开失败与打开后进程退出，并保留失败包用于诊断。回包丢失时先读事务与当前进程，禁止重复安装或并发回滚。

模型Key文件存在不等于智能体可用。605新旧凭据文件存在且权限600，但当前DeepSeek路由要求的字段不存在，真实任务返回MISSING_CREDENTIAL；报告默认能力/真实模型失败，禁止输出Key、复制别台Key或伪报Harness已就绪。

凭据诊断补充：records/payload/secret是官方凭据文件允许的一种记录结构，不能把没有明文API引用误报为整台设备完全没有凭据。先核对实际选择的provider及该provider在凭据服务中的解析结果，区分API Key路由和账户路由；本轮确定事实仅为deepseek-official真实请求MISSING_CREDENTIAL，尚未证明升级丢失Key。

Windows路径补充：xzl实际注册的办公安装位置为C:\\Program Files\\KemiRemote，而旧便携预检冻结的是C:\\Program Files\\RustDesk。必须读取实际注册身份、进程和签名再形成事务，不能以固定目录或固定D盘要求处理全部机器。此差异目前是实现缺口，不授权跳过安装格式、签名或回滚门禁。


## Windows 同源构建恢复补充（2026-10-01）

- PowerShell 执行策略按实际解释器和作用域核验。本次 58 的 Windows PowerShell 5 为 Restricted，既有 PowerShell 7 有效及 LocalMachine 均 RemoteSigned，其他作用域 Undefined。已通过现有 PowerShell7 正常 -File 执行固定准备脚本，无策略修改或绕过参数。此现场差异不能泛化为遇到拒绝就换解释器；有组织策略、授权拒绝或安全确认时保留边界，使用真正已允许的既有入口。
- 离线 enforce-lockfile 报很多“版本未变化”但需变更时，先比较 PUB_HOSTED_URL、锁文件 URL 与缓存来源。本次 Mac 冻结包为 pub.flutter-io.cn，Windows 默认 pub.dev；只按冻结源设置构建进程的包源，不删锁文件或换依赖版本。修订后的实际构建终态仍须单独读取。
- 复用旧平台输入清单时核对新 lib 文件和 native/harness 顶层 mjs。本次补齐941项客户端输入与16项Harness源模块；不能遗漏集群任务运行器、便携更新Host/事务及MCP入口，也不能把Mac Node或平台模块直接搬到Windows。实际旧Windows打包目录仍是DSH0.1.7，候选需要0.2.0，须按既有准备脚本生成并核验平台运行时。
- 计划任务 Ready、无cargo/rustc且日志^C/退出3221225786表示已终止，不是仍在编译。保留首败日志、核验无竞争任务及精确runner哈希后复用原缓存恢复同任务。本次原生Release11m50s结束、退出0；Windows App签名安装及六机稳定仍未通过。
- --vibekits-harness-protocol退出0不等于协议健康：本轮新EXE命令经IPC询问旧后台，得到ok=false/control_response_invalid。须核对真实服务响应，在新后台部署后重验，不能只用CLI退出码填通过。

对应实现与原始结论见项目 tool/cluster_windows_dev368_prepare.ps1、tool/cluster_windows_dev368_build_revision3.cmd 和 docs/acceptance/WINDOWS_DEV368_RESUME_2026-10-01.md。

### 2026-10-01 Windows dev368 构建、签名准备与中断恢复

只使用原仿真ID核验设备与主机指纹。控制端同事短暂更新会清空连接表，不代表远端构建失败；恢复后重新connect原ID并读取同一个任务、日志与退出文件，禁止重复启动构建。58本次原生Release及Windows Flutter Release均退出0，实际主程序1.9.0-dev.368+2368；依赖锁中的pub.flutter-io.cn与Windows默认pub.dev不一致导致首次enforce-lockfile失败，使用原缓存与进程级原镜像地址修复，未修改锁或升级依赖。Windows Harness仍旧0.1.7时，需要通过成熟prepare_harness_runtime.ps1准备该候选要求的0.2.0-rc.2及Windows模块，不可复制Mac模块。

复制含近三万运行时文件的候选可能超过SSH观察预算，exit255不能直接判复制失败。本轮远端仍完成复制与签前清单；恢复后真实清单224项、20项未签，先核对目录、进程、文件和hash，不重复解压/复制。PowerShell5把ConvertFrom-Json数组包在@(...)中可能造成count=1；先按真实JSON数组及当前引擎展开检查，不误报文件遗漏。签名在caucy的WTS Active会话1通过固定GUI启动器进行。SSH截图黑屏则使用绑定本次signtool PID的已有受限Session1截图程序；截图实际确认空PIN框后展示给签名人员，仅人员输入PIN。

目前这些是构建与签名准备证据，不是最终签名、覆盖升级或六机长期稳定通过。只保留已验签原App及回滚点，签名未完成不得打包发布。Mac132本次原仿真ID的普通与强制中继均返回transport_failed/Remote desktop is offline，办公372799163界面持续连接且日志实际返回offline；这是通道失败证据，不等于物理电脑关机，不能假装已经访问目标。


### 2026-10-01：硬件令牌输入后，外壳签名仍因时间戳网络失败

不要把 PIN 输入完成、内层签名通过或安装包生成解释为外壳签名成功。此次 dev368 内层 224/224 通过，外壳 SignTool 却报 timestamp server could not be reached or returned invalid response，退出 1，安装包保持原未签 SHA-256。先保留失败日志和未签包，禁止发布/安装，不重复编译。

按 DigiCert 官方排障文档检测 `http://timestamp.digicert.com/timestamp/health/heartbeat`；HEAD 根网址不是有效健康检查。本次 Windows58 DNS 解析官方地址正常，系统默认本机代理转发健康请求返回 502，同机 curl 直连健康请求返回 204，证据指向本机代理路径。不能直接推断 DigiCert 服务整体宕机。

诊断应仅输出代理主机/端口、是否代理、DNS、健康 HTTP 状态，不输出代理账户、认证头、配置令牌。不要删除应用配置或重置证书。沿用原官方时间戳地址、固定 helper、原证书和冻结候选；网络调整只应在已授权范围内精确作用于该域名，并保存原值、处理并发修改、结束时恢复。新进程可能再次要求 PIN；先绑定新 PID、确认活动桌面、展示输入前空框截图，再由人员输入，不能沿用旧窗口证据或代填。

当前记录仅确认故障定位，第二次尝试正在等待令牌输入。签名恢复、代理恢复和安装可用性还未验收，不能将本条称为已经成熟验证的更新成功方案。执行结果以项目 `docs/acceptance/WINDOWS_DEV368_RESUME_2026-10-01.md` 后续证据为准。


## Windows 更新排障补充（2026-10-01）

遇到 SSH 正常但 SFTP 失败、安装返回 1 且无日志、错误 4551 或 CodeIntegrity 3033/3077、升级期间 SSH 255 时，读取 [本次排障实录](windows-update-incidents-20261001.md)。其中区分已验证成功和待验收，不关闭策略、不盲目重复安装。


Mac同身份原位覆盖、SSH255结果回查和无Xcode现场处理，参见[已验证步骤](mac-atomic-update-lessons-20261001.md)。只使用原仿真ID，区分实际更新、心跳和模型验收。
