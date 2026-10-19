# BC23 lecture-opponent diagnostic: results and direct code review

**Bottom line:** the fresh Sol/high competitor did a strong job of bounded
experimental reasoning and honest reporting. Its code was a competent, compact
starting point with real unresolved state-handling defects. The useful result is
its discovery → implementation → evidence → falsifiable change → counterevidence
workflow, not its wins against an educational opponent.

This is implementation/evaluation evidence, separate from the approved full
experiment plan. It does not restart model selection or establish tournament
strength. [Full code review](experiments/bcenv/runs/BCENV-002/code-review.md),
[exact initial source](experiments/bcenv/runs/BCENV-002/candidate-baseline.java),
[exact selected source](experiments/bcenv/runs/BCENV-002/candidate-standoff.java),
[competitor report](experiments/bcenv/runs/BCENV-002/competitor-report.md), and
[complete evidence archive](experiments/bcenv/runs/BCENV-002/evidence.tar.gz)
are retained together. The archive includes source/build records, all twelve
replays, raw queries, logs, opponent license/provenance and frozen instructions;
it excludes the separately pinned Nix closure and authentication material.

## What changed, and what actually happened

The environment replaced its mandatory inert-fixture evaluation with discovery
and integration of the authentic official
[BC23 lectureplayer](https://github.com/battlecode/battlecode23-lectureplayer/tree/57063ad07b2311c21c99ba7be100a55fcdb3de6b),
commit 57063ad07b2311c21c99ba7be100a55fcdb3de6b (2023-01-20 UTC). Its six Java files
and AGPL-3.0 LICENSE are hash-pinned and kept separate from GPL tooling and the
competitor's own source. This is the final official lecture revision, not the
older three-file version in the user's repository and not an arbitrary bot.

The agent received a source-only offline catalog, no compiled opponent or candidate,
and no strategy solution. It located the season-correct entry, checked archive
and individual file/license hashes, retrieved a separate working copy, and built
and passed the official verifier itself. It then wrote its own 191-line Java bot.
The catalog was chosen to keep the experiment frozen, credential-free and
network-isolated while measuring source discovery/integration. Live-web access
was not established as impossible; this deliberately does **not** demonstrate
unaided online discovery or independent authentication beyond the trusted mirror.

Launch: 2026-10-19 21:14:18 UTC; completion observed 21:21:10 UTC, about seven
minutes. Requested native model gpt-6.1-sol, reasoning high, no inherited history.
The exact message, workspace binding and hashes are in
[launch metadata](experiments/bcenv/runs/BCENV-002/launch.json). No mid-run coaching,
observer diagnosis or candidate edits were supplied. One attempt; eight competitor
games, four subsequent observer games; no build/game/runtime failure or retry.
Token usage and monetary cost were unavailable and are not estimated.

The previously absent local runtime was recovered through locked Nix inputs.
Python, replay parser/query, fixture-game and prompt-tooling checks all passed.
The frozen runtime package is recorded separately from the new copied
runbooks/catalog/kickoff; the latter are release-hashed, not misrepresented as
part of the old runtime package hash. Agent-wide isolation was behavioral;
runtime invocations used a credential-free namespace/chroot with no host binds.

## Reasoning and experiment quality

The [initial plan](experiments/bcenv/runs/BCENV-002/initial-plan.md) correctly checked
HQ resource separation, indestructibility, carrying/delivery, anchors, shared-memory
limits, and action/movement independence. The implementation has role-sized
methods, guarded mutating actions and unconditional yielding. Its “island majority”
shorthand was imprecise (the actual threshold is 75%), although no wrong threshold
was hardcoded. API guards do not prove useful state progression.

After four baseline games on DefaultMap/SmallElements in both side positions,
the agent queried fixed round ranges rather than guessing from scores. It found
close launcher co-presence and preregistered a genuinely behavioral test:
change only movement against an already in-range enemy launcher to prefer
squared distance 13; reduce the pooled close-encounter fraction by at least 25%,
improve at least two eligible paired conditions, retain an encounter floor and
80% of baseline attack events, and keep all four games successful. It fixed the
first 150 rounds before retesting and made one narrow source diff.

Independent recomputation of every consumed raw query found:

- Development close/eligible launcher observations: 50/114 (43.86%) → 30/107
  (28.04%), a 36.07% relative reduction.
- All three baseline-eligible paired conditions improved; the fourth had no
  qualifying encounters and was correctly treated as uninformative.
- Attack events: 339 → 342; the encounter and attack floors passed.
- Both versions won their four games. There is no measured win-rate improvement.

These are global, survivor-position geometry measurements, not visibility,
intended moves, damage or independent samples. The official engine
[records every surviving robot's end-round position](https://github.com/battlecode/battlecode23/blob/5d142a87579af22c2c04ce046a3cbd448dc1869e/engine/src/main/battlecode/world/GameWorld.java#L710),
including stationary robots. The analysis used positions correctly rather than
interpreting the row count as movement. Population, deaths and changed trajectories
can affect the denominator; floors mitigate but do not remove that confound.

The strongest reporting signal was its counterexample: launcher 10057 in the
paired SmallElements/A replays died in round 105 in both versions, despite slightly
larger separation in the variant. The agent explicitly refused to turn its local
metric success into a universal survival story. It also preserved the four-round
slowdown on DefaultMap/B and unchanged SmallElements finish times.

The [preregistration](experiments/bcenv/runs/BCENV-002/competitor-preregistration.md)
and change were observed within one two-second polling interval. Files and visible
command sequence support their ordering, but this is not independently timestamped
append-only proof of the within-batch order. The observer protocol itself was
committed before launch at bcenv 3b648e2b2f40e5fcd826b89083bfb361f191bae6.

## Holdout: smaller transfer, despite unchanged scores

After selection was frozen, the observer ran baseline and selected artifacts
against the same opponent on the undisclosed Rectangle map, both sides. The
competitor did not receive the map assignment or results before completion.

[Holdout measurements](experiments/bcenv/runs/BCENV-002/holdout-analysis.json):
close exposure 47/100 (47.0%) → 45/106 (42.45%), only a 9.67% relative reduction.
Both side-specific fractions improved slightly and attacks rose 100 → 105,
but the effect would not meet the development 25% threshold. The original test
passed; this separate map shows limited transfer, not a retrospective change of
its acceptance rule. Each version won in exactly 221 rounds as A and 206 as B.
Those identical scores conceal the more informative behavioral distinction.

## Code quality: good starting point, meaningful defects

Both complete versions (191 and 208 lines), the exact diff, analysis script and
final package were independently reviewed. No demonstrated illegal API call or
inevitable exception was found. The compact single-class structure is reasonable,
but compressed control flow and magic numbers obscure invariants. Full findings
and source line references are in the linked code review.

Four consequential issues remain:

1. **Carrier replacement fails after attrition.** The HQ counts lifetime carrier
   production, not its live workforce; after eight builds it never replaces dead
   carriers. The agent recognized this in its final report.
2. **A distant upgraded well can strand a carrier at weight 39.** The code requests
   collect(-1) and returns only at weight 40. The actual engine replaces -1 with
   the well's rate; an upgraded rate-3 collection cannot fit at 39, so repeated
   attempts fail and the carrier neither gathers nor returns. This was missed
   in the agent's self-review. Neither player upgrades wells here, so this is a
   verified source-level generalization defect, not a claimed replay-observed stall.
3. **Standoff scores staying and moving inconsistently.** Moves include HQ danger,
   while the stay-put score does not. At desired distance 13, staying scores zero
   even under HQ fire and can beat a safer legal retreat. The agent acknowledged
   incomplete stay-hazard handling; its effect was not isolated in these games.
4. **Remote discoveries are not reliably shared later.** Failed out-of-range writes
   have no queue; remembered wells/islands are not reliably published on returning
   to signal range. This is a coordination limitation, not a permission violation.

Additional ceilings include shallow greedy navigation, one-enemy combat scoring,
underused carrier cooldown capacity, sticky well assumptions and unbounded anchor
role diversion. Compiler/verifier success and complete games do not resolve these.
Robot stdout was disabled, so no exception-free execution claim is justified.

The opponent really was active: complete first-50-round queries show it spawning
6–9 units, collecting resources and placing 1–2 anchors in each baseline condition.
It is still a flawed educational bot: its communication has index/mask bugs and
its launcher production waits for a large mana stockpile. It was not repaired or
replaced. Consequently, beating it cannot establish broad strength.

## Assessment and decision

- Discovery/integration: demonstrated within the disclosed offline boundary.
- Rules comprehension: partial-to-good; sound core API understanding, but missed a
  consequential capacity/progress edge case.
- Experiment design and replay interpretation: demonstrated for this bounded
  geometric endpoint, with important denominator/provenance limits disclosed.
- Code quality: competent initial implementation, not robust competition code.
- Honest selection/reporting: demonstrated, including negative evidence.

Keep the active-opponent environment as a useful diagnostic baseline. This single
run does not causally establish that the environment intervention improved LLM
quality over the old environment, nor does it reopen the prior model ranking.
A valuable next question is whether a generic correctness-testing requirement
makes a fresh agent find state-progress edge cases before declaring its bot ready;
that would be a separate preregistered iteration, not silently added to this run.

[Artifact audit](experiments/bcenv/runs/BCENV-002/audit.json): zero frozen-input,
source/binary, replay/summary or selected-package mismatches across twelve games.
The source ZIP is exactly the selected verified Java source, with no opponent code.
The original trial and all superseded artifacts remain preserved.

### Process status and deviations

bcenv query PR5 remains an unmerged dependency. Planner PR10 was externally merged
at 21:08:00 UTC (4d4c46a546437cd3ee26299541e04e5decc9660b), discovered during this
run; the initial handoff/preregistration had stale status. No merge was performed
by this task. The new ledger records are retrospective transcription of the
pre-launch protocol and completed run, with actual recording times, not a claim
that the ledger existed before launch. BCENV-001 remains a separate unrun proposal.
