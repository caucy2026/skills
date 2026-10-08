# Mandatory scoring and reporting

## Scope and cadence

Score on every management cycle (default 30 minutes) and immediately when the user asks. Include each monitored member and the manager. Explicitly excused/resting members are listed as exempt; never score them zero. A blocked member still receives an assessment record. Save the assessment even when notification policy requires silence.

Before evaluating, state the time window, latest user requirements, actual assignment and acceptance criteria. Separate work observed within the window from older milestones. Scores describe execution and delivery evidence, not personal worth, activity volume, or percentage complete.

## Fixed weights

- Requirements: 35. Alignment with the user's result, method, priority and scope.
- Effective output: 25. New code, measured evidence, valid tests or falsifiable findings in the window.
- Acceptance closure: 20. Relevant build, real use, regression and evidence against the declared artifact; mark historical milestones separately.
- Efficiency: 10. Necessary work and useful failed experiments, avoidance of repetition, and timely safe continuation.
- Risk and collaboration: 10. Preservation of accepted behavior, shared state and other contributors' work; honest reporting.

For every numeric score, record the five component values, their sum, supporting evidence and concrete deductions. Check the arithmetic. Do not give full requirements credit just because no new deviation is visible, or credit a manager-performed check as new member output. A useful failed experiment can earn output/efficiency points. Compilation, one screenshot, messages, or a test-call success cannot earn unproved acceptance points.

Use 90–100 excellent, 60–89 satisfactory/in progress, and below 60 needs correction only for sufficiently supported assessments. 100 requires the declared end-state acceptance and relevant compatibility gates. A high score never bypasses release gates.

## Evidence, uncertainty and fairness

Check raw timestamped events, actual files and commands, tests/artifacts, reasonable long-running jobs, and user intervention before scoring. Status summaries are only pointers. Resolve stale-state conflicts before assigning a definitive score.

Never omit a score field or stop at an unexplained “pending verification.” Complete the missing read-only checks in the same cycle when possible. If an external/tool failure prevents a sound numeric rating, keep the member in the report with an explicitly INCOMPLETE assessment: verified earned points as a lower bound, assessed weight, unassessed weight, possible score interval and the missing evidence. Example: verified 30 points across 50 assessed weight, remaining 50 unassessed means range 30–80, not a definitive 30/100. If nothing was observed, record no defensible numeric rating and the manager's verification failure; never fabricate one. Such records do not enter rankings or low-score interventions. Repair and replace the incomplete assessment promptly; the cycle remains incomplete meanwhile.

A low definitive score needs two independent negative evidence types. Below 20 also requires at least three verified absences: raw progress, relevant file changes, build/test progress, or a reasonable long task. Missing access is not absence of work. Do not reuse an old score as current evidence or reduce a score merely because the user is angry.

## Responsibility and intervention

Separate delivery delay from its cause: member execution, manager coordination, application approval, or external dependency. A member blocked by an approval they cannot grant is not automatically inefficient or idle by choice. The manager owns finding the blockage, scoped resolution, feasible fallback, and confirming real resumption. Record justified waiting and unknown responsibility without assigning blame.

Below 60 is not automatic permission to interrupt. A work-method reminder requires all of: confirmed noncompliance, no user intervention in the last 30 minutes, no valid long task being disrupted, and no duplicate reminder for the same problem this cycle. Work continuation and concrete dependency coordination are distinct from criticism. Members producing evidence should be left alone.

For an unfinished stopped member, send one concrete next task. Then verify a fresh execution event rather than just message receipt or an active label. A pending application approval is not cleared by writing “agree” in chat. Use available authorized mechanisms; never bypass a tool restriction. If blocked, report the exact missing action and keep recovery open.

## Manager score and correction

Apply the same five weights to manager work: user requirements and complete roster; independent verification and useful coordination; verified recovery/acceptance; timely nonrepetitive checks; and safe, fair boundaries. Do not award points for statements of intent. Specific deductions must identify omissions such as a missed score, stale-state judgment, false acceptance, unnecessary interruption, or unverified recovery.

If a score or report was wrong, retain the old record and append the corrected evidence, corrected component sum, reason and prevention step. Do not rewrite history to hide the error, compensate with arbitrary high scores, or use an exaggerated self-score as a substitute for fixing the failure.

## Report completion gate

Use the vertical template in templates.md. Before saving/sending check:

1. Complete roster including manager and explicit exemptions.
2. Latest requirements, time window, facts vs claims, and current task for each member.
3. Five supported component values totaling the displayed score, or a clearly incomplete evidence assessment.
4. Concrete deductions and blocker ownership; no historical output counted as new.
5. Intervention eligibility and actual follow-up evidence; unresolved recovery remains open.
6. No tables, mixed-member lines, bundled paths/hashes, or overflowing narrative lines.
7. The next check and unfinished obligations survive context compaction and handoff.

Keep each narrative line within 60 Chinese characters where feasible. Put long paths and hashes on separate lines; use short clickable labels in user-facing reports rather than breaking a machine identifier. Keep one field per paragraph. Every member gets the same field order. An explicit request for scores receives all requested members together, not a statement that scoring will happen later.

## Mechanical check

Before finalizing a full checkpoint, save its score ledger as JSON and run
`python3 scripts/check_scores.py /absolute/path/review.json` from the skill folder.
The object contains `window`, `members` (excluding Manager), optional `exempt`
(name to reason), and `assessments`. Each assessment has `member`, `components`
(requirements/output/closure/efficiency/boundaries), `score`, `evidence` (source
references), and `deductions`. Below 60 also requires `negative_evidence_types`
with two independent categories. Use `status: incomplete` for an unfinished
assessment; the checker intentionally fails it rather than certifying a missing
score. A valid checker result checks roster and arithmetic only, never truth or
fairness. If execution tools are unavailable, perform the same checks manually
and record that limitation; do not discard the scoring obligation.
