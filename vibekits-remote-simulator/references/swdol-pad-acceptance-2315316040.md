# SWDOL PAD 实机验收与同事接续

2026-10-14实测方法；这是设备/应用实例，不是其他设备默认配置。当前用户授权的PAD仿真ID为 **2315316040**，已核KEMI Vibe Pads S1、Android普通shell UID2000、默认主屏逻辑display0、1920×1280。ID不代替设备首次同意、仿真开启或ADB授权；同事先确认本轮分配和应用/账号无人占用。

## 连接和身份

Harness内使用registered simulator connect/status/catalog/call。外部Mac控制器沿本技能的tool-contract及mac-pad-remote-adb，通过现有invoke.rb本地loopback桥连接同routingId。核connected=true、p2p_or_relay、adbReady和本次动态adbSerial，再用独立ADB server连接、get-state和getprop读回型号。历史127.0.0.1临时端口均失效，不硬编码端口，不通过远程桌面或PAD SSH猜路线。

connected/adbReady不等于当前ADB实际可用。已观察同ID status仍connected但shell offline：保存错误，只disconnect本任务serial并connect当前status返回serial，实际shell/PID/Activity回读后续做；不kill-server、不重启PAD/adbd或宿主。截图超时是观察失败，不直接称游戏黑屏；已发出的输入不盲目重发。操作异常立即回查本页母指南，4分钟/5分钟仍无有效证据停止同条件盲试并记录首个差异。

## 完整包与正常操作

从最新本机主线及授权dirty冻结所有客户端/共享/服务端/第三方/工具输入，逐文件锁SHA；完整构建、稳定签名、保留原资源索引和数据，不用旧core重包。上传大包可用项目既有apk_byte_delta精确父→目标运输，设备parent/target SHA和完整签名APK一致后才普通pm install-r；随后独立核installed base.apk完整SHA、版本、PID、Activity和屏幕。差分运输不是局部.so安装或行为通过。保留当前包和一个回滚包，不pm clear/uninstall。

当前包名com.swdol.client.nativegpu，实际Activity com.caucy.swdol.mobile.MobileActivity；新环境仍核manifest。800×600逻辑画布按当次实际canvasViewport逆映射输入，键盘/系统insets不可猜。密码只用已核权限的stdin标准按键帮助器与私有reader，绝不放ADB input text、argv、环境、日志或Git；公共演示文本不推广到私密凭据。已有APP登录成功后的安全存储可用于正常UI回填，不写库伪造认证。

## 后台、动画与输入取消

先锁程序/资源SHA、PID和唯一Activity/Task。先启动screenrecord并确认活跃，再执行正常登录、传送、HOME或手势；主屏screenrecord默认显示在此PAD有效，--display-id0曾被拒，input与screencap的逻辑/物理display必须分别实查。HOME返回使用实际Launcher图标/任务切换，不用am start诊断intent代替。

完整快照仅在启动时开启swdolTraceMovement的候选上可请求；核同PID更大snapshot id、完整part/count/bytes，再解码。trace=false默认进程不能假装快照可用。诊断singleTop intent在此ROM可能触发pause/resume/resize，所以取消/恢复先保留无intent独立录像，至少观察返回后再请求状态；诊断不能成为“取消发生”的原因。

动画按单调经过时间推进，FPS只影响采样。15–144Hz时钟性质测试不代替物理不同FPS的ACT/行走进度。静止截图不证明等待/入图/传送/返回动画；同包录像检查实际帧变化与返回输入。持有摇杆按HOME必须先证明已在移动，再核返回后的轴/临时目标/行动与发包停止；76曾位置稳定而状态run、移动提交继续增加，不能用“位置没变”误报释放通过。多指、键盘、窗口拖放及锁屏各自保留未验项。安全锁需设备正常授权解锁；屏幕提示或普通wake不证明凭据锁已解开。

## 性能与证据边界

测试期间持续采CPU/帧率，PSS/native/GPU内存按较低频率另取窗口，避免meminfo污染同一SF采样。CPU以进程utime+stime增量除全CPU jiffies增量，记全设备百分比及核数；换算单核百分比须乘核数并明确标签。SurfaceFlinger latency的0及9223372036854775807是无有效present时间，必须排除；不要全文件替换版本数字，曾把sentinel上限改坏导致伪低FPS。原始窗口保留，修正解析时保留旧错误值与纠正原因。换PID重绑采样，不混后台/旧缓冲与前台稳定FPS。

短单图PSS波动/回落不是无泄漏证明；1GiB登记不是全部RSS；需同包冷暖A→B→A、多地图/循环和长期趋势。源码、组件、真实UI、原版差分、性能、发布资格分别记录。当前已有正常HOME/传送/IME局部实测，但GM20图、全部UI、跨帧率物理速度和长期泄漏并未关闭。

本任务唯一当前账在SWDOL仓库document/Mac与Android统一bgfx仿真架构及迁移记录.md；按当前章节和实测制品接续，不复制历史PASS到新包，不接管同事已完成的装备/鸿蒙。私有原日志、凭据、数据库和截图不上传此技能库。结束走正常登出，核所属实例退出；ROM可能再创建无Activity的cached-empty进程，要与活跃世界区分，不反复重启或改系统预加载。只精确清理本任务可重建旧临时APK，保留输入、身份及原始失败/回归证据，最后释放本任务ADB和仿真连接。
