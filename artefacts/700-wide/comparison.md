# comparison

## One time-saving
The agent-style hand-off saved time by scaffolding the full second pipeline pattern in one pass: synthetic raw data generation, bronze-to-silver cleaning, gold aggregations, DQ checks, and notebook chart code. Building that structure from a blank page would have taken more than 5 minutes even before review.

## One mistake
The human review had to check the dropout-rate denominator explicitly. This is the same error class as the earlier returns-rate metric: an agent can easily drift to `dropped_count / completed_count` instead of `dropped_count / total_enrollments`. The reviewed final pipeline uses `dropped_count / (completed + in_progress + dropped)` through `total_enrollments`, which matches the business definition.
