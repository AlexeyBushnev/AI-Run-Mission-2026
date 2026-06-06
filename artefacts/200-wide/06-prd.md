# Parity Investigation Assistant

## Description
Parity Investigation Assistant helps data quality engineers and data engineers investigate parity defects between legacy and migrated IoT pipelines faster, with human review and reusable evidence output. The target outcome is to reduce average parity-investigation time by **at least 25%** during the pilot, measured weekly from defect assignment to reviewed root-cause note, without lowering evidence-review acceptance.

## Target User
Primary users are data quality engineers and data engineers investigating parity defects in migrated IoT data pipelines. Secondary user is the reviewer who accepts or rejects investigation output based on evidence quality.

## Top User Stories
1. **Investigate a parity defect** — start an investigation from a defect record and load the required context in one place.  
   **AC:** If required inputs exist, the system creates a linked investigation run; if inputs are missing, the run is blocked and missing inputs are shown.

2. **Review investigation context** — see defect scope, evidence sources, and relevant context without manual searching.  
   **AC:** The context view shows linked artifacts and partial-load failures explicitly; the view loads within **5 seconds** for 95% of requests.

3. **Generate a root-cause hypothesis** — receive an evidence-backed hypothesis faster.  
   **AI Eval Card stub:** show a hypothesis only at confidence **≥0.75**; refuse if evidence is missing or contradictory; first response within **30 seconds** for 95% of runs; fallback is “insufficient evidence” plus next validation steps.

4. **Record assumptions and validation steps** — make the output reviewable and trustworthy.  
   **AC:** A hypothesis must include explicit assumptions and at least one validation step; incomplete outputs cannot be submitted for review.

5. **Support human review before closure** — keep the final engineering decision human-owned.  
   **AC:** Investigation output cannot be closed without human review status recorded.

## Scope Boundary
In scope: AI-assisted investigation support, context loading, evidence-backed hypothesis generation, reusable investigation summaries, and human-reviewed output.  
Out of scope: automatic production fixes, automatic defect closure, or final engineering decisions without human review.

## Success Metric
**Primary outcome metric:** average parity-investigation time reduced by **≥25%** during the pilot with no drop in evidence-review acceptance.

## Decision Memory
The biggest scope call was to keep the feature focused on **AI-assisted investigation and reviewed evidence output**, not automated defect fixing. The reason is that trust, review quality, and investigation speed are the validated needs today, while automatic remediation would add higher risk, weaker feasibility, and lower reviewer acceptance. The rejected alternative was an auto-fix assistant that proposes and applies code or pipeline changes directly.
