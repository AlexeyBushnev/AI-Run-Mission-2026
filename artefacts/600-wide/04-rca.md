# 04-rca

## 1. Defect summary

**Source defect / fallback case**  
SAP inventory sync lag of more than 120 seconds between reservation time and pickup-confirmation time makes the POS show stock that the web layer has already reserved, and the Click & Collect order is cancelled at pickup. Phantom-stock cancellation rate climbs above the documented 7% baseline.

**Why this is the most painful defect**  
- It is customer-visible at the worst possible moment: the shopper arrives at the store and still leaves without the item.
- It directly affects revenue, trust, and Retail Ops workload.
- Once shipped, it is hard to detect early because the reservation looked successful earlier in the journey.

---

## 2. Root cause

**Root-cause hypotheses considered**

1. **Inventory freshness budget missing at pickup confirmation**  
   - Condition: the pickup-confirmation path accepts SAP inventory data older than the safe freshness window.  
   - Evidence to confirm: logs show pickup confirmation using inventory reads older than the allowed threshold.  
   - Evidence to rule out: all failing confirmations used fresh reads within the expected threshold.

2. **Held-stock state is not written or enforced at reservation time**  
   - Condition: the reservation does not create a reliable held-stock token or equivalent compensating state for pickup.  
   - Evidence to confirm: reservation exists in commerce flow, but no held-stock record exists when pickup is attempted.  
   - Evidence to rule out: held-stock token exists and is enforced correctly on every failed pickup.

3. **Race between web reservation and store-side pickup confirmation**  
   - Condition: the web channel and store confirmation path read inconsistent stock states from different timing windows.  
   - Evidence to confirm: timestamps show reservation acceptance and pickup confirmation reading different inventory states for the same SKU/store.  
   - Evidence to rule out: both paths used the same synchronized state and still failed.

4. **Store namespace / region mapping mismatch**  
   - Condition: pickup confirmation reads inventory from the wrong store or region namespace.  
   - Evidence to confirm: failed orders show mismatch between reserved store ID and store queried at pickup.  
   - Evidence to rule out: all failed orders query the correct store namespace.

**Chosen hypothesis**  
The strongest hypothesis is the combination of stale inventory acceptance and missing compensating reservation state.

**Root cause sentence**  
The condition that made this bug possible was that pickup confirmation accepted SAP inventory data older than the safe freshness window and had no enforced held-stock token from reservation time to prevent stale stock from being treated as collectable.

---

## 3. Guard test

### TC-GUARD-01 — Pickup confirmation must reject stale inventory state without held-stock protection
- **Category:** edge
- **Priority:** 1
- **Preconditions:**  
  - A Click & Collect reservation exists for a store/SKU.  
  - Inventory data available to pickup confirmation is older than the allowed freshness threshold.  
  - No valid held-stock token is present for the reserved item.  
- **Steps:**  
  1. Create a reservation in one supported region and let the inventory state age past the allowed freshness threshold.  
  2. Attempt pickup confirmation at the store POS for the reserved item.  
  3. Repeat with a different SKU class or payment method in another supported region.  
  4. Observe the pickup-confirmation result.
- **Expected result:**  
  The system must not confirm pickup from stale inventory alone. It must reject or explicitly escalate the flow, preserve consistent order state, and show a clear stock-unavailable or stock-unverifiable outcome.

### Condition-focused coverage extensions
This guard test should be rerun with:
- a different region/store combination
- a different SKU class
- a different payment method

That prevents the same bug from returning through a neighboring input shape.

---

## 4. Recommended fix

Write and enforce a held-stock token at reservation time, expire it at the reservation-window close, and reject pickup confirmation when the SAP inventory read is older than the defined freshness ceiling.
