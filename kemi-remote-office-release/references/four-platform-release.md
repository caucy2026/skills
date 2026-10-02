# KEMI 远程办公四端编译、签名、公证和双渠道发布手册

核对日期：2026-09-30。四端为 Android PAD arm64-v8a、macOS Universal arm64/x86_64、Windows x64、Linux x86_64 AppImage。适用于 Common 与 KEMI 商场直接分发；Apple/Microsoft 应用商店属于其他技能和独立产品变体。本手册是执行说明，不是“四端本轮全部已验收”的声明。

## 1. 准备、源码与身份

1. 读当前全局/项目 AGENTS 和 LOCAL 环境约束。定位真正 Git 根目录：本机例子是 `/Users/newlink/kemi/RustDesk/client`，外层 RustDesk 目录不是客户端 Git 根。其他同事按实际克隆目录设置 `REPO`，不要照抄本机路径。
2. 核对 KEMI 源码远端、默认分支、完整提交与子模块，沿用项目规定 `main`；历史文档和 workflow 自动 push 触发器仍可能写 `master`，不能因此把旧分支当当前源码。保留未提交改动，解决冲突后非强推同步，确认远端回读。必要时从冻结 ref 手动触发现有 CI，不为发布文档顺便修改工作流。
3. 记录 `git rev-parse HEAD`、`git status --short`、`git submodule status --recursive`、`git diff --check`，以及版本、锁文件、桥接生成器、依赖基线和构建参数。审阅并提交所有入包改动；测试脏工作区要保存改动清单，不能称干净正式版。
4. 四端完整发布用同一冻结源码；平台热修逐端保留实际源码/版本，不把未更新平台标为新版本。`flutter/pubspec.yaml` 为 `version_name+build_number`，与 Cargo 产品版本一致；商场 `version_code` 为实际包内整数，须高于该平台线上值。不得凭发布批次名覆盖包内事实。
5. 检查构建机磁盘、当前任务与缓存。此发布 Mac 的可再生输出必须位于 `/Volumes/ORICO/kemi-build-cache/`，先核验挂载、可写、空间；分任务配置 TMPDIR、Cargo target、Gradle、Flutter build、Xcode DerivedData。其他机器执行自己的 LOCAL 规则。现有 Mac Universal 脚本明确要求 ORICO，此脚本在无该挂载的机器不能原样执行；使用已配置的发布 Mac，不能假建目录或偷偷改路径。
6. 保存上一正式包、旧公开元数据和旧清单的不可变副本，记录大小、SHA-256、签名及适用平台，作为恢复依据，不覆盖或删除。

| 平台 | 固定发布文件 | 身份及签名 |
|---|---|---|
| PAD | `KEMI-PAD.apk` | `com.newlinksz.kemi.remote`；Huanglong 平台证书 SHA-256 `c8a2e9bccf597c2fb6dc66bee293fc13f2fc47ec77bc6b2b0d52c11f51192ab8` |
| Mac | `KEMI-macOS.zip` | Bundle ID `com.newlinksz.kemi.remote`；Developer ID Team `26T5WV4GLP`；固定顶层 `KEMI远程办公.app` |
| Windows | `KEMI-Windows.exe` | 产品同源完整 x64 Release；指定 EV Authenticode 证书，内层与外层分别签名 |
| Linux | `KEMI-Linux.AppImage` | 产品 x86_64 AppImage v2；当前流程无单独代码签名/公证 |

证书轮换先核验原身份、有效期、授权连续性和迁移，不把历史指纹当永久有效。不得更换应用身份、删除钥匙串、清 TCC 或卸载重装来掩盖升级问题。

## 2. 凭据入口（只存入口，不存秘密）

- Android：授权的 keystore 与四个环境变量 `KEMI_ANDROID_KEYSTORE`、`KEMI_ANDROID_KEY_ALIAS`、`KEMI_ANDROID_STORE_PASSWORD`、`KEMI_ANDROID_KEY_PASSWORD`。既有发布机的受控私有配置 `priv/xtqx.md` 9.1 节记录远程办公平台签名；9.2 属于传书，不能混用。同事必须通过授权凭据渠道取得，不复制到 skill/Git/日志。先核对证书指纹，再让 Gradle 完成签名。
- Mac：登录钥匙串中带私钥的 `Developer ID Application: zhen ji (26T5WV4GLP)`，运行 `security find-identity -v -p codesigning` 核对。公证默认用钥匙串 profile `KEMI_NOTARY`；新机器由账号持有人用 Apple app-specific password 或 App Store Connect API key 安全建立 profile。可用 `xcrun notarytool store-credentials KEMI_NOTARY` 的交互提示；不在命令行、聊天或文档拼入口令，不借上传 token 代替 Apple 凭据。
- Windows：签名机登录用户的 `Cert:\CurrentUser\My` 与硬件令牌，确认证书有效、代码签名 EKU、私钥可用。历史证书 thumbprint `B82824C01226426C2D2BD423F883DCBC999C7E82` 仅是已验参照，每次发现并明确指定当前证书，不用 `/a`。PIN 只由签名人员在令牌对话框输入，代理不读取或存储。
- Common：发布器优先 `NEWLINK_COMMON_PASSWORD`，再 macOS Keychain service `KEMI Newlink Common Publisher`，最后隐藏交互输入；用户名默认 `common`。已有有效钥匙串凭据直接复用，新增保存凭据需授权。
- 商场：官方管理员登录取得 Bearer token；凭据和上传 token 仅留在权限 0600 的临时文件/内存，流程结束清理临时凭据。无凭据时继续本地构建验收，不能伪造上传完成。

## 3. PAD 构建、平台签名与覆盖安装

详细依据：[Android 构建](android-build.md)、[仓库发布 runbook](repository-runbook.md)。以下以当前脚本为准：Flutter 3.24.5（`dec2ee5c1f98f8e84a7d5380c05eb8a3d0a81668`）、Rust 1.97.1、cargo-ndk 4.1.2、NDK 28.2.13676358、JDK 17、flutter_rust_bridge_codegen 1.80.1。

1. 在 REPO 使用 `res/bootstrap-kemi-flutter.sh` 和既有固定 Android vcpkg 准备流程；核对 lock、SDK/NDK、JNI 库和生成桥接，不升级全局 Flutter。
2. 当前发布机已有参数：JAVA_HOME `/Users/newlink/jdk/jdk-17.0.19+10/Contents/Home`；ANDROID_SDK_ROOT `/Users/newlink/android-sdk`；Android vcpkg `/Volumes/ORICO/kemi-build-cache/rustdesk-pad-edge-287/vcpkg`，installed root 为同级 `vcpkg-installed-arm64-v8a`。这些是本机已验缓存，其他机器必须核对实际工具链，不创建空目录冒充依赖。
3. 依照脚本当前支持配置项目专属 CARGO_TARGET_DIR、GRADLE_USER_HOME、TMPDIR 与 Flutter 中间目录。当前 main 脚本支持 `KEMI_ANDROID_EXTERNAL_RUN_DIR`；旧隔离测试树参数可能不同，先读当前脚本。完整缓存可用时 `KEMI_PUB_OFFLINE=1`；依赖原使用 `PUB_HOSTED_URL=https://pub.flutter-io.cn` 和 `FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn`。
4. 私密环境注入后执行（从 REPO）：

```bash
res/build-kemi-android-release.sh --abi arm64-v8a
```

干净源码统一包装入口为 `res/build-kemi-from-source.sh android`。不要绕过脚本直接 `flutter build apk` 或用 debug keystore。正式版本不设置 `KEMI_ALLOW_DIRTY=1`。

5. 接收脚本输出 `flutter/build/kemi-release/KEMI-PAD-<版本>-<commit前12位>-arm64-v8a.apk` 和 build-info。脚本核对 Release 非 debuggable、包名、实际 versionCode、zipalign（16KB 对齐门禁）、v1/v2 签名、固定证书。必要独立复验用 SDK 同版本 `apksigner verify --verbose --print-certs`、`zipalign -c -P 16 4`、`aapt dump badging`；不打印 keystore 内容或口令。
6. 覆盖升级用 `adb -s <已授权地址> install -r <该APK>`，不卸载。回读包版本、UID、权限、默认 IME、设备配置和 `/data/app/.../base.apk` SHA-256，必须等于最终候选。测试主副屏双向启动/扩展、浏览器投放、HOME 退出后按钮状态、收回恢复、键盘提交/修饰键、连接和文件传输。按当前验收任务记录白盒解码器、帧尺寸、首帧、CPU/PSS/FD、崩溃/ANR；既有 100 次旧哈希结果不能套用到新 APK。
7. 固定正式名只复制已经验收的这一 APK，后续 Common 和商场都上传同一字节。

## 4. Mac 双架构构建、Developer ID、Apple 公证

详细依据：[Mac 签名公证](macos-signing-notarization.md)、[仓库 runbook](repository-runbook.md)。历史 Mac 参考末尾仍写 Flutter 3.24.5，那是旧版本记录；当前 Mac 脚本固定 `.toolchains/flutter-macos-3.27.4`、独立 macOS lock，Android SDK 保留 3.24.5。以冻结脚本和 `build-toolchain-policy.md` 为准，记录本轮 Rust 版本，不拿旧 CI Mac Rust 值代替本地实测。

1. Apple Silicon 发布 Mac准备 Xcode CLI、CocoaPods、项目固定 Flutter、桥接生成器、双架构 Rust/vcpkg（`arm64-osx`、`x64-osx`）、FFmpeg VideoToolbox。正式入口会调用 bootstrap 并编两套：

```bash
KEMI_BUILD_CACHE_ROOT=/Volumes/ORICO/kemi-build-cache/rustdesk-source-build res/build-kemi-macos-universal.sh
```

当前脚本拒绝已有 flutter/build 与同名候选；保留并核对旧目录用途、运行占用后才能恢复性移开，不删除或中断同事构建。单独 `res/build-kemi-developer-id-macos.sh` 是单架构候选。

2. 构建日志的实际 Xcode DerivedData 必须属于本项目；不允许用户全局 Flutter build-dir 指向 VibeKits。核对本轮 Flutter AOT、新 Rust dylib、service、display helper、连接管理器来源；每个承诺的 Mach-O 都包含 arm64/x86_64。脚本先合并再使用 `res/sign-kemi-developer-id-macos.sh` 显式签内嵌代码，最后以 Runner Release.entitlements、`--options runtime`、安全时间戳签外层。
3. 默认身份不变，`KEMI_MACOS_TIMESTAMP=required`；off、adhoc、旧测试证书不能正式发布。候选签名验收：

```bash
codesign --verify --deep --strict --verbose=2 '<Universal候选App>'
codesign -dv --verbose=4 '<Universal候选App>'
codesign -dr - '<Universal候选App>'
```

检查 Identifier、Developer ID、Team、Runtime、entitlements 和当前正式版 designated requirement。`--deep` 用于验证，不作为重新签名捷径。

4. 候选生成在 `../BIN/release/candidates/`，正式签名候选 ZIP 仍未公证。提交准确候选 ZIP：

```bash
xcrun notarytool submit '<Universal签名候选ZIP>' --keychain-profile KEMI_NOTARY --wait
xcrun notarytool info '<本次提交ID>' --keychain-profile KEMI_NOTARY
```

只接受 `Accepted`；Rejected/Invalid 用 `xcrun notarytool log '<ID>' --keychain-profile KEMI_NOTARY '<日志路径>'` 查精确原因。In Progress 保留 ID 跟进；上传中断不等于完成，不盲重编 App。

5. 对 ZIP 所提交的同一 App 装订，不能直接 stapler ZIP：

```bash
xcrun stapler staple '<已Accepted的App>'
xcrun stapler validate '<已Accepted的App>'
spctl --assess --type execute --verbose=4 '<已Accepted的App>'
```

将 App 以固定名 `KEMI远程办公.app` 放到独立打包目录，保留 Framework 符号链接，装订后重新打包：

```bash
(cd '<打包目录>' && /usr/bin/zip -qry --symlinks '<最终ZIP绝对路径>' 'KEMI远程办公.app')
unzip -tq '<最终ZIP>'
shasum -a 256 '<最终ZIP>'
```

6. 最终 ZIP 顶层只有一个 `KEMI远程办公.app`（其内部合法 helper App 不算第二个顶层 App），无 `._*`/`__MACOSX`。模拟浏览器隔离与系统归档解压，覆盖 `/Applications/KEMI远程办公.app` 并真实启动；验证不进 AppTranslocation、不报损坏/-47、主 App 和连接管理器仍能使用原录屏/辅助功能授权。对实际解压包再次 codesign、stapler、Gatekeeper，要求 accepted / Notarized Developer ID。
7. 验签在正常 macOS Security/trustd/钥匙串上下文；沙箱 Authority unavailable 与哈希未变并不能证明制品损坏，使用授权的正常上下文复核。核验通过的 post-staple ZIP 才复制为 `KEMI-macOS.zip`。

## 5. Windows 构建、双节点挂载、内外层签名

必读：[两节点实际流程及故障恢复](windows-two-node.md)、[完整硬件令牌签名流程](windows-signing-workflow.md)。读配套 simulator/device-lab 技能并核验当前设备目录。历史 signing ID 可能变化，不能从参考旧 ID 直接连接；编译机 A 与签名机 B 身份、SSH host key、用户会话均须匹配现时可信记录。

1. A 本机固定 Rust 1.75、Flutter 3.24.5、LLVM 15.0.6、VS C++/SDK、项目 vcpkg，源码以冻结 Git bundle/快照传至版本目录并回读 SHA。xzl `C:\kemi\build` 是该机器既有用户特许；B 工作目录 `D:\KEMI-Test`，其他机执行本机约束。
2. 复用版本化构建脚本及日志，`vcvars64.bat` 后 `set "VCPKG_ROOT=<本项目vcpkg>"`，不要带尾空格。以下为编译核心，前置依赖/资源/生成器按完整流程：

```text
cargo build --locked --features hwcodec,vram,flutter --lib --release
cargo build --locked -p dylib_virtual_display --release
flutter build windows --release --no-pub
```

Flutter 指向 A 的项目 SDK。先按锁文件解析依赖；核对 generated_bridge.dart/freezed.dart、注册器和插件 junction，同源新 `rustdesk.exe`、`librustdesk.dll`、`flutter_windows.dll`、`data/app.so`、插件、虚拟屏 DLL、打印机/USB 驱动资源。缺失驱动必须从版本固定来源恢复并保留原 CAT 签名，不能用旧自研 DLL 凑包。
3. 编译错误 4551 查同时间 CodeIntegrity 3033/3077 和精确文件。按参考已验恢复/授权签名辅助工具流程处理，不关 WDAC、Smart App Control、全局 Developer Mode 或 ExecutionPolicy。先确认原任务状态才重试，禁止多份竞争构建。
4. A 的完整 stage 为只暴露本版本目录的 loopback WsgiDAV；A→B host-key-verified reverse SSH forward，让 B 经 `\\127.0.0.1@38889\DavWWWRoot\...` 在 D: 建目录链接。端口是历史已验例子，使用当前授权既定配置，不暴露盘根目录。先比较 A 实体文件与 B 挂载文件 SHA-256；在 B 原位签名必须改变 A 实体文件，不复制 A→B 候选。
5. B 在登录交互 Session 1，以固定链 `vibekits.device.app_control → Launch-Sign-<run>.exe → CMD → PowerShell → Invoke-KemiAuthenticode.ps1` 启动。SSH Session 0 仅适合读取状态，不能显示 PIN。按引用完整步骤展示已核对的空 PIN 窗口并等待签名人员输入；不截取或读取输入后的 PIN。
6. 内层按实际资源清单枚举全部需签 EXE/DLL，不能机械套 15/18 个历史数目。固定 helper 用 ExpectedFileCount、ExpectedThumbprint 和新 ReportPath；签名实现 `/fd SHA256 /tr http://timestamp.digicert.com /td SHA256`，逐个 `signtool verify /pa /all /v /tw`。保存路径、字节数、嵌入签名证书/时间戳、SHA-256、verify 返回码和总 PASS；注意系统 catalog 与嵌入 signer 差异，按固定验证器判断。
7. 内层 PASS 后在 A 复制本轮 Runner.res 至 `libs\portable\Runner.res`，用项目 Python 依赖运行既有 packer（从 `libs\portable`，SIGNED_STAGE 是完整已签树绝对路径）：

```text
python generate.py -f "<SIGNED_STAGE>" -o . -e rustdesk.exe
```

输出通常在 workspace `target\release\rustdesk-portable-packer.exe`，以本次 Cargo 实际输出为准。再为外层单文件建立独立签名 run，经同一挂载在 B 签名，要求第二份 PASS，A/B 最终 SHA-256 和字节数一致。打包后再改内部资源会使签名证据失效。
8. 用最终外层签名包在 A/B 实际解包/安装、验证主程序哈希、完整资源、真实 UI、连接和输入；PID/MainWindowHandle=0 或 Session 0 黑图都不能证明 GUI 成败。保留用户原服务/配置并恢复临时隔离，覆盖升级不清用户数据。正式名 `KEMI-Windows.exe`。用完后在无任务占用时清理本次临时隧道、挂载、WebDAV 与临时访问 key，保留正式包和报告。

## 6. Linux 固定 CI 和 AppImage

详细依据：[Linux workflow 摘录](linux-workflow.md) 及冻结仓库 `.github/workflows/kemi-distribution.yml`、`flutter-build.yml`、`kemi-docs/ci-build.md`。历史 CI 文档写 master 和旧版本，当前源码身份仍遵循第 1 节。

1. CI 固定 Rust 1.75、Flutter 3.24.5、LLVM 15.0.6、vcpkg baseline `120deac3062162151622ca4860575a33844ba10b`；focused profile 仅 x86_64，先 build-rustdesk-linux 完整 Flutter bundle→DEB，再 build-appimage。不使用 Ubuntu 本机旧安装包冒充。
2. 现有工作流可手动绑定已推送冻结 ref（先核验 gh 身份、仓库与现有 run，避免取消其他构建）：

```bash
gh workflow run kemi-distribution.yml --repo caucy2026/rust-desk --ref '<冻结ref>'
gh run view '<本次run-id>' --repo caucy2026/rust-desk --json headSha,status,conclusion,jobs
gh run download '<本次run-id>' --repo caucy2026/rust-desk --name 'kemi-linux-x86_64-<完整commit>' --dir '<专属输出目录>'
```

确认 run 的 headSha 与冻结 SHA 相同，下载的 artifact 来自该 run；保留 run ID/attempt。`publish-release=false` 不会自动发布 Common 或商场。
3. 配方版本取本轮 VERSION；已维护工作流处理同名 mv、root chmod、仅 AppDir.squashfs 时与 type2 runtime 组装，并上传最终 `kemi-linux-x86_64-<SHA>`（历史保留 14 天）。没有最终上传 artifact 不能算 Cloud Ready。
4. 核验 `file` ELF x86-64、AppImage type2 魔数（偏移 8 的 `41 49 02`）、可执行位、版本、完整动态依赖、字节数/SHA-256。在实际目标 Linux 桌面启动并测试连接、输入、可用扩展功能及授权延续；CI job 的 `--skip-tests` 不算用户验收。
5. 此既定路线没有 Authenticode/Apple 公证，也未声明另行 GPG 签 AppImage。SHA256SUMS 是完整性清单，不能写为签名。最终 `KEMI-Linux.AppImage` 独立验收，Linux 未验证不能说四端 PASS。

## 7. 汇总正式六文件

正式目录为 REPO 的同级 `BIN/release`；先核对已有用途再覆盖，每个文件来自已通过的最终候选。固定六名称：四端文件、第 1 节名称，加 `SHA256SUMS.txt`、`release-manifest.json`。

- SHA256SUMS 包含全部四端，即使本轮只更新一端。用 `shasum -a 256 KEMI-PAD.apk KEMI-macOS.zip KEMI-Windows.exe KEMI-Linux.AppImage` 生成，按本轮受控 staging 写入，上传前再 `shasum -a 256 -c SHA256SUMS.txt`。
- manifest 以当前客户端解析契约及已有正式完整 schema 为准（仓库 client-distribution.md、客户端 cloud resource 解析器）。targets 包含 `android/windows/macos/linux`、实际 version、architecture、固定 file、整数 size、小写 sha256、md5，及既有要求的 URL/签名、公证/source/run 字段。不要从可能陈旧的 BIN 本地 manifest 直接重发。
- 从已验证线上清单读取未更新平台；热修不伪造四端同版本，不以老包替新版本。先保存旧清单，再基于最终包计算新清单，公开 URL 用最终上传回传值，不编造 CDN 路径。客户端使用的服务器/公钥及资源白名单沿用项目配置，不借发布更改。

## 8. 发布 Common

必读 [Common 合同](common-contract.md) 和 `newlink-common-release` 技能；使用它现有 `scripts/publish_common.py`，不要用浏览器表单替代已可用 API。固定项目 Common、六个资源 ID 与本地 filename 在合同中。

```bash
python3 ~/.codex/skills/newlink-common-release/scripts/publish_common.py --version '<本批次版本>' --release-dir '<正式六文件目录>' --dry-run
python3 ~/.codex/skills/newlink-common-release/scripts/publish_common.py --version '<本批次版本>' --release-dir '<正式六文件目录>' --verify-download
```

既有 fast path 在精确文件已验证/授权时可省重复 dry-run；首次交接、可疑制品、签名改变用上述 audited path。热修增加 `--items KEMI-PAD,SHA256SUMS,release-manifest`（替换对应平台名）；完整四端发布省略 items。

顺序四端二进制→SHA256SUMS→manifest last。发布器校验 record ID/name/project，公开 `plugData`：`https://www.newlinksz.cn/screensaver/api/plugData?projectName=Common&name=<资源>` 的版本、MD5 和 HTTPS CDN URL。`--verify-download` 对选择资源回下载；要求大小、MD5、SHA-256 与本地最终包一致，结果 `COMMON_RELEASE=PASS`。批次版本与每端包内版本在清单分别如实记录。

上传一半失败时，不提前更新 manifest，不拿旧包凑位；保留已成功二进制，查失败对象，核对公开状态后只恢复必需部分。恢复旧版本也必须采用保存的确切正式字节和完整清单、manifest 最后，不盲降客户端版本。

## 9. 发布 KEMI 商场

必读 [商场 API 合同](market-contract.md)、[签名认证闭环](signing-certification-closure.md) 和 `kemi-market-publish`。每次执行先读取在线官方文档，文档 API 变更不能依赖本快照：

- https://kemi.newlinksz.com/kd/docs/ai-publish
- https://kemi.newlinksz.com/kd/docs/app-upload
- https://kemi.newlinksz.com/kd/docs/store-api
- https://kemi.newlinksz.com/kd/docs/app-self-update/android （其他平台替换 android）

1. 官方管理员登录 `https://kemi.newlinksz.com/usercenter/api/auth/login`；API 根 `https://kemi.newlinksz.com/kd-api`。先 GET `/api/apps/list?os_type=<os>&keyword=<package>&page=1&pageSize=20`，按精确 `(package_name,os_type)` 匹配。历史 PAD14/Mac61/Windows62 只作参照，Linux 和全部当前 ID 从实时记录确认；恰好一个则 update，零个才 create，多个先核查，不新建重复记录。
2. 读取完整现有记录与可见分类，保留名称、图标、语言、截图、描述、permissions、展示开关等字段。上传新的二进制 version_code 严格递增；同版仅可修元数据，不偷换不同 hash 二进制。
3. PAD 用 `/api/upload/apk-token`、`apk-complete`；桌面 `/api/upload/package-token`、`package-complete`。category Windows `winpkg`、Mac `macpkg`、Linux `linuxpkg`。请求 filename 和精确 integer size，按返回 upload_url multipart 上传 token/key/file，再 complete 返回 key/filename/size。要求 status200、HTTPS URL、exact size 和 SHA-256；桌面 complete 可能不解析包内版本，须使用已验证实际版本，不能复制空字段。
4. POST `/api/apps/update` 带现有 app_id 与完整元数据、正确 package/os/version、最终下载 URL。必须同时写 `file_size_bytes` 整数和 `file_size` 同字节数字符串，`apk_sha256` 为最终文件小写 SHA-256；不要用“25MB”等展示值。不擅自改 force_update。
5. 回读开发记录、GET `/api/store/apps/<id>?os=<os>` 和不带 category 的 GET `/api/store/apps?page=1&pageSize=100&os=<os>`：版本、hash、两个大小字段、HTTPS、store 可见性一致，列表包含该 App。
6. CDN 完整回下载，同一最终文件 SHA-256/字节数一致，重新验签（Mac 解压验签/公证，Windows Authenticode，PAD固定证书）；用前一线上 version_code 查 `/api/store/update/check?package_name=<package>&version_code=<old>&os=<os>` 必须 has_update=true、目标包一致，用新 code 查必须 false。Windows/Mac/Linux 显式 os，防止串端。
7. 在目标机远程办公 App 自己的商场实际下载更新并启动、验证原配置/身份/系统授权延续。用户要求仿真渠道时用 simulator 操作该 App 商场；simulator 直接 download/app_install、ADB install、SSH 复制属于其他安装方式，不能算应用内商场更新。线上与设备已经同版时记录“已最新＋界面/白盒核对”，不降级重装刷次数。权限拒绝、不支持 UI、Session0 不可见分别记录，不把工具能力不足写成源码故障。

## 10. 最终交接与故障处理

每端独立记录：完整源码 SHA/子模块/是否脏、工具链、构建机、版本、绝对包路径、字节数/SHA-256、签名主体/证书指纹/时间戳报告、Mac 公证 ID/Accepted/staple/Gatekeeper、实际升级前后授权、功能证据、Common ID/公开 URL/MD5/回下载、商场 app_id/os/version/size/hash/正反更新检查/应用内更新结果。

PASS 需要同一最终哈希贯穿构建、验收、上传、回下载、安装；未做项写 NOT_RUN/待验收，明确具体限制。一个平台失败只补该平台及实际受共同源码改动影响的平台；不重复编译已有效包，不以历史 100 次、签名成功、上传100% 或后台 PID 替代目标验收。

文档冲突优先顺序：当前用户明确范围与有效授权 → 系统/平台权限边界 → 当前适用 AGENTS/LOCAL → 冻结源码脚本与当前 API 契约 → 有时间标记的历史案例。旧 Mac 文档错误“装订 ZIP”、历史 master、旧 Flutter/版本/设备 ID 必须依照本手册纠正；不把历史成功或未完成案例描述为本轮四端发布结果。
