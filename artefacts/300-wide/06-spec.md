# 06-spec

## User story
As a click-&-collect shopper, I want to see estimated store availability with a visible confidence cue before I reserve, so that I can avoid a wasted trip when stock is uncertain.

## Base AC
- AC1. When a product has store stock data, the product page shows an availability indicator per nearby store.
- AC2. When no store within range has the item, show “Not collectable nearby” and a delivery option.
- AC3. When stock data is missing for a store, omit that store and do not guess.
- AC4. When the user taps a store, show last-confirmed time and distance.

## Refined AI-AC mappings

| AI-AC | Component | Variant / State | Color token | Typography | Placement | Visual gate |
|---|---|---|---|---|---|---|
| Confidence | Availability badge | `low-confidence` = “Likely available” when confidence < 0.70 | `status/warn/bg`, `status/warn/text` | label / semibold / small | Product page, directly under item title and in store row | Must not render “In stock” below threshold |
| Refusal / fallback | Fallback callout | `fallback-stale-data` when data > 30 min old or confidence unavailable | `status/error/bg`, `status/error/text` | body / regular / small | Store row and confirmation screen | Must show “Check with store” + contact option |
| Latency | Availability module | `loading`, `loaded`, `timed-out` | `surface/default`, `text/default` | body / regular / small | Product page availability block | 95% of nearby-store results visible within 2s |
| Disclosure | Helper text | `estimate-disclosure` | `text/subtle` | caption / regular | Immediately adjacent to availability label | Must state estimate from store data; not a guaranteed hold |
| Feedback | Feedback row | `helpful-yes-no` | `surface/default`, `border/default` | body / regular | Fallback or low-confidence state footer | Must show visible feedback action after uncertain result |
| Negative AC | Reservation CTA / copy | `no-guarantee-copy` | `text/default` | body / regular | Product page and reserve/confirm screen | Must not show exact shelf count or imply guaranteed hold |

## Components

### 1. Availability badge
**Purpose:** communicate store-level availability with confidence-aware wording.

**States**
- `high-confidence`: “In stock”
- `low-confidence`: “Likely available”
- `fallback`: “Check with store”
- `unavailable`: “Not collectable nearby”

**Token references**
- `status/success/*`
- `status/warn/*`
- `status/error/*`
- `text/default`
- `text/subtle`

**Linked AC**
- AC1
- AI-AC1 confidence
- AI-AC4 disclosure
- AI-AC6 negative AC

**Asset reference**
- `artefacts/300-wide/05-mockup.html` — screen 1 product page

### 2. Store availability row
**Purpose:** show per-store availability status, freshness, distance, and next action.

**States**
- `available-estimated`
- `stale-data-fallback`
- `not-nearby`
- `selected`

**Token references**
- `surface/card`
- `border/default`
- `status/warn/*`
- `status/error/*`

**Linked AC**
- AC1
- AC3
- AC4
- AI-AC2 refusal / fallback
- AI-AC3 latency

**Asset reference**
- `artefacts/300-wide/05-mockup.html` — screen 1 store list

### 3. Reserve / confirm panel
**Purpose:** let the shopper continue with clear uncertainty handling before commitment.

**States**
- `reserve-with-caution`
- `request-confirmation`
- `pick-another-store`

**Token references**
- `action/primary/*`
- `action/secondary/*`
- `status/warn/*`

**Linked AC**
- AI-AC1 confidence
- AI-AC4 disclosure
- AI-AC6 negative AC

**Asset reference**
- `artefacts/300-wide/05-mockup.html` — screen 2 reserve / confirm

### 4. Fallback callout
**Purpose:** explain why the system cannot confirm availability and present safe alternatives.

**States**
- `stale-data`
- `no-confidence`
- `alternative-options`

**Token references**
- `status/error/*`
- `action/primary/*`
- `action/secondary/*`

**Linked AC**
- AC2
- AI-AC2 refusal / fallback
- AI-AC5 feedback
- AI-AC6 negative AC

**Asset reference**
- `artefacts/300-wide/05-mockup.html` — screen 3 fallback

## Negative AC carried into spec
The product must **not**:
- state an exact shelf quantity
- imply the item is reserved, held, or guaranteed for pickup
- show “In stock” when confidence is below 0.70
- estimate collectability when data is older than 30 minutes and no confidence can be calculated

## Definition of Handoff Done check
- [x] User story + base AC present
- [x] ≥ 3 AI-AC refined to component / variant / token / placement / visual gate
- [x] `06-context.md` covers feature + audience + environment + constraints + out-of-scope
- [x] `06-spec.md` lists ≥ 2 components with states + token references
- [x] Asset / data reference explicit and resolvable
- [x] Negative AC carried into `06-spec.md`
