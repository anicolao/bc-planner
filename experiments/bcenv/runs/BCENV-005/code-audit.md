# BCENV-005 independent frozen-code / learning-loop audit

Frozen assessment, October21 2026, following competitor stop/freeze14:53:12UTC.
The reviewer has not read BCENV-005 held-out plans, directories, opponents or
outcomes. No candidate strategy edits or coaching occurred. One authorized
observer rerun of the existing tests produced a new output directory only;
no matches were launched. All conclusions below precede held-out scores.

Paths are relative to `vm-reassessment/`. `S` means
`frozen-005/src/tide/RobotPlayer.java`; `T` means
`competitor-005/tests/checks/Main.java`; `W` means `competitor-005/work/`.

## Timeline and evidence integrity

Independently recomputed the91-event service hash chain in
`competitor-service-005/audit.jsonl`. Notes precede their source-matching submit
events at sequence pairs **1/2,25/26,35/36,56/57,67/68,71/72,77/78,84/85**.
The trajectory is baseline; rejected pure wall following; bundled production/HQ
safety; early anchor reservation; delayed reservation; rejected role/home/state
bundle; hybrid navigation; rejected isolated island-freshness correction.

These are actual immutable-through-interface pre-submission statements, not just
a retrospective journal. They bind source versions and earlier replay receipts;
they do not prove private cognition, novelty, honesty or absence of observations
outside the permitted interface. The coordinator's `receipt-audit-005.json`
independently reports8 notes/submissions,64 games and53 verified feedback
receipts, no audit failures. Refused requests are incompletely logged; successful
reads are a lower bound. Native stop evidence is external to the service, which
has no persistent stop marker. No complete native access transcript is available.

Final selected V7 submission is `s_4b963e20fb334da6afa80bfd71797428`, note sequence77.
Individual selected Java hash:
`3f852d409a9f4bb840d4f99bdc516d288364436990f64c9ed7bb5aecb2d5a33d`.
Service source hash:
`e1605b1680175e5bd91dd66616a1e0e69f618c3c737226de2aaceef59c00e8a7`.
Observer test binary hash matches the selected verified binary:
`d3d5e00d258f726ce83f82eacc530ab0439a3e18895c42f51e3d461933c64d9a`.

## Primary assessment

| Axis | Rating | Basis |
|---|---|---|
| Legal artifact/provenance | supported | Final compile/verifier artifacts and selected source binding; observer reran actual selected classes successfully using the fixed helper. |
| Observable prospective hypotheses | supported | Eight source-bound notes precede submission; notes002–008 name falsifiable expectations, contrary evidence and limitations. Stronger evidence than a final document labeled prospective. |
| Replay-grounded reasoning | supported | Specific prior references in notes; independently checked53 saved pages in14 intervals follow returned offsets to completion. Event claims below are directly supported. |
| Correctness/state progress | partial | Real Java scenario tests plus actual replay sequences demonstrate useful paths; stale ownership and resource/current cases remain unresolved. |
| Experiment discipline | supported | Preserved losing experiments and failed tests; isolated V4→V5 reservation change and V5→V7 navigation comparison; rejects V8 after failed8/8 prediction and restores exact V7. |
| Code quality/invariants | partial | Role-separated methods, explicit navigation arrival ranges and guarded actions; dense mutable static state, incomplete reset/coverage and correctness risks below. |
| Information boundary/no coaching | partial | No violation observed in reviewed records; no complete native tool trace. Same-user procedural restrictions are not technical confinement. Self-attestation and unchanged supplied inputs cannot establish every read. |

**Verdict:** a credible observable cooperative learning loop is supported by
pre-result source-bound hypotheses, negative evidence, actual candidate-class
tests, replay analysis and explicit selection. Code correctness and complete
boundary compliance are not thereby proven. Keep the practical environment,
retain its audit limitations, and assess competitive generalization separately.
One run does not complete the broader competence program.

## Concrete source-inferred risks (not claimed observed failures)

1. **Stale island ownership persists in the selected version.** `S:45–57`
   overwrites shared records from all cached islands without freshness metadata;
   `S:98–101` prefers any local cache over later shared state. A robot remembering
   neutral ownership can overwrite a newer friendly report or repeatedly choose
   an already-owned target. V8's attempted correction was competitively rejected;
   FINAL and note008 acknowledge this explicitly. A development loss does not
   establish that the correction was wrong, nor erase the V7 defect.
2. **Well-resource classification is incomplete.** `S:43` maps all non-mana wells
   to adamantium, including elixir. Local observations refresh entries, but
   shared publication compares whole encoded values (`S:53–55`), so changed
   resource types can coexist as stale duplicate coordinates. Once a carrier
   chooses `well`, `S:129–130` does not reconsider it while nonnull. This can
   perpetuate a wrong resource assignment. No elixir/conversion test exists.
3. **Current safety is not an invariant.** `safeMove` checks only the immediate
   destination (`S:137–138`). Greedy scoring adopts a pushed endpoint only if
   safe (`S:223`), but an unsafe endpoint does not reject the move: scoring falls
   back to the immediate square although actual current movement may still occur.
   Wall following, retreat and combat micro also omit full current dynamics
   (`S:157,181–184,198–211`). This is a source-level safety gap, not an attributed
   game loss. The reverse-current test does not simulate actual pushing.
4. **Lifecycle and failure observability are limited.** Home is chosen once
   (`S:35–39`) and carrier well selection is sticky. These are disclosed limits,
   not demonstrated failures in the reviewed games. The catch/yield loop
   (`S:23`) can keep a bot alive despite repeated errors; replay does not prove
   absence of exceptions or bytecode stalls. No actual engine controller,
   concurrency model or bytecode budget is represented by the test harness.

The earlier general arrival-range risk is not asserted here: anchor navigation
explicitly uses range0 (`S:110`), while HQ delivery uses range2 (`S:127`), and
`moveTo` honors that parameter (`S:195,199`). This is meaningful state separation.

## Java test credibility

Executed `./candidate-check test --build work/build-final --tests tests
--main-class tide.Main --output work/observer-test-audit` after freeze.
`W/observer-test-audit/check.json`, `test.log` and
`W/observer-test-audit-response.json` retain passing results and bound hashes.
Tests call the actual verified candidate methods, not a parallel Python policy.

`T:38` genuinely exercises10,800 encode/decode cases. `T:39–51` checks distinct
HQ registration, no movement while mining, placement branch, movement, funding
thresholds, a long wall, U obstacle and reverse-current choice. Observer run
reproduced wall29 and U47 simulated turns. Failed test001 (missing mock return),
test003 (old navigation), test010/011 (hybrid drafts) remain in W; corrected
mock failure is not misreported as an engine bug.

Coverage is narrow: `T:28–31` declares any anchor carrier eligible to place on
neutral island1, so the placement test verifies branching, not island reachability
or legal placement geometry. Fake sensing usually returns empty arrays and
`canSenseLocation` is false except the current scenario (`T:19,25`). Movement
changes position without current displacement (`T:23`); cooldowns, occupancy,
resource accounting and bytecode behavior are simplified. No full collection→
return→deposit→anchor-delivery lifecycle or combat micro scenario is tested.
`reset` (`T:36`) does not reset every static field, notably island caches; present
assertions pass in their fixed order but general test independence is unproven.
These are useful actual-code checks, not engine-equivalence or coverage proof.

## Replay reasoning and causal restraint

Independently checked raw paged V7 game6 carrier13241, rounds200–266:
36 PICK_UP_RESOURCE actions, PLACE_RESOURCE241, PICK_UP_ANCHOR242,
PLACE_ANCHOR266. This demonstrates real economic and anchor-delivery progress,
not merely a winning label. Files:
`W/replay-007-g6-c13241-200-266-p0.json` through `-p2.json`.
All53 saved pages form14 fully continued intervals; merged convenience files are
not substituted for the raw feedback receipts.

Notes004/005 compare early launcher exchanges and HQ spawn/craft timelines while
correctly separating bundled changes, net resource deltas and causal inference.
Note007 does not pretend terminal placement proves a navigation mechanism;
note008 explicitly says replay cannot expose shared-array freshness. This is
appropriately restrained. Mock obstacle success plus fixed-schedule wins still
cannot establish general pathfinding robustness.

Development results reported are5/8,3/8,8/8,7/8,8/8,6/8,8/8,7/8;
V7's median terminal round306.5 is a descriptive selection statistic over the
reused development schedule, not an independent strength estimate. The separate
selection-plan file's claimed pre-V8-result timing is not itself service-receipted;
source-bound note008 already states the8/8 prediction and preserve/revert intent.
No hidden reasoning or held-out performance is inferred from these artifacts.
