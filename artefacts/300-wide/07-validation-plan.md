# 07-validation-plan

## Objective
Validate whether the redesigned availability assistant helps click-&-collect shoppers understand uncertainty before they commit to pickup, especially in low-confidence and fallback states.

## Test format
Task-based moderated usability test with the lo-fi prototype from `artefacts/300-wide/05-mockup.html`.

## Participant profile
- Shoppers who use click-&-collect or similar retail pickup flows
- At least some participants must be people who care about same-day pickup and avoiding wasted trips

## Task questions

1. **Show me how you’d check whether this item is collectable at a store near you today.**
2. **Show me how you’d decide whether the “Likely available” message is strong enough for you to continue.**
3. **Show me what you would do if the page says “Check with store” instead of giving a confident availability result.**
4. **Show me how you’d choose between the closest store and the store with the stronger availability confidence.**
5. **Show me how you’d tell whether Meridian is promising a guaranteed hold or only an estimate.**

## What to observe
- Whether participants notice the confidence cue
- Whether participants understand that “Likely available” is not a guarantee
- Whether participants can use the fallback path without confusion
- Whether participants can explain the difference between estimate and hold
- Whether participants choose a safer option when confidence is weak

## Success criteria
- At least 4 of 5 participants correctly explain that low-confidence availability is an estimate, not a guaranteed hold
- At least 4 of 5 participants successfully use the fallback path when confident availability is not available
- At least 4 of 5 participants identify the freshness / uncertainty signal without prompting

## Risks to watch
- Users may still read “Likely available” as a promise
- The fallback path may feel like a dead end instead of a safe alternative
- Confidence language may reduce trust if it feels vague or evasive
