# Windows 仿真通道构建与传输排障（2026-09-28）

这些是 58 号 Windows 设备 `4240650696` 的实测故障，不是所有设备的默认状态。先核对当前用户授权、路由 ID、主机名和已记录的 SSH 指纹；不要把历史目录名或连接状态当作实际运行版本。

- `vibekits.simulator.connection_status` 报 `sshReady=true` 只说明控制通道已建立。每次关键操作还要检查 `ssh_exec` 内层 `ok`、`exitCode`、目标主机和命令结果。长命令返回 `exitCode=255`/`Connection to 127.0.0.1 closed by remote host` 后，**先查原进程、固定日志、退出标记和产物**。本次 Cargo 编译在 SSH 响应关闭后仍有 cargo 与多个 rustc 进程，盲目重启会造成双重构建。
- 相反，从短 SSH 命令用 `Start-Process` 启动后台 CMD 后，曾只写出 `started.txt`，SSH 会话结束时子进程消失，没有 Cargo 日志、target 或退出标记。留存尝试日志，确认该精确进程树完全退出，再改用该节点已成功过的同步 SSH 固定构建入口。不要仅凭 `Start-Process` 给出的 PID 声称构建已开始。
- `vibekits.simulator.upload_file` 在此机返回相对路径 `.vibekits-simulator\<ID>\<file>`，实际位于当前用户目录。需要 D 盘工作区时先以远端 `Get-FileHash`/长度核对，再移动到 `D:\KEMI-Test\inbox\<版本>`，复核目标哈希和临时源已不存在。仅有 C 盘的节点采用其项目文档核准的 C 盘工作区，不能机械要求 D 盘。
- macOS 默认 tar 可能把 26 个预期文件打成 52 项：每项多一份 `._` AppleDouble 侧车。**解包前**比较 `tar -tzf` 的实际条目与哈希清单，发现额外项立即拒绝。重新从冻结文件逐项哈希后生成只含预期条目的干净 tar，另记新包 SHA；不要直接解包再删除额外文件。
- Windows 执行策略可能拒绝仓库中的未签 `.ps1`；不要修改执行策略或把报错记成业务源码测试失败。可运行的既有固定 CMD 原生编译路线可按已核来源复用，但 `.ps1` 专项门禁仍标未执行，另以源码指纹、Rust 定向测试和产物验签补证。
- Windows 旧版 APP 能运行是有效正控。若新版孤立 relay 的 `--vibekits-harness-protocol` 返回 `control_response_invalid`，先核对旧控制端、账号和完整启动/IPC 注册流程；不能把退出码 0 当通过，也不能只凭这一条脱离运行态的探测断定新版失败。最终仍要用新版实际进程、同 ID 仿真连接、房间心跳和原授权做覆盖前后对照。

在 58 上，远程办公本机 EXE 后来独立变为签名有效的 `1.4.127+384`；文件时间早于本次 `app_control launch`，不能把版本变化归功于这次启动。`--get-id` 返回办公 ID `238638760`，与仿真 ID 不可互算。安装任务若只有公开 `+369`，应按实际版本拒绝降级，不能为了完成验收覆盖可运行的新版。

## 58 从源码重编 dev336 的新增现场记录（2026-09-29）

- 不能把旧 Cargo target 的成功当成新源码重编。58 新建独立 `rustdesk-harness-relay-dev336-fresh` target，先跑原生定向测试 11/11，再构建 Release。首次同时有另一项完整 Office Cargo 构建时，第三方 `windows-0.51.1` 编译器以 `0xc0000409` 退出；这不足以单独证明是内存争用。保留失败日志、不打断他人任务，等另一构建结束后以 `CARGO_BUILD_JOBS=1` 对同一源码重试，测试 11/11 与 Release exit 0，产物另取 SHA。
- 固定源码归档可缺少 `.gitignore` 排除的构建输入。58 的 dev336 首次 Flutter 构建因缺少 WinDivert 2.2.2-A 头文件失败；只从本机已成功构建的旧版本工作树复制同版本厂商文件，并以明确的头文件和库文件 SHA 核对，不要替换应用源码或重新下载不确定版本。固定版本 Git/gh/Lark/ADB/7zip 运行时也须逐个入包校验。
- Flutter SDK 位于另一个账户创建的目录时可能出现 Git `dubious ownership`。本次只对单个 Flutter 进程设置 `GIT_CONFIG_COUNT=1`、`GIT_CONFIG_KEY_0=safe.directory`、`GIT_CONFIG_VALUE_0=<已核实 SDK 路径>`，没有全局信任目录；`flutter pub get` 后复核 `pubspec.lock` 哈希不变。
- Windows Node 24 不接受把 `C:\...` 绝对路径直接传给 `node --import`。会话重绑定故障注入测试中的本地模块路径须转换为 `pathToFileURL(path).href`；本机和 Windows 真机三组测试均通过后，才重新跑 Harness runtime 准备。
- 新 relay 的独立协议探针在旧 dev232 APP 正占用 IPC 时得到 `control_response_invalid`。在构建期只允许明确标记为 `protocolProbe=deferred`，整包结构检查可以继续，但**安装新 APP 后必须再运行默认在线协议验收**；不可把 deferred 写成 PASS 或永久放宽接受的响应。
- 用 Python 拼 Windows `C:\Program Files\PowerShell\7\pwsh.exe` 时，普通字符串中的 `\7` 会变成 bell 控制字符，使原本可运行的验证脚本报路径错误。生成远端脚本应使用原始字符串或双重反斜杠，上传前打印并核对实际命令。
- 签名前检查活动控制台和现存 `signtool.exe`。58 的 Session 1 桌面已有另一项 KEMI 远程办公签名及 SafeNet PIN 窗口，不能并行启动 VibeKits 签名或把那个 PIN 窗口归功于 VibeKits。先记录本任务候选清单、签名入口与哈希，等待原进程终态；下一次须重新取本次 PIN 截图和运行报告。不得读取或输入令牌 PIN。
- In the dev336 signing preflight, a manifest created by Windows PowerShell 5 and validated by PowerShell 7 produced different `Sort-Object FullName` order for Git command files. Comparing rows by index yielded a false `PRE_SIGN_MISMATCH` although each relative path, byte count, and SHA-256 matched. Build a map keyed by relative path and reject duplicates/unexpected paths; do not rely on cross-version sort order.
- A `[string[]]` batch passed to an external `pwsh.exe -File helper.ps1 -Path $batch` expanded into separate positional command-line arguments, and the helper rejected the second file before SignTool launched. Invoke the already validated helper directly in the same PowerShell process with `& $helper -Path $batch`, then check its exit code and versioned report. Preserve every failed run directory; never count a pre-SignTool failure as a signing attempt or retry against a possibly modified candidate without rechecking the frozen manifest.
- Hardware-token ownership is live state. The earlier Office SignTool exited, but another KEMI Remote Office SignTool appeared in Session 1 before the VibeKits v4 launch. Recheck the exact process command line immediately before launch, and do not run concurrent signing jobs against the same token.
- In dev336, the original Authenticode helper reported five Microsoft `System.*.dll` files as the Microsoft Catalog signer after signing 175 files. `CreateFromSignedFile` showed the expected product certificate embedded in each file, and `signtool verify /pa /all /v /tw` showed a valid DigiCert timestamp with exit 0. Do not re-sign those five merely because `Get-AuthenticodeSignature.SignerCertificate` resolves to the Catalog certificate. A versioned helper must compare the embedded signer and require SignTool `/tw` evidence.
- The same helper's per-file `Bytes` field used a `FileInfo` captured before signing, while its `Sha256` was calculated after signing. A continuation precheck that compares current signed length to that field falsely reports drift. For previously signed files, compare the frozen post-sign SHA-256 and independently verify the signature; for untouched files, compare the original byte count and hash. Preserve failed run IDs and do not blindly re-sign a partially signed batch.
- During dev336 remaining-file signing, screenshot and then SSH/MCP tunnels reset; the same simulator ID became `Remote desktop is offline` while the controller's local VibeKits process stayed running. `connection_status` had briefly reported `sshReady=true` even though actual SSH/MCP calls reset, so test real calls. After reconnection, inspect the independent Windows signing process and versioned reports before any retry; never infer PASS or FAIL from a stale tunnel status.

## 58 reboot and resource incident (2026-09-29)

- The host rebooted at 09:37 after the dev336 signing job stopped at `SIGNING_REMAINING_49`; no final 224-file report exists. Preserve the partially signed candidate and verify each previously signed file before any continuation. The running VibeKits after reboot was still dev232, so an available simulator channel does not prove dev336 was installed.
- Windows System event 2004 at 09:23 and 09:28 recorded low virtual memory with `ToDesk.exe` using about 10.8 GB; event 7023 reported the page file too small, and Kernel-Power event 41 confirmed an unclean reboot. The page file was 2 GB. Signing overlapped these events, but the logs do not establish SignTool as the memory consumer. Before any rebuild, check free physical memory, page file, D: space, ToDesk growth and competing build/sign processes; run one build at a time and stop before memory is exhausted.
- The old app crash log contains `读取 Windows Credential Manager 失败（0）` from cluster startup, but a Windows Credential Manager test launched through simulator SSH runs in a noninteractive logon session. On this host a direct Win32 `CredReadW` P/Invoke from SSH returned 1312 (`ERROR_NO_SUCH_LOGON_SESSION`), while the Dart FFI adapter surfaced 0. Do not treat an SSH credential test as an interactive-app acceptance result or map error 0 to “not found.” The attempted leaf-FFI change did not pass and was reverted. Reproduce and verify credential behavior in the actual logged-in app session without exposing stored secrets.
- A Flutter SDK copy named `flutter-3.41.9-build157` lacked `bin\cache\dart-sdk\bin\dart.exe` and repeatedly ran `update_engine_version.ps1` without entering tests. Its exact test process tree was stopped after proving no progress; use the existing complete `flutter-3.41.9-clean` SDK after checking its Dart executable and snapshot. Do not start a second Flutter job while the first remains alive after an SSH tunnel drop.
- When cloning a versioned signing chain, verify the **entire** launcher EXE → CMD → PowerShell path after compilation. On 58, replacing lowercase `vibekits336-inner-...-06` changed a new log path but missed uppercase `Resume-Vibekits336-inner-...-06` in the launcher/CMD. The new GUI launcher therefore executed the previous script, even though the versioned V7 script itself was correct. Inspect the live parent/child command lines and unique attempt ID before attributing work to a new run; preserve the original run record and describe the actual script that ran.
- SSH screenshot on this node returned a valid but all-black PNG. A fixed Session 1 C# helper launched through `vibekits.device.app_control` captured the real desktop at `D:\KEMI-Test\results\vibekits-dev336-windows\vibekits336-inner-20260929-07\pin-session1-before-input.png`; the checked image showed an empty SafeNet PIN prompt. The user must enter PIN on the target machine; never read or type it over the controller. After presenting the image, track the same signing attempt to its final report.

## 58 安装器切换失联及局域网恢复路径（2026-09-29）

- `app_control launch` 能在 Session 1 启动固定的签名脚本，但**不能据此推断**它启动的更新脚本在 VibeKits App 自己关闭后仍会存活。dev336 的受控安装脚本写出 `PREFLIGHT_PASS`，随后关闭旧 App，仿真通道立即离线；局域网复核显示脚本、旧 App 均不再运行，安装器从未启动，新安装目录不存在，自动回退亦未运行。设计安装器/自更新时，要先在可恢复的测试机证明独立更新进程能越过父 App 退出，再允许它关停 App；固定脚本中的“超时回退”在进程本身会被杀掉时没有保护作用。不要把 `app_control launch` 的成功响应或旧进程退出写为安装 PASS。
- 58 的项目可信记录给出 LAN `192.168.3.58`、ED25519 `SHA256:ikZ6NXAH3VFBGooSCeKW0JY9+h0cIcQOzib4fxmvz6M`。仿真离线后，按 `kemi-windows-device-lab/references/node-security.md` 先核 TCP/22、实时 keyscan 与固定指纹，再用已有 `kemi-test` 公钥账号和严格主机密钥检查读取 `D:\KEMI-Test` 状态；不要用 `StrictHostKeyChecking=no` 或猜密码。当前 `kemi-test` 是非管理员的独立测试账号，没有已登录 `caucy` 的交互令牌；从 Session 0 启动 App 不能证明原仿真 ID/授权恢复，也不能跨账号伪造。必须由已登录用户在本机启动原 App，或使用事先验证且属同一用户的独立交互更新代理。
- 若仿真 `connection_status` 仍报 `sshReady=true` 而实际调用失败，先用实际 `ssh_exec` 验证，再 `disconnect`/`connect`。重连返回 `Remote desktop is offline` 时，优先读 LAN SSH 的版本化状态和进程事实；不得因观察超时重启第二个安装器。恢复旧 App 后核原 ID、进程版本、授权与服务，再改用独立更新入口。旧版完整目录与已签 dev336 安装器保留，不删除用户配置。

## 619 单 C 盘包传输与独立任务探针（2026-09-29）

- 619 的仿真 SSH 命令可用，但 `vibekits.simulator.upload_file` 对 37 B 探针和 258 MB 安装器都报 `sftp_upload_failed: /usr/bin/scp: Connection closed`。先用小文件区分传输子系统问题和大文件问题；不要反复重试同一上传。该机仅有 C:，用户已明确要求按设备实际盘符调整，本次只暂存于 `C:\KEMI-Test\inbox\vibekits-dev336`，不因历史 D: 示例去改分区或强行挂载。
- 未认证的 LAN HTTP 单文件服务被平台自动审批拒绝，不能换命令绕过。可用更严格的已授权单目标传输：只允许目标现行 IP、随机一次性 Bearer 令牌、短时 HTTPS、已有测试 CA、无目录列表，远端用 CA 验证主机名并对最终安装器再核 SHA-256 与 Authenticode。619 的 Schannel 对没有吊销发布点的私有测试 CA 报“revocation status unknown”；`--ssl-no-revoke` 仅关闭此吊销查询，同时保持 CA/主机名验证。此次 258640576 B 传输、哈希与签名通过后，监听自行关闭并清除一次性令牌。临时端口 57098/TCP 的已释放记录见 hbbv 本机端口台账。
- 为避免 58 的 App 子进程死亡，在 619 **不关闭旧 App**时测试 Task Scheduler 的当前用户交互任务：由 Session 1 的 `zjc` 注册/启动探针，系统服务执行时写出 `user=zjc, sessionId=1`；确认 `LogonType=Interactive` 后按精确任务名注销。此结果只证明任务计划程序接管了当前用户任务，尚未验证 App 退出后的更新存活。后续安装前先用无损的独立任务生存测试或首台设备门禁，不可直接把探针 PASS 当升级 PASS。

## 58 双通道恢复、凭据读取和增量构建（2026-09-29）

- 旧 VibeKits 被其 `app_control` 子脚本关闭后，仿真 ID `4240650696` 离线，但办公 ID `238638760` 仍在线。经 KEMI 远程办公连接到**已核身份的同一台 58**，在 `caucy` 桌面通过资源管理器启动保留的旧版 EXE，原仿真 ID 再次返回 `connected=true`。这证明双通道可用于抢救原交互用户的 App；独立 SSH 账号 `kemi-test` 只能只读观察，不能代替 `caucy` 启动同一身份。
- 用 Task Scheduler 的 `LogonType=Interactive` 先做无副作用探针，实际写出 `caucy|Session 1`，再让同一用户的独立计划任务执行升级。此次安装器退出码 `0`，新 EXE 落盘且签名有效；五分钟内未得到同 ID 验收标记，任务按脚本恢复旧版，原 ID 重连。要分别记录“安装器成功”和“运行验收失败并回退”，不能合并宣称成功。
- 新版试运行的 `app-crash.log` 在 `ClusterTaskSettings.load` 记录 `读取 Windows Credential Manager 失败（0）`。Dart FFI 分两次调用 `CredReadW` 与 `GetLastError` 无法可靠读取同一 native 调用的线程错误，`0` 不是“凭据不存在”。针对性修复在 Windows runner 的同一个 MethodChannel 回调中连续执行这两步，仅 `ERROR_NOT_FOUND=1168` 返回缺失，其余错误保持 fail closed；不可删凭据、换 ID 或重装掩盖问题。真正通过仍需安装后读旧凭据、原 ID 和 Harness 验收。
- 58 的 Flutter SDK `D:\KEMI-Test\tools\flutter-3.41.9-clean` 属于 `kemi-test`，交互 `caucy` 构建时 Git 报 `dubious ownership`。只在该构建进程设置 `GIT_CONFIG_COUNT=1`、`GIT_CONFIG_KEY_0=safe.directory`、`GIT_CONFIG_VALUE_0=D:/KEMI-Test/tools/flutter-3.41.9-clean`，不要改全局 Git；同源增量 Windows Release 用时 337.7 秒、exit 0。执行本地无 Zone.Identifier 的项目 `.ps1` 校验时，可仅对该 PowerShell 进程使用 `RemoteSigned`；保持机器策略不变。若任务脚本“启动成功”但没有日志，先查计划任务 `LastTaskResult` 和独立启动标记，别反复发起构建。
- Windows PowerShell 传给 Robocopy 的 `/LOG:` 不能写成 `/LOG:(Join-Path ...)`；它会返回 16，目标保持空目录。先核精确目标为空，再新建版本化脚本，把 `'/LOG:' + (Join-Path ...)` 作为**单个字符串参数**传入。旧已签候选和失败证据保留，V2 复制状态 PASS 后才替换本轮改变的 `vibekits.exe` 与 `data\app.so`。


### 2026-09-29 58 dev340 自更新启动器：当前卡点与安全处理

58 的已签 dev340 安装包及独立安装/回滚脚本预置后，`vibekits.device.app_control` 启动 4 KiB C# 包装器返回 PID，但没有生成 `install-58-schedule.json` 或 `install-58-result.json`，旧 dev339 仍在交互 Session 1；不能据包装器 PID 声称安装已开始。随后直接在 `caucy` SSH Session 0 执行上传的 `Schedule-Vibekits340-58-20260929.ps1`，系统返回 `UnauthorizedAccess` / “此系统上禁止运行脚本”。这是执行策略门禁，不能用进程级 `-ExecutionPolicy` 覆盖，也不能将脚本文本改走 `Invoke-Expression` 绕过。应沿用该机已允许的原生、可审计启动方式（例如已签名的安装器与 Task Scheduler 的原生命令或签名脚本），先确认独立进程确实注册且落下结果文件，再允许它结束旧 App。当前安装未启动，实际进程仍为 dev339；回滚点与原 ID 可用。


### 2026-09-29 58 dev340 已验收的双通道自更新路径

在原仿真 ID `4240650696` 可调用时，先冻结原进程路径、旧版 dev339、安装器 Authenticode 有效与 SHA-256 `FC60C3F6C96E939A87C89BB5BA71FA23B72BCBE3C4BB201D5B5492C858B28213`；用 `robocopy` 把运行目录复制到 D 盘回滚目录，比较主 EXE SHA-256 与目录字节数完全一致。58 禁止运行未签名 `.ps1`，因此没有改变执行策略，而是通过允许的 `-EncodedCommand` 调用 Task Scheduler cmdlets，在原 `caucy` 用户的 Interactive LogonType 下注册**直接执行已签名 Inno EXE**的独立任务。`LastTaskResult=267009` 只是运行中，不能记 PASS。安装器 `/LOG` 记录 RestartManager 检出旧版主程序、relay 和三个同目录 Harness Node 占用。通过原仿真 SSH 只读确认五个 PID 都指向 `D:\KEMI-Test\installed\Vibekits\`，再注册一个独立原生 `taskkill.exe /PID ... /F` 任务只关闭这五个已核进程。仿真随之断开，但办公 ID `238638760` 的 KEMI 远程办公桌面可访问同一 `LAPTOP-LUOPP1CH`；在真实桌面看到 Inno 的 `Try again / Ignore / Cancel` 提示，选择 **Try again** 后安装器继续解包，不能选 Ignore 掩盖锁文件。安装结束后通过办公桌面的资源管理器沿 `D:` → `KEMI-Test` → `installed` → `Vibekits` 找到并启动 `vibekits.exe`。注意远程办公的剪贴板粘贴曾超时、键盘布局把路径输入错乱；不反复盲输路径，直接用资源管理器逐级点击。不要把连接窗口在线等同桌面已连。

随后先 `vibekits.simulator.disconnect` 清理旧连接缓存，再 `connect` 原 ID；返回新的 `connectedAt`、同主机名/SSH 指纹、`p2p_or_relay`、SSH/MCP ready。真实 SSH 查询实际运行进程在 Session 1、产品版本 `1.9.0-dev.340+2340`、主 EXE SHA-256 `9172AF289700587F6A6DC0565B7E6A3CC671C82A0B4EE530F669C8052E1C4916`、Authenticode `Valid`、安装计划 `LastTaskResult=0`。hbbv 六机房实时页同 ID/办公 ID `238638760` 在线，档案版本 55，设备描述来源 Harness，App 版本 dev340。以上证明 58 此次覆盖升级和入房恢复 PASS；不证明删除重装保 ID、任务执行通过或另外五台更新完成。过程中 `connection_status/connect` 曾复用旧会话并显示 connected，但 SSH 返回 connection reset；必须清缓存重新连接并执行实际工具调用。


### 2026-09-30 xzl 单 C 盘 Windows：原 ID 仿真自更新并入房 PASS

原仿真 ID `6192992780`、办公 ID `159974026`、主机 `xzl`。先仿真 SSH 验原 dev319 进程、C 盘安装位置及 340 GB 可用空间；**不要复制 58 的 D 盘路径**。58 已签 dev340 安装器 SHA-256 `FC60C3F6C96E939A87C89BB5BA71FA23B72BCBE3C4BB201D5B5492C858B28213`。xzl 的 SFTP 上传即使 37 B 探针也失败，改用已验证的单次 HTTPS 传输，仅允许 xzl 的 LAN IP；Windows `curl` 用已有本机 CA 与 `--ssl-no-revoke`，保留 CA/主机校验，传完关闭临时 52260。下载端核字节/哈希/Authenticode。旧目录先备份到版本化回滚点，主 EXE SHA 与目录总字节完全一致。交互用户 `zjc` 的计划任务执行 CMD：`start /wait` 已签 Inno `/SP- /SILENT /CLOSEAPPLICATIONS /FORCECLOSEAPPLICATIONS /NORESTART`，记录 exit 0，再启动原安装路径 App。不要把计划任务“已注册”、仿真断开或 `app_launch_requested` 单独算成功；重连**原 ID**后，用 SSH 核 Session 1 实际进程、版本 `1.9.0-dev.340+2340`、主 EXE SHA `9172AF289700587F6A6DC0565B7E6A3CC671C82A0B4EE530F669C8052E1C4916`、签名 Valid、原主机指纹不变。随后 `vibekits.cluster.rooms` 查服务与房间，`cluster.apply` 提交六机房申请；网页批准后等客户端自动接入，最终 6/6 在线，xzl Harness 描述在设备详情可见。若仿真真失联，先核办公 ID 是否同机可用，再按双通道恢复流程处理；不能凭连接缓存显示 connected 判断工具可用。

### 2026-09-30 58 dev344 源码包遗漏与固定签名清单

58 的隔离 Windows dev344 源包只带主要 Flutter/Harness 目录，`flutter pub get --offline` 虽通过，但首次 Windows assemble 因 `pubspec.yaml` 引用的 macOS 图标和模型资产缺失而失败；补齐后又在 CMake `INSTALL.vcxproj` 失败。不要只看 MSB3073 包装错误：在构建目录直接运行生成的 `cmake -DBUILD_TYPE=Release -P cmake_install.cmake`，可得到第一项真正缺失文件。本次依次是 `docs/schemas/lmcp-*.json`、`examples/lmcp/future-app.manifest.json`，随后是 pub 缓存 `sherpa_onnx_windows-1.13.8/windows` 缺 `sherpa-onnx-c-api.dll` 和 `onnxruntime.dll`。前者从同一冻结源码按 SHA-256 补入；后者从 58 当前运行、已验收的 dev340 安装目录按哈希 `655888A1A498104BAB697735AAE3A5B82EB09685A3FA8B2367D1718654BC7CFF` / `90BA97C4C96AAD0D75E784239E519486B33603BE6D45E187F836DE1F9BBCBBF5` 复制。CMake 安装脚本单独 exit 0 后，再运行完整 Flutter Release，最终 exit 0；EXE 版本 `1.9.0-dev.344+2344`。后续冻结源包须按 `pubspec.yaml` 与 `windows/CMakeLists.txt` 两份显式资源清单逐项核对，不靠失败后逐个猜。

候选单独复制并盘点得 29,072 个文件、224 个 PE、20 个未签；先前 dev340 的固定签名脚本期望 22 个未签，不能机械复用数字。本次按新清单改成 20，保留 224 总数。文本替换时 `Count -ne 22` 会误匹配 `Count -ne 224` 前缀，将其变为 204；启动前必须回读脚本中的全部总数、待签数、路径及版本。签名启动后仿真 SSH 截图仍可能全黑；本轮复用 Session 1 固定 C# 截图器，绑定本次 `signtool` PID/窗口并核对前景，截图显示 SafeNet 空 PIN 框。PIN 只由用户在设备上输入，不能从进程启动或截图推断签名完成；需等本轮完整报告与验签。

### 2026-09-30 仿真覆盖 dev345：系统局域网授权与旧 App 抢占端口

Mac 原位覆盖后先读独立脚本 `PREFLIGHT_OK → INSTALLED_VERIFIED → STARTED`，再用原仿真 ID 核 SSH 主机指纹、实际进程的 `lsof txt` 路径、`32147/32148` 端口归属、`vibekits.cluster.rooms` 和后台秒级心跳。529 覆盖后 `cluster.rooms` 报 `No route to host`，但从设备 SSH ping 192.168.3.65 成功、HTTPS 端口可握手。仿真截图上有两个叠放的系统“本地网络”弹窗；对 `com.apple.UserNotificationCenter` 做 `vibekits.device.ui_inspect`，上层是无关 86Box，第二个 AXWindow 的文字才是“允许 Vibekits 查找本地网络中的设备”。只对已核准的 VibeKits 按钮操作后，rooms 立即 live/connected、服务端心跳恢复。不要盲点最前方的“允许”，也不要把 macOS 授权门禁误判为服务器路由故障。覆盖升级重新弹出系统本地网络许可违反“旧版授权延续”的理想门禁，需进一步查根因并回归；不可伪造系统许可。

132 覆盖脚本写 `STARTED` 后 `simulator.call` 返回 `mcp_timeout`，后台暂时离线。SSH `lsof -nP -iTCP:32147 -iTCP:32148 -sTCP:LISTEN` 查到端口归 PID 38369；`lsof -p 38369` 的 `txt` 指向 `upgrade-rollback/dev344-before-dev345-20260930.app`，证明是旧版回滚副本进程；dev345 另有 PID 38373 却未绑定端口。只 TERM 经核对的旧 PID，再重启原安装路径的新版；随后一个 dev345 PID 绑定两个端口、`cluster.rooms` 返回 live/connected、后台同仿真 ID 新版本心跳恢复。此类情况不要只看 `pgrep` 显示的命令路径，它可能是已移动 App 的旧进程路径别名；以 `lsof txt` 判断实际加载的二进制。不得终止无关进程或误删回滚包。

Windows 58 长时间的仿真 SSH 命令有时返回 255，原 `robocopy` 仍在后台继续；复制完成后先对比源/候选 29,072 文件与 873,524,487 字节，再扫描 PE，不能看到连接断开就重跑复制。dev345 复制的 Flutter `.plugin_symlinks` 普通目录和旧 `CMakeCache.txt` 原路径需在**新副本**中分别改名保留备份再重建；原 dev344 工作区不动。一次构建任务被 Ctrl+C 中断（Task Scheduler `LastTaskResult=3221225786`），固定退出文件没写出；核查无旧编译进程后保留日志，按同一任务续跑，最终 exit 0。dev345 另冻 224 PE / 20 待签候选；签名必须绑定本轮 SignTool PID、Session1 和空 SafeNet PIN 截图，PIN 只由人在设备上输入，完整验签前不可标 PASS。
