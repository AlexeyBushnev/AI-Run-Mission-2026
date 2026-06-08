# 00-options

## Decision to open
How should Meridian Phase 1 read inventory and bridge the online / in-store cart while SAP ECC remains the inventory source of truth?

---

## Option 1 — Direct synchronous reads against SAP ECC

**Core idea**
- The new commerce platform asks SAP ECC directly for near-real-time inventory when product, cart, or checkout flows need it.
- Online and in-store cart logic stays thin and relies on SAP as the live source of truth.
- Minimal new inventory platform logic is introduced in Phase 1.

**What it optimises for**
- Simplicity of architecture
- Lower upfront build scope
- Clear source-of-truth model

**What it sacrifices**
- Checkout and availability latency
- Resilience when SAP is slow or unavailable
- Flexibility for future omnichannel features

**Meridian constraint that pressures it hardest**
- **SAP batch-update / latency reality** — if SAP data is stale or slow, the user-facing experience inherits that weakness directly.

---

## Option 2 — Event-driven inventory read model hydrated from SAP via Kafka

**Core idea**
- SAP remains the system of record, but inventory events are published into Kafka and used to hydrate a read-optimized inventory view for digital channels.
- Product page, cart, and checkout read from the derived inventory model rather than hitting SAP directly.
- Online / in-store cart bridging is handled through event-driven state propagation and bounded service contracts.

**What it optimises for**
- Better digital-channel latency
- Loose coupling from SAP runtime behavior
- Stronger long-term omnichannel architecture

**What it sacrifices**
- More moving parts and operational complexity
- Event consistency challenges
- Higher skill demand on the internal team

**Meridian constraint that pressures it hardest**
- **Junior team operability** — Kafka, outbox/event reliability, replay, and read-model correctness may be hard for a junior internal team to own early.

---

## Option 3 — Buy a cross-channel inventory service

**Core idea**
- Use a commercial cross-channel inventory capability as the bridge between SAP ECC and the new headless platform.
- The bought service owns inventory aggregation, store availability logic, and channel-facing APIs.
- Meridian integrates the platform and checkout flows to the vendor rather than building the read model itself.

**What it optimises for**
- Faster time to usable capability
- Reduced in-house platform complexity in Phase 1
- Better fit for a team that needs a more guided operating model

**What it sacrifices**
- Vendor dependency and recurring cost
- Less architectural control
- Potential mismatch with Meridian-specific flows and regional edge cases

**Meridian constraint that pressures it hardest**
- **18-month / $42M program with quarterly stage gates** — a bought service may look attractive for speed, but commercial fit, procurement, and integration limits can still become stage-gate risk.

---

## Divergence check
These three options differ in a load-bearing way:

1. **Synchronous runtime dependency on SAP**
2. **Event-driven derived read model**
3. **Buy rather than build the inventory bridge**

They are not three microservice variations of the same idea.
