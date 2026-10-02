> 2026-09-30 核对的操作参考。原始来源：`/Users/newlink/kemi/RustDesk/client/kemi-docs/REMOTE-OFFICE-RELEASE-RUNBOOK.md`。历史版本、设备 ID 和结果只用于复现依据；执行以当前源码脚本、设备目录及本手册的冲突处理说明为准。本文不含签名私钥或口令。

# KEMI 远程办公：从源码到签名、验收和发布

本文件汇总四端的既定构建、签名和发布入口；每一端仍按自己的真机证据独立判定 PASS/BLOCK。Windows 真机构建和签名按 `kemi-windows-two-node-release`（单节点时按 `kemi-windows-device-lab` / `kemi-windows-remote-signing`）技能；Linux 按 `.github/workflows/kemi-distribution.yml` 和 `ci-build.md` 中的实际平台流程。商场和 Common 分别遵循 `kemi-market-publish`、`newlink-common-release` 技能。

**最高发布门槛：覆盖更新必须继承旧版已取得的全部授权。** 用最终签名包原位覆盖旧版后，在真机验证录屏、辅助功能、平台/系统权限和依赖这些权限的实际操作；主界面显示“已授权”不能代替连接管理器或其他辅助进程的功能验证。任何权限重新申请、辅助进程失去授权、卸载重装或重置权限后才可用，都判为 `BLOCK`，不得上传。

## 0. 冻结本次版本和源码

在 `client` 目录记录 `git rev-parse HEAD`、`git status --short`、`git submodule status`、`flutter/pubspec.yaml` 版本，以及所有会进入包的未提交文件。同步既定主分支后再冻结；有未提交业务改动时先审阅并纳入可追溯源码，不能把 `KEMI_ALLOW_DIRTY=1` 的测试候选当成正式发布。Android 和 Mac 均须从**同一冻结源码**构建；构建后记录绝对路径、字节数、SHA-256、版本码和签名身份。不要从文件名或 Git HEAD 缩写推断脏工作区 APK 的完整来源。

先确认 `flutter` 用户级设置没有把 `build-dir` 指向其他项目。2026-09-24 曾发现 `~/.config/flutter/settings` 指向 VibeKits，导致 Xcode 实际输出不在远程办公的 `flutter/build`；脚本随后可能签名旧 UI。Mac 构建脚本现以进程级 `XDG_CONFIG_HOME` 固定 `build-dir=build`，不修改用户全局设置；检查正在运行的 `xcodebuild` 的 `-derivedDataPath`，只接受本项目 `flutter/build/macos` 或由本项目脚本创建的专属构建符号链接。若路径不符，停止并隔离候选，不得用修改 `Info.plist` 版本号补救。

## 1. PAD：项目固定工具链和系统签名

按 `android-clean-clone-reproducible-build.md` 准备固定 Flutter 3.24.5、Rust 1.97.1、NDK 28.2.13676358、依赖及受控黄龙平台证书；私钥和密码只从受控环境注入。正式入口是 `res/build-kemi-android-release.sh`，干净克隆入口 `res/build-kemi-from-source.sh android` 会调用它。不要直接用 `flutter build apk`、debug 证书或旧 APK 改版本号。脚本必须核对包名 `com.newlinksz.kemi.remote`、arm64 ABI、versionCode、Release 非 debuggable、zipalign、v1/v2 签名和固定证书指纹。

把脚本生成的**同一 APK**覆盖安装到授权 PAD，回读 `/data/app/.../base.apk` 的 SHA-256，与本地候选逐字节一致后才开始真机验收。覆盖升级要保持系统权限；连接、单屏/双屏/扩展、首帧、收回、前后台恢复、键盘、文件传输、CPU/内存、崩溃/ANR 等按 `keyboard-quality/TEST-PLAN.md` 和 `app-release-stability-gate` 执行。每个新增和历史缺陷的要求轮数、失败判据不能因为赶发布时间而自行降低。失败则修复、重新构建并对新哈希重测。

每次 PAD 交付还必须执行 [PAD 六机 1080p 优先及完整画面适配门禁](ANDROID-PAD-RELEASE-DETAILED-REGRESSION-20260912.md#18-2026-09-29-六机-1080p-点对点显示门禁)：先请求远端精确 1920×1080；实际收到该尺寸则主副屏点对点显示。远端不支持时，PAD 在 1920×1080 视频容器内等比显示完整实际画面，四边可见、无裁切或滚动，输入坐标仍准确。逐台保存模式清单、请求/切换日志、硬解码帧、PAD 画面边界及键盘、性能证据；缺少任一台证据即记为未通过，后续版本不能跳过。

### 本机已有工作区参数（2026-09-27 +374再次核验）

本机用户明确允许沿用内盘工作区构建，依赖继续引用已经存在的缓存，不迁移、不重新下载。此记录仅适用于当前Mac，其他机器按其本机约束。

- `JAVA_HOME=/Users/newlink/jdk/jdk-17.0.19+10/Contents/Home`，将其bin和既有cargo bin加入本进程PATH。
- `ANDROID_SDK_ROOT=/Users/newlink/android-sdk`。
- `KEMI_VCPKG_ROOT=/Volumes/ORICO/kemi-build-cache/rustdesk-pad-edge-287/vcpkg`。
- `KEMI_VCPKG_INSTALLED_ROOT=/Volumes/ORICO/kemi-build-cache/rustdesk-pad-edge-287/vcpkg-installed-arm64-v8a`。
- 锁文件与已有pub缓存来自 `PUB_HOSTED_URL=https://pub.flutter-io.cn`；`FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn`，完整缓存可用时 `KEMI_PUB_OFFLINE=1`。
- 签名环境仍从既定受控凭据文件注入，不打印、不写日志；测试脏工作区才使用`KEMI_ALLOW_DIRTY=1`，不能因此称为正式冻结版本。
- 本机 PAD 远程办公平台签名身份使用受控 `priv/xtqx.md` 的 **9.1 节**密钥路径/别名/口令，先以 `keytool` 验证证书 SHA-256 与本节固定指纹一致。9.2 节是 KEMI 传书记录，不能从其中的路径直接给远程办公签名。2026-09-27 +375 首轮误取 9.2 路径，在 Gradle `packageRelease` 报密码/keystore 不匹配；改用 9.1 且预检证书后才继续原脚本。

仍只调用`res/build-kemi-android-release.sh`。缺少这些环境会误选不含Android库的默认vcpkg或错误pub缓存域名；应对齐本记录，不新增编译路线、不升级工具链。374构建及实装哈希在`evidence/pad374-peer-info-race/build-info.txt`。

## 2. macOS：Developer ID 候选

按 `macos-developer-id-release.md` 使用项目内 Flutter 3.27.4、独立 `pubspec.macos.lock`、固定 Rust/vcpkg/CocoaPods 和原 Developer ID 身份。单架构候选入口 `res/build-kemi-developer-id-macos.sh`；正式双架构候选入口 `res/build-kemi-macos-universal.sh`（干净克隆为 `res/build-kemi-from-source.sh macos`）。不要把单架构测试 ZIP、旧 App 或直接 `flutter build macos` 当成正式包。

在候选签名前逐项确认：

1. 本轮 `xcodebuild -derivedDataPath` 属于远程办公，不属于 VibeKits/其他项目；本轮 `App.framework/Versions/A/App` 实际生成且归入候选。核对源 App 与候选的 Flutter AOT SHA-256。仅改 `CFBundleVersion` 不算重编 UI。
2. 本轮 Rust Release `liblibrustdesk.dylib` 与候选 `Contents/Frameworks` 文件 `cmp` 一致；`service`、display helper 和登录项辅助 App 来自同一轮构建。脚本对此有硬门禁。
3. `Info.plist` 的 Bundle ID、`1.4.127 (<本轮构建号>)`、固定顶层名 `KEMI远程办公.app` 正确；Universal 包内每个承诺的 Mach-O 同时含 arm64/x86_64。
4. Developer ID、Team ID、Hardened Runtime、entitlements、`codesign --verify --deep --strict` 和 `spctl` 通过；对比现装正式版的 designated requirement 与 TCC 授权，覆盖升级后不能再次索取录屏/辅助功能权限。

Xcode 在 `clang -v -E -dM` 探测阶段若两个 `clang` 与 `SWBBuildService` 长时间 0% CPU 且堆栈停在管道 `write()`，这是**构建未完成**，不是可忽略的警告；不得签名旧 `flutter/build`。2026-09-24 在 Flutter 构建、直接 `xcodebuild`、独立 Pods 工程以及 arm64/Rosetta 均复现；移走本项目 `XCBuildData`、换 PTY 都未解除。相同的 `clang` 命令独立运行正常，采样显示它在 Xcode 服务持有的输出管道上阻塞。因此可确认当时卡在 Xcode 构建服务的工具探测输出处理，而非 Rust/Flutter 应用源码编译错误；无法从此证据归责到某人或某次源码改动。先结束确切卡住的构建进程并保留日志，再检查构建服务和本机状态。尚未证明可靠的恢复参数，不能把临时试探写成成熟路线，也不能因脚本退出就改用旧包发布。

## 3. 公证、最终 ZIP 与真机门禁

只有双架构候选和真机验收通过后，按 `macos-developer-id-release.md` 使用本机 `KEMI_NOTARY` 钥匙串 profile 提交 Apple 公证。要求返回 `Accepted`，对 App `stapler staple` / `validate`，再重打最终 ZIP；`stapler` 不能直接装订 ZIP。对**最终 ZIP**检查唯一顶层 `.app`、无 AppleDouble、双架构、签名、Gatekeeper，并模拟下载解压、覆盖到 `/Applications/KEMI远程办公.app` 后实际启动，核对既有录屏和辅助功能授权保留。公证前候选和已安装旧版均不能冒充最终发布包。

## 4. 发布顺序和回读

使用 `app-release-stability-gate` 冻结候选和给出 PASS；需要发布的平台逐个执行其门禁。PAD 单平台热修可以只更新 PAD，Mac 留在现有正式版，但不得说“四端已发布”。Common 用 `scripts/publish_common.py`：先平台二进制、再完整四端 `SHA256SUMS.txt`、最后 `release-manifest.json`；KEMI 商场更新现有远程办公记录，不新建重复 App。上传前后核对同一最终文件的字节数、SHA-256、签名/公证、公开版本码、更新检查和 CDN 回下载；发布失败不得把旧包改名为新版本，也不得提前更新 manifest。

发布记录须分别写明 PAD/Mac 的源码身份、候选哈希、实机用例结果、签名与公证、Common/商场记录和回下载哈希，以及仍未覆盖的测试。任何一项未通过，只能报告该平台 `BLOCK`，继续修复，不得写“正式发布完成”。

## 5. Windows x64：编译机 A、签名机 B

复用 `kemi-windows-two-node-release/references/rustdesk-2026-09-24.md` 的完整记录。先核对两台仿真机当前 ID、主机身份、源码哈希、版本及目录；历史路径只是这两台机器的已验路线，不能照搬到其他机器。已验拓扑为 A（xzl，`C:\kemi\build`）编译，B（58，`D:\KEMI-Test`）在已登录桌面会话使用硬件令牌签名。A 的 C: 路径是该机器的用户特许，其他机器仍执行其本机路径约束。A 中源码、输出和日志按版本各占独立目录，不把上轮 `target`、Flutter `Release` 或打包结果当作本轮产物。

在 A 用固定 Rust 1.75、Flutter 3.24.5、LLVM 15.0.6、项目 vcpkg 基线和 VS C++ 工具链：锁定依赖后编 `cargo build --locked --features hwcodec,vram,flutter --lib --release`，再编完整 Flutter Windows Release；核对新生成的 `librustdesk.dll`、`rustdesk.exe`、`flutter_windows.dll`、`data/app.so` 和插件同源。执行 `vcvars64.bat` 后重新设置带引号的 `VCPKG_ROOT`。遇到缺失的 `generated_bridge.freezed.dart`，先比对 bridge 源码和生成器版本，再复用已核验生成物或按固定生成器重建；不能拿旧目录凑包。WDAC/CodeIntegrity 4551 要保留精确事件与失败日志，只在同一文件恢复正常执行后做一次有界原命令重试，不改系统保护策略。

把 A 的完整内层目录通过既定反向隧道挂载到 B，挂载前后比对同一文件 SHA-256；在 B 的交互会话中用既定 `Invoke-KemiAuthenticode.ps1` 工作流签所有内层 PE。PIN 只由人在 B 输入。回读 B 的 PASS 报告、签名证书、时间戳及 A 实体文件哈希。随后在 A 按 `libs/portable/generate.py` 打包**已经签名的完整内层树**，再在 B 对单文件外层 EXE 单独签名、核对 A/B 最终字节一致。内层和外层任一报告缺失都不能发布；不能把上轮的签名报告套用到新 EXE。用最终签名 EXE 在两台 Windows 上真实解包、启动、连接、扩展、收回及输入，保留并恢复原安装。正式上传固定名 `KEMI-Windows.exe`，由最终哈希绑定商场/Common 记录。

## 6. Linux x86_64：固定工作流与 AppImage

Linux 复用仓库 `.github/workflows/kemi-distribution.yml` / `ci-build.md` 的固定 Flutter、Rust、vcpkg 和 AppImage 生成链路，从同一冻结源码与版本构建；只接收本次 run 的 Linux x86_64 产物，不能复用历史 DEB 或 AppImage 冒充当前代码。核对完整 Flutter bundle、ELF x86-64、AppImage v2 魔数、可执行位、版本、大小和 SHA-256；AppImage 构建 job 成功但没有实际上传产物不算通过。历史上遇到过配方硬编码旧版本、同名 `mv` 失败、root 拥有产物导致 `chmod` 失败和只生成 `AppDir.squashfs`，应按该工作流现有门禁核验实际文件，不临时另造打包路线。Linux 目前没有等同 macOS 公证或 Windows Authenticode 的签名步骤；不得把哈希清单说成代码签名。最终固定名 `KEMI-Linux.AppImage`，在目标 Linux 上实测启动、连接、扩展能力与输入后才标记 PASS。

## 7. 四端统一交接，避免重复构建和误签

每批建立一张记录：冻结源码 commit + 子模块哈希 + 所有参与构建的未提交文件、四端实际版本号、各自构建机与输出绝对路径、最终文件大小/SHA-256、签名身份与验签报告、安装路径、实测版本和回下载哈希。测试用包和正式包分开标记；源码或二进制有任何变化，就失效该端旧哈希及对应的验收/签名证据。一个平台失败只重建该平台及受共同源码改动影响的平台，保留其他平台仍有效的结果。上传使用 `BIN/release/` 固定四文件名及清单；先核对每个已验收文件，再传平台文件和 `SHA256SUMS.txt`，最后更新 manifest 和商场记录。发布后用公开链接回下载逐字节比对并实装；未达到此步只写候选或 BLOCK。

## Windows 间歇失败的强制分流

先读 [2026-09-27 根因记录](WINDOWS-BUILD-FAILURE-ROOT-CAUSE-20260927.md)。编译期生成工具被CodeIntegrity拦截、源码同步缺office_identity、运行期未签名插件被拦截是三类不同故障。不能都称为“编译环境坏了”，不能靠反复编译代替定位。当前xzl已实证要求完整内层PE签名后才能可靠开展新包运行验收；遵循既有58跨机器签名流程。每次构建仍需核验同时间事件和精确文件，不能把旧结论不加核对套到新失败。

签名前必须比较完整资源清单，不仅核对Rust/Flutter构建成功。2026-09-27 +369直接Flutter Release只有14个PE；与+353完整目录比较，缺少dylib_virtual_display.dll和usbmmidd_v2驱动目录（包含INF、CAT及x64 DLL）。应按固定源码编译虚拟屏桥接DLL、按固定依赖来源补齐驱动资源并验证原驱动签名/版本；不得直接把旧版自研DLL当新编译产物。缺项未补齐前不启动令牌签名。不同历史包PE数量可能不同，必须解释实际差异，不能机械凑18个。
