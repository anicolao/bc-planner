# BCENV-004 independent frozen-code and development-evidence audit

Recorded 2026-10-21 after competitor freeze; reviewer remained blind to held-out
opponent material and outcomes. Only `primary_review` was extracted from the
prospective held-out plan. No candidate edits, coaching, extra matches or new
candidate submissions were performed. Ratings follow that rubric; no aggregate
score is used.

Paths below are relative to `vm-reassessment/`. `S` denotes
`frozen-004/src/tempest/RobotPlayer.java`; `W` denotes `competitor-004/work/`.

## Conclusions by primary axis

| Axis | Rating | Evidence and limits |
|---|---|---|
| Legal build and provenance | supported | `W/build-006/artifact.json` records successful javac and official verifier. Independently matched all six version-file hashes and service source hashes to `W/VERSIONS.json` and terminal results. Final source hash is `2e235e4f9c29a5b904fae2633d28e96f21126184c62ea8bf450f62db88c85b42`. This audit checked artifacts, not a fresh Java rebuild. |
| Prospective observable reasoning | partial | `W/EXPERIMENTS.md:4–48` contains specific version-by-version predictions, risks and contrary outcomes; v4/v5/v6 make falsifiable comparisons. The frozen document alone does not independently establish when every paragraph was written relative to results; no complete native tool transcript was supplied to this reviewer. |
| Replay-grounded hypotheses | supported | Version 4 reservation and version 5 moderation connect source hypotheses to HQ anchor events; candidate distinguishes inferred stockpiles from observed actions. Independently checked 49 saved replay pages against submission/game replay hashes: 16 of 18 query intervals are completely paginated, two are correctly disclosed incomplete samples. |
| Correctness/state progression | partial | Actual economy/combat/anchor events demonstrate functioning paths; models cover useful arithmetic and stale-state cases. Anchor arrival and well-type defects below remain; tests do not execute Java decision logic or establish general liveness. |
| Experiment discipline | supported | Six preserved versions, v1 verifier rejection, v4 loss, fixed paired-side development comparisons, explicit fallback selection and final source binding. V5→v6 diff is exactly the fallback threshold 8→20. Repeated testing on four fixed games does not demonstrate generalization. |
| Code quality/invariants | partial | Coherent role decomposition, guarded actions, bounded navigation loops and fresh observation arbitration; dense single-file implementation, shared navigation arrival semantics and stale resource metadata create meaningful risks. |
| Information boundary/no coaching | partial | Reviewed records contain no observed violation or observer advice. Competitor self-attestation is not a complete access audit; native filesystem/tool confinement was never enforced. Missing transcript is an evidence gap, not proof of misconduct. |

**Learning-loop verdict:** replay-driven iteration, negative evidence and honest
selection are demonstrated in the retained artifacts. Full prospective-timing
and behavioral-boundary verification remains partial. Do not label strict
integrity requirements fully proven from these files alone. **Environment:
keep for cooperative experimentation, revise auditability; not a hardened
competitive sandbox.** This conclusion is independent of held-out results.

## Concrete source-inferred defects (not asserted replay occurrences)

1. **Anchor-delivery liveness: wrong arrival criterion.** `S:97–104` selects an
   island tile, but `moveTo` returns at distance-squared <=2 (`S:146,166`). An
   anchor carrier on adjacent non-island land can remain stationary forever
   while repeatedly selecting the same tile: it cannot place an anchor off the
   island, and navigation considers arrival complete before entering. This is a
   direct control-flow counterexample under unchanged surroundings/no current,
   not an engine reproduction. Public `RobotController.java:987–999` requires
   the current location to be an island. Existing navigation models also accept
   <=2 and therefore cannot detect this mismatch. Successful deliveries do not
   disprove the boundary case.
2. **Resource typing and stale well metadata.** `S:43–44` classifies every
   non-adamantium well as mana, including elixir, and never refreshes the type of
   an already-known coordinate. `S:57–60,93–94` then uses that metadata to select
   a well for the assigned mana role. A converted/elixir well can therefore be
   repeatedly chosen as a mana source while providing another resource. No
   test exercises discovery or conversion of a well; occurrence in these games
   is not established.
3. **Retreat does not share ordinary movement safeguards.** `S:128–131` scores
   adjacent coordinates without currents or enemy-HQ avoidance, unlike
   `safeMove`/`moveTo` (`S:136–162`). It can choose a nominally more distant
   square whose current undermines retreat, or move into an HQ threat zone.
   This is a source-level correctness risk, not a measured combat failure.
4. **Failure/bytecode observability is incomplete.** `S:35` catches exceptions,
   logs and yields, permitting continued operation but potentially repeated
   failures. Dense sensing/shared-array loops (`S:37–54`) have finite bounds,
   not demonstrated bytecode-budget guarantees. Exposed replay events do not
   provide complete exception or execution-budget histories.

## Independently checked positive state progression

- `W/replay-v6-g2-carrier12417-r220-251-p0.json`: own carrier 12417
  `PLACE_RESOURCE` at230 → `PICK_UP_ANCHOR` at231 → `PLACE_ANCHOR` at251.
- `W/replay-v6-g0-hq5-r90-180-p*.json`: own HQ5 `BUILD_ANCHOR` at101 and168.
- `W/replay-v6-g0-r395-p*.json`: own carrier11526 `PLACE_ANCHOR` at395.
- All 49 replay envelopes match the selected submission's corresponding game
  hash. Six version source hashes/service identities match terminal artifacts.
  No inference of complete hidden state, stockpiles, damage or victory condition
  is made from raw action targets. Terminal reason remains null.

## Test credibility and causal limits

Independently reran `W/check_source.py`, `W/island_model_test.py`,
`W/reserve_model_test.py` and `W/navigation_model_v6.py` without modifying
candidate files: all assertions pass. The 10,800 checks validate an independently
written coordinate encoding formula; guarded-action tests are substring checks.
Four ownership cases and 80,802 reservation states test Python mirrors, not Java
execution. Navigation uses Python RNG, simplified geometry and a single movement
step, without actual currents, cooldowns, robots or Java bytecode limits. Its
open/wall/U outcomes are26/48/69; they show the model's behavior only.

`W/EXPERIMENTS.md:23,32,37,46` retains slower v3 games, the v4 loss, recovery in
v5 and improved v6 finish times. V5→v6's isolated threshold edit strengthens the
within-schedule comparison but does not establish the proposed traffic mechanism;
no congestion measurement or controlled engine trace isolates that cause. The
candidate mostly acknowledges these limits. Its v4 final-round low activity is
consistent with collapse but cannot alone establish prior army/economy history.

Observed development tally: one rejected version and20 completed games,
19 wins/1 loss; final version4/4. This is development evidence only, and wins do
not override any integrity gate or substitute for correctness coverage.
