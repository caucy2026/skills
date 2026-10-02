# Mac 仿真通道覆盖安装：1321656264 成功样本

这是一次**远程可回滚覆盖安装**，不是不停进程的热重载。仅在用户授权更新精确设备和 App 后使用；不扩大到其他设备或商城发布。示例的安装步骤成功，目标机的工作区真实选择验收仍须另做，不能把安装成功写成功能通过。

## 先锁定对象与包

1. 连接用户指定的仿真 ID，确认 `connected=true`、`transport=p2p_or_relay`、SSH/MCP ready、主机名及已知 SSH 主机指纹。读出目标机架构、macOS 版本、**实际运行进程路径**、包版本、Bundle ID、Team ID、可用空间；不要仅凭应用清单推断安装路径。
2. 在本机完成项目既有 Mac 门禁，使用原 Developer ID 签名；如该渠道要求公证，提交精确签名 ZIP，等待 Apple `Accepted`，装订票据，再验证 `codesign --verify --deep --strict`、`stapler validate`、`spctl --assess`。公证/签名授权与外传边界仍按当前任务判断。装订后**重新封最终 ZIP**，固定字节数和 SHA-256；不能传公证前的 ZIP 充当最终包。
3. 通过 `vibekits.simulator.upload_file` 上传最终 ZIP。用远端独立 `shasum -a 256` 和 `stat` 与本机值比对。上传工具返回成功仍不代替远端复算。

## 在原路径受控覆盖

1. 在远端独立暂存目录解包，确认新 App 版本、签名和 Gatekeeper。长时 `ssh_exec` 可能因命令超时断开；先只读复查解包进程、文件和校验结果，不能把断线视为解包成功或直接重试覆盖。目标机联网限制可能使远端 `stapler validate` 无法访问 CloudKit；要分别记录本机票据验证与远端 Gatekeeper 的实际结果，不伪称远端票据检查通过。
2. 确认旧进程的绝对路径与旧版版本、预定回退目录不存在。部署脚本在**目标机后台**执行精确版本和签名检查，正常结束旧主进程；旧进程未退出则停止。把旧 App 原样改名到回退目录，把暂存 App 移到原运行路径后启动。不要使用可能安装到另一目录的通用 `app_install`，也不要删除用户数据、凭据或旧包。
3. 健康检查同时要求新进程运行于原路径、磁盘版本为新版本、Harness 本地 HTTP 服务响应。未认证请求返回 `401` 表示服务在响应且需要认证，不应误判为启动失败。失败时先停止新进程，再恢复旧目录并启动旧包；核对磁盘和实际进程版本一致。
4. 断开旧仿真会话，以**原 ID**重连，再核对主机指纹、运行 PID/路径/版本、MCP 实际只读工具调用、屏幕和具体目标功能。`connected=true`、绿色状态、端口监听、HTTP 401、签名或截图均不能单独证明用户功能通过。界面辅助功能检查默认遍历可能超时；先用有界 `ui_inspect`（例如 `maxDepth:2,maxNodes:20`）区分大控件树超时与未授权，再逐步扩大。系统辅助功能若真未授权，须由目标机用户在 macOS 中授予，不能绕过。

## 2026-09-30 的已验证事实

设备 `1321656264` 是 `macdeMac-mini-2.local`、Intel/macOS 12.6.4，旧进程运行在 `/Users/mac/Library/Caches/Vibekits.app`，dev346/2346。dev351/2351 的公证提交 `78d7ba82-f050-4360-b7e1-db30b8d9fdab` 返回 `Accepted`；票据装订、本机深度验签及 Gatekeeper 均通过。装订后的 ZIP 为 423134582 字节，SHA-256 `8f0f6d04b788c62b21b69c142435aa10e3d4bc9fa73badbfc13626054bddc6b0`，远端复算一致。目标机解包后深度验签和 Gatekeeper `Notarized Developer ID` 通过；远端票据服务连接失败，不能把该项记作远端 PASS。受控脚本把旧版留在 `/Users/mac/Library/Caches/Vibekits-dev346-2346-rollback-20260930.app`，新版在原路径运行，PID 60920、HTTP 401。断开重连仍得到原 ID、相同主机指纹、SSH/MCP ready；屏幕显示 dev351 Harness。有界 `ui_inspect` 返回 `authorized=true`。**工作区实际选取、Harness 任务、重启后持久性尚未因此自动通过**，继续依项目验收文档核验。
