# 01-vision

## Initial vision

The Parity Investigation Assistant helps data quality engineers and data engineers investigate parity defects between legacy and migrated IoT pipelines faster and more consistently. Instead of running an ad hoc manual investigation each time, the team uses one AI-assisted flow that proposes evidence-backed root-cause hypotheses, records assumptions and validation steps, and leaves a reusable investigation artifact under human review. The goal is to reduce average parity-investigation time from the current baseline to **at least 25% lower within the pilot period**, while keeping evidence-review acceptance stable.

## Problem statement

Parity defects take too long to investigate today, which delays reporting decisions and reduces trust in migrated data outputs.

## Target user

Data quality engineers and data engineers investigating parity defects in migrated IoT data pipelines.

## Outcome metric

Average parity-investigation time, measured weekly from defect assignment to reviewed root-cause note; target: **≥25% reduction during the pilot** with no drop in evidence-review acceptance.

## Adversarial critique (fresh-session capture)

1. **The baseline is not defined clearly enough.** “Current baseline” is vague unless it names how it is measured and which cases are included.
2. **The output sounds useful, but the decision boundary is weak.** The draft says the assistant helps, but not what makes the pilot succeed or fail.
3. **The user value is indirect.** The draft explains internal efficiency, but it should connect more clearly to business impact: faster trusted reporting and lower delivery friction.

## Revised vision

The Parity Investigation Assistant helps data quality engineers and data engineers investigate parity defects between legacy and migrated IoT pipelines faster, with more consistent evidence output, under human review. For the pilot, the team will compare the same class of parity defects against a manually investigated baseline measured from defect assignment to reviewed root-cause note. The feature succeeds if it reduces average investigation time by **at least 25%** across the pilot cases without lowering evidence-review acceptance, so reporting decisions can be made faster with less rework and stronger trust in migrated data outputs.
