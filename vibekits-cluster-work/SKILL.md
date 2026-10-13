---
name: vibekits-cluster-work
description: 接续 VibeKits Harness 与 hbbv 集群的源码开发、真实设备升级、房间任务闭环、多客户隔离、委托 MCP、规模验收及交付，继承完整目标并复用成熟路线。单设备操作、单次签名或能力编辑仍使用对应专项技能。
---

# VibeKits 集群工作

让接手者从真实现场继续完成原目标；不是重新立项，也不是仅把最后一个修复做完。技能不授予新设备、新发布或跨会话沟通权限。

## 接手入口

1. 完整读取适用 AGENTS.md、同目录 LOCAL-ENVIRONMENT-RULES.md；定位 Harness 与 hbbv 源码、当前交接、最新验收台账。使用 [接续快照](references/current-project.md) 定位本项目，换机器时重新映射路径，不能照搬本机磁盘约束。
2. 继承 [完整目标 G01–G10](references/goals.md)，逐项记录现状、证据、剩余责任；用户明确取消才删目标。版本构建、文档或备份完成不能代替业务目标完成。
3. 先对账在途构建、签名、公证、传输、安装、任务分配：设备原身份、任务 ID、PID 与创建时间、唯一作业名、日志及终态。结果未知不重启事务。核对执行归属；共享桥或同事任务不能擅停。
4. 复用有效通过证据，选择能推进剩余目标的最短路径；立即执行已有授权内的工作。局部等待期间做独立工作，不以轮询或文档代替实施。

## 按当前动作路由

| 动作 | 先读技能及依据 |
|---|---|
| 连接、远程操作或恢复 | `vibekits-remote-simulator`、`vibekits-cluster-deployment`；[成熟操作](references/operations.md) |
| 集群实际任务与分工 | `vibekits-cluster-agent`；原房间任务、分配、claim、ACK、审计回执 |
| 能力声明 | `vibekits-cluster-capabilities`；声明不代表已授权或实测通过 |
| hbbv 修改和部署 | `hbbv-server-build-deploy`；保留服务器身份和持久数据，勿动 hbbc/hbbs/hbbr |
| 桌面构建覆盖升级 | `vibekits-fleet-compatibility`、`vibekits-release-error-preflight`；项目升级标准和历史错误矩阵 |
| Windows 实机与硬件签名 | `kemi-windows-device-lab`、`kemi-windows-remote-signing`；D 盘、交互会话、PIN 门禁 |
| PAD 开发或发布 | `vibekits-pad-development`、对应发布历史；不借桌面包替代 |
| 商城发布 | `kemi-market-publish`；正确目标发布成功且公开可获取才通过 |
| 全应用稳定性验收 | `app-release-stability-gate`；复用现有证据，补真实缺项 |
| 云端构建收尾 | `cloud-build-cleanup`；只清本任务已不用的可再生产物，保留正式包和证据 |
| 总结或指定交接 | `project-handoff`；仅编写本技能不创建聊天或派发任务 |

专项技能在当前环境不可用时，读取其项目文档中的已验证路线；不得声称已执行不可用工具。

## 不可丢的执行判断

- 原仿真 ID、应用签名身份、登录、Key、信任、系统权限和用户数据连续性是覆盖升级验收内容。不要卸载、清数据、换包名或重置钥匙串掩盖问题。
- 仿真失败先查桥和原事务，再用已登记同机远程桌面恢复；黑屏、输入失效、认证失败、离线分开诊断。普通同范围确认可完成，PIN、身份变化、平台拒绝保持边界。不能用另一通道绕过明确拒绝。
- 模型可用、工具可用、任务已分配、执行已授权是四件事。无 Key/额度设备仍可提供 CPU、构建或签名；不能伪造 model-ready。真实模型验证使用既定分析会话，计费失败不自动重复。
- 服务公开信息中的 execution 字段可能是调用者作用域，须用实际鉴权上下文判断；owner_attested 元数据不能替代 signed 执行证据。
- 房间委托 MCP 只凭真实原生身份、envelope、socket 和 connection generation；不能用 SSH 注入授权或改 authorized_keys 伪装成功。
- 当前按用户最新要求先设计和验收七台登记设备；100+ 真设备及24/72小时属于后续扩展证据。300个合成会话、loopback、单测或签名不能替代实际设备、真实网络、覆盖升级和任务闭环；不把后续设备清单变成本轮等待前提。
- 源码共享脏树只精确改本任务文件；备份用独立索引和正常推送并读回，不全量 add/reset/stash/强推。备份范围与整个源码同步分开报告。

## 收尾和维护

每次阶段成果更新项目台账：目标编号、设备/服务身份、版本与哈希、实测时间、证据路径、失败与下一步；技能中的日期快照只用于导航。新增已验证经验更新 operations，易变状态更新 current-project，完整原始记录仍在项目内。交付说明已验证结果与剩余缺项；原目标未达成不标完整通过。
