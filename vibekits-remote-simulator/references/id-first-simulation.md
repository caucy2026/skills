# 仿真 ID 优先：设备操作与安装收尾

用户提供仿真 ID 时，以该 ID 为唯一操作入口。先 connect，校验 connected、routingId、p2p_or_relay、可信主机指纹，再通过 simulator.call、ssh_exec、upload_file、download_file、screenshot 操作。不要要求固定 IP、另配 SSH 或把内网地址写死到安装步骤。工具返回的临时传输地址仅为内部实现，不替代设备 ID；网络变化后重新连接同一 ID。

ID 在线且已授予本次操作所需权限时，主动完成检查、取包、验签、安装、启动、普通弹窗处理与实际可用性核验。只给出了 ID 也应能开始；不能把心跳、connect 成功或安装退出码当作最终可用。系统安全边界、首次同意、PIN、密码、权限不足等仍按工具要求处理，不宣称在线即可绕过这些限制。

## 发起端桥失效

ECONNREFUSED 到本机 loopback 是控制端桥问题，不是远端 ID 离线。只读核验当前 VibeKits 进程、监听、桥文件 processId；如当前同事候选使用 VIBEKITS_DATA_HOME，则使用该进程实际发布的 Mcp/tool-bridge.json。只提取所需目录，不能输出完整环境或 token。旧默认桥文件可能仍存在但属于已退出进程。不要停止同事进程、覆盖配置或复制凭据来掩盖错误。

2026-09-30 实例：默认文件 PID519/50077 已失效；当前候选 PID6548 使用隔离数据根，实际桥53370。对照文件PID与监听后使用该桥，5298938227 原 ID 连接成功，主机 kemideMac-mini.local、既有指纹一致，SSH/MCP ready。cluster.rooms 实际调用成功；随后发现其房间连接仍超时。因此只能报告仿真恢复，不能报告集群通过。

## 集群服务与仿真通道分开判断

集群客户端当前 HTTPS 服务地址是独立协议配置，不是仿真操作的替代入口。房间请求失败时，可经原仿真 ID 查询设备路由与服务响应以定位原因；不转用固定 IP 操作目标。当前实现服务器内网地址随网络变更而失效，需要修复服务接入的可迁移性，不能靠永久固定内网 IP 满足产品要求。

## 安装后确认与使用

先获取当前目标窗口证据，匹配应用路径、PID、登录桌面 Session；优先语义按钮，Flutter 原生控件未暴露时按当前截图坐标操作，执行前再校验窗口边界和进程，执行后截图确认结果。普通关闭、完成等按钮在既有安装授权内主动处理；不盲点未知同意，不读密码控件，不绕过安全桌面。

Windows SSH Session0 截图黑屏不代表应用没启动。已授权交互桌面存在时，用同用户 Interactive/Limited 短任务截图，隐藏自己的 PowerShell 窗口，不关闭其他同事终端。SFTP Connection closed 时，证据文件可通过仿真 SSH 分块只读 Base64 获取，限定大小并校验完整 SHA256，不反复重传。

xzl 实例：正式 KEMI Send PID17376/Session1 的“对方拒绝了请求”结果页，按已观察“关闭”按钮收尾；任务退出0，后续截图回到主界面并发现附近设备。用户选中文件保留，未登录云端能力不宣称通过。软件安装完成须同时核对签名、版本、实际运行路径、原身份/授权和此次目标功能。

## Explicit bridge selection

The bundled invoke.rb supports VIBEKITS_TOOL_BRIDGE_FILE for an already verified current-process connection file. Verify processId and its actual loopback listener first. Keep the default when it is live; do not copy tokens or stop a colleague candidate. Syntax and a real 605 connection_status call passed on 2026-09-30. Candidate exit invalidates the selection: inspect current state again, rather than retrying a stale port.

## Windows UI evidence verified

The reusable scripts are scripts/simulator_windows_ui_inspect.ps1 (inspect exact PID/path in the existing interactive session, no clicks) and scripts/simulator_windows_read_file.py (bounded read-only SSH evidence download with SHA256 validation). The UI inspector passed on xzl and 58; 58 screenshot confirmed the real main UI and nearby devices, without an outstanding installer prompt. Do not call this the cluster-agent Remote Office update acceptance.

Shared-file correction: invoke.rb was subsequently restored to its original default-only implementation by another writer. Check current source before relying on VIBEKITS_TOOL_BRIDGE_FILE; the earlier successful explicit-path test is historical evidence, not proof the current script still supports that option. A current bridge must match the live process and listener; do not retry the stale default port.

## Current implementation correction

The final fix now installs simulator_bridge_locator.rb and invoke.rb live discovery. It checks the running App PID, file owner/mode, loopback endpoint and listening socket; deduplicates case-insensitive APFS files by inode. All six original device IDs passed connect and actual applications calls through the final standard script. Earlier default-only restoration notes are historical; recheck shared source if another writer changes it. Client transport-timeout relay recovery has passed 2 focused tests but is not yet packaged/deployed.

## 当前交互约定（2026-10-02）

本节替代旧记录中的“仿真同意必须输入密码/PIN”。依据项目 docs/acceptance/SIMULATION_CONFIRMATION_WITHOUT_PASSWORD_2026-10-02.md、SIMULATOR_CONSENT_LISTS_NEXT_RELEASE.md 和当前确认窗口源码。四平台目标交互为普通确认/取消，不额外要求电脑登录密码、仿真密码或 PIN；操作系统自身安装、隐私和安全确认仍按其要求处理。尚未真机通过的平台不能写成已交付。

### 名单入口与连接

在目标 App 的“设置 → 高级”查看远程仿真开关、仿真授权、允许名单与拒绝名单。当前 Mac 实机已看到允许项的“撤销/拉黑”；拒绝项恢复允许由目标人员操作并独立验收。其他平台核对实际入口，不套用 Mac 坐标。

用原 ID 连接并验证可信身份。未知请求方等待目标人员确认，目标弹出“允许此设备仿真访问？”。人员点击允许/拒绝，再完成普通确认；取消或“暂不处理”不授权。仿真开启、房间批准、数字 ID 和名称均不等于首次同意。目标人员可以本机操作，或通过已授权远程办公操作同一确认框；发起智能体不能经仿真 UI、SSH、HTTP、模型工具或名单文件代替自身首次授权。取消密码不取消人员决定、身份绑定与修订校验。

人员确认成功后弹窗应关闭，刷新名单核对精确身份和授权修订，再按原 ID 重连并实调只读工具。有效授权且身份未变的重连、覆盖升级不应重复确认。

### 允许反复出现或按钮无响应

不要连续点击、重置钥匙串、清空授权或改写名单。记录精确请求 ID、名单修订、有效期、运行路径/版本和有界日志，刷新设置中的名单判断是否已提交。过期、撤回、身份或修订变化不能提交旧决定。提示“无法确认操作结果”时关闭后核实状态，再决定是否重试；未知结果不能视为允许。模态确认期间底层 Harness WebView 应停止接收点击，结束后恢复；实际测试允许、拒绝、暂不处理和输入恢复，不能只凭源码或单元测试称通过。

### 分层判断

- ID 旁绿色/服务器在线只证明该时刻服务器通信观测。在线而无法互动应定位故障，不能直接断言物理设备离线；绿色不是 SSH/MCP 执行成功证据。
- 保留结构化 consent_pending、consent_denied、peer_blacklisted、consent_revoked、remote_disabled、identity_mismatch；权限问题不改报离线，不改中继绕过或盲目重试。旧客户端缺 code 时保留原始结果并检查版本，不凭文案猜测。
- 分别记录可信身份、授权修订、SSH/MCP ready、工具目录及实际只读调用。集群心跳、仿真连接和模型回答不能相互替代。

### 覆盖升级和执行记录

核实实际运行 App 路径，完整签名包原子替换并留回退；保持 Bundle/Team、原 ID、身份、配置和有效名单。目标端用独立交接任务完成退出、替换、立即重启，不依赖被退出 App 的子进程。控制端承担同事接口或传输时不重启；必要短暂切换后立即恢复。控制端重启后重新发现真实桥 PID 和监听，不复用旧端口、会话或缓存成功。

用户要求在 Harness 对话中执行时核对该版本的真实任务入口并保留执行结果；仅执行 SSH 不得声称对话里已执行。探测复用当前任务会话。记录请求、事务终态和结果，隐藏令牌、私钥和凭据。

### 当前证据边界

2026-10-02 Mac 本机三次 dev441 冷启动实测原 MCP 状态和授权文件保持；名单页面允许3项、拒绝0项可读取。这不等于首次允许、拒绝、拉黑、恢复全部通过。dev441 和 dev442 本机仍复现非活动窗口第一次点击输入不接收文字，签名、公证或保留授权不能替代完整交互验收。后续按现有 C01–C12 和 MH-04-S1 复验；Windows/PAD/Linux 独立验收，不继承 Mac 结果。
