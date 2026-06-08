# 07-adversarial

## Adversarial review setup
This pre-mortem assumes a **fresh-session review mindset**: the job is to break the Meridian Phase 1 architecture, not defend it.

## Stressor A — 10× Black Friday peak load

### 1. Break point
**Container / relationship:** Apollo GraphQL Gateway → Inventory Read Cache / downstream services  
**First user symptom:** Product pages and cart refresh become slow or intermittent during peak browsing and checkout bursts.

**Decision:** Patch now  
**Patch:** Add explicit edge throttling and degraded-read behavior at the gateway for non-critical inventory refreshes.  
**Changes:** `02-containers.mmd`, `05-patterns.md`, `06-nfrs.md`

### 2. Break point
**Container / relationship:** Checkout Service → Order Database  
**First user symptom:** Customers see slow checkout completion or duplicate-submit fear during peak payment/order write volume.

**Decision:** Patch now  
**Patch:** Add write-path protection with queue-aware backpressure and idempotency enforcement for checkout submission.  
**Changes:** `02-containers.mmd`, `05-patterns.md`, `06-nfrs.md`

### 3. Break point
**Container / relationship:** Inventory cache warm-up path from SAP ECC / Kafka into Redis  
**First user symptom:** Availability looks stale or inconsistent under burst load, increasing phantom-stock risk.

**Decision:** Accept risk for Phase 1  
**Accepted risk owner:** Tomás Reyes — Architecture  
**Reason:** Full resilience hardening of cache hydration under extreme peak is valuable, but the Phase 1 cost/complexity is higher than the immediate payoff. Existing NFRs and reconciliations reduce, but do not remove, this risk.

---

## Stressor B — Hostile inputs at EU checkout

### 1. Break point
**Container / relationship:** Stripe → Checkout Service webhook boundary  
**First user symptom:** Replayed or malformed PSD2 SCA callbacks may create duplicate or inconsistent payment/order states.

**Decision:** Patch now  
**Patch:** Add explicit webhook signature verification, replay protection, and idempotency key enforcement on callback handling.  
**Changes:** `03-integrations.md`, `04-adr-002.md`, `06-nfrs.md`

### 2. Break point
**Container / relationship:** POS Client / Apollo Gateway / Identity Service loyalty-QR lookup path  
**First user symptom:** Malformed or hostile loyalty-QR payloads could create lookup failures, false customer-not-found states, or security issues.

**Decision:** Patch now  
**Patch:** Add strict input validation and bounded failure behavior for QR parsing and lookup; reject malformed tokens before downstream fan-out.  
**Changes:** `03-flow-instore-cart.mmd`, `03-integrations.md`, `06-nfrs.md`

### 3. Break point
**Container / relationship:** Apollo GraphQL Gateway input surface  
**First user symptom:** Excessive or malformed query shapes may increase latency or expose weak validation paths at checkout or cart lookup.

**Decision:** Accept risk with owner  
**Accepted risk owner:** Asha Sundaram — Compliance / Security  
**Reason:** Gateway query-hardening can be improved further, but Phase 1 should explicitly track the remaining exposure as a monitored security risk rather than pretending it is closed.

---

## Stressor C — Partner outage (SAP ECC down 2 hours / Stripe degraded)

### 1. Break point
**Container / relationship:** Apollo Gateway → SAP ECC inline fallback on inventory cache miss  
**First user symptom:** Store associates cannot reliably retrieve or trust inventory status for one or more cart items during assisted checkout.

**Decision:** Patch now  
**Patch:** Add a hard degraded mode: on SAP outage, do not keep retrying inline fallback on the hot path; return “stock unknown — confirm with floor staff” after bounded timeout.  
**Changes:** `03-flow-instore-cart.mmd`, `05-patterns.md`, `06-nfrs.md`

### 2. Break point
**Container / relationship:** Checkout Service → Stripe  
**First user symptom:** Checkout stalls or fails for card payments, especially in EU flows that already depend on PSD2 SCA round-trips.

**Decision:** Patch now  
**Patch:** Add explicit degraded payment state and retry-safe recovery path instead of treating provider degradation as a generic checkout failure.  
**Changes:** `03-integrations.md`, `05-patterns.md`, `06-nfrs.md`

### 3. Break point
**Container / relationship:** Regional operations / in-store assisted flow during extended dependency outage  
**First user symptom:** Store staff fall back to manual workarounds, increasing queue times and customer frustration.

**Decision:** Accept risk for Phase 1  
**Accepted risk owner:** David Park — Store Operations  
**Reason:** A full offline-capable assisted checkout recovery design is possible, but it is broader than the current Phase 1 scope and should be owned as an operational risk until later phases.

---

## Summary of patches to apply

1. **Gateway degraded-read behavior under peak load**  
   Update: `02-containers.mmd`, `05-patterns.md`, `06-nfrs.md`

2. **Checkout idempotency + backpressure on write path**  
   Update: `02-containers.mmd`, `05-patterns.md`, `06-nfrs.md`

3. **Webhook verification + replay protection**  
   Update: `03-integrations.md`, `04-adr-002.md`, `06-nfrs.md`

4. **Strict QR input validation**  
   Update: `03-flow-instore-cart.mmd`, `03-integrations.md`, `06-nfrs.md`

5. **Bounded degraded mode for SAP outage on cache miss**  
   Update: `03-flow-instore-cart.mmd`, `05-patterns.md`, `06-nfrs.md`

6. **Explicit degraded payment state for Stripe issues**  
   Update: `03-integrations.md`, `05-patterns.md`, `06-nfrs.md`

## Accepted risks

| Risk | Owner | Why accepted now |
|---|---|---|
| Inventory cache hydration may still lag under extreme Black Friday conditions | Tomás Reyes — Architecture | Phase 1 accepts some stale-read risk rather than overbuilding the platform before later phases |
| Additional GraphQL / hostile query hardening remains incomplete | Asha Sundaram — Compliance / Security | Risk is visible and should be monitored explicitly rather than hidden behind vague “secure by design” language |
| No full offline assisted-checkout recovery for extended partner outage | David Park — Store Operations | Operational workaround exists; full productized recovery is larger than Phase 1 scope |

## Final note
The design’s most dangerous weak spots are not generic bottlenecks; they are the **SAP inline fallback path**, the **Stripe callback/payment boundary**, and the **hot-path gateway surfaces under peak or hostile input**. Each is now either patched or explicitly owned.
