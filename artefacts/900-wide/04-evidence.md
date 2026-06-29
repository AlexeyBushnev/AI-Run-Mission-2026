# 04-evidence

## 1) Control identity
- **Control name:** cart-summary API auth and per-client rate-limit guard
- **Framework mapping:** SOC 2 CC6.1 / CC6.6 (logical access and restriction of unauthorized or excessive access)
- **Plain-language description:** The control requires a valid API key for the summarise-my-cart path and blocks a client after 5 requests within 60 seconds, returning a `429` instead of allowing unlimited calls.
- **Scope:** `summarise-my-cart` request path for `cart-api`
- **Named owner:** David Park

## 2) Test method
- **Bypass-case tested:** over-limit request burst against the summarise-my-cart path
- **Verbatim test procedure:**
  1. Use a valid API key: `valid-key-123`
  2. Send 6 requests from the same client inside a 60-second window
  3. Confirm requests 1–5 return `200 ok`
  4. Confirm request 6 returns `429 rate_limit_exceeded`
- **Commit SHA:** `480b640c09cc93f8c7ce13d16f5f63b43b02907e`
- **Log file path:** `security-control/logs/bypass-test-rate-limit.json`
- **Test date:** 2026-06-29
- **Test command:** `python3 test_bypass_rate_limit.py`
- **Actual output excerpt:**
```json
[
  {
    "request_number": 1,
    "allowed": true,
    "status_code": 200,
    "reason": "ok"
  },
  {
    "request_number": 2,
    "allowed": true,
    "status_code": 200,
    "reason": "ok"
  },
  {
    "request_number": 3,
    "allowed": true,
    "status_code": 200,
    "reason": "ok"
  },
  {
    "request_number": 4,
    "allowed": true,
    "status_code": 200,
    "reason": "ok"
  },
  {
    "request_number": 5,
    "allowed": true,
    "status_code": 200,
    "reason": "ok"
  },
  {
    "request_number": 6,
    "allowed": false,
    "status_code": 429,
    "reason": "rate_limit_exceeded"
  }
]
```

## 3) Monitoring
- **Design intent metric:** `cart_summary_rate_limit_rejections_total`
- **Design intent threshold:** page if rejections exceed `100` in `5` minutes or if rejection rate exceeds `5%` of cart-summary requests over `15` minutes
- **Who would be paged:** L2 on-call for `cart-api`, escalating to L3 service owner if sustained
- **Design intent note:** Alert wiring is not implemented in this kata environment; this is the production monitoring target, not a claim of live monitoring

## 4) Audit trail
- **Log location:** `security-control/logs/bypass-test-rate-limit.json`
- **Retention period and legal basis:** 90 days for security investigation and service protection; kata artifact only in this environment
- **Immutability mechanism:** none — kata artifact
- **Access control:** local repository access only in this kata environment

## Result
The control blocks the bypass case it was designed to stop: the 6th request in the same 60-second window is denied with `429 rate_limit_exceeded`, proving the guard blocks the attack path rather than only allowing the happy path.
