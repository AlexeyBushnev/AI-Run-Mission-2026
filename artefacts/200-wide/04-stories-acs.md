# 04-stories-acs

## User stories

### 1. Investigate a parity defect
As a data quality engineer, I want to start a parity investigation from a defect record, so that I can understand the likely cause faster.

### 2. Review investigation context
As a data engineer, I want to see the relevant defect context in one place, so that I do not waste time gathering the same information manually.

### 3. Generate a root-cause hypothesis
As a data quality engineer, I want the assistant to propose an evidence-backed root-cause hypothesis, so that I can focus my investigation faster.

### 4. Record assumptions and validation steps
As a reviewer, I want every suggested hypothesis to include assumptions and validation steps, so that I can judge whether the conclusion is trustworthy.

### 5. Produce a reusable evidence summary
As a data engineer, I want the investigation to end with a reusable evidence summary, so that future defects can be resolved faster.

### 6. Handle missing or incomplete inputs
As a data quality engineer, I want the assistant to detect missing required inputs, so that I do not rely on a weak or misleading investigation.

### 7. Refuse unsupported conclusions
As a reviewer, I want the assistant to refuse unsupported conclusions, so that the team does not trust hallucinated analysis.

### 8. Show investigation status
As a user, I want to see whether the investigation is in progress, blocked, or ready for review, so that I know what to do next.

### 9. Reuse prior investigation patterns
As a data quality engineer, I want to reuse prior investigation patterns for similar defects, so that repeated parity issues are handled more consistently.

### 10. Support human review before closure
As a reviewer, I want the investigation output to require human review before closure, so that the final engineering decision stays human-owned.

---

## Acceptance criteria for top stories

### Story 1 — Investigate a parity defect

**AC 1.1**  
Given a valid defect record with required investigation inputs,  
When the user starts an investigation,  
Then the system creates a new investigation run linked to that defect.

**AC 1.2**  
Given an investigation run has started,  
When the required context is loaded,  
Then the user can view the defect scope, related outputs, and investigation status in one place.

**Error path**  
Given a defect record is missing required inputs,  
When the user starts an investigation,  
Then the system must stop the run and show which required inputs are missing.

**NFR**  
The investigation run must be created and the initial context displayed within **10 seconds** for 95% of runs.

---

### Story 2 — Review investigation context

**AC 2.1**  
Given a valid investigation run exists,  
When the user opens the investigation context,  
Then the system shows the defect identifier, affected scope, and linked evidence sources.

**AC 2.2**  
Given linked context artifacts exist,  
When the user opens the context view,  
Then the system shows the latest available versions of those artifacts.

**Error path**  
Given one or more context artifacts cannot be loaded,  
When the user opens the context view,  
Then the system must show which artifact failed and continue showing the artifacts that are available.

**NFR**  
The context view must load within **5 seconds** for 95% of requests and must preserve a readable structure for manual review.

---

### Story 3 — Generate a root-cause hypothesis  
**AI Eval Card stub**

- **Confidence threshold:** show a root-cause hypothesis only when model confidence is **≥0.75**
- **Refusal trigger:** refuse to generate a conclusion when required evidence is missing, contradictory, or below the minimum evidence threshold
- **Latency ceiling:** first hypothesis response within **30 seconds** for 95% of runs
- **Fallback:** if the threshold is not met, return “insufficient evidence for a hypothesis” and list the next validation steps the engineer should run

**Patched edge/error path**  
If two evidence sources strongly contradict each other, the assistant must not select one silently; it must flag the contradiction and request human review.

**Patched NFR**  
The assistant must log the evidence references used in the hypothesis so the reviewer can trace the suggestion.

---

### Story 4 — Record assumptions and validation steps

**AC 4.1**  
Given the assistant proposes a hypothesis,  
When the result is displayed,  
Then it includes the explicit assumptions used to form the hypothesis.

**AC 4.2**  
Given the assistant proposes a hypothesis,  
When the result is displayed,  
Then it includes at least one validation step the engineer can perform next.

**AC 4.3**  
Given the reviewer opens the result,  
When assumptions or validation steps are missing,  
Then the investigation cannot be marked ready for review.

**Error path**  
Given the hypothesis output is incomplete,  
When the user tries to submit it for review,  
Then the system blocks submission and identifies the missing fields.

**NFR**  
Assumptions and validation steps must be written in plain language that another engineer can follow without extra explanation.

---

## Adversarial pass — strongest critique points captured

1. Some original stories did not say what happens when defect data is incomplete.
2. The AI story was too optimistic and did not clearly define refusal behavior.
3. The draft ACs were weak on NFRs, especially latency and traceability.
4. Review-stage controls were not strong enough to stop incomplete outputs from being treated as done.

---

## Patch summary after adversarial pass

1. Added explicit missing-input error path to Story 1.
2. Added partial-load error path to Story 2.
3. Added contradiction refusal rule and evidence-trace requirement to Story 3.
4. Added review-blocking rule for incomplete outputs in Story 4.
5. Added at least one NFR to each top story.
