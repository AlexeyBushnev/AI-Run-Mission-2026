# 02-primary-signal

**Playground context**  
North American residential HVAC / smart-home IoT, $5B+ revenue band.  
Regulatory pressure: CCPA/CPRA plus connected-device cybersecurity obligations.  
Dominant problem from 01-context-brief: weak trust in telemetry and migration outputs because data-quality and parity defects slow reporting and downstream decisions.

**Source quality note**  
This file uses a **public-source fallback**, not internal interviews or support-call transcripts. The verbatims below come from public forums and public support communications, so they are useful directional signal but weaker than direct customer interviews.

## A. Customer / user verbatims clustered into themes

### Theme 1 — Users want control, but smart-home automation can feel over-engineered
- “there is no manual mode” — source: r/ecobee discussion, “No manual mode, ridiculously over engineered”
- “people overhwhelmingly dislike the changes” — source: r/HomeImprovement discussion about ecobee app update

**Interpretation:** Users do not only want automation. They also want predictable override, low-friction control, and app changes they can understand.

### Theme 2 — Reliability failures destroy trust faster than feature gaps
- “they’re known for doing this” — source: r/hvacadvice post about Nest thermostat and damaged furnace board
- “it's nothing but trouble” — source: r/Nest post, “Nest thermostat is just junk”

**Interpretation:** When climate-control products are seen as causing failures or instability, trust breaks at the product level, not only at the feature level.

### Theme 3 — Product lifecycle and support continuity are part of the customer pain
- “will no longer connect to or work in the Google Nest app” — source: public Nest end-of-support notice reposted in r/Nest

**Interpretation:** Customers depend on long-lived connected-device support. Support or connectivity loss becomes a real operational risk, not only a technical detail.

## B. Competitor teardown — ecobee (consumer thermostat + app workflow)

**Workflow walked:** product page → app capabilities → installation/setup path → scheduling/automation → energy reporting

### Solved well
1. **Setup and onboarding**
   - The app offers “step-by-step installation instructions.”
2. **Comfort and occupancy-based control**
   - ecobee says SmartSensor can detect occupied rooms and adjust temperature.
3. **Basic energy visibility**
   - ecobee now surfaces Home Energy Reports in the app and positions them as easier to access and use.

### Solved partially
1. **Energy insights**
   - Energy reports exist, but support docs say a thermostat must be registered for a full calendar month before reports start generating.
2. **Automation**
   - Scheduling, geofencing, Follow Me, and Autopilot improve comfort, but public verbatims suggest some users experience smart features as too complex or hard to override.
3. **Whole-home ecosystem value**
   - ecobee combines thermostat, sensors, home monitoring, and rebates, but this is still mainly a consumer control experience rather than an operational data-trust solution.

### Unsolved for this segment
1. **Telemetry trust and migration parity**
   - The consumer product improves control and reporting, but it does not solve backend parity, pipeline quality, or engineering trust in migrated outputs.
2. **Engineering-grade root-cause visibility**
   - Energy reports and app controls help the end user, but they do not expose the kind of pipeline, schema, or transformation evidence needed by data and engineering teams.
3. **Client-boundary governance**
   - The product helps at the user layer, but not at the delivery-system layer where data boundaries, approval rules, and governed artifacts matter.

## C. Re-rating the three pain points from 01-context-brief

### 1. Product trust is now a market issue, not just an engineering issue
**Re-rating:** Confirmed  
**Why:** Public verbatims directly show loss of trust from reliability, forced automation, and lifecycle concerns: “there is no manual mode,” “they’re known for doing this,” and “will no longer connect to or work in the Google Nest app.”

### 2. Competition is shifting from single devices to connected ecosystems
**Re-rating:** Confirmed  
**Why:** The ecobee teardown shows a combined offer across thermostat control, room sensors, home monitoring, automations, rebates, and in-app energy reports. This supports the idea that the competitive surface is now ecosystem-shaped, not only device-shaped.

### 3. Internal data quality becomes strategy-critical when products, reporting, and compliance all depend on telemetry
**Re-rating:** Sharpened  
**Why:** The teardown did not directly prove backend data-quality pain from customer verbatims, but it showed that competitors are increasing the amount of customer-facing reporting and automation. That raises the cost of weak telemetry trust and strengthens the original pain as an operational and delivery-side risk rather than a direct customer quote.

## Ranked pain points by strength of PRIMARY evidence
1. **Product trust is now a market issue** — strongest direct quote support
2. **Competition is shifting to connected ecosystems** — strong teardown support
3. **Internal data quality becomes strategy-critical** — sharpened by teardown, but still less direct from public customer quotes

## Sources used
- Reddit, r/ecobee, “No manual mode, ridiculously over engineered,” public discussion.
- Reddit, r/HomeImprovement, “Opinions on Home Automation,” comment on ecobee app update.
- Reddit, r/hvacadvice, “If all HVAC guys hate Nest, what’s the best smart thermostat?”
- Reddit, r/Nest, “Nest thermostat is just junk.”
- Reddit, r/Nest, “Upcoming end of support for Nest Learning Thermostats...”
- ecobee App Store listing.
- ecobee product pages for Smart Thermostat Premium / Enhanced.
- ecobee support pages for Home Energy Reports, Follow Me, Smart Home & Away, and registration requirements.
