# Meridian Retail Group — implementation & rollout plan

## Milestones
| Milestone | Date | Entry criterion | Exit criterion | Owner |
| --- | --- | --- | --- | --- |
| Mobilization complete | 2026-08-26 | Contract award, named sponsor, core team assigned, kickoff held | Approved scope baseline, working governance cadence, confirmed dependency register | Delivery Lead |
| Core checkout build complete | 2026-11-06 | Scope baseline approved, environments ready, API/service contracts confirmed | Non-AI checkout path implemented, integrated, and ready for formal test | Engineering Lead |
| AI cart-summary + controls ready | 2026-12-18 | Core checkout path stable, gateway access approved, security/ops gates defined | AI-assisted cart summary integrated through approved gateway, cost cap path defined, security and operational controls evidenced | Solution Architect |
| UAT exit and release readiness | 2027-02-05 | Test pack approved, support model drafted, release checklist agreed | UAT signed off, rollback/runbook approved, release readiness accepted by steering committee | QA Lead |
| Production rollout + hypercare exit | 2027-03-05 | Release approval, support roster active, hypercare plan approved | Production live, hypercare KPIs stable, service transitioned to BAU support | PM / Service Transition Lead |

## Governance cadence

### Steering committee — monthly
- **Attendees:** executive sponsor, client product owner, EPAM delivery lead, solution architect, security lead, operations lead
- **Decision rights:** scope changes above threshold, budget decisions, milestone acceptance, unresolved escalation decisions, policy exceptions
- **Purpose:** remove blockers, approve major changes, confirm readiness to move between phases

### Sprint governance — biweekly
- **Attendees:** delivery lead, engineering lead, BA, QA lead, architecture representative, client product representative
- **Decision rights:** sprint priority, story acceptance at working level, dependency sequencing, defect/tech-debt trade-offs within approved scope
- **Purpose:** manage execution rhythm and short-horizon delivery choices

### Retrospective — biweekly
- **Attendees:** delivery team, champion representatives, selected client working-team members
- **Decision rights:** team-level process adjustments, working-agreement changes, improvement experiments
- **Purpose:** improve delivery flow and adoption friction handling

### Executive sponsor
- **Named sponsor:** Sarah Chen
- **Authority:** written authority to unblock policy, budget, and escalation decisions beyond manager-level resolution

## Change management

### Resistance handling
1. **Skeptical engineer**
   - Likely concern: AI-assisted feature and delivery controls create overhead or reduce engineering autonomy
   - Response pattern: show evidence of reduced rework, keep technical quality gates explicit, involve engineer champions in tool/prompt review
2. **Anxious BA / business analyst**
   - Likely concern: new delivery artifacts and AI-native practices will make requirements work less clear or less valued
   - Response pattern: anchor adoption in better traceability, require artifact-based sign-off, pair with champions on early reuse cases
3. **Busy stakeholder**
   - Likely concern: ceremonies and approvals add time with unclear benefit
   - Response pattern: shorten updates to decision-ready summaries, escalate only when a decision is needed, track missed decisions as delivery risk

### Adoption tracking
1. **Artifact created in version control**
   - Signal of adoption: required delivery/security/ops artifacts are created in repo rather than kept in private notes
   - Measurement: weekly count of required artifacts created or updated in the agreed folder structure
2. **Prompt or template reused by another teammate**
   - Signal of adoption: one person’s AI-native practice becomes team practice
   - Measurement: reuse count in shared files or explicit references in PRs or delivery artifacts
3. **Retro insight committed to a working change**
   - Signal of adoption: retros produce real process change, not only discussion
   - Measurement: number of retrospective actions closed with linked evidence in the next sprint

### Champion network
| Champion | Role | Focus | Protected time |
| --- | --- | --- | --- |
| Aleksei Bushnev | Delivery / engineering bridge | delivery artifacts, AI-native workflow adoption, handoff discipline | 15% |
| Security champion | Security partner | risk gates, evidence-pack quality, control adoption | 10% |
| Ops champion | Platform / operations lead | rollback, runbook, support readiness, cost-cap adoption | 10% |

## Stakeholder map
| Stakeholder | Interest | Influence (H/M/L) | Key concern | Engagement signal to monitor |
| --- | --- | --- | --- | --- |
| Sarah Chen (client executive sponsor) | delivery outcome, budget control, adoption credibility | H | delays, unclear ownership, AI risk exposure | response time on escalations and milestone approvals |
| Client product owner | usable checkout improvement and release confidence | H | scope drift, delivery quality, dependency churn | backlog decision turnaround and attendance in sprint reviews |
| EPAM delivery lead | predictable execution, margin protection, escalation clarity | H | hidden scope, stalled approvals, governance drift | risk-log freshness and closure rate on actions |
| Engineering team | buildable scope and workable cadence | M | overloaded ceremonies, unclear acceptance, unstable dependencies | retro sentiment and completion rate of sprint commitments |

## Comms plan
| Audience | What they get | Channel | Cadence | Owner |
| --- | --- | --- | --- | --- |
| Client executive sponsor / steering committee | milestone status, top 3 risks, decisions needed, budget and readiness summary | steering deck + live meeting | monthly | Delivery Lead |
| Delivery team | sprint goals, dependency changes, blocker list, retro actions, adoption signals | sprint board + standup / review notes | biweekly with in-sprint updates as needed | PM / Engineering Lead |

## Why the two cadences differ
The sponsor has high influence and low tolerance for noise, so communication is decision-focused and monthly unless escalated. The delivery team needs short-cycle execution signals, so cadence is biweekly with operational updates inside the sprint.

## Notes
- This plan treats change management as more than training: it includes resistance handling, adoption tracking, and a named champion network.
- Quality and risk gates are grounded in the carried-forward QA, security, and operations artifacts rather than generic governance language.
