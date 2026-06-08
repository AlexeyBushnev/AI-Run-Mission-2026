# K 5.W.9 - By-hand vs by-agent comparison

## What both produced
Both approaches produced the same core delivery chain for the logsum feature:
- a written spec (`spec.md`)
- an implementation (`src/logsum.py`)
- tests (`tests/test_logsum.py`)
- a CI workflow (`.github/workflows/ci.yml`)
- a refactor review note (`refactor-notes.md`)
- a provenance artifact (`provenance-note.md`)

Both paths also preserved the same intended feature behavior:
- group events by normalized `level`, trimmed `service`, and normalized `message`
- treat missing `level` as `UNKNOWN`
- skip malformed timestamp rows with a warning
- keep the default CLI behavior unchanged when no extra flag is passed

## Where the agent saved time
1. **Boilerplate generation**
   The agent was faster at producing first drafts of repetitive artifacts such as the CI workflow, provenance note, and test skeleton.

2. **Cross-file consistency**
   When asked for a bounded change like `--min-count N`, the agent updated code, spec, and tests in one pass instead of requiring manual hopping between files.

3. **Documentation speed**
   The agent produced structured notes quickly: context-load checks, refactor notes, provenance, and Q&A scaffolding all came out faster than writing them manually.

## Where the agent went wrong or shorter
1. **Repeatedly re-offered unchanged files**
   In several later katas, the agent provided download links for files that were effectively unchanged. This saved no review time and created confusion about what had really changed.

2. **Weak environment awareness**
   The agent struggled to verify tests reliably in this runtime. It could generate the test suite, but the execution evidence was weaker than the supervised path needed. Green intent is not the same as a trustworthy green run.

3. **Overstated completion risk**
   Some artifacts looked complete before they were fully verified. Example: test and refactor outputs were drafted correctly in structure, but local execution evidence was incomplete or environment-limited.

## What the agent did better
1. **Faster first-draft coverage**
   The agent was better at getting all required sections onto the page quickly, especially for specs, CI files, provenance notes, and structured review artifacts.

2. **Consistency of wording**
   The agent kept terminology aligned across files more consistently than a rushed manual pass would have done.

3. **Constraint-following on bounded tasks**
   When the task was narrow and explicit, such as adding `--min-count N` while keeping default behavior unchanged, the agent handled the code + spec + tests bundle efficiently.

## What I learned about supervised vs async
The supervised path was stronger where correctness depended on:
- reading diffs carefully
- catching silent removals
- checking whether evidence was real rather than merely plausible
- deciding whether a failure was a code bug, test bug, or spec ambiguity

The async / agent path was stronger where the work was:
- bounded
- low-ambiguity
- repetitive across files
- easy to compare against a contract

The biggest difference is not code generation. It is **evidence quality**.  
Supervised work made it easier to trust what changed and why. Async work made it easier to produce artifacts quickly, but only when the task boundary and provenance were explicit.

## What I would do differently next time
1. I would define the task boundary even more tightly before switching to agent execution.
2. I would require the provenance note **before** reviewing the diff every time.
3. I would treat runtime verification as a separate acceptance step, not as something implied by generated artifacts.
4. I would avoid accepting “updated file” outputs unless I can point to the exact changed behavior or changed lines.
5. I would use the agent first for scaffolding and bounded deltas, but keep supervised review for spec edge cases, refactors, and anything affecting behavior preservation.

## Three concrete deltas
1. **Supervised path advantage:** the implementation bug around missing `timezone` import was caught and fixed with explicit human review of the execution result.
2. **Agent path advantage:** the `--min-count N` task was easy to push across code, spec, tests, and provenance in one bounded pass.
3. **Agent path weakness:** repeated delivery of unchanged files reduced trust in whether later outputs actually differed from the reviewed state.
