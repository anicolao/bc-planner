# BCENV-009: public finalist validation feasibility

Prospective design before009 preflight or competitor launch. The standing
long-running environment mandate continues. Parent accepted an explicit bounded
increase from64 to80 public games on the existing VM, not new monetary spending,
credentials, access relaxation or merge authority. No previous bot is resumed.

## Development-only motivation and scope

Recent public-development runs exhausted eight versions before45minutes and
used fewer than150 replay requests. A candidate knowingly selected its highest
repeated-schedule score despite a retained failing synthetic test. These traces
motivate studying selection evidence, not forcing all mock tests green or giving
strategy fixes. Eight repeated conditions drive both edits and selection; that
is useful paired debugging evidence but a narrow, adaptively reused signal.
No causal explanation of independent evaluation results is asserted here.

Keep the existing eight-game training schedule, both public opponent revisions,
map/side order, engine/API/rules and generic validation helper unchanged. Add one
locked public selection phase. This bundles additional game budget and selection
information; one feasibility run cannot isolate their causal effects or establish
reliable broad competence. Training-map rotation is deliberately deferred.

## Prospective budget and phases

- Fresh fork-none requested gpt-6.1-sol/high, remaining time within a hard
  45minute live-service-start budget.
  Requested settings are not independent runtime attestation.
- Up to8 accepted training source versions,8games each,64 training games maximum.
  Build rejections consume a version but do not create replacement games.
- Exactly2 distinct already-completed, verified submission IDs are nominated
  together with a provisional choice, before any validation feedback. Candidate
  records its concise source-bound rationale; no operator chooses its finalists.
- Lock atomically reserves16 public-validation games: each finalist receives the
  same8cells (2new public maps ×2existing public opponents ×both sides).
- After lock reject all new source submissions, re-nominations and additional
  validation requests. Validation is serial and source-bound; reuse the frozen
  source/build only after identity verification. Stop on first failure, no retry,
  substitution, altered schedule or timeout-as-loss conversion.
- Expose results and bounded replay queries for both immutable finalists through
  the enforced interface. Candidate selects exactly one original finalist ID,
  restores its exact submitted source bytes, writes final evidence/limitations
  and stops. No post-validation code version is accepted.
- Total maximum80 public games,24notes,150replay requests; all phases consume the
  same conservative service-start45minute deadline; candidate receives the
  remaining time, at most45minutes. Public match wall limit120seconds/512MiB heap
  remains fixed. Incomplete work/deadline/failure remains explicit; no arbitrary
  operator final selection or hidden extra games to complete a favorable result.

The trusted service records UTC start/deadline plus monotonic elapsed-time
bounds at initialization. Every worker invocation is capped by the smaller of
its ordinary timeout and remaining run time; no new match, submission, finalist
lock or final selection begins after expiry/stop. Candidate is stopped at the
same hard deadline. Incomplete validation cannot produce a completed selection;
no operator fallback is fabricated. Observer-only diagnostics may be retained.
All CI/preflight/parent-conditional readiness gates precede live initialization;
independent final parity and native spawn follow immediately. Preflight has its
own separately recorded deadline. Only a never-used, empty pre-candidate service
may be restarted after a readiness delay, with the attempt explicitly recorded;
never reset a running competitor's deadline.

State transitions: training → finalists locked → validation running → validation
complete → selected. Pending training prevents locking; incomplete/failed builds
are ineligible. Reserve all16games before dispatch; persist phase, nomination,
provisional choice, receipts and selected identity. Existing no-resume service
policy stays fail-closed on reused roots after interruption; do not reconstruct
fresh training state and silently replay work. Test concurrent/duplicate requests.

## Public map selection, not private benchmark adaptation

Use the pinned official public map inventory. Predeclared seed:
`BCENV-009-public-validation-v1`. Rank map name/content-hash records using the
exact algorithm documented in `experiments/bcenv/runs/BCENV-009/validation009-public-map-plan.json`; exclude
only Quiet and BowAndArrow training maps and take the first2ranked entries.
Freeze inventory/hash/algorithm before any009 match. Do not inspect geometry or
filter based on candidate results, strategy or evaluator membership. Validation
maps are novel to this training schedule, not necessarily unknown to the model
or absent from an evaluator panel. Public assets are not claimed secret.

All validation cells are trusted operator configuration; candidate requests
cannot name arbitrary map paths, opponent builds or source overrides. Both
finalists receive identical ordered cells. These results inform selection and
are therefore not an independent held-out performance estimate.

## Engineering and launch gates

1. Exact code/protocol CI green; independent state-machine/receipt/source-binding
   and budget review. Cover wrong/pending/duplicate IDs, failed sources, changed
   source/build/map bytes, nomination races, post-lock edits/submissions,
   re-nomination, repeated validation/selection, restart refusal and stop-failure.
2. Actual public tutorial end-to-end integration through the same shared
   host-Python launcher and fixed offline adapter command; explicitly budgeted
   as32games:2official tutorial training submissions×8 plus2locked finalist
   validation jobs×8. Both tutorial snapshots retain identical original source
   bytes but distinct submission IDs; no strategic edits. Negative phase requests
   create no games. This32game engineering gate is separate from80candidate
   games. Preserve all attempts, no automatic retries.
   Verify real locking, both finalist jobs/results and bounded terminal replays.
   At most2pages per early/terminal window (≤128queries total); retain any
   continuation and distinguish terminal source coverage from full selected
   record enumeration. Both-team activity must be positively observed.
3. Same integration/live identity plus same-process bounded adapter probe;
   no nested outer Nix service. Ambient environment equality across launches
   is not independently attested. Same-user native workspace restrictions remain
   cooperative, not hard confinement or full access tracing.
4. Independently reviewed fresh source-empty export; no prior candidate source,
   tests, review/results or evaluator material. Generic phase/budget documentation
   only, no bot-specific hints. Empty live service and fixed input manifest.
5. Parent readiness gate before fresh launch. Stop/freeze selected source,
   binaries, all versions/receipts and static inputs after candidate/service stop.
   Blind process/code review fixed before separate evaluator outcomes.

## Endpoints and independent observed regression

Record provisional/final choice, both finalists' paired training/validation
outcomes, replay-grounded selection rationale, known-test tradeoffs, all versions,
wall time/query/game use, interface failures and immutable selected-source proof.
No required switch, post-hoc score threshold or assumption that a new validation
winner is broadly better. Candidate authored tests/claims remain limited evidence.

Private prospective regression adoption:9336ASCII bytes, SHA256
`897345ed6dba2b0537656651eec6bc8744814f43edb8cdfa0f3b954805641648`.
Same evaluator-observed panel/order/pins,24serial games maximum, uniform300second
wall cap/512MiB, stopfirstfailure/no retry/substitution. No panel contents enter
candidate inputs; no new private plan file before stopped/frozen confirmation.
Public validation overlap is not filtered away or used to claim pristine
holdout. Report functionality, process, correctness and performance separately.

This prospective document contains no independent evaluation outcomes. Private
raw records remain local; any pending denied summary payload is excluded from
this branch and is not indirectly published here. Public development/engineering
records and future summaries remain subject to their applicable permissions.

## Engineering readiness — 2026-10-22 11:53 UTC

[bcenv PR21](https://github.com/anicolao/bcenv/pull/21), exact head
`f0a7591d3f5ec401384e3120d0c12d5c3cb40922`, passed CI39771651402 and
390 local tests. Independent review fixed deadline propagation into detached
engine/compiler children and late phase decisions. A loaded-host synthetic
fixture wait timed out once; isolated rerun passed, test-only wait slack was
increased, and all29 phase tests passed. This is not omitted from the review.

The separate fixed tutorial preflight completed32 games,110 bounded replay
queries, both-team activity and terminal source coverage for every game. All16
training replays reproduce the prior eight tutorial fixtures. Lock, both
validation jobs and selection succeeded; five negative phase requests were
rejected without extra games. No retry or runtime substitution occurred.
The driver exited0; explicit service interruption exited130. No graceful
shutdown marker is inferred. Mechanical audit found no discrepancy in296
chained events,32 game charges and110 feedback receipts. Its182 process receipt
instances include repeated immutable snapshots, not182 unique launches.

The installed local runtime remains `7yh1yrs7m8yk4idh1x2rpqcqn7f7yhx9`. CI's
clean-Git runtime is `jbi5ggy37yggb8fhfrs9f98sfyb0xdp1`: the CI merge and head
have the same Git tree, all52 installed entries were compared,51 are exactly
byte/mode/type identical, and the sole wrapper difference is its own store
prefix. External dependency references match. Raw NAR equality is not claimed.
The live service must retain the exact preflight runtime and configuration.

The fresh56-file export is independently hash-checked, source/test/work-empty
and free of prior candidate or evaluator material. All remaining launch gates
are explicit in [engineering readiness](experiments/bcenv/runs/BCENV-009/engineering-readiness.json).
No009 candidate has launched at this checkpoint; the live45minute clock must
start only after updated protocol CI and parent conditional readiness.

## Fresh launch — 2026-10-22 12:01 UTC

Updated readiness head `0a5fb11bf827ea0158aa10f6aedea376a68a3e71` passed
CI39774405244 before service initialization. Parent orchestration accepted the
conditional gate under the standing mandate, not a new user reply. Independent
live review verified actual preflight identity/config parity,56 unchanged
inputs and empty source/tests/work/service/mailbox.

The live clock started12:00:06.398226 UTC; hard deadline12:45:06.398226 UTC.
Fresh fork-none requested gpt-6.1-sol/high launch was requested12:00:50 and
acknowledged12:01:07; creation is bounded by that interval, not independently
attested to a finer time. Startup consumed about60.6seconds by acknowledgement,
leaving2639.4seconds. The clock was not reset for the candidate. Exact fixed
KICKOFF.txt bytes were supplied without prior candidate/evaluator context.
See [launch record](experiments/bcenv/runs/BCENV-009/launch.json).

Observer-only monitoring follows; no strategy intervention or duplicate trial.
Stop and freeze before private evaluator materialization. This active launch
is not a completion or competency result.

## Frozen public development result — 2026-10-22 12:36 UTC

The fresh candidate completed all64 training and16 locked-finalist validation
games, with no recorded infrastructure failure or retry. Eight source-bound
notes and38 bounded replay receipts are retained in a verified209-event chain.
Exactly two completed versions locked before validation; no subsequent source
submission or re-nomination occurred. Both finalists had5/8 training and4/8
validation wins. The final selection kept provisional V3 under its stated tie
rule; this run does not demonstrate that validation improved selection.

Native completion was received12:30:25 UTC. Explicit service interruption
returned exit130 at12:30:35; no graceful shutdown marker is inferred. Freeze
was recorded12:30:57.988 UTC, before the12:45:06.398 hard deadline. All56 fixed
inputs and5011 frozen-file hashes were independently rechecked unchanged.
Selected source matches original and validation snapshots; an independent
old-runtime rebuild reproduces source inventory, class bytes, binary identity
and raw package ZIP exactly. The service normalized source hash, adapter
inventory hashes, raw Java digest and ZIP hash are separately labeled.

The [blind review](experiments/bcenv/runs/BCENV-009/blind-source-process-review.md)
was fixed before independent evaluator outcomes. Eleven copied compile/JVM
reruns reproduced four finalist passes, four retained failures and three later
experimental passes. Explicit checks are genuine, but mostly narrow arithmetic,
ownership and local predicates: successful execution is not general correctness.
Later tests do not transfer to older selected sources; retained counterexamples
and source-level limitations are distinguished from new engine failures.

The interface and immutable finalist workflow functioned in this bounded run.
Training and validation remain separate public selection evidence, not an
independent performance estimate. No causal improvement, broad competence,
hard confinement or complete intermediate access/edit trace is claimed.
See the [development summary](experiments/bcenv/runs/BCENV-009/development-summary.json)
and its linked hash-bound mechanical records. No independent evaluator outcomes
or denied publication payload are included in this update.
