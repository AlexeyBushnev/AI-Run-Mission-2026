# Meridian Retail Group — fresh-session review

## Three sharpest concerns

### 1. Phase 2 exit is still vulnerable to hidden scope
**Concern:** “Implemented and testable end to end” is directionally good, but a buyer could still argue that non-functional readiness, support readiness, or edge-case integrations were implicitly included before Phase 3 starts.

**Patch applied:** Phase boundaries were tightened so AI controls, rollback, and operational readiness are explicitly moved into Phase 3, while Phase 2 is limited to the baseline non-AI checkout path being implemented and testable.

### 2. The sub-vendor governance could be exploited if acceptance evidence is vague
**Concern:** A named subcontractor with “templates and recommendations” can become a soft dependency unless the evidence they owe and the gate they pass through are explicit.

**Patch applied:** The outline now names the required evidence from N&N — policy config documentation, test evidence, rollback notes, and cost-control assumptions — and states that they do not deliver directly to Meridian unchecked.

### 3. Client-side decision latency is a real delivery risk and could be disputed later
**Concern:** The assumptions mention named decision-makers, but the consequence of delayed decisions is not fully visible in the outline. A buyer may later treat blocked decisions as vendor delay.

**Patch applied:** The phase-entry and key-assumption language were tightened to require named decision-makers and phase sign-offs within bounded windows, so delayed client decisions are visible as dependency risk rather than silent delivery slippage.

## Weakest part attacked
The weakest part was **Phase 2 boundary clarity**, because that is the place where delivery teams most often absorb unstated scope before the estimate is even built.

## Patch summary
The solution outline was updated so:
- Phase 2 stops at the stable non-AI checkout path
- Phase 3 owns AI summary, controls, gateway/cost/security hardening, and rollback readiness
- Sub-vendor evidence and gate expectations are explicit
- Client decision dependency language is tighter and more falsifiable
