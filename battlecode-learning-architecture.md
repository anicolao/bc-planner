# Battlecode agent learning system

**Status:** Initial design, 2026-10-15  
**Purpose:** A shared reference for Alex and dot before implementation begins.

The system should enable coding agents such as Codex CLI to produce competitive Battlecode entries through an evidence-driven learning loop. Its central requirement is detailed understanding of match replays: an agent must be able to explain what happened, predict how a proposed change will alter behavior, and check that prediction against subsequent matches.

This document records the direction agreed in conversation and proposes a concrete architecture for carrying it out. The competition edition, rules, runtime, hosting, budget, and submission requirements remain unresolved. No platform integration or replay capability described here has yet been verified.

## Responsibility and scope

### Agreed responsibility

dot designs and coordinates the system that enables coding agents to compete effectively. This includes experiment structure, agent coordination, evaluation quality, and clear reporting of progress. Alex sets the ambition, constraints, and resource budget.

Hosted execution through GPT Work or an equivalent system is the intended direction. The design does not assume agents will run on Alex's Mac. The execution platform is a later choice, based on the interfaces and capabilities the learning loop requires.

The immediate deliverable is this design. Implementation, launching workers, spending compute, and submitting competition entries are separate steps requiring an agreed scope.

### Meaning of learning

Here, learning means accumulating tested improvements to bot code and strategy, together with durable evidence about what worked, what failed, and why. It does not require training a neural network or fine-tuning the coding agents. Those could be considered separately if useful.

## The failure this system must prevent

In Alex's previous attempt, the coding agent proposed plausible-sounding improvements without adequately understanding what was happening in the game. It could change code, inspect an aggregate statistic, and construct a story about success or failure that the match itself did not support.

An outcome measure can be noisy, miscomputed, or insensitive to the intended behavior. Even a real improvement in win rate does not establish that the agent's explanation is correct. A bot may win for a different reason, exploit a narrow opponent weakness, or improve on one map while regressing elsewhere.

Replay analysis therefore belongs inside the learning loop. It is not an optional explanation added after selecting a winner. The agent needs access to specific turns, units, events, and spatial relationships, alongside information about what its bot could actually observe and decide at the time.

## The learning loop

The following sequence is the proposed operating form of the agreed replay-centered approach.

### 1 Establish a reproducible baseline

Preserve the baseline code revision and a match manifest containing:

- Engine and rules version.
- Map, sides, opponent revision, and random seeds where supported.
- Build, execution, and resource configuration.
- Match outcome, replay, logs, and available decision telemetry.

Record anything that cannot be reproduced exactly. Keep the baseline immutable for the duration of an experiment so later comparisons refer to a known bot.

### 2 Inspect a match and identify an opportunity

Inspect the replay in enough detail to identify a specific failure or opportunity. Cite the match, turn range, units, and events that support it.

Separate three kinds of statement:

- **Observed fact:** What the replay or trace directly shows.
- **Inferred cause:** An explanation consistent with those observations.
- **Unknown:** Information the available artifacts do not establish.

Do not diagnose a decision using information the bot could not have known. Distinguish full game state from each unit's available observations, received communications, and inferred knowledge.

### 3 Write a hypothesis before changing code

Every candidate change starts with a short experiment proposal:

- The observed failure or opportunity and its evidence.
- The suspected mechanism behind it.
- The proposed code change.
- The observable behavior expected to change.
- The expected competitive benefit.
- Evidence that would disconfirm the hypothesis.
- The comparison and evaluation plan.

For example, a hypothetical diagnosis might be: units arrive at an engagement separately and are defeated before reinforcements arrive. A proposed coordination change should reduce the gap between arrivals. The first check is whether that gap actually shrinks; the separate competitive question is whether the resulting behavior improves outcomes without unacceptable delays elsewhere. This is an illustration, not a finding about an existing Battlecode bot.

### 4 Implement one bounded candidate

Assign a narrow change to a coding-agent worker in an isolated candidate revision. Give it the hypothesis, relevant evidence, constraints, and acceptance criteria. Preserve a traceable diff against the baseline.

Avoid combining independent strategy changes in one experiment. If a combined change is necessary, record the coupling and the limits it places on interpreting the result.

### 5 Run checks and a controlled comparison

Run rules-compliance, build, and smoke checks before expensive evaluation. Then compare the baseline and candidate on matched scenarios, controlling maps, sides, opponents, seeds where supported, and execution configuration.

Preserve failures and incomplete runs. Distinguish build errors, runner failures, timeouts, and legitimate game losses rather than silently mixing them into a single score. Validate outcome extraction against authoritative match results when implementing the evaluator.

### 6 Verify the predicted behavior

Inspect the candidate replay and decision trace at the relevant moments. Determine whether the predicted behavioral change occurred and whether the evidence supports the proposed explanation.

If the behavior did not change as predicted, investigate the implementation, observations, instrumentation, or hypothesis. Do not rewrite the original prediction after seeing the result. Any new explanation becomes a new hypothesis with its own test.

### 7 Evaluate competitive usefulness

Separately assess whether the candidate improves competitive performance across varied maps, sides, seeds where available, and opponent styles. Look for regressions, resource costs, and sensitivity to the test set.

Report the amount of evidence and uncertainty. Keep holdout evaluations separate from the scenarios used to develop changes where practical. Repeatedly tuning to the same opponents or maps can overfit the evaluation set.

No fixed promotion sample size or target win rate has been agreed. These depend on the competition, variability, evaluation cost, and Alex's resource constraints.

### 8 Decide and preserve the lesson

Classify the experiment as promoted, rejected, or inconclusive. Record the evidence and rationale, preserve the artifacts, and identify the next question. Failed and inconclusive experiments belong in the record alongside winners.

A promoted candidate becomes a new named baseline. Keeping previous baselines makes regression checks and rollback possible.

## Two separate evaluation gates

1. **Behavioral gate:** Did the intended mechanism occur, and what evidence shows it?
2. **Competitive gate:** Did that behavior improve performance sufficiently and reliably, accounting for costs and regressions?

Passing the first does not imply passing the second. An outcome improvement without the predicted mechanism does not validate the hypothesis. Treat it as an unexplained result to investigate rather than proof that the proposed strategy worked.

Behavioral evidence is not complete causal proof either. Matched comparisons, repeated tests, and targeted follow-up experiments strengthen the explanation. When evidence remains insufficient, the appropriate decision is inconclusive.

## Proposed architecture

These are logical responsibilities. They need not be separate processes, services, or agents, and they do not commit the project to specific products.

### Coordinator

dot maintains the active baseline, prioritizes hypotheses, assigns bounded experiments, checks evidence quality, and owns integration decisions within the agreed scope. It reports progress in terms Alex can inspect: the question tested, observed behavior, outcome, uncertainty, and next step.

### Coding-agent workers

Workers inspect evidence, propose hypotheses, implement isolated changes, and return reproducible results. Their deliverables include code revisions and evidence references, not unsupported claims that a strategy is better.

### Hosted runner and competition adapter

A runner builds bots, executes matches, records configuration, and collects artifacts. A competition-specific adapter handles the actual engine, rules, replay format, and result conventions. These interfaces must be established from the selected competition's official materials.

### Replay and state inspection

A replay inspection interface should expose structured state and events, supplemented by visual or spatial rendering where useful. Candidate operations include:

- Open a match and inspect its manifest and result.
- Seek to or step through a turn.
- Inspect a unit and its history.
- Query events or units in a spatial area and time range.
- Compare baseline and candidate behavior around a relevant event.
- Retrieve the evidence supporting a claimed observation.

Comparison must account for divergence: after a change, units or events may no longer align one-to-one at the same turn. The tool should make comparison assumptions explicit rather than implying exact correspondence.

Validate replay parsing and event fidelity against the official replay format and client during implementation. Missing or ambiguous data must be labeled, not reconstructed as fact.

### Decision telemetry

Ordinary replay data may show actions without showing why the bot selected them. Where legal and practical, instrument the bot to record relevant observed inputs, chosen action, target, policy branch or reason, errors, and resource constraints.

Link telemetry to the match, turn, unit, and code revision. Preserve the distinction between contemporaneous bot telemetry and an analyst's later interpretation. Assess instrumentation overhead and competition restrictions before relying on it.

### Experiment and evidence store

Store manifests, immutable revisions, hypotheses, replays, telemetry, evaluation results, and decisions with stable identifiers. Each conclusion should link to the artifacts that justify it. Durable records allow work to pause and resume without losing the reasoning behind earlier decisions.

### Evaluator and promotion gate

The evaluator checks result integrity, performs controlled comparisons, summarizes uncertainty and regressions, and evaluates the two gates separately. The coordinator owns the final integration decision under criteria agreed with Alex.

## Experiment record

Each experiment should contain:

- Experiment ID and parent baseline.
- Original hypothesis and evidence references.
- Candidate revision and execution configuration.
- Opponents, maps, sides, seeds, and scenario-selection rationale.
- Predicted behavioral change and observed result.
- Competitive outcome measures and uncertainty.
- Errors, costs, regressions, and missing evidence.
- Decision and rationale.
- Replay, telemetry, log, and build artifact references.
- Lessons and the next question to investigate.

Retain the original hypothesis when adding later interpretation. A concise summary should make the record usable in voice conversation, while detailed artifacts support inspection.

## Coordination and operating constraints

- Use small tasks with clear completion and acceptance criteria.
- Keep candidates isolated and designate one accountable integration owner.
- Prevent simultaneous changes from silently altering the comparison baseline.
- Require evidence references for worker conclusions.
- Agree time, compute, concurrency, and spending limits before execution.
- Preserve enough state to resume an interrupted experiment safely.
- Escalate missing evidence and uncertain results rather than filling gaps with a plausible narrative.

## Proposed initial implementation sequence

1. Choose the competition edition and obtain its official engine, rules, submission requirements, and replay specification.
2. Identify usable prior code and produce one reproducible baseline match.
3. Implement and validate replay inspection, including the distinction between full state and bot-visible information.
4. Demonstrate one detailed diagnosis grounded in cited match events; identify any missing decision telemetry.
5. Add hypothesis records and run one controlled candidate comparison through both evaluation gates.
6. Verify the saved artifacts are sufficient to reproduce and explain the decision.
7. Only then scale to concurrent workers and a broader evaluation pool.

The first milestone is one trustworthy end-to-end experiment, not a large volume of generated code.

## Open decisions

- Which Battlecode edition and competition rules are the target?
- What existing repository, bot, replays, or tooling can be reused from the previous attempt?
- Which hosted platform supports the required launch, execution, artifact, and monitoring interfaces?
- What does the official replay contain, and what must be captured separately?
- What runtime and instrumentation limits apply?
- What compute budget, time horizon, and concurrency are acceptable?
- Which opponents and scenarios form the development and holdout evaluation pools?
- What evidence is sufficient for promotion, and what regressions are unacceptable?

These questions guide the next design pass. They do not prevent adopting the core requirement now: improvements must be grounded in an accurate understanding of actual match behavior.
