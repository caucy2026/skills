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

## 后续实测边界（2026-10-14）
77正常持有摇杆HOME返回已核到idle、位置稳定与移动提交0→0，水平双指返回也有无intent录像后才采快照；均只作为各自子例。极低帧率组件检查另发现LegacyWorldTickScheduler原积压>30退回1策略：1Hz十秒213 world steps，其余2–144Hz所测节奏303，presentation始终600；该边界仍未修，不能称全部FPS速度通过。exec-out PNG观察超时后，经同ID/串口恢复，普通shell screencap写唯一设备临时文件再adb pull已获得完整PNG；仅证明此恢复路径，不能唯一归因为网络或将原失败补成通过。

## 2026-10-15 本人分享列表：必须覆盖真实平台通道
该PAD的SWDOL79 FakeHttp分页测试通过，但实际FrameworkHttpsTransport拒绝包含问号的endpoint，GET cursor放URI导致真机无法读取。成熟纠正是在同认证业务入口传JSON POST cursor/limit，服务端严格类型/范围，不放宽通道路径安全规则；80同源候选在真实账号信息页观察到本人码、默认折叠、展开“暂无分享账号”，与后台只读索引0条一致。普通刷新、HOME/Launcher同PID返回及再折叠实际审图已观察。空列表不证明非空账号、两个角色槽、姓名等级或长列表滚动；不制造生产注册/绑定迎合验收。
后台Linux构建完整源码/Object/ASM闭包，测试超过工具调用预算时先核原进程是否终态，再用已有脱离执行方式保存log/exit，不能超时重启重复测试。仅切SWDOL HTTPS、备份SQLite和原unit，按实际映射核native库；game及HBBC/HBBS/HBBR比较PID/起时必须一致。部署与真实业务/客户端/全部地图/发布分开。详情仍引用SWDOL现有运营管理主文档与迁移账，不把该实例过程推广到其他App。


## 2026-10-15 IME必须核真实按键与未遮挡字段

`mInputShown=true`、`mIsInputViewShown=true`只证明系统状态，不能替代实际键盘、字段可见和真实屏幕按键提交。81曾仅有底部工具条；同输入法的普通Settings EditText实际点击可显示完整键盘，回游戏旧81也能显示，不能据此认定隐式请求是唯一根因。对照只能取消，不保存系统名称/设置，不切换默认输入法迎合验收。

82完整键盘遮住游戏字段；WMS应用window仍1920×1280且IME占据下半屏，adjustResize标记不证明NativeActivity taken surface尺寸已改变。83在Android30+按真实IME Insets/可见区域约束所属window，复用既有native重绑/4:3画布与指针映射；关闭输入及pause/resume恢复原height/y/gravity。显示请求仍严格限定用户点击、foreground和focusToken，不用SHOW_FORCED或启动逻辑焦点弹键盘。

用同一完整签名候选检查：启动不弹→点击完整键盘/完整字段→真实屏幕非私密字符→屏幕退格恢复原值→Back全屏→HOME/Launcher隐藏与再点击；再核正常登录、角色、入图、世界聊天IME画布、取消后的摇杆和键盘开启时HOME。窗口刚开始动画的第一张图可能仍旧布局，先核当轮实际窗口/稳定画面，不能靠重发输入。83有限实测证明账号字符提交/恢复、画布及返回；世界草稿字符可见、中文组合、全部业务字段、锁屏、跨图、各OS及长期性能仍未完成。

私有完整证据保留在项目唯一迁移账关联目录，不上传账号/密码/数据库/原始系统窗口日志到技能库。83完整APK SHA与输入身份见该账，主线修复提交67ed5fe0仅Android窗口接缝及说明；发布资格仍BLOCKED。


## 2026-10-15 世界草稿84–87失败与回滚边界
84普通Java TextView草稿不可见、gfxinfo Java绘制0；85附属窗口字出现但位置错误，86实际窗口尺寸接口后仍有父子窗口偏移，87原点调整造成纵向压缩，四者均FAIL。不能把“字出现”当原4:3画布/坐标/输入通过；不能仅凭gfxinfo0泛化所有Java控件不绘制。WMS frame、Decor/content尺寸、ANativeWindow buffer、EGL drawable、bgfx reset与present viewport、触摸原点和附属窗口坐标需在同一窗口代次关联，先有界判别再编码，不靠猜偏移反复连编。
全部本轮实验代码已选择性反向撤回，保留原先同事改动；设备已不清数据回滚完整签名83，installed base SHA独立匹配60ab5208b1ab2b1a9bb2ac71cdcd64d27a34130bc51061adddeb3bdfaa71d7fa。原失败、源输入和回滚证据仍在唯一迁移账，主线记录7d0d7d62，草稿显示与其他10组目标未关闭。键盘Back后的窗口变化期不要立即套用旧坐标点退出；先核稳定画布/实际系统菜单，再正常登出并审图，不把脚本执行完当退回登录。


## 2026-10-15 长后台、动画与监控续证

95完整新签名包同一PID的登录页/角色页/城市世界HOME2秒返回及世界实际114.647秒后台返回，分别有真实Launcher、独立返回录像和其后更大id的ready/idle快照；世界位置保持，恢复后正常摇杆/UP移动及停止已观察。仅关闭这些有限案例，不转计锁屏、进程回收、其他时长或全部生命周期。入图及map1→0→1转场的原圆点在实际4Hz取帧中亮点相位连续变化；各视频仍绑定同包与当轮服务BIN，不用像素hash变化单独证明动画正确，更不代表全部过程/跨FPS速度通过。城市返回仍24.9–27.8FPS，1Hz积压反例继续OPEN。完整身份/原视频只引用项目唯一迁移账95章。

性能采样须对齐场景事件和计划总时长；本轮主监控600点1311秒、退出补采60点，均有真实终态，但中间约55.3秒缺口必须保留。不能把两段拼成全程无间断。PSS原值为KiB，271151KiB约264.8MiB；低频内存快照不证明native/GPU全部所有者或无泄漏。SF --latency返回的是末尾present窗口，连续查询最新时间戳不变时为陈旧窗口，不能把其FPS当后台仍在绘制；保留原始三列时间、无效sentinel和新present判据。

退出动作前态必须取实际执行录像的首帧，不能只依赖较早菜单截图。95首次退出录像起始时系统菜单已经关闭，随后native日志虽证明点击坐标送达，却不能证明命中了退出按钮；归为前态不成立/退出未验，不擅自修命中框。另有晚于该点击约140秒的非本任务摇杆轨迹，不能倒推它导致先前15秒退出失败。对照本任务动作账、同PID SWDOL-INPUT的时间/seq/Down-Move-Up及完整视频，分别记录真实控制冲突与产品缺陷；发现未分配操作先协调设备归属，避免继续触控或强关正在被使用的实例。


## 2026-10-16 Android正常退出接口与认证拒绝
共享前台Cancel/Quit必须沿LegacyFrontView.intent→providers.quit→Android平台finish真正关闭所属Activity。99补齐AndroidWorldServices此前漏接的provider，正常登录页Cancel以及认证拒绝Return后Cancel均已实机回读Activity消失，未force-stop。Android仍可保留cch-rec缓存进程/空Task；PID仍在不单独证明界面没退出，也不为制造“退出”不断杀缓存进程。游戏内登出回登录和应用Quit分别验，不混成一个结果。
现网master -10映射的“当前区域正在保存资料”是通用失败提示，不据中文推定真正保存或角色被占用。先核本轮现网PID/exe/SHA、认证worker结果、lease及节点；lease inactive和节点active也不等于认证完整健康。不为过验收删lease/写DB/循环登录；服务拒绝时世界/HOME脚本不能计入世界通过。具体99包与证据只引用项目迁移账，不固化为下轮版本。
本机adb.session_open的get-state心跳曾正常而端到端shell仍超时；仍须实际shell读回，不能将心跳当通道稳定修复。仅回收本任务session和serial，真实失效时按同ID重新取地址；本轮工具返回transport=relay是实际记录，须结合身份/授权/实际调用核查，不假写p2p。


## 2026-10-16 同PID重开后的诊断序号重置
101实测正常Quit使Activity销毁后，Android可保留同PID；再次启动的新native宿主diagnosticSequence从1重置。旧采集器只接受id大于前次最大值，因而对真实新记录误报超时。成熟纠正：请求前保存同PID epoch格式日志的完整记录集合，请求后仅消费未见过的带时间戳记录，再按本次id重组并核part/count/bytes、请求期间所属PID和实际页面；pidof也加有界超时。旧超时保留，不清logcat制造通过，也不要求重启健康游戏。101同PID重开实际新id1（角色页）、随后id2（世界ready/idle）已核；序号不再作为跨Activity生命代次的单调身份。返回后的独立录像/画面仍须先于诊断intent，不能让该工具触发的生命周期成为恢复证据。

## 2026-10-16 旧世界画面不等于运行时仍存活
102在摇杆HOME后发起转场，出现SWDOL-MOBILE shared frame: singular camera bridge；宿主删除runtime但PID和旧GPU画面仍在，后续快照超时。先读同PID的共享frame异常、当前runtime/准备状态与新快照，不将此类失败归为ADB不稳，也不以旧画面或输入脚本结束计传送通过。已失效界面无法正常退出时，归档后只关闭所属故障实例，明确记录force-stop而非正常Quit。
103的有限修正是首个正常世界步前继续动态准备画面，等待ACT资源、class10锚点及相机同时就绪，不补造ACT/RNG步。实际摇杆HOME后0→1→0、两段圆点连续相位与新权威地图快照已核；仍不代表全部地图、低物理FPS速度或最新同源服务端通过。运行时与后台资格分别记录，未通过后台不切生产。


## 2026-10-16 104同包低呈现FPS验收入口

先核实际包/源码身份。104的MobileActivity仅在初始swdolTraceMovement=true的会话接受swdolAcceptanceFrameDelayMs（0—1000）；用现有singleTop intent显式设置1000可测到约0.97—0.99个新增present每秒，0恢复正常。普通启动实测忽略该参数、约60FPS。它是有界trace验收控制，不是系统屏幕Hz或产品FPS设置；其他版本不假定已有此能力，结束恢复0并正常Quit。

SurfaceFlinger旧128帧窗口会混入前一模式，按上次最大present时间筛新增记录，再核新帧间隔，保留原始三列和sentinel。CPU仍按进程/全CPU ticks，PSS低频取样。断链前后分段，offline和device not found均不算游戏黑屏；原ID重连核新serial/同型号/包/PID/实际页面后续做，不把get-state当端到端稳定。

104正常约40FPS与约0.99FPS的一个同起点、暖定方向、nominal4秒恒定摇杆案例得到相同终点；只作为该案例，不能覆盖全部输入相位或稳态速度。快照intent会触发生命周期及取消输入，所以先显式UP并保留独立停止录像，不能中途发快照后声称按压未被打断。当前控制角色在统一运动所有权前/键盘的旧时钟仍有213对303的组件反例；不能只暖定摇杆后测试便报所有动画一致，后续需覆盖该分叉及无取消的观测。


## 2026-10-16 Linux资格与本地所有者锁的实测入口

原数据根、Object/ASM和测试模块分别显式绑定：CMake的SWDOL_TEST_LEGACY_SERVER_ROOT指向实际只读mlzo/表根，SWDOL_TEST_OBJECT_DBF指向冻结Object及同目录完整ASM，SWDOL_PURE_WAITING_MODULE/OBJECTS绑定同源模块/表。不能把未投影的相邻xyOnlie目录或Mac绝对路径缺失当业务失败；也不能跳过测试写通过。packager同时收server/deploy/*.py，启动器须在归档内，和Object/ASM精确大小写、逐字SHA一起验证。

LocalServiceOwnerFence在Mac继续gethostuuid，原生Linux读取有效持久machine-id并缓存进程身份；不打印实际标识，不用随机值/hostname兜底，Android不走此分支。保留0700目录、0600锁、设备inode、SQLite HAS_MOVED、O_NOFOLLOW/CLOEXEC及持有fcntl描述符，不unlink锁。用exec后的独立进程验证真实互斥，再验证重复申请失败不释放旧锁、释放后重取、路径/目录/数据库替换及权限/符号链接拒绝；实际服务UID另测。root单例通过不等于服务资格。

实际104的共享权威、世界关闭、计费及菜单18项与HTTP7项通过；它们是该版本范围，不是以后固定绿灯。锁还被邮件恢复线程使用，补邮件数据库、两库领取冷恢复和迁移检查；只读核配对及当前route，备份world/auth/sms/mail，不因代码更新自动激活迁移。只切游戏时四运营BIN即使编好也未上线，必须分别记录。

切换前核零所属连接/活跃角色、当前exe/SHA与unit，正常停旧节点、验证退休，再用新nonce启动和核续租；不清lease、不回写健康。回退只撤自己的精确dropin并回旧BIN，数据库不覆盖后续业务进度。构建等待核原PID及终态，不重复开编译；云端文件传输完成后再开始连续PAD验收，通道断开按status/实际shell恢复并保留监控间隙，不能猜原因。


## 2026-10-16 有界被动采样与编辑焦点回归（105/106已实测范围）

动态ADB端口每次由ID2315316040重新取得，不能固化下文历史端口。普通快照am start intent会触发pause/resume/resize并取消持有输入，不能在按键/摇杆保持期间调用后再称按压连续。105新增既有trace会话限定的swdolAcceptanceSnapshots预算0—30，前台最多约1Hz沿已有JNI采样；一次arming intent只在实验开始前发送。收集器须等am start实际返回并写armed回执后再按压，保存按压开始/结束时间；期间只读新日志。用epoch完整记录集合区别新样本，按id/part/count/bytes和同PID组装，不仅比较旧最大id。预算结束或会话关闭后停止；正常性能评价不使用强制低FPS压力样本。

同点正常与约1FPS比较应同时记录世界步、控制BODY调用、实际位置和run/idle，不把调用次数当每次ACT换帧。106键盘/摇杆稳态约12单位/世界步的有限样本通过，但按压起止相位和全部动画仍未验。run而原地先核原入口与碰撞；暖定摇杆后才测不能覆盖闲置/键盘所有权。按公开W键的shell辅助器必须UID2000、主屏0、有界保持、finally发UP；不接收密码或将账号凭据放argv。

隐藏编辑器无编辑任务时也可能占焦点。dumpsys activity top应先按所属TASK/Activity块定位，再看该块的mHasWindowFocus和Sink焦点标志；不能选到包含包名引用的别家窗口。106明确编辑时才启用Sink焦点，结束/暂停撤销并归还游戏内容视图；正常编辑、退格、Back、GM提交和键盘/摇杆所有权切换分别验。只有IME工具条不能报完整软键盘通过；ASCII不能报中文组字通过。

HOME返回先拍独立录像再发诊断。即使ready/idle、pending0、位置稳定且场景继续绘制，角色被前景物体遮住也只证明状态/输入释放，不能记角色可见或原版相机匹配。城市106实测28.8—29FPS仍低于30；两个混合场景PSS监控段不得拼成无泄漏证明。跨图准备圆环须从同一原视频连续解码并人工核亮点相位；106两次各7/14份相位不同仅证对应跨图，不能推及所有过场。私有快照、账号材料、完整日志和原录像保留项目证据目录，公开技能只存方法及适用边界。

## 2026-10-16：GM输入的远端shell转义与真实退格

外部ADB即使用参数数组，`adb shell input text ~`仍会经远端shell解析，单个`~`会展开为该shell的HOME（本轮为`/`），因此草稿实际是`/Zone...`，不能提交后当GM权限/地图错误。逐字符输入公开GM命令时，把远端命令构成`input text `加该字符的POSIX shell quoting（Python shlex.quote）；空格用真实Space键。不要用JSON.stringify代shell quoting，不把密码放argv。先核完整公开草稿，再Enter；本轮~Zone2/原Plot5884落点量化的实际转移已核Zone/ACT2、ready/idle及地表图。逐字符路线是有界操作恢复方法，不证明原批量输入或真实软键盘已修。

清草稿不能假定Delete成功。本轮114把token-bound物理Delete送进无编辑分支的世界快捷键，vp未删除会污染后续命令。116从同冻结完整构建，实际两公开字符→两Delete→空草稿已看前后图，复用既有eraseNativeText消费者；旧token/no-token/Up边界有实际方法组件反例。软键盘显示仍OPEN；系统inputShown=true不当键盘可见。大PNG传输超时后，先核远端完整文件，只重拉该文件，不重发游戏动作；本轮4MiB PNG约53秒，15秒回传预算不够，必要用有界75秒传输进程并轮询同一handle、继续独立工作，不能把不完整本地图当证据。
