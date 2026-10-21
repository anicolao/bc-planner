# Development observations
Launch: 2026-10-21 13:25:43 UTC; deadline 14:10:43 UTC.

## Version 1 plan (before implementation)
Implement independent economy/anchor bot: harvest with carriers, communicate HQ/well/island coordinates, build launchers for defense and expansion, and ship standard anchors to neutral islands. Launcher target selection prioritizes combat units and retreats when locally outnumbered. Navigation uses legal adjacent moves with recent-location penalties and current-aware endpoints. No opponent source or nonpublic information is used.

Predictions: source should compile legally; carrier collection and HQ transfers should both appear in early replays, launchers should move and attack, and anchors should be built/taken/placed by midgame. Wins are uncertain; progress in these states is the initial criterion. Known risks: local navigation can stall, approximate combat strength and symmetry targets can misdirect, and remote discoveries cannot be shared until radio range is regained.

Version 1: build-001 javac succeeded but verifier failed. The CLI output only printed artifact path, and I submitted before treating the artifact status as the authoritative gate. This is a process defect; the failure is preserved. Submission s_9ce31b2af2994541960423fa79626e8c accepted; waiting for terminal outcome before any later submission. Protocol roundtrip tests passed, but are not gameplay correctness evidence.

## Version 2 plan
Version 1 terminal result is rejected/compile_rejected, no games played. Verifier specifically forbids Class.getSimpleName. Remove reflection from exception reporting, retaining the same strategy. Prediction: verifier passes and service runs four games; behavioral predictions from v1 remain unchanged. Require artifact.status=succeeded before submitting.

Version 2 local build status is `verified` (the successful terminal label, not `succeeded`; the overly strict local assertion failed due to this label misunderstanding, not a compiler/verifier failure). Both compile and verify steps succeeded. Submission s_f894356e94d941bfa8bffa792c7b4dd1 accepted.

Navigation model (work/navigation_model.py) tests the v2 scoring policy independently of the engine. Open path arrives in 26 modeled moves, but the 25-tile wall and U enclosure do not escape within 400 modeled moves. This supports a navigation defect hypothesis, not a claim that either development map contains these obstacles. Also found by source review: stale cached neutral island records can overwrite fresher team-owned records. Candidate later changes should add persistent obstacle following and restrict island writes to fresh observations.

Version 2 terminal: 4/4 wins (DefaultMap A 405, B 435; Rectangle A 299, B 392 rounds). Replay evidence: full r50 pages on DefaultMap show own carriers PICK_UP_RESOURCE and PLACE_RESOURCE and own launcher LAUNCH_ATTACK. HQ3 r80-100 shows resource receipts and spawning but no anchor crafting in that particular HQ/time window. Full final Rectangle-A r299 includes own carrier 11885 PLACE_ANCHOR and launcher attacks. Thus economy/combat/anchor state progress is established, not just wins. Raw targets are preserved, not interpreted as damage or coordinates. Initial wide-range replay pages were intentionally samples and marked incomplete; subsequent single-round windows follow all continuation offsets.

## Version 3 plan
Retain v2 strategic parameters, add a bounded persistent wall-follow fallback after eight non-improving navigation decisions, cache per-turn enemies for movement scoring, and prevent stale neutral island memories from overriding newer shared ownership. Prediction: independent navigation wall/U tests improve while service remains 4/4, with no increase in runtime errors. Match speed may change unpredictably because paths and deterministic random draws change. Preserve v2 as fallback.

Version 3 terminal: 4/4 wins, but slower on every paired game (412, 531, 517, 444 rounds versus v2 405, 435, 299, 392). Navigation model improved (open 26, wall 44, U 59 modeled moves); this does not establish faster real-map play. Fresh/stale island policy model passes four cases. HQ5 v2 r70-200 complete robot-filtered replay contains no anchor event. Source review identifies resource starvation: carrier production spends adamantium as soon as 50 is available, and launcher production spends mana at 45; anchors need 80 of both simultaneously. This is a plausible delay mechanism, not a replay-proven stockpile measurement.

## Version 4 plan
Keep v3 correctness fixes and navigation, but explicitly reserve 80 of both resources for an anchor from round 60 after five carriers have been built. Continue spawning from resources above that reserve; once the anchor is built, normal production resumes. Prediction: anchor pickup/placement occurs earlier and median finishing rounds fall, while preserving four wins. Risk: military/economic growth can suffer if reserve waits too long. This isolates the spending priority change from combat tactics.

Version 3 final Rectangle-B round 444 fully paginated: own carrier 10211 PLACE_ANCHOR, collection events and launcher LAUNCH_ATTACK remain present. One page had projection_output_limit (124 returned of 128 source rows); the next request correctly used next_record_offset=252 rather than assuming 256, and completed the interval. No complete absence-of-runtime-errors claim is possible from these exposed fields.

Version 4 reservation predicate model passes 80,802 resource states: eligible construction preserves active 80-resource reserve. This proves arithmetic of the modeled predicate, not successful gameplay scheduling.

Version 4 terminal: 3/4 wins. DefaultMap-A loses at 629; other games win at 277,160,178. Reservation strongly accelerates three games but introduces a loss, so it is not an acceptable final improvement on its own. Replay HQ5 r60-150 confirms BUILD_ANCHOR at 95,126,144 (v2 same HQ had none r70-200); Rectangle-A final r160 own carrier 11092 PLACE_ANCHOR confirms faster capture. DefaultMap-A final r629 contains opponent carrier 12217 PLACE_ANCHOR and very little own activity (one own resource pickup); this supports late military/economic collapse but does not identify every cause.

## Version 5 plan
Moderate anchor investment: start after round 90 and at least six carriers/six launchers built, enforce 50 rounds between HQ anchor crafts, and suspend reservation/crafting when an enemy launcher is directly visible at HQ. Keep v3 navigation/caching fixes. Prediction: regain DefaultMap-A win while keeping some of v4's anchor timing benefit; fail the hypothesis if any development loss remains. The safety policy uses only local sensed enemies, not replay-derived coordinates or opponent code.

Version 5 terminal: 4/4 wins at 469,460,251,222 (mean 350.5), versus v2 mean382.75 and v3 mean476. This recovers the v4 loss, and improves both Rectangle games against v2, though both DefaultMap games remain slower than v2. No claim of generalization beyond these fixed games. Additional v3 carrier10211 complete r189-444 trace establishes repeated PLACE_RESOURCE, PICK_UP_ANCHOR at403 and PLACE_ANCHOR at444: the last capture was not a hundreds-of-round anchor-carry stall.

## Version 6 plan (last allowed submitted version)
Change only the navigation fallback activation from eight to twenty non-improving movement decisions. Hypothesis: reduce premature wall-following caused by temporary friendly traffic while preserving eventual static-obstacle escape. Prediction: independent wall/U tests still terminate; retain 4/4 service wins and potentially reduce finishing rounds versus v5. If worse, choose a prior immutable submitted version. No further submissions after this.

Version 5 replay grounding: DefaultMap-A HQ5 builds anchors at101 and177 in the fully paginated r90-180 interval, versus v4 at95,126,144. This is consistent with reduced anchor spending frequency; local combat threat and resource effects cannot be separated. Rectangle-A finalr251 own carrier12417 PLACE_ANCHOR and own launcher attacks establish deployed state progress. Correction to v1 risk wording: no symmetry inference was implemented; launcher exploration after round70 uses deterministic pseudo-random destinations.

All six source submissions are now spent (v1 compilation rejection, v2-v6 four games each if completed). No further source experiments or submissions will be made. Awaiting v6 terminal result, then select a submitted version and verify exact restoration.

Version 6 terminal: 4/4 wins at395,447,251,222 (mean328.75). This is the lowest mean among the 4/4 versions tested. The fallback-threshold hypothesis is supported on these fixed games: both DefaultMap finishes improve versus v5, both Rectangle finish rounds are unchanged. No repeated stochastic trials or held-out results are available.

Final selection: version6 / s_f6c3960b5ace4284ace24ed6a4fe5a6e. Final replay evidence: DefaultMap-A HQ5 BUILD_ANCHOR at101 and168; finalr395 own carrier11526 PLACE_ANCHOR. Rectangle-A carrier12417 r220-251 trace includes PLACE_RESOURCE230, PICK_UP_ANCHOR231, PLACE_ANCHOR251. These are recorded event names and rounds, not inferred hidden state. Final verification will compare src to the immutable submitted snapshot and build artifact, then stop.
