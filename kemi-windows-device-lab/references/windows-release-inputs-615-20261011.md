# Windows发布输入：615现场经验

本记录是已验证方法，设备路径、版本、计数与指纹均须按当前项目发现，不是其他项目默认值。

- 冻结pubspec.lock使用pub.flutter-io.cn时，Windows命令必须设置相同PUB_HOSTED_URL。615缺此变量时enforce-lockfile报119个来源变化，版本没有变化；恢复镜像后原锁门禁通过。不能去掉enforce-lockfile或升级依赖来掩盖来源差异。
- Windows采用已验证的三段语义build-name及独立整数build-number。615误用1.9.0.615时，生成配置和最终EXE均回落1.0.0；恢复1.9.0-dev.615/2615并增量构建后，配置和真实EXE一致。编译exit0与源码版本正确均不能替代成品资源核验。使用项目tool/verify_windows_release_version.py核对pubspec、generated_config.cmake和最终FileVersionInfo的字符串及数字版本；UTF-8源码与JSON显式UTF-8读取，避免Windows默认GBK解码失败。
- 直接测试hbb_common可能启用重复的WebRTC开发依赖，固定Rust1.75无法编译其is_multiple_of。沿既有独立测试投影，仅移除重复强制开发依赖，保持原可选生产依赖、锁定版本、断言及生产源码不变；记录投影前后hash。615真实18项授权/身份/待确认/存储测试通过，生产1084项非生成输入与新relay字节核验通过。不能把旧二进制的证明套给新relay，也不能把投影测试称产品运行通过。
- 新relay元数据可能没有旧脚本直接赋值的属性。615在sourceFingerprintSha256 setter处退出，签名未启动；确认终态与候选字节后，用Add-Member兼容添加属性，并从已知失败点续做。保留首失败，不重复构建或复制完整候选。
- 原注册长命令包装器的exec参数含一个未使用占位参数；缺少它会在远端完成后保存控制端回执时报IndexError。先核实际PID/日志/终态，不因控制端报错重跑远端工作。

证据：[615构建与版本门禁](https://github.com/caucy2026/vibekits/blob/main/docs/acceptance/WINDOWS615_UNSIGNED_BUILD_VERSION_GATE_20261011.json)、[615原生授权与暂存](https://github.com/caucy2026/vibekits/blob/main/docs/acceptance/WINDOWS615_NATIVE_PERMISSION_AND_STAGE_20261011.json)。签名、覆盖升级、真实模型/房间任务与长期稳定仍需独立验收。
