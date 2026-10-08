# 资产反查、剧情保存与验收

## 装备/钱变动怎么追

当前工具：/Users/kemi/coding/swdol2026/server/tools/read_inventory_audit.py。
调用形状：python3 <path> --database <private_runtime_copy.sqlite> --principal-and-slot <principal/slot> --limit 100 --output <private_report.json>。

它只读IAR1库存审计，给eventId、Unix提交时间、causeKeys、前后revision/镜像SHA及位置变化。--object-id可筛对象，但当前实现漏装备版本变化和Hand子物变化；空slotChanges不是无资产变化。原始审计保留这些bytes，需当前LegacyCompatStorageCodec与InventoryImage完整解码核Hand父/子、Body72、EQ ID+版本、Bank/Temp。原v1零Hand迁移与工具显示也不同，区分原值和迁移解释。

valueOrCount按Object.maxStack解释：max1单件DWORD通常版本，Count=1；可堆叠Count是数量、Version=0。原Version不自动等于全局不可变实例ID。原Body72物理槽与合法插入容量不同，原插入按D8，扣料原预检/删除扫描物理槽；不要为了统一风格破坏原规则。

追交易双方的同一事务原因/库存前后、角色代次、物品版本/数量、钱守恒；找获得、消耗、移到Hand/包/Bank/Temp、给谁、销毁和删角。审计causeKeys是关联线索，不自动是完整业务事件详情；旧历史、非库存状态未覆盖，明确未知，不称任意丢装均可解释。

## 剧情必须核哪些持久域

Mark、任务可见、称号资格与当前称号、材料扣除、装备/版本、金钱/经验、已学技能、pending reward、世界演员生成/结束/尸体归属、重生点分别核。Mark完成不证明其他域完成。重复做剧情应按原状态返回相同拒绝/对白或同ID回放，不重复扣发。

当前组合仓储实验有真实SQLite回滚/重复/重开保护，但重开adapter不是进程崩溃；人工库存后像不是实际exchange算法。我方一侧成功不是原版同条件通过。

## 失败注入与恢复矩阵

在本任务独立数据库/制品进行，不损坏共享原库：提交前失败、审计prepare/COMMIT失败、断线、杀独立测试进程、在线重启、旧格式迁移、损坏记录、revision冲突、旧owner/地图代次写入、删角重建同槽、重复request及负载下同时交易/剧情。

核失败前态字节仍在、审计/业务同事务无半更新，重启后结果完整、重复无第二次奖励、所有关联actor/租约/AOI回收可重登。硬终止时可失日志末尾但不能仅用不下线退出验证耐久；SQLite NORMAL/WAL与FULL/powerloss边界分别描述。

已知审查坑：生日Luck初始化与Age/Fame序列化是不同缺口；LAH/LAI/NCS坏count reserve可能巨额申请；槽复用称号/待办继承与全局演员历史需分别处理；没有controller worldSession的失败入图TCP关闭不自动释放backend暂存状态。用实际同制品验证，不把这些旧结论当当前已修。

## 报告及归档

每项状态：已复现组件、静态风险、原/我方配对通过、失败、不可比较、缺证据。列精确路径/行/源码HASH、程序/资源/数据库身份、前态、动作、原响应/DB、我方响应/DB、差异、直接间接回归和关闭条件。

证据私有原始，公开只脱敏摘要/真实授权截图。每两小时交接，代码归属清楚且审查完成的有限文件选择性备份；自动审批拒绝不能绕过，远端SHA没回读不能称已云备份。百分比只按完整硬门，不以文档数/查询数/编译通过增加。
