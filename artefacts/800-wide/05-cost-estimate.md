# 05-cost-estimate

## Input assumptions
- Cloud rent: **$1,500 / month** (3 pods + 1 Postgres + 1 Redis + 1 load balancer)
- AI input tokens / call: **1,200**
- AI output tokens / call: **200**
- AI calls / month: **3,000,000**
- Kata price point: **$2.50 / 1M input tokens** and **$10.00 / 1M output tokens**
- Current official OpenAI GPT-4.1 price point used for comparison: **$2.00 / 1M input tokens** and **$8.00 / 1M output tokens**

## Line-by-line arithmetic

### Token volume per month
- Input tokens/month = `3,000,000 × 1,200 = 3,600,000,000`
- Output tokens/month = `3,000,000 × 200 = 600,000,000`

### Monthly AI cost — using the kata price point
- Input cost = `3,600,000,000 / 1,000,000 × $2.50 = $9,000`
- Output cost = `600,000,000 / 1,000,000 × $10.00 = $6,000`
- AI meter total = **$15,000 / month**

### Monthly AI cost — using the current official GPT-4.1 comparison point
- Input cost = `3,600,000,000 / 1,000,000 × $2.00 = $7,200`
- Output cost = `600,000,000 / 1,000,000 × $8.00 = $4,800`
- AI meter total = **$12,000 / month**

## Monthly total

### At the kata price point
- Cloud rent = **$1,500**
- AI meter = **$15,000**
- **Total = $16,500 / month**

### At the current official GPT-4.1 comparison point
- Cloud rent = **$1,500**
- AI meter = **$12,000**
- **Total = $13,500 / month**

## Spend split
The cost split matters because the two parts behave differently:

### Kata price point split
- Sticky cloud rent: **$1,500** → **9.1%**
- Scaled AI meter: **$15,000** → **90.9%**

### Current official GPT-4.1 comparison split
- Sticky cloud rent: **$1,500** → **11.1%**
- Scaled AI meter: **$12,000** → **88.9%**

## Spend owner
This spend should be owned by the **cart / checkout feature team and its product or business budget owner**, not by the platform team alone. The platform team provides the floor, but the summarise-my-cart feature drives the metered AI spend.

## Ship line and recommendation
Use this decision threshold for first release:

- **Ship**: total monthly cost **≤ $12,000**
- **Ship with mitigation**: total monthly cost **> $12,000 and ≤ $15,000**
- **Reject / do not ship as-is**: total monthly cost **> $15,000**

### Recommendation
- **Using the kata price point ($16,500/month): REJECT as-is**
- **Using the current official GPT-4.1 comparison point ($13,500/month): SHIP WITH MITIGATION**

The reason is clear from the split: cloud rent is not the problem; the AI meter is the dominant risk.

## DIAL hard cap and alert
Recommended gateway controls:

- **Hard cap on AI spend:** **$12,000 / month**
- **Alert threshold:** **$9,000 / month**
- **Escalation threshold:** **$10,500 / month**
- **Action at hard cap:** degrade or disable the “summarise my cart” feature rather than letting uncapped AI traffic continue

## Operational note
A cap without an alert below it is too late. The alert must fire before the hard cap so the team can respond while the feature is still serving normally.

## Bottom line
This app is mostly a **metered-AI-cost problem**, not a cloud-rent problem. The arithmetic supports a strong operational bound: if the feature ships, it should ship with a DIAL cost cap and alerting from day one.
