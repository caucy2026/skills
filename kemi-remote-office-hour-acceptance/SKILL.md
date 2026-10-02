---
name: kemi-remote-office-hour-acceptance
description: 将KEMI远程办公现有验收文档逐项映射为一小时内执行的合并全功能流程，保留兼容性、历史回归及100轮计数和真实接收证据；用于制定与执行验收，不负责构建发布。
---

# 一小时完整覆盖验收

使用 kemi-remote-office-acceptance 的身份核验、原脚本及测试误差诊断。先完整读取当前项目AGENTS、本机规则、验收主文档、R01–R34 JSON及keyboard-quality/TEST-PLAN.md；再读取本技能[覆盖与时间表](references/coverage.md)。项目位置从当前工作区发现，不复制个人机器路径或设备ID。

目标是一小时内完成全部验收覆盖和报告，不能到时即停止、漏项算通过。时间表是执行预算，尚不是实机一小时成功证明。开始即记录候选哈希、对应源码、脏路径、设备双ID和实际在线状态；日志观察器与接收器一次建立，全程采样，避免每个按键重新连接或截屏。

## 合并原则

同一连接的两分钟驻留同时验连续真实帧、中英文、解码组件、Surface呈现、CPU/GPU/内存/FD/fence/TCP；同一次扩展同时验双路动态帧、浏览器投放、第二APP往返、焦点与输入、按钮状态；同一次收回/HOME同时验窗口销毁、资源释放、键盘隐藏、状态恢复。保留原文各平台、起始屏、方向、模式、次数与断言，一个动作可以给多项证据，不能给未执行动作计数。

三个键盘F/N/G及极简态M逐项对照原矩阵，实际中文候选提交、英文、删除、回车和组合键到自建接收器；两屏方向必须验证另一编辑器不变。鼠标菜单、滚动、拖放用宿主实际结果；文件必须经过APP传输并双向hash；语音必须实际说话并核对接收文本。不能用后台注入文本冒充键盘、剪贴板或语音操作。

按用户要求不用录像；R02用操作后前10秒连续呈现计数、帧时间与动态内容标记验证黑屏，无法证明视觉内容时保留必要视觉校准。帧回调成功不等于画面正确。视觉布局、动画和按钮图案也不能只凭enabled属性通过。

## 100次与全功能计数

从当前文档读取100轮的准确含义及每变体10次。明确区分连接100次、按键100步、功能变体10次和全功能整轮100次。原表要求100完整五主机轮时保留该门禁，不能静默改成100连接子循环。将一小时的全部覆盖与100轮要求分别列账，只有两者均满足才能声明对应验收通过。

使用同一候选已有有效证据仅限可追溯、设备/变体/前置完全匹配的子项；不把旧版本通过移到新包。不重复已经有效完成的后台长观察，但没有证据时不能用短窗宣称长时稳定。驻留要求针对原文指定场景，不能无依据套到每次连接造成多余等待。

## 门禁与异常

逐项输出原用例ID、平台/模式/方向、要求次数、实际次数、时间、动作、宿主接收结果、证据路径、PASS/FAIL/BLOCK。任何必测ID缺失、原屏分辨率被更改、旧帧、错误peer、投放窗口不可见、文本少字/重复、解码路径违反要求、资源未回收均阻断发布。硬件支持格式核对真实组件与Surface；不支持格式按用户授权软件解码，禁止把硬件支持误判为编码器能力。

第一次异常保存，检查焦点、遮挡、屏幕、权限及观察通道，再同条件复测。无重复有效复现不修改产品；有效复现后读历史约束、列最小修复和影响矩阵，再针对影响项重测。单PAD动作串行，只读采样可以并行，不干扰客户输入。

开始10分钟内用实际节拍校验60分钟预算。发现赶不上时立即减少重复连接、UI树抓取和纯等待，不能删必测项或降低断言。到60分钟仍缺项意味着本次未达一小时目标，继续完成并记录超时原因，不自动PASS。整理报告与覆盖率必须从真实证据生成。无未知bug不能由任何有限测试保证；交付声明仅限已覆盖条件。

## 重叠执行：远控与视频流

当当前验收范围包含RTSP/RTMP时，在远控循环前启动同一冻结PAD候选的视频服务及独立网页播放器；远控连接、键盘、鼠标、扩展、文件操作期间并行观察真实播放进度、断流恢复、延迟和硬编码组件。不能只验证网页加载或服务已启动。复用当前视频流验收方案及支持对应协议的网页播放路径，浏览器不能直接播放的协议不得临时搭建新转码系统来代替。

长时稳定观察从首次真实播放开始计时，贯穿后续功能动作；远控正常切设备不要求无关地重启视频服务。协议各自断开重连必须执行；涉及同一编码器/Surface的资源竞争动作按真实支持的组合排程，不能为压时间假定RTSP和RTMP可同时开启。单PAD点击、键盘输入及屏幕切换仍串行，网页/日志/资源读取可并行。

共享计时、独立断言：远控必须有正确peer、新帧和实际输入；流必须有客户端实际播放帧、时间戳及恢复；任何一边成功不能替另一边计数。先采仅远控基线，再采混合负载，结束依次停流、断远控并采全关闭回落；归属不清不得称CPU低或无泄漏。结束前确保测试流、播放器及自建接收器正常关闭。

语音测试复用已聚焦的输入接收器；文件传输期间并行观察另一屏视频；后台驻留期间执行宿主版本/签名及权限只读核对。不要把更改同一焦点、升级同一客户端或抢占同一显示屏的动作并行。重叠减少纯等待和重复启动，不删除重复次数、协议分支、硬件热插拔或授权延续证据。


## 2026-10-02 execution status

The first PAD417 run did not achieve the one-hour full-coverage target. Source sync and build succeeded; only bounded subsets have valid evidence. Full100 remains 0/100. Treat this schedule as an unverified budget, never as a release PASS. Read the latest PAD417-ONE-HOUR-RESULT-20261002.md and its coverage ledger before reuse.

For N/F keyboards, an English letter can remain in preedit; verify the visible candidate and commit before asserting receiver text. Preserve first-backspace-after-Chinese differences, inspect actual keyboard callbacks and host key events, and do not infer source failure from an accepted touch injection alone. Repeated observer/channel failures are not product failures. Closed-state codec dmabuf=0 and a short CPU sample do not prove all fences or long-term memory are released.

## 输入接收器现场守卫

每组键盘动作前及切连接后，核对 PAD 当前实际选中 peer 与接收器所在办公ID一致；请求ID、旧日志或接收器文本不变不能替代当前目标核验。窗口可见/应用frontmost不代表编辑区有焦点：检查 AXFocusedUIElement、sheet和编辑区AXFocused。自建TextEdit发生自动保存冲突时，保留双方版本再恢复编辑焦点，并回读保存后的实际文档名；不得清空未知输入、关闭无关客户弹窗或给准备动作计远控通过。目标或焦点不满足时标记测试前置失败，保留证据，纠正后复测，不认定源码故障。

## 控制器连续性与减少观察开销

目标核验在每组开始与连接切换后执行；同组逐动作实际回读接收文本及焦点，避免每个按键重复抓取完整 UI 树。未收到明确目标变化时，不凭旧首帧推断新的连接。将模式、窗口和资源观察合并为共用采样，逐项保留独立断言。

控制器换代必须协作停止：在下一组开始前检查停止标志并写终态，然后新控制器检查实际正文、预编辑及语言。看到上一组最后一条结果落盘不代表生产者已停止，它可能已经注入下一组首键；不可仅据此杀进程再从新组重复注入。发生该类交接差异保留首败与控制器栈，只在精确自建文本核验后恢复夹具、清洁前置重测，准备动作不计验收次数。

## 显示与IME操作前置

复用触点前核对当前真实前台Activity、显示ID及键盘窗口归属。非扩展可能使用KBoardPhysicalKeyboard，扩展输入可能使用标准InputMethod；必须根据窗口owner、mDisplayId、isVisible、surface与实际触摸区域确认，不以窗口名只查一种。鼠标焦点迁移或键盘开关后重新核对可见状态；窗口未显示不得向旧键盘坐标注入、计失败或修改源码。

Android输入显示参数使用现场input帮助核验：input [-d DISPLAY_ID] keyevent KEYCODE_HOME，-d在command前；错误参数可能变成其他按键或默认显示操作。HOME试验前后保留两屏Activity、窗口与按钮状态，单屏目标不成立时不计回归。UI树获取未达idle时不用旧XML作当前页面，先读取窗口/Activity定位；必要时仅一次视觉校准。

## Per-display position and overlay guard

A minimal keyboard can remember different positions on each display. After a display switch, validate the actual control position for that destination; never copy the previous display touch points. The outer PhysicalKeyboard window can remain full-screen in all modes, so its frame is not the geometry of the visible control panel. Preserve the first incorrect-coordinate result and repeat with valid geometry before attributing a product defect. Use one necessary visual calibration only if native window/control evidence cannot resolve geometry.

When the physical overlay occupies the app display, hide it with its real control and verify the window is gone before tapping app controls beneath it. A successful touch injection into a transparent overlay does not prove an app toolbar action occurred. Preserve any unknown text in an old owned receiver; create a unique fresh document, then guard exact text and focus. Do not erase unknown input or identify its author without evidence.

PAD417 follow-up: 10 hide/reopen/HOME/reopen groups completed 40 real window transitions in 19.39 seconds; minimal Enter/delete and corrected cross-display subsets have 60 matching host text receipts. These are measured subsets, not a proof of one-hour full coverage or 100 complete rounds.

## White-box observer and evidence efficiency

For an execution that must minimize screenshots and overlap work, use [white-box execution](references/whitebox-execution.md). This specifies actual receiver evidence, safe overlap and measured pacing; it does not waive a regression ID, variant or complete-round requirement.


## PAD418 白盒效率实测与UiAutomation互斥

已实测输入工具触摸与SOURCE_MOUSE各10组复制、粘贴、Enter，共60个实际接收结果；资源监测同步，零截图。读取whitebox-execution中的实际节拍和守卫。UIAutomator dump与SOURCE_MOUSE instrumentation必须串行，尽管dump是只读观察；交叠会造成测试工具UiAutomation连接/退出异常，不能认定产品崩溃。日志、资源读取仍可并行。子项通过不代表一小时全部覆盖或100整轮已完成。
