# Final competitor 004

## Selected source
- **Version 6**, submission **s_f6c3960b5ace4284ace24ed6a4fe5a6e**.
- Exact final code: `src/tempest/RobotPlayer.java`.
- Snapshot: `work/v6/tempest/RobotPlayer.java`.
- Java source file SHA-256: `2e235e4f9c29a5b904fae2633d28e96f21126184c62ea8bf450f62db88c85b42`.
- Service source archive SHA-256: `0ae8c2f32053048f84537ee01bedda217abde5efc03deb8225c3f0564a22780f`.
- `work/FINAL-VERIFICATION.json` verifies the final source equals both the v6 snapshot and the source compiled in the verified build.

## Strategy
Carriers harvest assigned mana/adamantium wells, deposit at nearby HQs, and deliver standard anchors to neutral islands. HQs produce carriers and launchers; anchor resources are reserved only after round 90, six carriers and six launchers built, with a 50-round craft interval and no locally visible enemy launcher. Launchers prioritize enemy launchers, attack low-health targets, retreat when locally outnumbered, and otherwise explore. Navigation combines recent-visit/current-aware scoring and a wall-follow fallback after 20 non-improving movement decisions. Shared communication publishes HQs, wells and fresh island ownership observations.

## Development outcomes
| Version | Result | Rounds: Default A/B, Rectangle A/B |
|---|---|---|
| 1 | Compile/verifier rejection | No games |
| 2 | 4 wins | 405,435,299,392 |
| 3 | 4 wins | 412,531,517,444 |
| 4 | 3 wins, 1 loss | 629 loss,277,160,178 |
| 5 | 4 wins | 469,460,251,222 |
| **6** | **4 wins** | **395,447,251,222** |

V6 has the lowest mean finish time among tested 4/4 versions (328.75 rounds). Selection prioritizes avoiding development losses, then finishing speed and retaining navigation/ownership correctness fixes. These are four fixed development games, not a held-out estimate.

Six source versions were submitted; v1's rejection consumed one version. Total: **20 games, 19 wins, 1 loss; 49 replay requests**. All source snapshots, rejected builds and unsuccessful experiments are preserved. No further submissions were made.

## Tests and replay-grounded evidence
- `work/build-006/artifact.json`: Java compilation and official verifier both succeed (`verified`).
- `work/check-v6.txt`: 10,800 coordinate/state encoding roundtrips and source-level guarded-action checks.
- `work/navigation-model-v6.txt`: independent grid policy reaches open/wall/U targets in 26/48/69 modeled moves. V2's model failed wall/U within 400 moves. These are policy models, not engine simulations.
- `work/check-islands-v3.txt`: four fresh/stale ownership arbitration cases; `work/check-reserve-v4.txt`: 80,802 reservation arithmetic states. These mechanisms are retained in v6.
- `work/replay-v6-g0-r50-p*.json`: own carrier resource pickups/transfers and launcher attacks establish economy and combat progress.
- `work/replay-v6-g0-hq5-r90-180-p*.json`: own HQ5 BUILD_ANCHOR at rounds 101 and168.
- `work/replay-v6-g2-carrier12417-r220-251-p0.json`: own carrier PLACE_RESOURCE230, PICK_UP_ANCHOR231, PLACE_ANCHOR251, establishing the delivery state sequence.
- `work/replay-v6-g0-r395-p*.json`: final-round own carrier11526 PLACE_ANCHOR.
- `work/result-v6-002.json`: authoritative complete four-game outcomes and replay hashes.

All targeted multi-page intervals follow returned continuation offsets, including projection-output truncation. Two initial broad replay requests were only samples and are not treated as complete intervals. Raw action targets and resource deltas are not misrepresented as hidden world state, damage, collection totals or stockpiles.

## Failed hypotheses and defects
- V1 accidentally used forbidden reflection in exception reporting. The local artifact showed verifier failure, but I submitted before gating on it; service rejected it. Fixed in v2. The build helper's successful label is `verified`, not `succeeded`; an initial label assertion was incorrect and is preserved.
- V3 improved synthetic navigation but slowed every development game versus v2.
- V4's aggressive anchor reservation accelerated three wins but lost DefaultMap-A. Replay confirmed early repeated anchor crafting and an opponent final anchor placement, but does not prove a unique cause of collapse. V5 moderated investment and recovered four wins.
- Local navigation is heuristic, with no completeness guarantee under currents, traffic or complex terrain. Well memory is capped at32 locations. Harvest roles are ID-based rather than globally load-balanced. Launcher exploration/micro is simple, with no coordinated island defense, explicit healing plan, or systematic removal of enemy anchors.
- Replays do not expose a complete robot-knowledge/world-state or exception log; successful games and guarded actions do not prove absence of runtime errors or bytecode stalls.
- No opponent source, coaching, web, connectors, sibling workspaces or held-out evaluation were used.

Detailed pre-change predictions and observations: `work/EXPERIMENTS.md`. Submission/source ledger: `work/VERSIONS.json`.
