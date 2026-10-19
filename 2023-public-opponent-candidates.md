# Battlecode 2023 public opponent candidates and engine compatibility

Research checked 2026-10-19 UTC. This is public competition intelligence, not a benchmark roster or an evaluation schedule. No bot strategy was edited. Repository files and official records were read; candidates were not compiled, instrumented or played during this research.

## Executive finding

A defensible progression exists: the official lecture bot for tutorial diagnostics; Beaver Bois and the separate Newbie runner-up as non-finalist candidates; and Gone Fishin’, 4 Musketeers and don’t @ me as historically proven finalist teams. Historical team placement is evidence about a team’s submitted bot in its contemporary tournament, not automatic proof about every package in its repository.

**The current 2.0.3 environment must not be described as a faithful finalist-strength benchmark.** Finalist repositories declare 3.0.13, and the later rules materially change combat, economy, islands and sensing. Compilation alone cannot resolve that mismatch. Preserve the old lecture diagnostic as a separately named ruleset; establish and validate a later-engine track before making competitive claims.

## 1. Official engine provenance and material changes

The Battlecode GitHub API resolves these official release tags:

| Release | Release date | Source revision |
|---|---|---|
| [2.0.3](https://github.com/battlecode/battlecode23/releases/tag/2.0.3) | 2023-01-20 | `5d142a87579af22c2c04ce046a3cbd448dc1869e` |
| [3.0.13](https://github.com/battlecode/battlecode23/releases/tag/3.0.13) | 2023-02-02 | `9b890f83672c98b81cc153f618bd56e1ab6134b5` |
| [3.0.14](https://github.com/battlecode/battlecode23/releases/tag/3.0.14) | 2023-02-04 | `1a9e55f6a9c0204f1f5f5cf6d6c2cac0d1f108b6` |
| [3.0.15](https://github.com/battlecode/battlecode23/releases/tag/3.0.15) | 2023-02-05 | `af42086ecd09709dc603b2aaa9e9b98312c9ef79` |

The current bcenv Nix definition pins the first source revision and the official 2.0.3 JAR. The official [3.0.13 specification/changelog](https://github.com/battlecode/battlecode23/blob/9b890f83672c98b81cc153f618bd56e1ab6134b5/specs/specs.md.html) documents the January 24 post-Sprint-2 rebalance and later fixes. Direct source comparisons establish:

| Mechanic | 2.0.3 | 3.0.13 |
|---|---:|---:|
| Launcher mana cost | 60 | 45 |
| Launcher attack damage | 30 | 20 |
| Launcher movement cooldown | 15 | 20 |
| Carrier action cooldown | 8 | 10 |
| Amplifier mana cost | 30 | 15 |
| Standard-anchor cost, Ad/Mn | 100/100 | 80/80 |
| Standard/accelerating-anchor healing each round | 1/2 | 4/6 |
| Island healing locations | Island tiles | Within squared radius 4 of island tiles |
| Elixir conversion threshold | 700 | 600 |
| Well-upgrade threshold | 1700 | 1400 |

Primary implementation evidence: [2.0.3 RobotType](https://github.com/battlecode/battlecode23/blob/5d142a87579af22c2c04ce046a3cbd448dc1869e/engine/src/main/battlecode/common/RobotType.java), [3.0.13 RobotType](https://github.com/battlecode/battlecode23/blob/9b890f83672c98b81cc153f618bd56e1ab6134b5/engine/src/main/battlecode/common/RobotType.java), [3.0.13 Anchor](https://github.com/battlecode/battlecode23/blob/9b890f83672c98b81cc153f618bd56e1ab6134b5/engine/src/main/battlecode/common/Anchor.java), [GameConstants](https://github.com/battlecode/battlecode23/blob/9b890f83672c98b81cc153f618bd56e1ab6134b5/engine/src/main/battlecode/common/GameConstants.java) and [Island](https://github.com/battlecode/battlecode23/blob/9b890f83672c98b81cc153f618bd56e1ab6134b5/engine/src/main/battlecode/world/Island.java).

Important discrepancy: the changelog says “Launcher damage decreased from 40 --> 20.” The actual 2.0.3 source has 30, so the cross-version comparison above uses 30, not the erroneous historical number. This is one reason to inspect code and the released artifact rather than rely on narrative version labels.

Additional changes include allowing carrier attacks using held anchors, rejecting incorrect resources for well upgrades, and limiting cloud sensing when the sensing robot is inside a cloud. The 3.0.13 release corrects which location determines that sensing limit. See the [pinned controller implementation](https://github.com/battlecode/battlecode23/blob/9b890f83672c98b81cc153f618bd56e1ab6134b5/engine/src/main/battlecode/world/RobotControllerImpl.java).

The public source tree grows from 32 map resources at 2.0.3 to 103 at 3.0.13/3.0.15. These are source-tree counts, not a verification of a downloaded later JAR. The [official 3.0.13-to-3.0.15 comparison](https://github.com/battlecode/battlecode23/compare/3.0.13...3.0.15) changes client/spec files and the engine’s `SPEC_VERSION` string only, from 3.0.13 to 3.0.14. No gameplay implementation or map-resource change appears in that source comparison. This does not itself authenticate the compiled JAR or establish the exact server artifact used in finals.

The [3.0.14 release](https://github.com/battlecode/battlecode23/releases/tag/3.0.14) is explicitly labeled for the final tournament. Its [release workflow](https://github.com/battlecode/battlecode23/blob/1a9e55f6a9c0204f1f5f5cf6d6c2cac0d1f108b6/.github/workflows/release.yml) must also be checked before drawing artifact equivalence conclusions: non-public releases inject private maps and publish privately. Thus public gameplay-source equivalence does not establish identical released map sets or obtainable final-server binaries. A public 3.0.13 runtime can be a transparent final-rules benchmark without being misrepresented as the exact finals deployment.

### Required compatibility gate

1. Pin the intended official release, source revision and independently computed hashes of engine JAR, API docs, maps and build inputs. Check the JAR’s embedded version and concrete constants. Do not infer artifact identity from its filename.
2. Keep 2.0.3 and the later ruleset as distinct environments/results. 3.0.13 matches the inspected finalist manifests; selecting 3.0.15 instead requires the source/artifact-equivalence check just described.
3. Compile each selected package and its own utilities, without modifying strategy, against that engine using a pinned Java 8 toolchain. Avoid compiling every obsolete package in a repository as a proxy for the intended entry point.
4. Run the official instrumenter/verifier and active smoke matches in both side positions. Check exceptions, bytecode failures, resource collection, spawning and engagement. A successful process exit is insufficient.
5. Use maps from the same pinned ruleset, and record engine, map, source and compiled-player identities with every result. A counterfactual run on 2.0.3 can be useful if explicitly labeled; it does not reproduce the historical competition.

## 2. Candidate tiers and exact repository pins

All six primary candidates below contain the same 34,520-byte repository-root AGPL-3.0 license text, independently downloaded at their pinned commits. SHA-256: `76a97c878c9c7a8321bb395c2b44d3fe2f8d81314d219b20138ed0e2dddd5182`. Git blob: `dbbe3558157f5861bff35dcb37b328b679b0ccfd`. This verifies the declared repository license, not a complete audit of every contributor’s rights.

### A. Tutorial: official lectureplayer

- Repository: [battlecode/battlecode23-lectureplayer](https://github.com/battlecode/battlecode23-lectureplayer/tree/57063ad07b2311c21c99ba7be100a55fcdb3de6b).
- Pin: `57063ad07b2311c21c99ba7be100a55fcdb3de6b`, 2023-01-20; package `lectureplayer`, six Java files.
- Official repository description: “Contains an example player based on the battlecode 23 lectures.” This establishes educational provenance, not tournament placement.
- Repository version: 2.0.1. Existing project evidence already reports this exact source successfully built, verified and played on 2.0.3; this research did not rerun that test. Later-engine behavior remains a separate test.
- Use: active tutorial diagnostic and integration check. Do not use wins against it as evidence of competitive strength.
- [Pinned license](https://github.com/battlecode/battlecode23-lectureplayer/blob/57063ad07b2311c21c99ba7be100a55fcdb3de6b/LICENSE).

### B. Non-finalist field candidate: Beaver Bois

- Repository: [beaverbois/battlecode23](https://github.com/beaverbois/battlecode23/tree/4892382943da5a8527906467739a64db51ccc50d).
- Pin: `4892382943da5a8527906467739a64db51ccc50d`, 2023-09-19; README-only latest commit. Intended package `USQualifiers`, 12 Java files, explicitly identified by the team as its final submitted code.
- Repository version: 3.0.5; Java 8 build configuration. Static imports use Battlecode, Java standard libraries and the same package. No external bot library was detected in that package’s imports. This is not a successful build/verifier claim.
- Strength: team README reports 25th of 96 in US qualifiers. The [tournament standings](https://challonge.com/bc23usaquals/standings) independently show participation and a W-L-W-W-W-L match history. Their compressed rank groups display Beaver Bois as group 5, not a literal ordinal 25. Keep the exact 25/96 number attributed to the team.
- The package changed after qualifiers; latest package-touching commit is January 31. Exact server-submission equality is unverified.
- [Pinned license](https://github.com/beaverbois/battlecode23/blob/4892382943da5a8527906467739a64db51ccc50d/LICENSE).

### C. Non-finalist field candidate: no thoughts head empty

- Repository: [reeceyang/battlecode-2023](https://github.com/reeceyang/battlecode-2023/tree/0a9a855ea15780f692dc994a390e39041a184597).
- Pin: `0a9a855ea15780f692dc994a390e39041a184597`, 2023-02-20; version 3.0.13.
- Official [Battlecode past-years page](https://battlecode.org/past.html) identifies the team as Newbie second. This is the separate Newbie competition, not second overall. US-qualifier standings also show a W-L-W-W-L history.
- Candidate package `v5anaconda`, nine Java files. Its [February 6 commit](https://github.com/reeceyang/battlecode-2023/commit/9f833c8b462e7cfcee1ffcf11a2e013d88bca6c6) says “final tournament bot.” That label alone cannot prove which tournament or exact submitted artifact it represents. Default Gradle teams point to `reeceplayer`, a different package.
- Use as a candidate after package provenance and runtime checks, not as an already calibrated middle-strength opponent.
- [Pinned license](https://github.com/reeceyang/battlecode-2023/blob/0a9a855ea15780f692dc994a390e39041a184597/LICENSE).

### D. Finalist: Gone Fishin’, official second place

- Repository: [carlguo866/battlecode23-gonefishin](https://github.com/carlguo866/battlecode23-gonefishin/tree/1c3ff39bca59e302c6c1092025e413bd0a102ab9).
- Pin: `1c3ff39bca59e302c6c1092025e413bd0a102ab9`, 2023-02-08; version 3.0.13.
- Placement confirmed by the [official history](https://battlecode.org/past.html) and [final standings](https://challonge.com/bc23final/standings). The official site hosts the [team’s postmortem](https://battlecode.org/assets/files/postmortem-2023-gone-fishin.pdf).
- Prefer investigating `submit26_final`, 13 Java files, created by [f5e5492977b1a6031b4b856b4e301cc034d71309](https://github.com/carlguo866/battlecode23-gonefishin/commit/f5e5492977b1a6031b4b856b4e301cc034d71309), February 3, with message “Submit26: Final.” This is stronger artifact evidence than choosing the working package by name alone; no server upload hash has been located.
- README names `bot1` as the main code, but it received February 6 post-final cleanup that changes source beyond package renaming/comments. Do not silently substitute it for the preserved snapshot.
- Both packages hardcode launcher damage 20, a concrete semantic mismatch with 2.0.3. The package includes its utilities; README credits 4 Musketeers’ utility library, so these are not completely independent code lineages.
- [Pinned license](https://github.com/carlguo866/battlecode23-gonefishin/blob/1c3ff39bca59e302c6c1092025e413bd0a102ab9/LICENSE).

### E. Finalist: 4 Musketeers, official third place

- Repository: [maxwelljones14/BattleCode2023](https://github.com/maxwelljones14/BattleCode2023/tree/074963dacf1c597518655de4c7542c36de6bc554).
- Pin: `074963dacf1c597518655de4c7542c36de6bc554`, 2023-02-07; version 3.0.13.
- Official history/final standings establish third place. [Maxwell Jones’s project page](https://maxwelljon.es/projects/battlecode/) directly links this repository and the official-hosted postmortem.
- Candidate `MPWorking` has 35 Java files including generated navigation and utility classes. Its February 3 history includes [87869e3ce8af825aade3869dc5c84ada658dad9d](https://github.com/maxwelljones14/BattleCode2023/commit/87869e3ce8af825aade3869dc5c84ada658dad9d), “Turn off debug. Final submission :)”, followed by two later same-day edits. Latest package edit is `c971455429d55db24c6f14e59e169da88fa03853`.
- `MPIgneous` is an earlier named snapshot, not demonstrably the final entry. Default Gradle match configuration selects examplefuncsplayer. Actual final-upload equality and clean runtime behavior remain unverified.
- [Pinned license](https://github.com/maxwelljones14/BattleCode2023/blob/074963dacf1c597518655de4c7542c36de6bc554/LICENSE).

### F. Finalist: don’t @ me, official history labels seventh

- Repository: [georgezhang02/battlecode23](https://github.com/georgezhang02/battlecode23/tree/83f81b5568772ecb4f77af462f512dae7aaa4968).
- Pin: `83f81b5568772ecb4f77af462f512dae7aaa4968`, 2023-02-03; version 3.0.13.
- The [official history](https://battlecode.org/past.html) labels the team seventh; its [official-hosted postmortem](https://battlecode.org/assets/files/postmortem-2023-dont-at-me.pdf) names George Zhang among the authors. The repository is additionally mirrored under the team’s name by Battlecode Archive. The PDF’s embedded repository URL was not independently extracted in this pass.
- `FB_ZZZ`, 14 Java files, has a final-questioning commit message: “ZZZ BOT IS APPARENTLY THE FINAL?” Treat that as a plausible candidate, not exact submission authentication.
- The final-standings page uses compressed rank group 6 for this team and Meteor. Avoid treating that display as literal sixth overall or overruling the official historical label.
- [Pinned license](https://github.com/georgezhang02/battlecode23/blob/83f81b5568772ecb4f77af462f512dae7aaa4968/LICENSE).

## 3. Additional leads and exclusions

- **Producing Perfection, official winner:** [Battlecode Archive’s mirror](https://github.com/battlecode-archive/2023-Producing-Perfection) declares AGPL-3.0, but its default branch is `bruhment` at `64a7b4a6acb9ed9233f06f34f7f0d34a65a82d73`, dated January 26. Do not call that default HEAD the championship bot. Its `master` is `2e231f31a4622909b0dfd34a68c9b634dde1c803`, dated February 8, after finals. A February 7 merge includes a final-bot label, but exact package/submission provenance needs a separate check. Mirror creation/push dates in 2026 do not prove the original public-release date.
- **IvanGeffner/Battlecode23:** public source at `8f8188b83375b4031223fd37bd8512f1b9485fad`, containing `fortytwo`, but no root license and GitHub reports no license. Exclude from a redistributable open-source opponent catalog unless permission or a valid applicable license is found. Public visibility is not sufficient permission; see [GitHub’s no-license guidance](https://choosealicense.com/no-permission/).
- **Other archive entries:** camel_case (MIT), Mittens, Meteor, Your Anchor Is On Another Island and others merit later independent provenance checks. Merely appearing in a named mirror is not sufficient to authenticate the source of a tournament placement.

## 4. Licensing, build viability and evidence limits

AGPL permits running, copying and modifying under its terms. Retain license/copyright notices, attribution and exact corresponding source when distributing covered binaries; identify modifications, and assess the source-offer requirements if a modified covered program is exposed over a network. Keeping opponents as separately built, unmodified artifacts is operationally useful but is not by itself a complete licensing analysis. The [license text and conditions](https://choosealicense.com/licenses/agpl-3.0/) govern. Do not relabel AGPL opponents as GPL tooling or remove their upstream notices.

All six candidate repositories have Java 8 source/target settings and Battlecode Maven dependency configuration. Static package inspection found local utilities and standard Java/Battlecode imports, not missing third-party jar imports in the nominated packages. Some include broad java.io imports; imports alone neither prove prohibited runtime behavior nor establish verifier success. Legacy Gradle wrappers, all-package builds, network dependency resolution, stale default players and generated-source assumptions are practical failure modes. No build or verifier result was produced by this research.

A fair competitive report should distinguish:

- Historical placement of the team.
- Evidence linking a package/revision to its actual submission.
- Successful compilation and instrumentation on the selected engine.
- Successful active games without pathological runtime failures.
- Measured performance on a declared suite, including paired side positions and failures.

These are different claims. None should silently stand in for another.

## 5. Public availability and contamination limits

These sources and strategy reports are public and have commit histories dating to 2023. Commit dates do not prove when a repository became public. They may have entered model training data, retrieval indexes or previous human/agent study; this research cannot determine whether any particular model saw them during training.

Public opponents support reproducible benchmarking but cannot establish training-data novelty. Preventing access during an experiment only bounds in-run exposure. Repeatedly examining an opponent’s source, scores or replays also turns that opponent into development data. Different packages from one repository are correlated versions, and even distinct teams share utility code, ideas and a common metagame.

Therefore use wording such as performance against pinned public historical opponents, disclose allowed retrieval and prior exposure, and keep any later sealed evaluation assignment outside public candidate documentation. No sealed selection or evaluation schedule is recorded here.
