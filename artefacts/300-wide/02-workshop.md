# 02-workshop

**consumes_from:** `artefacts/300-wide/01-journey-map.md`, `artefacts/300-wide/01-heuristics.md`

## Workshop plan

**Decision to close:**
Do we show estimated store availability with a visible confidence / uncertainty cue on the product page, or hide availability until store confirmation exists?

**Decision-owner:**
Sarah Chen — Head of CX

**Participants:**

* Sarah Chen — Head of CX
* David Park — Retail Ops
* Marco Rossi — Regional GM
* Engineering Lead
* Product / Design facilitator

**Goal:**
Close one decision about how Meridian should handle uncertain store availability before the shopper commits to pickup.

**Must decide:**

* Whether availability is shown as a confident fact or as an estimate with uncertainty
* Whether the user sees uncertainty before reservation
* Whether an alternative store suggestion is part of the first design direction

**Must explore:**

* User reactions to confidence / uncertainty language
* Ways to reduce wasted trips without removing all speed from the flow
* Alternative interaction patterns for uncertain stock

**Out of scope:**

* Pricing
* Loyalty
* Store staffing policy
* Full inventory-platform redesign

**Timeboxes:**

* 5 min — frame the decision and success condition
* 15 min — diverge with HMW questions and ideas
* 10 min — converge on the strongest design direction for next-step prototyping

---

## HMW questions

### Theme 1 — Make uncertainty visible before commitment

1. How might we show that store availability is an estimate, not a guarantee?
2. How might we help the shopper understand stock confidence before reserving?
3. How might we signal stale or weak stock data without killing trust?
4. How might we prevent the binary “In stock” promise when certainty is low?

### Theme 2 — Reduce the wasted-trip risk

5. How might we help shoppers avoid driving to a store for nothing?
6. How might we warn the shopper at the right moment if pickup confidence is weak?
7. How might we give the shopper a safer choice when store stock is uncertain?

### Theme 3 — Recover gracefully when the preferred store is risky

8. How might we suggest a better nearby option before the shopper commits?
9. How might we keep the journey moving when the first store is a weak choice?
10. How might we preserve trust even when Meridian cannot promise shelf availability?

---

## Divergent ideas

### Theme 1 — Make uncertainty visible before commitment

1. Replace “In stock” with a confidence-based label such as “Likely available” when certainty is below a defined threshold.
2. Add a freshness note under availability, for example “Updated 18 minutes ago.”
3. Show a simple confidence indicator with plain-language explanation before reservation.

### Theme 2 — Reduce the wasted-trip risk

1. Add a warning state before reservation when confidence is low: “Availability may change before pickup.”
2. Offer a “Check with store” action when inventory freshness or confidence is below threshold.
3. Delay strong confirmation language until a stronger store-level signal exists.

### Theme 3 — Recover gracefully when the preferred store is risky

1. Suggest the nearest store with higher-confidence availability before the user reserves.
2. Show two store options side by side: closest store vs most reliable store.
3. Offer a backup path such as delivery or another store when local confidence is weak.

---

## Facilitation note

During divergence, do not judge ideas. Capture all options first.
The workshop succeeds if it closes the decision on **how Meridian should present uncertain availability before the shopper commits**.
