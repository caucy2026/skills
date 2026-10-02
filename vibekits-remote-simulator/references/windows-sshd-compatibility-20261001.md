# Windows SSHD 兼容性排障与验收

## 当前现场事实

xzl 原仿真ID6192992780、办公ID159974026、用户zjc。覆盖更新前由登录用户运行 C:\vk-build\sshd\sshd_config_syskey 对应的自定义sshd，系统服务此前也是Stopped，但原ID真实SSH、SFTP有效。修正签名包已进入安装日志阶段。更新后仿真返回remote_disabled，办公通道可连接；现场显示“系统已授权，但SSH端口22尚未就绪”，只读Get-Service确认系统sshd仍Stopped。不能推断用户没有确认。OpenSSH/Admin最近5项为2026-09-27的CreateProcessW error5/posix_spawn，属于旧记录，不能当作10月1日本次启动根因。新版实际版本、安装exit及本轮sshd启动日志仍待读回。

## 官方资料核对（2026-10-01）

- 微软推荐系统内置Feature on Demand，前提至少Windows10 1809或Server2019；GitHub独立发行与内置版本可能不同：https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse
- 微软确认Server/Client/libcrypto版本混用可造成1053；独立包需核对组件配套，不机械只安装Server：https://learn.microsoft.com/en-us/troubleshoot/windows-server/system-management-components/openssh-server-service-wont-start-error-1053
- 微软确认部分系统更新后的1053/1067/7034可能与ProgramData/ssh及logs目录权限相关。必须依据对应版本、事件和实际ACL诊断，不能给Everyone写权限或关闭保护：https://learn.microsoft.com/en-us/troubleshoot/windows-server/system-management-components/error-1053-1067-7034-after-update-openssh-doesnt-start
- Win32-OpenSSH项目建议在无正在使用的目标服务时用精确sshd调试模式获取启动原因，并核查文件权限：https://github.com/PowerShell/Win32-OpenSSH/wiki/Troubleshooting-Steps
- 现代发行默认ETW，Admin记录错误、Operational记录信息；按版本选择事件日志或现有文件日志：https://github.com/PowerShell/Win32-OpenSSH/wiki/Logging-Facilities

## 研发修复约束

不能再把UAC拒绝和脚本执行失败合并成一个泛化错误。每次启用记录runId、系统build/架构、sshd及配套组件实际路径版本、服务账号/启动参数、配置文件路径、sshd -t结果、启动退出码、普通错误输出与最新匹配事件、最终监听状态。只输出与故障相关的信息，不记录密钥或完整凭据配置。

先识别已有工作的SSH通道，区分系统服务与自定义进程；升级不得杀死原唯一工作通道后盲目改用标准服务。保留原主机key、公钥授权、用户和监听范围。现有通道可用时先完成实际认证/传输，不以服务Stopped认定整台机器不可用。新启用只有在授权有效、配置校验和实际监听/登录通过时才报告成功。失败保留本轮诊断及回退点，不无限重复弹管理员确认。

## 逐项验收（尚未全通过）

1. 内置FOD、独立安装版、自定义已运行进程分别识别正确；至少实测58及xzl，不据两台结果宣称所有Windows版本兼容。
2. 用户确认后脚本失败，界面显示实际阶段、退出原因和日志定位；拒绝则单独显示拒绝。
3. 匹配组件版本、配置语法错误、目录/host-key权限错误、服务存在但端口不同分别诊断；不修改无关配置或扩大监听。
4. 原已授权版本覆盖升级，仿真ID与host key、配置、公钥授权持续有效；第一次目标端授权门禁仍保留。
5. 应用重启后无需重复授权，原ID实际SSH/MCP/SFTP可用，房间新心跳与任务反馈可查；失败回退恢复原功能。
6. 连续运行、断线重连和网络切换按真实运行证据验收；未实测版本明确列为未验证。

## 后续现场核查

系统服务注册指向 C:\Windows\System32\OpenSSH\sshd.exe，LocalSystem、自动启动。原305字节syskey配置仍保留，端口22、127.0.0.1监听、同一系统host key及SFTP声明。普通用户运行默认sshd -t返回ProgramData/ssh/sshd_config Permission denied，这只证明普通用户不能读取受保护配置，不能证明LocalSystem服务同样无法读取；需要管理员下校验及本轮事件进一步判断。远程办公模拟键入存在IME、Shift字符及队列顺序问题：必须观察完整命令再发送Enter；优先仿真SSH结构化执行，备用办公诊断用短命令与实际文件名补全，不把输入损坏产生的错误归因于SSHD。


## 通用 SSHD 服务决策与当前核验（2026-10-01 21:06）

产品采用微软维护的 Win32-OpenSSH，不另造 SSH 协议实现。系统内置安装和官方独立发行包属于同一实现，但不能把不同来源的 sshd、客户端和加密 DLL 混装。独立发行包必须锁定版本、架构、官方来源和签名，通过目标 Windows 版本实机验证后才能发布；当前尚未选定或部署新的独立发行包。

现场事实：xzl 运行 dev368，PID 26168，路径仍为既有 installed-test。管理员 PowerShell 的 Start-Service sshd 失败；sc.exe start sshd 进入 START_PENDING，随后 sc.exe query sshd 返回 STOPPED / WIN32_EXIT_CODE 1067。管理员执行 sshd -ddd 显示 OpenSSH_for_Windows_9.5、LibreSSL 3.8.2，读入现有配置并成功监听；本地端口探测连接关闭后诊断进程退出。主机 Ed25519 指纹与原记录一致。OpenSSH/Admin 最近三条仍为 9 月 27 日，不能当作此次新故障证据。服务模式失败与前台可启动的差异需要继续检查服务身份、目录 ACL、组件实际路径和系统事件；未确认根因前不大面积重设权限。

### 所有 Windows 共用的生命周期

1. 识别 Windows 构建和架构，读取现有服务二进制路径、版本、运行账户与已有监听者；禁止仅凭 capability 状态替换能工作的独立安装。
2. 已有健康通道先验证身份、公钥认证和 SFTP；原有授权有效时保持使用，避免每次重连再次弹 UAC。
3. 必须安装或修复时，仅执行固定、签名核验后的维护流程；首次系统授权由目标工作人员或已授权远程办公完成。授权拒绝、安装失败、配置失败、服务退出、身份验证失败分别反馈。
4. 服务由 Windows 服务管理器管理，启动和退出独立于 App 更新。安装前保留配置、主机密钥、公钥授权及原始服务设置；失败恢复原包和原配置，不重建 ID，不删除钥匙串或用户数据。
5. 仿真仍经设备 ID 的 P2P/中继路由；不为恢复开启额外公网 SSH 入口。首次设备同意、白名单和黑名单必须在发放有效会话/SSH 公钥之前执行。
6. 健康定义必须包含：服务运行、SSH 握手、正确主机指纹、批准设备公钥登录、短命令执行、SFTP 往返、App 重启后恢复及持续心跳。仅有端口或心跳不算通过。

### 分项验收与发布门禁

- Windows 58、xzl：旧版本授权后覆盖安装 → 保留两个 ID/名称/配置 → 无重复授权即可重新仿真；完整重启再验证。
- 系统 OpenSSH、官方独立 OpenSSH、已有定制配置分别验收，不覆盖其他项目的 SSH 服务。
- 启动失败有阶段、错误码和可追溯报告；1067 现场必须查清并修复，不能用反复点击授权代替。
- 拒绝首次授权不能建立会话；加入允许列表后正常连接；黑名单拒绝有明确协议反馈；移除授权立即停止新会话能力。
- 升级失败回滚后旧版本仍能工作，原主机指纹和信任保持。
- 未测试的 Windows 版本标为未验证，不宣称“所有版本已支持”。

代码当前补充：harness_system_ssh_service.dart 的提升权限子进程记录 capability/host_keys/configuration/service_start 阶段及错误标识，不再把全部失败混同授权拒绝。此补充尚未编译部署到目标设备，实机通过状态仍为待验收。

源代码回归：2026-10-01 执行现有 harness_system_ssh_service_test.dart，7 项通过；仅证明既有源代码契约、公钥保留/撤销等测试通过，不能替代 Windows 服务实机验收。


### 后续排除与恢复动作（21:17）

ProgramData/ssh 目录 ACL 为 SYSTEM、Administrators 完全控制，Authenticated Users 只读执行；logs 为 SYSTEM、Administrators 完全控制。已检查部分没有发现普通用户写权限，不能直接套用网上 ACL 修复。系统事件明确记录服务多次异常停止（此次检查最近记录累计 30 次），与端口就绪失败一致。

xzl 安装计划任务为 Ready，确认没有正在进行的安装。停止已核对版本路径的 dev368 PID 26168 及其子进程，不触碰远程办公。随后从已验证 rollback-dev346 备份用 robocopy /E /XJ /NFL /NDL 覆盖原 installed-test；未使用 /MIR、/PURGE，也未删除用户配置。由于远程键盘把冒号等符号失真，带 /R:0 参数的未执行命令已清空，没有执行；最终复制沿用默认重试，必须现场监测，若有复制错误及时终止该复制，不允许放任百万次重试。当前复制已启动，尚未核验完成。

远程办公恢复输入教训：远程执行优先仿真 EncodedCommand/上传固定脚本；Office 仅作通道失效恢复。英文输入状态、逐条截图核对及 Escape 清空可避免错误执行。屏幕键盘 Shift 会切换中文输入，不能把它当成未经验证的通用粘贴替代方案；本次尝试未取得稳定符号输入，不能写成成功方法。

21:18 已完成旧版文件恢复：29,935 个源文件，28,208 复制，1,727 跳过，0 失败，85 个额外文件保留；主程序 SHA-256=45F0A91FBAD1B997FB73904E48076ABBEB0642313E82B99B0CE4279D55F242FE，与升级前备份一致。21:22 使用管理员终端 cd 到准确目录后 explorer .，通过普通 Explorer 双击主程序启动；没有直接从管理员终端启动 App。启动与通道恢复仍需进一步核验。


### 已定位的客户端逻辑缺陷

setEnabled 原代码即使 Windows 端口已就绪，仍强制进入提升权限/系统 capability/Start-Service 路线。xzl 升级前使用正常的独立前台 daemon，而系统服务本身停止；启动一个失败的系统服务会使整个启用操作抛错，覆盖原本能用的端点。这是源码中确认存在的逻辑缺陷；它是否解释所有其他 Windows 现场，尚未验证。

源码已改为状态已符合时直接保留现有端点，不在重连时重复提权或替换 SSH 服务；设备身份、公钥验证和首次设备授权仍在建立会话前分别检查。完整业务健康检查仍必须包含认证和 SFTP，监听端口本身不能作为最终验收。此修复尚未编译部署，不能宣称 xzl 仿真已经恢复。

官方 latest release 当前页面明确写 Preview / non-production ready，不能把 latest 当成生产稳定版本直接推送全部设备；通用服务发行包须明确版本和 Windows 支持范围，并通过实机门禁。

## dev369 实际构建与清理记录

通过 58 原仿真 ID 4240650696 校验冻结输入 949 份，实际变动 32 份，全部旧文件先备份在 D:\KEMI-Test\results\v369-source-inputs\before-apply。源码改动保留现有可用 SSH、按注册服务路径选择同源组件，并记录提权失败阶段。当前候选尚未签名和覆盖升级验收，不能据此宣称兼容性通过。

本轮错误：构建入口误用了 dev368 修订2，漏带修订3已验证成功的 PUB_HOSTED_URL=https://pub.flutter-io.cn，造成 119 个包版本未变但源站不同，enforce-lockfile 退出65。保留 first-failed-lockfile 日志，补回原镜像参数继续，不移除锁文件门禁、不升级依赖。另一次 prepare 预检哈希录入重复片段被门禁拒绝，纠正到实际上传 SHA 后通过；Windows SSH 命令引号损坏时恢复已验证 EncodedCommand 参数方式，不把连接成功当作命令成功。后续复用必须从最后成功修订入口开始，而非文件名相近的旧入口。

用户授权清理旧临时构建产物。确认 29357 份普通文件 CRC 与保留的 Vibekits-dev368-r14-notarized.zip 相同，并核查无运行占用后，清理本任务 dev368-r14-fleet-20261001/extracted（1162020 KiB）和 dev368-ssh-source-check-20261001/build（71168 KiB）。保留压缩包、公证记录、源码、测试源和报告、当前 dev369 输入、安装包与回滚产物。两个目标合计逻辑约1.18 GiB。ORICO df 观察可用由22 GiB变为30 GiB；共享磁盘同时存在其他工作，不能把全部可用空间变化归因本次清理。58 此时 C盘约11 GB、D盘约48 GB可用，未删除正在编译的构建树。

签名下一门禁：第一轮必须把内部待签文件与预生成 Inno 运行文件放在同一批，第二轮签最终安装包；保留合法第三方签名，逐文件核验时间戳和完整签名。两轮 SignTool 调用不等于保证硬件令牌只弹两次 PIN。未完成真实签名和覆盖升级前保持待验。

dev369 实际原生 Release 编译已结束：pub-get.exit=0、flutter-build.exit=0，日志用时371.3秒。真实 Windows PowerShell 按 UTF-8 读入冻结脚本后 Parser.ParseInput 返回 SSHD_SCRIPT_PARSE_PASS。PowerShell5 ParseFile 默认ANSI会误读含中文的UTF-8无BOM诊断文本，不能据此断言应用 EncodedCommand 有语法问题。应用传参使用UTF16编码，脚本文件必须明确UTF8读取或带BOM。

暂存实测29645文件、834.10MB全部复制、0失败。签名前 Get-AuthenticodeSignature 全树检查超过单次仿真 SSH 命令时限，连接退出255不能视为业务失败或对方离线；先读回现有 stage.log、precreate-runtime.log、进程，保留候选，改用固定版本 GUI → CMD → PS 在活动会话运行，只恢复剩余清单阶段。禁止重做已成功构建、重复制候选或删除证据。WTSGetActiveConsoleSessionId=1、WTSQuerySessionInformation(ConnectState)=0(Active)；此节点没有query.exe，使用WTS只读核验，不以该命令缺失判断无人登录。

本轮暂存补充错误及修正：只按.node扩展名选择文件会误把依赖里的Darwin Mach-O纳入Windows签名，必须延续PE文件头MZ识别；保留跨平台依赖文件，不通过删除依赖绕过。恢复脚本裁剪时漏定义$main，清单已经生成而摘要失败，补回变量和ProductVersion校验，只完成剩余摘要。PowerShell5中@(ConvertFrom-Json)可能把数组包成一个元素，不能用.Count=1断定清单只有1份；使用既定PowerShell7或直接赋值数组。新候选完整PE计数233：原224份EXE/DLL、8份Windows.node模块、1份Inno运行文件；待签29份。manifest SHA256 D391672CF33B995EE2F1C037E423DF1B5F0653326AD57EB30ABA347DB5BF9F02。误计摘要被纠正，未使用它执行空批签名；全部失败过程保留，不把错误写成成功路线。

签名实际阻塞：成熟 Invoke-KemiAuthenticode.ps1 仅接受受支持扩展名，Windows原生.node即使MZ也被输入门禁拒绝，第一轮尚未调用SignTool。保留attempt01-before-sign-input-extension证据和原助手，不放宽系统安全策略；为每份.node生成独立临时.exe，先验证与原文件SHA一致，纳入同一29文件签名批，签后按SHA校验复制回原.node路径。保留signed-node-copy-map.json可追溯。与.e32临时.exe方式相同，加载路径与文件内容格式不改变；本轮签名和真实启动验证仍必须通过才算成功。若原文件被改动，冻结清单哈希门禁拒绝，不盲目覆盖。

## dev369 latest verified delivery status

Final signing summary: PASS, SignRounds=2, InnerCount=233. Installer size259069384 bytes; SHA256=0D07E46C934AA3E262BA61480233AFCE298614054AFAD4272CA4929002D6E9C0. Inner mainSHA256=21255FD2C0E047B437658770DAA3F0284B7441090041B490785F2EC059ECC994. Certificate and timestamp verified. This does not prove runtime acceptance.

58 original simulatorID4240650696 reconnected with retained host fingerprint. Guarded dev369 installation task registered and started in normal caucy interactive session. Backup and rollback retained. Installation completion and fresh functional reconnect still require verification.

xzl Office159974026 remains reachable. Absolute config path passes sshd -t; relative config path fails despite PowerShell working directory. Native PowerShell Tab completion avoids remote Shift/colon typing corruption. Clipboard paste timed out and inserted only v; do not record as successful route. Foreground daemon launch with absolute configuration produced no immediate error. Fresh simulator6192992780 still returns remote_disabled; daemon launch is not simulator acceptance.

Cleanup: verified redundant extraction and inactive generated test build removed, logical1.18GiB. Latest available space ORICO33GiB, system data32GiB. Shared volume changes are not wholly attributable to this cleanup. Sources, signed artifacts, rollback, reports and active builds retained.

## xzl 原仿真实际恢复（2026-10-02 00:04）

恢复方式：保留旧版 dev346 回退实例与配置，通过已有办公ID159974026启动原系统OpenSSH二进制和原C:\vk-build\sshd\sshd_config_syskey配置的前台daemon；不替换主机密钥、不修改设备允许名单、不关闭系统安全策略。首次原ID6192992780真实重新连接于15:55:27 UTC，随后执行PowerShell成功；再次于16:04:30 UTC原ID重连成功。主机xzl/用户zjc、SSH指纹SHA256:rwYyN4kBR2RGcZ3uDjIudStAMV4F/ss7UYVPmU7IC+0一致，SSH/MCP ready。

实际旧主程序dev346+2346，SHA256=45F0A91FBAD1B997FB73904E48076ABBEB0642313E82B99B0CE4279D55F242FE，普通交互Session1 PID19244；原Relay PID8388。前台sshd PID26328及其子进程使用原绝对配置路径，系统sshd服务仍Stopped。这证明旧路线已恢复，不证明通用系统服务或新版升级通过。仿真恢复后真实cluster.rooms仍报mDNS解析11001、roomsAreLive=false；必须继续修复集群接入，不能把连接成功当作入房成功。

58 当前原仿真ID返回remote_disabled，办公ID238638760实际连接显示离线。已配置LAN测试端口可建立TCP，但ssh-keyscan未取得可信主机密钥，不能据此登录或宣称该IP是同一机器。服务端最后设备档案仍为dev368，最后心跳15:28:13 UTC；安装完成状态和当前运行版本尚未取得。不得重复安装或改变ID掩盖缺少证据。

控制端排障补充：Flutter部分AX按钮点击没有执行预期动作，设备卡菜单的实际坐标“连接”才创建58会话并取得真实离线提示；不要把返回无异常当作已点击成功。办公错误对话框通过Tab+Return关闭，返回原xzl会话。窗口缩放/标题栏坐标错位尚未形成稳定通用办法，不能记为保证成功。

## 升级事故复盘：已证实缺陷与未证实原因（2026-10-02）

必须由本次交付负责的缺陷：旧版 Windows setEnabled 在端点已启用时仍强制提权并修复系统服务，不保留独立工作 daemon；dev369 安装脚本只验证签名、文件、版本及启动请求，未验证原仿真 ID 的实际认证、远程命令和文件传输，回滚分支仅覆盖安装错误而非启动后通道失效。因此安装退出0不能作为交付完成，本轮不得发布为通过。

本次真实日志：xzl 的 OpenSSH/Operational 显示已接受原公钥并成功启动命令会话；过去存在 subsystem request for sftp failed, subsystem not found。当前独立配置已有绝对 Subsystem sftp C:/Windows/System32/OpenSSH/sftp-server.exe，组件确实存在，不能将历史错误直接认定为当前文件传输仍失败。系统服务仍停止，不在健康前台 daemon 占用22端口时盲目启动服务制造端口冲突。

58 原ID仍明确返回 managed Harness access is disabled。未取得安装 state.json/failure.json/install-inno.log，不能认定新版已启动、具体异常来自哪一代码行，亦不能将办公离线直接归因安装器。已请求最小本机启动以恢复入口，同时继续使用 xzl 已恢复的原 ID 排障。

后续发布门禁：独立于被升级 App 的守护流程；安装后有限时间内核验原 ID、原信任指纹、已有授权、真实远程命令和文件传输；未通过须在不删除用户配置和密钥的条件下恢复已验证旧包，并再次验证真实通道。不得仅检测进程或监听端口，亦不得通过重置授权掩盖升级回退。

### xzl 安装器与传输实际复核（2026-10-02）

通过原 ID6192992780读取上次 signed-runtime 安装日志：2026-10-01 20:14:19 Installation process succeeded，Need to restart Windows? No；install-exit.txt=0，install-phase.txt=START_REQUESTED。故安装退出成功与启动后通道可用必须分开验收；现有记录没有自动完成后者。

恢复后的真实 SFTP 下载已通过：C:\vk-build\sshd\sshd_config_syskey，305字节，SHA256=1825a505937df6f0551b2e4ecdc329c3fd64197e507cacd2ebafa43dfd545fb7。传输结果 downloaded=true、原 ID与hostname xzl一致；这是当前文件下载功能证据，不能扩展为最新版更新或六机入房通过。58 同轮核验仍返回remote_disabled。

### 回退后的版本误判已定位并修改

xzl 原ID真实查询：RegistryBuild=2368、RegistryVersion=1.9.0-dev.368+2368，FileProductVersion与FileVersion均为1.9.0-dev.346+2346。文件回退没有恢复注册表，因此只读注册表不能证明升级成功。WindowsClusterUpdateService._registryCheck 已增加真实ProductVersion末尾build与注册表VersionCode一致性核验；不一致即报 installed file and registry build mismatch，不修改设备授权或配置。

真实 Windows PowerShell 对 dev346文件/2368注册值（拒绝）、dev346/2346（接受）、四段数字版本2369（接受）、无效版本（拒绝）返回REGISTRY_FILE_CHECK_PASS。此为实际脚本规则验证；改动尚未编译签名部署，不能宣称新版设备已经包含修复。独立看门狗及完整失败回滚仍待完成。

### 更新完成状态的回退复核（源码回归）

WindowsClusterUpdateService.status 原先仅在 launching/launch_unknown/awaiting_reconnect 阶段检查已安装版本，verified_reconnected 会保留历史完成结论。现已对 verified_reconnected 重新核验实际安装身份、仿真与集群重连条件；回退或检查异常撤销完成状态。保留原安装结果未知时的阶段语义，不自动重跑安装。

定向 windows_cluster_update_service_test.dart 共16项通过，包含已完成后回退、ID变化、授权撤销、一次性上传和不重复安装。首次隔离测试因缺 third_party 本地引用未加载，恢复原依赖目录引用后继续；首轮语义回归发现未知状态被错误改名，调整为仅撤销历史verified状态，最终16/16通过。未升级依赖、未删除断言、未改正式设备授权。此改动尚未进入已签 dev369，成品部署待验。

### 独立升级守护候选（尚未部署验收）

新增 tool/windows/dev369-20261001/Watch-VibekitsUpgrade.ps1，独立于被更新App运行，绑定明确旧包/候选哈希、原仿真ID和一次升级AttemptId。控制端必须在真实认证、命令、文件传输和房间重连后原子提交对应commit.json；超时不把监听口或进程存在当成功。守护仅对精确候选目录停止其进程，安装器仍在运行或文件哈希改变时保留现场，不覆盖；恢复采用同卷完整目录替换，保留.failed现场，避免新DLL残留混入旧包，不碰用户配置/密钥/信任。恢复启动请求仍须原ID独立复验，不能宣称已经恢复成功。

真实 xzl 上传脚本已成功，初稿UTF8 Parser.ParseInput返回WATCHDOG_PARSE_PASS。未运行生产回滚、未集成正式启动器，后续同卷检查补丁需重验；该候选不能直接作为成熟一分钟更新路线。58办公原ID238638760再次尝试显示“远程电脑处于离线状态”，不是仅凭窗口标题判断。

### 经 xzl 核验 58 备用入口（2026-10-02）

132 原仿真ID1321656264返回Remote desktop is offline，办公ID372799163实际连接亦显示离线，按用户既定两通道都不可达时暂缓该机的规则继续其他设备。

从已恢复 xzl 原仿真ID执行既有58地址192.168.3.58的ssh-keyscan，得到OpenSSH9.5主机公钥，计算指纹SHA256:ikZ6NXAH3VFBGooSCeKW0JY9+h0cIcQOzib4fxmvz6M，与58可信记录一致。说明58备用SSH在xzl网络可达，不能再笼统说整机关闭。

尝试通过现有已认证xzl ID隧道建立仅127.0.0.1的转达连接，严格校验原指纹、公钥登录，不复制私钥。xzl SSH明确拒绝目标转发：channel open failed: administratively prohibited。未成功登录58，未读取安装状态；已停止本次临时转发，不修改AllowTcpForwarding/PermitOpen，不换代理绕过该限制。这个新证据定位了备用路径受限点，不能记成恢复成功。

### 守护候选不能直接执行：策略兼容性门禁

守护增加旧包发布者指纹校验、候选签名校验、安装目录与备份/结果目录双向嵌套拒绝以及同卷恢复限制。最新5406字节，SHA256=a8ae5b70a6a179cdfc4f4944f11248333db435d2d84df5008b7152ea5f043b52，上传成功，Windows UTF8 Parser.ParseInput 返回WATCHDOG_PARSE_PASS。

xzl 无 PowerShell7；PowerShell5各Scope未定义策略，实际执行 -File 时系统禁止脚本运行，FullyQualifiedErrorId=UnauthorizedAccess。此次以非法RoutingId和未创建的隔离路径测试前置，未修改真实安装或启动回滚。不能通过ExecutionPolicy Bypass、InvokeExpression重执行同一被拒脚本或改安全设置来宣称测试通过；须将守护纳入可信签名交付并在原策略下复验。当前仅语法通过，计划的正常提交/超时/实际回滚测试尚未执行。

旧dev346主EXE真实Authenticode为Valid，发布者B82824C01226426C2D2BD423F883DCBC999C7E82，恢复保留该身份。最新签名候选包和令牌在58，58入口尚未恢复；不把未签脚本下发当作可用恢复方案。
