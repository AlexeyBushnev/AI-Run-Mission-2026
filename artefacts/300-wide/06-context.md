# 06-context

## Feature in one sentence
Meridian Availability Assistant helps click-&-collect shoppers judge whether an item is really likely to be available at a nearby store before they commit to pickup.

## Audience
Primary audience: click-&-collect shoppers who want to avoid a wasted trip.  
Secondary audience: retail operations and support teams who need fewer pickup cancellations and fewer trust failures.

## Technical environment
- Web product page and reservation flow
- Availability estimate based on SAP inventory sync plus store-level signals
- AI-enabled availability estimation in the product experience
- Non-PII stock and store metadata may be used in the AI path
- Customer identity and order history stay out of the AI path

## Hard constraints
- Stock data may be stale because SAP sync latency is 15–30 minutes
- GDPR / CCPA must be respected for any personalised surface
- No guaranteed hold language unless a separate hold-confirmation flow exists
- AI output must expose uncertainty when confidence is low
- Fallback must appear when confidence cannot be calculated or data is too old

## Out of scope
- Pricing
- Loyalty
- Store staffing policy
- Full inventory-platform redesign
- Automatic guaranteed hold without separate confirmation logic

## Related artifacts
- `artefacts/300-wide/00-jtbd-feasibility.md`
- `artefacts/300-wide/01-journey-map.md`
- `artefacts/300-wide/01-heuristics.md`
- `artefacts/300-wide/02-workshop.md`
- `artefacts/300-wide/03-decision.md`
- `artefacts/300-wide/04-ai-ac.md`
- `artefacts/300-wide/05-mockup.html`

## Build intent
This handoff is for an AI coding agent building the lo-fi availability-assistant flow. The build must preserve the low-confidence and fallback states, not only the happy path.
