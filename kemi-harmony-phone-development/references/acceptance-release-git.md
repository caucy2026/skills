# 精确候选验收、上架与Git备份

## 基本按钮与连接矩阵

先核验已安装候选、实际前台、屏幕/折叠尺寸、设备身份、登录状态和远端测试对象。建立独立测试窗口才可输入，不能在同事工作窗口做Delete/Enter、重启或锁屏。用户限制“输入由用户验证”时，记录人工结果，不自动发送文字。

- 主页四导航、账号入口、最近设备、退出；客户端页共享PAD布局、缓存立即显示、下载与哈希校验；设置弹窗可开关/取消；关于本地简介和后台图组离线回退。
- 连接保存设备→实时画面→显示菜单适应窗口/质量→键盘开关→鼠标/触屏模式→快捷面板→更多刷新→工具栏收起/展开。
- 更多菜单按远端平台显示账号/密码、重启、锁定、刷新等，打开菜单不能宣称已验证危险动作；不在承载工作的机器重启。
- 断开取消保持会话；断开确认回主页；退出取消保持；退出确认回系统桌面；原包重新启动保存设备无需再次远端密码。
- 折叠/展开、横竖屏改变后重新读取布局，不套旧坐标。统计显示FPS不是输入命中证明。

## 百次设备切换

脚本参数均为现场值，候选文件由本轮安装记录确认，脚本只校验给定文件哈希，不自行证明手机上装的就是该文件。

```bash
python3 -B '<skill>/scripts/switch_devices.py' \
 --hdc '<既有hdc>' --target '<授权IP:端口或USB键>' --expected-model HOP-AL00 \
 --candidate '<已覆盖安装的signed.hap>' --sha256 '<精确SHA256>' \
 --peer '<授权Mac标签1>' --peer '<授权Windows标签>' --peer '<授权Mac标签2>' \
 --count 100 --out '<新的私密运行目录>'
```

起始peer必须不是当前已选中设备；检查每次目标selected=true、无连接等待、没有权限/连接错误、非整体空白帧。竖屏每次切换后滚到设备区域再判断selected。所有截图保留并做联系表逐张核对，无串屏及整屏黑屏。图像方差只能排除某些空白帧，不能判断图中文字/目标内容或全部像素正确。不要沿用旧landscape硬编码crop。

旧脚本第一次等待超时的原因为新页面重置横向工具栏滚动，第二Mac实际上已有H265画面；这是前置条件失效，保留记录，修复后新run重测，不隐瞒首轮超时。

## 不可被控验收

1. 编译包只有INTERNET、没有被控extension/background；源码被控启动、入站路径、注册禁用。
2. 实际远控状态下按App UID/PID查/proc/net/{tcp,tcp6,udp,udp6}，确认无被控LISTEN；检查默认直连21118拒绝。
3. 对项目现有服务器的在线注册与PunchHoleRequest需要授权涉及的设备ID/目的地。已授权的同对象测试可复用；不能把新账号或新服务器泛化为已授权。
4. 已验证方案：对照Mac online=true、手机=false，向手机发标准入站请求返回ID_NOT_EXIST、无socket_addr；保存协议证据不发送密码/桌面/文件。
5. 客户端页可开8686只读下载服务，离开页关闭；这是文件分发，不是被控服务。运行时证据仅证明当前配置范围，不承诺未来任意漏洞不存在。

## 签名/上架边界

调试证书/Profile和发布证书/Profile分开，Profile改名不改变类型。最低API23/arm64仍是兼容条件，不能“任何鸿蒙手机都能安装”。正式APP包、签名验证、覆盖升级、隐私资料、应用图标系统圆角遮罩、截图和审核状态需要当前实际证据。

本轮实名认证故障：当前“撼地神牛”账号显示体验入口；点击个人开发者下一步才出现“身份信息已被其他账号认证”提示。用户口述已认证不能替代账号发布资格核验。官方账号查询涉及实名、证件照片及邮件，由身份持有人按平台流程完成；不从浏览器秘密/Cookie猜登录账号，不代为提交身份证材料。开发者账号不同于App的KEMI账号。

公开发布使用适用public-app-distribution技能，并浏览当前华为官方要求。上传、审核中、审核通过、公开下载分别记录，不把GitHub源码push算正式上架。

## GitHub和本地备份

仅精确鸿蒙独立分支推送，不合并main或改默认分支。不要git add -A：AGC图片、远端截图、signing材料可能未跟踪。逐路径添加源码、测试、文字报告和此技能。

本机global Git曾将HTTPS重写为SSH；已验证的命令级覆盖：

```bash
git -c 'url.https://github.com/caucy2026/kemi-remote-office-harmony.git.insteadOf=https://github.com/caucy2026/kemi-remote-office-harmony.git' \
 -c credential.helper= -c 'credential.helper=!gh auth git-credential' \
 push https://github.com/caucy2026/kemi-remote-office-harmony.git HEAD:refs/heads/harmony-phone-pad-parity-20261001
```

只在该仓库授权范围使用，不改全局配置。用 `gh api repos/<仓库>/branches/<分支> --jq '.commit.sha'` 核验精确远端提交，检查default_branch仍main、private仍true。不要把tokens输出。

本地 `git bundle create <新的备份目录>/harmony-phone.bundle --all` 然后verify，保存源码提交和signed包哈希；不得覆盖旧包。源码和私密签名材料分开备份，代码bundle不包含忽略的签名密钥。

技能追踪源在鸿蒙仓库 `client/skills/kemi-harmony-phone-development`，安装到实际CODEX_HOME/skills（本机~/.codex/skills），修改后验证再同步两份。安装技能不修改应用或系统授权。
