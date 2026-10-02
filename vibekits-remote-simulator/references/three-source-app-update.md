# 仿真通道更新应用：三种包来源与三分钟操作路径

适用：已获授权且目标仿真 ID 在线。先 `vibekits.simulator.connect`，核对 ID、主机名、指纹、系统、仿真许可；调用 `vibekits.device.applications`，必要时读取**实际运行文件**的版本和签名。确认目标应用身份、当前版本、安装形态、运行进程、签名和回滚位置。升级完再核对落地版本、签名、进程/界面、原设备 ID 和原授权。三分钟是熟悉设备且包已就绪时的目标，不是未经验证的完成保证。

## 入口一：用户给 HTTPS 绝对地址（Common 等）

1. 核对 URL 所指平台、架构、应用 ID、目标版本、发布来源，并取得发布方的字节数及 SHA-256。必须 HTTPS；不把网页地址当安装包地址，不靠文件名推断签名。
2. 优先让目标机用 `vibekits.network.download` 带 `expectedSha256`、`maxBytes` 下载。如果 MCP 调用超过回环桥超时或大包传输失联，先查目标机是否已有完整文件；不要重复下载。Mac 可由已授权 `simulator.ssh_exec` 在目标机后台 `curl --fail --location` 到 `.part`，核对 SHA/大小后原子改名。Windows 可先试 BITS；如果 BITS 因 `0x800704DD` 缺交互网络上下文失败，在目标机使用 `curl.exe --fail --location --ssl-no-revoke`；此选项只跳过不可用的吊销检查，不关闭证书链与主机名校验，禁止 `-k`。大包 SFTP `scp: Connection closed` 时改用目标机下载，不反复传同一包。
3. 根据真实包格式调用目标 `vibekits.device.app_install` 的受支持合同，或使用下述平台分支。Mac 单 `.app` ZIP：校验 ZIP、Bundle ID/build、`codesign --verify --deep --strict`、`spctl -a -t exec -vv`，在保留旧版和授权前提下安装；Windows MSI、Inno、便携 ZIP 是三种不同合同，不能把任意 `.exe` 当安装器。Windows Inno 可在已登录用户的交互 Session 1 用计划任务运行静默参数和 `/LOG=...`，然后核对 `LastTaskResult=0`、安装日志和实际 EXE。仅“下载并打开”不等于安装完成。

## 入口二：设备上的 KEMI 商场

1. 通过商场公开 API（如 `GET https://kemi.newlinksz.com/kd-api/api/store/apps?os=windows|macos&keyword=...`）取得相应平台的版本码、包 URL、精确大小和 SHA；同时可在设备应用中心观察同一条目。对比实际安装 build；同版或目标更旧就报告 `current`，不降级。
2. 商场是包来源，不保证包就是安装器。2026-09-30 的 Windows KEMI 传书商场 +154 ZIP 为便携文件，包含 `kemi_send.exe`，不是 Inno；Mac +157 ZIP 包含签名且公证通过的 `.app`。必须先识别格式，再走平台安装合同。用户若要验证商场内点击流程，另查点击后的下载、安装确认和最终版本；商场按钮只“下载”时不可报更新成功。
3. 已验证：Mac 1321656264 的商场 +157 包在目标机核对 77,178,101 B、SHA-256 `ae883c303c2772002cc48170334c25aba6e52b9c4242fbc86d676062e796141f`，通过 Gatekeeper、签名、仿真卸载后重装、真实进程与房间心跳。4456560334、5298938227 的同一包安装和应用列表 build 157 已通过；进程/使用体验需单独核对。Windows 商场 +154 包可通过 BITS 下载、验哈希和主程序签名，但不能把便携 ZIP 伪报为 Inno 安装成功。

## 入口三：本地或签名/编译机器已有产物

1. 先找到**对应平台和架构**的最终签名产物，不使用缓存编译中间件、未签候选或另一设备的错误架构。记录绝对路径、大小、SHA、签名、应用 ID、版本和构建来源。若产物在另一台仿真机器，先在该机器核验，再用已授权传输工具送到目标机；大包 SFTP 失败可经已有 HTTPS 单文件分发地址让目标机下载，仍由目标机重算哈希。不得凭共享目录名猜产物。
2. 到达目标机后的安装和验收与入口一完全相同；包来源不会放宽权限、签名、版本、防降级或回滚门禁。Mac 先核对 `.app` 的 Bundle ID 和签名要求一致；Windows 检查 Authenticode 与 MSI/Inno/便携合同。覆盖 VibeKits 自身时安装可能切断仿真桥，等待原仿真 ID 重连，并核对房间心跳；仿真确实失联再查已登记的办公 ID，不能从一个 ID 计算另一个。

## Windows 实测的安装与故障分流（2026-09-30）

- Windows 58 `4240650696`：C 盘安装、D 盘存放包及回滚。Common 的 KEMI 传书已签 Inno +158 从 HTTPS 经目标机 `curl.exe --ssl-no-revoke` 下载并验 SHA `50a7850ac41ed07405d734577d6e2812df19c227fca02c7715d0c08613cd3d6f`、Authenticode `Valid`。先备份原目录，原 56 个文件/73,783,746 B；因为原版已是 +158，执行同版本覆盖验证，没有降级或先卸载。目标机 `explorer.exe` 在用户 `caucy` 的 Session 1，计划任务 `-LogonType Interactive -RunLevel Limited` 运行 Inno `/VERYSILENT /NORESTART /SUPPRESSMSGBOXES /LOG=...`；返回码 0、日志 `Installation process succeeded`、落地 EXE +158/签名 Valid。另起交互计划任务启动安装目录 EXE，PID 12600 在 Session 1，故“下载→安装→启动”闭环通过。计划任务启动时 PowerShell SSH 的 CLIXML progress 乱码不代表错误；读 `exitCode`、任务结果、日志和进程。
- Windows xzl `6192992780`：Common 的 KEMI 传书已签 Inno +154 经 BITS 下载、SHA `799fe773c690157f65ac20b38c81395ecd37419679c365c6b0496c5b5b30855c`、Authenticode Valid；交互计划任务安装结果 0，注册表和落地 EXE +154。旧 `C:\kemi\tools\KSEND\kemi_send.exe` 的长期运行单实例进程 PID 14940 无主窗口、无 Established TCP 连接；核对该 PID 的精确路径后仅停止该旧进程，保留旧文件作为回滚。交互计划任务启动新安装目录 EXE，随后实际进程 PID 17376 在 Session 1、路径 `C:\Users\zjc\AppData\Local\Programs\KEMI Send\kemi_send.exe`，因此新路径启动通过。计划任务的启动结果码 267009 可表示任务仍在运行，应用启动应以实际进程路径为准。若旧进程有活跃传输或窗口，不可照搬停止步骤。
- BITS 脚本应使用 `.JobId`，不是不存在的 `.Id`；“空值错误”后先查询已传输作业并完成/取消重复作业，避免重复下载。PowerShell `-EncodedCommand` 必须 UTF-16LE Base64，生成后先做本地往返核验；错误填充会出现远端解析错误。Mac zsh 中 `status` 是只读特殊变量，安装脚本状态文件变量用 `job_status`。Mac `device.app_install` 超过回环 MCP 超时不代表安装成功或失败，回查应用列表和进程再决定补救。

## 结果记录

每台记录：仿真 ID、办公 ID（若有）、主机名、平台/架构、来源类型与原始 URL 或产物路径、目标机包路径、字节数/SHA/签名、安装前后版本、安装日志/进程/界面、原 ID 与授权、房间心跳、回滚位置和未通过项。失败先定位为连接、下载、格式、签名、交互会话、安装、启动或版本/授权验收中的哪一层，修复该层，不重复整条流程。

## 本机与进程路径校验补充

2026-09-30 本机 `1554650784` 同时有三个同 Bundle ID 的 KEMI 传书副本，`/Applications/KEMI传书.app` 虽显示 build 157，签名校验失败；因此 `device.app_uninstall` 无法安全判断应删哪一份。用仿真 SSH 下载并校验同一商场 +157 ZIP，保留原用户目录 +155 到 `~/Downloads/KEMI传书-before-157-20260930.app`，在 `~/Applications/KEMI传书.app` 安装签名且公证通过的 +157，脚本状态 `PASS`。`ps` 可见该新路径的主进程 PID 43753 和后台服务 PID 43842。系统 `/Applications` 的另一份损坏副本仍在，不能因此声称所有副本已统一；后续清理由安装所有者确认，不用删除用户数据来绕过签名错误。macOS `ps` 的非 UTF-8 转义输出会使直接按中文路径 `grep -F` 漏报进程，必要时按 PID、可执行文件 inode 或应用控制工具核实。

Mac 后续启动核对：4456560334 的现有 KEMI 传书进程 PID 82892 在 AppTranslocation 路径，并有两个 ESTABLISHED TCP 连接；虽然新 `~/Applications/KEMI传书.app` 的 build 157 与签名已通过，不能为了证明新路径启动而中断当前传输。5298938227 的旧缓存路径进程 PID 995 与新安装路径并存，且曾有瞬时连接；后按已核对 PID 和路径发送正常 TERM，旧进程退出后启动签名有效的用户安装目录版本，新进程 PID 15038 从 `~/Applications/KEMI传书.app` 运行，build 157。445 必须在确认无活跃任务后按“核对旧进程路径和连接状态→安全退出旧实例→打开新绝对路径→核实新 PID/路径”补验；不能把脚本 `open` 返回 0 当成新进程运行。

补充：445 的运行中 AppTranslocation 包实际 build 151（新安装包为 157），连接到 `192.168.3.74` 和 `192.168.3.65`。529 的旧进程在 5 秒采样中间歇连接同两台设备（目标本机 `192.168.3.68`）；两次带“无活跃连接”门禁的切换均以 exit 8 安全退出。仅一次空连接截图不能证明持续空闲。529 已按原路径核对后完成运行实例切换；445 新包已落地，但旧 build 151 仍在运行，且有已建立连接，不能把安装成功说成运行版本更新成功。

445 的旧进程切换操作曾被自动审批拒绝，理由是它仍有已建立连接，终止可能中断传输或工作；不可换用另一条命令绕过。先用只读方式核对是否有活跃传输，再按正常退出流程，必要时请设备使用者安排空闲窗口。

445 安全退出补验：对旧 PID 82892 的 `lsof` 未见用户目录文件句柄，`nettop` 连续两次采样均为 205 MiB 入站、2489 KiB 出站，样本期间无增长；随后尝试应用级 `quit`，应用返回“用户已取消” (-128)，旧进程保持运行。不得因此改用强制结束；需在该设备用户结束当前操作后再尝试正常退出并验证新安装路径。网络静止的短样本不足以否定应用内仍有需要保留的会话。
