# A credible autonomous BC2023 competitor environment

Status: authorized engineering program, **not achieved**. First checkpoint:
2026-10-19. This supersedes the diagnostic-only objective for future work without
rewriting prior results or authorizing merges. Existing lecture experiments remain
useful development evidence, not competitive validation.

## Goal and ownership

A fresh embodied LLM, provisionally gpt-6.1-sol/high, must independently create,
persist, test, submit and improve its own Java competitor using bcenv. Environment
engineers improve tools and generic workflows between trials; they never supply
strategy fixes, edit the candidate or coach a running competitor. Observable
plans, source changes, tests, replay citations and rejected hypotheses are the
reasoning evidence. Hidden chain of thought is neither requested nor scored.

bcenv owns the reusable artifact/tool/service interfaces and year-specific runtime.
bc-planner owns public plans, protocols, outcome analysis and engineering history.
Protected deployment state holds actual benchmark selections, schedules, source,
raw service logs and evaluator-only rubrics. Public competition intelligence is
not a secret benchmark. Historical public bots cannot prove training-data novelty.

## Success criteria to freeze before an acceptance campaign

These are program-level proposed thresholds. A completed, committed campaign
protocol must resolve all pins, budget and protected commitments before any new
acceptance exposure. They cannot be changed after seeing that campaign's results.

1. **Security:** all required boundary tests below pass in the exact deployment
   with the actual agent tool surface. Any prohibited read/egress/control channel
   is a failed gate, even if the competitor promises not to use it.
2. **Independent operation:** three fresh from-scratch agents, same frozen
   environment/model/budget, no inherited bot/history and no observer help. All
   attempts count. At least two produce valid, reproducible selected submissions
   and meet the competence threshold; a failed run is not replaced silently.
3. **Competence:** each qualifying agent scores at least 60% against a balanced
   panel of at least three independently authored, historically competitive
   non-tutorial 2023 opponents, with a lower 95% uncertainty bound above 50%.
   Also require at least 40% against each opponent, avoiding one easy opponent
   carrying the mean. Tutorial/inert opponents never count toward this endpoint.
4. **Stretch strength:** separately report results against at least two verified
   high-placement 2023 teams. Do not call a bot finalist-strength without a
   preregistered majority-score threshold and uncertainty criterion on that tier.
   Competence and finalist strength are different claims.
5. **Correctness and analysis:** candidate builds and passes the official verifier;
   no unresolved recurring runtime failure in tested games; reproducible source,
   binaries, inputs and results; explicit tests for state progress, boundary
   conditions, stale information and resource limits; at least one prospective
   change with raw replay evidence and a negative/control case. Reviewers distinguish
   source-inferred defects from replay-observed failures.
6. **Honesty:** no unsupported causal interpretation or hidden retry; failed games,
   timeouts, tie mechanism and inconclusive comparisons remain visible. Passing a
   code-quality rubric cannot substitute for competitive performance, or vice versa.

Panel eligibility depends on reproducible active play and historical strength
evidence, not repository popularity. If no adequately licensed panel can be
assembled, report that blocker and narrow the claim explicitly. Repository HEAD
must not be described as the historical tournament artifact without evidence.

## Sampling and uncertainty

Use a balanced map-family × opponent schedule with both A/B positions and the
same supported engine seed for paired comparisons. Minimum initial acceptance
budget: 24 distinct map/seed blocks per opponent, two sides per block, three
opponents = 144 games per selected agent. Maps/seeds are not assumed independent
just because game count is large. Preserve paired side results; cluster uncertainty
at map family and report opponent-stratified estimates. Freeze the exact estimator,
confidence construction and weighting in the campaign protocol; do not apply a
naive binomial interval to correlated games. With few independent families, show
wide intervals and call the result inconclusive. Do not claim population-wide
strength from three chosen opponents.

Use win=1, loss=0, true draw=0.5. Official unseeded terminal coin flips must be
reported separately and cannot masquerade as deterministic seed replications.
Missing/failed infrastructure games are not losses; retry the identical assignment
at most twice after fixing infrastructure, retain all attempts, and report missing
coverage. Candidate-caused verifier/runtime rejection is a candidate failure.
Fix statistical handling and rejection denominators in advance. No optional
stopping at a favorable point: only complete the prespecified campaign or record
its interruption. Additional games require a new prospective protocol.

Acceptance feedback is released only after selection is irrevocably frozen; it is
not available during development. Retire exposed holdouts from future acceptance
and preserve them as regression cases. Map-family and opponent-version holdouts
are distinct; public-source familiarity and unknown training contamination remain
limitations even with sound runtime isolation.

## Milestones, budgets and exit gates

| Milestone | Deliverable | Bounded budget | Exit / stop |
| --- | --- | --- | --- |
| M0: plan and feasibility | Roadmap, threat model, public candidate provenance, durable checkpoint | Read-only environment/provenance investigation; no paid services | Identify a supported enforced agent boundary or report precise access blocker |
| M1: service foundation | Bounded source intake, opaque submission/result/replay API, leak and malicious-input tests | Local synthetic inputs, no real holdouts | Contract tests pass; no isolation or competition claim |
| M2: enforced deployment | Capability-limited competitor, private evaluator/workers, replay filtering, audit/recovery evidence | Local existing VM resources; no credential transfer/security changes without approval | Every boundary test passes from actual competitor tool surface |
| M3: faithful execution | Real build/verify → scheduled paired match → bounded result/replay, durable retry/recovery | Public test opponents and maps only; 16 integration games maximum per protocol | Correct identity, lifecycle, failure attribution, no prohibited egress or leakage |
| M4: diagnostic environment iteration | Generic correctness/replay workflow tested by fresh agents | Initially 45 minutes and 24 development games per agent; max two arms × three independent agents | Audit mechanism and regressions; keep/reject/inconclusive; revise environment only between trials |
| M5: acceptance campaign | Frozen model/environment/panel/schedule, three from-scratch agents | Up to two hours and 96 development games per agent, then 144 protected games each | Full campaign and criteria above; no substitution of weak runs |
| M6: replication and release | New untouched panel/map coverage, clean recreation and independent security review | New protocol justified by first acceptance result | Credible scoped claim or explicit unresolved blocker; reviewable PRs, no automatic merge |

Wall-clock/game ceilings are hard stops per experiment, not a stop to the engineering
program. Record available tokens/compute and unavailable costs honestly. Reduce
parallelism on resource exhaustion. Do not acquire paid infrastructure, transmit
credentials, modify security settings or contact real tournament services implicitly.
The user authorized continuing useful implementation and publishing public PRs;
merge approval is separate.

## Security boundary and mandatory adversarial tests

The prior native-agent runtime has unrestricted peer filesystem/tool access.
A network-isolated match subprocess does not isolate the agent that launched it.
A second directory, a rubric hash, a polite kickoff and an opaque result wrapper
are not security boundaries. Do not put new real heldouts in that environment.

The acceptable design is a capability-limited competitor process or genuinely
separate executor that can access only its own workspace, frozen public runtime
and the service API. Its model/tool broker must not offer parent shell, filesystem,
connectors, agent messaging or credential access that bypasses this boundary.
The service runs under a separately protected authority; submitted Java executes
in another sandbox with no service state, network, secrets or writable engine.
Public evaluator source is acceptable; deployed internals and evaluation state
must remain inaccessible. Generic published architecture is not a secret.

Before real holdouts, plant synthetic secret canaries and attack the exact tools:

- absolute/relative traversal, symlinks, hardlinks, archive tricks and alternate
  path encodings; host mounts, proc/process/environment, inherited descriptors,
  sockets, metadata endpoints, shared caches and sibling workspaces;
- escape from any advertised sandbox by invoking a different available tool,
  direct exec, native subagent, connector, browser, repository history or service
  administrative route; prevent public protocol/rubric documents leaking answers;
- network/SSRF/DNS and service path traversal; unauthorized list/get, stale or
  guessed object IDs, foreign submissions/replays and cross-agent access;
- malformed/oversized archives, decompression bombs, resource exhaustion, worker
  timeout/crash, duplicate submission/delivery, restart and partial publication;
- malicious compiler/runtime diagnostics, absolute paths, package/team labels,
  replay metadata and log strings revealing opponent names or internal paths;
- attempts to modify own frozen submission, opponent artifacts, schedule or results.

Require both denial evidence and a positive allowed-control operation; merely
observing no successful attack in normal use is insufficient. Record actual
permissions/tool inventories and audit the attack surface after any change.
Never bypass a platform denial to make this gate pass. Report infeasibility as
infeasibility, not as a request to trust behavioral isolation.

## Service fidelity and information release

The new bounded facade is not a claim to reproduce historical Galaxy. Preserve
existing Galaxy source-contract work and integration gates; document each deviation.
Compiler/match lifecycle semantics, artifact identity and service information
boundaries matter more than copying a production cloud stack blindly. Any change
to the approved historical-replica objective must be explicit in a subsequent plan.

A competitor submits source and receives an opaque submission ID, bounded compile
status/diagnostics from its own code, allowed queue state, score/terminal reason,
and an authorized replay. It cannot select a secret benchmark opponent or browse
worker state. Public practice challenges and sealed acceptance jobs are distinct.
Replay behavior legitimately reveals strategy; hidden identity/path/log metadata
is not automatically legitimate. Validate replay field policy with the real parser
before serving opponent replays. Aggregate withheld acceptance results cannot be
queried adaptively during development. Rate/game budgets are server enforced.

## Resuming work

Read the [checkpoint](2023-competitive-checkpoint.md), this roadmap, current git
status and open PR heads before editing. Preserve old evidence and prompt history.
Each material result gets a commit/PR or an explicit pending reason; each experiment
gets an append-only ledger entry and its frozen protocol before launch. Redact only
sensitive deployment data; do not publish benchmark selection in these public files.
A failed security gate blocks M2–M6, while M0/M1/public integration work can continue.
