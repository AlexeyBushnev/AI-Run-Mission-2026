from collections import defaultdict, deque
from dataclasses import dataclass
import time


@dataclass
class Decision:
    allowed: bool
    status_code: int
    reason: str


class CartSummaryGuard:
    """Simple auth + fixed-window rate limit guard for the summarise-my-cart path."""

    def __init__(self, valid_api_keys=None, max_requests=5, window_seconds=60):
        self.valid_api_keys = set(valid_api_keys or {"valid-key-123"})
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests = defaultdict(deque)

    def check(self, api_key: str | None, client_id: str, now: float | None = None) -> Decision:
        now = time.time() if now is None else now

        if not api_key or api_key not in self.valid_api_keys:
            return Decision(False, 401, "unauthorized")

        bucket = self._requests[client_id]
        while bucket and now - bucket[0] > self.window_seconds:
            bucket.popleft()

        if len(bucket) >= self.max_requests:
            return Decision(False, 429, "rate_limit_exceeded")

        bucket.append(now)
        return Decision(True, 200, "ok")


def demo():
    guard = CartSummaryGuard()
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
    return results


if __name__ == "__main__":
    import json
    print(json.dumps(demo(), indent=2))
