# Meridian Retail Group — AI-native delivery section

## AI-native delivery on Meridian checkout modernization

| SDLC phase | Target maturity (by month N) | Adoption metric | Tooling baseline | Key risk |
| --- | --- | --- | --- | --- |
| Intake | **L1 by month 2** | **80% of new intake items** have an AI-assisted first-pass qualification note by month 2 (**denominator: all new intake items opened in the month**) | **EPAM DIAL** — allow-list status: approved; **Office 365 Copilot** — allow-list status: approved for standard productivity use | Low-quality intake prompts create misleading opportunity framing |
| Plan | **L2 by month 4** | **75% of approved work items** have AI-assisted draft scope or acceptance-criteria text by month 4 (**denominator: all work items approved into planning**) | **EPAM DIAL** — approved; **Office 365 Copilot** — approved; **ChatGPT / Claude** — use only if allow-list confirmed for the engagement | Planning artifacts drift if AI drafts are accepted without human review |
| Build | **L2 by month 5** | **60% of implementation tasks** show AI-assisted contribution in prompt logs, commit notes, or paired coding evidence by month 5 (**denominator: all implementation tasks closed in the period**) | **GitHub Copilot** — approved; **EPAM DIAL** — approved; **Claude Code / Cursor** — conditional, only if engagement allow-list permits | Code-generation speed outruns review discipline and increases hidden defects |
| Validate | **L2 by month 5** | **70% of test cases or eval runs** are expanded, reviewed, or judged with AI-assisted support by month 5 (**denominator: all test cases / eval runs executed in the period**) | **EPAM DIAL** — approved; **GitHub Copilot** — approved for engineering-side test support; **specialized judge tooling** — allowed only if approved on the engagement | Weak AI-generated tests create a false sense of coverage |
| Handoff | **L1 by month 6** | **100% of release candidates** include AI-assisted first-pass rollout, runbook, or status draft artifacts by month 6 (**denominator: all release candidates entering handoff**) | **Office 365 Copilot** — approved; **EPAM DIAL** — approved | Handoff documents become polished summaries without enough operational truth |
| Learn | **L2 by month 6** | **1 retrospective improvement per sprint** is converted into a reusable AI-enabled artifact, prompt, or working rule by month 6 (**denominator: all retrospectives held in the period**) | **EPAM DIAL** — approved; **Office 365 Copilot** — approved | Learnings stay local to one person and do not become team practice |

## Measurement plan
- **Intake:** source of truth = intake tracker / qualification memo folder / prompt logs where available
- **Plan:** source of truth = Jira or backlog tool labels plus linked planning artifacts in version control
- **Build:** source of truth = version control evidence chain, PR notes, coding-session evidence
- **Validate:** source of truth = QA eval pack, test report artifacts, judge/eval run records
- **Handoff:** source of truth = release folder, runbooks, support pack, readiness artifacts
- **Learn:** source of truth = retro notes plus committed follow-up artifacts or process changes in version control

## Tooling baseline and allow-list note
This section assumes Meridian is proposed under an **RFP-led** engagement shape and defaults to **EPAM pre-approved AI tooling**. Any tool outside the pre-approved baseline must be checked against the engagement allow-list before commitment in the proposal or delivery plan.

## What is not automated
The following remain human-owned decisions and are **not** automated:
- scope approval and acceptance-criteria sign-off
- client commitments and milestone promises
- architecture trade-off approval
- risk acceptance and compliance sign-off
- security and production release decisions
- performance conversations, staffing decisions, and role-management calls
- contract changes, commercials, and any client-binding statement

## Summary
This AI-native section is intended to be gradable in six months: each phase has a target maturity, a measurable adoption metric with a denominator, a named tooling baseline, and a named risk. The targets are stretchable but realistic for a delivery team that already uses structured artifacts across engineering, QA, operations, and security.
