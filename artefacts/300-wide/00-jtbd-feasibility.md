# 00-jtbd-feasibility

**Feature:** Meridian availability assistant
**User:** Click-&-collect shopper

## JTBD

When I need an item soon and want to collect it from a nearby store, I want to know whether it is really likely to be available there, so I do not make a wasted trip for a product that is not actually on the shelf.

## Feasibility checklist

### Branch 1 — AI IN THE PROCESS (team using AI to design / deliver)

| Check                                 | Verdict | Rationale                                                                                                        |
| ------------------------------------- | ------- | ---------------------------------------------------------------------------------------------------------------- |
| Client permits AI tools for delivery? | Yes     | The brief says EPAM CodeMie is pre-approved and third-party AI is permitted for delivery with anonymised inputs. |
| Sensitive data kept out of AI inputs? | Yes     | Non-PII stock and store metadata go to the AI; customer identity and order history stay out of the AI path.      |
| Approved toolset named?               | Yes     | CodeMie is explicitly approved, and Claude / GPT / Gemini are allowed with anonymised inputs.                    |

**Branch 1 verdict:** **Yes** — AI may be used in the delivery process because tools are permitted, sensitive customer data is excluded, and the approved toolset is named.

### Branch 2 — AI IN THE PRODUCT (the availability assistant itself)

| Check                                                           | Verdict     | Rationale                                                                                                                     |
| --------------------------------------------------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Stock data ready + fresh enough for the promise we’d make?      | Conditional | SAP sync latency is 15–30 minutes, so stock may be stale and the product must avoid over-promising certainty.                 |
| Regulatory framework clear (GDPR / CCPA; AI Act class)?         | Conditional | GDPR and CCPA clearly apply to personalised surfaces; AI Act high-risk classification is not expected, but still unconfirmed. |
| Worst-case understood (who is harmed if the estimate is wrong)? | Yes         | If the estimate is wrong, the shopper wastes a trip, trust drops, and Meridian risks cancellations and churn.                 |

**Branch 2 verdict:** **Conditional** — AI in the product is acceptable only if the assistant is positioned as an estimate, handles stale data explicitly, and avoids promising guaranteed store availability.

## Approved tools for the rest of the series

* EPAM CodeMie
* Claude / GPT / Gemini for delivery work with anonymised inputs only

## Working decision

Proceed with the feature **conditionally**: AI is clearly allowed in the process, and AI in the product is allowed only with clear uncertainty handling, no false guarantee language, and confirmation of the regulatory position before release.
