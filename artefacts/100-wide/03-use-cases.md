# 03-use-cases

**Input pain points**
1. Product trust is now a market issue, not just an engineering issue.  
2. Competition is shifting from single devices to connected ecosystems.  
3. Internal data quality becomes strategy-critical when products, reporting, and compliance all depend on telemetry.

## Candidate use cases and scoring

| # | Use case | Type | Pain point | Value (1–5) | Value rationale | Feasibility (1–5) | Feasibility rationale | Total |
|---|---|---|---|---:|---|---:|---|---:|
| 1 | Device-telemetry anomaly detection for early defect discovery | Classical ML | 1, 3 | 5 | Could reduce trust-damaging field issues and reporting errors early. | 4 | Data likely exists, but production tuning and alert quality matter. | 20 |
| 2 | LLM support-ticket summarizer for thermostat/device failures | Generative AI | 1 | 3 | Useful for faster triage, but mainly operational efficiency. | 5 | Easy to pilot with existing ticket text. | 15 |
| 3 | Agentic parity-investigation assistant for migration defects | Agentic | 3 | 5 | Directly targets slow investigations and weak trust in migrated outputs. | 4 | Feasible with repo context, rules, and human checkpoints. | 20 |
| 4 | Energy-usage forecast for customer-facing recommendations | Classical ML | 2 | 3 | May improve product value, but indirect to the current core pain. | 3 | Needs stable historical data and validation. | 9 |
| 5 | LLM-generated customer incident explanations from telemetry evidence | Generative AI | 1, 3 | 4 | Improves trust and communication when issues happen. | 3 | Useful, but risky without strong grounding and review. | 12 |
| 6 | Agentic root-cause workflow for cross-system reliability incidents | Agentic | 1, 3 | 5 | High value if it cuts time from symptom to root cause across teams. | 3 | Harder because it crosses data, code, and system boundaries. | 15 |
| 7 | Churn-risk model for connected-device disengagement | Classical ML | 2 | 2 | Possible business value, but weaker link to validated primary pain. | 3 | Technically possible, but signal quality may be weak. | 6 |
| 8 | LLM installer/support copilot for knowledge retrieval and answer drafting | Generative AI | 1, 2 | 3 | Improves support consistency, but not a distinctive strategic edge. | 5 | Straightforward to build with existing knowledge sources. | 15 |
| 9 | Agentic compliance-evidence pack generator from telemetry/reporting changes | Agentic | 3 | 4 | Useful where reporting and controls need audit-ready evidence. | 3 | Feasible, but depends on clean source artifacts and boundaries. | 12 |
| 10 | Multi-device household behavior clustering for cross-sell journeys | Classical ML | 2 | 2 | More commercial than urgent for the validated pain set. | 2 | Needs strong consent, data quality, and activation design. | 4 |

## Deduplication note

Near-duplicates reviewed:
- #3 and #6 overlap, but are not duplicates.  
  #3 is focused on migration parity defects; #6 is broader cross-system incident root cause.
- #2 and #8 overlap partly, but are not duplicates.  
  #2 summarizes failure tickets; #8 is a broader support/installer copilot.

## Top 3 by score

1. **Device-telemetry anomaly detection for early defect discovery** — 20  
2. **Agentic parity-investigation assistant for migration defects** — 20  
3. **Agentic root-cause workflow for cross-system reliability incidents** — 15  

## Commodity check on top 3

### 1. Device-telemetry anomaly detection for early defect discovery
**Commodity check:** Partly commodity.  
General anomaly detection is widely available in observability platforms, including edge/device monitoring with anomaly detection and outlier detection.  
**Decision:** Keep, but only if scoped to thermostat / smart-home telemetry patterns and linked to domain-specific defect signatures rather than generic anomaly alerts.

### 2. Agentic parity-investigation assistant for migration defects
**Commodity check:** Not commodity.  
This is strongly project-specific because it depends on your repo, data products, migration rules, parity logic, and human review flow.  
**Decision:** Keep.

### 3. Agentic root-cause workflow for cross-system reliability incidents
**Commodity check:** Not fully commodity.  
Many vendors support observability and alerting, but the agentic workflow that traces from incident signal to code/data/root-cause package inside your delivery context is not a standard off-the-shelf product.  
**Decision:** Keep.

## Final top 3 to carry forward

1. **Agentic parity-investigation assistant for migration defects**  
   Strongest fit to the validated telemetry-trust pain and current project reality.

2. **Device-telemetry anomaly detection with domain-specific defect patterns**  
   Valuable if kept domain-shaped, not just generic observability anomaly detection.

3. **Agentic root-cause workflow for cross-system reliability incidents**  
   High value for reliability trust, though operationally harder than the first two.
