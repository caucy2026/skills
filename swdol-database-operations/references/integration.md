# 服务器后续如何接入数据库

## 当前与目标分开

当前服务端 C++ DatabaseAdapter/DatabaseTransaction，由SQLite实现kv_store、schema_meta、inventory_audit_v1；不是已实现与原SQL Server/MySQL双库等价的新数据库服务。历史Python JSONL/fsync持久化是参考实现，不能当现在运行服数据库。原GameInit/DB协议目录是合同/数据组件，需实际调用/测试才能说接入。

新认证、运营计费、邮件市场方案在对应综合设计仍有NOT_IMPLEMENTED/未验门。不要把point float、游戏金币、时间期限、服务器GM等级合成一个余额/权限；各自权威明确。

## 接入顺序

1. 选择兼容路线：保持我方SQLite私服、在独立测试实例增加SQL适配器，或复用原认证接口。先核用户任务目标，不能为了省事只做一种客户端可登录。
2. Schema契约：原账号/角色外键映射、表/字段/列型/NULL/编码/单位/版本、唯一约束、归档、角色代次、地图实例和时间源逐项绑定。旧SELECT* ABI只用于原解码证据，新实现按具名字段。crossgate与swdol主键不得猜等值。
3. Typed仓储落到DatabaseAdapter。DatabaseAdapter当前只定义schemaVersion/migrate/begin，DatabaseTransaction定义get/put/erase/commit/rollback，其中erase默认返回false。expectedRevision CAS、request幂等和owner/admission栅栏必须由对应仓储及业务实现逐项核实，不能称接口自带这些保证；新适配器应保持已验证事务语义，不把同进程mutex当跨进程唯一owner。
4. 同库资产/剧情/奖励成组事务，提交后outbox通知；不得只下线才存交易。stage回调共享同事务，不嵌套begin。审计追加失败应回滚业务，保存原因与精确前后像。
5. 跨认证库/游戏库用明确补偿与幂等业务ID或已验证原入口；不能声称两个独立库自然ACID。创建账户半成功、认证成功但无角色、会话占用、重复登录/退出及点数结算分支独立验。
6. 存档导入在新私库：字节参考→版本化typed转换→检查来源ID/角色代次及合法容器→即时读回→正常客户端入图。现Role95参考导入脚本没有typed转换，不能省略此阶段。
7. 原表与我方键映射升级需迁移版本和双读对照；旧格式18/21/23账户记录、LISv1/2/3、日志/称号/待办/演员结束记录覆盖。改schemaVersion数字不代表迁移完成。
8. 对每个写域做合法/拒绝/取消/重复/断线/重启/并发/故障实验，A/B/C及长期D链，同发布制品受影响回归；能上线由完整硬门决定。

## 多线程和追踪

地图状态唯一owner/序列化事件；跨角色交易稳定参与者排序或同一DB事务，不同时持多把不明顺序锁。记录角色/地图/lease/epoch/revision/request/commit/event序号，保证从前台动作追到DB和发布。busy_timeout不保证mutex死锁不发生，FULLMUTEX不保证业务锁顺序正确。锁竞争、超时、反向交易和callback异常需实际证明。

角色删重建不能沿用principal/slot历史归属；保持明确incarnation或已证生命周期隔离。全局地图Actor的历史可能需持续，删角清理不能盲删使演员复活/消失。资产事件instance/lot设计、所有非库存审计、运营API都按实现/未实现逐项记，不造全局唯一ID。

## 新增市场与包裹的统一规则

详见[市场与库存扩展](market-and-inventory-extension.md)：总包裹只做现有库存投影；真实容量扩展使用版本化sidecar。新增钱包、订单、托管、领取、审计和outbox通过业务ID与角色代次关联原版来源；这些是接入设计，不是已实现表或已通过功能。
