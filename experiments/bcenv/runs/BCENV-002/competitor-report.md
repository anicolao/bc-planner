# Local Battlecode 2023 lecture-opponent diagnostic

## Outcome and selection

Selected the verified standoff variant in competitor/src/mybot/RobotPlayer.java, package mybot. It passed the preregistered behavioral test and won all four paired retests. The baseline also won all four. This does not demonstrate improved win rate or tournament strength.

Eight games total, run sequentially, only the two permitted development maps. No failed builds, failed games, environment failures, installs, live network requests, replica/viewer use, or competition submissions. Initial plan was written before candidate code; one candidate modification was preregistered after baseline and before editing. Completed well within 25 minutes and 12 games; stopped on workflow completion.

| Map / candidate side | Baseline result / rounds | Standoff result / rounds | First150 close/engagement baseline → standoff |
|---|---|---|---|
| DefaultMap / A | win /372 | win /270 |12/18 →5/23|
| DefaultMap / B | win /324 | win /328 |0/0 →0/0|
| SmallElements / A | win /171 | win /171 |24/62 →17/47|
| SmallElements / B | win /190 | win /190 |14/34 →8/37|

Results and hashes: work/{baseline,standoff}-{default,small}-{A,B}/result.json and replay-summary.json. Each result identifies map, team packages, verified source/binary hashes, engine hash, process exit, and replay hash. work/evidence-index.json consolidates these identities. Every game used the same unchanged active lecture artifact, and explicit A/B reversal; automatic alternate-order was false.

## Source discovery and independence

Found the season-correct official educational source in supplied sources/catalog.json. Upstream repository https://github.com/battlecode/battlecode23-lectureplayer, commit 57063ad07b2311c21c99ba7be100a55fcdb3de6b, catalog commit time 2023-01-20T02:46:15Z, license AGPL-3.0. Verified archive SHA256 and all six Java files plus LICENSE, retrieved into work/opponents/lecture/, retained provenance.json and LICENSE outside its Java source root, and compiled/verified work/opponent-build myself. No upstream wrapper or script was run. Full provenance/limits are in work/opponents/lecture/README.md.

This establishes agreement with the trusted frozen offline mirror, not independently verified live upstream authenticity, signed Git provenance, or unaided online discovery. Opponent source was inspected for integration and behavior. Candidate strategy and implementation were independently authored, with no opponent code copied; sources and packaged candidate remain separate. Inert fixtures were not used as opponents or readiness substitutes.

## Plan and observed behavior

work/initial-plan.md records relevant rules/API checks and intended behavior before authorship. HQs register themselves, establish miners, spend mana on launchers, and after round 120 reserve 100 mana / 100 adamantium for standard anchors. Carriers use an ID-based two-thirds-mana preference, transport full 40-unit loads to their chosen HQ, and take anchors when empty and adjacent. Sensed wells and islands are shared only with permission. Launchers prioritize military targets, attack before and after movement, ignore indestructible HQs as attack targets, and patrol center/reflected-home guesses. Greedy local movement uses legal steps and a 12-position revisit penalty.

Raw first 150-round candidate action totals show actual economic/anchor activity in both versions: baseline 97 PLACE_RESOURCE events, 8 BUILD_ANCHOR, 8 PICK_UP_ANCHOR, 6 PLACE_ANCHOR; standoff 96, 8, 8, 6. This establishes activity, not gross resource quantities or mining efficiency. For example baseline DefaultA HQ 5 built an anchor round 136 / event 137 / action-row 7; carrier 10218 picked one up round 142 / event 143 / row 9 and placed one round 143 / event 144 / row 6. Raw targets are preserved without treating their encodings as coordinates unless specified by the tool.

## Preregistered experiment and evidence

work/experiments/001-preregistered.md predates variant editing; 001-change.diff shows the single focused change. For a selected visible enemy launcher already within squared 16, movement changes from approach to choosing stay/legal step closest to squared distance 13. Production, economics, anchoring, other navigation and attack selection are unchanged.

The fixed first 150-round endpoint measures candidate launcher recorded positions whose nearest opposing recorded launcher is within squared 20, and what fraction are within squared 8. It is a global geometric proxy, not reconstructed visibility or sensor knowledge. The baseline pooled result was 50/114=43.86%. Preregistered keep criteria required relative reduction>= 25%, improvement in>= 2 of 3 baseline-eligible pairs, at least 57 eligible observations, at least 272 attack events (80% of 339), and 4/4 wins. DefaultB had no baseline eligible observations and supplies no directional evidence.

Retest: 30/107=28.04%, a 36.07% relative reduction, all three eligible pairs lower. Eligible observations 107 >= 57, LAUNCH_ATTACK events 342 >= 272, wins 4/4. Thus all predefined criteria passed; keep standoff. work/baseline-analysis.json, work/standoff-analysis.json and unchanged analysis script work/analyze.py provide calculations. Descriptive first 150 launcher deaths fell 5→3, but death causes are not established and survival was not the preregistered endpoint. Attack events are not successful-hit/damage counts.

Bounded raw queries: each game has three inclusive windows 1–50, 51–100, 101–150, each limit 10000, under work/query-{version}-{condition}-{start}-{end}/. All 24 returned selections are untruncated and complete, source streams complete, all requested positive rounds present. Each query-result.json/replay-query.json records hashes, coverage and original event/vector indexes. An extra baseline DefaultA 1–30 query is retained. Robot-specific SmallA 100–110 queries, limit 1000, each returned 41/41 records with full coverage, directly inspect candidate 10057.

Important negative evidence: robot 10057 in SmallA died round 105 / event 106 / death-row 0 in BOTH versions. Its recorded distances from opponent 10155 at rounds 102/103/104 were 4/4/1 baseline versus 4/5/2 standoff. The standoff implementation modestly separated this pair without saving that robot. This refutes any blanket story that range discipline always prevents deaths. DefaultB became four rounds slower (324→328); Small map finish times were unchanged. Faster DefaultA completion alone is not proof of the proposed mechanism.

Terminology clarification: the preregistration mentions “end-round” vectors. The justified measurement is per-round recorded positions, exactly as work/analyze.py computes. No temporal ordering between movement/action/death vectors within a round is inferred, and currents may affect positions. No endpoint or analysis was changed in response to outcomes.

## Correctness review, assumptions and unresolved defects

- Official Java8 compiler and BC23 verifier accepted both candidates and the opponent. Every game process exited 0 with completed replay/footer and valid extracted fields. Verifier acceptance is evidence of allowed bytecode/API usage, not proof of game-logic correctness.
- Uses only battlecode.common, plain Java and allowed stdout for caught exceptions. Infinite loop and finally/yield maintain liveness. Each mutating game action is immediately gated by its can* check. Broad per-turn Exception catch preserves turns, but stdout is disabled by the pinned run configuration: these games DO NOT establish exception-free execution. Bytecode overruns/resumption remain unprofiled.
- Shared slots 0–3 HQ, 8–11 adamantium, 12–15 mana, 21–55 islands are disjoint and within 64. Map sizes <=60 guarantee location encoding 1..3600, plus ownership flags <=11792, within 65535. Island id <=35 is assumed from supplied rules. Per-robot statics are not shared; communication uses the actual shared array.
- Carrier action/capacity guards, positive transfer amounts, collect(-1), neutral-island checks before placement and empty-anchor pickup prevent obvious invalid state transitions. Every record is side-scoped; robot IDs are never assumed persistent between games. The illustrative same ID comparison is independently identified in each corresponding replay.
- Lifetime carrier-production cap does not replace attrition after eight; this is an unresolved strategic defect. Initial HQ association can bind the nearest already registered HQ, not necessarily the spawning HQ. Stockpiling anchor policy can inhibit military production and overproduce anchors after nearby neutral islands are exhausted.
- Greedy navigation is incomplete, lacks persistent terrain/current modeling, and can oscillate or fail at congestion/obstacles. No complete search, island reachability proof, enemy-HQ symmetry inference, carrier retreat or coordinated army control. Standoff optimizes one selected enemy, ignoring other launcher threats; stay scoring does not fully model HQ/current hazards. These are known limitations, not repaired after evaluation.
- Wells/island broadcasts have no timestamps and may be stale. Carrier well memory is sticky and does not explicitly handle a well changing resource type. Distant carriers may lack write permission; anchor exploration can revisit known or unreachable goals. Empty carriers away from HQ do not proactively return just to pick up newly produced anchors.
- Only two known development maps, one educational opponent revision, one deterministic run per condition, no held-out maps/seeds, no confidence interval or independent replicates. Aggregate robot-rounds are dependent and denominator changes may reflect population/trajectory changes. Educational source has its own limitations; success here establishes local integration and this bounded behavioral observation, not general strategy quality.

## Deliverables and reproduction

Selected verified build work/standoff-build; source aggregate a469c308c9923869056eb6cb4d838a3057d33f5bfaa7cb13c49d1a06f96901d5, binary aggregate d648c82e433402e21cee1b623e3a3a4048d4c33a92e69e109db2e764638db377. Packaged source work/selected-package/source.zip, SHA256 c03da311741fc725f7f130db2b6a2c403ab55c5c31b39b4181ac4e4433ad77f6; package.json links source/binary/engine identities. ZIP contains only mybot/RobotPlayer.java, checked byte-for-byte against selected verified source and competitor/src. Baseline verified source/artifacts, raw queries, negative examples and superseded code are preserved. No failed attempt was deleted (none occurred).

Commands: work/commands.log (late-entered invocations explicitly labeled) and exact compiler/engine commands in immutable artifact/result JSON. To reproduce, run from this assigned workspace using ../../bcenv, use a NEW output path on every invocation, build the separate lecture and mybot source roots, then explicitly swap --team-a and --team-b on the two permitted map paths. Reusable data analysis is python3 work/analyze.py {baseline|standoff}. No pinned runtime/tools/maps/rules/catalog were modified.
