# Independent fixed-input review: BCENV-012

2026-10-22. **PASS for this initial input snapshot.** No candidate/helper, game, build or test execution; no source edits or private evaluation material accessed. This does not authorize preflight or candidate launch, and does not attest pending CI.

## Exact inventory

- Export: `competitor-012/`; manifest `competitor012-export-manifest.json`, SHA256 `9333e9d1f8fee6353f32dd9b03dd71dd80d91757213a35846523524dd3bab80a`.
- Independently enumerated exactly57 regular files; every hash matches the manifest. No additional files/directories beyond listed-file ancestors and the three designated empty directories; no symlinks or special files.
- `src/`, `tests/`, `work/` are empty; `mailbox/` is absent.
- Independently rehashed only the57 initial static allowlist paths in011 against its initial manifest SHA256 `26b216760992f4975f9d22aad152578bc854c89a11e7f20286f9631c50abff80`. No prior candidate-generated source/tests/work/results were read for this task.
- Exactly51 files remain identical; six changed: `candidate-check`, `.candidate-check/inner-launcher`, `.candidate-check/manifest.json`, `KICKOFF.txt`, `README.md`, `docs/public-finalist-validation.md`.
- Both launcher changes are exactly011→012 path rebinding. The helper manifest changes only workspace and the two derived launcher hashes; runtime/API/helper source pins remain unchanged. The exported client is byte-identical to `bcenv/services/local_trial_client.py` and its manifest hash. Nothing was installed or executed to establish these static facts.

Mechanical evidence: `reviewer/INPUT-012-MECHANICAL.json`, SHA256 `76746bf1be57aa24e7292c95fcf032ecbd10366a0f4410c01c6258a9aa12ebaf`.

## Content and consistency

Read the exact kickoff, README and phase guide. They consistently specify21600 seconds from service initialization,24 versions×8 training games=192, exactly two locked completed original finalists×8=16,208 maximum total;72 notes,450 replay requests sharing2000 reads, and2200 mailbox attempts including invalid attempts. They require immediate remaining-time inspection, preserve source snapshots, forbid post-lock changes/re-nomination/retries, and require final choice/restoration of one existing locked original only after both validations complete. Failures/deadline/uncertain outcomes remain stopping conditions; no fallback, session restart or allowance extension is offered.

The300-second run/initial-summary and120-second other-child semantics are accurate, including remaining global deadline and the distinction from aggregate request time. Local test execution is explicitly not assertion coverage/correctness or engine equivalence. Optional diagnostics remain optional and are not an exception/correctness oracle. The1GiB service-owned sampled guard is not presented as hard quota or workspace confinement; in-flight overshoot and conservative scan-race halting are disclosed.

New checkpoint/milestone text is generic: self-chosen hypotheses, exact IDs, pending work, supported/untested claims and concise public records, not private chain of thought. The reviewed changes contain no earlier candidate policy, strategy, tests, outcome feedback, evaluator material or operator-authored bot fixes. The remaining51 files are the hash-verified previously reviewed initial public rules/API/generic-tool inputs, not files copied from generated work. No broader native-access audit or hard isolation is inferred.

Budgets and phase rules agree with the reviewed continuity-v1 code and prospective protocol snapshot SHA256 `79537285349afe465c407dcb4cea016904f6b559c5a138b5016e502ff26b6f12`. A subsequent protocol link-only update is outside this fixed input snapshot; it need not change candidate files.

## Gates still outstanding

Exact published code/protocol CI, concrete preflight driver/config review, prerequisite calibration termination, authorized eight-tutorial-game preflight and stopped-receipt audit, then parent conditional readiness and actual empty live parity must be checked separately. This review makes no claim that any of those later gates have passed or that six-hour native uptime/recovery is guaranteed.
