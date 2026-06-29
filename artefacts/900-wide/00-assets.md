# 00-assets

## Asset inventory

| Asset | Rank | Rationale |
|---|---|---|
| Customer authentication tokens / session identifiers | HIGH | Token theft or misuse would allow account takeover and unauthorized cart or checkout actions. |
| Customer cart contents and checkout state | HIGH | This data directly affects purchase flow and can reveal intent, pricing, and personal shopping behavior. |
| Order history and order records | HIGH | Unauthorized access or tampering would affect customer trust, financial reconciliation, and support operations. |
| DATABASE_URL and database credentials | HIGH | Exposure would give direct access to core transactional data stores. |
| DIAL_API_KEY / gateway credentials | HIGH | Leakage could allow unauthorized model calls, spend abuse, or misuse of governed AI access. |
| Audit logs and security-relevant application logs | MEDIUM | They contain sensitive operational context and may expose identifiers, but are primarily supporting evidence rather than the primary business record. |
| Redis cache contents | MEDIUM | Cached cart/session data is sensitive and useful to attackers, but usually shorter-lived than the system of record. |
| Observability metrics, traces, and AI gateway telemetry | MEDIUM | These reveal traffic shape, incident details, and usage patterns that can aid an attacker or leak business-sensitive operations data. |
| Aggregated usage / performance summaries | LOW | High-level aggregates are useful but usually less sensitive because they do not directly expose individual customer actions. |
| Static application configuration without secrets | LOW | Misuse can still help reconnaissance, but the impact is lower than secret-bearing or customer-record assets. |

## Highest-priority assets
- **Customer authentication tokens / session identifiers** — HIGH because compromise enables direct impersonation.
- **DATABASE_URL and database credentials** — HIGH because compromise grants access to core data stores.
- **DIAL_API_KEY / gateway credentials** — HIGH because compromise enables metered abuse and unauthorized AI access.
