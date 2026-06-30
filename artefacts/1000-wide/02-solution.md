# Meridian Retail Group — solution outline

## High-level approach
We will deliver Meridian’s checkout modernization as a phased program that stabilizes the current checkout path first, then introduces the AI-assisted cart-summary capability through Meridian’s approved gateway, and finally operationalizes the service with security, cost, and support controls. The solution is grounded in the carried-forward spec, architecture, engineering, data, operations, and security artifacts already developed across Modules 200–900, so the proposal is based on defined scope and evidence rather than bid-time invention.

## Compliance shape
**RFP-led (greenfield bid)** — the proposal commits to a target delivery shape before contract signature. Default tooling assumption is EPAM pre-approved AI tooling; any client-data egress or regulated-data handling will require legal and compliance review before tooling is expanded.

## Phases

| # | Phase | Entry | Exit | Duration | Owner role |
| --- | --- | --- | --- | --- | --- |
| 1 | Mobilize and confirm scope | RFP intent confirmed, bid conditions accepted, named Meridian sponsor and working team in place | Approved scope baseline, signed delivery assumptions, confirmed architecture and dependency map | 2 weeks | Delivery Lead |
| 2 | Build and integrate core checkout modernization | Approved scope baseline, environments ready, API and service contracts confirmed | Checkout service, integrations, and baseline non-AI path implemented and testable end to end | 10 weeks | Engineering Lead |
| 3 | Add governed AI cart summary + harden controls | Core path stable, gateway access approved, security and operations gates agreed | AI-assisted cart-summary implemented through approved gateway, with cost cap, threat-model evidence, DQ/ops/security controls, and rollback path | 6 weeks | Solution Architect |
| 4 | UAT, rollout, and hypercare transition | Business acceptance criteria, test pack, support model, and cutover checklist approved | Production release completed, hypercare exit signed off, runbooks/support ownership handed over | 4 weeks | PM / Service Transition Lead |

## Outsourced capability
We do not have a dedicated specialist bench in **AI gateway policy integration and advanced cost-governance automation** in-house at the level this program may require. We will sub-vendor this capability to **N&N Digital Controls Ltd.**

**Integration:** N&N delivers gateway policy configuration templates, cost-governance automation, and control recommendations that plug into our checkout-service build, operations pack, and AI-native delivery section. Their deliverables are reviewed and integrated through our architecture, security, and operations workstreams.

**Governance:** N&N does not deliver directly to Meridian unchecked. They ship through EPAM-led review gates. Required evidence includes policy config documentation, test evidence, rollback notes, and cost-control assumptions. Escalation path: N&N workstream lead → EPAM Solution Architect → EPAM Delivery Lead → Meridian sponsor if dependency or quality risk threatens milestone dates.

## Key assumptions
- Meridian provides named decision-makers for scope, architecture, security, and release within 5 business days of request.
- Gateway access for the AI-assisted cart-summary path is available in the planned window and does not require a net-new vendor onboarding cycle.
- Client-side APIs, data contracts, and identity dependencies remain materially stable after Phase 1 baseline approval.
- Hypercare covers production stabilization, not net-new feature scope.
- Commercial assumptions and change control apply to any scope beyond the approved checkout modernization and cart-summary chain.

## Client-side dependencies
- Named executive sponsor with authority to unblock policy, budget, and escalation decisions
- Meridian security/legal review for AI gateway usage and data handling
- Client environment, access, and identity-provider readiness
- Client SMEs for checkout, support, and operations acceptance
- Timely review and sign-off of phase exits, especially UAT and release readiness

## Out of scope
Anything outside the checkout modernization and governed AI cart-summary chain — including estate-wide platform replacement, ERP modernization, and non-approved AI vendor onboarding — is out of scope unless added through formal change control.
