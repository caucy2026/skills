# 本机已验证环境与来源

这是2026-10-01的本机配置记录，不要求同事复制磁盘或个人路径。执行前读取适用AGENTS.md及同目录LOCAL-ENVIRONMENT-RULES.md。本机规定所有可再生构建/缓存使用已挂载、可写的 `/Volumes/ORICO/kemi-build-cache/`，不能外盘离线时写到系统盘同名目录。

## 工作区隔离

- 外层 `/Users/newlink/kemi/RustDesk` 不是产品Git根。
- 原PAD/桌面源码 `/Users/newlink/kemi/RustDesk/client` 有其他同事工作，禁止直接移植、覆盖或切它的分支。
- 鸿蒙独立仓库 `/Users/newlink/kemi/RustDesk/harmony-phone`，产品源码在 `client/`。
- 鸿蒙分支 `harmony-phone-pad-parity-20261001`；私有GitHub `caucy2026/kemi-remote-office-harmony`。默认分支 `main` 保持原代码；同事克隆后明确切鸿蒙分支。
- 原隔离基线 `c440ac4c5098682abfab5be521dfcc2f35d608f8`。实际后续构建工作区曾以 `d75671b` 为核心基线加明确页面覆盖；不能因为工作分支更新就声称已全量重编核心。
- 固定物理构建目录 `/Volumes/ORICO/kemi-build-cache/rustdesk-harmony-phone/build-workspace/flutter`。
- 原生库缓存及工具链根 `/Volumes/ORICO/kemi-build-cache/rustdesk-harmony-phone`；证据放 `research/` 的唯一运行子目录。
- 本地正式代码备份 `/Users/newlink/kemi/RustDesk/harmony-phone-backups/20261001`；使用新增目录和Git bundle，不覆盖原备份。

## 工具链

- HDC：`.../toolchains/hdc-public/toolchains/hdc`，历史3.2.0f；旁边依赖库须保持。先 `version` / `checkserver` 核对，不全局换工具。
- CLI：`.../toolchains/cli-6.1.1.418/command-line-tools`。
- Flutter-OH：`/Users/newlink/kemi/RustDesk/harmony-phone-flutter-sdk-source`，固定 `eea47c62cc5ff1000db068306ffe7279d53e889b`，Flutter3.41.10 OHOS；其他端Flutter版本不同，不能升级主线。
- Java17：`/Users/newlink/jdk/jdk-17.0.19+10/Contents/Home`。
- Rust1.90.0、目标 `aarch64-unknown-linux-ohos`、FRB代码生成器1.80.1。
- 入口 `client/res/harmony-phone-env.sh` 为Bash；不能用zsh直接source后忽略BASH_SOURCE相关错误。
- 该环境设置PUB_CACHE/TMPDIR/CARGO_TARGET_DIR/RUSTUP_HOME/CARGO_HOME/HVIGOR_USER_HOME/npm缓存；固定LLVM及Host sysroot用于FRB。

## 设备与当前包快照

- HUAWEI Pura X Max、HOP-AL00、arm64-v8a；最初读取API24，2026-10-01无线重连实际API26。每轮重新读取，保留历史差异。
- USB连接键、无线IP/端口是现场参数；取 `hdc list targets` 和用户授权的最新地址，不把旧值写死在脚本。
- 当次成功无线目标 `192.168.1.142:35653`；电脑端HDC服务的8710端口不是这个手机端口。
- 包名 `com.newlinksz.kemi.remote`，EntryAbility，1.4.127+407，最低API23，目标API24。
- 本次账号候选SHA256 `7babdbb6ac0430ba321dc0f758a2eecad7dbc36d5fe0478cf62a28c6273862ad`；文件 `entry-account-final-signed.hap`。这是历史已安装基准，下次使用当前冻结记录。
- 现有单手机调试Profile有效期曾为2026-10-15；执行时重新校验，不承诺未来有效。

## 项目资料按阶段定位

`client/kemi-docs/` 下：HARMONY-PHONE-ADAPTATION-20260930.md（初始过程，含后来被覆盖的范围）；HARMONY-PHONE-CONTROLLER-STATUS.md（核心/签名早期记录）；HARMONY-PAD-FUNCTION-TEST-REPORT-20261001.md（分候选测试和故障）；HARMONY-ACCOUNT-INTEGRATION-20261001.md（账号与原生存储）；HARMONY-CHANGELOG-20261001.md（本轮变更与反馈）；HARMONY-FORMAL-DISTRIBUTION-PREFLIGHT-20261001.md（发布资格）。旧文件的“未安装”“未登录”等不是当前实时状态，优先最新实际命令、候选和用户指令。
