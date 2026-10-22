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

- Fresh fork-none requested gpt-6.1-sol/high,45minutes from recorded launch.
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
  same45minute native wall budget. Public match wall limit120seconds/512MiB heap
  remains fixed. Incomplete work/deadline/failure remains explicit; no arbitrary
  operator final selection or hidden extra games to complete a favorable result.

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
