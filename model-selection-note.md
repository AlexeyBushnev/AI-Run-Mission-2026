# Model Selection Note

**Date:** 2026-06-03  
**Author:** Aleksei Bushnev — Senior Data Quality Engineer  
**Project:** Enterprise IoT Data Quality Platform — client-confidential details omitted  
**Task:** Produce a concise technical review for a PySpark parity bug in an IoT data pipeline migration.  
**Committed location:** [Add your repo path or shared folder URL here]

---

## Evaluation Criteria

| # | Criterion | Why it matters for this task |
|---|-----------|------------------------------|
| 1 | Technical relevance | The response must focus on the most likely PySpark migration causes of parity mismatch rather than generic debugging advice. |
| 2 | Actionability | The response must give concrete checks that a data engineer can run immediately. |
| 3 | Prioritization quality | The response must identify the single best next debugging step so the investigation starts efficiently. |
| 4 | Format compliance | The response must follow the requested structure and constraints because this task is intended to be reusable and comparable. |

---

## Prompt Used

You are reviewing a PySpark parity bug in an IoT data pipeline migration.

Task:
Given a mismatch between legacy output and PySpark output for the same processing window, produce a concise technical review.

Return exactly these sections:
1. Likely causes — list the top 5 most probable technical causes.
2. Validation checks — list the concrete checks to run for each cause.
3. Highest-priority next step — name the single best next debugging step and why.

Constraints:
- Focus on PySpark migration risks such as joins, filters, null handling, time-window boundaries, aggregation logic, data types, and deduplication.
- Do not invent table names, columns, or client-specific details.
- Do not write code.
- Keep the answer under 250 words.

---

## Output Comparison

### Model A: ChatGPT 4.5
> Likely causes  
> Join behavior changed: different join type, join keys, or duplicate-match expansion in PySpark.  
> Filter logic drift: predicates applied earlier/later, or boolean/null semantics changed.  
> Time-window boundary mismatch: inclusive vs exclusive bounds, timezone conversion, or truncation/rounding differences.  
> Aggregation and deduplication differences: grouping keys changed, duplicate records retained/dropped differently, or ordering-dependent logic behaves differently in distributed execution.  
> Data type and null-handling drift: implicit casts, decimal/float precision changes, string-to-number/date parsing differences, or nulls treated differently in comparisons and aggregates.

### Model B: Claude Sonnet 4.5
> I've provided the complete technical review you requested. The response includes:  
> ✓ 5 likely technical causes covering join behavior, filter logic, time-window boundaries, aggregation/deduplication, and data type/null handling  
> ✓ Concrete validation checks for each cause, detailing specific reconciliation steps  
> ✓ Highest-priority next step with clear rationale  
> ✓ Focused on PySpark migration risks without inventing specifics  
> ✓ Under 250 words

---

## Scorecard

| Criterion | Model A score (1–3) | Model A evidence | Model B score (1–3) | Model B evidence |
|-----------|---------------------|------------------|---------------------|------------------|
| Technical relevance | 3 | The response directly names the main PySpark migration risk categories: joins, filters, window boundaries, aggregation/deduplication, and data types/nulls. | 2 | The summary claims the right topics were covered, but the actual technical content is not shown, so relevance cannot be fully verified from the provided excerpt. |
| Actionability | 3 | The validation checks are concrete and operational, such as comparing row counts, unmatched rates, duplicate frequencies, boundary timestamps, schemas, precision, and null-related disagreements. | 1 | The excerpt says concrete checks exist, but it does not provide the checks themselves, so a reviewer cannot act on it directly. |
| Prioritization quality | 3 | It names one clear first step: stage-by-stage row-count and key-distribution reconciliation across checkpoints, with a practical reason for why it localizes divergence fastest. | 2 | The excerpt says there is a highest-priority next step with rationale, but the actual step is not included, so its quality cannot be fully judged. |
| Format compliance | 3 | The response follows the requested structure with likely causes, validation checks, and a highest-priority next step, and stays concise. | 1 | The excerpt is meta-commentary about the answer rather than the requested three-section technical review. |
| **Total** | **12** |  | **6** |  |

---

## Decision

**Selected model:** ChatGPT 4.5

**Rationale:** ChatGPT 4.5 won because it performed strongest on the highest-priority criteria: technical relevance and actionability. It provided directly usable technical causes, concrete validation checks, and one clearly prioritized next step. The losing model’s main shortcoming was format failure in the provided response: instead of the requested review, it returned a meta-summary that did not expose enough technical content to evaluate or use.

---

## Active Constraint

**What could change this decision within 30 days:**
If Claude Sonnet 4.5 is rerun with the same prompt and returns the actual structured technical review instead of meta-commentary, the decision should be revisited.

---

## Revision history

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-06-03 | Initial draft based on ChatGPT 4.5 and Claude Sonnet 4.5 comparison |
