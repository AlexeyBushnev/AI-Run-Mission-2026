# 05-patterns

| Pattern | Where on L2 | Meridian constraint it addresses | Trade-off |
|---|---|---|---|
| Strangler Fig | **Apollo GraphQL Gateway** routes Phase 1 traffic to new Meridian services while legacy regional stacks continue to serve unmigrated capabilities behind the cutover boundary | CTO mandate: **no Big Bang**; 22 regional stacks must coexist while the target platform grows in phases | The routing/cutover layer becomes a long-lived dependency and cannot be removed until the last regional capability migrates |
| Outbox | **Cart Service** and **Checkout Service** publish state changes to **Order Event Bus (Kafka)** through an outbox-based transactional publish path | ADR-002: cross-service consistency is needed without distributed transactions | Adds CDC / replay / operational complexity and raises the bar for observability and recovery |
| Bulkhead | Isolate **payment-method-specific checkout paths** and dependent connection pools / workers around **Checkout Service → Stripe** and regional payment integrations | Local payment methods vary by region; a failure in one market/payment path must not break all checkout flows | More runtime isolation means more pods, more configuration, and less efficient shared resource use |
| Circuit Breaker | On synchronous edges from **Apollo Gateway → SAP ECC fallback path** and **Checkout Service → Stripe** | SAP ECC and payment-provider outages must not cascade into broad customer-facing failure | Requires disciplined timeout, retry, and fallback tuning; poor thresholds can hide real issues or trip too aggressively |
| BFF (Backend for Frontend) | Separate experience shaping for **Web App**, **Mobile App**, and **POS Client**, all fronted through the gateway boundary | Meridian serves different surfaces with different interaction shapes; POS needs assisted cart lookup while web/mobile need customer-self-service flows | More surface-specific logic to maintain and keep aligned across channels |
| CQRS-style read segregation | **Inventory Read Cache (Redis)** as the read-optimized side, hydrated separately from the write/source side anchored in **SAP ECC** and events | Inventory lookups need low-latency reads while SAP ECC remains the system of record | Increases consistency and cache-warmup concerns; stale reads must be handled explicitly in UX and operations |
| Saga (limited use) | **Checkout Service** coordinating payment, order persistence, and downstream event publication across the order path | Phase 1 checkout spans multiple steps and dependencies where all-or-nothing distributed transactions are not realistic | Compensation logic becomes harder to reason about and test; overuse would increase team complexity |

## Patterns explicitly not recommended for Phase 1

| Pattern | Why not recommended now |
|---|---|
| Event Sourcing (system-wide) | Too costly in operational and cognitive complexity for a junior internal team inside an 18-month staged transformation. The Phase 1 problem is coexistence and safe integration, not rebuilding every domain around event streams as the primary source of truth. |
| Pipe & Filter (as a named top-level architecture pattern) | Useful at narrower processing boundaries, but not load-bearing enough for the main Phase 1 cutover story compared with Strangler Fig, Outbox, and resilience patterns. |
| Service mesh / Istio-style platform pattern | This is a deployment/platform concern rather than a load-bearing application architecture pattern for this kata, and would likely overburden the team in Phase 1. |

## Open questions

1. **Pattern recommended but not yet fully placed:** BFF is architecturally plausible, but the current L2 uses a single Apollo Gateway rather than explicit Web BFF / Mobile BFF / POS BFF containers. Review whether Meridian should keep one gateway in Phase 1 or split per-surface experience orchestration later.
2. **Pattern overlap note:** CQRS-style read segregation is already partly expressed through the Redis inventory read cache hydrated away from SAP ECC. Treat this as an existing read/write separation choice rather than a signal to introduce a large new CQRS program.
3. **Regional isolation review:** Bulkhead should likely be applied at least per payment-method / regional checkout dependency, but the exact deployment/runtime placement belongs to later Infra & Ops design.
