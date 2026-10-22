# BCENV-009 public finalist-validation engineering review

2026-10-22. Independent narrow review of the proposed public service phase, not
candidate strategy, candidate performance, or evaluator outcomes. No competitor
source, heldout material, evaluator panel, or evaluator results were inspected.
No real matches were launched by this reviewer. Frozen 007/008 roots were untouched.

## Disposition

**Engineering review passed, conditional on exact-code CI, pinned-runtime parity,
the separately authorized 32-game public tutorial integration, clean export and
parent launch approval. This is not candidate-launch authorization.**

Reviewed working branch `feat/public-finalist-validation`, based on
`ceaac7af0c940d4587b890eff17f2924fe7ddbe1`, plus the prospective planner009 protocol
and integration009/run-check.py. Final implementation SHA256 identities:

- services/public_finalist.py: `85613ee9c1c747f751986fcb4a2f0a2227d2b7040a6fe3db735728f01a02fcc1`
- services/local_trial.py: `801d1dee20ba3cd9f45426946031e681f0b6505321b2efad953156d3c4524fa6`
- services/launch_local_trial.py: `d77c4bc5524939879a420b6f0fee53fa60b1dc7125aafdf97379a8edb4229002`
- runtime/artifacts.py: `657159dafb5cf1fc4f9001927446b1d9217e4fa4bc1186a34989571b4a321da7`
- seasons/2023/adapter.py: `ebbd92c9a25118fdc16558739c66ab20d9d1f7f0c2af2c8279e46c905f71783f`

## Findings resolved before disposition

1. Initial outer-only deadline could kill the adapter while its separately
   sessioned JVM child survived. The fixed adapter forwards the same absolute
   monotonic deadline to all five child-execution call sites; child execution
   refuses expired starts, bounds each wait and kills/reaps on timeout. The
   outer service permits five seconds of cleanup grace rather than killing the
   child supervisor first. The actual synthetic detached-child test verifies
   SIGKILL, reap/PID disappearance and refusal of a follow-on child.
2. Lock/selection identity hashing could cross the deadline after an initial
   request check. Both now recheck and record the decision timestamp immediately
   before mutation. Selected phase is explicit. Timestamp checks are application
   observations, not hard-real-time kernel/disk guarantees; receipt fsync and
   bounded cleanup may finish later and must not be represented as extra work.
3. Integration negative checks initially expected a nonexistent `error` key.
   They now assert `status:error` and exact reasons; early selection rejection
   occurs deterministically before lock. Replay pagination is bounded at two
   pages per early/terminal window (at most 128 queries for 32 games), with next
   offset and selected-window enumeration separately recorded. Source/footer
   coverage is not represented as exhaustive returned event enumeration.

## Reviewed invariants

- One RLock serializes nomination, source submission, result and replay requests;
  pending training prevents lock. Exactly two distinct completed original IDs
  are eligible; identical source hashes are allowed for the official tutorial
  engineering fixture. Validation IDs are separate from original finalists.
- Lock reserves the fixed 16-game schedule before dispatch. Training accepts at
  most eight versions; attempt receipts precede execution; phase and total caps
  are 64/16/80. Concurrent nomination cannot schedule a second validation run.
  New source, re-nomination and repeated selection are rejected after lock.
- Verified source, packaged source and binary inventories are compared at
  capture/lock/validation/selection. Opponent and map identities and commands are
  checked; requests cannot supply arbitrary trusted paths or replacement code.
- Validation reuses one ordered schedule for both finalists. Stop-first failure
  halts the phase and marks pending validation not-run; no uncertain work is
  automatically replayed. Existing roots cannot resume as fresh training.
- Atomic fsynced phase evidence and hash-chained audit receipts preserve phase,
  nomination, selection and attempted-game accounting. Persistence/scheduling
  errors halt. This is a cooperative same-user integrity profile, not protection
  against a malicious host-file editor or a resumable transactional service.
- Validation replay routing uses its own worker/cells and validation submission
  ID, retains bounded schemas/read/replay quotas and replay content hashes.
  Independently exercised note-enabled reference generation binds validation ID,
  original source hash, feedback hash and an audit sequence after lock.
- Service-start duration is at most 2700 seconds, not a freshly armed candidate
  budget. Every child gets the same absolute cutoff; no subsequent child starts
  after expiry. Unfinished validation or no valid selection is not a fallback
  winner. Parity compares configured duration, not launch-specific clock values.

## Independent verification and limitations

- Initial focused public finalist suite: 27 tests passed before deadline fixes.
- First combined run during concurrent source edits: 49 tests, one stale AST
  expectation failure after adapter forwarding changed to `deadline_options`.
  This mixed-snapshot run is not a final gate.
- Stable combined run of `tests.test_public_finalist`,
  `tests.test_absolute_deadline`, `tests.test_artifacts`: 48 passed, one error
  from a synthetic fixture's 10-second future wait under concurrent build/test
  load, before the tested nomination. No correctness assertion failed.
- Isolated rerun of that success case plus all absolute-deadline and launcher
  tests: **20 passed in 6.484s**. Actual nested child termination and launcher
  duration/schedule parity rejection passed. Test-only wait limits should be
  made tolerant of loaded CI hosts; no production budget relaxation is needed.
- Extra independent synthetic note-enabled replay receipt check passed.
- Read operator smoke evidence
  `engineering/deadline009-runtime-smoke/summary.json`: zero games, new pinned
  runtime `7yh1yrs7m8yk4idh1x2rpqcqn7f7yhx9-bcenv-2023-0.1.0`, expired compiler
  never started, future-deadline compiler/verifier both reaped under one cutoff,
  old runtime rejects the new flag. This is inspected worker evidence, not an
  independently repeated JVM run.

The reviewer has not run the full aggregate CI or real 32-game integration.
Those remain required external gates. Public finalist data are selection data,
not independent held-out performance evidence. No claim of improved bot quality,
causal efficacy, hard filesystem isolation or exact ambient-environment equality
is made by this review.

## Final test-only follow-through

Worker raised only synthetic fixture scheduling waits (flush/release to 30 seconds,
entered gate to 10 seconds), without production timing changes. Worker-reported
focused 29-test rerun passed in 3.081 seconds. Final hooked local commit:
`f0a7591d3f5ec401384e3120d0c12d5c3cb40922`. Reviewed implementation hashes and
pinned runtime are unchanged; authenticated publication and exact remote CI remain
parent/worker gates, not implied by the local commit.

## CI runtime equivalence follow-through

Independently recomputed the actual alternate-store installed inventories for
local `7yh1yrs7m8yk4idh1x2rpqcqn7f7yhx9` and CI/reproduced
`jbi5ggy37yggb8fhfrs9f98sfyb0xdp1`: 52 entries, 51 raw-equal; the only differing
file is `bin/bcenv`, byte-equal after replacing only each own immutable store
prefix. Modes/types and all installed source/classes agree. Fresh `nix path-info`
confirms CI runtime NAR `sha256-MebHWJjOdNoViN7bQVfQXZyTEjUCMuAD4h3cMS1KWFw=`
exactly matches downloaded CI release metadata; non-self dependency references
of both closures agree. They are different store/NAR identities, not claimed
byte-identical packages.

Independently repeated authenticated read-only GitHub commit lookup for CI merge
`1634e15bc32eb41384309a7c89c2f2d8bcf96271`: tree
`13b4dddaca665e866cc3f0a470423b23ea2ccb20`, matching locally resolved head f0a7591.
Evidence: `engineering/runtime009-ci-equivalence.json`,
`engineering/pr21-ci-evidence/`, `engineering/pr21-ci-commit.json`.
No active runtime/configuration was changed by this review.
