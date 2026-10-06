---
name: hbbv-server-build-deploy
description: 整理、测试、打包、备份和部署hbbv房间与能力管理服务器源码，保留服务器身份、设备授权和持久数据；不用于hbbc或RustDesk hbbs/hbbr发布。
---

# hbbv服务器源码交付

先读取目标项目AGENTS和本机环境规则，确认源码、部署目标与当前活动任务。源码包含server/、web/、contracts/、client/、quality/和docs/；运行入口、依赖及部署参数以当前源码为准。不要把网页更新可见当作Python模块已重载。

## 构建与验证

当前服务器是Python/SQLite源码运行项目，无需C/C++或Rust编译。使用Python3.10+专用虚拟环境；现场已验证Python3.12。在机器规定的构建目录创建环境，执行`python -m pip install -r server/requirements.txt`，保留锁定依赖，不顺便升级。当前锁定jsonschema4.26.0、cryptography50.0.1，以实际文件为准。

设置TMPDIR到项目专用可再生目录，`python -B -m unittest discover -s server -p 'test*.py' -v`。针对修改运行必要测试；真实HTTP测试需要允许本地监听。源码测试、合成100节点并发和真实设备验收分别记录，不能互相代替。当前新增发现/邀请相关27项通过，不等于完整长期稳定或生产部署通过。

## 启动

通用入口`server/app.py`，先执行`python -B server/app.py --help`核对参数。回环开发：

```sh
python -B server/app.py --data-dir /private/hbbv-data --password-file /private/admin-password.txt
```

远端HTTPS按实际目标替换参数：

```sh
python -B server/app.py --data-dir /private/hbbv-data --database-name integration.sqlite3 --host 0.0.0.0 --port 21122 --public-host cluster.example:21122 --tls-cert /private/tls-cert.pem --tls-key /private/tls-key.pem
```

上例是参数模板，不能直接启动或据此宣称目标已部署。新数据库默认hbbv.sqlite3；迁移现有验收数据库时显式选择integration.sqlite3，避免启动空库。密码文件只初始化新账号，不用于覆盖已有密码。现有服务身份、任务签名私钥、设备记录与授权须一起保护；不打印私密材料。

`server/run_local_https.py`是当前Mac双监听验收入口，具有ORICO挂载检查、既有数据目录、专用证书及TLS1.2现场兼容设置；不能原样搬到Linux或把本机限制变为通用要求。生产使用通用入口并按真实环境验证TLS与服务管理。task-execution-scope省略时不启用签名任务上下文；配置范围不等于每设备已获授权，不降低签名租约、本地grant和操作permit门禁。

## 备份、部署与回退

用户已要求只备份main时，沿用项目成熟独立索引备份脚本，普通推送并核验远端树，冲突按双方内容主动解决；不force、不reset、不覆盖共享未提交改动。此项目归档在私有仓库priv的hbbv/前缀。备份源码和说明，不备份数据库、密码、令牌、TLS私钥或设备私钥到Git。

部署前按kemi-server-ports查目标唯一台账，核验listener与已有预留；不得操作hbbc/hbbs/hbbr。冻结通过的源码哈希，私有备份现有SQLite及配置/身份，确认无活跃租约、外部操作或升级事务。沿既有supervisor一次正常部署，记录意图防止重复重载；观察超时不代表进程已停止。

部署后核验实际加载源码、HTTPS证书、原serverId、持久房间及成员、认证隔离、管理MCP目录和逐台客户端心跳/工具。先一台再批量切换；错误保留原配置和数据库回退点，不用新身份或空库掩盖失败。全局接入协作技能的完整真机场景仍待验，不把本技能当作已通过证明。

## 当前项目入口

本机源码/README与远端准备记录位于项目hbbv；具体本机路径和端口通过kemi-server-ports本地索引获取。当前生产21122是设计预留，实时占用和公网部署待核验。参考项目docs/REMOTE_DEPLOYMENT_READINESS_2026-10-06.md与86_SERVER_INITIATED_ROOM_INVITATIONS_2026-10-05.md；源码变更后重新核验相应入口，不照搬历史状态。


## 已验证部署路线（2026-10-06）

以VibeKits工具为主：remote.list_profiles确认已保存host/port/user及主机指纹；remote.ssh_exec执行有界命令，remote.sftp_upload上传精确文件且overwrite=false。open_interactive返回导航器未连接时，先在VibeKits开发工具打开SSH/SFTP工作台，不换成外部SSH、不绕过主机指纹。保存凭据成功不代表密码认证成功；认证失败优先读取服务器限定长度auth.log，区分Failed password与Accepted password，不输出秘密。

本次实际目标：/opt/vibekits-group，域名kemi-chat.newlinksz.com来自RustDesk部署源码并与服务器hbbc public_base_url及证书SAN一致；21122/TCP由统一台账预留，已检查ss、全部socket与Docker映射无冲突。其他环境从各自台账发现，不照搬此地址。

冻结源码server/web/contracts及逐文件SHA清单；SQLite在线backup生成一致性迁移副本，上传后核对SHA和quick_check。原task-signing-key.pem是服务私钥，迁移前必须满足工具审批对材料与目的地的具体授权；拒绝后不得改名、打包或改工具绕过。授权后限制600，只供原服务身份使用。设备私钥、密码与令牌不打印、不写Git。保存原服务UUID、原成员审批和同一签名公钥；不能让启动入口在缺原私钥时生成新身份冒充迁移。

专用venv使用锁定requirements；长安装用后台原PID及限定日志观察，不重复安装。远端27项邀请/管理MCP测试已通过。独立vibekits-cluster.service以通用app.py启动，显式database-name=integration.sqlite3、原数据目录、可信HTTPS域名及原执行范围；使用Umask0077、NoNewPrivileges、PrivateTmp和只读系统保护，仅数据目录允许写。systemctl daemon-reload只登记单元；启动前核对端口，启动后确认原hbbs/hbbr/hbbc的PID及active状态保持。

设备迁移使用cluster.status保存安全摘要，然后cluster.configure(serverOrigin、trustedHosts、trustedCertificatePem、serverSimulationId)。公网受信证书不带旧自签CA。地址改变后首次rooms可能只返回“发现中”，等待原异步同步再读取；不要因瞬时空房间重复申请。155真实迁移已保持原UUID、安装身份、批准成员并恢复实时入房；其他设备与云端心跳须分别核验，不能凭数据库历史批准称全部在线。仿真连接与房间心跳分别验证，离线桌面不得恢复。

公网管理台使用原管理账号及浏览器正常认证，不将令牌放URL。展示给用户前核验真实页面；公网部署、基础入房和27项隔离测试都不等于完整任务执行、评分或100台长期协作通过。
