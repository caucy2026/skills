# 怎么对应账号、角色、数据库与运行态

## 对齐表（私有保存）

账号登录名→crossgate.serial_number→实际登录服结果→MySQL游戏账号键→charpool.AccountID/RoleID→真实选角槽→当前Section/session/PID/演员代次。跨库账号关系键必须由实际schema/认证合同与成功登录确认，不能假定serial_number等于useraccount.ID。

我方principalKey→roleSlot→角色不可复用代次/源RoleID映射→roleLease(roleId/epoch/owner)→mapAdmission generation→world会话→observer-local handle。没有已实现incarnation就记缺口，不造字段。

玩家RoleID、NPCPool RoleID、ObjectID、运行Actor索引、observer handle、party/chat标识属于不同域。运行查找先kind+实例/代次，再取源身份；同名、同坐标和同数字不够。

核账号→角色与角色→账号双向一致，实际MCP正常选角入图确认原名字节/Section/会话。账号在线哨兵和角色在地图是不同状态；无权清别人租约或踢人来修测试。

## 同条件最小实验

1. 锁原EXE/资源/当前运行探针代次、我方APP/BIN/SQLite路径，查询器schema及HASH。
2. 同角色种族/性别/职业/等级、装备及版本、Body/Hand/Bank/Temp、技能/状态、Mark/称号、时钟/RNG条件逐项定义。新账号则从创建/登录/建角开始；不是每次强行复制角色私有库。
3. 原库必要行双读，保存列名与Base64/NULL及hash；MyISAM期间变化不当一致前态。
4. 一边MCP正常操作，一边前台出包/后台解析、条件、状态、提交、发布事件；记录事件序号、runId、角色映射，不以探针心跳代替业务。
5. 我方相同输入，窄读即时状态/审计；按命名字段与版本化解码比较，而不是把Master包头偏移直接当DataCenter对象偏移。历史建角包有12字节头，Luck/Fame误归因必须复用已核合同。
6. 记录相位截图、opcode与正文原GBK、变量代入、扣点/金币/材料/奖励、拒绝/取消、重复、正常下线/断线、重登与在线服务重启。受影响旧功能用同一制品。

## 数据复制

原MyISAM物理备份不能在正在写入时随便复制.MYD/.MYI就称一致。优先成熟窄只读导出；全库一致备份需具体维护方案/授权，业务暂停/锁库都不得由技能自动授权。保留引擎、列序、默认值和编码。备份恢复在独立实例先验证，不覆盖原在线库。

我方SQLite运行WAL时单copy .sqlite可能漏提交。用SQLite online backup API或经授权的受控停写/关闭后复制，并回读完整性、行/键、角色快照及SHA。不要删除-shm/-wal凑磁盘空间；不要把备份连接的新PRAGMA说成运行连接耐久配置。

## 测试新账号与新角色：注册、自然创建、首次登录

用户明确授权为完成测试自行创建新的测试账号、角色；同范围不重复询问。只新增本任务测试身份，不覆盖已有账号/角色，不改旧密码、点数、库存、Mark或位置；不因此获得删角、踢号、清租约、重启共享服务的许可。

### 1. 开测前

- 确定A=原客户端→原服、B=我方客户端→原服、C=同一我方制品→我方服；D兼容链另验。需要双人同时在线时用不同测试账号，不让同账号登录互踢。
- 记录本轮runId、库/端点、APP/BIN/资源SHA、分配的XP、后台观察器代次；新名字采用短ASCII唯一名称，账号与角色名分别查重。不能靠旧PID/旧Ready。
- 密码由本机受控来源或本轮内存产生，私有凭据登记0700目录/0600文件，工具通过stdin/现有私有读取器使用；不进命令行、技能正文、截图、网页和Git。凭据读取器不认识新账号时先登记到其实际支持的私有来源，不假设新号可自动查到。
- 先注册再启动本任务独立我方服，避免驻留accounts_未刷新。现役authenticateDetailed读内存账户，DB外部新增不能自动保证当前进程可登录；只重载/重启自己的隔离服务，不影响共享服。

### 2. 原版账号注册：两库均登记

正常注册入口若已有当轮成功回执，优先复用；没有已核入口时复用9/30授权双库受控注册，不编造一个MCP注册工具。

1. 按original-databases.md确认在线MySQL swdol与SQL Server crossgate及当轮schema。只在目标新账号行窄查，不输出Password/pass列。
2. 游戏侧useraccount原静态路径写AccName/Password/State=0/KeyID/LoginID，RID和ManageLV取当轮表默认；每列类型、KeyID/LoginID生成合同和口令表示先核，不按旧离线54表/引擎假设在线结构。
3. 认证计费侧Member_Data_Table精确userid不存在才插入，serial_number由实际identity生成。9/30已成功样本是chargtype1、初始point1000、login_state0；这是该轮测试配置，不是所有新号统一默认。本轮测试预算按任务确定，不回填已有账号的点数。
4. 使用既有授权执行器/私有Windows读取器；SQL Server复用来宾OSQL.EXE的-E/-S127.0.0.1成功路线，实际二进制位置先核。当前成功回执未给出可直接移植的完整跨库SQL脚本，因此不得凭此摘要拼造VALUES；必须结合在线schema和原受控注册记录生成窄化、正确绑定的语句。
5. 两库不是一个已证ACID事务。逐库保存成功回执；超时先只读查是否已插入，禁止盲重试。若仅一库成功，记录半完成，再只补确实缺的另一库；不删除已存在旧行作回滚。
6. 两库回读新行、账号键、空角色槽和凭据匹配布尔值，再从正常客户端登录。只建MySQL行曾得到Master0009=-4；补crossgate后才成功。serial_number不等于MySQL AccountID，也不等于Master0009正值。

### 3. 我方账号注册：独立SQLite现有工具

源工具server/tools/RegisterLegacyAccount.cpp，registerDatabaseAccount使用事务注册，账号/口令各1–20字节且拒NUL/Tab/CR/LF。先核本轮服务器实际DB及账户来源；不把外部TSV模式或私有参考SQLite当正式账户库。

从当前源编译到本任务独立临时位置（2026-10-04已编译及临时库注册/重复回读验证）：

```sh
cd /Users/kemi/coding/swdol2026
clang++ -std=c++20 -Wall -Wextra -Werror -pthread \
  -Iserver/src -Ishared -Iclient/src \
  server/tools/RegisterLegacyAccount.cpp \
  server/src/auth/LegacyCompatAccountStore.cpp \
  server/src/persistence/SqliteDatabaseAdapter.cpp \
  server/src/persistence/LegacyCompatRoleStateRepository.cpp \
  server/src/persistence/LegacyCompatInventoryRepository.cpp \
  server/src/persistence/SharedRoleLeaseStore.cpp \
  server/src/persistence/LegacyStoryProgressRepository.cpp \
  -lsqlite3 -o /private/tmp/swdol-register-test-account
```

调用形状为`register-tool DB_ABSOLUTE_PATH SEED_TSV_PATH`，stdin第一行账号、第二行密码；用subprocess.run([...], input=account+'\n'+password+'\n', text=True)从内存传入，不用shell echo口令。空新库需已验证seed；已有坏账户BLOB不能重置为空。工具不会覆盖已有账户键，初始化/加载异常必须保留错误。

注册成功exit0/code0并返回principal；重复exit4/code1返回已有principal，不是成功新增，也不重设口令。9/17测试与本轮隔离复验均印证此语义。将principal私有记录后，以DB模式启动同库独立服务器；角色仍为空，注册不等于建角。

### 4. 原生建角流程

1. 正常登录并核0009/000A，看到本账号真实空槽才进入创建页面；已有角色保留，选另一个空槽。我方常规slot0/1，不能抄DataCenter五RID槽。
2. 原版XP复用swdol-xp-control的焦点/DirectInput/定向普通键盘；按当前实际页面逐页截图，再操作种族、性别、面容/体型、唯一角色名、合法生日、职业、思想和属性分配。已有9/30成功基线为人族男剑客、首项儒家、七属性5/5/5/5/5/5/3；这是比较用样本，不是强制所有职业33点默认。
3. 按Character.DBF合法组合选择；UI思想序号0–5对应wire1–6，wire0未选；旧d1227d5及“改道家才成功”结论已撤回，以dab2e0b及9/30 14:15原字节纠错为准。不要全局禁儒家。
4. 最后确认页先核名字字节、种族/性别/职业、外观、生日、思想、属性与出生字段，再按原确认按钮提交。后台观测Master ClientCreateRole0200/InitialRoleData/DataCenter048C，关联0200应用50字节与0201回执。
5. 0201失败不造卡/不改角色列表；-1提示重名但也曾用于错误思想，文本不能独证失败根因。成功必须返回预期槽、刷新真实000A，并保留原槽。
6. 原版完整五页全自动脚本/逐页固定坐标仍未验证，不能套登录脚本称已全自动建角。我方现有世界MCP的ui_pointer_down/up不证明能控制FrontFlow建角文本输入；launch_client通常是测试登录/选槽入口，不是create_account/create_character工具。先核当前控制能力，缺前流输入时用已授权正常原生UI，不伪造API。
7. 使用产品LegacyLoginConnection+CharacterCreationRequest的短时0200诊断可定位字段，须标网络诊断创建，不能替代原生APP建角验收。

### 5. 查账号—角色与验收

- 原服：userid→crossgate serial；游戏AccName→useraccount账号键/RID槽→charpool.AccountID/RoleID。账号到角色及角色到账号双向回读，名字保留原字节。不能拿相等数字或姓名当映射证据。
- 我方：principal/slot→实际创建角色/roleLease→地图session/observer-local handle。前台新卡、后台创建事件、DB角色和子域记录应同轮一致；不假设新增生日等字段已完整保存。
- 正常选新角首入图，核0017七字段、0600/0400、0010/0658、初始装备/版本、Body/Hand、技能、Mark/称号和HP/MP；状态就绪后才做剧情，不把占位数值当初态。
- 正常下线再登录同槽，核新角色仍在且状态相同；我方仅本任务隔离服做在线保存/重启恢复。注册、建角、首入、即时DB、重登、重启分别记结果；组件/注册工具验证不冒充GUI完成。
- A/B/C用匹配种族职业外观/技能/前态独立创建，截图同相位配后台/协议/DB。测试账号留受控台账，不随意删角色或清公共资料。

### 6. 限时排障与现场收尾

注册/建角资料先准备，再计注入恢复180秒；超时停重复试错回查成熟技能，不重置计时冒充成功。正常建角不是已测27秒暖登录路线，没有已验证三分钟全建角承诺。0009负码查双库登记与真实身份；0201拒绝查合法字段/精确分支；空建角页长停曾66秒被断开，页面过期先正常重新认证而非重复注入。登录卡住可强关本人客户端重登；连续两次同症状按最新授权重启本任务VM，重启后仍卡立即提醒用户重启后台。具体按swdol-xp-control/references/failures.md两次升级恢复，不自行重启原服。

关闭测试UI前正常下线，停有界采集，按磁盘技能精确清本任务不用且证据已归档的注入临时文件；不删角色库/SQLite WAL/SHM、活跃探针或未归档证据。

依据：9/30 05:00、09:00、11:20（含14:15纠错）、15:30四份回合记录及各自evidence；server/tools/RegisterLegacyAccount.cpp、auth/LegacyCompatAccountStore.cpp、现役客户端MCP工具表。这些流程细节不代表注册/建角全链已经双端验收通过。

2026-10-04 本轮完整APP r315程序4ca093…、资源76a56d…、529输入一致后实际打开正常FrontFlow Login页。现有SWDOL_MCP_BACKGROUND=1使rememberedLoginPassword在读取Keychain前返回，未放入测试凭据或自动登录；旧账号名仍会显示，必须现场清空。自绘字段Cmd+A未全选，Backspace实际逐字删除；只在已知非秘密文本与新截图核实后清除，不在密码截图里验明文。这只证明原生GUI字段可操作，尚不是注册/登录/建角通过。世界MCP没有create API时用已授权正常原生UI，不用--start-create跳页冒充自然流程。
