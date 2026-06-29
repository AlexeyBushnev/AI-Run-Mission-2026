# 04-incident-runbook

## Incident
**Symptoms**
- About half of `cart-api` pods are in `CrashLoopBackOff`
- Kubernetes events show `OOMKilled`
- The failure began about 20 minutes after a deploy that added the AI “summarise my cart” step
- Error rate is climbing
- Latency on the remaining healthy pods is rising as they absorb the extra load

## Ranked hypotheses

### 1. Memory exhaustion caused by the new AI summarise step
- **Why this is ranked #1:** `OOMKilled` is direct evidence of memory exhaustion, and the timing lines up with a deploy that added a memory-heavier feature path.
- **Supporting evidence:** crash started shortly after deploy; pods are not just unhealthy, they are specifically being killed for memory; healthy pods show rising latency because fewer pods are serving traffic.
- **Cheapest next diagnostic step:** compare current pod memory usage and container restart events before vs. after the deploy; inspect the deployment diff for the summarise-step change and current memory requests/limits.

### 2. Missing or too-low Kubernetes memory requests/limits for the updated workload
- **Why this is ranked #2:** the deploy may have increased real memory demand while the manifest still reflects an older, smaller memory profile or lacks explicit limits/requests entirely.
- **Supporting evidence:** Kata 8.2 already identified missing or weak resource controls as a likely first-draft gap; OOM after a feature expansion often means the runtime envelope was not updated.
- **Cheapest next diagnostic step:** inspect the Deployment manifest actually running in the cluster and compare configured memory requests/limits with observed container memory use.

### 3. Memory leak or runaway request fan-out in the new summarise path
- **Why this is ranked #3:** if the new summarise flow retains too much data per request or multiplies calls/work in memory, pods can grow until killed even if limits were previously adequate.
- **Supporting evidence:** the issue appeared after a code change tied to the AI path; rising latency on surviving pods suggests extra work or memory pressure, not only a static config error.
- **Cheapest next diagnostic step:** sample application logs and traces for requests that invoke the summarise step; compare heap/process memory growth and request characteristics on pods that restart.

## Immediate mitigation
- **Roll back the deployment** to the version before the AI summarise step.
- This is the fastest customer-impact reduction step because it removes the new memory-heavy path and restores the previous pod behavior.

## Durable fix
- **Set and validate correct memory requests/limits for the updated workload**, then re-test the summarise step under realistic load before redeploying.
- If the summarise path is retaining or loading too much data, fix that code path as an L3 engineering change before re-release.

## Runbook entry

| Row | Content |
|---|---|
| **Detection** | Alert: `cart-api` pods in `CrashLoopBackOff` and/or Kubernetes event `OOMKilled`; customer-facing signals: rising 5xx rate and higher latency on surviving pods |
| **Diagnosis** | 1. Confirm `OOMKilled` in pod events. 2. Check whether the incident began after a recent deploy. 3. Compare memory usage against current requests/limits. 4. Confirm whether the new AI summarise step is present in the active release. |
| **Fix** | Short term: roll back to the previous stable release. Medium term: raise or right-size memory requests/limits and validate the summarise path under load. Long term: optimize the summarise implementation if memory growth is excessive. |
| **Rollback** | Use the CI/CD rollback path from Kata 8.3 to redeploy the previous known-good image/revision, then verify pod restarts stop and latency/error rate return to baseline. |
| **Owning support tier** | **L1:** detect and page. **L2:** confirm OOM, execute rollback, verify recovery. **L3 / engineering:** patch the summarise code path and retune resource limits for the next release. |

## Operational note
This is primarily an **L2 recovery / L3 fix** pattern:
- L2 should not debug the code in depth at 2 a.m.; it should confirm OOM and roll back.
- L3 owns the durable code and sizing correction.
