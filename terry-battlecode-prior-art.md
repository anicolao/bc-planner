# Terry Van Belle's Battlecode implementations: findings and learnings

**Status:** Source review, 2026-10-16. Static source inspection; no matches, remote jobs, opponent downloads, or competition submissions were run. This document records observations, lessons and limitations from Terry's systems. It does not select bc-planner's architecture or define implementation work.

## Summary of findings

The inspected projects contain replay inspection tools, paired match evaluation, experiment records, and agent coordination procedures. Their failure records describe mechanisms that never executed, measurements attached to the wrong bot, misleading engine inspection, co-adaptation to weak opponents, and operational failures in shared workspaces. These records provide context for interpreting the implementations and their reported results.

## Attribution, scope, and source boundary

Terry is **Terry Van Belle**, GitHub account `terryvanbelle`. Attribution was established from the Terry section of bcenv's [historical review](https://github.com/anicolao/bcenv/blob/7f868dc561667a336e7eeba65ea89167d7716fa1/HISTORICAL_LEARNINGS.md#terry-van-belles-agentic-battlecode-projects), then cross-checked against the public repositories and their sister-project links. `anicolao/battlecode-2026` is a different predecessor: Terry's BC26 [benchmark manifest][26-benchmark] names it as an opponent. It is not Terry's implementation.

Public visibility and default-branch revisions were checked with GitHub CLI on 2026-10-16:

| Project | Inspected revision | Role |
| --- | --- | --- |
| [battlecode22-vibe][22-root] | `b1d36b4d82f931b37385e45e87eeecf92df54782` | Single-lineage development; Python replay state reconstruction and ASCII rendering |
| [battlecode26-vibe][26-root] | `f8b127aeabc65a7875c6da3dcc6e79a5fb170a02` | Java replay diagnostics, paired gauntlets, independent benchmark opponents |
| [battlecode25-vibe][25-root] | `9713f08052a6791bb6402fa17740814004615d43` | More developed measurement doctrine, experiment identity, multiple lineages and recovery tooling |

The 22 and 26 revisions match the earlier bcenv review; BC25 has advanced beyond its September 11 snapshot. In particular, its [protocol][25-multi] records that Alice and Carol were retired on September 14 and Darla became the only live lineage. Its headline introduction still describes three agents. The dated amendment describes a later operating plan than the headline introduction; actual process state was not independently observed.

Season numbers name the rulesets, not proof of contemporary tournament participation. Repository results below are self-reported local measurements. This review neither reproduces them nor establishes autonomous tournament success. Source files are evidence of an implementation; instructions describe intended behavior and do not prove compliance.

## Observed components

| Responsibility | Inspected implementation | Observation |
| --- | --- | --- |
| Engine selection | BC25 [engine-jar.sh][25-engine] | Resolves the engine version from a pin rather than selecting an arbitrary cached JAR |
| Replay and state inspection | BC22 Python reconstruction; BC26 Java extractor | Different levels of reconstruction and event detail, with season-specific assumptions |
| Match execution | BC25 [tournament.sh][25-tournament] | Exports committed sources, compiles bots separately, runs both sides, and retains results |
| Experiment identity | BC25 [bot_identity.py][25-identity] | Identifies a workspace bot at run launch using normalized Java source |
| Evaluation | BC26 [compare_gauntlets.py][26-compare] | Pairs results by opponent, map and side |
| Agent learning and memory | BC25 [training algorithm][25-training], [methods][25-methods], [protocol][25-multi] | Documents experiment procedures, preserved state and information-sharing rules |
| Coordinator recovery | BC25 [watchdog][25-watchdog] | Observes liveness outside the model session and attempts terminal-based recovery |

## Learning-loop observations

### 1. Instrument errors can invalidate strategy conclusions

The [engine resolver][25-engine] documents a concrete failure: an old JAR in a shared cache produced false engine conclusions. Its implementation selects the version from `arena/engine_version.txt`, errors if absent, and includes a test-only override so testing does not alter the shared pin. This is a useful fail-closed pattern. It still locates a filename rather than checking a cryptographic artifact digest; filename agreement alone does not establish artifact identity.

The [training procedure][25-training] calls for early engine probes, triggered API-coverage checks, bytecode monitoring, and confirmation that a candidate code path actually runs. Its cadence and numerical promotion rules are specific to that procedure, not demonstrated season-independent results. API usage alone does not establish strategically correct behavior.

### 2. Mechanism evidence and competitive results are distinct

Terry's procedure distinguishes local mechanism checks, paired comparisons, ablations and frozen-roster evaluation. It also records examples where mechanisms improved without converting into wins. The distinction illustrates why a positive competitive score alone does not validate the hypothesized mechanism.

The BC25 [objective revision][25-objective] explicitly changes the goal from beating the other live lineage to absolute strength. Its [benchmark history][25-history] now records Darla's best `v3` result as 84/150 (56%), but a best `TSPAARKHS` result of 1/150. Crucially, that file lists **record-setting complete runs only**. It is neither a complete chronological performance curve nor a controlled estimate of how much each accepted change helped. The summary alone does not establish the contribution of individual changes.

A fixed opponent pool measures progress relative to that pool. Independent opponents reduce shared-lineage blind spots; repeatedly studying their scores or replays can still turn them into development data. The inspected scores alone do not establish generalization to unseen opponents. BC26 allows benchmark replay analysis, whereas BC25's later objective limits lineages to coordinator-produced benchmark scores. Those are different experimental policies, not a single reusable access rule.

### 3. Determinism changes sampling, not the need for validation

The [training algorithm][25-training] argues against repeating identical deterministic games as if they were independent evidence. This review did not test determinism for any engine, map, seed or runtime. Under the stated deterministic assumption, repeated identical games do not add independent samples, although they can expose execution inconsistencies. Paired sides control some positional effects; they do not guarantee balanced maps or statistical independence.

The BC26 [comparison script][26-compare] indexes results by `(opponent, map, bot_side)` and uses only the intersection. It does not validate engine versions or seeds; duplicate keys overwrite earlier rows. Consequently, its output can conceal duplicate rows or unpaired jobs and does not itself establish compatible execution conditions. Its round delta is a useful diagnostic, but surviving longer can reflect inactivity rather than better play.

### 4. Experiment state persists outside model sessions

The BC25 [multi-agent protocol][25-multi] uses cold-start summaries, closure maps, unfinished run IDs and explicit reopening conditions. Its [training procedure][25-training] preserves rejected and void iterations, preregistration, unfinished checks, and superseded claims. These records externalize state beyond a single model session; this inspection did not measure their effect on restart reliability.

The records distinguish closed avenues, reopening conditions and superseded claims. Their conclusions remain conditional on the engine, bot architecture, opponents and measurements involved; a failure in one lineage does not establish a universal limitation.

## Replay implementations

### BC22: reconstructed round state, not decision-time knowledge

The [Python decoder][22-decoder] supports raw or gzipped FlatBuffers, match selection, round windows/stride, ASCII boards, terrain, moves, health, mining and indicators. Its CSV metrics include resources, unit counts, Archon health, attacks and soldier centroid/spread. Terrain/resource reconstruction applies resource deltas, Vortex to rubble, and inferred lead regeneration. These are offline diagnostic capabilities.

Its robot model is deliberately partial: ID, team, type, position and HP, without complete levels, modes, cooldowns or knowledge. Prototype health is documented as unmodeled. Rendering combines end-of-round state with events grouped by category, so it cannot establish the exact information available at an intra-round decision. The CSV includes the eventual winner on each row: appropriate as an analysis label, but direct future-information leakage if mistakenly treated as a planner observation.

The [tests][22-tests] build a synthetic four-round replay and cover reconstruction, resources, deaths, regeneration and Vortex. The optional real-replay test searches `matches/`, while tracked examples are under `replays/`; these examples are not automatically exercised by that discovery path. This inspection did not establish independent expected-value coverage for every metric. Nonzero map origins present an additional uncertainty: movement coordinates are normalized against the origin, whereas resource-drop indexing follows a different path. This is a validation risk, not a reproduced defect.

### BC26: better event detail, but lossy and tightly schema-coupled

The actual [Java source][26-decoder] is more capable than its [README][26-replay-readme]: it has robot tracking, round windows, initial-terrain neighborhoods, per-team turn facts including idle turns, and events for traps, grabs/throws, cheese, squeaks and collisions as well as damage and deaths. The README still says there is no test suite and lists implemented events as omitted. The source and tests at this revision therefore describe more functionality than that README.

It is not a lossless event API. Some actions print only a name, unknown types are silently omitted, and indicator output keeps only strings containing `OVERRAN` or `near-limit`. Team filtering selects whose turns print; it does not restrict facts to that robot's legal vision. Aggregates usually appear every 25 rounds. The printed output is a selective, omniscient diagnostic view rather than a complete event stream or a bot-visible observation record.

The decoder manually traverses an action-union vector using vtable slot 26, splits a combined kings/cheese field using division and remainder by 10, and decodes packed locations using map width. This review did not independently validate those conventions against the official engine/schema; printing `specVersion` does not itself validate them. Static robot labels and cooperation state are not reset on each MatchHeader, creating a multi-match isolation risk. A cooperation value at the start of a requested window does not by itself establish a transition within that window.

The [test file][26-tests] contains useful window-label, grab/throw and turn regressions. However, its default replay path is absent from this checkout; the default test invocation therefore lacks that fixture in the inspected checkout. Some assertions recheck decoder arithmetic rather than an independent oracle, and trap-removal coverage permits zero removals. This inspection did not establish coverage of multi-match isolation, empty events, malformed vectors, decompression bounds or unknown schemas, or independent real-replay agreement with the official client. Neither decoder currently establishes a bounded, hardened parser for arbitrary uploaded input.

### Limits of replay evidence

The inspected tools combine native replay fields, reconstructed state, derived metrics and rendered output. These have different evidentiary limits: inferred state is not a raw event, and omniscient replay information is not necessarily legally visible to a bot. Bot decision reasons cannot be established from replay outcomes alone when contemporaneous decision telemetry is absent.

## Runner and orchestration findings

BC25's [tournament script][25-tournament] has thoughtful protections: a run lock, separate compile checks, explicit forfeits, paired sides, concurrency limits, and a private copy of the executing shell script. These address real shared-workspace failure modes.

Static inspection also identified these boundaries:

- Source export repeatedly resolves `HEAD`; per-bot attribution is collected afterward. A concurrent commit can make the recorded metadata disagree with an earlier export. This is a potential attribution race; it was not reproduced here.
- Copying the shell script does not freeze sourced helpers, map files, engine artifacts, or bot data. The script copy alone therefore does not establish immutable execution inputs.
- The runner extracts results from text and permits failed Java invocations to continue to parsing. Continuing to text parsing after a process failure limits what a parsed result alone proves about execution success.
- [bot_identity.py][25-identity] normalizes package declarations and hashes Java content to identify equivalent snapshots. This is a good human-facing label, not a complete execution hash: it omits engine, maps, classpath, resources, tool versions and runtime flags. Equivalent normalized source labels therefore do not prove equivalent execution environments.
- The [shared helpers][25-lib] embed Terry's GCE project and SSH assumptions, can start a VM, and disable host-key checking. The helpers depend on Terry-specific infrastructure and security assumptions. They were not executed in this review.
- The [watchdog][25-watchdog] uses a lock, heartbeat age and cooldown outside the model session, but recovery nudges a tmux session and launches a CLI with permission bypass. That recovery path is coupled to a terminal session and its authorization model. A nudge sent is not evidence that a job resumed.
- The protocol's information barriers are research rules, not demonstrated security isolation. Shared working trees, generated scripts and process metadata can leak strategic information. The prose barriers alone do not establish independent-lineage isolation.

## Licensing and verification limits

BC22 and BC26 each include a root [AGPL-3.0][22-license] [license text][26-license]. In BC25, this inspection found a license under `scaffold/`, but no root license covering all original project tools. Public visibility alone does not establish permission to copy every file. This branch contains analysis and source links, not imported implementation. File-level reuse permissions beyond the observed license texts were not established. No legal compatibility conclusion is made here.

We have not run Terry's tests, replay decoders, engine or cloud scripts; reproduced benchmark scores; measured costs; verified tournament eligibility; or established full bot-visible observation reconstruction. The source audit establishes observations about the inspected snapshots, with the uncertainties described above; it does not establish a deployable system or prescribe future work.

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
