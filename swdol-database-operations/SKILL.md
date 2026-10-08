---
name: swdol-database-operations
description: 整理、查询和对齐SWDOL原版crossgate认证计费库、swdol游戏库与我方SQLite持久化；用于数据库接手、账号角色查找、状态差分、资产追溯、保存与重启验收及新适配器接入，不将静态合同或组件测试冒充原服一致。
---

# SWDOL数据库操作与接入

首先确定目标数据库，不把不同数据库的账号、角色或运行句柄混用。用户所称两份原版数据库是SQL Server crossgate与MySQL swdol；我方当前SQLite是另一个持久化实现，私有字节参考SQLite又是另一用途。

- 查原版连接、认证和游戏表：[original-databases.md](references/original-databases.md)。
- 查我方实际库、键、事务与服务器接线：[self-server.md](references/self-server.md)。
- 账号/角色对应和前后差分：[identity-and-comparison.md](references/identity-and-comparison.md)。
- 丢钱、丢装备、剧情重登与重启：[audit-and-acceptance.md](references/audit-and-acceptance.md)。
- 后续数据库适配器/运营接入：[integration.md](references/integration.md)。
- 新市场、总包裹、扩展容量及原版来源追溯：[market-and-inventory-extension.md](references/market-and-inventory-extension.md)。
- 文档分类、现行与历史裁决：[document-map.md](references/document-map.md)及[数据库文档清单](references/document-inventory.json)。清单匹配不是全文审查完成。

## 每次操作的固定前置

记录runId、UTC、任务独占环境、数据库host/engine/version/schema、我方BIN/APP与源SHA、schemaVersion、目标账号键/RoleID或principal/slot/代次。使用项目当前成功的查询入口及私有凭据读取器。端口、PID、XP A/B归属、库文件路径都现场核，不能沿用历史记录。

默认原版只读；测试账号创建或其他写入按已有具体授权处理，技能本身不新增写库、重启、踢号、清租约许可。用户已经授权的相同范围操作不用重复审批；工具明确拒绝则不绕过，保留原因，做不受阻的工作。

不输出口令列、完整账号表、账号/IP原始日志；凭据仅在内存或stdin传递，不进argv、截图、网页、Git。私有配置和原始数据库备份留受控目录。Windows Administrator凭据不是SQL认证密码。

必须保存原二进制/GBK、NULL、列序、对象版本字段，不能只保存解码后的文字；数字相同也不代表同一个角色或演员。先核schema再写参数化查询，旧MySQL3.23不硬套现代SQL语法或事务能力。

## 最有效的验证路线

按已有前后台注入技能准备环境，同时MCP正常触发前台动作与后台业务观测，比较提交前后的窄范围数据库字节。恢复注入超过180秒立即停重复试错、看成熟技能和最近成功记录；用户最新要求每次调试验证也不得超过180秒；超时立即回查成熟文档和最近成功记录，不能用原“只限注入”的说明延长试错。

复用 swdol-xp-control、client-server-dynamic-trace、swdol-static-dynamic-analysis；交接复用 project-handoff，验收复用 swdol-acceptance-handoff。探针加载/心跳、SQL SELECT成功、组件绿色均不能代表剧情或交易验收。

原版客户端→原服A，我方客户端→原服B，同一我方制品→我方服C；长期原版客户端→我方服D另验。每项同角色前态/相位截图、协议、后台分支、即时DB、重复、重登、服务重启和受影响回归齐全才关闭。不同制品/状态不一致记不可比较。

数据库整理和技能完成不等于服务器完成；保持全项目目标。每两小时按用户要求记录改动、已完成/未完成、证据、下一步；选择性备份获准产物，远端SHA回读后才说已上云。停采集、精确清本任务可再生临时文件，绝不删除数据库、WAL/SHM、VM磁盘或未归档证据。

## 新测试账号与自然建角

用户授权为测试自行新建账号/角色时，先读[注册→原生建角→首次登录与身份回读](../swdol-database-operations/references/identity-and-comparison.md#测试新账号与新角色注册自然创建首次登录)。原服两库登记、我方stdin注册、思想wire1–6、空槽UI和正常首入/重登分别验；不把管理预置或网络0200诊断当原生建角通过。授权只覆盖测试新身份，不覆盖修改旧角色/资产、删除或共享服务重启。

## 每次验证三分钟止损

用户要求每次调试验证180秒内完成；超时停止重复尝试，认真回查对应文档、成功记录与本轮差异，查清未理解/遗漏步骤后再验证。统一按[验证180秒与超时文档回查](../swdol-xp-control/references/failures.md#每次调试验证180秒超时回查文档用户最新要求)，不重置计时或缩小完整验收目标掩盖超时。


## 资源收尾与前台占用

按用户要求，自己创建的APP/进程、临时文件和打开的文件/句柄/数据库事务/socket/锁必须自己收尾，验证后关闭不用实例，尽量后台操作、少占前台，效率第一。执行[统一现场收尾准则](../client-server-dynamic-trace/references/disk-and-scene-cleanup.md)，以实际退出/释放/删除回读为准；保留必要证据，不误删活跃资源。该规则不代替产品保存/验收，也不暂停完整目标。
