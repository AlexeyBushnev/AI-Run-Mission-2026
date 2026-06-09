# 01-test-cases

## In-scope reference
1. Loyalty/account resolution for a shopper who starts online and completes or confirms pickup in-store.
2. Cart and reservation continuity across web, mobile, and store-assisted pickup flow.
3. Store-level availability and pickup confirmation path that depends on SAP-backed inventory signals.
4. EU pickup-confirmation payment path where PSD2 SCA may be triggered.
5. Customer and associate error-handling for stock mismatch, identity mismatch, and payment-confirmation failure.

---

## TC-01 — Milano happy reservation and pickup
- **Category:** critical-path
- **Priority:** 1
- **In-scope item:** 2, 3
- **Preconditions:** Customer has a valid Meridian account; item is available in Milano store; reservation window is open.
- **Steps:**  
  1. Reserve one item on web for Milano pickup.  
  2. Arrive at the Milano store within the reservation window.  
  3. Associate scans the pickup QR.  
  4. Confirm pickup.
- **Expected result:** Reservation is found, SAP-backed availability confirms pickup, customer receives the item, and order state changes to collected.

## TC-02 — Milano happy path with mobile reservation
- **Category:** regression
- **Priority:** 2
- **In-scope item:** 2
- **Preconditions:** Customer uses Meridian mobile app; item is available for pickup.
- **Steps:**  
  1. Reserve item in mobile app.  
  2. Open reservation QR in app at store.  
  3. Associate confirms pickup.
- **Expected result:** Mobile reservation is retrievable in-store and pickup completes successfully.

## TC-03 — Milano boundary pickup at 47h59 of 48h window
- **Category:** edge
- **Priority:** 2
- **In-scope item:** 2, 5
- **Preconditions:** Reservation was created almost 48 hours earlier; pickup window still technically open.
- **Steps:**  
  1. Present reservation 47h59 after creation.  
  2. Associate scans QR.  
  3. Confirm pickup.
- **Expected result:** Reservation is still accepted and pickup succeeds because the window has not expired.

## TC-04 — SAP shows zero stock between reservation and pickup
- **Category:** critical-path
- **Priority:** 1
- **In-scope item:** 3, 5
- **Preconditions:** Reservation exists; SAP inventory changed to zero after reservation.
- **Steps:**  
  1. Customer arrives for pickup.  
  2. Associate scans reservation QR.  
  3. System checks SAP-backed availability.
- **Expected result:** System rejects or escalates pickup confirmation, does not complete collection, and presents a clear stock-mismatch message.

---

## TC-05 — Cross-region reservation: Italian customer, German pickup store
- **Category:** edge
- **Priority:** 2
- **In-scope item:** 2, 5
- **Preconditions:** Customer account is registered in Italy; chosen pickup store is in Germany; feature enabled for both regions.
- **Steps:**  
  1. Customer reserves in Italy-facing channel.  
  2. Pickup is set to a German store.  
  3. Associate retrieves reservation in Germany.
- **Expected result:** Reservation is visible across regions, store context is correct, and pickup can proceed if policy allows it.

## TC-06 — Cross-region happy path with multilingual customer details
- **Category:** regression
- **Priority:** 3
- **In-scope item:** 2
- **Preconditions:** Cross-region reservation exists with localized UI and customer data.
- **Steps:**  
  1. Reserve item in one region.  
  2. Pick up in another supported region.  
  3. Confirm collection.
- **Expected result:** Reservation continuity works and user-visible details remain coherent across regions.

## TC-07 — Cross-region partial pickup on multi-item reservation
- **Category:** edge
- **Priority:** 2
- **In-scope item:** 2, 3
- **Preconditions:** Reservation has multiple items; one item is available, one is delayed.
- **Steps:**  
  1. Customer arrives at pickup store.  
  2. Associate retrieves the reservation.  
  3. One item is handed over and one remains unavailable.
- **Expected result:** System supports or clearly rejects partial pickup according to policy, and final order state is accurate.

## TC-08 — Region not live for Click & Collect
- **Category:** negative
- **Priority:** 2
- **In-scope item:** 5
- **Preconditions:** Customer attempts pickup in a region where Click & Collect is not enabled.
- **Steps:**  
  1. Attempt to retrieve reservation at unsupported region/store.  
  2. Associate scans QR or enters reservation reference.
- **Expected result:** System refuses the flow cleanly and surfaces a clear message that the pickup location is unsupported.

---

## TC-09 — Identity stitch on first in-store pickup after web sign-up
- **Category:** critical-path
- **Priority:** 1
- **In-scope item:** 1
- **Preconditions:** Customer signed up online and has not yet completed an in-store pickup.
- **Steps:**  
  1. Reserve item online.  
  2. Arrive at store and present QR / loyalty identifier.  
  3. System resolves account identity.
- **Expected result:** Correct account is resolved and pickup proceeds without duplicate-account confusion.

## TC-10 — Identity stitch with existing loyalty profile
- **Category:** regression
- **Priority:** 2
- **In-scope item:** 1
- **Preconditions:** Customer has both an online account and an existing loyalty profile expected to be linked.
- **Steps:**  
  1. Reserve item online.  
  2. Present loyalty ID in store.  
  3. Associate retrieves reservation.
- **Expected result:** Linked identity is resolved correctly and no duplicate customer record is used.

## TC-11 — Loyalty ID resolves to two merged accounts with conflicting tiers
- **Category:** negative
- **Priority:** 1
- **In-scope item:** 1, 5
- **Preconditions:** Test data contains conflicting merged-account scenario.
- **Steps:**  
  1. Customer presents loyalty identifier.  
  2. System attempts account resolution.  
  3. Associate tries to continue pickup.
- **Expected result:** System blocks automatic resolution or escalates to manual review; it must not expose the wrong account or complete pickup against the wrong identity.

## TC-12 — Pickup attempted with different government ID than reservation name
- **Category:** negative
- **Priority:** 1
- **In-scope item:** 1, 5
- **Preconditions:** Reservation exists under one customer identity; presenter identity does not match policy.
- **Steps:**  
  1. Associate retrieves reservation.  
  2. Customer presents mismatching ID.  
  3. Associate attempts confirmation.
- **Expected result:** System or process rejects pickup or requires approved override path; item is not handed over without valid match.

---

## TC-13 — Loyalty-points credit for partial pickup
- **Category:** critical-path
- **Priority:** 2
- **In-scope item:** 2, 5
- **Preconditions:** Multi-item order exists; loyalty program active; one item will be collected.
- **Steps:**  
  1. Retrieve partial-pickup reservation.  
  2. Confirm collection of one item only.  
  3. Check loyalty points outcome.
- **Expected result:** Loyalty credit reflects only the collected item(s) and does not over-credit the customer.

## TC-14 — Loyalty credit visible within expected window
- **Category:** regression
- **Priority:** 3
- **In-scope item:** 5
- **Preconditions:** Successful pickup completed; loyalty account active.
- **Steps:**  
  1. Complete pickup.  
  2. Refresh loyalty view in app/web.  
  3. Verify points visibility.
- **Expected result:** Loyalty points appear within the expected time window for successful pickup.

## TC-15 — Loyalty program unavailable during pickup completion
- **Category:** negative
- **Priority:** 2
- **In-scope item:** 5
- **Preconditions:** Pickup is otherwise valid; downstream loyalty credit service is unavailable.
- **Steps:**  
  1. Complete pickup.  
  2. Attempt loyalty update.  
  3. Observe customer/account outcome.
- **Expected result:** Pickup completion is not silently lost; loyalty failure is retried or surfaced according to design, and customer-facing state remains consistent.

## TC-16 — Wrong loyalty points amount after return/reserved-item split
- **Category:** edge
- **Priority:** 3
- **In-scope item:** 5
- **Preconditions:** Reservation contains mixed items or adjusted fulfillment state.
- **Steps:**  
  1. Complete only the valid collected portion.  
  2. Check loyalty credit result.
- **Expected result:** Loyalty points correspond exactly to fulfilled pickup items and not to cancelled/uncollected ones.

---

## TC-17 — EU pickup confirmation with PSD2 SCA challenge success
- **Category:** critical-path
- **Priority:** 1
- **In-scope item:** 4
- **Preconditions:** EU payment-confirmation path is enabled; SCA challenge required.
- **Steps:**  
  1. Start pickup confirmation requiring SCA.  
  2. Complete SCA challenge successfully.  
  3. Finalize pickup/payment confirmation.
- **Expected result:** SCA challenge is shown correctly and pickup confirmation succeeds.

## TC-18 — PSD2 SCA failed or abandoned
- **Category:** negative
- **Priority:** 1
- **In-scope item:** 4, 5
- **Preconditions:** EU payment path active; SCA challenge required.
- **Steps:**  
  1. Start pickup confirmation.  
  2. Fail, cancel, or abandon the SCA challenge.  
  3. Attempt to continue.
- **Expected result:** System rejects completion, keeps order/pickup state consistent, and surfaces a clear retry or failure message.

## TC-19 — SAP timeout at pickup confirmation
- **Category:** negative
- **Priority:** 1
- **In-scope item:** 3, 5
- **Preconditions:** Reservation exists; SAP-backed check is required; SAP sandbox is forced to timeout.
- **Steps:**  
  1. Associate attempts pickup confirmation.  
  2. System requests inventory confirmation.  
  3. SAP response times out.
- **Expected result:** System does not falsely confirm pickup; it degrades or escalates according to design and shows a clear message to the associate/customer.

## TC-20 — Klarna split-pay cancelled mid-reservation
- **Category:** negative
- **Priority:** 2
- **In-scope item:** 4, 5
- **Preconditions:** Reservation/payment path uses split-pay provider; payment is cancelled before pickup.
- **Steps:**  
  1. Create reservation with split-pay setup.  
  2. Cancel payment state before pickup.  
  3. Attempt pickup confirmation.
- **Expected result:** System rejects pickup/payment completion and surfaces the payment-state failure rather than allowing an inconsistent pickup.

---

## Negative-case count check
Explicit negative cases: TC-04, TC-08, TC-11, TC-12, TC-15, TC-18, TC-19, TC-20
Total explicit negatives: 8
