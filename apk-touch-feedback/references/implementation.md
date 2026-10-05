# 实现记录与跨 App 复用指南

## 可复用做法

Flutter：为 Filled/Elevated/Outlined/Text/Icon/SegmentedButton 配置 pressed overlay，颜色沿用主题，仅混入低透明暖色。InkWell/ListTile 使用受边界裁剪的立即着色 ink；如果默认淡入让快速点击看不见，可实现无持续 ticker 的 InteractiveInkFeature，confirm/cancel 时 dispose。导航包装层可用 Listener 观察按下并用 IgnorePointer 绘制，不替代 NavigationBar 的选中回调；支持 RTL、非等宽布局时必须按实际目标矩形命中，不能直接复制等分算法。

原生 Android/Compose：优先复用现有 pressed state/ripple 或 interactionSource，保留无障碍语义、焦点、禁用态及触摸目标。不要为了统一效果重写所有手势。

耗时动作状态按 idle → running → success/error/cancelled 管理。按钮即时反馈与任务进度分离；启动任务前更新局部状态，IO 异步，CPU 密集工作按平台移到 worker/isolate，并限制并发。单纯 await Future 并不能把同步 CPU 工作移出 UI 线程。动画只在可见且 running 时存在；返回页面、失败和取消清理订阅/timer。保留页面状态时要评估 retained view 的内存成本。

## 已有 VibeKits 实现证据与边界

参考源码相对路径：lib/app/pad_press_ink.dart、pad_feedback_navigation_bar.dart、app_theme.dart；测试 test/app_touch_feedback_test.dart。2026-10-02 记录覆盖八类通用控件与一级导航：按下 16 ms 像素变化、回调未执行，抬起只执行一次。真机已有一级入口按压与选中证据，但不能据此宣称所有二级按钮或所有等待态已通过。

2026-10-03 同进程多轮全页面导航出现 Native Heap 持续增长；健康的标准 heapprofd 采样定位主要新增分配到 Flutter FreeType CFF 字体加载栈。PAD 原来指定 Windows 字体，改用系统 sans-serif 的对照仍待实机验证，不能作为已解决根因写入其他 App。此例说明按压测试成功不等于资源门禁通过，字体/图片/Markdown 也需要单独测量。

2026-10-05 后续实证：主字体改为打包TrueType、再补TextTheme fallback，仍未消除长导航增长。有效heapprofd与匹配Build ID/.text的引擎、Dart符号将主要存活分配定位到按钮RenderParagraph→_RenderInputPadding→FreeType CFF。实际渲染FilledButton文字的fontFamily测试为null：ButtonStyle独立textStyle只设字重，替换了完整主题字体。只为Android按钮文字样式补主字体/fallback，保留桌面字段，负例变正例；dev513的43项帧/字体/取消测试、10000事件、独立CPU与内存窗口通过。该设备证据不是所有App的通用结果。

复用时：当字体改动或原生堆增长与文字布局相关，检查实际RenderParagraph/控件独立textStyle，不只检查ThemeData声明；保持原字体首选、字重、颜色、禁用和手势语义。符号必须与目标机器码一致，采样缓冲溢出/客户端错误不能拿来完整归因。不要重启清缓存掩盖增长，也不要把单次缓存预热、ADB观察断流、零差异动画采样误判为产品根因。等待动画像素应与同一任务的运行状态互证，停止应验证真实取消终态。

## 可执行验收方法

1. 建立按钮矩阵：主导航、设置、对话/模型菜单、确认/取消、删除、下载、仿真开关、自绘控件；覆盖 light/dark、禁用、长按、滑动取消、重复点击。
2. Widget 帧测试在 pointer-down 后 pump 一帧，对比像素；此时动作计数应为 0，up 后为 1。验证 cancel 不提交。仅检查 onPressed 或截图最终状态不够。
3. 真机用正常触摸验证立即反馈；需要帧时间时用可靠的 frame timeline/视频或应用测量，确认数据源有真实帧。Flutter gfxinfo 的 0 帧不能当流畅证据。动作超过 1 秒时核对局部动画、可取消及其他会话仍可操作。
4. 同设备同版本固定会话、页面顺序、进程年龄与采样窗口，测冷启动、空闲、导航重复轮次、聊天滚动和推理时 CPU/PSS/native heap。标注 CPU 单核/全机口径。没有温度/功耗证据不宣称低发热；不强制八核固定频率。
5. 资源持续增长先定位分配来源，不以重启、超时或卸载页面掩盖问题。按需加载组件只针对确定未使用的常驻成本，保留基本功能和状态。
6. 覆盖安装核对包名、签名、版本、聊天、原 ID 和授权连续性。远程仿真要实际连接返回的动态 ADB 地址并读取设备身份；在线/connected/adbReady 标志不代替端口可达和 ADB 命令成功。

交付矩阵字段：控件/状态、预期反馈、帧测试、实机动作、耗时/动画、CPU/内存、结果与证据。发布沿用项目原技能，此技能不授予额外设备操作或发布权限。

## Native screenshot feedback sample occlusion gate (2026-10-05)

A focused target app is insufficient on PAD: KBoardPhysicalKeyboard can be a non-focusable full-screen touch overlay. Before and after every native press sample, inspect the actual D0 input window. Reject samples while the overlay covers the target; use only its observed normal hide control, never stop or modify another app. Guarded PAD522 checks cover180 down/cancel observations. A32ms or180ms sleep before screenshot is not measured display latency; pair native visibility checks with16ms widget-frame tests. Duplicate semantic nodes with identical bounds are not distinct buttons.
