# BC23 model selection: current environment stage

This separate results note continues [the pilot and code-review history](2023-implementation-notes.md).
It does not revise the approved [2023 experiment plan](2023-experiment-plan.md).
The earlier native pilots, blocked CLI attempts and observer reviews remain
historical evidence, not retrospectively preregistered trials.

**Recommendation:** provisionally use **gpt-6.1-sol / high** for the defined local
BC23 implementation and evidence-grounded learning workflow. Both models passed
the preregistered adequacy standard. The preference is narrow and small-sample;
the exact decision and limitations appear below.

## Environment and process changes

The user asked for a repeatable way to design, evaluate and record environment
changes, then authorized continued iteration until a model recommendation and
adequate performance in the defined environment were supported.

[Process PR #10](https://github.com/anicolao/bc-planner/pull/10), reviewed here at
`c04a66e14277b42d9593677579588f4c453623b7`, introduces a protocol template,
append-only experiment ledger and validation. Its BCENV-001 instruction-only
proposal was **not run**: preflight found the original extractor retained only
32 generic samples, inadequate for arbitrary late-round diagnosis. That is a
preflight design finding, not a failed competitor experiment.

BCENV-002 was a separate prospective engineering check, recorded before editing.
It added a generic bounded replay-query command: explicit replay and round range,
optional robot filter, record bound, raw events and explicit coverage/semantics.
It does not infer strategy, reconstruct bot knowledge, or change competitor code.
Independent official-schema accessors cross-checked 57 records at retained rounds
121, 177 and 299, with the source replay unchanged. Both compressed and decoded
inputs above the 64 MiB limit were rejected. Existing readiness checks and the
new checks passed. This establishes the tested tool contract, not improved model
performance by itself.

The resulting [bcenv tooling PR #5](https://github.com/anicolao/bcenv/pull/5) is
pinned to `4d9813ac022a4be94686cf7d39cdb40edb5eec33`, with
[foundation CI passing](https://github.com/anicolao/bcenv/actions/runs/38977351024).
Its base foundation is `9a2ab53ff3545165dde660923151adf655c27810`, the later
user-authorized merge of [bcenv PR #4](https://github.com/anicolao/bcenv/pull/4).
That merge supersedes the earlier pilot note's historical draft status for PR #4.
Process and tooling PRs are drafts; these results do not authorize their merge.

## Prospective fixed-environment comparison: BCENV-003

BCENV-003 compares explicitly requested native `gpt-6.1-sol` / high against
`gpt-6-astra` / high in the same fixed tool-plus-workflow bundle. The protocol,
exact inputs, resource bounds, rubric and choice rule were frozen before launch.
The environment bundles replay-query access with a generic evidence workflow;
this study does not separately estimate either component's causal effect.
Backend build/version, token use and inference cost were not exposed. The native
harness does not resolve the previously blocked Codex CLI path.

Six fresh no-history sessions used independent repositories, three matched pairs:

| Case | Starting point | Development map | Unseen-map inert check | Active check |
| --- | --- | --- | --- | --- |
| K | Known prior Astra baseline, without its analysis | DefaultMap | Cat | DefaultMap |
| S1 | From scratch | DefaultMap | Forest | DefaultMap |
| S2 | From scratch | ArtistRendition | Frog | ArtistRendition |

K is a known observer-selected continuation and cannot establish the independent
adequacy floor. S1 and S2 are separate from-scratch tasks, not repeated samples
of K. Each observer check uses both sides and frozen selected source. The active
opponent is the unchanged first-pilot selected bot: previously known to the
observer, hidden from competitors. Thus these are unseen-to-competitor transfer
checks, not an untouched researcher dataset or a tournament benchmark.

Each agent had 20 minutes and at most eight sequential development games, plus
four observer holdout games, under a shared 72-attempt/120-agent-minute ceiling.
Pair launch order was counterbalanced across cases. No mid-run strategy coaching
or post-holdout tuning was permitted. General agent read isolation remained
behavioral; runtime commands had the separate credential-free namespace/chroot
boundary. No full clean-room claim follows.

The common candidate objective was both-side inert wins, then the lowest
worst-side winning round, with mean as tie-break. Before editing, agents had to
send prediction/artifact hashes to the observer. This adds independent receipts
to the previous timestamp-only ordering evidence, without claiming a trusted
immutable journal or perfect provider attestation.

## Frozen assessment and decision rules

Four components were scored separately from 0 to 2: causal grounding, experiment
validity, implementation quality and practical result. No posthoc weighted total
was allowed. A correctly falsified causal prediction could earn full learning
credit; practical credit for a fix required retaining it in the selected artifact.
An active loss alone was not a severe code defect, and selected-only active tests
could not establish regression relative to an untested active baseline.

A model had to meet all of these to count as adequate for this scoped workflow:

- Both independent cases: causal = 2, experiment = 2, implementation = 2,
  practical at least 1, with practical = 2 in at least one case
- All four unseen-map inert side checks are genuine objective wins
- No severe evidenced runtime/code defect in active heldouts

K could not rescue a failure of that floor. If both models passed, a relative
preference required never-worse component scores across both independent cases
and at least one strictly better component. Otherwise the rule retained a tie,
except for a separately bounded operational timing rule. These are demanding
small-sample decision criteria, not a confidence interval on model reliability.

## Audited results

Component order below is causal / experiment / implementation / practical.
Assessors received anonymized labels; coding style or self-disclosure can weaken
blinding. Scores are not a weighted total.

| Case | Sol high | Astra high | Decision role |
| --- | --- | --- | --- |
| K | 2 / 2 / 2 / 1 | 2 / 2 / 2 / 2 | Known biased diagnostic, excluded from adequacy/choice |
| S1 | 2 / 2 / 2 / 2 | 2 / 2 / 2 / 1 | Independent scratch case |
| S2 | 2 / 2 / 2 / 2 | 2 / 2 / 2 / 2 | Independent scratch case |

### What improved over aggregate-outcome analysis

- **S1 Sol:** with HQ manufacture unchanged at round 61, the same carrier's
  second pickup moved from 93/94 to 62 in both sides. A source-guarded stock check
  latched a partial-load return; exact resource events showed a 10-unit deposit.
  This distinguished dispatch timing from manufacture timing. The selected
  completion rounds improved from 196/173 to 155/175.
- **S1 Astra:** adjacent spawning produced all six predicted earlier pickups at
  round 2 rather than 3/4/4, yet completion worsened from 121/152 to 147/209.
  Astra restored the baseline. This is grounded falsification and honest
  selection, not a causal-quality failure; it leaves no retained practical fix.
- **S2 Astra:** correcting predicted current occupancy to permit the mover's
  vacated origin reduced a loaded carrier's dwell from 40/40 to 5/40 rounds in
  the round-41–80 interval, with first divergence at 43. Selected completion
  was 125/161. Earlier-anchor variants were rejected when worst-side duration
  worsened.
- **S2 Sol:** cumulative endpoint-visit cost moved a loaded carrier out of a
  repeated loop at round 49 instead of 81. A later retained dispatch change
  moved pickup from 77 to 52 on both sides while manufacture remained at 51;
  exact non-team-delta events through 50 were unchanged. The dispatch wait fell
  from 26 to one round. Selected completion was 126/93. Practical credit is
  tied to the retained preregistered behavioral fix, not aggregate speed alone.

These findings use exact primitive records with source/rules checks. They do not
claim unobserved bot knowledge, intentions, full replay reconstruction or exact
within-round ordering that the query does not expose.

### Frozen selected-source holdouts

All S1/S2 results below are genuine 75%-island-capture wins, not random or
island-count tiebreaks. A/B indicate candidate side.

| Case / condition | Sol A / B rounds | Astra A / B rounds |
| --- | ---: | ---: |
| S1 Forest / inert | 1024 / 559 | 499 / 470 |
| S1 DefaultMap / active | 205 / 240 | 269 / 199 |
| S2 Frog / inert | 142 / 162 | 154 / 190 |
| S2 ArtistRendition / active | 108 / 99 | 157 / 148 |

K's Cat/inert capture wins were Sol 218/210 and Astra 159/153. Both split their
active DefaultMap checks: Sol lost A at 473 and won B at 1379 by capture; Astra
lost A at 588 and won B at 2000 by island-count tiebreak. These are disclosed
known-case outcomes, not an overall strength ranking or independent adequacy
samples. The mixed relative holdout durations also do not support a universal
speed advantage.

## Integrity, resource accounting and deviations

All six frozen-input/source/binary/build-lineage/selected-ZIP/development-replay
audits passed, as did all 24 observer-game lineage audits. Assessors inspected
selected Java and primitive evidence; no severe tested-path defect was
established. Disabled robot stdout still prevents an exception-free guarantee.

There were 34 executed development games plus 24 observer games: **58 games**.
Each S2 agent additionally requested one run using its initial unverified build.
The runner rejected both before engine launch, producing no game/replay. Counting
those conservatively yields **60 run requests**, below the shared 72-attempt
ceiling. Each S2 agent executed eight development plus four observer games, with
13 requests including its rejection. This distinction is a recorded deviation,
not silently omitted failures or retroactive success. Both initial builds used
forbidden reflection only in exception diagnostic text; constant-string repairs
and failed artifacts were retained. One observer-directory preparation failure
launched zero builds/games and was retried identically. There were no replacement
agents or selective outcome reruns.

The audit interprets the per-slot cap as eight **executed development games**,
while charging pre-engine rejections against the explicitly attempt-counted
shared ceiling. If every preflight rejection were instead counted under an
unstated eight-request slot cap, each S2 arm would exceed it. This interpretation
caveat remains visible; the frozen cap was not rewritten and no failure was
discarded or assigned an invented score penalty.

Combined native request-to-terminal time was 39m16s, below the 120-agent-minute
ceiling. Per-case seconds, Sol/Astra: K 275/382; S1 301/381; S2 525/492.
Timings are inconsistent across models and scheduling-confounded. No speed,
token-cost or charge advantage is established.

## Decision

The independent final rule audit confirms **both models meet the frozen absolute
adequacy floor** for this defined local workflow. Use **gpt-6.1-sol with high
reasoning as the provisional default**. This is a weak, small-sample preference,
not a broad capability gap.

Sol is equal on seven of the eight independent-case component comparisons and
better on S1 Practical, with none worse. It retained a validated practical
improvement in both scratch cases; Astra retained one in S2 and correctly
restored the baseline after a harmful S1 candidate. Astra's honest negative
result still receives full causal and experiment credit. This exact distinction
satisfies the frozen Pareto rule; K contributes nothing to that choice. Another
small sample could reverse the preference.

S2 Sol's practical credit is for retained measured behavioral fixes, not merely
its one-round worst-side improvement. Its later strict speed predictions failed
and remain failures. The separate timing preference rule was not met.

The preregistered stopping criterion is met. The neither-adequate environment-
correction branch is not triggered, and unused budget is not a reason to run
undeclared trials in search of a stronger winner. This recommendation does not
merge the tooling/process drafts or change account/model settings.

## Claim limits

Two independent task pairs, one fixed active opponent, deterministic side/map
checks and no repeated fresh-agent samples support only a narrow recommendation.
They are not independent Bernoulli reliability trials and do not justify a
numerical reliability confidence interval. Heldouts were unseen by competitors,
not an untouched researcher dataset. The study does not establish combat-rich
strategy quality, other-season performance, behavior after model updates, full
replica acceptance or hard agent-wide isolation. The earlier pilots' limitations
remain visible; this stage does not retroactively strengthen their claims.


## Evidence retention and provenance

The final independent audit recomputed 762 frozen input-file identities, 25
build records, all 58 development/observer replay and class-copy lineages, and
all six selected ZIP/current-source identities, with zero mismatches. Applying
the fixed candidate objective independently selected the recorded build in every
slot. All 13 archived prediction/selection texts matched their receipts;
11 strategy interventions had independent receipts before observed edits. Initial
construction and restoration receipts are distinguished from new interventions.
These checks do not prove absence of undisclosed access or provide tamper-proof
external timestamps.

BCENV-003's private protocol was committed at
`123d8f3346979ab7bbb5e501fcc81e65fdbc7f81` before its preregistration ledger event
and launches. The retained ledger has 20 validated events; a trusted prior prefix
at `0cb3257` was checked for preservation. Results, deviations and the final
decision were appended without rewriting prior events. The public process
proposal/ledger in PR #10 and this retrospective results narrative are distinct
from that executed private protocol and evidence ledger; neither is presented as
having preregistered the older pilots.

Retained SHA-256 commitments:

- BCENV-002 engineering preregistration: `dd4455c377aca574ace23d9aa5dfd69954f29ca169504c0a1f2c029e7ca6346b`.
- BCENV-003 preregistration: `a005017a53223e682c91f1d27b9935021fd2b8d268119fa9c1b01dfdf472a391`.
- Frozen detailed rubric: `0c96ebc29674f24b64b0e34cad60bb71c8fe6129fb6f630b164674333a978b73`.
- Final outcome summary: `a3de8bc59a5da2b894c84c7397624a3725ca66df7b50a34c0dc4ebee2d584051`.
- Final rule/integrity audit JSON: `4bb15454ac75cfe15d30e6bff5f057e906cb502e01d0c3eb077e39dfbe935e7a`.
- Final rule audit narrative: `56add823f44c96a79914755429b7d310ad99453259a3bc9d5496af3576b102fc`.
- Final execution ledger: `f0af55257d0598209f371b56820d7092d8887cbf68c7460d456829c318256cf0`.

The private evidence archive is versioned at commit
`f6198559d8a97448f8a18e7b6d2e5f2dfa75205a`. These identities are commitments to
retained bytes, not public download links. Candidate source, raw runtime records
and exposure-sensitive artifacts are not published in this PR.
