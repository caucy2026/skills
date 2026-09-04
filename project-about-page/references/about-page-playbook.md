# “关于”页产品化设计、在线资源缓存与验收通用手册

## 1. 文档用途

本手册把 KEMI OFFICE Windows“关于”页从一次性界面整理成其他项目可复用的设计与工程方法。
可复用的是信息层级、缓存状态机、安全约束、交互规则和验收流程。KEMI自有APP均属于同一
产品系列，可以复用经过产品负责人确认的系列产品图片；不可直接复制的是其他APP的产品名称、
图标、口号、功能列表、支持格式、安装身份和版本文案。

系列图片复用必须记录资源集合、具体文件名、摘要和授权范围。图片可以表达KEMI系列硬件或
统一工作场景，但页面正文必须描述当前APP的真实能力。共享图片接口不可用时，已发布APP仍需
通过随包图片或完整缓存正常展示，不能让“关于”页依赖在线服务才能打开。

**最高原则：项目介绍必须由项目当前真实能力生成并经产品负责人确认。** 未开发、未验收或只在
计划中的能力，不得写入“关于”页；不能把 KEMI OFFICE 的 84 种格式、离线能力、Vibe Coding
定位或宣传接口原样套给其他项目。

## 2. 第一性原理

“关于”页同时承担四件事：

1. **身份确认**：用户能立即确认产品名、图标、版本和归属。
2. **价值说明**：两行以内说明产品为谁解决什么问题，不写空泛口号。
3. **能力核对**：列出用户当前安装版本真正支持的能力或格式。
4. **动态沟通**：在不拖慢启动、不依赖持续联网的前提下展示可更新的产品宣传内容。

因此它不能只是一个图片广告页，也不能直接依赖网络。网络失败、图片损坏或接口变更时，身份、
价值和能力信息仍必须完整可读。

这里的“动态沟通”仅指经过缓存和完整性校验的产品介绍、宣传图与能力说明，**不包含本 APP
版本检查、下载、安装或更新错误状态**。应用自更新属于应用级生命周期能力，必须与“关于”页
和“应用中心”解耦；具体规则见第 11 节。

## 3. 每个项目必须先填写的真实产品档案

实现 UI 前，项目必须在自己的设计文档或配置中填完下表，并附能力来源。空项不能用 KEMI 默认值
顶替。

| 字段 | 填写规则 | KEMI OFFICE 当前实例 |
|---|---|---|
| 产品正式名 | 与安装器、窗口标题、应用图标名称一致 | `KEMI OFFICE` |
| 产品图标/标识 | 使用项目正式资产，不用框架默认图标 | KEMI OFFICE 产品图标；页内简化为蓝底 `K` 标识 |
| 一句话定位 | 说明产品类型和主要用户 | 本地优先的多格式办公与文档工具 |
| 第一行价值 | 8–16 个汉字，说明差异化 | `KEMI 定制，极致精简` |
| 第二行价值 | 说明使用目标或受益者 | `为自己而设计，为更多人所用` |
| 离线降级标题 | 网络失败时仍成立的能力 | `轻量、专注，打开即用` |
| 离线降级说明 | 只能写已交付能力 | 支持多种办公与通用文档格式，本地优先，离线也能安心查看 |
| 应用版本来源 | 必须来自构建版本，不手写常量 | `KOFFICE_VERSION` / `release-version.properties` |
| 内容资源版本 | 必须来自已激活远端清单 | `data.version` |
| 支持能力来源 | 从路由、文件关联或统一能力清单生成 | Windows/PAD 内容格式统一清单，共 84 种 |
| 资源接口 | 每个项目独立配置，必须 HTTPS | KEMI `kemi_s1_xc` 资源接口 |
| 品牌主色 | 来自项目 Design Token | KEMI 蓝 `#1769e0` |
| 无网策略 | 明确本地文案和本地资产 | 显示产品特点，不显示白屏或永久加载 |

### 介绍文案的证据规则

- “离线”“隐私”“本地处理”只能在核心功能断网实测通过后使用。
- “支持 N 种格式”必须由代码中的去重扩展名数量自动计算，并与打开对话框、拖放路由和系统
  文件关联一致。
- “快速”“秒开”“流畅”“安全”等性能或质量词必须有对应验收报告，不能只凭主观描述。
- 版本号必须读取安装包真实版本；宣传资源版本与应用版本分开显示，不能混为一谈。
- 版权、许可、公司名称和联系信息按项目真实主体填写；没有的信息不要虚构。

## 4. KEMI OFFICE 当前页面信息架构

页面按从“身份”到“证据”的顺序排列：

```text
关于入口（独立图标）
└─ 关于页，最大内容宽度 1080px
   ├─ 品牌区：标识 + 产品名 + 两行价值说明
   ├─ 16:9 宣传图区：缓存图片 / 加载状态 / 离线产品介绍
   ├─ 数量一致的竖线指示器
   ├─ “为 Vibe Coding 而生 <资源版本>”
   └─ 支持格式区：9 个真实分类、84 种扩展名
```

现有 KEMI OFFICE 格式分类为 Word、Excel、PowerPoint、OpenDocument、PDF 与电子书、文本/配置/
开发、数据/网页/矢量图、兼容办公/图元、二进制/图片。其他项目必须按自己的能力重新分组，不得
为凑数量展示无法打开的格式。

## 5. 视觉与交互规范

### 5.1 页面融合

- “关于”是首页/Backstage 的一级入口，图标、行高、点击热区与“开始/新建/打开”等入口一致。
- 内容容器最大宽度 1080px，居中；左右内边距 24px，窄窗口自动变为一列。
- 品牌标识为 64×64px、16px 圆角；标题 26px，说明 16px。
- 宣传区固定 16:9、16px 圆角、浅边框和轻阴影；`object-fit: cover`，不拉伸图片。
- 支持格式使用小型标签，分类在宽屏为两列、760px 以下为一列。
- 颜色、字体、圆角和阴影必须来自当前项目的 Design Token，不硬拷 KEMI 蓝。

### 5.2 轮播

- 0 张：显示加载或离线本地介绍；绝不白屏。
- 1 张：显示图片，不启动无意义定时器。
- 多张：每 5 秒切换；点击图片进入下一张并循环。
- 指示器数量严格等于有效图片数；点击某个指示器直接跳转，当前项使用品牌主色。
- Enter/Space 与鼠标点击行为一致；图片包含可读 `alt`，轮播区有 `aria-label`。
- 用户手动切换后重置 5 秒计时，避免刚点完立即自动跳走。
- 离开“关于”页必须清理轮播和刷新定时器，防止隐藏页面继续耗电或更新已销毁 DOM。

### 5.3 状态呈现

| 状态 | 呈现 | 禁止行为 |
|---|---|---|
| 首次、联网同步中、无缓存 | 居中小型加载动画 + “正在准备产品内容…” | 白屏、全页遮罩、阻塞首页 |
| 有活动缓存 | 立即显示旧缓存，后台检查新版 | 等网络返回后才显示 |
| 同步成功且有变化 | 完整下载校验后无感切换整套资源 | 一张一张替换造成混版 |
| 同步失败但有缓存 | 继续显示活动缓存或备份缓存 | 删除旧缓存 |
| 同步失败且无缓存 | 显示项目真实离线介绍 | 无限转圈、暴露网络错误堆栈 |
| 单图加载失败 | 隐藏损坏图并保留其他图片 | 让损坏图占据空白轮播位 |

## 6. 启动与缓存架构

### 6.1 不阻塞启动

应用首个窗口创建后进入空闲阶段，再用低优先级后台线程检查资源。KEMI OFFICE 当前延迟 3 秒，
启动、打开文档和首屏渲染均不等待网络。

### 6.2 双指针缓存

```text
Marketing/<resource-name>/
├─ active.json              当前完整可用清单
├─ backup.json              上一套完整可用清单
├─ <version-manifest-hash>/ 当前文件目录
└─ .staging-<...>/          下载中临时目录，失败可整体删除
```

同步流程：

1. HTTPS 获取远端 JSON，验证状态、资源版本和文件数组。
2. 比较版本、数量、文件名、排序、大小和 MD5；任何一项变化都重建完整集合。
3. 文件下载到随机/内容寻址的 staging 目录，不写活动目录。
4. 每张图片验证 MIME、大小和 MD5；全部通过后写 `manifest.json`。
5. 通过同卷 rename 与 `WRITE_THROUGH` 原子发布目录。
6. 原 `active.json` 复制为 `backup.json`，再原子替换 active 指针。
7. 仅保留 active 与 backup 指向的目录，安全清理更旧缓存。

该设计能正确处理远端图片增加、删除、重排和同版本内容修订；不会把半套新图片与半套旧图片
混在一起。

### 6.3 浏览器隔离

Web UI 不接收 `%LOCALAPPDATA%` 真实路径。Windows 宿主把缓存根目录映射为隔离虚拟主机，例如：

```text
https://<project>-marketing.local/<cache-folder>/<content-addressed-name>
```

浏览器只接受该前缀，不能通过 URL 浏览本地其他目录。KEMI OFFICE 使用
`COREWEBVIEW2_HOST_RESOURCE_ACCESS_KIND_DENY_CORS`，页面每 5 秒读取轻量本地状态；后台完成发布
后再整体更新轮播。

## 7. 远端资源协议与安全约束

### 7.1 KEMI OFFICE 当前生产配置（2026-08-20 实际读取）

KEMI OFFICE 宣传资源生产接口为：

```text
https://kemi.newlinksz.com/kd-api/api/open/resources?user_id=8&name=kemi_s1_xc
```

参数含义：

| 参数 | 当前值 | 用途 |
|---|---|---|
| `user_id` | `8` | KEMI 当前资源所属用户/租户标识 |
| `name` | `kemi_s1_xc` | 当前宣传资源集合名，也是缓存隔离名 |

2026-08-20 实际请求返回 `status=200`、资源版本 `1.0.0`、3 张 PNG。文件名为
`kemi-s1-1.png`、`kemi-s1-2.png`、`kemi-s1-3.png`，排序为 0/1/2；每项均包含独立 CDN HTTPS
URL、字节大小和 MD5。CDN URL 是服务端动态数据，客户端只能从清单读取，不能把某次返回的 CDN
地址硬编码进源码。

KEMI Windows 当前配套配置为：

```text
资源端点：  上述完整 HTTPS URL
资源集合：  kemi_s1_xc
缓存根：    %LOCALAPPDATA%\KEMI\KOffice\Marketing\kemi_s1_xc
活动指针：  <缓存根>\active.json
备份指针：  <缓存根>\backup.json
虚拟主机：  https://kemi-marketing.local/
宿主调用：  GETMARKETINGRESOURCES
启动策略：  首个窗口创建后等待 3 秒，低优先级后台同步
前端刷新：  “关于”页打开期间每 5 秒读取一次宿主缓存状态
轮播周期：  5 秒
```

应用版本取编译宏 `KOFFICE_VERSION`；资源版本取接口 `data.version`。页面当前显示
`为 Vibe Coding 而生 <资源版本>`，不能把 `data.version` 错当成安装包版本。

### 7.2 服务端实际响应契约

建议响应至少包含：

```json
{
  "status": 200,
  "data": {
    "version": "1.0.0",
    "files": [
      {
        "name": "product-01.png",
        "url": "https://example.invalid/product-01.png",
        "mime": "image/png",
        "md5": "32位十六进制摘要",
        "size": 123456,
        "sort_order": 0
      }
    ]
  }
}
```

KEMI 当前宿主解析要求如下：

```typescript
interface MarketingServiceResponse {
  status: number; // 必须为 200
  data: {
    version: string; // 1..96 个安全 token 字符
    files: Array<{
      name: string;       // 显示名，不直接作为本地路径
      url: string;        // 必须 https://
      mime: 'image/png' | 'image/jpeg' | 'image/webp';
      md5: string;        // 当前接口为 32 位十六进制
      size: number;       // 1..20 MiB
      sort_order: number;
    }>;
  };
}
```

宿主提供给 Browser 的不是远端响应原文，而是经过缓存完整性检查后的最小结果：

```typescript
interface MarketingBrowserReply {
  appVersion: string;
  version: string;
  status: 'loading' | 'ready' | 'offline';
  files: Array<{
    name: string;
    url: string; // 只能是 https://kemi-marketing.local/...
    sort_order: number;
  }>;
}
```

`GETMARKETINGRESOURCES` 必须只读本地 active/backup 缓存，不在 Browser 请求线程直接访问公网。
`ready` 表示至少一套缓存完整；`loading` 表示无缓存且首次同步尚未明确失败；`offline` 表示无可用
缓存且后台同步失败。

### 7.3 其他项目拿文档后的最小改造清单

其他项目可以复用状态机和缓存算法；KEMI系列APP还可以按上述边界复用已确认的系列图片。
编码前必须一次性定义并替换：

```text
PRODUCT_NAME                 产品正式名
PRODUCT_MARK                 正式图标或页内标识
PRODUCT_VALUE_LINE_1/2       由真实能力得出的两行介绍
OFFLINE_TITLE/DESCRIPTION    断网时仍真实成立的介绍
BRAND_COLOR                  项目 Design Token
MARKETING_ENDPOINT           项目自己的 HTTPS 接口
MARKETING_RESOURCE_NAME      项目自己的资源集合名
MARKETING_CACHE_ROOT         项目自己的 LocalAppData 路径
MARKETING_VIRTUAL_HOST       项目自己的隔离虚拟主机
APP_VERSION_SOURCE           项目构建系统的真实版本源
CAPABILITY_MANIFEST          项目真实能力/格式单一来源
```

最小实现文件职责：

1. `AboutView`：只负责产品档案、加载/离线视图和能力清单渲染。
2. `AboutController`：负责 5 秒刷新、轮播、键盘、指示器和离页清理。
3. `about.css`：只使用项目 Design Token，提供 16:9、响应式布局和状态样式。
4. `MarketingCacheService`：负责 HTTPS、白名单解析、下载校验、active/backup 与原子发布。
5. `HostBridge`：只向前端返回虚拟主机 URL 和最小状态，不暴露本地路径、令牌或远端原文。
6. `CapabilityManifest`：生成/校验关于页、打开路由和系统关联，禁止三套手写列表漂移。
7. CI：用固定 JSON fixture 测 0/1/多图、增加/删除/重排、摘要错误、断网和 backup 回退；再用
   项目生产接口做非阻塞集成烟测。

如果项目没有在线宣传接口，应删除网络同步层，随安装包提供经过版本管理的本地图片和离线介绍；
不能为了复用 KEMI 页面而调用 KEMI 的 `user_id=8&name=kemi_s1_xc` 数据。

最低门禁：

- 接口和文件 URL 必须是 HTTPS；拒绝重定向到非 HTTPS。
- 图片数量 1–24；单文件 1 byte–20 MiB。
- 只接受项目明确支持的 PNG/JPEG/WebP；实际解码后还要校验内容类型。
- 摘要、大小、排序和名称必填；服务端升级后建议迁移到 SHA-256，MD5 只作为现有接口兼容校验。
- 远端文件名不能直接当本地路径；本地名使用索引+摘要+受控扩展名生成。
- 拒绝 `/`、`\\`、NUL、`.`、`..`、超长 token、重复文件名和超出数量/大小上限。
- JSON 解析、下载、写盘和清理均失败关闭；失败只影响新资源，不破坏活动缓存。
- 日志只记资源版本、数量和失败类别，不记录认证令牌或用户隐私。

## 8. 能力列表必须与产品路由同源

最容易出现的问题是“关于页写支持，但产品实际打不开”。推荐建立单一能力清单，生成或验证：

```text
统一扩展名清单
├─ 关于页分组和数量
├─ 打开文件对话框过滤器
├─ 拖放/命令行路由
├─ Windows OpenWithProgids / SupportedTypes / Capabilities
├─ Android Intent MIME/后缀声明
└─ 自动测试参数集
```

如果短期内无法代码生成，CI 至少逐扩展名比较这些消费者。KEMI OFFICE 已用
`scripts/verify-windows-source-parity.sh` 校验 Windows 关于页、原生路由与打开过滤器的 84 种内容
格式一致；`.apk` 是 Android 操作能力，不进入 Windows 内容格式清单。

## 9. 项目落地步骤

1. 填写“真实产品档案”，标注每条能力的代码/验收报告来源。
2. 建立统一能力清单，去重并计算展示数量。
3. 接入与现有首页一致的“关于”入口和图标，不新增风格冲突的导航。
4. 先完成静态品牌区、真实能力区和无网状态，再接在线轮播。
5. 原生层实现后台同步、双指针缓存、原子发布和虚拟主机映射。
6. UI 层实现轮播、键盘、指示器、状态机和离页清理。
7. 加入源代码门禁、接口 fixture、缓存损坏/断网测试和正式安装器验收。
8. 产品能力或格式变化时，先改统一清单和实际路由，再更新“关于”页；禁止只改宣传文字。

## 10. 验收矩阵

### 内容真实性

- [ ] 产品名、图标、版本与安装器/窗口标题一致。
- [ ] 两行介绍符合当前项目实际用途，未复制其他项目文案。
- [ ] 每条质量/性能描述都有测试证据。
- [ ] 支持数量与去重后的真实能力清单一致。
- [ ] 关于页、打开、拖放、系统关联对每个扩展名一致。

### 网络与缓存

- [ ] 首次有网：显示加载状态，完整下载校验后一次性出图。
- [ ] 首次断网：停止加载动画并显示本地产品介绍。
- [ ] 有缓存断网：立即显示旧缓存。
- [ ] 版本不变且清单不变：不重复下载。
- [ ] 同版本增加/删除/重排/改大小/改摘要：完整重建并准确呈现。
- [ ] 中途断网、磁盘满、摘要错误、图片损坏：active 不受影响，无半成品。
- [ ] active 损坏但 backup 完整：自动显示 backup。

### 视觉与交互

- [ ] 0/1/3/24 张图均无空白、重叠或多余定时器。
- [ ] 点击图片循环，点击指示器直达，Enter/Space 可操作。
- [ ] 指示器数量与图片数量一致，当前项使用品牌色。
- [ ] 100%/125%/150%/200% DPI 和小窗口/最大化均不截字、不横向溢出。
- [ ] 离开页面后不再刷新已销毁 UI，反复进入无定时器泄漏。
- [ ] 图片、版本、格式区与项目现有字体、间距、圆角统一。

### 性能

- [ ] 后台同步不增加首页和文档首屏关键路径耗时。
- [ ] 有缓存进入“关于”页 100ms 级呈现本地内容，不等待网络。
- [ ] 轮播只切换 opacity/合成层，不触发整页布局抖动。
- [ ] 缓存清理不在 UI 线程执行，磁盘占用受 active+backup 上限约束。

## 11. 关于页、应用中心与本 APP 自更新的强制隔离

| 入口 | 负责内容 | 严禁内容 |
|---|---|---|
| 关于页 | 产品身份、真实能力、版本展示、版权、许可、宣传资源 | 检查更新按钮、下载进度、更新失败、异常堆栈、SQL/接口原文 |
| 应用中心 | 浏览和安装当前平台的**其他应用**，分类、搜索、详情和安全下载 | 本 APP 自更新卡片、本 APP 检查更新按钮、把更新失败混入商城列表 |
| 全局自更新服务 | 后台检查本 APP 新版本；确认有更高版本时显示全局提示 | 在无更新、网络失败、服务端失败时占用页面或持续弹窗 |

Windows、macOS 必须共用同一职责模型。不能为了平台开发方便，在 Windows 把更新放进关于页、
在 macOS 又放进应用中心；也不能让不同平台出现两套错误文案和交互。

当前版本、无更新和任何检查失败均不能在关于页或应用中心创建更新卡片。只有响应通过完整合同
校验且远端整数版本更高时，才能显示一次应用根级全局提示。面向用户和产品页面不得出现
`FormatException`、HTTP/JSON 原文、SQL、数据库字段、Token、路径或堆栈。

应用市场接口、HTTP 与业务状态双层校验、下载完整性、Windows Authenticode、macOS Developer ID
与 Apple 公证、生产故障诊断和发布正反向验收统一以 VibeKits 仓库的
[`docs/59_KEMI_APP_MARKET_CROSS_PLATFORM_INTEGRATION_STANDARD.md`](https://github.com/caucy2026/vibekits/blob/main/docs/59_KEMI_APP_MARKET_CROSS_PLATFORM_INTEGRATION_STANDARD.md)
为单一执行规范。本手册只定义关于页设计和宣传资源缓存，不复制市场协议，避免两份文档随服务
演进产生冲突。

## 12. KEMI OFFICE 当前源码索引

| 内容 | 源码位置 |
|---|---|
| 关于页 JSX、真实格式分组、加载/离线内容 | `upstream/browser/src/control/backstage/AboutView.tsx` |
| 入口、轮播、点击/键盘、5 秒刷新与定时器回收 | `upstream/browser/src/control/Control.BackstageView.ts` |
| 页面布局、16:9 图片、竖线指示器、响应式格式区 | `upstream/browser/css/backstage.css` |
| 关于图标嵌入 | `upstream/browser/Makefile.am`、`upstream/browser/images/lc_about.svg` |
| 原生 HTTPS、清单验证、双指针缓存、虚拟主机 | `upstream/windows/coda/CODA/CODA.cpp` |
| 可重放 Windows 关于页增量 | `patches/0177-windows-about-carousel-and-format-parity.patch` |
| Windows 总体构建与正式验收证据 | `docs/engineering/WINDOWS_X64_SINGLE_SCREEN_BUILD.md` |
| 格式一致性门禁 | `scripts/verify-windows-source-parity.sh` |

## 13. 其他项目复制前检查

复制组件前必须删除或替换下列 KEMI 专属值：

- `KEMI OFFICE`、`K` 标识、`#1769e0`；
- `KEMI 定制，极致精简`、`为自己而设计，为更多人所用`；
- `为 Vibe Coding 而生`；
- `kemi_s1_xc`、KEMI 接口和 `kemi-marketing.local`；
- `%LOCALAPPDATA%\KEMI\KOffice`；
- 84 种格式、九个分组及其支持承诺。

替换后重新执行完整验收矩阵。只换 Logo、不核对产品能力和缓存安全，不算完成“关于”页移植。
