# SWDOL交接：目标、分工与成熟注入

先发现当前项目实际根目录及最新人类资源分配。历史XP A/B/PID/端口不得硬套；本任务是审查时只读审核，不为交接去抢现场环境。

## 目标示例（交接时核最新主本）
- 长期：完整原版行为的权威服务端；原版客户端和我方客户端直连我方服均可完成任务与行为，原D链不可被代理转原服代替。
- 中期：新手村Map00、长阳城Map01、迷雾Map04所有目标剧情分支、状态/材料/称号/奖励与保存恢复同条件闭环；未完成Boss/全地图专项仍保留。
- 短期：双新账号正常登录/原生建角、Plot601选择/取消、缺材料/成功、扣发、重复及即时DB/冷重登；具体下一个未闭合门以当前账本为准。
- 当前旧server审查职责：完整月内代码/文档/历史纠错/依赖/证据审查与交接，不能把现场研发的部分成绩当审查完成；未经新授权不联系/管其他同事。

主本：server/DEVELOPMENT_GOALS.md、server/DEVELOPMENT_STATUS.md；第一原则：document/第一原则-任何修复不得破坏已验收功能.md。路径相对实际根目录，长期/中期/短期不是固定一天进度；112门或31项等分母必须以当前主本逐门证据核，旧80.4%不作当前值。

## 必须掌握的全局技能表
| 用途 | 必读入口 | 继续读什么 |
|---|---|---|
| 原版XP前端启动、输入附加、登录、进图、操作 | [swdol-xp-control](../../swdol-xp-control/SKILL.md) | references/runbook.md、cold-recovery-180s.md、对应failures.md；最新成功记录 |
| 服务器后台授权注入、PID/模块/collector与事件关联 | [client-server-dynamic-trace](../../client-server-dynamic-trace/SKILL.md) | references/runbook.md及项目目标Map安全runbook；已成功attach记录 |
| 静态与前后台动态重建、MCP触发及通用算法对齐 | [swdol-static-dynamic-analysis](../../swdol-static-dynamic-analysis/SKILL.md) | references/project-runbook.md、original-server-mcp-closed-loop.md；最新专题合同/纠错 |
| 客户端/服务端分别验收、两小时交接和云端备份 | [swdol-acceptance-handoff](../../swdol-acceptance-handoff/SKILL.md) | references/role-acceptance.md、handoff.md |
| 本轮磁盘巡检、停写与清现场 | [共享清理规程](../../client-server-dynamic-trace/references/disk-and-scene-cleanup.md) | 每轮前/中/后检查宿主、XP、WinServer真实余量 |

原版后台Map04现有安全入口示例为项目xyOnlie/tools/legacy-dynamic-trace/MAP04-SAFE-RUNBOOK.md；换Map必须核该Map已验证流程，不拿Map04历史PID或DLL当其他Map当前身份。Windows文件传递确需SMB时另读vm-smb-file-delivery技能，不临时另造传输体系。

## 接手从零恢复与180秒止损

1. 操作前读路线和成功记录，准备本轮最小动作与证据目录；核分配VM、宿主窗口、游戏页、后台唯一owner/健康、现役模块代次与单collector。后台已经健康有探针时只核就绪，不重复LoadLibrary或另开服务器。
2. 前端按XP runbook的普通登入器→开始游戏→更新提示→新PID一次输入附加/已驻留复用→真实填写授权身份→选服/选角→进图。账号输入错误先核页面/焦点/身份，不盲归因DInput。实际参数/坐标按当前画面，不复制旧值。
3. 后台按Map已验证attach-only流程，只补缺失探针；先核EXE/切片/载荷/ABI/SHA与collector，后核目标PID Ready/新心跳及业务事件。宿主、XP游戏与WinServer后台身份分开。
4. 从恢复/注入开始连续计时。180秒需前后台所需探针Ready、真实登录正确地图、一个正常动作及对应本轮后台业务事件、原图/身份/时间证据。仅INJECT_OK/Ready/发出按键不够。首次缺依赖重建、XP正常启动耗时如实计入，不拼暖登录纪录宣称冷恢复已过。
5. **超180秒立即停止重复试错。** 记录最后已证阶段，仔细读cold-recovery-180s.md、相应failures.md、最近成功记录和Map安全文档；逐项比对页面/焦点、PID代次、输入消费、监听owner、字节/hash、缺模块及业务覆盖。纠正后再恢复，保留失败轮，不重置T0隐藏超时。不反复猜坐标、不造新启动器、不无界重新注入。完整业务目标继续保留。
6. 用户已授权连续登录失败且确认本任务XP确实卡住时可主动重启该VM，无需重复审批。先按文档区分账号错误、原服不响应或焦点错误与XP卡死，保存证据/VM身份；不重启健康XP，不碰同事VM，不把此授权扩大为重启后台/踢号/清租约。重启后重新发现全部身份，按成熟恢复路线，记录真实耗时和终态。
7. 采集设时长/字节/事件数上限和最低余量。收齐即停；归档原证据并回读后，精确删除本任务不用且无进程使用的EXE/旧PID BIN。活跃DLL、未封口日志、唯一证据、源码、数据库和VM盘不删；核空间实际释放、日志停止增长与服务健康，失败不写成完成。

技能“写进文档”不等于接手者已会。接手者要实际走一次已授权闭环并计时；未过180秒如实FAIL/OPEN，不保证每个未知环境三分钟成功。

## 分职责验收与差分闭环

A原版客户端→原版服；B最新完整我方客户端→原版服；C与B同程序/资源SHA客户端→独立我方服；A/B定位客户端，B/C定位后台。D原版客户端→我方服是长期终验。需要同步时记录真实采集时间差；顺序实验明确顺序，不拼历史图。

服务端：角色/剧情全部分支及变量owner、Mark、材料/金币/称号/奖励、交易资产守恒、魔法距离/范围/叠加/HPMP、NPC/Boss仇恨/回血/死亡/掉落/尸体/重生/RNG、昼夜、在线同步与即时提交/重启恢复。角色代次不能用可复用slot代替；单线程/SQLite组件不算百客户端。

客户端：原版资源/布局/字体/确定取消/滚动与四态，真实键鼠/Pad/WASD/摇杆走停/相机/模态/Hand，角色实际动作、法术连续阶段、挂点/旁观/下线、真实地图脚底/碰撞/昼夜及权威回包。不得自绘剧情窗口代替原版，也不把本地预测叫后台确认。

联调：同可比前态、同动作与时间窗，前/中/后原图可放大，原版后台动态+协议+即时DB+重复/重登+同制品回归齐全才该门PASS。已发现的原合同纠错先读，不能只按旧文字或组件绿测去改常数。

账号/角色查询、双库与选择槽对齐、私有快照限制及静态动态闭环细节，执行前读[账号角色与算法分析闭环](account-role-and-analysis-loop.md)。
