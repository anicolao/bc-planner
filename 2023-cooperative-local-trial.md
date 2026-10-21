# BCENV-004: cooperative local-VM trial

Prospective protocol, October 21, 2026. This is a new experiment, not an
extension or reclassification of the exhausted preflight-001 match budget.
The competitive program remains unfinished.

## Revised scope

Alex asked whether the existing VM can host the service and whether the earlier
isolation requirements were stronger than necessary, then approved proceeding.
This profile tests a cooperative fresh native agent and a trusted local service.
It does not claim malicious-agent containment, per-agent filesystem isolation,
an enforced six-tool model surface, production authentication, aggregate cgroup
quotas, or protected multi-tenant deployment. Earlier hardened gates remain
unchanged for deployments that make those claims; they no longer block this
explicitly narrower experiment.

The VM already answers loopback HTTP, has Python and Java, and runs all 286
PR15 Python tests. Authenticated CLI startup fails with EROFS before inference;
native agents are the supported experimental transport. No credentials are
copied, paid account created, security mask bypassed, or public listener opened.
All acquired dependencies use the existing Nix wrapper and pinned flake.

## Information separation and validity

The fresh competitor receives only a new candidate directory, exported public
rules/API/tool documentation, service client, and frozen kickoff. No inherited
conversation, planner repository, strategy advice, reference bot source, or
evaluation material is passed to it. Native tools can technically read sibling
files; instructions and review are procedural restrictions, not an OS boundary.
The competitor must use the service for opponent matches and feedback and must
not inspect service internals, other workspaces, source catalogs, connectors, or
other agents. Audit observed tool use. A violation invalidates this trial; do
not silently turn it into acceptable evidence.

Only disclosed public development opponents are present during development.
Do not materialize or expose any selected held-out opponent sources, binaries,
schedule, rubric details or results while the competitor is active. Freeze the
selected source ZIP and report, stop the competitor, verify its work is finished,
then perform separate observer-owned evaluation. Holdout feedback never returns
to that competitor. Public historical source may already be in model training;
this experiment establishes no training novelty or hard confidentiality.

## Pins, budgets and gates

- Baseline: bcenv PR15 commit 59242ba9935d777f787596adfc0b2b1efc34650d,
  official public engine 3.0.13, not private finals binaries.
- The local service implementation, runtime closure, exported documentation,
  kickoff, maps and source manifests will be hashed in a launch record before
  the native competitor starts. No launch with unresolved service/runtime pins.
- Requested competitor: gpt-6.1-sol/high, fresh context. Record the tool-reported
  model/effort evidence; requested settings are not independently inferred identity.
- Development opponents: official lectureplayer at
  57063ad07b2311c21c99ba7be100a55fcdb3de6b (tutorial), and Beaver Bois
  USQualifiers at 4892382943da5a8527906467739a64db51ccc50d (non-tutorial).
  Retain upstream AGPL source/license provenance. Neither is a hidden holdout.
  The service exposes Beaver Bois on DefaultMap and Rectangle, both sides per
  submission (four games). Lectureplayer is the pre-launch integration control.
- Pre-launch engineering budget: four new matches maximum, two paired sides
  between the development packages on DefaultMap and Rectangle. Compiler or
  service failures count as attempts; no invisible retry or deadline extension.
  Both packages must compile/verify and produce active complete replay evidence
  before launching the competitor. Failing this gate requires a recorded
  environment correction and a separate prospective integration protocol.
- Competitor budget: one initial run, 45 minutes and at most 24 submitted
  development games total (six submitted source versions × four games), whichever
  is reached first. Rejected builds consume a submission slot, not a played game.
  Serial worker execution;
  each game has the existing 120-second process timeout and 512 MiB JVM heap.
  Source size, response bytes, replay pages and game count are service bounded.
  No claim of aggregate CPU/disk/PID enforcement is made.
- An infrastructure failure stops the run without coaching or modifying its bot.
  Fix the environment, retain evidence, and preregister a fresh run rather than
  continuing a contaminated session. Candidate-caused failure is a result.
- Post-freeze evaluation will have its own private prospective manifest and
  fixed bounded schedule before running any held-out games. This document does
  not assert that one trial satisfies the larger three-agent competence campaign.

## What to assess

Primary evidence is observable plans, source quality, explicit tests, state
progress and boundary-case handling, replay-linked hypotheses, prospective
experiments, and honest treatment of negative results. Do not request hidden
chain of thought or tell the competitor which strategic defects to fix.
Wins and losses against genuine non-tutorial opponents are important secondary
evidence, not a substitute for reasoning/code assessment or replicated strength.

The competitor selects and freezes its submission without observer advice.
Independent review distinguishes source-inferred bugs from replay-observed
failures and causal claims from correlations. Retain all rejected builds,
timeouts, unsuccessful experiments, map/side assignments and exact artifacts.
Report actual native token/currency usage only when available, never invent it.

## Stop and next decision

This bounded run ends with a frozen selected package/report or an explicit
failure. Review the service and learning-loop evidence and decide whether to
keep, revise, or reject this environment. Further trials need new prospective
records, not arbitrary repeat-until-win sampling. Continue the authorized
long-running engineering goal through justified fresh iterations, without
merging PRs or incurring unapproved costs.
