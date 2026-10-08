---
name: swdol-static-dynamic-analysis
description: Reconstruct SWDOL client/server behavior by combining version-locked static analysis with authorized paired runtime instrumentation, evidence grading, replay, and end-to-end validation. Use for protocol, rendering, movement, combat, UI, resource, persistence, or compatibility investigations in the SWDOL projects; do not use for ordinary implementation work when a current verified contract already answers the question.
---

# SWDOL static and dynamic analysis

Treat the original executable, original resources, original server, protocol bytes,
candidate client/server, and visible result as one system. Dynamic instrumentation
produces evidence; it is never the product implementation.

## Start from the maintained project truth

Before acting, read the target repository's `README.md`, mandatory development
rules, documentation index, current global contract, relevant current topic
contract, and last verified injection/deployment record. Search existing evidence
before designing a new method. Preserve the proven VM, ABI, binary, launch order,
transport, collector, payload, and rollback unless repeatable evidence invalidates
that baseline.

For work in `/Users/kemi/coding/swdol2026`, always read:

- `document/README.md`;
- `document/20260905-静态分析与双端动态分析全局工作规范.md`;
- `document/20260902-客户端整体研究统一总合同与文档纠错.md`;
- the newest topic-specific contract and evidence ledger.

Read [references/project-runbook.md](references/project-runbook.md) before any
SWDOL static analysis or live trace. Read
[references/evidence-handoff.md](references/evidence-handoff.md) when planning a
run, grading a result, implementing from evidence, or writing a handoff.

When the most effective reconstruction path is to inject an original SWDOL server,
drive it with the reconstructed client through MCP, and compare the same action
against the candidate server, read
[references/original-server-mcp-closed-loop.md](references/original-server-mcp-closed-loop.md).
Use that closed loop for unfinished protocol, authority, movement, combat, plot,
inventory, transfer, persistence, or publication behavior. Do not substitute
component tests or a self-server-only E1 for missing original-server D1.

## Dynamic visual equivalence

For original-versus-candidate login/selection/map transitions, character motion,
spell particles, cast UI or claims of visually identical dynamics, read
[references/dynamic-visual-equivalence.md](references/dynamic-visual-equivalence.md).
It defines matched conditions, event/clock alignment, continuous-frame evidence,
deterministic versus stochastic particle checks, and acceptance boundaries.
Its paired-motion section traces one mover across both clients and the server
to separate transport delay, world-position error, camera differences and ACT sliding.
Do not use static screenshots or resource equality alone as dynamic proof.

## Select the smallest valid mode

For 86Box XP original-client injection, login, magic-book operation or teleport,
first read `/Users/kemi/.codex/skills/swdol-xp-control/SKILL.md` and its runbook.
It contains the measured 27.879-second warm login, the successful original-client
secret-realm transfer, durable commands, exact host/guest separation and failure
routing. Reuse that path rather than repeating setup or mouse-coordinate trials.

- **Static question:** lock binary/resource identity, recover data boundaries,
  control flow, ownership, failures, and candidate semantic boundaries. Stop when
  one minimal dynamic experiment can discriminate the remaining hypotheses.
- **Dynamic question:** state one falsifiable question, reuse existing observers
  before adding hooks, and capture one bounded action on an exact healthy target.
- **Combined reconstruction:** run the full `S0 -> D1 -> C1 -> typed contract ->
  R1 -> E1` chain. Do not skip from a screenshot or one hook to product logic.
- **Already verified behavior:** implement from the current contract and rerun its
  regression/E1 gate. Do not inject merely because injection is available.

## Non-negotiable decisions

- Bind every address and layout to a binary SHA-256. Revalidate probe bytes after
  every binary or tool change.
- Keep raw protocol fields, runtime identities, semantic projection, resources,
  world transforms, and presentation in separate layers.
- Correlate client and server by session/generation, runtime handle or
  `localObjectId`, opcode/request, Section/Act, and a bounded shared time window;
  never by display name alone.
- Default live work to read-only, low-frequency observation. Require explicit
  authority for mutations to HP, inventory, AI, timers, packets, return values,
  persistence, or service configuration.
- Use one collector and one payload generation for each exact target. Hot hooks
  copy bounded fixed-size records and return; cold workers handle formatting,
  symbolization, compression, screenshots, and networking.
- `INJECT_OK` is not evidence success. Require payload ready, exact target-PID
  heartbeat, and the expected business event.
- Never special-case an account, display name, map, ObjectID, or screenshot in
  product code. Convert evidence into typed general contracts and negative tests.
- Never claim completion from compilation, parsing, one screenshot, one account,
  one map, or one successful hook. State the exact evidence level and scope.
- Keep credentials out of source, durable docs, evidence names, and logs whenever
  avoidable.

## Completion

Finish only after target health is restored, raw evidence and hashes are retained,
observed/derived/inferred/unknown claims are separated, the candidate has a
deterministic replay or regression, and the same external behavior is tested with
the formal artifact. If any gate is missing, use an explicit partial or
contradicted status instead of “complete.”

## SWDOL前后台注入：三分钟止损（最高优先级）

按用户要求，从本轮恢复/注入开始连续计时；180秒内必须完成所需前后台注入、真实登录进图及对应后台动作验证。超时说明当前方法未达要求：**立即停止重复试错，仔细重读成熟注入流程、最近成功记录及对应故障说明，找出本轮与已成功流程的差异，纠正后再恢复执行。** 不盲目重复输入、重注入、换工具、造新路线或因单次失败重启虚拟机；连续两次登录卡住则按用户最新升级恢复规则重启本人VM，不得在这个非关键节点长时间循环。暂停的是错误的注入尝试，研发总目标继续保留。

具体计时、成功终态和故障分流见[180秒恢复与超时回查](../swdol-xp-control/references/cold-recovery-180s.md)。记录实际耗时、停在哪一步、已核证据、查阅文档及差异；不能重置计时掩盖失败，也不能把INJECT_OK、Ready或已发送按键当全流程通过。

## 磁盘巡检与现场清理

每次前后台注入/采集前、采集中及结束后，必须执行[磁盘与现场收尾](../client-server-dynamic-trace/references/disk-and-scene-cleanup.md)。及时清理本任务已不用且无活跃使用的旧注入文件；设定有界采集与停写/轮转，禁止长期无界写BIN。清理必须核实际空间释放，不删除活跃探针或未归档证据。

## 权威算法及多角色验证

前端操作配合后端探针验证裁决、状态、广播与保存，或以MCP编排多个角色检验并发和长稳时，读取[权威算法验收方法](../swdol-acceptance-handoff/references/server-algorithm-verification.md)。

## 新测试账号与自然建角

用户授权为测试自行新建账号/角色时，先读[注册→原生建角→首次登录与身份回读](../swdol-database-operations/references/identity-and-comparison.md#测试新账号与新角色注册自然创建首次登录)。原服两库登记、我方stdin注册、思想wire1–6、空槽UI和正常首入/重登分别验；不把管理预置或网络0200诊断当原生建角通过。授权只覆盖测试新身份，不覆盖修改旧角色/资产、删除或共享服务重启。

登录卡住按用户最新[两次升级恢复](../swdol-xp-control/references/failures.md#登录卡住的两次升级恢复用户最新授权覆盖旧三次登录熔断)：强关本人客户端重登，连续两次同症状重启本人VM，仍卡提醒用户重启后台；不自行重启共享后台。

## 每次验证三分钟止损

用户要求每次调试验证180秒内完成；超时停止重复尝试，认真回查对应文档、成功记录与本轮差异，查清未理解/遗漏步骤后再验证。统一按[验证180秒与超时文档回查](../swdol-xp-control/references/failures.md#每次调试验证180秒超时回查文档用户最新要求)，不重置计时或缩小完整验收目标掩盖超时。
