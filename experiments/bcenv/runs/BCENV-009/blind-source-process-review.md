# BCENV-009 blind frozen source/process review

2026-10-22. Fixed after candidate and service stopped, before reading any independent
assessment outcome. Review scope: prospective BCENV-009 functionality, process,
correctness evidence, public selection and source integrity endpoints. No heldout
files, evaluator panel/source, evaluator outcomes or prior competitor code were
read. No bot edits, coaching, additional matches or replay queries were performed.
Parent handles selected-source rebuild separately; this reviewer did not duplicate
that build.

## Disposition

**Recorded process and source-integrity checks pass; local correctness evidence is
genuine but narrow; broad game competence remains unestablished.** The locked
public validation functioned and supplied new paired selection evidence, but did
not change the provisional choice. This single run does not establish improved
generalization or causal benefit from validation.

## Freeze, identity and ordering

- Freeze009 records native candidate stopped at 12:30:25 UTC, service interrupted
  with terminal exit 130 at 12:30:35, freeze at 12:30:57.988001. No graceful stop
  marker is claimed. These are operator/native terminal observations, not a
  complete independent process-execution trace.
- Recomputed all 56 fixed input-manifest hashes: unchanged. Independently
  rehashed all 5,011 files listed across the frozen inventory roots: unchanged
  at review. Generated helper bytecode caches exist; fixed source/tool bytes
  match the prelaunch manifest. This is point-in-time cooperative integrity,
  not proof of every historical filesystem access or absence of transient edits.
- Selected original ID `s_236fe7567b554adf9b9c56092f2bad22` (V3), validation ID
  `s_c5e440b834b34bd7b3192fbdfb9c5092`. Restored candidate source, saved V3 source,
  and original/validation service source and build/source copies agree byte for
  byte (six copies). Raw Java SHA256:
  `7c42d9ac5d1fbd8e8cf25733fe8da76692685dbe023dc752d585bc8aab40c288`.
  Service normalized source hash:
  `7fe96c7fe63df8eaa9b4aa482fb7eabea3666de7907e8adc8c7b76f8aff7794c`.
  These are different hash conventions, not an inconsistency.
- Recomputed the complete 209-event audit chain. Eight source-bound notes precede
  their eight submissions; note replay references refer to earlier issued
  references. No submission occurs after lock. Lock is sequence 133 after all
  eight training completions; validation completions are 158 and 185, validation
  finished 186, final selection 209. Exactly 80 game attempts and 38 successful
  replay events are recorded. No failed request is present in retained responses;
  this is not a proof that all rejected/native operations would be logged.
- Finalist tests and SELECTION_PLAN.md filesystem timestamps precede the lock;
  the plan gives V3 as provisional choice and a validation-win/tie-retain-V3 rule.
  The service receipt independently establishes the provisional ID before any
  validation execution. The free-form plan's chronology relies on ordinary
  filesystem evidence, not a trusted precommit of its prose.
- Selected decision precedes service deadline, leaving about 915 seconds by the
  persisted phase snapshot. Maximum 2700-second clock began at service startup;
  no added candidate time or validation retry is represented.

## Public selection evidence

Training outcomes by version are 5, 5, 5, 5, 4, 4, 2 and 3 wins of eight, matching
service completion records. V3 and V4 were nominated once; each had 5/8 training
and then 4/8 validation, with identical paired validation outcomes. The final
choice retains V3 under the stated tie rule. Training and validation are kept
separate; neither is independent held-out assessment.

The candidate inspected actual validation replays rather than relying only on
scores. All 38 retained unique replay reference feedback hashes recompute.
Spotchecked cited V3 validation pages independently show BUILD_ANCHOR round 91,
PLACE_RESOURCE 112, PICK_UP_ANCHOR 113 and PLACE_ANCHOR 118. The cited losing-game
HQ 250–265 page contains resource-change action records only in that selected
window. Those pages close their selected record windows and report complete
source stream, while all_schema_fields_validated remains false. This supports
specific observed progress and limited sampled failure-state evidence, not
movement intent, damage, causal loss explanations or whole-match absence claims.
The candidate's final report makes these distinctions explicitly.

## Actual tests and independent reruns

Read selected source, both common test mains and the preserved counterexample
sources; checked four finalist receipts against their test-source, test-binary
and log hashes. These are not empty or printed-success-only mains:

- BotTest's check function increments a counter and throws AssertionError on
  false. Its actual execution prints 14,411 checks: 14,400 coordinate/owner-bit
  loop checks plus 11 policy/distance/well/movement checks. The count is dominated
  by arithmetic round trips, not 14,411 distinct game situations.
- AnchorTest explicitly fails on friendly replacement and on failure to place
  once in the neutral proxy case: two ownership checks. Neither proxy runs the
  engine or reproduces its full cooldown/current/visibility/resource rules.
- The selected V3 and alternate V4 each execute both common mains successfully.
  Receipts truthfully say execution_succeeded, assertion_coverage unknown and
  correctness not_established; inspected source and reruns provide the narrower
  evidence that these particular explicit failure conditions were executed.

Copied existing receipt directories to `reviewer/java-rerun009/`, outside all
frozen roots. Recompiled the copied test sources against their copied immutable
candidate classes and reran the original main with the pinned JDK, `-ea` and
bounded subprocess timeouts. No selected bot rebuild or new test scenario was
introduced. All 11 selected rerun outcomes reproduced:

| Existing case | Reproduced outcome |
| --- | --- |
| V3 BotTest; V3 AnchorTest | Both exit 0 |
| V4 BotTest; V4 AnchorTest | Both exit 0 |
| V1 friendly-anchor failure | Assertion failure, exit 1 |
| V6 synthetic long-wall failure | Assertion failure, exit 1 |
| First V7 local wall-follower failure | Assertion failure, exit 1 |
| V7b partial-deposit failure | Assertion failure, exit 1 |
| V8b HarvestTest; V8b ReturnTest | Both exit 0 |
| V7b extended navigation test | Exit 0 |

Rerun commands, copied sources/classes, separate reviewer logs and hashes are in
`reviewer/java-rerun009/run.py` and `summary.json`. Original inventory contains
45 test receipts (41 execution_succeeded, four failed); only the 11 listed cases
were independently rerun. All four recorded failures were included. Successes
of later experimental versions do not transfer to V3/V4. In particular, the
later harvest test refers to lastHealth absent from selected V3; no claim is made
that this exact test executed against V3. Candidate documents this compatibility
limit rather than treating all expanded tests as selected-source coverage.

## Frozen source findings and limits

Selected V3 source supports the disclosed remaining limitations. Carrier logic
calls deposit before checking whether cargo is full, so partial cargo adjacent
to home is transferred whenever the API predicate permits. Headquarters keeps a
lifetime carrierBuilt counter (rather than a living-carrier count), permitting
fewer replacements after losses. Movement is a local heuristic with recent-visit
penalties; one constrained legal-move proxy is not a navigation guarantee. The
main loop catches Exception and prints it before yielding, so compilation and
observed replay progress do not establish exception-free execution. Bytecode
safety, concurrent coordination, occupancy/current dynamics and combat quality
have not been comprehensively tested.

These observations are code-level limitations, not new engine failure results
or strategy recommendations. The long-wall counterexample was executed on V6
and the first local V7 attempt, not exact selected V3. The candidate preserves
that distinction and does not silently transplant later repairs into locked
finalists. A small historical documentation inconsistency remains: the opening
TESTS.md table describes an earlier round-100 anchor threshold; later version
notes and actual current tests identify the V3 round-50 policy. Use exact
version-bound test sources/receipts, not that stale introductory row.

## Overall interpretation

Observable evidence supports a substantive autonomous edit/test/replay cycle,
retention of negative results, genuine explicit local checks, source-bound
prospective submissions, a one-time immutable validation phase and an honest
no-switch choice. The interface treatment was used as intended. No observed
record establishes broad correctness, strong unseen-opponent performance,
causality for selection quality, or hard confinement. The candidate's claims of
no outside access/coaching are self-reports consistent with the available record,
not independently proven by hashes or the service audit. No evaluator result is
needed or used for this assessment.

## Prospective rubric ratings (no numeric aggregate)

Rubric-only axes supplied by the parent before this review was finalized; no
panel or outcome information accompanied them. Ratings apply to the stated
observations, not to general performance.

| Axis | Rating | Evidence and boundary |
| --- | --- | --- |
| 1. Legal artifact/provenance | Supported | Exact selected-source correspondence, verified build/package and fixed input hashes. Also inspected parent's selected-source-audit009.json and rebuild-audit009.json: independent old-runtime rebuild matches class bytes/source/raw ZIP; no matches run. Verifier acceptance is not general correctness. |
| 2. Prospective source-bound falsifiable hypotheses | Supported | Eight notes precede exact-source submissions. V3 predicts greater observed anchor progress with possible survival cost; V4 predicts survival/replacement gains; V7 predicts obstacle progress after a retained counterexample. Claims have observable disconfirming outcomes, though several interventions are bundled and hypotheses are not formally preregistered statistical tests. |
| 3. Prior replay references support claims | Supported, sampled | Note references precede notes and bind to real retained feedback. Inspected bounded progress/failure-state claims match cited records; no whole-game causal inference is justified. Not every natural-language claim was independently reconstructed. |
| 4. Actual-class meaningful assertions/state progress | Partial | Four finalist and seven other reruns reproduce genuine explicit checks/failures on copied actual classes; selected arithmetic/ownership/one-move checks are narrow. Game-state progress is replay-observed, not comprehensive executable engine assertions. |
| 5. Negative evidence, isolation and repeated exposure | Partial | All four retained failures reproduced; unsuccessful versions are preserved and lower public scores acknowledged. V3/V4 changes bundle multiple mechanisms; eight adaptive versions reuse the same training conditions. Validation adds paired public selection evidence, not independent replication. |
| 6. Guards, state lifetime/reset, freshness, navigation/error observability | Partial | Selected source uses API capability checks and neutral ownership guard, but lifetime production counters, partial deposits, heuristic navigation and broad exception handling limit assurance. Proxy tests do not establish full state evolution, dynamic freshness or bytecode safety. |
| 7. Boundary/no-coaching evidence | Not-assessable in full | Fixed inputs and recorded service operations are consistent with the boundary; no breach is observed in reviewed material. No complete native access, communication or intermediate filesystem trace was available, so absence of outside coaching/access cannot be proved. |
| 8. Immutable two-finalist lock and final selection | Supported within recorded interface | Exactly two completed submitted IDs lock before validation, no later submissions/re-nomination, both complete, final ID belongs to the pair, restored bytes agree and uncertainty is explicit. No claim of a complete historical edit trace; current source identity and service-side immutability are verified. |
