# 01-threats

| Element | Category | Threat | Notes |
|---|---|---|---|
| Customer Browser / Mobile App | Spoofing | An attacker steals a valid customer session token and submits checkout requests as that customer through the public interface. | External entity; S allowed. |
| Customer Browser / Mobile App | Repudiation | A customer disputes having triggered a cart-summary or checkout action, and weak request-to-user audit linkage makes the event hard to prove. | External entity; R allowed. |
| API Gateway | Spoofing | An attacker sends forged or replayed bearer tokens to the API gateway and gains access if token validation or audience checks are weak. | Process; all STRIDE categories allowed. |
| API Gateway | Denial of Service | A burst of oversized or repeated cart-summary requests saturates gateway capacity and delays valid checkout traffic. | Process under perimeter boundary. |
| cart-api Service | Tampering | A crafted request manipulates cart or checkout fields that the service trusts without sufficient server-side validation, altering order state. | Process handling untrusted input. |
| cart-api Service | Information Disclosure | The summarise-my-cart path sends more cart/customer context to the model gateway than necessary, exposing sensitive order details outside the app boundary. | Process to third-party path. |
| cart-api Service | Elevation of Privilege | A missing authorization check lets a lower-privileged user access or modify another customer’s cart or order data. | Process with direct data access. |
| cart-api Service | Repudiation | The service processes sensitive cart or checkout actions without durable, user-linked audit events, making abuse investigations incomplete. | Process writes audit events. |
| request flow from User to API Gateway | Tampering | An attacker injects malformed or malicious request parameters into the public API flow, aiming to trigger unsafe parsing or downstream query misuse. | Data flow; T allowed. |
| request flow from User to API Gateway | Information Disclosure | Sensitive cart identifiers or tokens leak in transit through misconfigured TLS termination or verbose edge logging. | Data flow; I allowed. |
| request flow from User to API Gateway | Denial of Service | Repeated unauthenticated or high-volume requests on the public flow exhaust edge or gateway resources and degrade checkout. | Data flow; D allowed. |
| Postgres Orders / Cart DB | Tampering | A compromised service path writes unauthorized changes to order or cart records, corrupting the system of record. | Data store; T allowed. |
| Postgres Orders / Cart DB | Information Disclosure | Over-broad queries or compromised credentials expose order history and customer purchase data from the transactional database. | Data store; I allowed. |
| Postgres Orders / Cart DB | Denial of Service | Expensive queries, lock contention, or abusive traffic make the database unavailable to checkout operations. | Data store; D allowed. |
| Redis Cache | Information Disclosure | Cached cart or session data is exposed through weak isolation or stolen access credentials, leaking live user state. | Data store; I allowed. |
| EPAM DIAL Gateway flow | Tampering | A manipulated prompt or request payload alters the meaning of the cart-summary request and produces unsafe or misleading model output. | Data flow to third party; T allowed. |
| EPAM DIAL Gateway flow | Information Disclosure | Cart contents or customer-linked details are sent over the gateway flow beyond the minimum needed for summarization. | Data flow leaving internal boundary. |
| EPAM DIAL Gateway flow | Denial of Service | A loop or surge in summary requests drives excessive AI traffic, causing latency spikes and cost runaway on the model path. | Data flow / metered dependency. |
| Audit / App Logs | Information Disclosure | Logs capture secrets, tokens, or raw cart payloads, making the logging store a secondary leakage path. | Data store; I allowed. |
| Observability Stack | Denial of Service | High-cardinality metrics or trace floods overload the observability pipeline and hide real production symptoms during an incident. | Data store / telemetry sink. |

## Check
- Distinct threats: 20
- Element types covered:
  - external entity
  - process
  - data flow
  - data store
- STRIDE-per-element constraints respected:
  - external entity: S, R only
  - process: all six
  - data flow / data store: T, I, D only
