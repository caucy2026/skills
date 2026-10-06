# 通过GitHub全局技能交接设备能力

## 当前协议可表达的内容

真实合同device-capability/1的declaration包含title、userStatement、summary、inputs、outputs、methods、conditions、limitations、tags、skillRefs、executionMode。不要新增skillName、githubUrl、workflowUrl、permissions、verified等未支持字段。方法字符串每项最多512字符、最多20项；skillRefs仅技能ID，不是URL。只有该设备实际已发现技能才填skillRefs；云端有文档不等于客户端已安装。

将设备用途写title/summary，平台/版本及实测范围写summary与limitations，操作步骤及技能名称和地址写methods，真实授权与运行环境写conditions。userStatement保留用户实际陈述；自动facts/health由客户端程序采集，不由智能体伪造。公共方法推荐字符串格式：

- `skill: kemi-windows-remote-signing | https://github.com/caucy2026/skills/blob/main/kemi-windows-remote-signing/SKILL.md`
- `workflow: https://github.com/caucy2026/skills/blob/main/kemi-windows-remote-signing/references/workflow.md`
- `docs: https://github.com/caucy2026/priv/blob/main/hbbv/docs/WINDOWS_SIGNING_DEVICE_58_2026-10-06.md`

以上是现有methods字符串内容示例，不是新增Schema。文档只传公开操作说明、输入/输出、范围、先决条件与验证证据索引；不传密码、设备令牌、PIN、私钥、完整用户日志或转储。

## 保存、网页发现与协同

先read实际Schema、advanced.capabilities、system.capability_check和claims/revision；依据用户具体授权仅改选中claim，expectedProfileRevision冲突重新读。保存后核验sync_status acceptedRevision和云端实际claim。后台同时显示用途、平台/实际版本来源、能力方法链接、条件、限制及最后心跳；界面链接存在与目标HTTP可读分别验证。

管理智能体按房间和能力检索→核对声明/证据/工具当前状态→读对应GitHub SKILL及workflow→按真实任务发布/竞标/唯一分配/租约执行。看到“签名”不能直接派任务或跳过本地grant、PIN、身份和忙碌事务约束。已有授权同范围正常确认直接执行；平台审批边界保持。

技能分发的canonical独立仓库是https://github.com/caucy2026/skills，技能目录位于仓库根；priv/hbbv/skills只是旧归档，不能当canonical。引用main方便发现；执行涉及已冻结构建/签名时，记录所读文档commit与内容hash防止描述和步骤漂移。无凭据HTTP实测成功才说公共可读；404/401时只说明需要原有读取权限或地址待修，不公开仓库/复制凭据来绕过。

## 已验证例：58（2026-10-06）

58原仿真ID4240650696的原签名claim已改为上述canonical技能与workflow链接；本机saved revision39、sync acceptedRevision40，实际云端profile40包含两链接，qualification仍not_asserted。实际455/2455且旧456签名事务有独立外层签名/时间戳证据；这些证据不证明现在令牌、PIN、模型或任务权限均ready。声明不伪称已安装签名技能。安装身份公钥摘要与主EXE文件SHA不同，不混用。

其他设备只能按其实际claims/平台/工具和已有证据描述；不能把58签名能力复制给其余六台。五台基础心跳与MCP在线仍不等于所有七台入房、模型执行或长期协同验收。全目标门禁见[端到端验收映射](full-goal-acceptance-map.md)。
