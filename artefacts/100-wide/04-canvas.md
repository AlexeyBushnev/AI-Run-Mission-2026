# 04-canvas

## Problem

When migration defects appear, engineering teams spend too much time manually comparing legacy and PySpark outputs, so reporting decisions are delayed and trust in the data stays low.

## Users

**Primary segment:** Data quality engineers and data engineers working on IoT pipeline migration.
**Sub-segments:** QA engineers validating parity, engineering leads reviewing migration risk, and delivery stakeholders waiting for trusted reporting outputs.

## Value

Reduce parity-investigation time by **≥40%** for migration defects while keeping human review in place and preserving investigation evidence quality.

## Assumptions

1. **≥50%** of parity investigations on the project follow a repeatable pattern that can be supported by a shared AI workflow.
2. Using an AI-assisted parity-investigation workflow can reduce average investigation time by **≥40%** without increasing false conclusions or missed defects.
3. **≥3** engineers on the team would reuse the workflow within **30 days** if it is provided as a shared artifact with clear inputs and output format.

## Solution

Create an agentic parity-investigation assistant that helps engineers investigate migration defects in a structured way. It should read the problem context, compare relevant outputs, suggest likely root-cause categories, guide evidence collection, and produce a reusable investigation summary. The assistant does not make the final engineering decision; it works under human review and produces reviewable artifacts instead of chat-only output.
