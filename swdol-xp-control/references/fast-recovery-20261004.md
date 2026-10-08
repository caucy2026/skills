# XP恢复耗时复盘与固定流程（2026-10-04）

本轮未完成三分钟登录及前后台业务闭环。r390从首个窗口排查文件创建起就超过314秒，该起点晚于实际开始，因此只是耗时下界。总耗时不能从中扣掉工具往返、思考或更换编号后重新计时。没有成功登录时，不把方案称为“三分钟保证”。

## 已测时间及主要损耗

| 项目 | 实测 | 判定 |
|---|---:|---|
| 单次控制附加并进入账号页 | 15.17、15.44秒 | 两轮B局部实机成功，非完整恢复 |
| 账号页登录脚本 | 55.75、56.42、55.79秒 | 最终仍停选服，均不算登录成功 |
| 新普通键序列内部耗时 | 2.76秒；捕获后3.46秒 | A未打开登入器，不能算加速成功 |
| r390窗口排查及后续 | 至少314秒 | 180秒门失败 |

主要损耗由执行方式造成：把固定连续操作拆成许多工具和模型回合；窗口最小化时反复走只查可见窗口的入口；定向键未消费后没有立即采用已有备用输入；在恢复中反复找路径和写临时脚本；固定延迟后继续发选角，未等服务器阶段完成。不能把这些全部归为服务器慢。

A最后实测：未捕获时桌面无变化；按成熟普通点击捕获后，标题变为释放鼠标提示且“我的文档”被选中，但六次Down没有得到登入器，仍未打开。Home+六Down在B曾成功，不得仅因图标顺序相同就把A也记成功。保留差异，不继续无证据重复该键序列。

## 固定与保留动态判断的边界

用户最新分配：当前客户端任务固定第一台A，另一同事第二台B。A精确名称 `XP SWDOL Voodoo3`；B为 `XP SWDOL Voodoo3 B`。完整标题中的 ` - 86Box` 用于消除前缀歧义。PID、窗口号、游戏PID和后台代次每次动态发现，不能固定旧数字。任何输入peer必须用lsof核为本任务宿主PID，不暂停同事VM。

固定复用标准登入器→开始游戏→更新错误“是”、已有观察器、审核的单次控制附加、已验证输入1.5/1.5/0.4/2秒节奏和stdin凭据读取。窗口不可见时直接用成熟focus-86box-window取消最小化；不先新写窗口扫描。屏保只做已验证Shift唤醒。出现未消费输入立即走已有故障分流，不重新发明控制器。

普通键序列已收进 `tools/xp-original-control/normal_input_sequence.py`，带精确VM/PID/窗口、共享输入锁、前台检查、前后截图和继承全局截止；目前只是局部发送入口，A登入器启动仍未通过。它不自动选择后续页面或声称登录通过。注入15秒路线待A实证后再收为跨VM固定流程。

## 下一轮目标预算（未验收）

身份/当前页15秒；标准启动30秒；只补缺失观察与控制20秒；认证/选服/选角60秒；真实动作与同代后台事件35秒；余量20秒。合计180秒。准备在执行前完成，执行后只回读必要终态；后台独立只读核验与前台启动并行，输入/注入变更顺序执行。现有脚本选服阶段需要明确就绪门，不能把固定2秒当就绪或盲点选角。

连续复跑必须一次完整包括前后台就绪、真实进图和后台动作。超时保留失败，再读对应成功记录、核差异；不得通过缩小目标、改编号或减少必要身份门伪造达标。

## 2026-10-04: verified A recovery details (CPU comparison run)

A reached the original world with helen2 at Changyang (545,569). Credentials-to-world took 55.658s; DirectInput attachment took 15.419s. Full recovery exceeded the user's 240s limit. These component timings do not establish a cold-recovery PASS. Evidence: `/private/tmp/cpu300-helen2-login-20261004/report.json` and `world.png`; archive temporary evidence before treating it as a durable reference.

- `86box_trace_media.swift` argument 2 takes the exact VM NAME, e.g. `XP SWDOL Voodoo3`; it appends ` - 86Box` internally. In contrast, `with_86box_input.py --title` takes the discriminating title prefix. Do not interchange these parameters.
- Verify the mounted file with `lsof -a -p <currentPID> <ISO>`. Without `-a`, unrelated descriptors are printed.
- A desktop Run used the proven HID path after mouse capture. Game credentials used the default PID-targeted path. Verify the actual page and foreground; do not force one delivery mode on every input.
- Generate Windows path literals with proper quoting (`repr` when generating Python), not literal string substitution: backslash-a becomes a control character. Credentials remain stdin-only.
- An immediate screenshot after Run may still show the desktop. Inspect the result of the SAME operation before retrying. ARM later visibly reported `Base observer ready`; early absence was not failure.
- Resolve Desktop from Shell Folders, rather than assuming an English Desktop path. Existing LAUNCH2.BAT followed that route. Use the existing launcher click helper, and send Y only after seeing the update-error question.
- Verify every control peer against its actual host VM PID. This login rejected a different VM's connection before succeeding. Never assume the first peer is A.

CPU300 is a reversible diagnostic comparison, not a proven fix or a mandatory injection prerequisite. Do not change server timeouts or system time to conceal the failure.


## 2026-10-06 已验证只读采样衔接与媒体选择纠错

本记录是局部成功路线，不是完整冷注入三分钟通过。A同一来宾客户端先由tasklist核PID；现场PID/窗口必须重新发现，不能复用下列历史数字。证据原位：`/private/tmp/original-name-native-bounded-chain-20261005/receipt.json`与`handle-79/series.json`；43项必要证据已归档GitHub main `2bf9fa8ffb63a0549571476aadbbd65f90af79c8`的`document/evidence/20260930-two-new-test-role-gate/current-main346-20261005/`。

- 实际工具路径是分析仓的`tools/legacy-dynamic-trace/with_86box_input.py`及`tools/legacy-dynamic-trace/build/86box-vminput`；不是产品仓同名目录或猜测`/tmp/86box-vminput`。先确认存在，在后台准备整组命令。
- A光驱当前Qt控件为窗口内`AXImage`，描述`光盘 1 (ATAPI): …`，不暴露AX动作。旧工具只找菜单项会失配。已实机成功的备用是：精确PID/窗口与输入锁→依据刚读控件几何普通右键→定位可见弹出菜单项→普通点击已存在的批准只读ISO历史项→立即归还前台→`lsof -a -p 当前PID ISO`回读。隐藏主菜单和可见上下文菜单有同名历史项，必须按当前可见弹出窗口几何唯一匹配，不能简单取第一个；不打印整个系统菜单或近期文件。
- 只读盘成功例含TICK.EXE/REMOTE.EXE。窗口媒体标签或点击返回0不能证明已挂载；还需句柄及实际盘内容/制品SHA。原生Open确曾打开，但GoTo快捷键两次无实际变化；该快捷键路线没有成功证据，不继续盲发或把AXFocusedWindow成功当文件选择成功。
- cmd存在但被游戏盖住时，已验证一次普通Alt+Tab可恢复实际提示符；先看提示符再输入。普通命令组开始0.8秒已验证消费间隔；`tasklist`先看到运行中再回看同命令完成输出，别立即重复。控件或焦点变化就停止该组。仅“输入已发送”不能核来宾PID。
- 本次完整14-record原客户端self采样：明确账号页后复用`session.py relogin --verified-stage credentials`，只有实际截图已确认账号才可`--remembered-account`；从credentials到默认进入世界动作54.242秒，紧接读取self14包11.121秒。主菜单第一次43.612秒动作序列实际仍在主菜单，保留FAIL，不靠后续成功抹掉。初入之后不要再开始长文档阅读/编译/路径研究，把接收器和全部命令预先准备。
- 已挂旧REMOTE制品SHA `331ea5997d12fa9b020d2dac2b343771cf33680b214182a57e7c024d0844fbfe`发送456-byte内存+clock组合；必须使用现成`collect_remote_actor_series.py --samples 1 --require-guest-clocks`。旧`collect_remote_camera_actor_v1.py`只接受412-byte，配错将全部丢弃。先READY再guest执行，单UDP端口顺序用，独立nonce/目录；首失败停止批量，保留失败与guest页/错误码。self COMPLETE不等于其他handle存在或字体/画面一致。
- Windows命令路径只生成一个反斜杠；先在后台校验最终argv，不把JSON展示中的转义当实际路径。游戏PID与宿主86Box PID不得混用。此次handle5零包仍INCOMPLETE，不能推断Actor不存在；新只读v2的诊断/缓存矩阵尚未guest验，不记录成成功。

同一窗口后台另有60条绑定样本，连接正常而非退出根因已修复；两个字段时间并不构成原子画面。原版与我方角色/地图/相机条件仍未对齐，不能称同条件一致。复用的是已证步骤；不保留历史PID为执行常量，不新增注入或任意地址RPC，不占B，不用这份记录降低完整目标/发布硬门。


### 2026-10-06新测试身份切换：实际解释器与计时纠错

需要SMB/MySQL授权内存凭据读取时，复用已安装依赖的`/Users/kemi/coding/xyOnlie/.venv/bin/python`；系统`python3`在本次读取前即报impacket缺失，不应重装或反复猜环境。凭据不进argv/文件。换新账号禁止remembered-account，原世界先底栏设置(776,582)→登出(750,550)→等安全倒数终态→核主菜单，再走成熟登录。60秒session在显式覆盖账号耗时后可能缺进图观察预算；本次55.979秒发进图、57.143秒记录WORLD_OBSERVATION_BUDGET_INSUFFICIENT，保留FAIL，回读真实终态，不能因此重启健康VM或重复登录。后续实际新Role280/281前后端同时在线已证；不据此声称60秒全流程通过。只操作A，不暂停B。
