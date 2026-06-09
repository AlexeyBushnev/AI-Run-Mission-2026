# 05-report

## 1. Coverage
We tested the Click & Collect journey across the highest-risk Phase 1 surfaces defined in `00-test-plan.md`: loyalty/account resolution, cart and reservation continuity, SAP-backed inventory check at pickup confirmation, EU pickup-confirmation payment flow with PSD2 SCA, and customer/associate error-handling for stock, identity, and payment failures. The executed focus set covered 10 priority cases drawn from `01-test-cases.md`, including critical-path, edge, and negative scenarios. We did **not** test SAP ECC inventory ground-truth correctness across the enterprise, full omnichannel coverage outside the Click & Collect journey, or Phase 2 cross-channel reservation patterns.

## 2. Pass rate and defect density
Because `03-defects.md` in this chain was prepared as a manual execution worksheet rather than a filled defect log, the numeric outcome below is marked **[ESTIMATED]** and should be replaced with actual session counts if available.

- **Critical-path:** 6/6 executed **[ESTIMATED]**
- **Edge:** 2/2 executed **[ESTIMATED]**
- **Negative:** 2/2 executed **[ESTIMATED]**
- **Overall executed:** 10/10 **[ESTIMATED]**

**Defect density [ESTIMATED]**
- SAP inventory / pickup confirmation: **3 defects / 6 relevant cases**
- Identity stitch / account resolution: **2 defects / 4 relevant cases**
- Loyalty credit / post-pickup crediting: **1 defect / 3 relevant cases**
- EU PSD2 SCA payment confirmation: **1 defect / 3 relevant cases**

These numbers reflect the risk concentration implied by the RCA and case mix, not a completed defect-count export. Replace them with session-actual values before using this report for a real rollout gate.

## 3. Top 2 problematic areas
1. **SAP-backed inventory freshness at pickup confirmation**  
   The most painful risk cluster remains phantom-stock behavior at the store: the feature can still fail when pickup confirmation depends on stale inventory state or missing held-stock protection. This is the area most likely to drive customer-visible cancellations at pickup and operational escalation.

2. **Identity resolution across web-to-store handoff**  
   The second highest-risk area is loyalty/account stitching, especially in merged-account or cross-region scenarios. Failures here can block pickup, mis-credit loyalty, or create privacy/compliance exposure if the wrong customer identity is resolved.

## 4. 5-item improvement backlog
1. **Add a held-stock token at Click & Collect reservation time and enforce it at pickup** — removes the inventory-race condition behind phantom-stock cancellations — **Engineering / Meridian platform team** — **P1**
2. **Enforce a 30-second freshness ceiling on SAP-backed pickup confirmation reads, with deterministic fallback behavior** — closes the stale-inventory path identified in `04-rca.md` — **Engineering / Meridian platform team** — **P1**
3. **Implement a deterministic identity-merge resolution rule with explicit escalation on conflicts** — reduces wrong-account retrieval and privacy-risk scenarios — **Engineering + Privacy / Compliance** — **P1**
4. **Add a PSD2 SCA failure recovery flow that preserves the reservation for a short retry window instead of failing hard immediately** — reduces EU drop-off and improves pickup completion resilience — **Engineering + CX** — **P2**
5. **Publish a daily operational dashboard for phantom-stock, identity-stitch failures, and cross-region pickup attempts** — gives Retail Ops and rollout leads a concrete go/no-go signal for next-country expansion — **Data + Retail Ops** — **P3**

## Release-readiness note
This report supports a **conditional rollout** view only. The scoped journey has good coverage on the highest-risk surfaces, but the inventory-freshness and identity-resolution clusters remain the two main blockers to broad expansion. Before rolling Click & Collect to the next two countries, replace the estimated execution metrics with actual defect/run data and confirm whether P1 backlog items 1–3 are fixed, mitigated, or explicitly accepted.
