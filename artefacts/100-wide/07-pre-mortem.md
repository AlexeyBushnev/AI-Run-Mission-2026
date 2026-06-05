# 07 Pre-mortem — Steering Committee Weaknesses

Source reviewed: `06-deck.pdf`

Role: most sceptical board member in a fresh review.

## Ranked top 3 weaknesses

### 1. Severity: Critical — ROI is asserted before it is evidenced

**One-line rationale:** The deck asks for approval while admitting the pessimistic case still needs validation, so the funding logic can be challenged as premature.

**Specific slide and line creating the weakness:**  
- Slide 06, line 1: “Base case pays back in 12 months; optimistic case in 3 months; pessimistic case requires more validation before funding.”

**Patch — slide-text change, no new slide:**  
Replace Slide 06 body text with:

> “ROI will be validated during the 30-day pilot: base case is payback within 12 months, optimistic case within 3 months, and continuation is gated on measured investigation-time reduction across three historical defect cases.”

---

### 2. Severity: High — The core value metric is not operationally defined

**One-line rationale:** “Reduce average investigation time by 40%” is compelling, but the deck does not define baseline, measurement method, sample size, or pass/fail threshold.

**Specific slide and line creating the weakness:**  
- Slide 05, line 1: “Target outcome: reduce average parity-investigation time by 40% while keeping human review and evidence quality intact.”
- Slide 07, line 1: “Binding risk: performance tracking. Without baseline metrics, the team cannot prove whether the assistant saves time or just moves work around.”

**Patch — speaker-note change, no new slide:**  
Add this speaker note to Slide 05:

> “For the pilot, ‘average parity-investigation time’ means engineer hours from defect assignment to reviewed root-cause note. Baseline comes from the same three historical defect cases run manually. Pilot success requires at least 25% time reduction without lowering evidence-review acceptance.”

---

### 3. Severity: Medium — The solution sounds like a generic AI helper, not a controlled delivery capability

**One-line rationale:** The assistant “suggests root causes” and “guides evidence capture,” but the deck does not state what prevents hallucinated analysis, unsafe recommendations, or inconsistent artifacts.

**Specific slide and line creating the weakness:**  
- Slide 04, line 1: “Agentic parity assistant reads context, compares outputs, suggests root causes, guides evidence capture, and leaves a reviewed investigation artifact.”
- Slide 03, line 1: “A shared AI-assisted investigation workflow can turn repeated parity debugging into a reusable delivery capability, not another one-off chat.”

**Patch — slide-text change, no new slide:**  
Replace Slide 04 body text with:

> “Agentic parity assistant reads approved context, compares outputs, proposes evidence-backed root-cause hypotheses, records assumptions and validation steps, and leaves a human-reviewed investigation artifact.”

## Summary steering-committee failure mode

The proposal is likely to fail not because the use case is weak, but because the current deck asks for approval before the measurement system is tight enough. The fastest repair is to convert the ask from “fund an assistant” into “approve a controlled 30-day measurement pilot with explicit continuation gates.”
