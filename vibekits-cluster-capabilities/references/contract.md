# 本机能力操作合同 device-capability/1

本包为待接入合同，运行时以已注册同版本工具为执行前提。

read与sync_status参数为{}，只读当前设备。mutate遵循 [输入Schema](contracts/claim-mutation.schema.json)，返回 [结果Schema](contracts/mutation-result.schema.json)。不得传输Schema之外字段。read返回本机profileRevision，供expectedProfileRevision条件写入；新建ID、origin、时间、revision均由程序赋值。

create/update均提交完整declaration；只替换本条用户声明，不改变确定性观测。原文userStatement由用户输入溯源，AI整理summary只作推断。初始成熟度是自述，由服务端另行评估，模型没有修改成熟度字段。

模型不调用云端上报API。独立客户端代理遵循 [档案报告Schema](contracts/capability-report.schema.json) 和 [心跳Schema](contracts/heartbeat.schema.json)，分别接收 [档案ACK](contracts/report-ack.schema.json) 和 [心跳ACK](contracts/heartbeat-ack.schema.json)。每次修改立即异步上报；4秒心跳提供版本核对，不替代变更上报。失联持久重试，关闭零集群网络；ACK接收与资格验证分开。

报文只由受控程序生成，设备身份必须匹配认证，档案revision/healthSeq由程序持久维护；禁止秘密、未知字段、重复JSON key和过期epoch覆盖。上下游还要做引用/身份/字段来源/跨字段语义校验，不能只靠Schema判断权限。

未知能力无需预定义名称或专用工具即可保存并进入候选；实际试用仍受本机真实工具、房间范围、任务预算和安全约束。禁止模型直接写verified/eligible，亦不能因未知能力没经过验证而拒绝保存正常自述。
