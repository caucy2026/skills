---
name: vibekits-cluster-deployment
description: 用 VibeKits 仿真 ID 远程诊断、更新和加入集群房间，核对实时心跳、设备能力及身份连续性；适用于六机或更多设备的集群搭建与入房故障排查。
---

# VibeKits 集群设备接入

目标是让指定设备以**原仿真 ID**在目标房间实时上线，并使服务端、客户端看到一致的成员、版本和能力。用户给出 ID 且已授权本次接入时，先走现成仿真通道和现有文档，不要求用户先提供 IP、SSH 凭据或手动点击。仿真通道当前可连接时，设备盘点、安装、客户端操作、入房申请及验证原则上由执行者完成；系统授权、硬件令牌 PIN 等必须由设备持有人在本机完成的步骤除外。不要把“尽一切办法”解释为绕过同意、身份校验或平台保护。

## 一分钟快速路径

这是一条**目标时长**，只适用于 App 已就绪、仿真已开、网络通、目标房间已存在且无需审批等待的设备；不是完成保证。

1. 直接对当前 ID 调 `vibekits.simulator.connect`，检查结构化结果的 `connected=true`、路由 ID、P2P/relay、SSH/MCP 就绪；对照可信主机名、主机密钥指纹和既有设备记录。旧日志显示离线时也重新做一次当前探测。连接拒绝、主机密钥变化或身份不符时停止该设备的变更。
2. 用仿真设备工具查**实际运行进程路径**和该包版本、签名身份、当前仿真 ID；再调用客户端房间查询工具 `vibekits.cluster.rooms`，取得 `roomsAreLive`、`connected`、`simulationReady`、已批准房间、能力同步状态。安装目录名、后台缓存和网站历史状态不能代替实时数据。
3. 若版本合格且仿真已开：读取目标房间目录 → 发起加入申请 → 用既有管理 API 检查申请的设备 ID、公钥指纹和房间并完成已授权审批 → 等客户端激活与心跳 → 双向核对客户端房间列表、服务端成员及在线状态。申请已在服务端创建但客户端报错时，不重复申请，先查请求 ID 与服务端修订。
4. 记录开始/结束时间、ID、主机、运行版本、办公 ID（存在时）、目标房间、申请/审批/激活/心跳状态。只有**原 ID、客户端实时状态和服务端实时心跳同时成立**才报“入房完成”。超时则按下述故障分流继续处理，而非让用户重做可远程完成的事。

不同客户端的接口参数、API 认证和当前目标房间以项目文档为准。远程工具用法见 [vibekits-remote-simulator](../vibekits-remote-simulator/SKILL.md)；能力格式与同步见 [vibekits-cluster-capabilities](../vibekits-cluster-capabilities/SKILL.md)；任务抢单与执行见 [vibekits-cluster-agent](../vibekits-cluster-agent/SKILL.md)。

## 故障分流与升级

连接失败先区分 `remote_disabled`、中继不可达、App/relay 进程未运行、ID 已变化、身份不匹配，按 [现场案例与恢复步骤](references/fleet-lessons.md) 排查。房间显示“已批准”但离线时，检查客户端能否从**该设备**到达服务端地址、TLS 信任、客户端集群开关和实际心跳；房间心跳在线不等于仿真通道可用，反之亦然。

升级须先冻结原 ID、主机指纹、安装路径、授权与签名身份；核对签名包哈希、版本、空间和回滚点；更新**当前正在运行的实例**，恢复运行后仍以原 ID 重连并核对实际进程、房间心跳、Harness 及既有授权。不要因一个 401 把认证监听器判死；不要仅凭脚本退出码或已安装目录宣称完成。Windows 签名/安装还须按 [Windows 设备实验室](../kemi-windows-device-lab/SKILL.md) 和 [远程签名](../kemi-windows-remote-signing/SKILL.md) 操作。

仅当上述门禁实测通过才填写验收。未通过时保留日志、服务端记录与可回滚实例，标出具体阻塞并继续不依赖它的其他设备。不得为凑齐人数伪造在线、改 ID、复制设备私钥或扩大审批范围。

For the six-device room, real-time room counts and online-first pagination, read [the dashboard and fleet acceptance cases](references/dashboard-fleet-lessons-20260930.md).

For network changes, stale controller bridges or conflicting online indicators, read [the verified incident and recovery procedure](references/network-switch-incident-20260930.md). Do not label a local bridge error or a transport timeout as proven remote-device offline.
