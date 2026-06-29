from rate_limit_guard import CartSummaryGuard
from pathlib import Path
import json

guard = CartSummaryGuard(valid_api_keys={"valid-key-123"}, max_requests=5, window_seconds=60)
client_id = "cust-42"
api_key = "valid-key-123"
now = 1723456800.0

results = []
for i in range(6):
    decision = guard.check(api_key, client_id, now=now + i)
    results.append(
        {
            "request_number": i + 1,
            "allowed": decision.allowed,
            "status_code": decision.status_code,
            "reason": decision.reason,
        }
    )

out = Path("logs")
out.mkdir(exist_ok=True)
log_path = out / "bypass-test-rate-limit.json"
log_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
print(log_path.as_posix())
print(json.dumps(results, indent=2))
