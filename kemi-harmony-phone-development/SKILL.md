---
name: kemi-harmony-phone-development
description: 移植、编译、企业认证、签名发布和 USB/Wi-Fi 调试 KEMI 远程办公原生鸿蒙手机控制端，复用 PAD 对齐、账号存储与华为应用市场发布记录。用于鸿蒙 HAP/APP 开发、问题修复和企业上架；不用于 Android APK 或直接部署 HBBC 服务。
---

# KEMI 鸿蒙手机开发与真机调试

沿用独立鸿蒙源码、固定 Flutter-OH/Rust 工具链和已验证安装路线。手机主动连接远端电脑，不提供被控能力；保留用户要求的 PAD 按钮和账号功能，不把最小权限解释成任意裁剪功能。

## 按当前任务读取

- 接续本机工作：先读 [references/environment.md](references/environment.md)，核对独立仓库、分支、当前候选、工具链和历史状态。
- 连接手机、定位锁屏/失联/日志问题：读 [references/usb-wifi-debug.md](references/usb-wifi-debug.md)。USB和无线使用相同HDC，不能用ADB是否发现手机判断原生鸿蒙是否在线。
- 移植、FRB、原生依赖、编译与签名：读 [references/build-port-sign.md](references/build-port-sign.md)。只在本机强制外盘规则允许的位置构建。
- UI、账号、颜色、缓存、密码问题：读 [references/fixes-and-account.md](references/fixes-and-account.md)，复用根因与修复，避免引入未上线额度探针。
- 按钮、设备切换、升级及只控不被控验收：读 [references/acceptance-release-git.md](references/acceptance-release-git.md)。实际测试还应使用项目 `app-release-stability-gate`；公开上架阶段使用 `public-app-distribution`，本技能不扩大发布授权。
- 企业认证、APP ID、正式证书/Profile及发布：读 [references/enterprise-store-release.md](references/enterprise-store-release.md)，包含本机签名材料位置和已验证发布现场。公开上架同时沿用public-app-distribution。

## 必须保持的产品约束

1. 使用原生 HAP/APP，不能把APK改扩展名。设备API从 `param get` 读取，SDK版本不是手机版本。
2. 保持同一发行身份的包名、签名、设备身份及凭据存储标识，覆盖安装不清数据。旧调试版`com.newlinksz.kemi.remote`继续保留；用户已明确选择的企业商店新身份为`com.newlinksz.kemi.desk`，仅publish产品使用，不能声称跨包自动继承旧数据。未来desk升级保持desk身份。
3. 当前控制端包只有INTERNET权限，无被控扩展与后台服务。还需禁止Rust被控启动、Rendezvous注册和入站控制路径；权限门禁不等于运行时证明。
4. 手机显示默认适应窗口；远端分辨率不因连接、重连或切显示器改变。基础触摸/鼠标/键盘协议保留。
5. 账号、额度与其他手机保持同一套服务端规则，不使用内部PAD身份假装普通华为手机；已有授权与隐私边界延续。
6. 逐个精确候选记录SHA256、源码和构建覆盖文件；重新签名、重建都会改变候选。旧包百次切换不能算新包百次通过。
7. 调试Profile有设备白名单和有效期，不能作为任意手机安装或上架完成证明。华为主体、法律声明、验证码与身份材料只按实际授权处理。

## 可复用脚本

- `scripts/device_probe.py`：指定HDC、目标和预期型号，只读身份及实时UI布局；型号不匹配立即失败。
- `scripts/switch_devices.py`：指定候选哈希和已授权设备标签，执行设备切换；禁止把已选中设备重复计数。自动恢复竖屏工具栏滚动，保存每次状态、截图与哈希。截图需私密保存并人工核对，方可判断没有串屏。脚本不会输入远端文字、重启或锁定远端电脑。

无需每次重新申请正常构建/测试授权。遇到缺证书、设备掉线、锁屏或真实账号凭据缺失时，继续不受阻工作并准确标注尚未验证项；不把入口可见或脚本命令返回0冒充功能成功。
