# 07-narrative

## Redesign summary
This redesign changes Meridian’s availability experience from a binary “In stock” promise to an estimate with visible confidence and fallback behavior. The goal is to reduce false certainty before the shopper commits to pickup and to provide safer options when the system is unsure.

## Benefit
The main benefit is fewer wasted trips caused by phantom stock. The redesign makes uncertainty visible earlier, helps shoppers choose a safer store or fallback path, and reduces the trust damage caused by a cancellation at pickup.

## Engineering cost
Low to medium. The first version mainly changes availability presentation, confidence handling, freshness display, and fallback states. It does not require a full inventory-platform redesign or a guaranteed-hold workflow.

## Design cost
Medium. The work includes redesigning the product-page availability module, reserve/confirm state, fallback state, and the supporting content and interaction logic.

## Content cost
Low to medium. Meridian needs clear uncertainty wording, disclosure text, fallback copy, and feedback wording that explain the estimate without sounding evasive.

## Expected outcome metric
Reduce click-&-collect cancellation at pickup caused by phantom stock from **about 7% to below 3%** after rollout of the redesigned availability experience.

## Why this metric matters
This is the clearest signal that the redesign is working. If the cancellation rate does not improve, then the new confidence and fallback design is not solving the real user problem, even if the interface looks clearer.
