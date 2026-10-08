# 市场、总包裹与扩展包裹：统一落库和原版对应

本页是接入方案，拟议逻辑实体/字段不是当前已建表。维护主本仍是产品document/20260927-运营管理平台邮件市场与资产对账完整设计.md及20260929-总包裹市场邮件统一入口研发目标.md；不另设一套冲突的规格。当前这些设计明确未完成运营API/邮件/市场正式事务与扩展库存全链。

## 三种库存功能不能混为一项

1. 总包裹是现有真实Body容器的聚合视图，不增加物品或数据库槽。原顶层Body[0..7]各自是物品或容器；包按Object+0x20容器flag与D8容量显示子格。直接物品只有顶层格，不虚构child[0]，其他槽不重排。
2. 单包窗口、总入口、运营只读页共用同一权威inventoryRevision快照；切视图不写资产账、不复制物品。UI窗口位置与物品持久状态分离。
3. 真正扩大容量才新增sidecar容器。例如旧12格设计的4个新顶层槽，不改旧8槽/564字节0658。它不是总入口固定12格，也不能把8个保留子槽全当合法容量。

## 新功能用哪个数据库

我方第一版通过同一逻辑持久层、DatabaseAdapter和Typed仓储接入。若钱包/订单/库存sidecar都在同一支持事务的物理库，就一个事务提交；不优先再造一个无法关联的market.db来绕过现库存revision。服务分成模块不等于数据库必须分成三个文件。

若部署必须异库/分片，明示跨库状态机和补偿，不称分布式ACID。API先受理幂等command，持久化订单/托管，目标地图库按同一业务ID幂等提交库存，确认持久回执后中心完成；回执丢失查询同ID，不换ID重扣重发。库存成功而中心未完成时保留可恢复中间态；不能退款同时又让物品保留造成双得。

原版库仍用于参考/认证适配，不在原charpool偷偷加市场字段、改原Body结构或硬写新物品。修改我方测试库/服务才是本需求的实现域。

## 拟议实体、写入者与关联字段

具体表名可随当前实现选择SQL表或版本化键，但下列关系与字段不能省略。所有新实体都要迁移版本、唯一键和读取索引；是否已建须查schema并标实现状态。

|逻辑实体|必需字段/约束|写入权威|原版对应或区别|
|---|---|---|---|
|RoleIdentityMapping|不可复用roleIncarnationId、principal/slot、sourceSystem/sourceRoleID、原导入SHA、created/deleted|角色生命周期服务|关联charpool.RoleID/AccountID；slot不是原不可变RoleID|
|AccountWallet|account/principal、币种、整数最小单位、balance、revision、导入原point及转换版本|账号账务服务|crossgate.point是账号点数，Body货币是角色金币，两者不互换|
|LedgerEvent|eventId唯一、业务ID/requestId、actor/operator/reason、delta、前后余额/版本、policyVersion、时间|对应事务服务|原SQL字段差分只能作基线，新增账本不是已复刻原费率|
|ContainerSidecar|roleIncarnation、containerId、generation、capacity、revision、原容器锚点、逐槽对象/版本或数量|地图库存单写者|旧Body/EQ/Hand保留原编码；新增格单独协议能力|
|ItemProvenance/ImportMapping|itemInstance或lot、ObjectID、valueKind/rawValue、数量、容器与原位置、sourceRoleID、baseline/event链|库存/资产服务|原Version不是已证全局唯一ID；不得直接作所有新表主键|
|MarketOffer|offerId/revision、Object/来源、数量/库存、价格与币种、限购/绑定/资格、状态|市场服务|0314原NPC金币商店保持原义；新市场单独能力协商|
|MarketOrder|orderId、唯一(account,requestId)、offerRevision、价格快照、数量、收货角色代次/容器、状态、失败原因|市场购买服务|与wallet、库存/托管、ledger、outbox关联；不信客户端价|
|AttachmentEscrow|attachmentId、来源事件/物品身份、数量/版本、目标代次、状态|邮件/托管服务|不是Body中已有物品，未claim不计入玩家当前库存|
|ClaimJournal|唯一claimId、attachment/order、recipient/roleIncarnation、期望库存版本、提交结果|领取/库存服务|重复只能同结果，不因为超时新建claimId|
|OutboxEvent|eventId/业务ID、目标会话代次、payload版本、待发送/已确认/重试次数|提交事务+投递者|先存后通知；网络发送成功不代替DBcommit|
|ReconciliationFinding|窗口、基线、相关事件/订单、版本、差额、未知原因/复核状态|只读对账job|历史资料不足显式partial，不自动判作弊/罚没|

不确定费率、原point精度换算及随机实例身份要保留原值、版本和未知，不能猜一个比例上线。旧玩家交易已存在，不因邮件模块“不支持玩家互寄”的局部范围删掉交易。

## 购买闭环（同库）

正常客户端提交requestId、offerId/revision、数量和目标角色代次/会话；服务端解析账户身份，不接收前端权威余额/最终库存镜像。验证上架、库存/限购、价格版本、余额、物品定义、合法容器空间、expectedInventoryRevision及mapAdmission/租约。

同一事务：建立/复查订单幂等键→扣钱包→扣商品库存/来源托管→写角色库存或待领附件→写订单结果、来源账、审计、outbox→commit。失败全部回滚，成功才投影0658/扩展容器/余额。HTTP超时返回待确认，客户端查原order/request，不再盲下单。

## 挂单、邮件和新增格操作

如果商品来自玩家库存，先由地图服务验证真实来源container/slot、version/revision、绑定及资格，再同业务ID移入escrow；浏览器选中格子并不授权直接DELETE资产。是否开放玩家售卖按产品需求及权限，不能由数据库技能自动扩大。

邮件claim和市场购买共用库存权威与资产来源；群发recipient snapshot固定，每人附件份数明确。满包/旧角色已删/代次不符/旧客户端能力不符不消费托管物。离线查持久快照，在线写操作路由当前地图单写者，不让运营SQL绕过内存状态。

真扩展容器命令含containerId/generation、角色代次、库存revision、槽和itemVersion；旧客户端只能读写它能表达的状态。按既有设计，持有扩展资产时旧端可写准入须拒绝或采用经验证的兼容策略，绝不允许旧0658覆盖sidecar。新旧客户端与原商店/Hand拖动回归同制品。

## 出问题怎样和原来对应

从commandId/orderId/claimId→订单前态/结果与offer revision→钱包流水→库存审计原因键→roleIncarnation→原sourceRoleID及导入SHA→原表/列/位置原字节；再关联本次session/Section/Actor/observer句柄、前台opcode与截图。

资产位置描述需明确：原Body顶层2或Body[0].child[3]、EQ[2]及Version、Hand父/子、Bank/Temp；扩展描述为sidecar/container/generation/slot，不能伪装成原Body第9槽。总视图只是同位置锚点投影。

钱守恒：期初+有来源收入-有去向支出=期末；余额差必须列具体缺事件。物品按instance/lot/数量流转守恒，singleton rawValue按对象定义保真。version-only/Hand子物变化不要只用当前审计工具slotChanges判断，回读完整镜像。

若这是原版已有行为，走A/B/C同条件；若是新市场/扩展功能，原版没有对应入口，应验原兼容边界与新功能合同，不伪称“与原版市场完全一样”。记录原已有域0差异和新增域独立验收。

## 上线前必须证明

同ID重复、不足点数/金币、满包、真实4/6/8容量、旧offer改价、并发最后一件、同账户计费竞争、跨图、断线重连、在线/离线、删角重建、提交前后杀独立进程、outbox丢确认、备份恢复。核不超卖、不重复扣点、物品恰好一份、库存/订单/钱账一致、既有交易/NPC金币店不回归。

新增表创建、网页原型、仓储单测各自只记本层；有全过程制品/事件/截图/DB重登/受影响回归才登记完成。当前设计未完成的门保持未完成。
