# 原版两数据库：用途、查看与连接

## 真实拓扑与入口

crossgate是SQL Server账号/计费/会话入口；MySQL swdol是角色/世界存档。Master、地图和Chat的游戏侧请求经DataCenter访问MySQL；JoyPark认证组件另用SQL Server。资料114旧“唯一数据库客户端”只指游戏核心程序，不能扩展到完整部署。

历史测试Windows地址192.168.128.2，端口3306/1433只是历史配置，须核实际进程与当前服务。20260930纠错：7000属于ChatServer，7888属于JoyparkLoginServer；不能只按端口猜服务。读取dataCenter.ini的Settings/DBHost/GameDB/User等定位MySQL配置，不读取Master配置猜MySQL；JoyPark配置另定位SQL Server连接。包含外层引号的旧连接串需按实际配置解析，不能猜口令。

已知Windows私有凭据入口 /Users/kemi/.codex/private/swdol-winserver/auth_reader.py，函数load_authorized_password只允许既有测试目标；传给SMB/现有执行器，不打印。/Users/kemi/.codex/worktrees/5ff5/xyOnlie/server/WINDOWS_TEST_AUTH_INTERFACE_20261001.md记录来宾osql -E成功；这是Windows集成认证，不证明远程TDS或SQL用户认证成功。

SQL Server成熟路径在授权来宾里用osql -E -S 127.0.0.1，先有界执行SELECT 1，再查crossgate元数据。localhost曾超时，不能盲试远程TLS/重复重启。实际查询执行器/二进制路径、当前配置和成功回执必须交接；本技能不编造一个通用在线MySQL客户端路径。

## SQL Server crossgate

先在已验证执行器使用 SELECT DB_NAME(), @@VERSION；USE crossgate 后用 sysobjects/syscolumns 等当前SQL Server版本支持的目录核表列。现代 sys.* 目录未确认版本前不用。用实际参数绑定，不拼账号输入，不调用会修改状态的存储过程来当只读查询。

|对象|用途及查找列|边界|
|---|---|---|
|Member_Data_Table|serial_number账号键、userid登录名；chargtype、point、last_point、期限、login_state及失败次数|pass禁止输出；nickname不是角色名；point是float，不能无合同改成游戏金币|
|Member_Login_Table|账号serial_number/userid，login/logout时间、目标服务器路由、process_state|IP/路由值只私有窄查；1900-01-01 logout哨兵表示未退出，不等同角色仍活跃|
|Banned_User_Table|封禁原因/时间/计费类型审计|不导出其他账号/GM信息|
|Suspended_User_Table|暂停视图|精确列型/完整枚举仍须当前schema|
|ISP_IP_List_Table|IP区间与约束|不是角色地图坐标；保持个人数据私有|

原脚本：process_state1活动/待处理，2是特定释放过程结果；serial_number%4是分片视图，不是四个独立物理库。Member_Query_SP用于认证/点数，Insert_Login_SP写会话，退出/计费/释放存储过程均有副作用，不能为修登录随便EXEC。

按精确userid窄查非敏感身份/状态列，再反查serial_number；同账号双读前后需当前会话印证。只插MySQL账号不能证明crossgate认证已登记。新账号注册须通过已验证正常入口或已授权双库流程，核失败回滚/重复/登录，不替换为手改login_state或点数。

## MySQL swdol

使用当前成熟只读执行器先 SELECT VERSION(), DATABASE(); SHOW TABLES; SHOW FIELDS FROM useraccount; SHOW FIELDS FROM charpool; 核实际表引擎、列序和字符集能力。用户值由执行器绑定；旧客户端不支持绑定时只接受已经验证的严格整数RoleID/账号键入口，账号文本不手工拼接。

|对象|作用|身份/数据域|
|---|---|---|
|useraccount|游戏侧账号驻留与角色槽|账号ID/名称、RID0..RID4、KeyID/State；当前schema确认具体列名|
|charpool|玩家角色主体|RoleID、AccountID、RoleName；种族职业性别、八维、HP/MP、Section/XYZ/Dir、Revive、EQArr、Mark/称号/Skill等|
|bodyitemstable|身体8顶层+每包保留子槽，共72物理槽|对象ID、Count、Version；实际包容量4/6/8按Object定义，保留8槽不代表8槽都可插入|
|bankitemstable|银行72槽|和Body分域；不能用查询得到数量代替正常银行权限|
|magictable|已学魔法100组ID/时间|不同于200字节Skill、快捷栏和持续状态|
|magiceffecttable|持续效果32组ID/值|重登截止时间/排序/控制还需动态合同|
|friendlist及实际分片|好友关系/分类/经验/备注|双向关系和模10分库依据调用参数；不猜表名后缀|
|guild*、givepool、资料/排行/消息表|社会与运营|赠送池8槽并有领取标记，不能只插物品行即声称邮件系统完成|
|npcpool、npcpool_add_on|NPC实例、覆盖|RoleID不是玩家RoleID；Object模板不是现场演员ID|
|corpse_base、corpse_bodyitemstable|尸体主体及72槽物品|type0x47、实例代次/归属/领取状态；查询主体存在不代表完整尸体|
|del_*、timeout_*|归档删除/超时转移|需要成组核父子表；不通配删除这些表|

schema确认后查询形状：SELECT RoleID, HEX(RoleName), AccountID FROM charpool WHERE RoleID=<bound_id>；由AccountID取角色列表，再用真实客户端列表确认槽。原DataCenter维护五槽，我方紧凑账户常规只有0/1，不能直接平移槽数。

charpool与四物品/魔法子表按RoleID窄范围双读，输出列名、NULL、原始Base64/HEX、每行SHA。MyISAM多表双读一致不是ACID快照；期间发生变化则重做/不可比较，不冻结共享服务器凑前态。

## 原保存与异常

原create插主表和四子表、逐域保存、多条UPDATE、好友/givepool操作无已证统一事务；原ExecSQL失败返回false，上层部分忽略。暂存SQL重放转.bak也不能证明执行成功。不能复制这些故障当我方兼容要求。

ConvertBIN构造SQL char(有符号字节...)，不是字符集转换。原SELECT *列序是ABI，我方新适配器必须具名列映射和参数绑定；不随意重排原表。

## 2026-10-04 SQL只读诊断回执

当前SQL Server 2008 R2 SP2 x86 Express。本轮5秒连接预算曾报TCP258/预登录响应延迟；30秒连接、10秒查询的SELECT1随后成功，来宾耗时8.91秒。这是诊断阈值证据，不证明XP卡住根因，不授权修改原服超时。连接超时、查询超时、缺回执分开记录；Query timeout即使EXIT=0仍失败。

使用已成功osql参数：-E -S 127.0.0.1。查询输出-o文件、stderr独立文件、cmd状态记录START/EXIT/END/DONE，启动器立即退出。派发DONE不等于查询DONE；SCM响应超时或只留START不证明SQL还在运行，须核当前匹配进程，不重复提交。输出占用时回读同一路径。勿把sqlcmd格式参数直接套给osql。

当前认证过程修改时间均8月14日；已查Master/Map/配置哈希未变。SQL sleeping/blocked0仅为采样时点；账号失败次数4无本轮时间因果，不当密码错误证明，不清租约。完整证据统一在/Users/kemi/Documents/Codex/server1003-evidence/login-change-audit-r278/result.json。

登录故障先读取实际部署loginserver.ini的LoginLogDir，不能只枚举core或log上层后声称无日志。本轮实际目录C:\swdol-server\log\login，有20261004日志；发现Member/Query失败、exception及timeout记录，后续目标登录result16的含义和请求关联仍未证明。原日志只留私有目录，报告仅时间、分类、码、SHA；不上传账号/IP原文。当前Joypark EXE b4398c…与已恢复原始快照相同。

已锁定JoyparkLoginServer b4398c…：成员查询入口40418c，异常日志串引用404381，404462向返回对象+7c写16；调用方40e453从该字段打印登录result。此异常分支result16是后台成员查询打开异常，不据其断言密码错误；还需请求关联及超时根因。实际程序数据库路由为.\SQLEXPRESS，不能把诊断127.0.0.1成功当命名实例发现/重连路径通过。静态合同：login-change-audit-r278/joypark-result16-contract.json，完整原始字节身份见同目录result.json。
