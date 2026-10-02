# USB、Wi-Fi HDC与真机诊断

## 目标与信任先核验

使用现有HDC，不切ADB。Mac USB描述符出现HUAWEI HDC Device而ADB无设备是正常原生鸿蒙情形。只操作已授权手机；多设备时每个命令都带 `-t`。

```bash
kemi_hdc='/path/to/existing/hdc'
"$kemi_hdc" list targets
kemi_target='<当前USB连接键或IP:端口>'
"$kemi_hdc" -t "$kemi_target" shell param get const.product.model
"$kemi_hdc" -t "$kemi_target" shell param get const.product.name
"$kemi_hdc" -t "$kemi_target" shell param get const.ohos.fullname
"$kemi_hdc" -t "$kemi_target" shell param get const.ohos.apiversion
"$kemi_hdc" -t "$kemi_target" shell param get const.product.cpu.abilist
```

真实USB调试流程：开发者模式/USB调试已开启→USB被系统识别→HDC状态→确认手机授权弹窗。用户已确认授权后，历史一次对指定连接执行 `hdc reconnect <连接键>` 恢复Unauthorized/Offline；先查看当前HDC帮助确认命令支持。不要清信任、换调试密钥或重启全部HDC来解决单机问题。

## Wi-Fi连接

手机无线调试页给出当前IP和连接端口。端口会变化；不要把本机HDC server默认8710当作手机无线端口，也不要猜测ADB配对命令适用。

```bash
"$kemi_hdc" tconn '<用户提供的手机IP:端口>'
"$kemi_hdc" list targets
kemi_target='<新IP:端口>'
"$kemi_hdc" -t "$kemi_target" shell param get const.product.model
```

本次实测 `tconn 192.168.1.142:35653` 返回Connect OK，随后list targets精确显示该目标，型号为HOP-AL00。切到无线后必须把脚本 `-t` 改为新连接键，不能仍使用旧USB序列。只核验授权地址，不扫描整个网段。

若USB列表Empty且系统USB列表也无目标，可能是物理断开；不要仅凭这一点断言所有连接不可用。已开启的无线端口可复用。旧IP:8710拒绝后用户提供35653才恢复，本轮没有重启HDC。

## 本机连接失败与真失联区分

本轮default sandbox下出现Connect server failed，获准执行同一HDC命令后正常；本机HDC server仍在线。这是工具访问权限问题，不是设备坏或需要用户重授权。优先用平台的精确工具审批恢复同范围访问。不能通过另一个工具绕过拒绝。

锁屏导致aa start返回10106102；先读取ScreenLockRootComponent确认实际锁屏。开发者模式下无法安全自动解锁，不关闭开发者模式、不模拟破解密码。此前用户解锁后直接沿原路线继续，没有卸载重装。

## 安装、启动、布局与日志

```bash
"$kemi_hdc" -t "$kemi_target" install -r '<冻结且校验过的signed.hap>'
"$kemi_hdc" -t "$kemi_target" shell aa start -a EntryAbility -b com.newlinksz.kemi.remote
"$kemi_hdc" -t "$kemi_target" shell uitest dumpLayout -p /data/local/tmp/kemi-layout.json
"$kemi_hdc" -t "$kemi_target" shell cat /data/local/tmp/kemi-layout.json
"$kemi_hdc" -t "$kemi_target" shell snapshot_display -f /data/local/tmp/kemi-frame.jpeg
"$kemi_hdc" -t "$kemi_target" file recv /data/local/tmp/kemi-frame.jpeg '<私密证据目录>/frame.jpeg'
"$kemi_hdc" -t "$kemi_target" shell hilog -x
"$kemi_hdc" -t "$kemi_target" shell uitest uiInput help
```

先看本机SDK/设备命令帮助，不假设aa/bm/hilog选项跨版本一样。`hilog -t Flutter` 错误：-t是日志类型，不是标签；本轮使用 `hilog -x` 有界读取后按包名/阶段/数字错误码筛选。禁止清日志、输出令牌或复制整个私有目录。

每次动作读取最新布局的bounds/text/selected/enabled，折叠/展开、IME、工具栏滚动会改变坐标。用于脚本的基本命令实测：uiInput click x y、swipe x1 y1 x2 y2 velocity、keyEvent Back/Home。inputText/text会实际输入，只有明确测试输入授权和隔离目标时使用。

## 返回键和控件注意事项

- IME显示时Back可收起输入法；IME不显示时Back会弹出关闭连接确认，不是通用关闭面板。
- 输入帮助用蓝色向下按钮收起；按钮图标若无语义，先截图校准并限制到当次分辨率，不能跨布局复用硬编码点。
- 关闭连接确认是“确认”，应用退出确认实际是“退出”；读取当前对话框，避免同名浮动确认按钮误定位。
- 竖屏底部工具栏横向滚动后才显示多个设备图标。切到新设备会回到左侧，等待选中状态前需再滚动显示设备。定位失败不能算应用连接失败。
- 展开/收起工具栏仅是本地UI；不要在远端画布上误做滑动或按键。

## 只读探针

```bash
python3 -B '<skill>/scripts/device_probe.py' --hdc "$kemi_hdc" --target "$kemi_target" \
 --expected-model HOP-AL00 --out '<私密唯一运行目录>/probe'
```

官方HDC文档：https://github.com/openharmony/docs/blob/master/zh-cn/application-dev/dfx/hdc.md 。原生无线调试连接与USB设备信任受系统约束，已有信任正常延续，不自动开启所有网络调试端口。
