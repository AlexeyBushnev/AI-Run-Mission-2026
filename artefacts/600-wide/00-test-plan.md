---
case: Meridian Retail Group — Click & Collect
feature: Cross-channel Click & Collect journey — QA one-page test plan
date: 2026-06-09
author: Aleksei Bushnev
---

# 00-test-plan

## In scope
- Loyalty/account resolution for a shopper who starts online and completes or confirms pickup in-store.
- Cart and reservation continuity across web, mobile, and store-assisted pickup flow.
- Store-level availability and pickup confirmation path that depends on SAP-backed inventory signals.
- EU pickup-confirmation payment path where PSD2 SCA may be triggered.
- Customer and associate error-handling for stock mismatch, identity mismatch, and payment-confirmation failure.

## Out of scope
- SAP ECC inventory ground-truth correctness across the enterprise.  
  Rationale: this is a source-system control area owned outside the feature team; this plan tests the feature's handling of SAP-fed availability, not whether SAP is globally correct.
- Full omnichannel platform coverage outside the Click & Collect journey.  
  Rationale: this plan is intentionally limited to one cross-channel flow so downstream test cases stay bounded.

## Top-3 risks
1. **Phantom-stock cancellation at pickup**  
   Failure: the feature confirms collectability even though the item is not actually available at the store.  
   User impact: the shopper makes a wasted trip and loses trust in pickup promises.  
   Business impact: direct revenue loss, higher cancellation rate, and escalation from Retail Ops because the 7% phantom-stock baseline does not improve.

2. **Identity collision or wrong-account merge**  
   Failure: the system resolves the wrong loyalty/account identity during cross-channel handoff or pickup confirmation.  
   User impact: a shopper sees another customer's order or loyalty history, or cannot retrieve their own order.  
   Business impact: GDPR/privacy exposure and incident escalation through compliance/security stakeholders.

3. **PSD2 SCA failure on EU pickup confirmation**  
   Failure: the payment-confirmation flow fails, loops, or times out when strong customer authentication is required.  
   User impact: the shopper cannot complete confirmation or pickup payment in the critical moment.  
   Business impact: conversion drop-off in EU flows and risk to regional pilot confidence.

## Entry criteria
- Phase 1 Click & Collect build is deployed to the QA region with test logging enabled.
- SAP sandbox is seeded with realistic store inventory deltas, including at least one stale or conflicting availability scenario.
- Identity-provider test setup is configured for normal, duplicate-account, and wrong-account-resolution scenarios.
- EU payment/SCA test path is enabled in QA with non-production payment credentials.

## Exit criteria
- Critical-path pass rate is **>= 95%** across approved priority-1 and priority-2 cases.
- **0** priority-1 phantom-stock failures remain open at test exit.
- **0** open severity-1 defects remain in identity, payment confirmation, or pickup confirmation flows.
- Named sign-off is recorded from **David Park** (Retail Ops) and **Sarah Chen** (CX / business owner) for the scoped journey.
