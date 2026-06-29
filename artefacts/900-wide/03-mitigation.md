# 03-mitigation

## Top critical risk copied from 02-risks.xlsx
- **Element:** Customer Browser / Mobile App
- **Category:** Spoofing
- **Threat:** An attacker steals a valid customer session token and submits checkout requests as that customer through the public interface.
- **Likelihood × Impact:** High × High
- **Severity:** Critical
- **Blast radius:** Blast radius: up to all active signed-in customers; potentially every live customer session at risk if token controls are weak.

## Three-class mitigation

### 1. Preventive control
- **Control:** Enforce a hard per-feature AI gateway cap, request-rate limit, and summarise-my-cart circuit breaker at the DIAL / gateway edge.
- **What it does:** Stops unbounded request loops or traffic surges from consuming unlimited model capacity and spend.
- **Threat property it closes:** Uncontrolled request amplification and unbounded model-call volume.
- **Why it matches the STRIDE category:** This is a **Denial of Service** threat, so the preventive control reduces the attacker’s or failure mode’s ability to exhaust service capacity and meter budget before customer impact spreads.
- **Owner:** Tomas Reyes
- **Due date:** 2026-08-15

### 2. Detective control
- **Control:** Add alerting on AI call rate, AI spend velocity, cart-summary latency, and gateway error spikes, with dashboards split by feature path.
- **What it does:** Detects when prevention fails or is bypassed, and gives support a visible signal before the service degrades broadly.
- **Threat property it closes:** Late or missing detection of runaway AI traffic and rising service pressure.
- **Why it matches the STRIDE category:** For a **Denial of Service** threat, detective controls are essential because the first sign is often load, latency, or spend abnormality rather than a clean application error.
- **Owner:** Sarah Chen
- **Due date:** 2026-08-12

### 3. Responsive control
- **Control:** Implement a kill switch that disables the summarise-my-cart feature and falls back to standard checkout behavior without model calls.
- **What it does:** Contains the damage quickly by removing the expensive / unstable feature path while preserving core checkout.
- **Threat property it closes:** Ongoing customer impact after the DoS pattern has started.
- **Why it matches the STRIDE category:** For a **Denial of Service** threat, a responsive control limits blast radius and restores service continuity when capacity is already under pressure.
- **Owner:** David Park
- **Due date:** 2026-08-10

## Residual-risk acceptance contract

| Field | Value |
|---|---|
| **Risk statement (cause / event / consequence)** | If AI request amplification, a client loop, or a misconfigured summarise-my-cart path overwhelms the DIAL gateway or cart-api service, then latency and error rates can rise sharply, causing checkout degradation, spend overrun, and customer abandonment. |
| **Named owner** | David Park |
| **Expiry date** | 2026-09-01 |
| **Re-evaluation triggers** | Any cap breach; more than 1 customer-visible incident tied to summarise-my-cart; more than 20% month-over-month growth in AI calls; any architecture change to the gateway/model path; any new region rollout. |
| **Approver** | Eva Müller |

## Why this set is defense in depth
- **Preventive** reduces the chance the traffic spike can start or grow unchecked.
- **Detective** gives visibility when preventive controls are insufficient.
- **Responsive** limits customer and financial damage when the threat is already active.

## Source note
Top row selected from 02-risks.xlsx
