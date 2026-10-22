# BCENV-011 separate match timeout: engineering review

2026-10-22. **PASS — no blocking finding in the reviewed implementation.** Reviewed uncommitted `feat/separate-match-timeout` changes against 66ff465; exact reviewed source hashes are in `match-timeout011-evidence.json`. No implementation edits, game execution, candidate material or private evaluation access.

## Narrow change and compatibility

Trusted operator configuration adds optional `match_timeout`. Its absence resolves to the existing `timeout` (including 90 default); an explicit null cannot silently default because the constructor uses a distinct sentinel. Exact integer type is required, excluding booleans/floats/strings; bounds 1–300. Existing timeout retains exact integer 1–120 bounds.

Only arguments beginning with the actual `run` subcommand use the resolved match timeout. A log label or nested argument named run cannot change routing. Builds, packaging and later action/own-diagnostic queries continue using the existing timeout. Both service entrypoints forward the value, and locked-finalist worker construction inherits it from the training worker; no per-finalist adaptation occurs.

Launch identity includes the resolved value: omitted and explicit legacy values are equal, while 300 versus 90 differ. Compatibility means unchanged default operation/limits, not byte compatibility with old launch records: the added identity field and changed service hashes appropriately require a newly reviewed launch comparison.

## Absolute deadline and cleanup

Inspected unchanged adapter run path: engine and initial ReplaySummary each receive args.timeout. Thus match_timeout is a **per-process** bound, not an aggregate per-game allowance. Initial summary receives 300 under the new profile; unrelated replay queries remain≤120. Engine settings, heap, rules, projections and runtime execution helper are unchanged byte-for-byte from 66ff465.

Existing absolute monotonic deadline is forwarded unchanged. The runtime caps each child wait to min(per-process limit, remaining absolute time), refuses spawning at/after expiry, kills and reaps timed-out child groups, and refuses follow-on work once expired. Training and validation workers share the same deadline. No clock reset or game-budget change is introduced.

Without a trial deadline, a 300-second run permits the existing two-step outer allowance 615 seconds. With the trial deadline, the outer adapter is supervised until remaining + 5 seconds so its independently-sessioned child can be reaped first. That cleanup grace is not authorization for additional game work; the inner absolute deadline remains decisive. The longer match bound cannot guarantee completion of 80 games within 2700 seconds, and incomplete/no-selection outcomes remain valid.

## Independent tests and scope

Using host Python, independently ran all 12 new match-timeout tests and 8 existing absolute-deadline tests: 20 PASS. Coverage includes absent/explicit defaults, boundaries and invalid types, run-only dispatch, both config entrypoints, failed readiness on invalid values, finalist inheritance, parity differences, fixed-deadline propagation, expired-spawn refusal, and actual nested detached-child termination/reaping with refused follow-on. Tests launch no game engine; the deadline suite uses synthetic subprocesses.

Documentation accurately distinguishes per-process versus total-game time, optional/default behavior, operator-only control, unchanged unrelated limits and remaining-budget clipping. Prompt history remains append-only; this engineering review does not attest every reconstructed provenance entry's chronology.

No unresolved blocker. Exact commit/publication/CI/release identity, clean 011 inputs/protocol and the separately authorized eight-tutorial-game preflight remain later gates. This review does not authorize live initialization or infer competitive improvement from the earlier standalone timing diagnostic.
