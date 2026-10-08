# Codex 全局技能库

面向 KEMI 应用开发、发布、远程调试、磁盘维护、视频制作和浏览器 3D 游戏的可复用技能集合。

本仓库目前包含 **59 个独立技能**：保留远端已有的 44 个技能，并于 2026-10-08 从本机 Codex 全局技能目录新增 15 个、更新 4 个，另有 1 个内容一致。每个技能目录包含 `SKILL.md`，并按需提供引用文档、脚本、素材和代理配置；不包含 Codex 系统内置技能、运行缓存或凭据。公开示例中的签名密码通过安全环境变量提供，本机凭据不上传。

## 2026-10-02 至 2026-10-05 新增同步 · 13 个

| 技能 | 用途 |
|---|---|
| [kemi-harmony-phone-development](kemi-harmony-phone-development/SKILL.md) | 鸿蒙手机控制端适配、构建、真机调试、企业认证和发布。 |
| [kemi-remote-office-release](kemi-remote-office-release/SKILL.md) | 远程办公四平台构建、签名、公证、发布及升级核验。 |
| [kemi-remote-office-acceptance](kemi-remote-office-acceptance/SKILL.md) | 真实设备全功能、历史回归、兼容性和100轮验收。 |
| [kemi-remote-office-hour-acceptance](kemi-remote-office-hour-acceptance/SKILL.md) | 一小时合并验收流程与真实接收证据。 |
| [kemi-server-ports](kemi-server-ports/SKILL.md) | 服务器端口查询、归属登记、预留及冲突核验。 |
| [kemi-windows-two-node-release](kemi-windows-two-node-release/SKILL.md) | 双Windows节点分工编译、硬件令牌签名和发布。 |
| [vibekits-cluster-agent](vibekits-cluster-agent/SKILL.md) | 集群竞标、有效分配下的执行及结果回报。 |
| [vibekits-cluster-capabilities](vibekits-cluster-capabilities/SKILL.md) | 设备能力声明、修改、停用及同步核验。 |
| [vibekits-cluster-deployment](vibekits-cluster-deployment/SKILL.md) | 集群设备远程部署、入房、身份和心跳诊断。 |
| [vibekits-fleet-compatibility](vibekits-fleet-compatibility/SKILL.md) | 桌面升级兼容性门禁与既有身份、授权、工作区保护。 |
| [vibekits-cluster-room-deploy](vibekits-cluster-room-deploy/SKILL.md) | 部署和恢复 VibeKits 集群房间，并验证远程连接。 |
| [apk-touch-feedback](apk-touch-feedback/SKILL.md) | 实现和验证 Android APK 的触摸反馈及交互一致性。 |
| [hbbv-server-build-deploy](hbbv-server-build-deploy/SKILL.md) | 构建、部署并验证 HBBV 服务端。 |

## 快速选择

| 你要做的事 | 首选技能 |
|---|---|
| 管理多个开发任务、跟进证据和验收 | [evidence-driven-engineering-manager](evidence-driven-engineering-manager/SKILL.md) |
| 接手项目并传递目标、进度、证据与下一步 | [project-handoff](project-handoff/SKILL.md) |
| 对客户端和服务端进行授权动态追踪 | [client-server-dynamic-trace](client-server-dynamic-trace/SKILL.md) |
| 发布前测试、修复、回归并证明交付结果 | [app-release-stability-gate](app-release-stability-gate/SKILL.md) |
| 上传已有安装包到 KEMI 商场 | [kemi-market-publish](kemi-market-publish/SKILL.md) |
| 在应用里实现商场和自动更新 | [kemi-market-integration](kemi-market-integration/SKILL.md) |
| 发布 KEMI 传书客户端 | [kemi-send-release](kemi-send-release/SKILL.md) |
| 根据 VibeKits 设备 ID 远程调试 | [vibekits-remote-simulator](vibekits-remote-simulator/SKILL.md) |
| 检查磁盘、清理可重建的历史产物 | [kemi-storage-cleanup](kemi-storage-cleanup/SKILL.md) |
| 严格保护源码和资料地清理编译缓存 | [safe-build-cache-cleanup](safe-build-cache-cleanup/SKILL.md) |
| 开展 SWDOL 原版兼容研发与验收 | [swdol-server-compatibility](swdol-server-compatibility/SKILL.md) / [swdol-client-compatibility](swdol-client-compatibility/SKILL.md) |
| 制作产品宣传视频 | [product-launch-motion](product-launch-motion/SKILL.md) / [remotion-promo-video-factory](remotion-promo-video-factory/SKILL.md) |
| 开始浏览器游戏项目 | [game-studio](game-studio/SKILL.md) |

## 技能目录

### 工程管理、追踪与质量验收 · 4 个

| 技能 | 用途与边界 |
|---|---|
| [evidence-driven-engineering-manager](evidence-driven-engineering-manager/SKILL.md) | 管理多智能体开发：明确职责、检查进度证据、量化验收、控制重复失败和无人值守边界；不用于普通单人实现任务。 |
| [app-release-stability-gate](app-release-stability-gate/SKILL.md) | 从源码、需求与历史故障生成可执行测试，进行真机验证、修复和回归，以证据判定 PASS 或阻塞；发布阶段调用相应发布技能。 |
| [project-handoff](project-handoff/SKILL.md) | 整理项目目标、实际进度、环境、成熟操作路线、验收证据、风险与首个续做动作，形成可执行交接。 |
| [client-server-dynamic-trace](client-server-dynamic-trace/SKILL.md) | 对授权系统执行低侵入客户端/服务端动态追踪、事件关联和回放验证，用于重建协议及状态机行为。 |

### 发布、上架与商场接入 · 9 个

| 技能 | 用途与边界 |
|---|---|
| [kemi-send-release](kemi-send-release/SKILL.md) | KEMI 传书完整发布：构建、签名/公证、打包、真实启动测试，发布到 Common 和 KEMI 商场；不处理远程办公资源。 |
| [kemi-send-common-release](kemi-send-common-release/SKILL.md) | 仅发布或更新 Common 中固定的四个传书客户端资源。 |
| [newlink-common-release](newlink-common-release/SKILL.md) | 发布 Common 中固定的六个 KEMI 客户端资源，支持单平台更新、清单最后写入及公开版本/MD5 校验；不负责 KEMI 商场。 |
| [kemi-market-publish](kemi-market-publish/SKILL.md) | 在 KEMI 商场发布签名包、更新元数据，验证 CDN 文件、商场展示与客户端升级。 |
| [kemi-market-integration](kemi-market-integration/SKILL.md) | 为 Android、Windows、macOS 应用实现商场浏览、按平台下载、安装和安全自更新；区别于上传发布。 |
| [kemi-apple-app-store-release](kemi-apple-app-store-release/SKILL.md) | KEMI macOS 应用的 Mac App Store 专用构建、签名、上传、提交、审核整改及状态验证；不负责 Developer ID 直装分发。 |
| [kemi-microsoft-store-release](kemi-microsoft-store-release/SKILL.md) | KEMI Windows 应用的 Microsoft Store 专用构建、签名、提交、整改与审核状态验证。 |
| [public-app-distribution](public-app-distribution/SKILL.md) | 公共应用商店、下载站及 GitHub Releases 等渠道的分发准备、提交和验证；适用时使用具体平台技能，不替代内部商场流程。 |
| [kemi-hbbc-release](kemi-hbbc-release/SKILL.md) | HBBC HTTP/HTTPS、账号、在线状态、用量和支付服务的构建、部署、验证与回滚；禁止借此替换或重启 RustDesk hbbs/hbbr。 |

### 远程设备、集群与硬件调试 · 9 个

| 技能 | 用途与边界 |
|---|---|
| [vibekits-remote-simulator](vibekits-remote-simulator/SKILL.md) | 通过 6–16 位设备 ID 与已授权接口进行远程诊断、传输、安装和测试，使用 VibeKits P2P/中继及设备工具。 |
| [vibekits-remote-node](vibekits-remote-node/SKILL.md) | 跨 Windows、macOS、Linux、Android 的节点发现、身份核验、LAN MCP 协作、远程构建及节点恢复；仓库保留的跨平台节点契约。 |
| [kemi-mac-remote-debug](kemi-mac-remote-debug/SKILL.md) | 通过 KEMI/RustDesk TCP 隧道承载 SSH，完成 Mac 日志采集、复现、候选部署及回滚；需要设备所有者授权。 |
| [kemi-windows-device-lab](kemi-windows-device-lab/SKILL.md) | 在可信 Windows 测试机 D 盘进行源码同步、原生 Release 编译、签名、安装、兼容性和性能测试。 |
| [kemi-windows-remote-signing](kemi-windows-remote-signing/SKILL.md) | 通过 VibeKits 远程执行 Authenticode 签名，处理硬件令牌窗口并验证签名结果；不记录 PIN 或私钥。 |
| [kemi-s1-hardware-debug](kemi-s1-hardware-debug/SKILL.md) | S1/huanglong 串口与 ADB 联合诊断，关联 HiV730 源码和 Git 历史，形成可追溯分析报告。 |
| [vibekits-cluster-agent](vibekits-cluster-agent/SKILL.md) | 在 VibeKits Harness 集群中竞标和执行已分配任务，并向对方仿真 ID 回报可验证结果。 |
| [vibekits-cluster-capabilities](vibekits-cluster-capabilities/SKILL.md) | 按固定 Schema 管理本机集群能力声明、同步状态和验证范围。 |
| [vm-smb-file-delivery](vm-smb-file-delivery/SKILL.md) | 通过 SMB 向授权 Windows 虚拟机安全交付文件、恢复映射盘并进行回读验证。 |

### 磁盘维护 · 2 个

| 技能 | 用途与边界 |
|---|---|
| [kemi-storage-cleanup](kemi-storage-cleanup/SKILL.md) | 检查和回收缓存、临时调试文件及过期可重建产物；保护源码、Git、文档、证书密钥、当前发布包、活动构建和聊天历史。不能用文件年龄单独判断是否可删。 |
| [safe-build-cache-cleanup](safe-build-cache-cleanup/SKILL.md) | 仅清理可重建的过期编译产物、编译器缓存、临时二进制和可重新下载缓存；禁止删除源码、文档、用户资料、Git 历史、发布归档和虚拟机磁盘。 |

### 视频与产品展示 · 5 个

| 技能 | 用途与边界 |
|---|---|
| [project-about-page](project-about-page/SKILL.md) | 根据真实产品能力设计关于页、介绍、宣传轮播、离线降级和安全缓存；不负责商店上架文案流程或应用自更新。 |
| [dual-screen-video-wallpaper](dual-screen-video-wallpaper/SKILL.md) | 制作高清、静音、全屏、无缝循环的双屏视频壁纸，覆盖 S1 双屏对齐、HEVC 编码、APK 集成和设备验证。 |
| [product-launch-motion](product-launch-motion/SKILL.md) | 产品发布片、宣传片和演示视频的创意、分镜、动态排版、配音同步与音画质量控制。 |
| [remotion-promo-video-factory](remotion-promo-video-factory/SKILL.md) | 用 Remotion 按产品类型蓝图实现宣传片，管理时间线、动效及逐帧视觉验收。 |
| [capcut](capcut/SKILL.md) | CapCut/剪映短视频剪辑计划、节奏、字幕、音乐授权和导出指导；智能体提供方案，人工在 CapCut 中执行和确认，所引用外部技能/服务需另行具备。 |

### 前端设计、浏览器游戏与 3D · 10 个

| 技能 | 用途与边界 |
|---|---|
| [game-studio](game-studio/SKILL.md) | 游戏早期技术选型与设计、实现、素材、试玩流程规划，再转交专门技能。 |
| [game-playtest](game-playtest/SKILL.md) | 浏览器游戏冒烟测试、自动化试玩、截图检查、HUD/覆盖层评审及问题记录。 |
| [frontend-app-builder](frontend-app-builder/SKILL.md) | 从视觉概念、实现到浏览器测试，构建或现代化前端应用、仪表盘、游戏和创意网站。 |
| [ideate](ideate/SKILL.md) | 根据产品设计简报生成图像化设计方向、替代方案和视觉探索。 |
| [three-webgl-game](three-webgl-game/SKILL.md) | 用 Three.js、TypeScript/Vite 实现游戏运行时，处理场景、GLB、物理和 WebGL 调试。 |
| [web-3d-asset-pipeline](web-3d-asset-pipeline/SKILL.md) | Blender 清理与导出、GLB/glTF 优化、碰撞体、LOD、压缩、纹理打包及运行时验证。 |
| [threejs-animation](threejs-animation/SKILL.md) | 关键帧、骨骼、形变、AnimationMixer 和 GSAP 动画控制。 |
| [threejs-geometry](threejs-geometry/SKILL.md) | 内置几何体、BufferGeometry、自定义顶点、法线、UV 和索引网格。 |
| [threejs-lighting](threejs-lighting/SKILL.md) | Three.js 灯光、阴影、HDR 环境和光照配置。 |
| [threejs-performance](threejs-performance/SKILL.md) | 实例化、绘制调用、LOD、裁剪、纹理和 GPU 性能诊断与优化。 |

### SWDOL 原版兼容研发 · 9 个

| 技能 | 用途与边界 |
|---|---|
| [swdol-acceptance-handoff](swdol-acceptance-handoff/SKILL.md) | 对 SWDOL 服务端、客户端和联调执行原版同条件验收、证据归档与交接。 |
| [swdol-client-compatibility](swdol-client-compatibility/SKILL.md) | 研发自研客户端的完整原版兼容状态机、输入、交互、渲染与防回归。 |
| [swdol-database-operations](swdol-database-operations/SKILL.md) | 对齐原版认证计费库、游戏库和我方 SQLite 持久化及状态差分。 |
| [swdol-document-governance](swdol-document-governance/SKILL.md) | 对研发文档分类、去重纠错、维护唯一主文档并检查可编码可追溯性。 |
| [swdol-gm-debugging](swdol-gm-debugging/SKILL.md) | 通过原版 GM 和后台观察建立可比实验环境并验证交互。 |
| [swdol-quest-task-delivery](swdol-quest-task-delivery/SKILL.md) | 依据真实 Flag、角色条件和怪物等级整理剧情任务并交付三 Tab 任务界面。 |
| [swdol-server-compatibility](swdol-server-compatibility/SKILL.md) | 组织服务端原版兼容研发、静态动态核查、持久化、差分和防回归。 |
| [swdol-static-dynamic-analysis](swdol-static-dynamic-analysis/SKILL.md) | 结合版本锁定静态分析和授权动态追踪，重建客户端/服务端真实行为。 |
| [swdol-xp-control](swdol-xp-control/SKILL.md) | 在 86Box XP 中操作授权原版客户端并进行登录、动作和有界证据采集。 |

## 安装

1. 下载本仓库 ZIP 并解压，或执行：

   ```sh
   git clone https://github.com/caucy2026/skills.git
   ```

2. 选择需要的技能，将其**整个文件夹**复制到 Codex 全局技能目录；不要只复制 `SKILL.md`。
3. 如已有同名技能，先备份并核对差异，避免覆盖个人配置。
4. 重新打开 Codex 或新建任务，再调用对应技能。

| 环境 | 默认安装路径 |
|---|---|
| macOS / Linux | `~/.codex/skills/<技能名>/SKILL.md` |
| Windows | `%USERPROFILE%\.codex\skills\<技能名>\SKILL.md` |
| 已设置 CODEX_HOME | `<CODEX_HOME>/skills/<技能名>/SKILL.md` |

正确示例：`~/.codex/skills/kemi-market-publish/SKILL.md`。不要多套一层仓库目录。

## 使用示例

在请求中写明技能名称、目标和验收要求：

```text
使用 $kemi-market-integration，为当前应用接入 KEMI 商场和安全自更新，完成测试与验收。
```

```text
使用 $app-release-stability-gate，检查当前候选版本，将历史故障纳入回归测试并给出发布结论。
```

```text
使用 $vibekits-remote-simulator，检查我提供的设备 ID，先只读诊断，再按授权执行修复。
```

```text
使用 $kemi-storage-cleanup，只读检查系统盘和外盘，列出可重建的历史缓存、大小、占用情况和清理风险。
```

## 依赖与安全边界

- 技能是操作规范和辅助资源，不是独立应用程序；安装不会自动配置工具链、开通远程访问或授予发布权限。
- 使用前完整阅读所选 `SKILL.md` 及其要求的引用文档。脚本、运行时、外部技能、浏览器、MCP/SSH/ADB、设备和账号按任务准备，不保证安装目录后即可在任意机器执行。
- 示例路径、账号标识、已登记节点和历史案例不能直接作为另一台机器的配置；需要现场核验目标、身份与权限。跨平台说明不代表所有平台均已完成真机验收。
- 不在仓库或日志中存放密码、令牌、私钥、证书私密材料、验证码或会话凭据。生产发布、设备控制和删除操作必须在对应授权范围内。
- 源码、Git、文档、签名材料、正式交付包和活动项目必须保护。仅当确认产物可再生、不被运行中任务使用且清理已获授权时，才按清理技能处理。
- 上传成功不等于发布完成，编译成功不等于功能验收通过；结果以对应技能要求的可核验证据为准。
