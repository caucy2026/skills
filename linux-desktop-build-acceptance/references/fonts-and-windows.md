# 字体、编码与透明窗口

## 先分清“乱码”是哪种

| 现象 | 首先检查 | 不应直接下的结论 |
|---|---|---|
| 同长度中文词都是相同方框/空白 | 字体cmap覆盖、所选family/fallback、FontLoader是否在首帧前完成、包内真实文件 | 系统字体一定没装；文件编码一定错 |
| 显示ä¸­æ–‡等乱码 | 源文件/资源/接口/终端的原始UTF-8字节与解码边界 | 换一套中文字体即可修复 |
| 旧版正常，新版异常 | 旧版**实际源码与完整包**的Linux条件分支、主题/按钮字体、资源SHA、SDK/引擎差异 | 最新main天然包含旧机器适配 |
| 字形被裁切、行高/基线异常 | 真实字体度量、TextStyle/行高、FittedBox与安全区、窗口尺寸 | 有字体文件就算正确显示 |

`locale`和`fc-match 'sans-serif:lang=zh-cn'`只证明系统环境/可匹配字体，不能证明Flutter实际用了它。先比较代码和包，不重装字体碰运气。

## 两个已证实案例，不能混成同一原因

**VibeKits，2026-10-22：**旧705在Linux和PAD均绑定随包VibeKitsPadSans；新版同步漏掉Linux条件，只在PAD绑定，Linux退回Windows字体名/引擎fallback。系统Noto存在、locale正常，两版TTF的SHA也相同。根因是Linux主题/按钮适配漏合，不是字体文件丢失。恢复原Linux分支、保其他端行为，旧源码负控失败/修后通过；746实际公开应用中心中文显示已查看通过。

**KEMI远程办公，2026-10-26：**ARM3.41.9系统Noto可用，但包缺随包CJK与明确主题绑定，真实“应用”“关于”出现方框。增加Linux-only Regular/Bold/OFL，启动前加载family，亮暗主题fallback，Linux CMake安装；不是强制其他端换字体或SDK。真实字形测试和454自有窗口中文字均验证。来源为RustDesk main `9d2a0cedcf8caf1e43428ba8b8def2bc8cc66951`及该提交`client/kemi-docs/LINUX454_FONT_CORNERS_ACCEPTANCE_20261026.md`；此结论不代表硬编/整包发布通过。

## 最小修复与验收

- 便携中文包需要时随包提供有许可和来源的CJK字体；不要每次下载新字体或复制系统字体覆盖项目。验证目标常用中文/拉丁/数字cmap、粗细资源、最终包路径、许可与SHA。
- family别名必须和加载/ThemeData/TextStyle一致。只有文件、assets声明或系统字体名不够；显式TextStyle可能覆盖主题。主窗口、CM和多窗口要各核启动链。
- 用实际引擎做缺资源负控、恢复重试、同长度不同中文词非空且非相同方框、实际字重区分；再查看新候选自己的公开中文界面。源码grep/测试数不能替代真实字形。
- 取图绑定实际PID/出生、窗口所有者和安全页面；不要读设备密码、Key、聊天或其他窗口。优先准确窗口/公开区域，不截全屏再裁剪冒充窗口范围。

## 倒角黑底不是字体问题

GTK CSS透明、RGBA visual、GL alpha与Flutter底面透明是不同层。检查每层，不把整窗opacity调低导致内容也透明。

实际ARM Flutter3.41的FlView有公开背景色接口，默认黑；锁定window_manager只改CSS。远程办公对主窗口和before-realize子窗口清除该底面。旧x64 Flutter3.24没有同名接口，不能无条件链接新符号；可按真实SDK做编译特性检测，或如已验证案例通过dlsym查公开接口，缺失保留旧路径。不要改全局pub缓存插件或用版本号猜API。

正常窗口验证四角**实际alpha**与内部不透明，保留合理阴影；最大化通常应方角，恢复后回原尺寸和圆角；子窗口另验。XComposite是预乘BGRA，保存PNG应转换成straight RGBA；丢弃alpha的RGB图像会把已透明的圆角显示成黑色，不能以此误判。只在已授权的自有窗口范围取样，不读根桌面。

## 证据定位

- VibeKits：`docs/acceptance/LINUX101_FONT_REGRESSION_CLEANUP_20261022.md`，含原错误、746完整运行与截图核验、Mac归档UID问题。
- 两App近期验收总表：VibeKits main `383d0546c12bcd4c6dee141dbdfe4369ce36df38`中的`docs/acceptance/LINUX101_RECENT_ISSUES_ACCEPTANCE_20261026.md`。
- 用户所称110已确认是原101，仅是案例设备，不能硬编码为其他项目默认目标。案例PID、IP、路径和历史PASS不是下次运行的当前事实。
