# REFERENCE

## Versioned rubric summary
- Use the current rubric from `00-rubric.md`
- Score each output per rubric dimension, not by overall impression

## Judge prompt
- Score each output against each rubric rule
- Give one-line reasoning per rule
- Flag borderlines within one band of the pass line
- Report per-rule agreement, not only a single average

## Calibration notes
- Hold below ship if any per-rule agreement is < 85%
- Known-bad calibration outputs must not score as pass

## Bucket contract
- happy: 10
- edge: 8
- adversarial: 6
- multilingual: 3
- sensitive: 3
