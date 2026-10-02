> 2026-09-30 核对的操作参考。原始来源：`/Users/newlink/kemi/RustDesk/client/kemi-docs/android-clean-clone-reproducible-build.md`。历史版本、设备 ID 和结果只用于复现依据；执行以当前源码脚本、设备目录及本手册的冲突处理说明为准。本文不含签名私钥或口令。

# KEMI Android/PAD 干净源码复现构建

> 目标：同事从 `caucy2026/rust-desk` 下载源码后，生成与KEMI正式渠道一致的包名、版本、ARM64业务内容和固定签名APK。

## 1. “一样的APK”如何判断

必须同时满足：

- 相同源码commit和`Cargo.lock`、`flutter/pubspec.lock`；
- `package=com.newlinksz.kemi.remote`；
- `versionName/versionCode`与`flutter/pubspec.yaml`一致；
- 只包含`arm64-v8a`；
- 使用同一受控证书；当前 PAD 1.4.127+310 正式渠道证书 SHA-256 为 `c8a2e9bccf597c2fb6dc66bee293fc13f2fc47ec77bc6b2b0d52c11f51192ab8`，实际以构建脚本的固定证书校验值为准；
- v1、v2签名、zipalign、Release非debuggable全部通过；
- 解压后所有业务文件的`apk_content_sha256`一致。

Android Gradle/apksigner可能改变ZIP容器或APK Signing Block中的非业务字节。因此，两次clean构建即使所有解压文件逐字节一致，整个APK的SHA-256仍可能不同。本项目在加入固定源码时间和自动恢复子模块后，实测两次`1.4.104+211`构建：

```text
第一次整包：57b86560bf3cb61e11a63f0d4c495fd07ee8e2d9a010f3453d26c9f561c45f54
第二次整包：22952b7c79ebe077b102d883207c746d26bf111f2f23b9dc1239d3590242af40
解压内容：  完全相同
内容指纹：  8bd96efe8dbb3fbadf0ae9aa685bba7c62058d1e5e595d640b3e84fe72d18390
```

所以：

- 需要“相同功能、身份和可覆盖升级”的同事重编包，使用本流程和`apk_content_sha256`验收；
- 需要“整包SHA完全相同”的文件，禁止重新编译，必须直接分发同一份canonical APK，并核对它公布的整包SHA-256。

## 2. 固定工具链

```text
Flutter             3.24.5
Flutter revision    dec2ee5c1f98f8e84a7d5380c05eb8a3d0a81668
Dart                3.5.4
Rust                1.97.1
cargo-ndk           4.1.2
JDK                 17
Android platform    34
Android NDK         28.2.13676358（r28c）
vcpkg               120deac3062162151622ca4860575a33844ba10b
ABI                 arm64-v8a
```

Flutter、vcpkg和构建缓存不上传Git。源码仓库只保存下载脚本、官方SHA、依赖锁文件和验收规则，签名私钥与密码必须通过公司安全渠道单独交接。

## 3. 第一次准备

### 3.1 下载源码

```bash
git clone --recursive git@github.com:caucy2026/rust-desk.git
cd rust-desk
git checkout master
git submodule update --init --recursive
git status --short
```

`git status`必须没有受跟踪文件改动。`.dart_tool`、Pods、build和`.toolchains`属于生成物，不应提交。复现已发布的 `1.4.127+310` 时须检出其源码提交 `ec321c81ab3a826542a48f48a845bc82ebc9745f`；直接使用后来更新的 `master` 会改变按 Git 提交时间生成的 `BUILD_DATE`，不能声称内容字节相同。

### 3.2 安装基础环境

安装JDK 17、Android SDK command-line tools、Rustup和Git。Android SDK至少安装：

```bash
sdkmanager \
  'platform-tools' \
  'platforms;android-34' \
  'build-tools;35.0.0' \
  'ndk;28.2.13676358' \
  'cmake;3.22.1'

rustup toolchain install 1.97.1
rustup default 1.97.1
rustup target add aarch64-linux-android
cargo install cargo-ndk --version 4.1.2 --locked
```

不要使用系统中碰巧存在的其他Flutter或其他项目SDK。

### 3.3 安装项目Flutter

```bash
./res/bootstrap-kemi-flutter.sh
```

脚本支持Apple Silicon Mac、Intel Mac和x86_64 Linux；只从Flutter官方存储下载3.24.5，并在解压前校验官方SHA-256。目标固定为：

```text
client/.toolchains/flutter
```

目录已存在但版本或Git revision不匹配时，脚本会拒绝覆盖，必须人工移走错误SDK后重试。

### 3.4 安装Android原生依赖

```bash
export ANDROID_SDK_ROOT=/你的/Android/sdk
./res/bootstrap-kemi-android-deps.sh
```

脚本在`client/.toolchains/vcpkg`准备固定commit，并按`vcpkg.json`构建`arm64-android`依赖。第一次构建耗时较长，完成后可复用；不能因为慢而切换未知vcpkg或复制其他项目的库。

## 4. 安全导入固定签名

管理员通过安全渠道提供：

```text
kemi-release-2026.p12
Alias：kemi-android-release-2026
Store/Key密码
```

私钥不得上传Git、写入脚本、文档或聊天记录。配置只存在当前终端：

```bash
export KEMI_ANDROID_KEYSTORE=/安全目录/kemi-release-2026.p12
export KEMI_ANDROID_KEY_ALIAS=kemi-android-release-2026
export KEMI_ANDROID_STORE_PASSWORD="${KEMI_ANDROID_STORE_PASSWORD:?Provide signing password through a secure environment}"
export KEMI_ANDROID_KEY_PASSWORD="${KEMI_ANDROID_KEY_PASSWORD:-$KEMI_ANDROID_STORE_PASSWORD}"
```

缺少任一变量时Release构建必须失败，不允许回退debug签名，也不允许同事自己生成新证书。

## 5. 一条命令构建

```bash
export ANDROID_SDK_ROOT=/你的/Android/sdk
./res/build-kemi-android-release.sh
```

脚本依次完成：

1. 拒绝受跟踪源码dirty；
2. 核对Flutter、Rust、cargo-ndk、JDK、SDK、NDK、vcpkg、固定子模块和两个锁文件；
3. clean后按锁文件恢复Dart依赖；
4. 临时应用项目维护的可复现构建补丁，以源码commit时间生成`BUILD_DATE`，重编ARM64 Rust核心并拒绝未解析的libsodium符号；
5. 清理旧JNI，只复制本轮`librustdesk.so`和对应NDK的`libc++_shared.so`；
6. 使用明确的`build-name/build-number`构建Release；
7. 检查包名、版本、ABI、debuggable、zipalign、v1/v2签名和固定证书；
8. 输出APK、整包SHA、解压内容SHA及完整构建信息；无论成功或失败，都恢复上游子模块和受跟踪的`src/version.rs`。

输出位于被Git忽略的目录：

```text
flutter/build/kemi-release/KEMI-PAD-<版本>-<commit前12位>.apk
flutter/build/kemi-release/KEMI-PAD-<版本>-<commit前12位>.apk.build-info.txt
```

首次联网构建完成后，可用本地缓存复验：

```bash
KEMI_PUB_OFFLINE=1 ./res/build-kemi-android-release.sh
```

## 6. 交付与问题定位

交付时必须一起提供：源码完整commit、APK、`.build-info.txt`和canonical APK整包SHA。不能只说“master最新版”。

常见停止点：

| 提示 | 原因与处理 |
|---|---|
| project Flutter missing/mismatch | 运行Flutter bootstrap；禁止改用全局Flutter |
| tracked source is dirty | 提交或恢复代码；临时测试才允许`KEMI_ALLOW_DIRTY=1` |
| NDK/platform missing | 用sdkmanager安装文档固定版本 |
| missing vcpkg library | 运行Android deps bootstrap并等待完成 |
| signing variable/certificate mismatch | 联系管理员重新安全导入固定p12，禁止生成新证书 |
| pub get changed lock | 源码与锁文件不一致，停止构建并Review，不得自动升级依赖 |
| unresolved sodium symbols | native缓存或归档工具错误，删除对应Rust target缓存后重编 |
| 整包SHA不同但内容SHA相同 | ZIP/签名容器差异；功能包一致，外发仍以canonical APK为准 |

构建完成后清理密码环境变量：

```bash
unset KEMI_ANDROID_KEYSTORE KEMI_ANDROID_KEY_ALIAS
unset KEMI_ANDROID_STORE_PASSWORD KEMI_ANDROID_KEY_PASSWORD
```
