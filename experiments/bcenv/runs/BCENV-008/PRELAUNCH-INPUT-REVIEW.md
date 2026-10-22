# BCENV-008 independent code/protocol/input review

Fixed2026-10-22 09:58 UTC. Reviewed code ceaac7af0c940d4587b890eff17f2924fe7ddbe1, prospective planner008 protocol cfbc496 and fresh008 export. No held-out material/outcomes inspected; no candidate or frozen roots modified.

## Verdict

No code publication or candidate-input blocker identified. Exact-head CI, real eight-game integration, live parity/empty state and parent readiness remain separate required launch gates. This is not authorization to skip them.

## Code and contract

Java-test receipt schema advances to v2. Zero-exit execution with intact snapshots yields execution_succeeded; assertion_coverage remains unknown and correctness not_established. assertions_enabled=true means configured -ea, explicitly not evidence any assertion or JVM actually ran. Compilation failure leaves execution_status=not_run. Runtime/assertion failure, timeout, output cap, snapshot/build integrity failure retain failed/nonzero outcome. Separate execution_status may be succeeded when later integrity check fails; overall status remains failed, appropriately distinguishing execution from evidence validity. Build receipts remain v1. No assertion-count heuristic, oracle, test framework, strategy fixture, access relaxation or runtime limit change introduced.

Independently ran pinned-Java focused suite:21 tests, all successful, no skips (reviewer/008-focused-tests.log). Fixtures cover real asserting main, print-only and empty mains all execution-only; false assertion nonzero; invalid Java not run; existing timeout/output/integrity/path constraints. Coordinator's351-test full-suite and exported-helper smoke are additional evidence, not rerun in this review.

## Input inventory and coaching boundary

Independently hashed all55 live files: exactly competitor008-export-manifest.json, SHA256c80781dc5c5caeb68bf8ba544534db3d33991a0bcdbf7f3916c18cea6328cd66.49unchanged versus007; six changes are README generic evidence language, helper semantics, kickoff workspace path, two launcher paths and derived helper manifest. Exported helper bytes match reviewed code. No symlinks; src/tests/work empty; mailbox absent. No previous bot, tests, review, score, experiment evidence or evaluator data copied.

README asks for expected condition, actual executable check, evidence and limitation; distinguishes printed/manual observation from assertions and marks untested claims. This is generic evidence hygiene, not bot strategy coaching. No prior candidate defect example or scenario is included. Same public rules/API/client/replay semantics and budget remain. Protocol honestly calls this narrow feedback-quality intervention, not evidence wording improves bot competence; cooperative same-user and runtime/instruction-reconstruction limitations retained.

Subsequent audit should judge claim inventories against actual test code and results, never accept inventories as machine-verified coverage. This review does not change or retroactively upgrade frozen007 test claims.

## Final launch-parity spot-check,10:14 UTC

Independently compared actual integration008/launch/launch.json and development-launch008/launch.json: identity objects exactly equal, both probe_passed and check_only=false. Live record SHA25669a9f20422aacacebeb81a3f42ae990e3b59fd78f8525adf54d2fcb11646f217. Rehashed all55 static inputs unchanged. src/tests/work and mailbox requests/responses all empty. Integration summary records8completed games/26queries, terminal coverage and both-team activity, all8replay hashes equal007, stopped exit130 with no graceful marker. No input/parity blocker found; exact CI checks and final parent launch acceptance remain coordinator responsibility. Cross-launch ambient environment equality still not attested.
