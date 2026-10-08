---
name: vibekits-cluster-room-deploy
description: 通过VibeKits工具部署hbbv服务器，按获授权仿真ID配置设备集群地址、双向入房、同步能力并用后台管理协作；适用于从服务器到设备房间的全链路接入，不代替签名发布或任务执行验收。
---

# 集群房间部署全链路

用户给出服务器、设备仿真ID、服务地址和目标房间并授权接入后，沿现有工具完成部署和逐台验收。先读项目AGENTS、本机环境规则及最新交接；部署细节读[hbbv服务器技能](../hbbv-server-build-deploy/SKILL.md)，能力编辑读[能力技能](../vibekits-cluster-capabilities/SKILL.md)，房间协作读[任务技能](https://github.com/caucy2026/skills-game/blob/main/vibekits-cluster-agent/SKILL.md)。技能可供同事复用，不携带账号、令牌、密码或私钥，也不授权给其他会话派任务。

## 一、连接与部署服务器

优先VibeKits自身SSH/SFTP：先remote.list_profiles，核验保存profileId的host、port、user、可信指纹；无保存会话用remote.open_interactive打开登录工作台，用户正常认证和首次可信指纹核对后再复用。通过system.describe_tool查运行时Schema；remote.ssh_exec参数为profileId、command，remote.sftp_upload为profileId、localPath、remotePath、overwrite。不用外部SSH替代用户指定工具，不自动接受身份变化。

用kemi-server-ports查唯一台账，核验ss监听、全部systemd socket、存在的容器映射及运维预留；不强占、重启hbbs/hbbr/hbbc。从该项目源码/部署配置查域名，再对照实际公开地址、DNS及证书SAN，不能凭IP或自述推断域名。

hbbv当前是Python/SQLite源码服务，无二进制编译。冻结server/web/contracts与逐文件哈希，在专用venv安装锁定requirements，运行必要真实HTTP和权限测试。用SQLite backup迁移一致性副本；保留原UUID、批准成员、设备安装身份、原授权及服务签名身份，上传后校验SHA与quick_check。服务签名私钥迁移必须满足材料与目的地的工具审批；拒绝后不能改名、打包、换工具绕过，未获批不启动生成新身份。

用通用server/app.py启动，明确数据目录、database-name、HTTPS证书、公共host和独立端口；run_local_https.py为本机验收脚本，不能搬到远端照用。部署独立服务单元，限定数据写入路径，保留旧服务回退。启动后严格TLS查询service-info、核对原serverId、实际监听及原服务PID不变。启动成功不等于公网、任务或长期稳定验收通过。

## 二、逐台修改获授权仿真设备的集群地址

对每个原ID先检查当前在线证据；用户禁止离线桌面恢复时不连接该桌面。调用simulator.connect({routingId})核验原主机及可信指纹，SSH/MCP各通道分开验。connect的SSH引导HTTP500不等于物理机器离线；先connection_status及实际MCP调用分流，未恢复就跳过该机并继续其他机，不接受新身份。

远端工具由simulator.call({routingId,toolId,arguments})调用；本机直接调用。读取cluster.status并保存脱敏旧配置作为回退点，再按当前Schema调用：

```json
{"serverOrigin":"https://可信服务域名:已登记端口","trustedHosts":["可信服务域名"],"trustedCertificatePem":"","serverSimulationId":""}
```

上述是cluster.configure参数模板：公网受信证书不沿用旧服务自签CA；专用CA须从已核验服务资料取得，不能跳过TLS。任务签名公钥只取可信服务身份资料。若同一origin重复配置，应保留原信任和有效授权；换服务不得复制另一设备的私钥或旧服务令牌。仅按授权使用cluster.set_enabled({enabled:true})，设备仿真须先就绪。

配置后cluster.rooms首个结果可能是“发现中”/非实时缓存；等待原异步同步再读，不能立刻重复申请。记录原ID、实际版本、配置前后安全摘要、服务UUID及连接状态。来源scope改变后由原安装身份正常证明恢复，不手改配置数据库或绕过批准。

## 三、客户端申请或后台主动邀请入房

客户端：rooms发现正确房间→cluster.apply({roomId})→原安装身份签名→后台核对原ID/安装指纹并按授权审批→客户端激活→新服务器新鲜心跳。

后台：选择本人管理的房间→单台/批量输入原仿真ID→逐台查看邀请回执→已开启集群的客户端rooms读取有效邀请→按实际配套版本cluster.apply({roomId,invitationId})响应→原签名申请与原审批→激活和心跳。老客户端没有invitationId时如实待验；不能把直接申请代替主动邀请通过。邀请不是开启仿真、批准成员或任务执行授权。批量部分失败不重放成功项，幂等键仅用于同一请求内容。

迁移原服务时，已批准成员可经原身份证明在新origin恢复；没有待审批申请时不再人为建申请。撤销、拒绝、过期和身份变化不得恢复旧批准。

每台入房通过需同时满足原安装身份/设备ID、客户端roomsAreLive与connected、目标membership approved、服务端新鲜心跳，以及实际只读MCP调用。缓存历史成员或设备自报simulationReady不足以证明全部通过。

## 四、设备能力与后台发现

设备能力来源分别显示确定性事实、用户声明、实际验证证据及当前就绪状态。读advanced.capabilities、system.capability_check、cluster.capabilities.read，按device-capability/1完整declaration及expectedProfileRevision调用mutate，再sync_status核对云端acceptedRevision。冲突重读，不覆盖他人声明；不自填verified、eligible、health、deviceId或凭据。

Windows签名示例声明需说明EXE/DLL/安装包输入、签名与验证报告输出、硬件令牌、可信证书、任务授权和人工PIN条件，tags可含windows/authenticode/signing，方法引用真实签名技能。PIN仅用户在硬件窗口输入；忙碌签名设备不抢占。保存声明成功不代表资源当前可用或已验证。

后台设备列表按平台、在线与能力关键词检索，查看最后心跳、声明、工具目录、安装身份、有效授权及任务负载。实际已部署目录中存在时，管理MCP可用hbbv_room_devices({roomId,q:"authenticode",platform:"windows",status:"online",limit:20})，并按nextCursor分页。目录缺接口时通过网页原入口，不猜端点或直接改数据库。

## 五、通过后台管理和协作

打开已核验HTTPS后台，使用原管理账号正常登录；不把令牌放URL。依页面可访问标签选择房间，管理成员申请/批准/拒绝/撤销、单批邀请、在线设备及能力详情。后台指南应内嵌具体步骤，不能仅给外部链接。能力自述匹配不会自动给操作权限。

任务由真实Harness智能体分析、冻结合同、发布、候选竞标、唯一分配及签名租约领取；设备按本地grant与operation permit调用工具。后台完整消息/ACK、审计、结果hash与独立验收决定评分，不能凭在线、竞标、已提交或工具exit0加分。缺模型凭据不复制密钥，不降低合同requiresModel/requiresAgent来凑通过。

## 六、交付证据和故障恢复

按设备逐项记录实际起止时间、版本、原ID/身份、配置、申请/邀请/审批回执、客户端实时状态、新服务器心跳、MCP调用、断联原因与恢复耗时。监控迁移后指向新服务器；未迁移机仍查旧服务器，避免旧心跳过期误报断联。采样不是采样间连续在线或自动进程守护证明。

新故障先区分控制桥、仿真、房间、进程和物理网络；只恢复可信原ID。活跃签名/升级事务只观察，不重复安装或重签。不可自主恢复时保留证据，继续其他设备。代码/技能备份main，解决真实冲突，不force/reset或改共享索引；私有数据不进Git。

本次现场事实：云端部署目录/opt/vibekits-group、独立21122服务、域名kemi-chat.newlinksz.com，原UUID延续；Linux27项邀请/管理测试通过。155/529/424/617已在新服务真实批准入房且云端心跳新鲜，原身份保持；仅证明四台基础接入，持续稳定及业务执行仍待验。双向邀请真机、完整任务执行/ACK/独立验收评分和100台长期协作仍待验。本文将来更新现场证据，路径与ID不作其他环境默认值。

仿真不可调用时按[实际远程桌面恢复清单](references/remote-recovery.md)处理；617办公通道已实测可达；用户报告PIN已输入后原仿真恢复并完成云端迁移，过程及尚未证实的500根因见恢复清单。锁屏不能未经日志定位称HTTP500根因。

房间设备用途及可执行方法通过[GitHub能力交接规范](https://github.com/caucy2026/skills-game/blob/main/vibekits-cluster-capabilities/references/github-capability-handoff.md)传递；完整交付范围按[全目标验收映射](https://github.com/caucy2026/skills-game/blob/main/vibekits-cluster-capabilities/references/full-goal-acceptance-map.md)逐项保留，不把基础在线当作最终协作通过。

迁移归属：仿真/集群代理/能力技能自2026-10-08在[caucy2026/skills-game](https://github.com/caucy2026/skills-game)维护；部署技能仍在本仓库。资源/维护恢复时阅读本技能既有恢复引用中的2026-10-08经验，不按旧相对目录猜位置。
