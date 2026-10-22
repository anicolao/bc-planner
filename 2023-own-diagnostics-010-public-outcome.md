# BCENV-010: public development stopped without a selection

Recorded 2026-10-22. The prospective [010 protocol](2023-own-diagnostics-feasibility-010.md) is unchanged.

## Original trial: incomplete, not a bot-performance result

The fresh competitor made six submissions and completed 48 training games. It
locked two immutable finalists before validation. Fourteen validation games
completed; the next engine process reached its 120-second wall cap and was
reaped (exit -9). One reserved cell was never attempted. Thus **63 attempts,
62 completed games, one unscored timeout, no final selected artifact**—not 64
completed games. Both competitor and service stopped at 14:07:30 UTC, before the
original 14:22:24.184 UTC deadline. There was no retry, fallback or private
evaluation, and the private panel remained sealed.

The failed process ran 120.182 seconds; about 990 seconds remained on the global
clock when termination was requested. It produced no replay and failed upstream
of diagnostic projection. This identifies the terminating limit, not why the
engine took that long. A public-opponent exception in its log is not established
as the cause. Raw mixed logs were not exposed to the competitor.

Independent mechanical review verified all 3,922 frozen files, all 57 fixed input
hashes, the 169-event audit chain, and exact source/build/package preservation
between the submitted and locked finalist snapshots. The workspace's later
unsubmitted source was **not** silently substituted. These checks are not a
complete filesystem-access audit or a competence assessment.

## Observable channel use

Eight notes and 24 replay queries were recorded: 18 own-diagnostic queries and
six action queries. Diagnostic replies returned 551 rows, 550 nonempty strings
and one continued page. Later notes referenced ten diagnostic and four action
receipts. This establishes use of the channel—not that the observations were
correctly interpreted, sufficient, or caused better performance. Indicator strings
still require deliberate emission; bytecode counts are not correctness or CPU
measurements. There is no automatic exception-free guarantee.

See [public terminal evidence](experiments/bcenv/runs/BCENV-010/public-terminal.json)
for counts, stop/freeze details and independent review commitments.

## Separate, prospectively bounded engineering diagnostic

After the original trial was immutable, the coordinator authorized **one**
standalone re-execution of the failed public assignment, with identical frozen
sources, binaries, map, engine, heap and normalized engine settings except output
paths; its wall cap alone became 300 seconds. The protocol and driver hashes were
recorded before execution. No candidate restarted, and no validation state was
repaired.

That engine completed validly in **122.407 seconds**, with a valid replay and
unchanged frozen roots. An independent reviewer verified the single-attempt
claim, input equivalence and chronology. This shows that 120 seconds was
insufficient for **this diagnostic execution**. It does not prove the original
stall cause or create a selection or competence result. The engine and initial
summary had separate bounded allowances; the outer 630-second cleanup envelope
was not an additional engine allowance. See the [diagnostic summary](experiments/bcenv/runs/BCENV-010/timeout-sensitivity-summary.json).

## Prospective continuation

BCENV-011 is being prepared with one narrow change: a trusted match-run allowance
of 300 seconds for both training and validation, still clipped by the unchanged
45-minute global deadline and maximum 80 games. Build, package and later replay
query limits remain at 120 seconds. A longer per-match limit may mean fewer
completed games under the same global cap; completion is not promised.
Implementation, independent tests/review, exact-head CI, a separate eight-game
public tutorial preflight and clean-input/live-parity gates must pass before a
fresh trial. The original 010 result remains incomplete. No merge or private
benchmark publication is authorized by this report.
