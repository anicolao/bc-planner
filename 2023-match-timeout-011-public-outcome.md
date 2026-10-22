# BCENV-011: public phases completed under the revised match cap

Recorded 2026-10-22. The prospective [011 protocol](2023-match-timeout-feasibility-011.md) is unchanged. This report contains public development and blind review evidence only, not independent evaluator outcomes. **The competitive goal remains unmet.**

## Completed public development, not a competence estimate

The fresh fork-none requested Sol/high competitor submitted eight versions and completed all 64 training games plus 16 locked-finalist validation games. There were no service-game failures, retries or substitutions. Both finalists trained at 5/8. Provisional V7 validated at 3/8; V8 validated at 4/8 and became the final selection under the pre-recorded selection criterion. Public validation therefore changed the provisional choice in this run. These adaptive public results are not an independent performance estimate or a causal comparison with earlier agents.

The source was locked before validation; both original-to-validation source, build and package inventories match exactly. Selection was recorded about 169 seconds before the hard deadline. The final workspace matches the selected original artifact byte-for-byte. A few hash-only observations also match after lock, but do not constitute a continuous write trace.

Native completion was verified at 16:07:52 UTC. The service was explicitly stopped at 16:07:55, before its 16:09:44.047616 deadline, with zero pending requests. The terminal tool receipt returned exit1 and no graceful marker; the exit-code cause is unestablished. All 160 engine/initial-summary children had already succeeded and been reaped before the deadline. This is operational stop evidence, not a claim of graceful shutdown or global process-namespace inspection.

## Observable reasoning and code quality

Independent review verified 4,898 frozen files, all 57 fixed inputs, the 196-event receipt chain, eight prospective source-bound notes, 24 replay replies and 14 prior replay references. Eighteen queries used own-team diagnostics and six used action projection. These counts establish recorded use, not that the channel caused better play or supplied complete state.

Six relevant final actual-class test mains independently passed on a copy of the frozen build. A disclosed abandoned-policy main still failed its assertion, as expected from the report. Across development, 34 retained test receipts include 28 successful executions and six failures; local compile/test failures were preserved rather than erased. Explicit assertions and observed state progress are meaningful, but simplified proxy controllers and selected cases are not complete game-engine coverage or proof of bot correctness. Passing a policy assertion does not establish that the policy wins.

The [fixed blind review](experiments/bcenv/runs/BCENV-011/blind-source-process-review.md), fixed before private scores, supports bounded provenance, prospective hypotheses, replay grounding and locked selection. Testing breadth, isolated causal experimentation, code correctness and boundary assurance remain partial. The separately reproduced old evaluation runtime matches the selected source, classes, binary inventory and source ZIP exactly; no bot change was introduced by that rebuild.

## Limits and next gate

The 300-second public run allowance remains clipped by the same 45-minute global deadline; other child subprocess limits remain 120 seconds. One completed engine took 122.661 seconds (the observed range was 2.786–122.661), using allowance beyond the former 120-second cap. Completion of this run does not prove universal timeout sufficiency or retroactively repair the incomplete 010 trial. This is a single fresh-agent feasibility observation, not a controlled estimate of benefit from the cap change.

The competitor is stopped and must not be resumed. Independent evaluation remains separate under its preregistered observed-regression protocol; no result from it is included here. Cooperative workspace restrictions, unchanged fixed-input hashes and service receipts do not establish hard filesystem isolation or an exhaustive native-access audit. Earlier local raw evidence lost during VM refresh remains an archival limitation. No merge or private benchmark publication is authorized by this report.

See the [public development summary](experiments/bcenv/runs/BCENV-011/development-summary.json), [freeze](experiments/bcenv/runs/BCENV-011/candidate-freeze.json), [source binding](experiments/bcenv/runs/BCENV-011/selected-source-audit.json) and [selected rebuild](experiments/bcenv/runs/BCENV-011/selected-rebuild-audit.json).
