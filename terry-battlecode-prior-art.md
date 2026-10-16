# Terry Van Belle's Battlecode implementation: what to reuse

**Status:** Research proposal, 2026-10-16. Static source inspection; no matches, remote jobs, opponent downloads, or competition submissions were run. This document proposes implementation work, not a completed integration.

## Recommendation

Use Terry's projects as reference implementations for the **measurement and replay layer** of our [learning architecture](battlecode-learning-architecture.md). Start with one season adapter, one immutable match bundle, and one replay-grounded experiment. Do not start by importing the multi-agent deployment or resuming the remote-access experiments.

The most valuable contribution is the failure record: mechanisms that never executed, measurements attached to the wrong bot, misleading engine inspection, co-adaptation to weak opponents, and operational failures in shared workspaces. Automating those failure checks is more useful than copying a large strategy or a fixed acceptance threshold.

## Attribution, scope, and source boundary

Terry is **Terry Van Belle**, GitHub account `terryvanbelle`. Attribution was established from the Terry section of bcenv's [historical review](https://github.com/anicolao/bcenv/blob/7f868dc561667a336e7eeba65ea89167d7716fa1/HISTORICAL_LEARNINGS.md#terry-van-belles-agentic-battlecode-projects), then cross-checked against the public repositories and their sister-project links. `anicolao/battlecode-2026` is a different predecessor: Terry's BC26 [benchmark manifest][26-benchmark] names it as an opponent. It is not Terry's implementation.

Public visibility and default-branch revisions were checked with GitHub CLI on 2026-10-16:

| Project | Inspected revision | Role |
| --- | --- | --- |
| [battlecode22-vibe][22-root] | `b1d36b4d82f931b37385e45e87eeecf92df54782` | Single-lineage development; Python replay state reconstruction and ASCII rendering |
| [battlecode26-vibe][26-root] | `f8b127aeabc65a7875c6da3dcc6e79a5fb170a02` | Java replay diagnostics, paired gauntlets, independent benchmark opponents |
| [battlecode25-vibe][25-root] | `9713f08052a6791bb6402fa17740814004615d43` | More developed measurement doctrine, experiment identity, multiple lineages and recovery tooling |

The 22 and 26 revisions match the earlier bcenv review; BC25 has advanced beyond its September 11 snapshot. In particular, its [protocol][25-multi] records that Alice and Carol were retired on September 14 and Darla became the only live lineage. Its headline introduction still describes three agents. Treat the dated amendment as history of the actual operating plan, and do not present the original topology as its current state.

Season numbers name the rulesets, not proof of contemporary tournament participation. Repository results below are self-reported local measurements. This review neither reproduces them nor establishes autonomous tournament success. Source files are evidence of an implementation; instructions describe intended behavior and do not prove compliance.

## Implementation map

| Responsibility in bc-planner | Prior art | Reuse decision |
| --- | --- | --- |
| Season and engine identity | BC25 [engine-jar.sh][25-engine] resolves the engine version from the pin instead of selecting an arbitrary cached JAR | Adopt the invariant; strengthen to digest-pinned engine and dependencies |
| Replay and state inspection | BC22 Python reconstruction; BC26 Java extractor using generated engine classes | Best starting points for a season adapter, with explicit completeness and schema checks |
| Match execution | BC25 [tournament.sh][25-tournament] exports committed sources, compiles bots separately, runs both sides, retains results | Reimplement behind a local executor contract; do not carry over cloud wrappers |
| Experiment identity | BC25 [bot_identity.py][25-identity] identifies a workspace bot at run launch | Adopt launch-time identity; extend beyond normalized Java source |
| Evaluator | BC26 [compare_gauntlets.py][26-compare] pairs opponent/map/side results | Retain paired comparison, add strict manifest and missing-job validation |
| Agent learning and memory | BC25 [training algorithm][25-training], [methods][25-methods], [protocol][25-multi] | Convert important prose obligations into machine-checkable records and gates |
| Coordinator recovery | BC25 [watchdog][25-watchdog] is external to the model session | Adopt independent liveness observation, not tmux keystroke recovery |

## What the learning loop actually teaches

### 1. Validate the instrument before interpreting the strategy

The [engine resolver][25-engine] documents a concrete failure: an old JAR in a shared cache produced false engine conclusions. Its implementation selects the version from `arena/engine_version.txt`, errors if absent, and includes a test-only override so testing does not alter the shared pin. This is a useful fail-closed pattern. It still locates a filename rather than checking a cryptographic artifact digest; filename agreement alone is not our desired engine identity.

The [training procedure][25-training] calls for early engine probes, triggered API-coverage checks, bytecode monitoring, and confirmation that a candidate code path actually runs. Adopt those as recorded checks. Do not inherit its cadence or numerical promotion rules as season-independent truths. An API name being used is not evidence of strategically correct use; instrument activation and expected behavior separately.

### 2. Preserve our two gates

Terry's procedure distinguishes local mechanism checks, paired comparisons, ablations and frozen-roster evaluation. It also records examples where mechanisms improved without converting into wins. This supports our separate **behavioral gate** and **competitive gate**. A positive score without the preregistered behavioral change is unexplained evidence, not validation of the original hypothesis.

The BC25 [objective revision][25-objective] explicitly changes the goal from beating the other live lineage to absolute strength. Its [benchmark history][25-history] now records Darla's best `v3` result as 84/150 (56%), but a best `TSPAARKHS` result of 1/150. Crucially, that file lists **record-setting complete runs only**. It is neither a complete chronological performance curve nor a controlled estimate of how much each accepted change helped. Inspect the per-run records before making progress claims.

A fixed opponent pool measures progress relative to that pool. Independent opponents reduce shared-lineage blind spots; repeatedly studying their scores or replays can still turn them into development data. Reserve a separately governed holdout if we want final generalization evidence. BC26 allows benchmark replay analysis, whereas BC25's later objective limits lineages to coordinator-produced benchmark scores. Those are different experimental policies, not a single reusable access rule.

### 3. Determinism changes sampling, not the need for validation

The [training algorithm][25-training] argues against repeating identical deterministic games as if they were independent evidence. Verify determinism for our exact engine, map, seed and runtime first. Then expand map/opponent coverage rather than count duplicate runs as extra samples. Retain repeated runs as an integrity test when needed. Paired sides control some positional effects; they do not guarantee balanced maps or statistical independence.

The BC26 [comparison script][26-compare] indexes results by `(opponent, map, bot_side)` and uses only the intersection. It does not validate engine versions or seeds; duplicate keys overwrite earlier rows. For our evaluator, duplicate scenario keys should be errors, missing jobs should remain visible, and comparisons should require a compatible evaluation manifest. Its round delta is a useful diagnostic, but surviving longer can reflect inactivity rather than better play.

### 4. Durable experiment state matters more than long agent context

The BC25 [multi-agent protocol][25-multi] uses cold-start summaries, closure maps, unfinished run IDs and explicit reopening conditions. Its [training procedure][25-training] preserves rejected and void iterations, preregistration, unfinished checks, and superseded claims. Adopt a compact structured state record with evidence pointers rather than requiring a worker to read an enormous chronological log on every restart.

A lesson should carry its engine revision, bot architecture, opponent distribution and measurement. A failure on another lineage is a useful prior, not a universal prohibition. Store the reason a closed avenue may be reopened, and distinguish a corrected explanation from the original observation it reinterprets.

## Replay implementation: the most direct reuse opportunity

### BC22: reconstructed round state, not decision-time knowledge

The [Python decoder][22-decoder] supports raw or gzipped FlatBuffers, match selection, round windows/stride, ASCII boards, terrain, moves, health, mining and indicators. Its CSV metrics include resources, unit counts, Archon health, attacks and soldier centroid/spread. Terrain/resource reconstruction applies resource deltas, Vortex to rubble, and inferred lead regeneration. This is a useful starting point for offline diagnostics.

Its robot model is deliberately partial: ID, team, type, position and HP, without complete levels, modes, cooldowns or knowledge. Prototype health is documented as unmodeled. Rendering combines end-of-round state with events grouped by category, so it cannot establish the exact information available at an intra-round decision. The CSV includes the eventual winner on each row: appropriate as an analysis label, but direct future-information leakage if mistakenly treated as a planner observation.

The [tests][22-tests] build a synthetic four-round replay and cover reconstruction, resources, deaths, regeneration and Vortex. The optional real-replay test searches `matches/`, while tracked examples are under `replays/`; these examples are not automatically exercised by that discovery path. Metrics need explicit expected-value tests. Nonzero map origins also deserve a regression: movement coordinates are normalized against the origin, whereas resource-drop indexing follows a different path. This is a validation risk, not a reproduced defect.

### BC26: better event detail, but lossy and tightly schema-coupled

The actual [Java source][26-decoder] is more capable than its [README][26-replay-readme]: it has robot tracking, round windows, initial-terrain neighborhoods, per-team turn facts including idle turns, and events for traps, grabs/throws, cheese, squeaks and collisions as well as damage and deaths. The README still says there is no test suite and lists implemented events as omitted. Inspect code and tests at the same revision.

It is not a lossless event API. Some actions print only a name, unknown types are silently omitted, and indicator output keeps only strings containing `OVERRAN` or `near-limit`. Team filtering selects whose turns print; it does not restrict facts to that robot's legal vision. Aggregates usually appear every 25 rounds. Our adapter should preserve raw typed events before generating summaries, report unsupported actions explicitly, and label the view as omniscient diagnostics.

The decoder manually traverses an action-union vector using vtable slot 26, splits a combined kings/cheese field using division and remainder by 10, and decodes packed locations using map width. Those conventions require validation against the exact official engine/schema; printing `specVersion` is not schema validation. Static robot labels and cooperation state are not reset on each MatchHeader, creating a multi-match isolation risk. A cooperation value at the start of a requested window should not be reported as a newly observed transition.

The [test file][26-tests] contains useful window-label, grab/throw and turn regressions. However, its default replay path is absent from this checkout; tests need an explicit fixture setup. Some assertions recheck decoder arithmetic rather than an independent oracle, and trap-removal coverage permits zero removals. Add multi-match, empty-event, malformed-vector, decompression-bound and unknown-schema fixtures, plus real replays checked against the official client. Neither decoder currently establishes a bounded, hardened parser for arbitrary uploaded input.

### Integration implication

Separate three layers: native replay decoding; versioned reconstructed state and derived metrics; agent queries and renderers. Preserve match/round/turn ordering and event offsets across all three. A query result should identify whether it is raw, reconstructed or inferred, and whether it is omniscient or legally observable. Bot decision reasons require contemporaneous telemetry or must remain unknown. This separation is the key missing piece between Terry's useful debugging tools and our proposed learning interface.

## Runner and orchestration: useful patterns, unsafe assumptions to avoid

BC25's [tournament script][25-tournament] has thoughtful protections: a run lock, separate compile checks, explicit forfeits, paired sides, concurrency limits, and a private copy of the executing shell script. These address real shared-workspace failure modes.

There are remaining boundaries we should improve:

- Source export repeatedly resolves `HEAD`; per-bot attribution is collected afterward. A concurrent commit can make the recorded metadata disagree with an earlier export. Resolve one revision once and export all inputs from it; hash the exported bundle.
- Copying the shell script does not freeze sourced helpers, map files, engine artifacts, or bot data. Freeze the entire execution bundle before dispatch.
- The runner extracts results from text and permits failed Java invocations to continue to parsing. Distinguish process failure, missing result, invalid replay, compile forfeit, timeout and legitimate game loss in typed output.
- [bot_identity.py][25-identity] normalizes package declarations and hashes Java content to identify equivalent snapshots. This is a good human-facing label, not a complete execution hash: it omits engine, maps, classpath, resources, tool versions and runtime flags. Preserve both semantic label and full bundle identity.
- The [shared helpers][25-lib] embed Terry's GCE project and SSH assumptions, can start a VM, and disable host-key checking. Do not execute or transplant these wrappers. Our first adapter should run in the chosen workspace without remote access or changes to security settings.
- The [watchdog][25-watchdog] uses a lock, heartbeat age and cooldown outside the model session, but recovery nudges a tmux session and launches a CLI with permission bypass. Do not copy that recovery path. Use an authorized process supervisor, one coordinator lease, explicit job states and idempotent reconciliation. A nudge sent is not evidence that a job resumed.
- The protocol's information barriers are research rules, not demonstrated security isolation. Shared working trees, generated scripts and process metadata can leak strategic information. If independent lineages later matter, give each isolated storage and expose only explicitly allowed results.

## Proposed integration contract

These are proposed interfaces, not features already implemented:

1. **Season bundle:** season, official engine origin/revision/digest, replay schema revision, dependency lock, runtime flags, rules version, maps and their hashes.
2. **Match manifest:** stable run/scenario IDs, baseline/candidate and opponent bundle hashes, map, sides, seed semantics, resource limits, expected artifacts, timestamps and terminal status.
3. **Replay query:** match ID plus turn range, unit IDs, area or event filters. Return structured observations, source-event offsets, schema/decoder version, completeness warnings and perspective. Render ASCII or images as views of those same observations.
4. **Decision trace:** match/turn/unit/source revision plus observed inputs, chosen action and policy branch where legal. Missing reasons remain unknown; an omniscient replay must not be labeled as the bot's observation.
5. **Experiment record:** immutable hypothesis, predicted change, disconfirmation criterion, exact code diff, mechanism measurement, paired competitive results, missing jobs, costs, decision and evidence references.
6. **Claim ledger:** observed / inferred / unknown, scope, source pointers, supersedes relationship and reopening condition. Retain rejected and inconclusive candidates.

## Smallest useful implementation sequence

| Step | Deliverable | Acceptance evidence |
| --- | --- | --- |
| 1. Select a season and inspect reuse permissions | Pin official engine, schema, dependencies and source boundaries | Every execution input has an origin and immutable identity; rights for copied files are checked |
| 2. Run one baseline match locally | Immutable manifest, logs, native replay, authoritative result | Re-run verifies determinism or explicitly records variation; no remote access required |
| 3. Implement one replay adapter | Structured turn/unit/event queries plus spatial rendering | Synthetic cases and a real replay cross-check against the official viewer; unsupported events are visible |
| 4. Diagnose one failure | Evidence-linked observation and hypothesis | Reviewer can trace claims to exact replay events and distinguish bot-visible information |
| 5. Implement one bounded change | Candidate bundle and preregistered behavioral measurement | Mechanism executes; behavior changes as predicted or hypothesis is rejected |
| 6. Evaluate and preserve | Matched comparison, missing-job audit, decision and replay links | Both gates reported separately; artifacts identify exactly what played |

Only after this works should we add parallel agents, remote runners, watchdogs or periodic tournaments. Remote access is not a prerequisite for this research branch or a local replay prototype.

## Reuse and verification limits

BC22 and BC26 each include a root [AGPL-3.0][22-license] [license text][26-license]. In BC25, this inspection found a license under `scaffold/`, but no root license covering all original project tools. Public visibility alone does not establish permission to copy every file. This branch contains analysis and source links, not imported implementation. Check file-level provenance and applicable permissions before vendoring, and keep original notices where required. No legal compatibility conclusion is made here.

We have not run Terry's tests, replay decoders, engine or cloud scripts; reproduced benchmark scores; measured costs; verified tournament eligibility; or established full bot-visible observation reconstruction. The source audit identifies promising components and specific validation work, not a deployable system.

## Pinned source index

All links below refer to inspected immutable snapshots.

[22-root]: https://github.com/terryvanbelle/battlecode22-vibe/tree/b1d36b4d82f931b37385e45e87eeecf92df54782/
[26-root]: https://github.com/terryvanbelle/battlecode26-vibe/tree/f8b127aeabc65a7875c6da3dcc6e79a5fb170a02/
[25-root]: https://github.com/terryvanbelle/battlecode25-vibe/tree/9713f08052a6791bb6402fa17740814004615d43/
[26-benchmark]: https://github.com/terryvanbelle/battlecode26-vibe/blob/f8b127aeabc65a7875c6da3dcc6e79a5fb170a02/BENCHMARK.md
[25-multi]: https://github.com/terryvanbelle/battlecode25-vibe/blob/9713f08052a6791bb6402fa17740814004615d43/MULTI_AGENT.md
[25-engine]: https://github.com/terryvanbelle/battlecode25-vibe/blob/9713f08052a6791bb6402fa17740814004615d43/tools/engine-jar.sh
[25-tournament]: https://github.com/terryvanbelle/battlecode25-vibe/blob/9713f08052a6791bb6402fa17740814004615d43/tools/tournament.sh
[25-identity]: https://github.com/terryvanbelle/battlecode25-vibe/blob/9713f08052a6791bb6402fa17740814004615d43/tools/bot_identity.py
[26-compare]: https://github.com/terryvanbelle/battlecode26-vibe/blob/f8b127aeabc65a7875c6da3dcc6e79a5fb170a02/tools/compare_gauntlets.py
[25-training]: https://github.com/terryvanbelle/battlecode25-vibe/blob/9713f08052a6791bb6402fa17740814004615d43/TRAINING_ALGORITHM.md
[25-methods]: https://github.com/terryvanbelle/battlecode25-vibe/blob/9713f08052a6791bb6402fa17740814004615d43/METHODS.md
[25-watchdog]: https://github.com/terryvanbelle/battlecode25-vibe/blob/9713f08052a6791bb6402fa17740814004615d43/tools/agent-watchdog.sh
[25-objective]: https://github.com/terryvanbelle/battlecode25-vibe/blob/9713f08052a6791bb6402fa17740814004615d43/OBJECTIVE.md
[25-history]: https://github.com/terryvanbelle/battlecode25-vibe/blob/9713f08052a6791bb6402fa17740814004615d43/benchmarks/HISTORY.md
[25-lib]: https://github.com/terryvanbelle/battlecode25-vibe/blob/9713f08052a6791bb6402fa17740814004615d43/tools/lib.sh
[22-decoder]: https://github.com/terryvanbelle/battlecode22-vibe/blob/b1d36b4d82f931b37385e45e87eeecf92df54782/tools/bc22_replay.py
[22-tests]: https://github.com/terryvanbelle/battlecode22-vibe/blob/b1d36b4d82f931b37385e45e87eeecf92df54782/tools/test_bc22_replay.py
[26-decoder]: https://github.com/terryvanbelle/battlecode26-vibe/blob/f8b127aeabc65a7875c6da3dcc6e79a5fb170a02/tools/replaydump/ReplayDump.java
[26-tests]: https://github.com/terryvanbelle/battlecode26-vibe/blob/f8b127aeabc65a7875c6da3dcc6e79a5fb170a02/tools/test_replaydump.py
[26-replay-readme]: https://github.com/terryvanbelle/battlecode26-vibe/blob/f8b127aeabc65a7875c6da3dcc6e79a5fb170a02/tools/README.md
[22-license]: https://github.com/terryvanbelle/battlecode22-vibe/blob/b1d36b4d82f931b37385e45e87eeecf92df54782/LICENSE
[26-license]: https://github.com/terryvanbelle/battlecode26-vibe/blob/f8b127aeabc65a7875c6da3dcc6e79a5fb170a02/LICENSE
