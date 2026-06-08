# 00-discovery-context

**Source note**  
This context pack is derived from the Meridian summary available in the kata materials and earlier module context, not from the full internal reference-case document.

## Business layer
- Meridian Retail Group is running a **$42M, 18-month transformation** to merge **22 regional commerce stacks** into one omnichannel-commerce platform.
- The business pressure is cross-channel retail consistency: Meridian needs a single commerce experience instead of fragmented regional stacks.
- Success depends on reducing operational fragmentation while improving customer-facing omnichannel journeys such as click-and-collect.
- Key stakeholders implied by the brief include board/program sponsors, commerce leadership, regional business owners, retail operations, and platform delivery teams.

## Product layer
- Meridian is an **omnichannel commerce platform** with customer-facing surfaces across web/app commerce and in-store-linked journeys.
- A named user moment already carried from Module 300 is the **click-&-collect availability assistant**: the shopper needs to know whether an item is really likely to be available at a nearby store before committing to pickup.
- The platform must support cross-channel customer flows, including browsing, cart, checkout, inventory visibility, and pickup/fulfillment experiences.
- Case details mention **local payment methods**, so checkout must work across different regional customer expectations and payment journeys.

## Engineering layer
- The target platform context includes **AWS EKS**; this is an explicit infrastructure/platform anchor and should be treated as given.
- Meridian must coexist with legacy enterprise systems while the transformation is underway; the kata set repeatedly references **SAP ECC** as the inventory source of truth during the transition.
- The architecture problem is not greenfield: online and in-store inventory must be bridged while legacy systems continue to operate.
- The case repeatedly frames integration questions around inventory, ordering, checkout, and event/data flows rather than isolated page-level UI changes.

## Regulatory layer
- **PSD2 SCA** applies on the EU checkout path, which means strong customer authentication must be supported in checkout flows and will add latency/flow complexity.
- **PCI-DSS Level 1** applies, which means card-payment handling must stay within strict payment-security controls and architecture boundaries.
- **GDPR** applies, so personal-data handling, consent, and regional data protections must be reflected in architecture decisions.
- The brief also names **local payment methods**, which implies region-specific checkout integrations and compliance behavior across markets.

## Five implicit assumptions

1. **Assumption:** A single target architecture can realistically replace or unify the regional stacks within the program window.  
   **Hint in brief:** "$42M, 18-month program to merge 22 regional commerce stacks."  
   **What breaks if wrong:** The roadmap, migration sequencing, and architecture options may be too optimistic; transitional coexistence may dominate longer than planned.

2. **Assumption:** SAP ECC inventory data can support the availability promises the digital platform wants to make.  
   **Hint in brief:** Meridian needs to bridge online and in-store inventory while SAP ECC remains the source of truth.  
   **What breaks if wrong:** Click-&-collect availability, reservation confidence, and cross-channel inventory features become misleading or unusable.

3. **Assumption:** The chosen payment architecture can satisfy both PSD2 SCA and local payment-method variation without fragmenting checkout again.  
   **Hint in brief:** PSD2 SCA / PCI-DSS Level 1 and local payment methods are all in scope.  
   **What breaks if wrong:** EU checkout performance, compliance, and regional parity may all fail, pushing the design back toward local exceptions.

4. **Assumption:** Regional business processes are similar enough that shared platform patterns will be accepted.  
   **Hint in brief:** The program aims to merge 22 regional stacks into one platform.  
   **What breaks if wrong:** Standardized flows, shared services, and common integration contracts may be rejected by regional stakeholders or require expensive variation paths.

5. **Assumption:** Cross-channel customer trust is worth designing as an architectural concern, not just a UX concern.  
   **Hint in brief:** The Meridian case centers on omnichannel journeys such as click-and-collect availability and checkout reliability.  
   **What breaks if wrong:** The architecture may optimize system consolidation while missing the real user failure modes that drive cancellations, churn, or weak adoption.
