# 我方SQLite：实际服务器如何使用

## 连接与只读查看

工程根 /Users/kemi/coding/swdol2026；实际库由本轮服务器启动参数/配置确定，不固定使用某个/tmp旧库。先核进程命令行、端点、BIN SHA及SQLite绝对路径，避免查私有原版参考库而误当服务端库。

读库用sqlite3只读URI mode=ro，再PRAGMA query_only=ON；不要调用SqliteDatabaseAdapter构造做只读巡检，因为它会open CREATE、建表、WAL和INSERT schema_meta。schema结构可查sqlite_master与PRAGMA table_info，不输出账号BLOB内容。

只读检查SQL：SELECT sqlite_version(); PRAGMA journal_mode; PRAGMA synchronous; PRAGMA busy_timeout; PRAGMA foreign_keys; SELECT version FROM schema_meta WHERE singleton=1; SELECT name,type FROM sqlite_master WHERE type IN ('table','index'); 按授权范围运行quick_check，完整integrity_check在独立副本或有界维护窗口进行。

每个连接PRAGMA不同：新只读Python连接的synchronous/busy_timeout不证明运行服务adapter配置。当前源码明确WAL、foreign_keys ON、busy5000、FULLMUTEX；未显式synchronous，历史本机探测NORMAL，不可称发布BIN已FULL/断电无损。

## 物理表

|表|作用|查看方法|
|---|---|---|
|schema_meta|存储格式/迁移版本|version单行，只读核；不能把改数字称完整迁移|
|kv_store|具名键→版本化二进制/紧凑账户记录|按精确绑定key查length(value)、HEX小头和SHA；解析器跟制品同版本|
|inventory_audit_v1|库存事务前后像、原因键、提交Unix时间|id有序，payload IAR1；先限定时间/角色私有处理，不导全库|

## 状态键与消费者

以下是已审路径；实际完整键名以当前StorageCodec/仓储为准，未列域不能按模板猜。

|域|典型键或仓储|服务器作用|
|---|---|---|
|账户|LegacyCompatAccountStore紧凑TSV BLOB|authenticate/create/select，包含凭据，禁止普通输出|
|角色|storage::roleStateKey(principal,slot)，LegacyCompatRoleStateRepository|位置/HPMP/经验/重生及版本CAS|
|库存|legacy-compat/inventory/v1/principal/slot|LIS镜像Hand/Body/EQ及可选Bank/Temp，CAS和审计|
|剧情Mark|legacy-compat/story/v1/principal/slot|LSP、revision、最多15999 Mark号|
|剧情事务|story/journal、replay-response/requestId|同ID同内容幂等、碰撞拒绝、响应重放|
|演员恢复|story/aggregate-history、aggregate-index|LAH/LAI意图发现，含全局地图演员历史；不能为删角盲删全部地图记录|
|待办奖励|story/pending-chat/v1/principal/slot|延时奖励队列，移除与库存/剧情同一提交|
|角色租约|role-lease/v1/roleId|epoch/owner/Unix到期，默认TTL30秒；代次、会话、地图admission另核|
|演员终结|narrative-end/v1/section/instance|NAE tombstone阻止剧情演员再次恢复|
|称号/任务可见/尸体/地上物|各Typed仓储|独立领域，不从Mark存在推断全都保存|

前台动作→协议解析/权限/条件→内存暂存→对应仓储同事务→commit成功→网络发布。交易两边库存、剧情扣发+Mark、待办移除、奖励日志要同事务；失败不通知成功。不等待角色下线才保存已经接受的资产交易。位置/周期属性何时checkpoint须专门验原时点与当前策略。

DatabaseAdapter.begin返回持有互斥的BEGIN IMMEDIATE事务；commit前同事务写审计，失败rollback，析构回滚。不要在stageAdditionalWrites回调里再调用会begin的仓储：复用传入DatabaseTransaction，避免递归同锁。SQLite busy5秒不限制C++mutex等待，不保证全服务无死锁。

read/write expectedRevision和owner/admission栅栏都需核，日志ID不等于角色代次。当前删角常规清role/inventory/story/visibility四键，称号/待办/恢复意图等需要生命周期隔离；不得假设所有键都清了。

## 参考副本不是运行库

tools/import_original_role_snapshot.py从已采集稳定五表JSON创建字节保真SQLite；当前硬核RoleID95，拒绝覆盖已有目标。它没有转换成LIS/LRS，不是任意角色导入器或在线MySQL查询器。使用前重新读源码，角色改变需已验证通用入口，不私改RoleID骗过校验。

调用形状：python3 /Users/kemi/coding/swdol2026/tools/import_original_role_snapshot.py --input <private_snapshot.json> --output <new_private_reference.sqlite>。输入columns与valuesBase64、NULL保留；私有0700目录/0600文件，读回SHA/RoleID。失败输出不宣布完整备份。


## 登录补充迁移的实际入口与边界

现有工具 `/Users/kemi/coding/swdol2026/server/tools/MigrateLegacyLoginData.cpp`，核心 `server/src/auth/LegacyLoginDataMigration.cpp`。读取已有库账户文本，默认只读预览，显式 `--apply-offline PREVIEW_SHA256` 才申请；offline由操作者确认，程序不检测或停止其他服务。实际允许friend、money、body-item、equipment-item、throwable-item五类；20260831说明中的四类是旧范围，不能作为当前完整列表。fbad2dc快照已含第五类，无法由该聚合提交确定首次开发时间。

它只事务保存账户文本备份和追加文本，不负责将原版数据库整体转换成我方typed角色状态，也不更新现有typed库存。启动是否指定外部TSV影响账户来源（Main当前21678起），应记录启动参数和来源SHA。存在独立新进程TCP迁移测试，但它不等于强杀/断电恢复；专用C++库存哨兵缺/v1/，不作为真实库存仓储验收证据。
