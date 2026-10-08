# Reusable Templates

## Project contract

```text
Project:
Final outcome:
Acceptance criteria:
Manager task/thread:
Members and task/thread IDs:
Responsibility boundaries:
Current / next / fallback priorities:
Evidence locations:
Final artifacts:
Reference truth sources:
Unattended permissions:
Manager delegated approval scope:
Prohibited actions:
User-attended experiment trigger:
Monitoring cadence:
Hourly ledger policy:
Notification policy:
Release validation matrix:
Repository and backup policy:
```

## Concrete member assignment

```text
Task:
End-state result:
Why this advances the project goal:
Allowed scope:
Inputs and dependencies:
Generalization requirement:
Acceptance steps and quantitative denominator:
Evidence paths and required hashes:
Final artifact or runtime identity:
Stop condition:
After three no-result attempts, ask:
Safe fallback work:
```

## Hourly acceptance ledger

```text
Window:
End-state requirement:
Planned __ / Completed __ / Acceptance candidates __
PASS __ / FAIL __ / Not comparable __ / Component only __ / Blocked __
Changed files and commits:
Commands and tests (passed/total; named failures):

Acceptance item: <ID>

Scenario and scope:

Criterion:

Expected:

Actual:

Verdict:

Evidence path:

SHA-256:

Repeat this item block for each acceptance candidate.

End-to-end data/state chain:
Reference/candidate media and comparability:
Generalization coverage and special-case scan:
Unverified items and one precise gap each:
Newly excluded hypotheses and evidence:
Same-route attempt count:
Next-hour primary task and acceptance:
Fallback task and acceptance:
```

For changes with shared or global impact, append:

```text
Blast radius:
Pre-change baseline:
Compatibility matrix (passed/total):
New historical regression failures:
A/B oscillation count:
Final-artifact real-path status:
Rollback point:
```

## 30-minute manager report

This is the canonical report layout. Repeat the member section for every
in-scope member; preserve the same field order. Do not use a table. If the user
requests only scores, use the short layout below, with the complete roster.

```text
监督报告｜HH:MM–HH:MM

一、本轮验收目标

<成员>：用户要求与本轮终态。

二、<成员>

状态：工作中 / 停止 / 阻塞

本轮完成：
1. 可确认事实。
2. 可确认事实。

验收证据：
1. 命令、计数或产物；成员陈述须明确标注。

闭环：PASS / PARTIAL / FAIL；依据。

兼容：PASS / OPEN / FAIL；依据。

用户介入：是 / 否 / 无法确认。

管理动作：未打扰 / 已续派 / 已提醒 / 已授权。

恢复验证：不适用 / 已实际恢复及证据 / 仍阻塞及责任方。

评分：NN/100。

分项：要求__/35；产出__/25；闭环__/20；效率__/10；边界__/10。

扣分：具体证据与原因。

三、评分汇总

<成员>：NN/100｜优秀 / 合格 / 需纠正

Manager：NN/100｜优秀 / 合格 / 需纠正

Manager分项：要求__/35；产出__/25；闭环__/20；效率__/10；边界__/10。

Manager扣分与未完成责任：

四、风险与下一轮

1. 待处理事项、责任人和下一检查点。

五、聊天历史

<成员>：容量；处理结论。

<休息成员>：获准休息；不评分。
```

For an incomplete evidence assessment, replace the score/component fields with
the uncertainty record required by scoring-and-reporting.md; never silently omit
the member or rank an evidence lower bound as a definitive score. Missing fields
say “无” or “不适用” with a reason rather than changing the layout. A requested
project-specific vertical template may keep its own headings; preserve the same
roster, scoring, uncertainty and recovery fields.

### Immediate score request

```text
评分窗口｜HH:MM–HH:MM

<成员>：NN/100｜结论

依据：实际产出及验收范围。

扣分：具体缺口及责任归属。

处理：管理动作与真实恢复状态。

Repeat for every member, then Manager. State approved rest exemptions.
Keep the five component values in the linked full checkpoint.
```

## Three-attempt help request

```text
End-state target:
Current blocker:
Attempt 1 — hypothesis / action / evidence / result:
Attempt 2 — hypothesis / action / evidence / result:
Attempt 3 — hypothesis / action / evidence / result:
Remaining unknown:
Requested input or validation:
Files, logs, commits, or artifacts:
Independent work now in progress:
```

## User-attended experiment

```text
Item:
End-state target:
Why user presence or new authority is required:
Prior attempts and evidence:
Smallest discriminating experiment:
Required user action/input:
Risk and rollback:
Expected duration:
Independent work proceeding meanwhile:
```
