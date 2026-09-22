# 可独立安装的全局技能

## 2026-09-22 全局技能同步

本次同步 29 个自定义技能的完整目录（定义、引用文档、脚本及素材），不包含系统内置技能、缓存或凭据。仓库原有的 `evidence-driven-engineering-manager` 与 `vibekits-remote-node` 保留，因此仓库共 31 个技能。

| 类别 | 本次同步的技能 |
|---|---|
| 发布与上架 | `app-release-stability-gate`、`kemi-apple-app-store-release`、`kemi-hbbc-release`、`kemi-market-integration`、`kemi-market-publish`、`kemi-microsoft-store-release`、`kemi-send-common-release`、`kemi-send-release`、`newlink-common-release`、`public-app-distribution` |
| 设备调试与维护 | `kemi-mac-remote-debug`、`kemi-s1-hardware-debug`、`kemi-storage-cleanup`、`kemi-windows-device-lab`、`kemi-windows-remote-signing`、`vibekits-remote-simulator` |
| 视频与产品展示 | `capcut`、`dual-screen-video-wallpaper`、`product-launch-motion`、`project-about-page`、`remotion-promo-video-factory` |
| 游戏与 3D | `game-playtest`、`game-studio`、`three-webgl-game`、`threejs-animation`、`threejs-geometry`、`threejs-lighting`、`threejs-performance`、`web-3d-asset-pipeline` |

每个技能均直接位于仓库根目录。安装时复制完整目录，并按对应 `SKILL.md` 核对依赖、设备授权及环境配置；不要把某台机器的路径或已登记设备当作所有使用者的默认配置。

## app-release-stability-gate

跨平台应用自动稳定性与交付技能。它从源码、发布差异和历史缺陷生成可执行测试，验证测试自身能发现故障，在真实设备或机器上执行功能、升级兼容、资源和耐久门禁，并在授权范围内自动诊断、修复、重编译和回归。发布已获授权时，它会继续签名、上传、发布端回读、客户端升级及打开验证，最终对精确候选字节给出 `PASS` 或带证据的 `BLOCK`，并生成交付回执。

完整目录 `app-release-stability-gate/` 是独立安装单元。它适用于移动端、桌面端、Web/PWA、设备端及带服务端的应用；实际发布阶段会调用对应平台或项目发布技能。

## kemi-market-integration

KEMI 应用商城跨平台客户端接入技能。用于为 Android、Windows 和 macOS 实现当前平台商城浏览、详情、流式下载、安全校验、系统安装以及本 APP 自更新，并通过自动测试、生产只读联调和目标真机完成闭环验收。

完整目录 `kemi-market-integration/` 是独立安装单元。它不包含管理员凭据，也不把管理员发布能力编译进客户端；需要真正上传和更新商城记录时使用 `$kemi-market-publish`。

## project-about-page

跨项目“关于”页和产品说明设计技能。它要求先从源码、构建配置和测试证据建立真实产品档案，再完成与项目现有界面融合的身份区、产品介绍、能力清单、宣传图轮播、离线降级及安全资源缓存；同时提供完整的状态机、双指针原子缓存、安全边界和验收矩阵。

完整目录 `project-about-page/` 是独立安装单元。引用手册中的 KEMI OFFICE 名称、口号、格式数量、接口、路径和颜色仅为已标注实例，其他项目必须替换为自己的真实资料，不能直接复制宣传承诺。

## kemi-market-publish

KEMI 应用商城多客户端发布技能。支持按平台校验正式安装包、查询并更新既有应用、上传 CDN、补全商城元数据，并闭环检查公开详情、文件完整性、版本更新与实际安装。适用于 Windows、macOS、Android、Linux 和 iOS；它不负责 Newlink Common 固定资源发布。

完整目录 `kemi-market-publish/` 是一个独立安装单元，包含 `SKILL.md`、`agents/openai.yaml` 和发布契约。技能不包含账号、密码、Token 或具体项目的私密发布信息，认证资料必须在每次任务运行时安全提供。

## kemi-hbbc-release

KEMI hbbc 的构建、测试、Linux 交叉编译、`BIN/server` 对齐、生产部署、线上验收和回滚技能。它只维护 hbbc，并明确禁止替换或重启 RustDesk 的 hbbs/hbbr。

技能目录是 `kemi-hbbc-release/`，安装时必须复制整个目录。示例：

```text
使用 $kemi-hbbc-release 构建 hbbc Linux 正式包，对齐 BIN/server，并在确认后只部署 hbbc。
```

## vibekits-remote-node

跨平台远程仿真、构建、LAN MCP 协作和设备诊断技能。包含 Windows、macOS、Linux、Android 的操作规则，以及 LMCP/2、SSH、RustDesk/ADB、长任务、权限和验收文档。58 Windows 节点是一个已登记实例，不是所有使用者的默认目标。

完整目录 `vibekits-remote-node/` 就是安装单元，包含 `SKILL.md`、`agents/openai.yaml` 和全部技能引用文档；不要只下载一个 SKILL.md。

## 安装

1. 在 GitHub 选择 Code → Download ZIP 并解压，或 `git clone https://github.com/caucy2026/skills.git`。
2. 将需要的完整技能文件夹（例如 `kemi-market-integration`、`project-about-page`、`kemi-market-publish`、`kemi-hbbc-release` 或 `vibekits-remote-node`）复制到当前账户的 Codex 技能目录。若设置了 `CODEX_HOME`，使用其 `skills` 子目录；否则使用下表默认路径。
3. 已存在同名目录时先备份并核对差异，不要直接覆盖个人配置。
4. 重新打开 Codex 或新建任务，让技能目录重新加载。输入对应技能名（例如 `$kemi-market-publish`）即可使用。

| 平台 | 默认目标目录 |
|---|---|
| Windows | `%USERPROFILE%\.codex\skills\<技能名>` |
| macOS / Linux | `~/.codex/skills/<技能名>` |

正确结果是 `<技能目录>/<技能名>/SKILL.md`，不要多套一层 `skills-main`。

## kemi-s1-hardware-debug

面向 KEMI S1/huanglong 的即装即用硬件调试技能。新同事只需提供当前 ADB 地址；Harness 会核验 ADB 身份，按 CH340/CH341 USB 特征自动发现可能变化的串口名，使用已验证的 115200/8-N-1/无流控配置持续监控串口，通过 ADB 操作 Android，并按时间关联两路证据。发现软件问题后，技能会用 Git 将故障签名定位到最小 HiV730 源码范围，给出置信度、修复及复测方案，最终生成持久化 Markdown 分析报告。

复制整个 `kemi-s1-hardware-debug/` 到用户全局技能目录后，VibeKits Harness 会通过共享的 `.codex/skills` 自动发现它；新任务直接使用 `$kemi-s1-hardware-debug`，不需要另配 Harness 路径。技能不包含密码、令牌或固定 COM/IP。

示例请求：

```text
使用 $kemi-market-integration，将当前应用接入 KEMI 商城浏览、下载安装和安全自更新，并完成自动测试、生产只读联调与真机验收。
```

```text
使用 $project-about-page，根据当前项目源码和已验收能力设计“关于”页、真实产品说明、宣传图缓存与离线降级，并给出完整验收结果。
```

```text
使用 $kemi-market-publish，将当前项目的 Windows、macOS 和 Android 正式安装包更新到 KEMI 应用商城，并完成逐平台闭环验收。
```

```text
使用 $kemi-hbbc-release 构建 hbbc Linux 正式包，对齐 BIN/server，并在确认后只部署 hbbc。
```

```text
使用 $vibekits-remote-node，先识别目标平台并只读检查局域网 MCP 能力。
```

```text
使用 $vibekits-remote-node，检查指定 Windows 节点的 SSH 身份与 D 盘构建条件。
```

## 独立使用的边界

技能加载、规则与协议查阅不依赖原作者电脑，也不需要 Python 或额外包。实际远程操作仍需要对应的 MCP/SSH/ADB 等工具、可达设备及合法授权；技能不是应用程序或远程控制服务，安装不会自动开放端口或授予权限。真正编译 APP 时才需要该 APP 的源码和工具链。

Windows/macOS/Linux 可安装本技能；Android 在这里主要作为 ADB/MCP 被控目标，不代表 Android 上可直接运行 Codex。Linux 适配规则已提供，但尚未据此完成真实 Linux 节点验收。

不包含密码、私钥、令牌。包含团队登记的公开身份数据和指纹；换用其他设备时必须建立自己的身份配置并核验，不能复用 58 节点配置。历史 SSH smoke 脚本仅以文本保存供审阅，不是自动运行的安装步骤。

工程、缓存、编译产物继续遵守所在节点的数据盘约束；只有全局技能定义位于 Codex 配置目录。
