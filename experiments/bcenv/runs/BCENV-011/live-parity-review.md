# BCENV-011 actual live parity

**PASS.** Independent read-only check at 2026-10-22 15:24:55.087824 UTC, before candidate launch. Evidence: `check-live011.py` and `live011-parity.json`.

Actual live and stopped-integration launcher identities/configurations are equal; both report probe_passed and check_only:false. Live/preflight configuration bytes match. Verified match_timeout300, other-operation timeout120, duration2700 and current host service source hashes. These are per-subprocess caps bounded by the unchanged absolute deadline, not total-request guarantees.

All 57 initial static input hashes match the fixed manifest. Source/tests/work and mailbox requests/responses are empty; no symlinks or unexpected mailbox entries. Service contains no jobs or audit work: phase training, zero game attempts/reservations, no finalists/provisional/final choice, not halted. Mailbox and phase deadline metadata agree; deadline minus start is2700seconds. Remaining time at check:2688.960561seconds. The already-running clock is not reset by this review.

- Live launch SHA256: `4f8391098040863be6460ee2c053620b14586d37ffd0e9acd41fc31961820a31`
- Integration launch SHA256: `d67ea37607d8d3050a5c3a4e8febe9a1fd2059cde04fe944d6a1f29fa2db967a`

This attests the observed identity/configuration and clean state only—not ambient-environment equality, hard confinement, future completion or competitive performance. No game, build, replay query or candidate code inspection occurred. Prior fixed input/preflight reviews remain unchanged.
