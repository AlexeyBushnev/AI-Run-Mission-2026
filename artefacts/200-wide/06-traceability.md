# 06-traceability

## Outcome Metric
**M1:** Average parity-investigation time reduced by **≥25%** during the pilot, with no drop in evidence-review acceptance.

## Traceability Matrix

| Story ID | Story | Moves M1? | How it moves the metric | Status |
|---|---|---|---|---|
| S1 | Investigate a parity defect | Yes | Reduces time to start by creating a linked investigation run with required inputs. | Linked |
| S2 | Review investigation context | Yes | Reduces manual context gathering and switching between tools. | Linked |
| S3 | Generate a root-cause hypothesis | Yes | Speeds early investigation by proposing an evidence-backed starting point. | Linked |
| S4 | Record assumptions and validation steps | Yes | Preserves review quality so time saved does not reduce evidence acceptance. | Linked |
| S5 | Produce a reusable evidence summary | Yes | Lowers repeat-investigation effort and speeds later similar investigations. | Linked |
| S6 | Handle missing or incomplete inputs | Yes | Prevents wasted time on weak investigations and forces early correction. | Linked |
| S7 | Refuse unsupported conclusions | Yes | Protects evidence-review acceptance while keeping the workflow trustworthy. | Linked |
| S8 | Show investigation status | Indirectly | Helps coordination, but has weaker direct effect on investigation-time reduction. | Weakly linked |
| S9 | Reuse prior investigation patterns | Yes | Speeds repeated defect handling through reusable patterns. | Linked |
| S10 | Support human review before closure | Yes | Keeps acceptance stable so time gains remain valid and usable. | Linked |

## Flag Check

### Unlinked stories
None.

### Dead metrics
None. The primary metric has multiple linked stories supporting it.

## Notes
- S8 is the weakest link because it supports coordination more than direct investigation speed.
- No story is unjustified scope under the current single-metric frame.
- If future releases add a second metric for reviewer throughput or evidence quality, S8 and S10 would become more strongly linked.
