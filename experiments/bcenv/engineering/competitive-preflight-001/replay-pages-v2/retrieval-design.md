# Bounded replay retrieval for durable scrimmage jobs

Date: 2026-10-20. Status: implementation proposal, not an approved trial configuration.

## Goal and current state

An agent should be able to inspect actual authorized gameplay evidence, choose its own explicit round window, and continue through that window without losing rows at an upstream or downstream cap. A bounded first prefix is useful evidence but cannot serve as a paginated replay unless the missing rows remain retrievable.

The current six-tool controller includes `scrimmage_replay`, but its adapter and durable ledger always withhold replay data. The v1 projector accepts only a bounded prefix of a validated complete ReplayQuery stream. It strips private metadata and preserves six raw event kinds. It cannot retrieve rows missing from that prefix. The durable ledger stores public aggregate results and accepted source identity; it stores no replay artifact or explicit run identity. The controller's issued submission set is ephemeral. Deterministic recapture and submit can recover the same owner's same-run job, but a run-derived idempotency-key hash does not establish durable authenticated run ownership.

The intended changes preserve v1 compatibility and add explicit versioned page semantics. No new gameplay, opponent source, heldout schedule, model/provider invocation, listener, authentication mechanism, or isolation change is part of this design. Real-heldout gates remain closed. Code remains trusted-side and outside competitor runtime packages.

## Trust and limits of the result

The host must independently establish authorization, owner/run scope, source immutability, parser success and integrity, and the own-team slot. Shapes, opaque IDs and content hashes alone establish none of those properties. Parser and projector validation is not an authenticity or security boundary.

The host selects the expected public spec version from frozen job configuration. Supported versions are exactly `3.0.13` and the separately retained `2.0.3` diagnostic mode. Input must exactly match. No model-controlled version or silent pooling is allowed. Engine summaries, raw query metadata, private paths, logs, source/binary hashes, map names and opponent/package/team names remain private. The output may reveal recognizable gameplay naturally; it does not implement robot visibility or promise that behavior cannot fingerprint a bot or map.

Rows retain own/opponent slot, robot IDs, coordinates, action codes and raw targets, birth/death evidence and signed net resource changes. All sides and adverse events remain eligible. No inferred hits, causes, strategy quality, balances or gross collection are added. Within-round schema group order is presentation order, not inferred chronology.

## Six-tool interface

Keep exactly the six existing tool names. Version the replay request/response contract and freeze the registry schema/version with the controller run. The existing context hash covers system/task bytes and must not be described as already binding the tool registry.

Use strict disjoint request forms for `scrimmage_replay`:

1. `manifest`: submission ID, operation, bounded offset and limit. Returns opaque replay IDs available for that job, expected public spec, and bounded per-match observed/reported round coverage. The listing itself is paginated when a job has multiple replay artifacts. No map/opponent/backend schedule labels are returned.
2. `window`: submission ID, operation, replay ID, explicit inclusive round start/end, nullable robot ID and bounded row limit. Creates or resolves an immutable view and returns its first page. There is no hidden default round window. Initially the producer's existing all-matches, separately indexed scope is retained and stated explicitly.
3. `page`: submission ID, operation, view ID and a bounded integer record offset. The view freezes replay source identity, window, robot filter, expected spec, row/byte limits and parser/projector version. Clients cannot alter those choices on continuation.

Each call rechecks owner/run/submission/replay/view visibility. A view ID is a reference, never an authorization token. Unknown IDs, mismatched owner/run and mismatched submission/view use the same bounded not-found result. Do not leak another owner's existence through quota, deduplication or detailed error behavior.

`record_offset` counts matching records after the explicit window and robot filter, in the documented stable match/event/group/vector order. It is not a round number, source event index or file byte offset. Team resource rows remain included under robot filtering. Return the next offset only when additional matching rows exist and actual output progress has occurred.

## Genuine producer-side pagination

Introduce `bcenv.bc2023.replay-query.v2` without changing the five-argument v1 Java invocation or its shape. The explicit page invocation supplies a bounded nonnegative record offset. It parses and validates the entire source stream, including data before the offset, after the page cap and outside the requested window. Identity joins must still process initial/spawn/death data before the selected page.

Count every matching row for the entire selected window, including per-kind totals, while materializing only the requested bounded slice. Memory must not grow with the skipped offset. Round/resource coverage remains whole-window coverage, independent of page contents. Use bounded arithmetic and reject offsets beyond the actual matching count; an offset exactly equal to the count is an explicit empty terminal page. Empty windows at offset zero are valid.

The source page must report separately:

- Complete source stream and extracted-fields validation status, with all-schema validation still false.
- Explicit query, including record offset, source row limit and inclusive bounds.
- Whole-window matching count and per-kind counts.
- Source page row count and exact source page end offset.
- Whether the requested source page slice is complete, whether more matching rows remain, and whether this single page contains the entire selected window.
- Existing per-match round/resource coverage with private names excluded only by the projector.

A source row limit does not mean the source replay was incomplete. A complete last page at a nonzero offset does not mean that page contains the entire window. Unknown/corrupt/incomplete evidence fails closed. No raw replay download fallback exists.

## Projector v2 and exact progress

Add `bcenv.bc2023.replay-feedback.v2` as a separate entry point, keeping the v1 function and schema unchanged. Reuse or preserve the established nested allowlists, strict numeric/enum bounds, duplicate-key/depth checks, explicit expected-spec selection, and full validation of every supplied row before local truncation. Unsupported record kinds reject rather than silently disappearing.

V2 distinguishes three dimensions:

1. Source completeness and whole-window round/resource coverage.
2. Source page completeness and position within the complete matching sequence.
3. Released output-page completeness after local row/byte limits.

The next retrieval offset is `input record_offset + number of records actually released`, never the source page end when a local cap withheld supplied rows. The next invocation must query the immutable source at that exact offset. A nonterminal response must release at least one row; if coverage plus one required row cannot fit, fail with a bounded output-limit result instead of a zero-progress continuation loop. Whole-window empty selections remain valid zero-row terminal responses.

Validate input source page arithmetic exactly: offset lies between zero and full matching count, source rows equal the bounded remaining slice, per-kind page counts do not exceed whole-window counts, and flags/end/next offsets agree. Full-window count equality is required only if the source page actually spans the whole window. Do not compare a middle page's local counts to whole-window totals as if earlier/later rows were present.

The v1 resource checks assume a prefix. V2 must permit a page beginning at resource row index 1 or in later schema groups. It must still reject duplicate rows, order/context contradictions, missing mandatory resource rows in wholly observable groups, impossible global resource totals and visible round counts exceeding source coverage. Boundary exceptions apply only where the page genuinely starts/ends, including pages spanning matches. Whole match/round checks cannot treat unseen rows as absent. Preserve all independently checkable contradictions without inventing completeness.

Return exact coverage and fixed truncation reasons, with source-window omission distinguished from local row/byte truncation. Only whole rows are serialized. The byte cap includes the complete final encoded response, IDs and coverage. The outer controller must separately account for its entire tool envelope and cumulative output budget.

## Durable identities and ownership

Add an explicit durable run binding at job creation if the replay route needs it. Preserve deterministic same-owner/same-logical-run recapture-and-submit recovery. Do not accept a bare ID from another run, infer run ownership by reversing a key hash, or silently bind legacy jobs that lack sufficient identity.

Bind each replay registration to owner, run, submission, stable opaque job identity, terminal result identity/generation, expected spec, own slot, reviewed producer identity and a private immutable replay snapshot identity. Public replay/view handles must be independently minted opaque values. Existing `s_` submission and projector `j_` job handles need an explicit stable mapping or an explicitly versioned identity simplification; a transient worker generation is not a public job ID.

Register evidence atomically with or consistently against terminal completion. Expensive parsing may occur outside the transaction, but recheck generation, lease and source/result binding at publication. A stale worker cannot publish to a reclaimed or differently completed job. Repeat registration of identical immutable evidence may be idempotent; a different source or terminal result must conflict. Never replace an existing view's underlying evidence.

A trusted provider resolves an authorized replay ID to its privately stored source. Requests contain no filesystem path, URL, command, hash, opponent selector or hidden schedule position. A raw query prefix can be cached as one page but cannot be used to fabricate later pages.

## Immutable views, storage and CPU quotas

The smallest viable storage design persists immutable view descriptors and the authorized complete replay snapshot, rendering uncached pages from that source with a frozen producer/projector configuration. Identical view/offset requests must produce identical canonical bytes. Fail closed on source or producer drift. There is no need to persist an unbounded copy of all projected rows or an unbounded per-offset cache.

Repeated full-stream parsing has a CPU cost even when the page is small. Bound parser wall time, memory, concurrency, request rate and total reads. A later immutable cache may reduce work, but it needs explicit byte/entry quotas and eviction semantics. Never claim the page size bounds total parser work by itself.

Illustrative engineering defaults for review, not approved experiment/trial budgets:

- Inclusive round span at most 256; requested page at most 64 rows.
- Projection payload at most 12 KiB, plus an independently checked complete controller envelope under its configured 16 KiB per-tool limit.
- At most 16 views per job, 64 per owner/run, 256 globally.
- Explicit source-retention byte and artifact-count quotas, charged per owner without cross-owner deduplication discounts that disclose shared source existence.
- Existing request-rate and aggregate controller-output budgets remain enforced. A 128 KiB total-output budget may prevent enumerating an entire game in one run; exhaustion must be explicit, not a false end-of-replay marker.

Limits are host configuration and frozen with a view. Quota exhaustion must not create partial immutable descriptors, mark unseen rows absent, or grant an unlimited replay fallback. Eviction/expiry must return an explicit unavailable state, not silently switch source.

## Replay-unavailable and failure states

Use a closed bounded vocabulary, subject to the enclosing service's existing error conventions:

- `not_ready`: queued/running job has no released replay.
- `replay_not_available`: completed/rejected/failed job lacks an authorized retained source.
- `replay_withheld`: publication policy does not permit replay release.
- `invalid_evidence`: missing, changed, corrupt, incomplete or version-mismatched evidence.
- `resource_limit`: a parser, retention, view, request or output budget prevents retrieval.
- Uniform `not_found` for inaccessible or mismatched references.

Availability is separate from a successful aggregate result. No raw parser error text, logs or internal path appears in an error. An empty matching window is an available terminal page with coverage, not an unavailable replay.

## Compatibility and implementation boundaries

V1 producer, projector and always-withheld controller contracts remain stable. New schemas are explicit rather than silently extending exact-schema consumers. Ledger migration, if needed, must be versioned and documented; legacy data must not gain inferred ownership. The public rules runtime must be pinned and validated before any retained real replay query.

Producer/projector slice:

- `seasons/2023/replay/ReplayQuery.java`: explicit offset-capable v2 path, whole-stream validation/counts, v1 preservation.
- `seasons/2023/replay/ReplayQueryTest.java`: independent schema fixtures and pagination/parser regressions.
- New `services/replay_feedback_v2.py`: bounded sanitized page projection.
- New `tests/test_replay_feedback_v2.py`: strict shape/coverage/progress and adversarial tests.
- New `contracts/replay-feedback-v2.md`: exact fields, semantics, trust requirements and hard limits.
- Optional separately assigned adapter command/test changes in `seasons/2023/adapter.py` and `tests/test_replay_query.py`; do not silently change the v1 command.

Routing slice, separately owned: durable run/replay/view bindings, bounded provider invocation/storage, ledger migration, controller request/response validation and tests. It must consume the actual v2 producer, not manufacture pages from stored v1 prefixes.

## Required verification

1. Java pagination concatenation equals an independently specified full matching sequence, with no gaps or duplicates and exact per-kind whole-window counts.
2. More than 10,000 matching rows, with late adverse action/death evidence retrieved at an offset beyond the old cap. No new engine game is required: use official-schema synthetic fixtures.
3. Every offset/page boundary through small fixtures, including middle resource groups, rounds and matches; robot filtering retains both teams' resource rows.
4. Corrupt events before/after the slice, beyond the cap and outside the window reject; incomplete source never releases a partial page.
5. Source limits and local row/byte limits independently shrink pages; next offset advances by actual released rows and eventually recovers all rows. A too-small byte budget fails without a zero-progress loop.
6. Empty windows, exact EOF offsets, invalid/past-end offsets, round gaps and missing-resource coverage remain explicit and arithmetically consistent.
7. V1 serialized outputs and semantics remain unchanged; both explicitly supported spec versions work and cross-version/unsupported evidence fails.
8. Nested/string metadata injection, duplicate JSON keys, bad enums/numerics and invalid rows beyond local output caps cannot leak or be ignored.
9. Owner/run/submission/replay/view mismatches are uniform; restart recapture/resubmit recovers only the correct job; legacy unbound jobs remain unavailable.
10. Stale worker registration, contradictory terminal result, source/version/producer drift and post-registration mutation fail closed.
11. Concurrent quota/retention exhaustion and crash recovery do not create visible partial state; no unlimited cache growth or cross-owner existence leak.
12. Complete controller envelopes and aggregate budgets are enforced with unchanged six-tool names; raw bytes, paths and download URLs cannot appear.
13. A scripted controller can inspect more than one explicit window and continue pages against the one already persisted authorized public replay. Preserve originals, report counts and coverage honestly, and run zero new games or model/provider calls.

Passing these tests proves the scoped engineering behavior exercised. It does not establish authenticated deployment, adversarial isolation, trial readiness, competitive strength or authorization for any heldout replay.
