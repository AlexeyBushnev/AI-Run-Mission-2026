# Meridian Retail Group — proposal pack

## Executive summary
Meridian Retail Group is seeking a delivery partner to modernize its checkout experience and introduce a governed AI-assisted cart-summary capability without losing control of cost, security, or operational support. We propose a phased modernization of the checkout-service flow for web and mobile, followed by controlled enablement of the “summarise my cart” feature through Meridian’s approved AI gateway, with security, operations, QA, data, and delivery evidence built in from the start rather than added after release.

We believe this proposal is strong for three reasons. First, it is **integrated end to end**: the solution, delivery model, test/reporting evidence, cloud operations readiness, and security controls are already aligned to one carried-forward chain rather than written as separate promises. Second, it is **governed AI delivery**, not AI as decoration: the proposal includes gateway-based model access, cost-cap recommendations, rollout controls, and a security evidence pack that makes the AI feature operable and reviewable. Third, it is **credible to run**, not only to build: the pack includes rollback-aware deployment, incident/runbook thinking, stakeholder-driven rollout governance, and support handover rather than assuming the buyer will infer these later.

Our recommended commercial model is **hybrid**: fixed-price against a tightly bounded core modernization scope, with controlled change mechanisms and explicit assumptions around client dependencies, gateway access, and any scope beyond the approved checkout and cart-summary chain. The top delivery risk is fixed-price compression against evolving scope and AI governance requirements. We mitigate that through explicit assumptions, a defined open-items log, a phased delivery boundary, and governance gates that separate approved baseline scope from additional change.

**Proposed team lead:** Delivery Lead / Program Manager (named in the staffing and rollout plan)  
**Named reference:** Meridian-style omnichannel commerce modernization with governed AI feature delivery (reference to be confirmed in bid defence)

---

## RFP response matrix

| Criterion | Weight | How we meet it | Evidence |
| --- | ---: | --- | --- |
| Solution fit to scope, constraints, and target architecture | 25% | We propose a phased checkout modernization with governed AI cart summary, rollback-aware deployment, and explicit in/out scope boundaries | `02-solution.md`, `05-plan.md`, Module 400 architecture pack |
| Delivery approach, staffing realism, and rollout readiness | 20% | We provide phased delivery, differentiated staffing variants, governance cadence, champion network, and rollout/hypercare structure | `03-staffing.xlsx`, `05-plan.md`, `05-timeline.md` |
| Security, compliance, and operational support model | 20% | We include threat modeling, mitigation, evidence pack, deploy-manifest audit, CI/CD supply-chain audit, incident runbook, cost cap, and readiness brief | Module 800 pack, Module 900 evidence pack, `04-evidence.md`, `06-readiness-brief.md` |
| Commercial value and total cost of ownership | 20% | We provide a repaired estimate with separate contingency and margin, a bounded assumptions register, and AI cost/cap visibility | `04-estimate.xlsx`, Module 800 `05-cost-estimate.md` |
| Relevant proof, references, and execution confidence | 10% | The proposal is grounded in carried-forward artifacts from PM/BA, design, architecture, engineering, QA, data, operations, and security rather than generic claims | Modules 200–900 artifact chain, especially M500, M600, M800, M900 |
| Price | 5% | Pricing is presented transparently with role × phase effort, delivery impacts, contingency, margin, and a hybrid commercial recommendation | `04-estimate.xlsx` |

---

## 1. Qualification summary
From the qualification memo, this is a **bid with conditions**. Capability and strategic fit are strong; commercial fit is acceptable only if AI spend, scope boundaries, and client-side dependency assumptions are made explicit. The pack retains the named deal-breaker: fixed-price without bounded scope, client dependency commitments, and AI spend governance should move this to no-bid.

Reference: `01-qualification.md`

## 2. Solution summary
The proposed solution is a four-phase delivery:
1. mobilize and confirm scope
2. build and integrate core checkout modernization
3. add governed AI cart summary and harden controls
4. UAT, rollout, and hypercare transition

The outline also includes an explicitly governed outsourced capability for advanced AI gateway policy integration and cost-governance automation, with named evidence requirements and escalation path.

Reference: `02-solution.md`  
Fresh-session critique and patch record: `02-review.md`

## 3. Staffing summary
The pack uses the **recommended balanced-to-hybrid delivery posture** rather than presenting variants as cosmetic headcount changes. Lean, balanced, and fast variants were defined as different bets; the recommendation selected the option that best supports predictable delivery and controlled risk for Meridian’s timeline and scope.

Linked workbook: `03-staffing.xlsx`

## 4. Estimate summary
The estimate has been repaired to separate:
- base effort
- delivery impacts
- contingency
- margin

It includes:
- active mitigation on every named risk
- bounded assumptions
- a commercial-model recommendation aligned to the buyer constraint and risk allocation logic

Recommended commercial model: **hybrid**  
Reason: this best balances buyer demand for cost predictability with the reality of dependency, AI-governance, and integration risk.

Linked workbook: `04-estimate.xlsx`

## 5. Implementation and rollout summary
The plan includes:
- milestone table with entry/exit criteria and owners
- steering, sprint, and retrospective cadence with decision rights
- named executive sponsor
- change-management coverage beyond training alone
- champion network with protected time
- stakeholder map with engagement signals
- differentiated comms cadence for different audiences

References:
- `05-plan.md`
- `05-timeline.md`

## 6. AI-native delivery summary
The proposal includes a measurable AI-native delivery section across:
- intake
- plan
- build
- validate
- handoff
- learn

Each phase names:
- target maturity by month
- adoption metric with denominator
- tooling baseline with allow-list status
- one named risk

It also explicitly names what remains human-owned, so the proposal does not imply unsafe automation.

Reference: `06-ai-native.md`

---

## Reconciliation notes
The proposal pack was reconciled across the prior artifacts to remove internal drift.

### Reconciled items
- **Estimate vs staffing:** estimate aligns to the recommended staffing posture rather than contradicting it with a different implied team shape
- **Plan vs phases:** rollout milestones match the four phases in `02-solution.md`
- **AI-native tools vs budget/governance:** AI-native section uses approved / controlled tooling assumptions consistent with the governance and cost sections, and does not imply unbudgeted or non-approved tools
- **Risk posture vs commercial model:** hybrid model is used consistently because pure fixed-price would understate delivery and governance risk

### Known synchronized proposal stance
- phased checkout modernization first
- governed AI cart-summary second
- security, operations, and support evidence embedded
- hybrid commercial framing with explicit assumptions and open items

---

## Open items log
| Open item | Why it matters | Owner needed |
| --- | --- | --- |
| Named buyer-side executive sponsor confirmation | Governance and escalation require written unblock authority | Meridian |
| Final named customer reference for executive summary | Strengthens proof and execution confidence in bid defence | EPAM pursuit lead |
| Final legal/compliance confirmation of engagement tooling shape | Needed before non-default tool assumptions are committed | Legal / compliance |
| Sub-vendor commercial and contractual confirmation for N&N capability | Required if outsourced capability remains in the final solution | Delivery lead / procurement |
| Final agreement on AI spend cap ownership and response path | Needed to turn the cost-control recommendation into an operational commitment | Product + operations sponsor |

---

## Proposal pack structure
- `00-rfp.md`
- `01-qualification.md`
- `02-solution.md`
- `02-review.md`
- `03-staffing.xlsx`
- `04-estimate.xlsx`
- `05-plan.md`
- `05-timeline.md`
- `06-ai-native.md`

This pack is intended to read as one coherent voice rather than a bundle of disconnected sections. The supporting evidence from Modules 100–900 is the proof layer behind the bid, especially for quality, security, operations, and engineering credibility.
