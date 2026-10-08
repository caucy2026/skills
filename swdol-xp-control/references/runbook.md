# 操作手册：下一次直接照做

## 0. 先知道这份手册解决什么

任务对象是 **86Box XP里的原版SWDOL客户端**，不是macOS自研客户端，也不是UTM Windows Server 2003后台。

已完成的实际动作是：启动原版、前端观察注入、DirectInput接管、登录、选服、选角、昆仑山进图、打开魔法书、切到特殊类、点击秘境传送、最终到达人族秘境。自研客户端用另一个阴阳师账号先验证了同样的技能路径。

最快执行原则：先判断当前在哪一页，只做剩下的动作。不要每次都“从部署开始”，也不要在魔法书已经打开时再点开关。

## 1. 固定位置：不用重新全盘搜索

| 内容 | 位置 |
|---|---|
| 本技能 | `/Users/kemi/.codex/skills/swdol-xp-control/` |
| 项目控制脚本 | `/Users/kemi/coding/swdol2026/tools/xp-original-control/` |
| 原版工具仓库 | `/Users/kemi/coding/xyOnlie/` |
| 既有DirectInput发送器 | `xyOnlie/client/tools/dinput-proxy/send_input.py` |
| 既有后台Map14脚本 | `swdol2026/tools/legacy-dynamic-trace/map14_attach_only_scm.py` |
| 既有collector | `xyOnlie/tools/legacy-dynamic-trace/collector.py` |
| 输入锁 | `/private/tmp/swdol-86box-input.lock` |
| 前台事务入口 | `xyOnlie/tools/legacy-dynamic-trace/with_86box_input.py` |
| 前台回读程序 | `xyOnlie/tools/legacy-dynamic-trace/build/mac-frontmost` |
| 精确窗口聚焦程序 | `xyOnlie/tools/legacy-dynamic-trace/build/focus-86box-window` |
| 成功载荷和截图归档 | `swdol2026/document/evidence/20260920-xp-control-artifacts/` |
| 暖重登计时证据 | `swdol2026/document/evidence/20260920-xp-minute-login/` |
| 原版施法和到达证据 | `swdol2026/document/evidence/20260920-xp-transfer-success/` |

路径前缀的 `xyOnlie` 展开为 `/Users/kemi/coding/xyOnlie`，`swdol2026` 展开为 `/Users/kemi/coding/swdol2026`。脚本不依赖聊天记忆里的临时源码。

## 2. 第一次动作：只读状态，不先乱点

```sh
python3 /Users/kemi/.codex/skills/swdol-xp-control/scripts/status.py \
  --vm-name "<本任务已分配的精确VM名>" --capture /private/tmp/xp-current.png
```

读取JSON里的 `vmPid`、`windowId`、`title` 和 `frontmost`，再看 `/private/tmp/xp-current.png`。这一命令不切前台、不登录、不注入。

如果显示多个匹配VM/窗口，先消除身份歧义，不选“第一个”。历史 `64669/2348/1768` 分别是当时宿主VM、窗口、游戏PID，不是下次的固定值。

### 按当前画面选分支

| 现在看到什么 | 下一步 |
|---|---|
| XP桌面 | 正常打开“登入器.exe”，见第3节 |
| 桃花源标准登入器，有“开始游戏” | 普通按钮启动，见第3节 |
| 更新错误框，问是否使用当前版本 | 选“是”，不要选否 |
| 游戏主菜单“进入游戏/离开游戏/版权宣告” | 若控制已就绪，跑第5节一分钟重登 |
| 账号密码页 | 核对保留账号、密码是否空、插入光标，再提交；不再点击主菜单坐标 |
| 服务器页 | 点击已确认服务器；不要重输密码 |
| 角色页 | 选择已授权角色，再点进入游戏；避开删除角色 |
| 世界，魔法书未开 | 第6节 `--panel-state closed` |
| 世界，魔法书开着且不是特殊类 | 第6节 `--panel-state other` |
| 世界，特殊类已选 | 第6节 `--panel-state special`，直接第一个技能 |
| 错误框/控制台挡住游戏 | 只处理当前窗口，别向背后的游戏盲发坐标 |

不要把菜单打开、角色站立或截图不黑当成完整会话健康；还需当前角色、地图和控制连接。

## 3. 桌面到“是”：就是普通按钮

### 2026-10-05现场校准：标准启动与新进程首次输入附加

本轮完整恢复耗时未达180/240秒，不能记达标。以下只记录已实测剩余动作，不能将局部耗时相加冒充冷恢复通过。

- 当前A已确认桌面单列图标中第七项是标准登入器.exe，第八项是800×600启动器；只在相同布局新截图确认后，可用Win+D、Home、Down×6选中，再核名称后Enter。绝对宿主点击未移动来宾鼠标时不要反复猜倍率。
- 已开标准登入器：本轮实际成功的驻留按钮工具为`C:\xyol-trace\xyol-client-launcher-click.exe`（r395成功记录复用）；进入“开始游戏”后更新错误框默认“是”用Enter继续。本轮D盘`clicker.exe`实际不存在，旧D盘命令只有现场存在才可用；不要为这个按钮另造注入体系。
- 原版输入器只支持规定ASCII字符。不要逐字输入中文EXE名；选已确认桌面入口或现存ASCII按钮工具。`target_keys run`先校验全部字符，未支持的引号会在发键前拒绝。vminput文本原曾遇中文后留下部分命令，源已加入全量前置校验，独立候选拒绝路径通过，当前安装二进制尚未替换。
- XP的taskkill不能同时使用/PID与/IM。本轮首个双参数命令实际未结束进程；纠正为已现场核验的/PID后成功结束旧1216。仅操作本人唯一游戏PID，不能套后台系统的命令语法。
- 新游戏进程只收到观察器Ready，不代表输入DLL已加载。本轮1560实际tasklist /m xyol-input.dll无匹配，控制连接超时4.198秒；先核模块，再一次运行现存`C:\xyol-tools\xyol-injector.exe`。新PID无模块才能首次附加；不要再次加载已驻留的DLL。
- 宿主先开27666单监听，命令输入立即归还前台，再后台accept；复用现有verify_input_peer_owner拒绝非A连接。当前1560首次控制附加从1791176546589628000到1791176550181290000共3.592秒，owner80742且仅发送noop。这只证明输入附加与owner，不是前后端登录进图成功。
- 登录脚本的SERVER_SELECTION_SENT和44秒响应截图仍可能是“正在连接”；停止在响应页供核验，未见实际选角不能继续发选角坐标。角色/世界/PID/backend事件均齐才关门。



用户明确说明过的顺序：

```text
先把焦点切到真实XP窗口
→ 打开桌面“登入器.exe”
→ “开始游戏”一次有效点击/双击组
→ 等待更新错误框
→ 选择“是(Y)”
→ 原版游戏主菜单/账号流程
→ 这之后才接DirectInput控制
```

### 必须选对桌面入口

- 正确：`登入器.exe`，显示桃花源大登录器和底部一排普通按钮。
- 另一个图标“启动器800×600”不是本次完整成功流程的入口。不能因为都能出现某个主菜单就把它们当同一启动链。

### 输入前后怎么保持前台不打架

单组输入统一包在：

```sh
python3 /Users/kemi/coding/xyOnlie/tools/legacy-dynamic-trace/with_86box_input.py \
  -- <本组已经确定的输入命令>
```

它独占输入锁，记录原前台PID，精确找到XP窗口，切入并回读，输入结束后恢复。原前台可能是Codex、自研客户端或其他用户窗口，必须恢复实际原值，不能固定恢复Codex。

工具退出码0只说明工具执行，不能证明按钮被游戏消费。检查下一阶段是否真的出现。不要在用户正在改变窗口时争抢焦点；组内变更就停下。

### 本次普通按钮的成功备用入口

若宿主双击没有可靠命中，复用XP中已有的正常点击器：

```text
C:\xyol-trace\xyol-client-launcher-click.exe
```

它是普通窗口点击工具，不是DirectInput。由XP交互用户执行，不由后台机器SCM执行。

准备一次定向键盘工具：

```sh
python3 /Users/kemi/.codex/skills/swdol-xp-control/scripts/control.py prepare
```

随后按当前VM PID发送Run命令：

```sh
python3 /Users/kemi/coding/xyOnlie/tools/legacy-dynamic-trace/with_86box_input.py -- \
  /private/tmp/swdol-xp-target-keys <当前VM_PID> run \
  'c:\xyol-trace\xyol-client-launcher-click.exe'
```

出现更新错误框后，使用普通Y键（macOS keyCode16）：

```sh
python3 /Users/kemi/coding/xyOnlie/tools/legacy-dynamic-trace/with_86box_input.py -- \
  /private/tmp/swdol-xp-target-keys <当前VM_PID> key 16
```

不要在没有“是/否”框时盲发Y；不要连续重开已运行的登入器。`Program PrevInstance`仅证明某个实例已经运行，必须看进程/窗口，不能猜游戏已登录。

## 4. 注入就绪：先复用，只有缺失才部署

### 两种注入不同

| 通道 | 作用 | 成功标志 |
|---|---|---|
| `C:\xyol-trace`观察器 | 读取协议/函数/绘制业务事件 | 当前目标的ready、heartbeat、所需业务探针 |
| `C:\xyol-tools` DirectInput | 输入移动/按钮/键盘状态 | 实际控制连接及游戏UI消费结果 |

两者不能互相替代。只有观察器ready，不代表能控制鼠标；只有控制TCP连接，不代表所有键盘模式都有效。

同一游戏PID若已驻留控制DLL，直接复用27666。不要再次LoadLibrary，不要重新挂部署盘，不要因三分钟掉线而重新注入。同一个进程回主菜单，控制载荷通常仍在；游戏进程或VM重启则重新核验。

第一次部署详见 [首次准备](provisioning.md)。已有成功归档制品，默认不重编。

## 5. 一分钟重登：实际计时通过

### 适用前提

- 当前画面确实是游戏主菜单。
- DirectInput已连接过且仍驻留；只允许一个27666监听者。
- 原服登录/目的地图健康，账号为已授权测试账号，未被另一端同时占用。
- 角色页为本次验证过的800×600布局、左侧目标角色；不是未知账号/删除角色页。
- 先运行status取本轮真实PID和窗口号。

### 标准命令

```sh
python3 /Users/kemi/.codex/skills/swdol-xp-control/scripts/control.py relogin \
  --account taishen \
  --expected-vm-pid <status返回的vmPid> \
  --window-id <status返回的windowId> \
  --remembered-account \
  --verified-stage main \
  --output /private/tmp/<本轮全新目录>
```

`--remembered-account` 只用于重登页面保留同一账号、空密码框已聚焦的状态。首次空账号页不加此标志。不同账号不能直接使用这个标志，否则可能给旧账号提交新密码。

### 脚本具体做什么

1. 记录单调计时；60秒超时失败。
2. 独占前台输入锁，核对VM代次。
3. 定位并聚焦实际XP窗口，保留原前台。
4. DirectInput点击主菜单“进入游戏”。
5. 从授权快照内存读取密码，stdin送给定向键盘工具，Enter提交。
6. 选择轩辕镜；保存服务器页。
7. 选择左侧角色；保存角色页。
8. 点击进入游戏，等待加载，保存世界页。
9. 恢复原前台并回读；输出脱敏JSON。

成功样本：2.607秒主菜单点击；4.081秒认证提交；8.816秒选服；15.446秒发出进图；总 **27.879秒**。本日其他暖重登记录也约26.7—27.4秒。

报告 `ACTIONS_SENT_VISUAL_VERIFICATION_REQUIRED` 不是PASS。必须查看 `world.png` 是否有预期角色、地图名称和世界HUD。确认后另写视觉判定，保留原报告。

## 6. 魔法传送：不要再在三个点击之间拆成十几轮

### 已确认的UI含义

自研客户端源码 `client/platforms/macos/BgfxCharacterLab.mm`：

- 800×600逻辑画布底栏 `x=600..636, y=570..594` 调用 `toggleBottomPanel(Magic)`。
- 中心 `(618,582)` 是紫色魔法按钮。
- `toggleBottomPanel` 在相同面板已经打开时关闭它，因此**只能单击，不能双击**。

自研客户端已实点完成“开→关→再开”，不是只引用源码。随后点击第五类和第一个格子，实际从昆仑山到Section0。

原版同样的按钮和图标已经实测；但原版魔法面板本轮起点 `(400,350)`，自研面板是 `(400,380)`，有30像素竖向差。两边设计相同不等于所有绝对坐标相同。

### 坐标表：不要混域

| 动作 | 原版游戏逻辑坐标 | 归零后的DirectInput相对量 |
|---|---|---|
| 魔法开关 | `(618,582)` | `(309,291)` |
| 第五个特殊类标签 | 约`(576,376)` | `(288,188)` |
| 特殊类第一格秘境传送 | `(436,410)` | `(218,205)` |

这些是本轮原版800×600、未拖动面板的已验证位置。不是宿主屏幕坐标，也不是带窗口阴影截图的像素坐标。窗口移动不会改变游戏逻辑坐标；面板拖动、分辨率变化则必须按新截图重新定位。

### 成功输入节奏

整组三步复用一个TCP连接。每步：

```text
发送 (-10000,-10000)，buttons=0       归零
等待1.5秒                           确保当前输入轮询消费归零
发送目标(dx,dy)，buttons=0           移到目标
等待1.5秒                           不在旧光标位置按下
发送 (0,0)，buttons=1                单次左键按下
等待0.4秒
发送 (0,0)，buttons=0                左键抬起
等待2秒
保存本步截图，然后做下一步
```

最后一次点击后等待施法和地图切换。按下后必须在finally中释放；不要断在持有鼠标的状态。成功脚本原件为归档 `executed-sequence.py`；持久化参数化入口为 `magic_sequence.py`。

### 已在世界，魔法书关闭时

```sh
python3 /Users/kemi/.codex/skills/swdol-xp-control/scripts/control.py magic \
  --expected-vm-pid <当前vmPid> --window-id <当前windowId> \
  --panel-state closed \
  --cast-secret-gate --verified-skill 10633 \
  --output /private/tmp/<本轮全新魔法证据目录>
```

### 魔法书已经打开时

- 不是特殊类：把 `closed` 改为 `other`，不再点开关。
- 已经是特殊类：改为 `special`，只点第一个传送格子。
- 用户只是要求查看魔法书：不加 `--cast-secret-gate --verified-skill 10633`，不主动施法。

`--verified-skill 10633` 是调用者已经检查当前角色学会秘境传送、特殊类第一格正确的声明，不是让脚本凭ID改状态。脚本仍只发正常鼠标输入。

### 成功如何判定

本轮原版截图逐步证明：

1. `xp-three-book.png`：魔法书打开，特殊类图标可见。
2. `xp-three-special.png`：第五类“特殊类”标签确认。
3. `xp-three-transfer.png`：名称“秘境传送”，说明“传送到昆仑秘境。”。
4. `xp-three-result.png`：人物施法、技能暂时灰掉；**这只证明施法进行中，不代表到达**。
5. `xp-transfer-final-verification.png`：小地图“人族秘境 `(231,212)`”，场景为新手指引区；到达通过。

界面说明“昆仑秘境”和实际小地图“人族秘境”并不表示选错技能：本轮对应Magic10633的目的Section0，必须结合实际资源与地图确认。

## 7. 三分钟窗口怎么用

先看自研客户端/源码，把路径准备好，再登录原版。不要边在线边寻找该点哪个按钮。

- 进入世界后记时间。
- 一次登录验证一批同场景菜单和关联状态：登录前准备入口、坐标、初态、操作顺序、采集点和预期结果；进图后连续执行开关、确认/取消、拖动、快捷栏及相关显示验证，不按单个菜单重复登录。需要不同权限、角色或地图的项目才分批；未知入口先在后台分析，不占在线窗口。单项失败只停止依赖动作，继续已准备的独立项目，身份/代次失配则停止该输入组。
- 常见操作整合成一条有60秒截止的输入组；不是每步发一条消息等下一轮推理。
- 150秒前停止追加动作，保存结果；超过当前会话期限先重登。
- 首次三分钟断线不要延长计时器或改EXE。原因分析独立安排，见断线参考。

## 8. 操作前检查清单（简短执行，不变成大测试）

```text
[ ] 目标是XP还是Server 2003？
[ ] 当前真实VM PID、窗口号？
[ ] 当前画面是哪一阶段？
[ ] 游戏进程/控制载荷代次是否仍然相同？
[ ] 是否已有其他任务占用27666或前台锁？
[ ] 初态魔法书是关、其他类、特殊类？
[ ] 角色已学、格子和目的地是否已确认？
[ ] 原前台已记录，动作后恢复？
[ ] 本轮证据目录全新？
```

除了首次部署所需CPU/文件身份门，不再先跑48项通用测试、十客户端、successor矩阵或旧Plot门。

## 9. 收尾

保存阶段截图、真实计时、目标身份和动作报告；不要记录密码。关闭本轮拥有的控制监听，停本轮collector以防无界日志；保留已授权的常驻观察器。

未由本任务启动的客户端、其他同事的实验和原服务器都不随意结束。若用户要继续观察，则保留当前原版会话并明确它仍受三分钟限制。

2026-10-03双VM纠正：status.py必须显式--vm-name，默认VM曾选择XP A而本任务分配B。不得依前台PID猜截图所有者；先核精确名、进程、窗口。该修正只读，不授权暂停另一VM。

## 同窗多证据采样补充

进图前把输入组、接收器、截图点和比较参数全部准备好；新登录重新取得角色运行句柄，即使游戏PID未变也不能沿用上次角色句柄。已核原版控制对象路线是`DWORD[0x80A368]→Actor首DWORD`，只在对应锁版本合同下使用，不把账号/角色ID当运行句柄或换版通用地址。进图后立即执行已准备动作组，组后归还实际原前台，再后台分析；避免在线窗口内长时间找路径或思考。

单对象缺事件或失败，只停止其依赖动作，继续其他已准备且独立的样本；版本/PID/代次门失败则停止整个本组，不能继续向失配目标输入。有22条预期记录的采样只收到21条、缺terminal时仍为`INCOMPLETE`，不能按部分数据写完成。

### 2026-10-07世界内点击不得停在边缘

FIX世界mode0/2的无按钮边缘输入会每处理给yaw±4度，原reset到左上再等0.6/1.5秒可能旋转相机；不能把UI之前朝北当作UI之后仍对齐。登录页原成熟reset路线不因此改写。

世界内先复用RCAMA4有界完整采样：record7 base806FF8，+72/+76为软件cursor X/Y，+28是倍率（本轮2），bounds须800×600；只按实际读回的cursor/gain计算内域相对移动，不猜旧坐标。fresh-read→鼠标输入→相机readback写成同一连续组，沿用当前proxy、VM精确身份/peer/input锁/组末归还前台。采样过期拒绝输入，不放宽阈值；实际yaw读回才能证明稳定。

本轮局部实测：434,468→400,300无点击yaw180保持；Action输入后仍180；朝北后yaw0，再Magic点击仍0，cursor618,582。证据在/private/tmp/camera-magic-fresh-before-20261007/capture/manifest.json与after同名目录；不等于完整冷注入180秒通过。当前/private/tmp/newpair-a-current-cursor-click-20261007.py为已测host候选，仅当前1560绑定；新游戏须重核PID及源码版本，不直接照抄历史数字。
