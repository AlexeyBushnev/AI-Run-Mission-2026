# 03-competitors

## Competitive map

| Product                                 | Approach                                                                                                                                                                                                                       | Strength                                                                                                                | Weakness                                                                                                                                                                          | Differentiator dimension                                        |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| **Monte Carlo**                         | Solves data incident investigation through observability, lineage, incident workflows, and automated root-cause support across modern data platforms. It is strong at tracing upstream causes and reducing time to resolution. | Strong observability + lineage + incident workflow support. Automated root-cause analysis is clearly part of the offer. | Built for broad data observability, not specifically for parity defects between legacy and migrated IoT pipelines. It is a platform, not a project-shaped investigation workflow. | Broad observability and incident management                     |
| **Acceldata**                           | Solves data reliability through observability, workload insight, anomaly detection, and root-cause support across complex data systems. It emphasizes performance, downtime prevention, and intelligent diagnostics.           | Strong on workload visibility, anomaly detection, and operational observability across data systems.                    | More platform-oriented than investigation-oriented. Less clearly shaped around reusable human-reviewed evidence packs for parity debugging.                                       | Deep operational observability and performance insight          |
| **Atlan**                               | Solves investigation support through metadata, lineage, impact analysis, and governance context. It helps teams understand where data came from, how it changed, and what depends on it.                                       | Strong lineage, metadata context, and impact analysis for debugging and auditability.                                   | Better at context and governance than at guiding a repeatable parity-investigation workflow end to end. It gives visibility, but not a project-shaped investigation assistant.    | Lineage and governance context                                  |
| **Us — Parity Investigation Assistant** | Solves one narrow job: parity-defect investigation between legacy and migrated IoT pipelines. It combines context, evidence capture, root-cause hypothesis support, and reusable reviewed output under human review.           | Strong project fit, direct link to current pain, and clear human-review boundary.                                       | Narrower than the platforms above and depends on good local artifacts, rules, and team adoption.                                                                                  | **Guide parity investigations with reusable reviewed evidence** |

## Where competitors are weak or identical

All three adjacent products are strong at **observability, lineage, or context**, but none is shaped around the exact user moment we care about:
**an engineer investigating a parity defect in a migration and needing a reusable, human-reviewed evidence package.**

That is the opening.

## Named differentiator

**Differentiate by guiding parity investigations with reusable reviewed evidence.**

This is stronger than “better UX” or “faster” because it names:

1. the verb — **guiding**
2. the job — **parity investigations**
3. the dimension — **reusable reviewed evidence**

## AI feature lifted from the scan

**Lifted AI feature:** automated / AI-assisted root-cause hypothesis generation grounded in lineage and incident context.

Why this one:

* Monte Carlo explicitly positions automated root-cause analysis as part of its value.
* Acceldata positions intelligent diagnostics and faster root-cause analysis as part of observability value.
* Atlan emphasizes lineage and impact analysis as the context needed for fast debugging.

## How we fold it into our feature

Our feature should keep **AI-assisted root-cause hypothesis generation**, but make it more specific than the platform competitors:

1. ground the hypothesis in the actual migration artifacts and parity context;
2. require assumptions and validation steps to be written out;
3. leave a **human-reviewed investigation artifact**, not just an alert or suggestion.

## Carry-forward decision

The AI capability that carries forward into the PRD is:

**“Generate evidence-backed root-cause hypotheses for parity defects, with explicit assumptions, validation steps, and reusable reviewed output.”**
