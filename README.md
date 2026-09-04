# 可独立安装的全局技能

## project-about-page

跨项目“关于”页和产品说明设计技能。它要求先从源码、构建配置和测试证据建立真实产品档案，再完成与项目现有界面融合的身份区、产品介绍、能力清单、宣传图轮播、离线降级及安全资源缓存；同时提供完整的状态机、双指针原子缓存、安全边界和验收矩阵。

完整目录 `project-about-page/` 是独立安装单元。引用手册中的 KEMI OFFICE 名称、口号、格式数量、接口、路径和颜色仅为已标注实例，其他项目必须替换为自己的真实资料，不能直接复制宣传承诺。

## kemi-market-publish

KEMI 应用商城多客户端发布技能。支持按平台校验正式安装包、查询并更新既有应用、上传 CDN、补全商城元数据，并闭环检查公开详情、文件完整性、版本更新与实际安装。适用于 Windows、macOS、Android、Linux 和 iOS；它不负责 Newlink Common 固定资源发布。

完整目录 `kemi-market-publish/` 是一个独立安装单元，包含 `SKILL.md`、`agents/openai.yaml` 和发布契约。技能不包含账号、密码、Token 或具体项目的私密发布信息，认证资料必须在每次任务运行时安全提供。

## vibekits-remote-node

跨平台远程仿真、构建、LAN MCP 协作和设备诊断技能。包含 Windows、macOS、Linux、Android 的操作规则，以及 LMCP/2、SSH、RustDesk/ADB、长任务、权限和验收文档。58 Windows 节点是一个已登记实例，不是所有使用者的默认目标。

完整目录 `vibekits-remote-node/` 就是安装单元，包含 `SKILL.md`、`agents/openai.yaml` 和全部技能引用文档；不要只下载一个 SKILL.md。

## 安装

1. 在 GitHub 选择 Code → Download ZIP 并解压，或 `git clone https://github.com/caucy2026/skills.git`。
2. 将需要的整个技能文件夹（例如 `project-about-page`、`kemi-market-publish` 或 `vibekits-remote-node`）复制到当前账户的 Codex 技能目录。若设置了 `CODEX_HOME`，使用其 `skills` 子目录；否则使用下表默认路径。
3. 已存在同名目录时先备份并核对差异，不要直接覆盖个人配置。
4. 重新打开 Codex 或新建任务，让技能目录重新加载。输入对应技能名（例如 `$kemi-market-publish`）即可使用。

| 平台 | 默认目标目录 |
|---|---|
| Windows | `%USERPROFILE%\.codex\skills\<技能名>` |
| macOS / Linux | `~/.codex/skills/<技能名>` |

正确结果是 `<技能目录>/<技能名>/SKILL.md`，不要多套一层 `skills-main`。

示例请求：

```text
使用 $project-about-page，根据当前项目源码和已验收能力设计“关于”页、真实产品说明、宣传图缓存与离线降级，并给出完整验收结果。
```

```text
使用 $kemi-market-publish，将当前项目的 Windows、macOS 和 Android 正式安装包更新到 KEMI 应用商城，并完成逐平台闭环验收。
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
