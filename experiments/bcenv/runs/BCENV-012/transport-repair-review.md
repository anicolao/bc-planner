# Independent atomic-publication repair review

**PASS for the narrowly scoped code repair and publication gate; not authorization to launch a service or run games.** Reviewed stable uncommitted patch against `877aa5d0f38ef8e56b8d6259d0c654d5929d284b`. Original failure diagnosis remains immutable at `reviewer/PREFLIGHT-012-FAILURE-DIAGNOSIS.md` (SHA604bd2deb7d20086fe8220f5d700ae0041f261770243e4b85a24b9db9bb9a413). All seven evidence hashes in that diagnosis were rechecked unchanged. No private material, candidate strategy, matches, replay retry, or service launch was used.

## Implementation review

- `services/local_trial.py:647–658`: only continuity recognizes exact32-lowercase-hex `.tmp` staging, before request charging. It uses `lstat`, permits regular empty/partial files through1,500,000 bytes, rejects symlinks/directories/special files/observed oversize, and catches only `FileNotFoundError` for the snapshot-to-inspection rename race. Legitimate staging is neither deleted, dispatched nor debited. Invalid staging fails closed rather than becoming an unlimited dispatch channel.
- Queue32 is checked against all directory entries before staging recognition. The unchanged storage guard still includes staging bytes; no storage accounting exemption or deadline reset was added. Idle staging is not a continuously enforced filesystem quota: existing sampled guard semantics remain.
- The three existing consumer cleanup calls now tolerate absent targets with `missing_ok=True`, not arbitrary cleanup failures. Committed requests retain transport debit and seen-ID registration before read; disappearance before reading yields the existing invalid-request response, while disappearance after dispatch preserves the response. Neither becomes a retry. Malformed names, invalid/oversize published payloads and repeated IDs remain bounded.
- The staging special case is continuity-only. The three missing-target cleanup tolerances are shared by legacy and continuity paths; thus legacy disappearance-error behavior is intentionally more tolerant, not byte-for-byte identical in that exceptional case. Ordinary valid request behavior, defaults and quota values are unchanged.
- Diff is confined to service handling,14 new synthetic tests, explanatory documentation and prompt provenance. Client, profile constants, adapter, engine, replay projection and candidate inputs are unchanged. No new recovery mechanism, source submission or selection rule was introduced.

## Independent checks and negative evidence

I independently ran all14 `test_mailbox_publication.py` tests: PASS in0.427s. These use the real published client with deterministic barriers both before publication and after the consumer directory snapshot; successful response and exactly one dispatch/debit are asserted. Additional cases cover staged-file types/sizes, queue overflow, storage measurement, deadline stop, committed-file disappearance, repeated IDs, malformed/oversize publication, and propagation of a non-FileNotFound cleanup error.

I separately reran the existing actual-mailbox2200 ceiling test: PASS in1.162s. It reaches2200 processed attempts,551 dispatches and the expected bounded response/remaining-request counts. That test deliberately mocks storage checkpoints to isolate transport accounting; it is not a storage-stress test.

Inspected worker aggregate log:498 tests PASS in46.441s (not independently rerun in full). Inspected old-head actual-client negative-control log: expected failure, specifically `consumer removed uncommitted staging`. The retained old service source hash equals `git show 877aa5d:services/local_trial.py`; this demonstrates sensitivity to the reported bug rather than a test that merely accepts both implementations.

## Remaining limits / release conditions

The separate storage scanner can still fail closed on concurrent entry disappearance; this accepted residual is unchanged and documented, not claimed solved. Targeted tests do not establish six-hour liveness, recovery, hard confinement, or a numerical storage-overshoot cap. Missing-file tolerance is not authorization to resend an uncertain operation. The original012 preflight remains failed; any replacement must have separate exact-code CI/review, prospective authorization, fresh roots and independently reviewed terminal evidence. No concrete blocker remains in this scoped patch.

## Reviewed bytes and test evidence

- `bcenv/services/local_trial.py`: `a3b7547984206eea38b4bdbc1063fef651621c36db45f088515f5785aca5591f`
- `bcenv/tests/test_mailbox_publication.py`: `6979429fea2b5c9bf8e2741520ae215a43779b9a791b36ba75ddae76c315fe38`
- `bcenv/docs/continuity-profile.md`: `84369126b761abfadbdc336cae657185c6edf6ee54b4b7e2b780e6131295115c`
- `bcenv/PROMPTS.md`: `1411069013a3bb247d006342fd80df98bebcdd31211b8be19f61844d64cc5188`
- `engineering/transport012-repair/reviewer-focused-tests.log`: `d0208e549c218f98c6b2eb6df1bc41b2195735ea388b00271ca52130e46d9a92`
- `engineering/transport012-repair/reviewer-mailbox-cap.log`: `657e32b3000ba826a40ec5859875a0c5a95c382992279a6a755470018fc55b14`
- `engineering/transport012-repair/full-tests.log`: `c8ec459f7b42eabb49435a707d64abcc68e0bd6e6b88b90fda7c6c3d4edb3862`
- `engineering/transport012-repair/old-head-negative-control.log`: `d33028bd6f39b3b5fa3e4abc13a031c87504f2615565e0fd439e0516de1ca2a5`
- `engineering/transport012-repair/local_trial-before.py`: `d156602455a94bf384a9d9cad05f1278a8388a2c5a903420094aae61b06f4226`
