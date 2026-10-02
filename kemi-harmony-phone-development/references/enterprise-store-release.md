# 企业认证、正式签名与华为应用市场

## 2026-10-02 隐私托管与 409 接续

详细候选及校验边界见 `kemi-docs/HARMONY-STORE-PRIVACY-409-20261002.md`。深圳企业资料已查到统一社会信用代码，备案主体保存后重开确认；AGC 校验仍不通过，不能将企业实名认证等同鸿蒙包备案。腾讯云原备案入口当前需要登录，不猜凭据或提交未授权身份材料。

用户明确确认隐私托管协议后，创建 KEMI远程办公鸿蒙隐私政策，协议 ID 2052076174464558016，AGC 列表状态完成；公开链接 `https://agreement-drcn.hispace.dbankcloud.cn/index.html?lang=zh&agreementId=2052076174464558016` 已读到真实深圳主体。正式草稿用隐私托管选择本协议；不能把托管 URL 填到自定义 URL 字段。若保存仍报旧 URL 错误，切回自定义清空隐藏 URL 再选托管，保存并重开核验。

官方 AppGalleryKit privacyManager 应在业务初始化前核对 getAppPrivacyMgmtInfo 与 getAppPrivacyResult，未同意才调用 requestAppPrivacyConsent；核对协议 ID、类型、版本及 FULL_MODE_AGREED，失败不得默认放行。类型 AppPrivacyLinkType 与 AppPrivacyType 需明确映射，直接比较会导致 ArkTS 编译失败。官方托管模式不能重复显示自建隐私确认弹窗。未上架 debug 模拟用官方 module.metadata 预置链接、真机及华为应用市场；正式包仍通过官方分发验证，不绕过 not trusted app source。

新的 publish 候选 1.4.127(409) 保留原 default remote/407；已编译、内外签名、官方双层验签、权限门禁 PASS，核心哈希保持 8a49d1f7...。正式 APP SHA256 1cee14e90d89c9954d405c54d6e58c5feca2fc632e2685588a917c01b95a24ad，HAP SHA256 561c9ac52ff77461e78f65cc07aadf158b0cf2509688cd4fd293a7dfcb90e8a9；路径为既有 publish 输出下 `desk-409-complete-signature`。409 于 2026-10-02 08:02:15 上传，合法性已达标，自检检测中；正式草稿已选入 409 并保存、重新载入确认。409 审核 DOCX 两页渲染检查后上传保存。未证明正式候选真机运行、提交审核或公开发布。

用户五分钟独占窗口内完成四页与客户端云端区原始截图，来源 remote/407，私密临时目录 `/private/tmp/kemi-store-screenshots-20261002`。不能改版本号伪装正式候选，也不公开历史设备/局域网信息。审核连接 DOCX 408 已上传保存重开确认；候选换为 409 后应补对应文件和验收。


现场记录截至2026-10-01。此文件只保存路径、用途和验证方法，不保存私钥、密码、设备UDID或登录Cookie。后续执行先核验现场状态，不把历史草稿当作发布成功。

## 认证与正确入口

开发者联盟overview→应用发布→AppGallery Connect→HarmonyOS。HarmonyOS与Android是不同发布入口，最终分发是华为应用市场；华为商城是商品商城。正式鸿蒙软件包类型为APP，不上传Android APK或改扩展名。

实际企业账号显示名“新智联软件有限公司”，主体“深圳新智联软件有限公司”，主账号已认证。旧个人体验账号的实名认证报错不适用于企业账号。认证状态通过当前账号页面和实际APP ID/发布证书创建结果核验；不自行填证件材料猜测账号。

## 包名和记录

原debug包com.newlinksz.kemi.remote提示已存在。用户明确授权新企业身份；harmony后缀被保留字符拒绝。office在第一步已保存为APP ID 6917617907411968133，用户随后指定desk，不再用于发布，也不擅自删除该记录。

最终com.newlinksz.kemi.desk，APP ID 6917617909010353055。应用名称KEMI远程办公，应用分类（非游戏），所属项目KEMI远程办公。创建流程第一步“下一步”已实际保存APP ID，第二步先关联项目，再最终确认开放能力页；不要误以为最终确认前什么都没创建。无本产品所需新开放能力，不申请定位、华为账号、ACL等。

APP与元服务→HarmonyOS→新建发布→选择desk包→手机→简体中文→确认。2026-10-01 22:36:52已建立未提交草稿；版本标识v2051798256643478528。建立APP ID和发布草稿不是上架成功。

## 本机签名材料位置（不可上传GitHub）

本机源码：`/Users/newlink/kemi/RustDesk/harmony-phone/client`。独立云仓库和分支沿environment.md，其他端及默认main不修改。

受保护签名根目录：`/Users/newlink/kemi/RustDesk/harmony-phone/client/flutter/ohos/signing`（Git忽略）。

| 材料 | 根目录下相对路径 | 用途 |
|---|---|---|
| 原调试私钥库 | kemi-harmony-controller-debug.p12 | 原remote调试版签名，不能替代企业发布身份 |
| 原调试CSR | kemi-harmony-controller-debug.csr | 调试证书公钥申请材料 |
| 原调试证书 | debug-certificate.cer | 调试应用证书链 |
| 原调试Profile | debug-profile.p7b | remote及指定调试设备白名单 |
| 密钥库密码文件 | store-password | 既有受保护口令来源，仅脚本读入，不输出、不提交Git |
| 设备UDID文件 | phone-udid | 原调试白名单注册，仅在授权华为流程使用，不打印 |
| desk专用发布私钥库 | release-desk/kemi-desk-release.p12 | EC/secp256r1，alias kemi-desk-release，PKCS12；只用于企业desk签名 |
| desk公开CSR | release-desk/kemi-desk-release.csr | 申请正式证书；发送到企业AGC，不含私钥 |
| desk企业发布证书链 | release-desk/release-certificate.cer | KEMI Desk Release 20261001，AGC显示生效，至2029-10-01 |

release-desk目录700，私钥/CSR/证书文件600；当前desk密钥库沿用受保护store-password作为口令来源，技能不记录口令值。原调试材料未改。下载证书原件`/Users/newlink/Downloads/KEMI Desk Release 20261001.cer`已复制到签名目录，实际签名使用受保护目录版本。证书文件SHA256：0b5814035e3868354275b1cc1fa1728ccfc2fce77719d99848fe8a61ec281b7f。

证书包含证书链，openssl x509默认只读第一张（根证书），不能把根证书期限/指纹当作应用叶证书。核验整链、叶公钥与CSR/私钥库匹配后再签名。

签名材料不进入源码Git bundle或云端提交。备份需新建私密目录，保持权限；不能覆盖旧密钥。记录实际备份路径和哈希，不把尚未做的备份写为已完成。恢复必须使用原desk密钥、证书/Profile和alias，不重新生成密钥掩盖丢失。

## 发布证书与Profile

证书→新增证书→KEMI Desk Release 20261001→发布证书→选择专用CSR。新增安全凭据的提交按电脑操作工具规则在动作时确认，2026-10-01用户已明确确认本次申请。已提交成功并下载。没有使用无关NLFramily证书/私钥。

Profile→添加→按APP ID选择KEMI远程办公（名称重复，必须核对6917617909010353055）→确认包名desk→KEMI Desk Harmony Release 20261001→发布（不是调试或指定设备发布）→选择KEMI Desk Release 20261001→不申请受限ACL→添加。Profile已添加成功，指纹自动关联到desk。下载文件为`/Users/newlink/Downloads/KEMI Desk Harmony Release 20261001Release.p7b`，已保存为签名目录`release-desk/release-profile.p7b`。文件SHA256为8cba42fd3288c42018ed0e7c91487ae4044669537d7de7d6a84535a60e8fb55d；CMS解析type=release，bundle-name=desk，app-identifier=6917617909010353055，APL=normal，permissions为空。下载事件曾20秒超时，但文件已实际下载；先核查文件，不重复创建Profile。

## 正式构建与验证

沿固定工具链和外盘physical build-workspace。SDK的ProjectBuildProfile.ProductBuildOpt实际支持bundleName/versionCode/versionName，publish产品可覆写为desk/408/1.4.127，default仍沿原AppScope的remote/407。验证编译后的module.json及APP pack.info，不能仅凭源码覆写生效。

正式产物须用Hvigor assembleApp等官方APP打包流程，不能把HAP改为APP。签名命令模板与秘密读取规则见build-port-sign.md；正式证书/Profile与debug分开。最低API23、arm64等兼容范围按编译包核验，不能保证任何历史鸿蒙手机安装。

正式包生成后记录源码提交/dirty、核心哈希、构建命令/日志、签名链、Profile类型/包名/APP ID/有效期、INTERNET唯一权限、无被控扩展及精确包SHA256。新desk首次安装与后续desk覆盖升级分别验收；不卸载remote调试版，不能用remote升级通过证明desk凭据延续。

## 上架资料与结果门禁

按当前AGC表单完成应用名称/图标、分类/标签、官网/客服信息、版本简介/截图、隐私和适用备案/资质。图标平台要求正方形直角PNG216或1024，由系统圆角遮罩；与包内一致，不因要求圆角去上传不一致图标。隐私/支持URL必须公开可读并与实际控制端账号行为一致。

上传后重新打开版本记录核验哈希/版本/状态；提交审核与公开发布分别记录。协议/法律声明若需要动作时确认，呈现真实条款；验证码/实名材料依平台边界处理。审核通过后还需公开入口、下载包及适用真机安装启动证据。后文已记录实际上传；当前仍未提交审核或公开发布，不将本文件视为完成证据。

## 2026-10-01正式候选实证

Hvigor命令`hvigorw --mode project -p product=publish -p buildMode=release assembleApp --no-daemon`在既有外盘ohos工作目录通过（48秒）。日志`/Volumes/ORICO/kemi-build-cache/rustdesk-harmony-phone/research/desk-publish-assemble-20261001.log`。APP路径`/Volumes/ORICO/kemi-build-cache/rustdesk-harmony-phone/build-workspace/flutter/ohos/build/outputs/publish/kemi-desk-1.4.127-408-signed.app`；SHA256 e4b3879cafe363d35ebc804ad83c00cebe8e291d21fb533898e3688fcf0db447。官方sign-app及verify-app均0，包内desk/408/1.4.127、phone、兼容API23目标24，仅INTERNET权限门禁PASS。

APP内精确HAP提取为同目录`kemi-desk-1.4.127-408-release.hap`，SHA256 25d3fef06194ff5cae3c5fd56c298fbfb220ab4e40535b762fa218025b6f2f61。叶证书公钥与CSR匹配，整链3张；叶证书SHA256指纹06:C4:B7:FD:ED:C3:DE:EA:37:6C:4F:BD:71:DD:4F:D3:7B:F5:94:E8:FC:25:7D:F3:67:D2:5A:98:1C:C1:CB:1B，有效至2029-10-01。

实际私密签名备份`/Users/newlink/kemi/RustDesk/harmony-phone-backups/20261001/desk-release-signing`（目录700，文件600），含desk私钥库、CSR、证书、Profile、验签导出以及store-password；不进入GitHub。手机HDC检查Empty，正式候选真机安装尚未验证，不能用旧debug验收替代。

## 必须纠正的正式签名陷阱

前述e4b3879c...APP只签了外层，内层HAP无签名；手机安装报9568320 no signature file。官方外层verify-app=0不证明APP内每个HAP已签名，不能上传该失败包。它保留作失败证据。

尝试让Hvigor signingConfigs直接读明文口令时，官方插件DecipherUtil.decryptPwd失败（exit255），需要DevEco加密口令配置；临时外盘配置已finally恢复，没有将密码放入跟踪源码。现场可复用的解决路线是固定SDK官方工具：

1. 对entry-publish-unsigned.hap使用原sign-app localSign参数、desk私钥/企业证书/release Profile，输出新目录entry-publish.hap。
2. 从Hvigor生成的unsigned APP取pack.info、pac.json。
3. `java -jar <SDK>/toolchains/lib/app_packing_tool.jar --mode app --hap-path <signed HAP> --pack-info-path <pack.info> --pac-json-path <pac.json> --out-path <unique unsigned APP> --force false`。
4. 官方sign-app签组装后的APP。分别verify-app核验内层HAP和外层APP，不依赖仅外层验签。

修正候选目录：`/Volumes/ORICO/kemi-build-cache/rustdesk-harmony-phone/build-workspace/flutter/ohos/build/outputs/publish/desk-complete-signature`。
- entry-publish.hap SHA256 7aa419b1aa1f2380cfb5fba6bce02b0f7aa7d9268cc098108fddffbeca7b7f3c。
- kemi-desk-1.4.127-408-release.app SHA256 ff627745621eecc34fbdd3e041691da88e90da6cce8f1aaaac9b9a0c00b7d948。
- 内层、外层官方验签均0，官方packing=0，精确APP权限门禁PASS。
- HDC重连原192.168.1.142:35653成功，型号HOP-AL00。修正HAP安装被9568322 not trusted app source拒绝，是真正正式分发信任限制。不能关闭系统验证/改release Profile冒充任意安装成功；沿AGC正式分发/云测试继续验证。旧remote仍保留。

## AGC表单与上传现场

版本资料已保存中国大陆发行（特定国家或地区→中国大陆；选好后境外授权框消失），产品简介和一句话介绍、AI不涉及。不能保留默认所有200国并未经动作时确认接受跨境个人信息授权。应用分类商务，办公软件标签；按当前表单复核保存与主标签。

表单必需负责人姓名/手机号（短信验证）/邮箱、工信部备案信息，缺失则请求持有人提供或指定已有材料路径，不猜证件号、不把企业认证当APP备案完成。另需隐私标签、年龄问卷及至少3张规范截图。远控依赖外部设备，建议按实际功能提交自测材料；不写未验证功能通过。

1254x1254图标上传被“图片尺寸不符合要求”拒绝，AGC接受216或1024正方形；保留原图案，只做规范尺寸交付并保持包内一致。文件chooser调用可能很慢，限定工具timeout并先查上传结果，不重复提交。

软件包管理→上传→测试和正式上架→上传APP。DOM的file input隐藏，可见上传区域为#fileDrop，先waitForEvent(filechooser)再点击该区域，setFiles精确双签名候选路径。2026-10-01已启动上传，需读取实际合法性和自检状态后再声明uploaded。后台提示10月1日19:00至10月3日12:00机房维护，上架自检可能排队；这不是已通过测试的证据。

最新上传结果：2026-10-01 23:11:20正式双签APP上传成功，后台desk/1.4.127(408)/phone/测试和正式上架，合法性已达标，自检检测中。图标相同原图案的1024尺寸导出已上传；正式公开发布和真机安装仍未完成。每次恢复必须复核后端状态。

## 备案与草稿版本绑定补充

用户提供现有KEMI远程办公APP备案截图，备案号粤ICP备19158712号-11A、域名newlinksz.cn，仅显示安卓平台；不据此宣称鸿蒙特征已备案。腾讯云官方FAQ明确同名同主体跨平台共用备案号，新增运行平台办理变更业务。沿原接入商备案记录补鸿蒙，不重复创建同名APP备案。正式叶证书MD5为0B:66:43:04:65:8D:6A:BA:BF:FF:39:A8:96:F4:BA:A3；公钥及依据见项目kemi-docs/HARMONY-DESK-FILING-PUBLIC-PARAMETERS-20261001.md。不可用根证书、debug或Android指纹。

AGC15项合法性检查全部通过；1.4.127(408)、37.97MB正式包已选取并保存到发布草稿。版本选取对话框刚打开可能暂显无版本，读当前同一对话框即可看到真实已上传行，不重复上传。选框实际为span.el-radio__inner。选择后新出现软件包加密，保留默认加密。上架自检仍检测中且官方维护公告仍在，不能称运行测试已通过。联系人姓名/手机已由持有人指定并保存，邮箱及手机验证仍缺；不将个人联系方式写入技能或Git。

## 内容分级与隐私标签实证

408发布草稿年龄问卷已提交并独立重开确认：中国区8+（本次仅中国大陆），不是儿童专用应用。会话聊天、账号个人信息、捐赠升级支付必须如实声明，不能全选否。问卷每个类别须先点左侧标题才展开；隐藏问题虽存在DOM，不使用force点击。表单先验证结果，再提交，回答是否仅面向儿童为否。

隐私标签已保存涉及个人信息收集，用途应用功能，包含实际账号/设备、订单/交易、远程会话及用量相关类别；重新进入草稿仍有17个数据项。华为通用类别示例不等于本产品采集所有示例。实际公开旧政策运营主体是香港新智聯科技有限公司，与当前深圳企业主体不同，且账号用量流程披露不足；未修改网站，也未把该地址填作本次完整政策。客户端也需最终一致的政策链接。核对清单见项目kemi-docs/HARMONY-PRIVACY-RELEASE-AUDIT-20261001.md。

## 官方邀请测试路线（2026-10-02）

为解决正式HAP的not trusted app source限制，进入应用测试→测试版本列表→创建测试版本→邀请测试（不选择公开测试）→描述鸿蒙desk正式408真机验收。配置中选择同一正式APP 1.4.127(408)，填写基础页面、按钮、断开、多设备切换与授权测试电脑范围，保存后离开再重开列表验证：408/邀请测试/准备提交，邀请量、下载次数、安装设备量均0。这仅是测试草稿，不是已邀请、已审核或已安装。

官方测试流程为配置测试版本信息→选择测试用户→发布测试版本，必填测试时间、测试说明、隐私声明以及负责人邮箱/手机验证。当前与正式上架共享的隐私及联系人资料缺口仍存在，不能使用草稿绕过正式分发信任检查或跳过验证。没有发送任何测试邀请，也未开放公开测试。后台正式APP上架自检仍检测中。

2026-10-02补充核验：正式草稿应用内资费选择其他，备注如实说明捐赠升级/服务器权限等级；保存后导航离开重开，其他仍选中且备注保持。正式包自检继续检测中。HDC list Empty后对既有192.168.1.142:35653 tconn恢复Connect OK，型号HOP-AL00，API26、OpenHarmony-7.0.0.105；只读device_probe布局存在ScreenLockRootComponent，故未采集应用截图、未绕过锁屏。私密探针文件/private/tmp/kemi-harmony-store-probe-20261002，仅本机保留，不进Git。

联系人补充：AGC个人信息页现有企业通知邮箱，应用审核结果通知已启用。正式408草稿已复用该既有渠道，保存后离开并重开核验一致，未另行猜邮箱或建立通知账号；具体地址仅保留平台，不写入技能。个人信息管理按钮跳转华为账号中心并要求重新登录，未填写凭据，返回AGC原会话仍有效。主办单位证件号、鸿蒙备案特征及正确隐私政策仍待核实，手机实时探针仍确认锁屏。

409 接续备份：独立鸿蒙分支 harmony-phone-pad-parity-20261001，提交 fa534515c102ee60413fcc5b3baf1e0d5fd51c9a 已推送现有私有 GitHub 仓库；main 和其他平台未修改。本地备份 harmony-phone-backups/20261002/privacy-409-fa534515c，Git bundle verify 通过，APP/HAP 备份哈希与上传候选一致。负责人资料已填入，短信已发送但尚未验证；验证码不得写入技能、Git或报告。
