---
name: client-server-dynamic-trace
description: Safely design, run, and document low-intrusion dynamic instrumentation across a client and server when protocol, state-machine, AI, UI, or persistence behavior must be reconstructed from a real system. Use for authorized binary injection, runtime tracing, paired client/server event correlation, and replay-based implementation validation; do not use for bypassing access controls or modifying third-party systems without authorization.
---

# Client/server dynamic trace

Use dynamic instrumentation as an evidence-producing experiment, not as the product implementation.

Before acting, read the target project's mandatory development rules and its last verified injection/deployment record. Preserve the proven toolchain, architecture, launch order, transport, and rollback method unless repeatable evidence shows that baseline no longer works.

When the target already has a resident observer, treat an “inject” request as a
readiness lookup first. Within one short status check, report either that the exact
PID and requested probe generation are ready, or that a new target process is
required. Do not invent a second launcher, GUI path, transport, or hot-added
payload merely because the requested probes were omitted from the current process.

## Choose the smallest experiment

1. Write one falsifiable question and the minimum user action or synthetic stimulus needed to answer it.
2. Identify the exact client process, server process, map/shard, ports, build hashes, and time window.
3. Capture a healthy pre-injection baseline. Never infer health from process existence alone; use the project's real readiness signal.
4. Prefer protocol capture or an existing observer before adding a new hook. Add hooks only at semantic boundaries that the existing evidence cannot expose.

For concrete probe design and execution, read [references/runbook.md](references/runbook.md). For result grading and project handoff, read [references/evidence.md](references/evidence.md).

## Non-negotiable runtime boundaries

- Operate only on systems and processes the user placed in scope.
- Default to read-only, low-frequency observation. Do not alter HP, inventory, AI state, timers, database rows, packets, or return values unless the user explicitly requests a controlled mutation experiment.
- Do not stop, restart, replace, or reconfigure unrelated services. Attach to one resolved PID; never use an ambiguous name match when multiple instances exist.
- Establish one collector and one payload generation per target. Detect and remove only stale artifacts owned by the current experiment before retrying.
- Keep hot hooks bounded: copy the minimum fields into a fixed-size record and return. Perform symbolization, formatting, compression, networking, screenshots, and retries on a cold worker.
- Use a unique evidence directory and append-only raw trace for every run. Never overwrite the previous successful baseline.
- Define a kill switch and rollback before injection. If readiness regresses, event volume becomes unsafe, or another service is affected, stop new collection, detach the current experiment, and verify recovery.
- Keep credentials and secrets out of source, logs, command lines when avoidable, evidence bundles, and durable documentation.

## Paired observation contract

Give client and server records a shared wall-clock basis and preserve each side's monotonic sequence. Correlate by time window plus stable protocol identities such as session, actor handle, object ID, request ID, map/section, opcode, or generation; do not correlate only by display name.

Record the full chain when applicable:

`user/client intent -> client validation -> outbound request -> server parse -> authority/state transition -> persistence transaction -> outbound publication -> client state application -> visible result`

Missing events are findings. Do not synthesize them, backfill guessed values, or treat a same-source probe as independent confirmation.

## Completion gate

An experiment is complete only when:

- the target remained healthy or was restored and verified;
- the requested action has a bounded, timestamped client/server trace;
- raw evidence, hashes, process identities, configuration, and exact commands are retained;
- conclusions state what was observed, inferred, contradicted, and still unknown;
- the result is converted into a deterministic regression or replay test when implementation work is in scope;
- the candidate implementation is rerun through the same external behavior and compared with the reference.

Do not claim the reconstructed feature is complete merely because injection succeeded or one hook fired.

## SWDOL前后台注入：三分钟止损（最高优先级）

按用户要求，从本轮恢复/注入开始连续计时；180秒内必须完成所需前后台注入、真实登录进图及对应后台动作验证。超时说明当前方法未达要求：**立即停止重复试错，仔细重读成熟注入流程、最近成功记录及对应故障说明，找出本轮与已成功流程的差异，纠正后再恢复执行。** 不盲目重复输入、重注入、换工具、造新路线或重启健康虚拟机；不得在这个非关键节点长时间循环。暂停的是错误的注入尝试，研发总目标继续保留。

具体计时、成功终态和故障分流见[180秒恢复与超时回查](../swdol-xp-control/references/cold-recovery-180s.md)。记录实际耗时、停在哪一步、已核证据、查阅文档及差异；不能重置计时掩盖失败，也不能把INJECT_OK、Ready或已发送按键当全流程通过。

## 磁盘巡检与现场清理

每次前后台注入/采集前、采集中及结束后，必须执行[磁盘与现场收尾](../client-server-dynamic-trace/references/disk-and-scene-cleanup.md)。及时清理本任务已不用且无活跃使用的旧注入文件；设定有界采集与停写/轮转，禁止长期无界写BIN。清理必须核实际空间释放，不删除活跃探针或未归档证据。


## 资源收尾与前台占用

按用户要求，自己创建的APP/进程、临时文件和打开的文件/句柄/数据库事务/socket/锁必须自己收尾，验证后关闭不用实例，尽量后台操作、少占前台，效率第一。执行[统一现场收尾准则](references/disk-and-scene-cleanup.md)，以实际退出/释放/删除回读为准；保留必要证据，不误删活跃资源。该规则不代替产品保存/验收，也不暂停完整目标。
