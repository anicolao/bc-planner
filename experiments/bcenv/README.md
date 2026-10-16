# Learning loop for changes to bcenv

Status: proposed operating process; no new trial is launched by this change.
Subsequent user authorization permits continued evaluation; individual protocols
still require frozen pins, budgets and isolation checks before execution.
This applies the [bot learning loop](../../battlecode-learning-architecture.md)
to **our environment, instructions, tools and evaluation**, not to bot strategy.
It supplements the approved [2023 plan](../../2023-experiment-plan.md); it does
not amend that plan or absorb the separate PR #9 implementation findings.

## One experiment, one attributable question

1. **Observe a deficiency.** Cite frozen transcript/replay/code evidence. Separate
   observed behavior, causal inference, unknowns and observer hindsight. Preserve
   the failure before proposing a fix. A familiar example is a development case,
   not an unbiased estimate of general capability.
2. **Freeze the comparison.** Copy `templates/experiment.json`. Resolve every pin:
   environment and candidate commits, exact kickoff bytes/hash, model identifier,
   reasoning setting, harness/version, rules/engine, Nix lock, dependencies,
   starting source, maps/opponents/sides/seeds and run order. Record unavailable
   determinism and provider version information honestly. Set independent-agent
   sample size, resource ceilings, stop/retry rules and missing-data treatment.
3. **Preregister before exposure.** Specify hypothesis, one attributable change,
   observable behavioral pass/fail thresholds, counterevidence, outcome/regression
   checks and decision rules before the candidate runs. Commit the completed
   protocol and hash it; append a `preregistered` ledger event before launching.
   The event records the frozen protocol's commit, path and SHA-256, plus an
   immutable observer-only rubric commitment. Review/authorization is a separate
   launch gate. A proposal with unresolved pins is not a preregistration.
4. **Change only the intended variable.** Version the patch separately from
   baseline. Hold kickoff constant when testing tooling; changing instruction and
   tool availability together is a bundled treatment and must be labeled so.
   Do not improve the competitor's strategy yourself. If implementing a change
   reveals a new confound, append a deviation, stop affected runs as specified,
   and preregister a new version rather than rewriting the old prediction.
5. **Run fresh, matched, uncoached trials.** Isolate workspaces and conversation
   history. Both arms receive identical authorized artifacts except the treatment.
   Randomize/counterbalance order; control model, effort, time/token/compute budget,
   fixtures, starting code and visibility. Record every attempt, including errors,
   timeouts and intervention. No selective reruns or silent replacement of weak
   agents. Infrastructure retries follow the frozen rule and remain in the ledger.
6. **Audit then evaluate.** First verify exact input/output hashes, timestamps,
   versions, exposure and completeness. Artifact consistency is not semantic
   correctness. Then score the preregistered behavioral mechanism from turn/unit
   evidence, including what the bot could know. Finally report downstream bot
   outcomes, regressions and cost separately. A win is not proof of diagnosis;
   a correct diagnosis is not proof of competitive improvement. Blind assessors
   to arm when feasible; log failures of blinding and inter-review disagreement.
7. **Decide and retain the lesson.** Append `keep`, `reject` or `inconclusive` with
   evidence, uncertainty, deviations, actual cost, lessons and next question.
   Keep requires the preregistered mechanism and regression criteria; insufficient
   evidence is inconclusive, not success. Keep means recommended environment
   adoption, not permission to merge. Failed experiments remain first-class data.

## Isolation and claims

- **Fresh continuation:** a new agent starts with a specified frozen baseline bot
  and authorized artifacts. This measures diagnosis/improvement of inherited code.
- **From scratch:** a new agent starts without that bot or its analysis. This
  measures a different task; never pool the two or call continuation from scratch.
- The observer rubric, expected weakness, prior review and results live outside
  the competitor filesystem, tool context, kickoff and conversation. A fresh
  child with inherited parent history is not uncoached. Use explicit allowlists
  and inspect the actual delivered context. Public planning material containing
  the answer must also be inaccessible during the trial; otherwise mark exposure
  and invalidate the independence claim. Hash a private rubric before runs; publish
  a redacted rubric or its full contents only after exposure-sensitive work ends.
- Known cases can test whether a tool exposes a mechanism. Generalization needs
  untouched, preregistered holdouts and independent trials. Repeated deterministic
  games on one map are not independent samples. Define holdouts before inspection,
  log access, retire them after use and never quietly tune on them.
- Log assistance verbatim. Safety/infrastructure intervention may be necessary;
  it is a deviation, not permission to coach the diagnosis or suppress that run.

## Durable records and workflow

`templates/experiment.json` is a copyable protocol/result checklist.
`proposals/BCENV-001.json` is the first **unrun proposal**, with open pins and gates.
`ledger.jsonl` is the append-only chronological event log, initially containing
its proposal and preflight deviation events. Each line uses `ledger.schema.json`; superseding events
reference earlier event IDs. Correct mistakes by appending `correction` events.
Never overwrite a preregistration, result, failed run or original artifact.
Keep large/private artifacts in approved immutable storage; record hash, locator,
access scope, producer and timestamp. A hash without retrievable bytes is not
reproducibility. Publish no raw private source, credentials or hidden rubric here.

Validate before committing (Node 20+, existing Nix-managed toolchain):

    node scripts/check-bcenv-ledger.mjs experiments/bcenv/ledger.jsonl BASE_COMMIT
    npm test

`BASE_COMMIT` must be the reviewed/trusted history boundary. The validator checks
schema-like field constraints, lifecycle references and byte-for-byte prefix
preservation against that commit. Omitting the base checks structure only.
Review still must check truthful claims, actual artifact hashes, hidden-context
isolation and preregistration timing; this tool cannot prove them. Merge conflicts
must preserve all events with unique IDs; order competing appends explicitly.
Do not rewrite old rows to make a conflict disappear.

The first proposed experiment is [BCENV-001](proposals/BCENV-001.json). Its source
is retrospective [PR #9](https://github.com/anicolao/bc-planner/pull/9), specifically
commit `302822e`; those prior trials were not preregistered under this new process.

## Improving this process itself

Keep this lightweight: use one completed record to ask whether a reviewer can
reconstruct the question, falsify the claim and trace the decision to evidence.
If a missing field or confusing gate prevents that, record the concrete failure,
make one small template/check change and check it on a retained record. Do not
retrofit old trials as preregistered or create an infinite hierarchy of process
experiments. Measure usefulness by recoverable evidence and honest decisions,
not checklist length. Remove redundant steps through review while preserving
original records and their provenance.

## Model selection after the diagnostic screen

The user's subsequent instruction is to continue until a model recommendation
is supported by evidence. BCENV-001 alone cannot decide that. Preregister the
model-comparison stage separately: cross the selected environment with explicitly
named model/settings, use fresh independent agents and several untouched cases,
report paired behavioral validity, independent discovery, unsupported claims,
downstream outcomes where actually tested, and actual time/token/compute cost.
Freeze a decision rule and uncertainty treatment before results; do not choose
weights or a winner afterward. Include from-scratch work if the recommendation
is meant to cover it. If results disagree across tasks, recommend by task rather
than force a universal winner. Continue until the preregistered evidence criterion
is met or an explicit budget/access/authorization blocker requires user input.
Do not declare a winner from repeated deterministic games or from the known case.

A relative winner is insufficient: preregister an absolute adequacy floor for the
intended environment/task (legal execution, grounded diagnosis, meaningful tests,
honest interpretation, reliable artifacts and acceptable cost). If every model
fails that floor, improve the environment and retest; report no acceptable model
yet. The user's instruction to iterate and notify completion does not authorize
claiming success merely because one weak result beats another.

### First proposal preflight finding (no trial)

The subsequent implementation coordinator inspected ReplaySummary.java and found
only the first 32 action/move/resource samples, with no arbitrary bounded-turn
query. BCENV-001's evidence-access prerequisite is therefore unresolved: do not
launch its instruction-only trial against that interface. A separately pinned
generic replay-query tooling proposal and engineering verification must precede
it. This is a preflight design finding, not an experimental failure or result.
