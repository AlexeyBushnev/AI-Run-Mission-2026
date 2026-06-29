# 06-readiness-brief

## Service
**cart-api** — checkout service with AI-powered “summarise my cart” step via EPAM DIAL

## Cloud Operations & Support Pack — one-page readout

### 1. How it deploys and rolls back
- **Deploy path:** containerized `cart-api` deployed to Kubernetes via CI/CD pipeline on push to `main`
- **Rollback path:** rollback should be a first-class CI/CD action, but the current workflow audit flagged the rollback gate as missing
- **Status:** **PARTIAL** — deployment path exists; rollback path is not yet explicit enough in the workflow

### 2. Who gets paged
- **Expected page path:** operations / support receives the runtime page first, then escalates by support tier
- **Known ownership:** L1 detects and pages; L2 confirms and executes runbook recovery; L3 fixes code/config for durable correction
- **Status:** **PARTIAL** — support tier flow is defined, but named on-call owner is **UNKNOWN — owner needed**

### 3. What is monitored
- The stack map identifies observability watching:
  - load balancer
  - Kubernetes cluster
  - cart-api service
  - Postgres
  - Redis
  - EPAM DIAL gateway
  - model call path
- Practical top signals from the incident and ops pack:
  - pod health / restarts / `CrashLoopBackOff`
  - `OOMKilled` events
  - error rate
  - latency on healthy pods
  - AI gateway usage / cost signals
- **Status:** **YES**, but explicit alert definitions are still **UNKNOWN — owner needed**

### 4. Per-month cost and the cap
- **Cloud rent:** about **$1,500 / month**
- **AI meter:** about **$15,000 / month** at the kata price point
- **Monthly total:** about **$16,500 / month**
- **Recommended DIAL hard cap:** **$12,000 / month**
- **Recommended alert threshold:** **$9,000 / month**
- **Spend owner:** cart / checkout feature team and business budget owner
- **Status:** **YES**

### 5. The kill-switch
- Operationally, the safe kill-switch is to **degrade or disable the AI summarise-my-cart step** instead of taking down checkout
- This also acts as a spend-control switch when the AI meter approaches the hard cap
- **Status:** **PARTIAL** — the policy is named, but the exact technical switch path is **UNKNOWN — owner needed**

### 6. Which support tier owns the top two ticket types
- **Ticket type 1:** `cart-api` pods crash after deploy / `OOMKilled`
  - **Owning tier:** **L2** for rollback and service restoration
  - **Playbook / runbook:** `04-incident-runbook.md`
  - **L3 role:** fix code path and retune memory/resources before next release
- **Ticket type 2:** AI cost runaway / cap breach risk
  - **Owning tier:** **L2** for feature degradation or kill-switch action; **L3 / product + ops** for durable cap/prompt/usage correction
  - **Playbook / runbook:** cost cap policy from `05-cost-estimate.md`
- **Status:** **YES**, though named people are still **UNKNOWN — owner needed**

## Maturity gap
The main maturity gap is that the app has the core operational artifacts, but several production controls are still only partially defined:
- rollback gate in CI/CD is missing
- kill-switch is policy-level, not yet clearly operationalized
- on-call owner and explicit alert thresholds are not yet named

## Headline from each prior file
- **01-stack-map.md:** request path and ops ownership are visible end-to-end, including DIAL and observability
- **02-deploy-manifest.md:** first-draft manifest misses production controls such as probes, resource limits, and proper secret handling
- **03-ci-workflow.md:** first-draft CI/CD misses key supply-chain controls, especially immutable action pinning, OIDC, signing, and rollback gate
- **04-incident-runbook.md:** top failure pattern is memory-related crash after the new AI summarise step; rollback is the immediate mitigation
- **05-cost-estimate.md:** the dominant cost is the AI meter, not cloud rent; ship safely only with a DIAL cap and alert

## Six readiness questions — answered or flagged
| Question | Answer |
|---|---|
| How it deploys and rolls back | Deploy path exists; rollback path is **PARTIAL** and needs an explicit gate |
| Who gets paged | Support tiers are defined; named on-call owner is **UNKNOWN — owner needed** |
| What's monitored | Core stack and AI path are monitored; exact alert definitions are **UNKNOWN — owner needed** |
| Per-month cost and the cap | **$16,500/month** at kata price point; cap **$12,000**, alert **$9,000** |
| The kill-switch | Disable/degrade AI summarise-my-cart; implementation path is **UNKNOWN — owner needed** |
| Which support tier owns the top two ticket types | L2 owns runtime recovery; L3 owns durable code/config fixes |

## L1–L3 support handover
- **L1:** detects alerts, opens incident, pages L2
- **L2:** follows runtime recovery playbooks (`04-incident-runbook.md`, cost-cap action path), restores service, verifies stabilization
- **L3:** fixes code, resource sizing, CI/CD control gaps, and permanent operational safeguards

## Verdict
**Not yet fully ready to operate and support.**  
**Primary blocker:** the service has no clearly defined rollback gate / operational kill-switch implementation, which means the two most likely operational failures — bad deploy and runaway AI feature path — are not yet bounded tightly enough for production confidence.
