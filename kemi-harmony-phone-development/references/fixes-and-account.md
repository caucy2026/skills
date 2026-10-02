# 已证实故障与账号适配

## 显示、密码与手机UI

| 故障 | 已验证根因与修复 |
|---|---|
| 蓝色变橙黄色 | Rust输出RGBA，Flutter因未包括isOhos选择了BGRA；将OHOS纳入RGBA分支。用实际蓝图标和红黄绿按钮核对；标准色卡误差测试仍是单独门禁 |
| 勾选记住密码仍反复提示 | PeerConfig读取的config_id未初始化，而写入按设备id；统一读取与保存键，沿原目录迁移/兼容，不清配置 |
| OHOS键盘插件缺失 | flutter_keyboard_visibility与enable_soft_keyboard未注册；OHOS使用viewInsets/didChangeMetrics，dispose取消可选订阅，避开不支持平台方法 |
| 产品图片缓存生成失败 | root.createTemp相对创建参数错误；改为'.staging-'，整组验证后原子切换，下载失败/路径穿越/坏图回退/空集合用4项测试验证 |
| 客户端每次缓冲很久 | 复用PAD布局，先显示缓存/上次快照；文件校验和下载到后台worker，仅一次对应变更。历史11–32ms首帧是特定候选10次测量，不推广为新包固定时延 |
| 默认显示非自适应 | 初始化和首帧将OHOS本地画布设为适应窗口，覆盖历史Original首选项；不改远端分辨率 |
| 删除/确认按钮被挤掉 | 浮动面板高度从58改103、宽46，删除VK_BACK单字符退格，确认VK_ENTER；不要把删除做清空全部 |
| 退出/断开无效 | 核验平台通道、会话同步关闭及正确对话框按钮。OHOS使用原生terminateSelf，断开先关闭会话再退出页面，防止异步dispose留下连接 |
| 误启用匿名额度 | 混入未上线四小时服务探针导致已连接即阻断；默认关闭旧探针。最新需求改为共享账号系统，使用共享usage lease与服务端规则 |

## 同一账号系统，不另建鸿蒙用户库

现有源码：`lib/mobile/pages/account_center_page.dart`、`models/kemi_account_model.dart`、`services/kemi_account/{auth_repository,account_models,account_storage,hbbc_account_api,hbbc_runtime_service}.dart`。

固定产品接口 `https://kemi-chat.newlinksz.com:21121`，app_id `kemi-remote`、channel_id `official`。公开app-config与integration.json提供当前接口状态/规则；不要固化历史游客/付费时长。普通华为手机kemi_owned_pad=false，真实brand/device/platform，不伪造Huanglong内部身份或MAC。

- 鸿蒙主页增加共享账号入口，初始化一次single-flight，生命周期控制presence前台状态。
- `HarmonyKemiAccountStorage`复用Dart存储合约，方法通道 `com.newlinksz.kemi/controller`；Android继续mChannel。
- 原生 `KemiAccountIdentity.ets`提供identity、SHA256withRSA签名和安全存储，串行操作。
- 方法：kemi_account_device_identity/device_sign/secure_read/secure_write/secure_write_tokens/secure_delete。参数沿用共享Dart协议，不输出密码或token。
- HUKS别名 `kemi.account.device-key.v1`：RSA2048、SIGN|VERIFY、SHA256、PKCS1v1_5；导出公钥X509 DER Base64，私钥不导出。
- installation_id保存在应用preferences，派生app-scoped SHA256 hardware_code；这是应用身份，不能声称卸载/清数据后仍是不可变物理身份。
- HUKS isKeyItemExist首次可能抛12000011（不存在），只捕获这一码后创建；其他错误不当作不存在，既有密钥不替换。
- ASSET SECRET单条最多1024字节：凭据/配置JSON分块保存，加密块全部成功后原子更新一个小清单；双token在同一完整版本更新。清单切换后清旧块；失败不能回退明文。
- 只接受access_token、refresh_token、account_cache、account_profile、donation_prompt_state五类secret名；system首次解锁后可用，不额外申请生物认证。
- package_info_plus无OHOS实现导致MissingPluginException并误显示“账号服务暂不可用”；使用既有原生getVersion接口。HUKS首次查找异常是第二个已修复原因，不能将该UI提示一概说成服务器故障。
- 捐赠服务曾直接new Android存储；所有token读取需正确选择OHOS通道。支付外链HTTPS/alipays交给系统，不伪造支付成功。
- 未登录中继被服务端拒绝后提示登录并返回账号页，是规则，不是连接挂死。不要为了让测试通过关闭lease或假装已登录。
- 更新保留session token、刷新凭据、设备绑定；需真实账号覆盖安装验证。60项unit/mock通过不等于真实短信/支付通过。

账号测试：`flutter test --no-pub test/kemi_account`。本轮60项；新增鸿蒙通道隔离、双token单次写入、失败和空签名拒绝。测试需要 `test/support/native_localization.dart` 设置限定本地化桥接，不用宽松全局native mock掩盖错误。

官方ASSET长度依据：https://github.com/openharmony/docs/blob/master/en/application-dev/security/AssetStoreKit/asset-js-add.md 。API具体名字优先读取固定SDK的ets/api/@ohos.security.{huks,asset,cryptoFramework}.d.ts，不凭记忆修改原生密码学参数。
