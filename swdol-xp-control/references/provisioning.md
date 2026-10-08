# 首次准备与从头注入

只有首次使用、VM/游戏代次变化、文件缺失或制品不匹配才进入这里。暖重登直接走操作手册，不重复安装。

## 1. 两台来宾先分清

| 系统 | 运行环境 | 入口与用途 |
|---|---|---|
| 原版服务端 | UTM / Windows Server 2003 | `192.168.128.2`，SMB445，Master4531，地图5000+ |
| 原版客户端 | 86Box / XP / Pentium II 450MHz | `xp_swdol_voodoo3`实际进程和窗口，SLiRP网络 |
| 宿主 | macOS | UDP27667 collector，TCP27666输入监听 |

不能把 `192.168.128.2:C$` 当XP的C盘。今天误投递到后台的 `C:\xyol-tools` 是错误路线，那里出现POLL_ALIVE不说明XP出了问题。

端口只有协议定位作用，不代替进程身份。Map14必须TCP5014唯一owner、进程名NewLocalServer.exe、配置LocalServer14.ini一致。图号公式只作线索，权威Section目录和实际listener才是准据。

## 2. 后台注入（与前端分开）

完整后台SOP：
`/Users/kemi/coding/swdol2026/document/20260918-原版怒火山Map14注入与服务器实体读取完整手册.md`。

只附加已运行进程，不启动/重启地图服，不改共享数据库。先在来宾内部只读确认：

```bat
netstat -ano | findstr ":5014"
tasklist /fi "PID eq <刚得到的唯一owner>"
wmic process where processid=<刚得到的唯一owner> get Name,CommandLine,ExecutablePath
```

零owner、多owner、名称或配置不符即停止，不猜PID。宿主端口可达不能代替这三项。

检查UDP27667已有collector。存在则复用、记录路径并切本轮时间窗；没有才新开一个：

```sh
python3 /Users/kemi/coding/xyOnlie/tools/legacy-dynamic-trace/collector.py \
  --bind 0.0.0.0 --port 27667 --output <新证据目录>/trace.jsonl --quiet
```

既有Map14脚本：`swdol2026/tools/legacy-dynamic-trace/map14_attach_only_scm.py`，密码只用getpass/stdin。

**注意现有脚本调用 `cleanup_before_server_injection`，本轮曾删除约5.3GB历史trace。下次不得默认重跑这个清理步骤。先查看当前脚本及清理范围；优先复用resident observer。需要新附加时，保留证据并移除/禁用实验副本的自动历史清理，不把已完成的删除当成必要注入步骤。**

当批准的脚本和制品均锁定后，其调用形状为：

```sh
PYTHONPATH=/private/tmp/xyol-impacket python3 <已检查的Map14脚本> \
  --build-dir <本轮已审计制品目录> --output-dir <本轮全新证据目录>
```

仅当前安全stdin输入密码，不把密码拼进命令行、Git、文档或日志。依赖缺失时安装到隔离目录，不因网络沙箱错误断言服务器已宕机。

通过条件全部满足：唯一owner、INJECT_OK/ALREADY_ACTIVE、PAYLOAD_LOADED、PROBES_ACTIVE、同PID新heartbeat和业务事件、注入后服务健康。本轮历史PID1952通过这些实际载荷门，但不能下次直接复用这个数字。

后台Map14和前端昆仑山Section10不是同图实验。两边同时有事件不等于同一行为已经关联。

## 3. 观察器自动附加前端

默认复用XP内 `C:\xyol-trace` 的常驻基础、effect、render等已批准观察器。按标准登入器启动新游戏PID后读取新事件，不为每次登录再次跑安装BAT。

需要核对：

```text
目标程序/资源身份
→ PAYLOAD_LOADED
→ 当前代次PROBES_ACTIVE
→ ClientTraceReady（实际游戏PID）
→ 同PID heartbeat
→ 本次需要的业务事件
```

观察器自身发出的 `ClientInjectionSucceeded` 中 `pid` 可能是观察器，目标PID在定向字段/寄存器；不能把212这类观察器PID当游戏PID。实际payload的ClientTraceReady/heartbeat来自游戏PID。

不能用旧日志、截图、程序存在或只有心跳证明新探针已预装。新探针不在当前PID内时必须按既有新PID流程准备，不能临时热叠。

## 4. DirectInput制品：优先用成功归档

目录：`/Users/kemi/coding/swdol2026/document/evidence/20260920-xp-control-artifacts/`。

| 文件 | 成功SHA-256 |
|---|---|
| xyol-injector.exe | e2446d42080df4f7de64829aea3c32c93de4bb2416d8fb8a6d16beecacfd4525 |
| xyol-input.dll | 476faadf547359d66e188860f2829388ca015587f554ae3994921211f9901ea9 |

旧文件中发现真实SSE2：movd/pshufd/movdqa使用xmm寄存器。Pentium II不能运行，不能跳过CPU审计。成功构建只沿用既有源码，采用：

```text
-target x86-windows-gnu -march=pentium2 -mno-sse -mno-sse2 -mno-sse3
-ffreestanding -fno-builtin -fno-exceptions -fno-rtti -fno-threadsafe-statics
Windows subsystem 5.01 / CRT-free
```

成功构建命令存于同目录 `build_xp_dinput_p2.sh`。这是复现记录，默认复用归档产物；不要每次重登重建。若确实重建，源码、编译器、产物SHA及CPU审计都更新，不能再沿用上述旧SHA。

```sh
sh /Users/kemi/coding/xyOnlie/tools/legacy-dynamic-trace/audit_pentium2.sh \
  <injector.exe> <input.dll>
```

必须得到 `PENTIUM2_OPCODE_AUDIT_OK`。这只证明CPU兼容，不代替动态门。

控制DLL除了输入钩子还含已授权实验的显存查询兼容逻辑；它不是纯只读观察器。本轮诊断版跳过Winsock IAT段，见断线分析。不要把控制载荷效果写成正式客户端算法修复。

## 5. 向真实XP投递，不走错误SMB主机

复用已验证exact-PID工具盘通道。先用status获得VM PID，再检查光盘：

```sh
<已准备的86box_trace_media工具> <当前VM_PID> 'XP SWDOL Voodoo3' status
```

工具源码在 `xyOnlie/tools/legacy-dynamic-trace/86box_trace_media.swift`，其运行必须匹配真实PID与窗口标题。不要把QEMU QMP脚本用于86Box。

工具盘只放本轮必要文件，手动执行，无AUTORUN open：

```text
INPUT.DLL  = 成功xyol-input.dll
INJECT.EXE = 成功xyol-injector.exe
RUN.CMD    = 有界复制和附加脚本
```

制作新的ISO、回读盘内字节与SHA，再用既有exact-PID挂载方法热换。不要编辑运行中虚拟磁盘，不重启VM，不重写网络。

XP内先 `tasklist /m xyol-input.dll`：已经加载则复用，不复制覆盖、不重注入。确认只有一个符合本轮原版EXE身份的游戏进程后再执行首次附加。

第一次复制脚本的基本形状：

```bat
@echo off
if not exist C:\xyol-tools mkdir C:\xyol-tools
copy /y D:\INPUT.DLL C:\xyol-tools\xyol-input.dll
if errorlevel 1 exit /b 1
copy /y D:\INJECT.EXE C:\xyol-tools\xyol-injector.exe
if errorlevel 1 exit /b 1
fc /b D:\INPUT.DLL C:\xyol-tools\xyol-input.dll
if errorlevel 1 exit /b 1
fc /b D:\INJECT.EXE C:\xyol-tools\xyol-injector.exe
if errorlevel 1 exit /b 1
C:\xyol-tools\xyol-injector.exe
type C:\xyol-tools\xyol-injector.log
type C:\xyol-tools\xyol-input.log
```

D盘必须先由当前XP实际目录确认，不照抄盘符。不要把首次部署CMD当作重登CMD反复执行。

## 6. 连接与第一条控制动作

宿主先开单一输入监听：

```sh
python3 /Users/kemi/coding/xyOnlie/client/tools/dinput-proxy/send_input.py \
  --listen 192.168.128.1 --from-top-left --dx 260 --dy 145 \
  --click --hold-ms 200 --settle-ms 1200
```

再从XP交互桌面执行首次注入器。成功本轮返回 `connected: 192.168.128.1:<临时端口>`，并实际从主菜单进入账号页。这里的peer为SLiRP映射，不代表服务端机器或游戏PID。

独立读取 `xyol-injector.log/xyol-input.log` 中的进程与控制就绪标志；不能只因TCP accept成功就写UI已响应。操作成功后复用同一载荷，不加第二套launcher。

## 7. 不做的事

- 不使用今天误投向Server2003的 `/private/tmp/deploy_xp_dinput.py`。
- 不用原服Administrator身份来推断XP交互用户/会话。
- 不在当前PID上重复LoadLibrary以修复缺失功能。
- 不把失败的MAGIC.VBS、UI.EXE、UIAGENT.EXE试验作为默认成功流程。
- 不为了这一轮操作改系统脚本宿主策略、放开权限或重启原服。

成功默认路线仍是已归档的DirectInput单连接连续鼠标序列与普通定向键盘登录。
