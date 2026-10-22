# Own-team diagnostics: independent engineering review

Reviewed 2026-10-22. **PASS for the reviewed projection implementation and offline evidence; no engineering blocker found.** This is not a new trial authorization, release-CI result, or competitive assessment.

## Scope and evidence

Reviewed dedicated Java extractor, strict Python projector, adapter/service/client routing, limits, receipts, documentation and Nix registration. Exact reviewed source hashes are in `own-diagnostics-check/evidence.json`. No implementation edits, new games, candidate material, private panel/outcomes or frozen-review edits were used.

Independent checks:

- All 31 projection/service/adapter Python tests pass (log: `own-diagnostics-check/python-test.log`). Tests exercise trusted slot routing, wrong-team receipts, replay mutation, source/reference/audit binding, shared quotas/deadlines, byte caps and invalid candidate-supplied paths/teams.
- Compiled final Java sources and ran assertion-bearing synthetic tests successfully. Explicit differential fixture changes/adds only opponent diagnostics and preserves the complete own query response, including paginated counts/cursors. Unknown and opponent robot filters have identical empty evidence apart from the requested ID. Malformed arrays, duplicate/reused/unknown identities, duplicate deaths, invalid strings/counters and absent channels are covered.
- Inspected the separate raw-vector reader and independently reran it on the two existing public tutorial integration009 replays (training and validation). All 106,573 recorded diagnostic rows across both slots agree, including 46 full-window/pagination/filter queries. Log: `own-diagnostics-check/raw-vector-rerun.log`. This compares raw-vector expected rows without using extractor helpers to construct the expected result; both implementations still use the official schema library.
- Replay and result SHA-256 values remain equal to the proof's saved input hashes. No new engine invocation was made.
- Installed `ir2mliawfvi6gg07rgrx1pfcp0bf3f0f` adapter and OwnDiagnostics source match reviewed working sources. All pre-existing installed replay classes remain byte-identical to frozen `7yh1yrs7m8yk4idh1x2rpqcqn7f7yhx9`. Build changes add the extractor; no gameplay/settings modification appears in the change set.

## Security and semantics

Ownership comes from trusted initial/spawn tables and the service's game slot, never an indicator prefix or candidate-selected team. IDs cannot be reused within a match. Spawn processing precedes diagnostic joins; death processing follows them, preserving same-round dying robots. Own filtering precedes counting/paging, and deterministic own-ID ordering exposes no raw vector positions or opponent diagnostic counts. Raw source metadata is discarded by the allowlisted projection.

The Python layer validates the entire supplied page, including locally withheld records; rejects extra row keys, malformed counts/cursors and invalid Unicode; and emits escaped untrusted strings capped at 64 UTF-16 units. The 32,768-byte feedback limit and 65,536-byte outer limit remain. Byte-cap continuation advances by the actual returned prefix; an impossible one-row envelope fails rather than returning a zero-progress cursor. Ownership authentication remains the Java extractor's responsibility, not something a shape-only sanitizer can establish.

The explicit mode is receipt-bound and shares existing query quotas and deadlines. Omitted/default action mode retains its existing path. Diagnostic stderr, engine logs and arbitrary source paths are not projected. Public fixtures plus synthetic differential checks support the own-only contract; they are not a proof against every malformed binary or timing side channel. Fail-closed malformed-source outcomes remain observable.

Indicators are deliberate final recorded emissions, not automatic exception capture; missing/empty/null evidence is distinguished and does not establish success. Bytecodes are recorded counters, not CPU time, correctness assertions or automatic overrun diagnosis. The documentation states these limitations. No performance or strategy improvement is inferred.

## Review follow-up resolved

Requested a stronger opponent-only differential fixture rather than relying solely on an omitted canary string; final synthetic tests now include it and passed independent rerun. No unresolved blocking finding remains in the reviewed bytes. Release build/CI and any future trial gates remain separate.

## Final clarity update and runtime smoke

Rechecked the final explicit `all_schema_fields_validated: false` coverage field, matching documentation and regression test; all 31 focused Python tests pass again. Exact final source hashes replace the earlier draft in `own-diagnostics-check/evidence.json`. Inspected real adapter-to-AdapterWorker smoke evidence for both trusted slots using the new closure and existing tutorial replay; each feedback names its expected team. Independently compared the saved old/new action-query artifacts byte-for-byte: identical. Source replay/result hashes in the smoke agree with the previously verified public input hashes. The smoke introduced zero new games.
