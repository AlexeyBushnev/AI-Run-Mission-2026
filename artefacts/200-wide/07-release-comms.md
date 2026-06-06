# 07-release-comms

## 1. Release-scope confirmation

### In scope
- Start a parity investigation from a defect record and create a linked investigation run. **[S1]**
- Show investigation context, defect scope, and linked evidence sources in one place. **[S2]**
- Generate an evidence-backed root-cause hypothesis when confidence and evidence thresholds are met. **[S3]**
- Record assumptions and validation steps with the hypothesis output. **[S4]**
- Produce a reusable evidence summary for review and future reuse. **[S5]**
- Detect missing or incomplete required inputs and block weak investigation runs. **[S6]**
- Refuse unsupported conclusions when evidence is missing or contradictory. **[S7]**
- Show investigation status as in progress, blocked, or ready for review. **[S8]**
- Reuse prior investigation patterns for similar defects. **[S9]**
- Require human review before investigation closure. **[S10]**

### Out of scope
- Automatic production fixes
- Automatic defect closure
- Final engineering decision without human review
- Direct code or pipeline changes proposed for execution

### Deferred
- Auto-remediation recommendations after review
- Advanced cross-project pattern learning beyond the current feature scope
- Expanded reviewer analytics and dashboarding

---

## 2. Open risks

| Risk | Owner | Mitigation |
|---|---|---|
| AI hypothesis quality is lower than expected on real parity defects | Aleksei Bushnev | Validate against pilot cases and enforce refusal/fallback behavior before release |
| Required investigation inputs are incomplete or inconsistent across defects | Mariia Koval | Define minimum-input checks and block investigation runs when required fields are missing |
| Reviewers do not trust the generated evidence package enough to adopt it | Yuri Bredzikhin | Require explicit assumptions, validation steps, and traceable evidence references in every reviewable output |

---

## 3. Stakeholder notification

### A. Delivery leads
**Subject:** Parity Investigation Assistant — planned release scope and readiness status

We are preparing the initial release of the Parity Investigation Assistant for parity-defect workflows in migrated IoT data pipelines. In scope are investigation start, context loading, AI-assisted hypothesis generation, reusable evidence summaries, refusal behavior for weak evidence, and mandatory human review before closure. Current open risks are AI hypothesis quality, inconsistent defect inputs, and reviewer trust in generated evidence. Target release timing is after pilot validation of the main success metric: at least 25% reduction in average parity-investigation time with no drop in evidence-review acceptance.

### B. Business / external stakeholders
**Subject:** Upcoming release — faster parity-defect investigations with human-reviewed evidence

We are preparing a first release of a new internal assistant that helps engineering teams investigate parity defects faster and document the result more clearly. The goal is to reduce investigation time while keeping review quality stable, so reporting and migration decisions can move faster with better evidence. The initial release is focused on investigation support only; it will not make automatic production decisions or apply fixes without human review.

---

## 4. What’s New / release note

- Engineers can now start a parity investigation from a defect record and create a linked investigation run. **[S1]**
- Investigation context and linked evidence sources are now shown in one place to reduce manual lookup. **[S2]**
- The assistant can propose an evidence-backed root-cause hypothesis when confidence and evidence thresholds are met. **[S3]**
- Investigation outputs now include explicit assumptions, validation steps, and reusable evidence summaries for review. **[S4][S5]**
- Human review is required before closure, and unsupported conclusions are refused when evidence is missing or contradictory. **[S7][S10]**

---

## 5. Spec update after ship

After release, update the **Success Metric** and **Top User Stories / Acceptance Criteria** sections in `06-prd.md` to reflect the shipped scope and measured pilot outcome, and update `06-traceability.md` if any deferred or cut stories changed the release boundary.
