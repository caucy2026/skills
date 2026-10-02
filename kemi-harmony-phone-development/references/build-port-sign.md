# 移植、固定构建与签名

## 源码复用

保持RustDesk/KEMI协议和Flutter页面，单独增加OHOS平台适配。参考上游PR15682只用于审查，不整包合并：参考含被控、麦克风和后台权限，超出此手机控制端目标。`target_env="ohos"` 的主动控制约束要在Rust入口执行，不能只隐藏按钮。

OHOS沿用Android的远端分辨率保持策略：`get_custom_resolution` 返回None；默认本地适应窗口，不去改远端物理显示模式。确认Rust server/create_tcp_connection/start_all/start_server/Rendezvous路径的OHOS拒绝与提前返回，普通远控可发起、其他会话类型按产品范围拒绝。

复用PAD“连接/客户端/设置/关于”页面、底栏、多个设备图标；最初过度裁剪更多菜单已纠正。远端刷新、账号密码提示等不必申请手机录屏/无障碍。手机不能自当内部双屏PAD；跨屏、固定1920×1280和KBoard假设按平台分开。

## 构建前置

读取 `client/res/harmony-phone-env.sh`、`client/scripts/ohos-env.sh` 和需要执行的脚本。核验外盘挂载/可写/空间；记录Git HEAD、dirty paths、子模块、锁文件、实际源与物理工作区覆盖清单。

本轮ArkTS通过跨路径符号链接构建曾触发OhmUrl解析失败，改为外盘物理源码快照。不要再次改全局Flutter build-dir或给其他项目升级依赖。

```bash
export JAVA_HOME='<现有Java17路径>'
source '<鸿蒙client>/res/harmony-phone-env.sh'
```

上述脚本使用Bash。环境中固定Rust1.90.0、FRB1.80.1、Flutter-OH修订及任务专属缓存。默认Rust鸿蒙组件下载曾镜像404，使用已有独立官方工具链；不改主线默认Rust。桌面tray-icon依赖被排除出OHOS，修订沿Cargo.lock，不追上游默认分支升级。

## Rust与FRB

既有入口：`client/scripts/build-ohos-ffi.sh`。使用固定核心目录 `RUSTDESK_CORE_ROOT`；执行前确认不是其他同事主工作区。脚本会暂时写/还原core生成桥接和缺失inline stub，只能在本任务独立源码里执行。

- FRB1.80.1与Dart3.11有生成API差异，复用 `patch-ohos-frb-dart.py`；移除控制端不存在的CoreEvent被控桥接用 `strip-ohos-frb-core-event-impl.py`。
- SDK libclang在本机加载曾挂起；FRB改用已验证Xcode host LLVM/sysroot，OHOS最终编译仍用官方NDK，不能把Host编译结果当手机库。
- rustfmt缺失会在代码生成阶段停止，补齐固定工具链组件，不忽略生成失败。
- 脚本按libvpx、libaom、libyuv、Opus入口构建固定原生依赖；Opus存在不等于手机启用麦克风。
- cargo使用 `--target aarch64-unknown-linux-ohos --release --locked --lib`，桥接manifest `client/native/ohos_bridge/Cargo.toml`。
- 产物 `librustdesk_ohos_flutter_bridge.so` 复制到物理Flutter工程 `ohos/entry/libs/arm64-v8a/liblibrustdesk.so`，附正确libc++_shared.so。
- 用NDK llvm-nm核验实际Dart调用及FRB运行时导出，历史337接口通过；接口数量会随源码变，不能固定数量冒充正确。查ELF动态依赖与架构。

## HAP

```bash
cd '<任务cache>/build-workspace/flutter'
flutter build hap --release --no-pub > '<证据目录>/hap-build.log' 2>&1
```

unsigned输出固定为 `ohos/entry/build/default/outputs/default/entry-default-unsigned.hap`。Flutter工具在Hvigor成功后仍可能因无调试签名提示退出1；需区分明确编译成功+当前新unsigned包与真实编译错误。**不能仅凭旧包存在忽略退出码**。检查构建开始/结束、日志错误、产物时间、哈希；接着独立官方签名，不声称无签名包可安装。

UI-only修复可只同步已审查Dart/ArkTS文件，不必重编未变Rust；必须记录核心哈希及基线。不得盲目复制全部dirty remote_page.dart；本轮曾意外包含未上线额度探针并阻断正常中继。

## 签名与权限

受保护signing目录内保存既有PKCS12、应用证书和调试Profile；文件名可从项目实际配置读取。密码/私钥/UDID不进入Git、报告或控制台。复用既有签名身份；签名工具subprocess使用参数数组，不打印完整argv或机密异常。

本轮成功命令结构：

```text
java -jar <官方hap-sign-tool.jar> sign-app -mode localSign
 -keyAlias <既有alias> -keyPwd <受保护渠道> -keystorePwd <受保护渠道>
 -appCertFile <应用证书.cer> -profileFile <适用profile.p7b>
 -inFile <新unsigned.hap> -signAlg SHA256withECDSA
 -keystoreFile <既有.p12> -outFile <唯一signed.hap>
 -compatibleVersion 23 -signCode 1
java -jar <同一工具> verify-app -inFile <signed.hap>
 -outCertChain <私密工作目录>/chain.cer -outProfile <私密工作目录>/profile.p7b
```

这只是成功参数模板，不能把示例当真实秘密，也不能混用Android平台签名证书。验证输出码0、签名链、Profile范围/期限、包名、代码签名、文件SHA256；再跑 `client/res/verify-kemi-harmony-controller.py <signed.hap或.app>` 读取编译后的module.json。不是仅检查源码module.json5。

当前允许INTERNET，拒绝额外权限、扩展服务、backgroundModes；检查器7项负向测试复用 `test-harmony-controller-package.py`。权限包门禁不证明手机不可被控。

覆盖安装 `hdc -t <目标> install -r <signed.hap>`；启动aa EntryAbility，验证当前包真实页面和行为。不卸载、不改包名、不重置用户配置解决签名问题。
