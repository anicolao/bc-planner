# BCENV-007 blind frozen review

Fixed2026-10-22 08:58 UTC before any evaluator scores/material were shared with this reviewer. Scope: stopped candidate source/tests, public development service audit/receipts/replays, final report and fixed-input inventory. No private evaluator source, schedule or outcome inspected. No feedback supplied to candidate; no frozen file modified.

Selected submission s_0bee2d14d8904e82acf94ef6ef0fb8b5, service source a049472f068333e355a69c3d2f4aae5d9c1d909b28c4a074fdc7d05bdc6a495f. Current source, final verified build snapshot and accepted service source independently compared byte-identical. All55 fixed input hashes unchanged.

## 1. Observable reasoning and prospective provenance — strong, bounded

Eight notes/eight submissions/eight completions;23 result polls and20 delivered replay requests. Independently checked every note precedes its submission and binds identical source/note hashes;15 note replay-reference links all predate respective notes. Notes contain falsifiable expected events/windows, explicit risks and caveats. Pending older results are acknowledged rather than invented. Receipt order establishes provenance, not soundness or native access compliance. No hidden reasoning assessment.

## 2. Replay-grounded experimentation — substantive, not complete

Version1 supplied baseline; wall-following trial improved synthetic trap escape but worsened game duration; negative outcome and sampled cycling motivated hybrid repair. Later experiments address survival, opening timing, cloud/current behavior and reproducible roles. Counterevidence is preserved; repeated4/8 outcomes are acknowledged. Some versions were prepared while previous results remained pending; this limits sequential causal interpretation. Selected final replay receipts independently exist and bind selected source: terminal388 window and losing-game round100 window are complete selected windows with validated source coverage, not reconstructed full state. No causal explanation of losses follows from them alone.

## 3. Actual Java tests and code quality — credible execution, partial correctness

Independently reran all eight retained final test mains against actual compiled final candidate classes with assertions enabled via pinned Java. All exit0; logs/results under reviewer/java-rerun007/. Reproduced80mana/150 synthetic turns plus island capture, escape distance29, open route15, barrier25, U-trap55, and role/logic/cloud/launcher checks. These are genuine executable checks, not prose or reimplemented algorithm-only tests. Initial verifier and expected baseline escape failures retained.

Important test weakness: MazeTest only prints reach time, with no assertion on successful arrival; NavigationTest asserts open route but merely prints barrier result. A future regression could exit0 despite those scenario failures. Their currently observed values support this run only. Simulations omit or simplify visibility, currents, occupancy, cooldown, bytecode limits and joint-unit behavior. No engine-equivalence claim justified.

Source is a single compact static RobotPlayer with decomposed behavior methods; shared-memory packing and bounded arrays are straightforward but dense magic indices/constants and broad catch-and-continue hamper diagnosis. Specific source-inferred risks: healing branch stops when squared distance<=2 from a representative island tile, which does not guarantee the unit stands on an island; lifetime carriersBuilt is not live population; island ownership records lack freshness/reservations; navigation traces have limited reset/progress state. These are review risks, not measured causes of any loss. Broad exception handling does not establish exception-free execution. Correctness remains partial despite useful state-progress evidence.

## 4. Selection, reporting and development performance — honest, limited

Final choice V8 is explicitly4/8 fixed development wins, all against one public opponent; other opponent remains undefeated. Version win counts4,4,3,4,4,4,4,4; no fabricated improvement claim. Selection weighs retained wins and observed fixes, while noting tiny winning-duration difference and no generalization evidence. Source and final tests correspond. Failed experiments preserved; model selection is reasonable within a weak/non-independent development signal, not proof of broad competence.

## 5. Environment/provenance and assessment boundary — functional cooperative loop

Repaired launch allowed64 development games and bounded replay use without recorded infrastructure failure. Source-bound notes, immutable snapshots and fixed helper checks provided an observable loop. Native same-user access remains cooperative, not hard confinement; complete native access tracing is unavailable. Input inventory unchanged proves fixed assets unchanged, not every out-of-workspace non-read. Requested model settings are not independent model attestation. No held-out performance score is included in this blind judgment; evaluator outcomes must be reported separately, without changing these findings or inventing a new threshold.

Overall: substantive autonomous implementation, testing and replay-driven iteration; partial code correctness, credible process, and limited public-development competitiveness. Independent evaluator results remain pending and cannot retroactively validate test semantics or infer causal bug effects.
