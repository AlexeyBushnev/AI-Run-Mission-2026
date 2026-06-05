# Maturity Gap Analysis

**Date:** 2026-06-03
**Author:** Aleksei Bushnev — Senior Data Quality Engineer
**Project:** Enterprise IoT Data Quality Platform — client-confidential details omitted
**Committed location:** https://github.com/AlexeyBushnev/AI-Run-Mission-2026/blob/main/maturity-gap-analysis.md

---

## Scorecard

| Dimension | Level (L1 / L2 / L3) | Score (1.0 / 2.0 / 3.0) | Evidence (2–3 sentences) |
|---|---|---|---|
| AI Capabilities | L2 | 2.0 | AI is used regularly across the team for coding support, technical research, documentation, analysis, and investigation work. The usage is not limited to one person and is part of day-to-day delivery, but it is still mostly assistant-style rather than agent-driven execution of sub-tasks. |
| Reusability | L2 | 2.0 | The team has started to create and reuse prompts, investigation patterns, and shared AI artifacts instead of keeping everything in private chats. Kata 2 produced a reusable prompt template committed for project use, which is evidence of shared reuse. However, reuse is still selective and not yet codified as a standard SDLC-wide operating pattern. |
| AI Champions | L2 | 2.0 | Yuri Bredzikhin can be named as a specific person who helps drive AI usage rather than the project relying only on unnamed enthusiasts. This is stronger than an L1 pattern because there is a visible person associated with practical adoption. However, the role still appears informal rather than supported by a broader champion network across core roles. |
| Performance Tracking | L1 | 1.0 | AI impact is still judged mostly through anecdotal feedback such as whether work feels faster or easier. There is no defined measurement framework for AI productivity, cost, or outcome quality on the project today. Without explicit metrics, the team cannot consistently evaluate whether AI usage improves delivery. |
| DAU | L2 | 2.0 | The team has about 15 people, and approximately 10–12 use AI tools daily based on real observed usage data. That places daily AI usage at a clear majority of the team. The project therefore fits L2 better than L1 on DAU, even though the usage is not yet tracked as part of a formal governance process. |
| **Average** |  | **1.8** |  |
| **Overall Level** | L1 |  | L1 = 1.0–1.9 / L2 = 2.0–2.9 / L3 = 3.0 |

---

## Gap Analysis

### Gap 1

**Dimension:** Performance Tracking  
**Current level:** L1  
**Why this gap is most damaging:** Without measurement, the team cannot distinguish real delivery improvement from anecdotal enthusiasm, so AI adoption decisions remain weakly governed.  
**Root cause:** There is no measurement framework for AI productivity or cost at project level.

---
## Gap 2

**Dimension:** AI Champions  
**Current level:** L2  
**Why this gap is most damaging:** AI usage remains dependent on individual initiative instead of becoming a team-level delivery capability that spreads reliably across roles.  
**Root cause:** Tool usage is individual and informal, not team-governed.

---

## 30-Day Improvement Plan

### Step 1 — addresses Gap 1

| Field | Value                                                                                                                                                                                                                                                                                   |
|---|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Action** | Define and publish a lightweight AI measurement sheet for the project with at least three tracked signals: number of reusable AI artifacts created, number of teammates actively using AI weekly, and one delivery-efficiency measure such as time saved or investigation acceleration. |
| **Owner** | Mariia Koval                                                                                                                                                                                                                                                                            |
| **Timeline** | 2026-06-12                                                                                                                                                                                                                                                                              |
| **Success metric** | A shared project document exists with at least 3 defined AI metrics, baseline values recorded once, and 1 review completed with project stakeholders.                                                                                                                                   |

---

### Step 2 — addresses Gap 2

| Field | Value |
|---|---|
| **Action** | Create a shared AI working area in the repository or team knowledge space and add at least 3 reusable project artifacts there, including prompts, templates, or skills, with named ownership and usage guidance. |
| **Owner** | Aleksei Bushnev |
| **Timeline** | 2026-06-30 |
| **Success metric** | The shared location exists and contains at least 3 committed reusable AI artifacts that can be run or reused by teammates without author explanation. |

---
## Peer Review

**Reviewer:** Mariia Koval — AI Champion / DQ Engineering Lead
**Date reviewed:** 2026-06-03

| Review question | Reviewer answer |
|---|---|
| Is the evidence for each dimension specific and observable — not aspirational? | Yes — the evidence is grounded in current project behavior and describes what the team does today rather than future plans. |
| Which score do you challenge, and why? | I challenge AI Champions and would also consider L1, because although a named person exists, the Champion role is still informal and not yet backed by explicit mandate or coverage across roles. |
| Is each root cause a structural/behavioural cause — not a symptom? | Yes — both root causes describe missing project-level operating structures rather than surface symptoms. |
| Are the success metrics measurable without asking the author? | Yes — both metrics can be verified directly from the shared document or repository state. |
| Would you sign off on this plan as a teammate? | Yes — the plan is concrete, time-bounded, and realistic for the next 30 days. |

---

## Revision History

| Version | Date | Change | Author |
|---|---|---|---|
| 1.0 | 2026-06-03 | Initial commit | Aleksei Bushnev |
| 1.1 | 2026-06-03 | Updated committed location and completed peer review section with named reviewer | Aleksei Bushnev |
