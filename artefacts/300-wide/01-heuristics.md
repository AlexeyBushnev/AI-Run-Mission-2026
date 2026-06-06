# 01-heuristics

**Method:** Nielsen heuristic review based on the supplied journey and screen descriptions  
**Screens reviewed:** product page availability label, reservation confirmation, pickup-counter email  
**Source quality note:** This is based on screen descriptions rather than live screenshots, so findings are design hypotheses that should be validated against real UI.

## Confirmed heuristic findings

| Screen | Element | Heuristic violated | Why it is a violation | Status |
|---|---|---|---|---|
| Product page | “In stock” availability label | Match between system and the real world | The label suggests a level of certainty that may not match actual shelf reality when stock is stale or inaccurate. | Confirmed |
| Product page | “In stock” without visible uncertainty or freshness cue | Visibility of system status | The system does not show whether the stock signal is recent, estimated, or uncertain. | Confirmed |
| Reservation confirmation | Confirmation message after reservation | Error prevention | The flow confirms pickup before preventing the core failure mode: phantom stock. | Confirmed |
| Reservation confirmation | Confirmation language without caution or next-step expectation | Help users recognize, diagnose, and recover from errors | The user is not prepared for what happens if the shelf check fails later. | Confirmed |
| Pickup-counter email | Pickup message that implies ready collection | Consistency and standards | If the email implies standard pickup confidence while the real stock is uncertain, the experience becomes internally inconsistent. | Conditional / likely confirmed |

## Discarded or weak findings

| Screen | Candidate issue | Reason discarded |
|---|---|---|
| Product page | “Aesthetic and minimalist design” | No real evidence from the supplied journey or screen description |
| Reservation confirmation | “User control and freedom” | Possible, but not strongly supported without the real screen and action set |
| Pickup-counter email | “Flexibility and efficiency of use” | Too generic; could not tie to a specific element in the supplied description |

## Most important violations to carry forward

1. **Match between system and the real world**  
   The “In stock” label does not match the real certainty level of shelf availability.

2. **Visibility of system status**  
   The journey hides uncertainty, freshness, and confidence when those are exactly what the user needs.

3. **Error prevention**  
   The flow allows a strong promise before the retailer has enough confidence to make it safely.

## Design implication

The redesign should make availability **legible as an estimate**, not a guaranteed fact, and should signal uncertainty early enough that the user can decide before committing the trip.
