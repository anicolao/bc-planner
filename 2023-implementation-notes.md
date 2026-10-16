# BC23 implementation notes: first LLM pilot

Status: observed local-only diagnostic result, 2026-10-16. This is a separate
implementation/evaluation note. It does not amend the approved
[2023 experiment plan](2023-experiment-plan.md), merged in
[PR #8](https://github.com/anicolao/bc-planner/pull/8) at
`7bf66b0122e06432ca53f43443f5bfe071335720`. Neither this draft nor the
[bcenv implementation draft PR #4](https://github.com/anicolao/bcenv/pull/4)
is approved for merge.

## Bottom line

The first pilot answers the immediate question positively: the supplied local
environment enabled a fresh LLM agent to author its own BC23 bot, compile and
verify it, run games, make and test one behavioral prediction, and package a
verified source submission artifact without mid-run coaching or runtime edits.
It does **not** establish competitive strength, full replay comprehension,
security-enforced agent isolation, or completion of the replica acceptance plan.
The useful next comparison is reproducibility and environment usability across
the selected CLI models, not a claim that this pilot picked a winning model.

## Implemented foundation versus observed pilot

The bcenv foundation separates year-neutral artifact/process helpers from BC23
rules, skills, build/verify/run/package tooling and replay extraction. The first
export packages these together; a separately pinned persistent competitor fork
is not established by this run. Builder-written inert-fixture checks are
infrastructure evidence, not autonomous competitor evidence.

The competitor was then launched fresh, without conversation history, from a
frozen export with packaged instructions and a bounded local-only kickoff. It
wrote the candidate and chose the change itself. It ran four sequential games
within a 12-game/20-minute budget. The builder did not author its strategy or
repair its code. The independent observer inspected the frozen artifacts without
changing competitor files or running additional games.

- Engine: official Battlecode 2023 2.0.3; packaged DefaultMap.
- Runtime package: `/nix/store/zrr2chl185cs2fg46knlhkk9nqgwh1pc-bcenv-2023-0.1.0`.
- Launch: 2026-10-16 21:39:30 UTC; completion approximately 21:42 UTC;
  independent audit approximately 21:44 UTC.
- Agent: native fresh session. Actual model ID and effective reasoning effort
  were unavailable in returned platform metadata. **No Codex CLI was used.**
- Agent isolation: behavioral restrictions. Runtime invocations separately used
  a minimal credential-free user/network-namespace chroot with no host mounts.
  Sandboxed runtime commands do not prove isolation of the agent's other tools.

Canonical implementation evidence is maintained in
[bcenv docs/PILOT-001.md](https://github.com/anicolao/bcenv/blob/1fac75bc5a42ca5b9fab405f44c0a8e44d27efaf/docs/PILOT-001.md)
and its [implementation log](https://github.com/anicolao/bcenv/blob/1fac75bc5a42ca5b9fab405f44c0a8e44d27efaf/docs/IMPLEMENTATION-2023.md). These links pin the audited implementation revision. This planner note
interprets that evidence rather than creating a second implementation log.

## Observed first learning loop

The original candidate used a carrier economy and island anchors. The sole
candidate change advanced `ANCHOR_START_ROUND` from 300 to 20. The prediction
was island-capture wins before round 300 in both slots.

| Match ID | Candidate build | Candidate slot | Winner | Final round | PLACE_ANCHOR events |
| --- | --- | --- | --- | ---: | ---: |
| match-001 | build-001, anchors from 300 | A | A | 361 | 5 |
| match-002 | build-001, anchors from 300 | B | B | 494 | 5 |
| match-003 | build-002, anchors from 20 | A | A | 201 | 5 |
| match-004 | build-002, anchors from 20 | B | B | 193 | 5 |

Both changed-build games met the bounded prediction: 160 and 301 rounds earlier
than their same-slot baselines. Engine logs report winning by capturing 75% of
sky islands. The prediction file timestamp precedes the selected build timestamp
(1792186893.7952225 versus 1792186894.471517 epoch seconds). This supports ordering,
but a mutable filesystem timestamp is not an immutable observer journal or
strong preregistration guarantee.

The fixture is `testplayerempty`: its headquarters return and freeze on round 1.
These results establish functioning activity and a sensible local feedback loop
against an inert fixture. They are not four wins against a live opponent. No
active combat opponent, map suite, seed suite or statistical strength estimate
was tested. No combat units, coordinated shared-array policy or robust
lost-carrier replacement were demonstrated.

## What the audit actually verified

The independent audit found zero frozen release hash mismatches, successful
compiler and official-verifier exits for both candidate builds and the fixture,
and four complete result records with zero engine/extractor exits. Replay and
summary hashes, source/binary-to-slot identities and reported winners agreed.
The selected source ZIP bytes equaled the current candidate and verified source
snapshot, and package metadata agreed with the selected build.

### Frozen identities

All following digests are SHA-256. Tree hashes identify the runtime's artifact
inventories; they are not interchangeable with a single file's digest.

- Kickoff: `6191901bbd82fcd850b8cfbfd01147500c0b9463e03e4ea7c4f6854941aaaa7f`.
- build-001 source_sha256: `5b209089a3352fc542463a2b1f28f1d9c3e0dfedb559e4a12d860bdc5ec69bf3`.
- build-001 binary_sha256: `feb6f90b8857cb878ddf3777b7be266be616deacd02972afa253a79101b5e96b`.
- build-002 source_sha256: `aaa110faf6ec5be8ee3f6151922013b391e0544da5b96c555e57490e7b4e706e`.
- build-002 binary_sha256: `5f6c48a3b7c3b9630e87e703eb4eefd7fc65b67539ba997d7e9ea48ad84440ed`.
- fixture-build source_sha256: `ce12ef63e60a1b813d8e88a8cb76acb3868ca2aa588ff23a59acedea7e1c1dea`.
- fixture-build binary_sha256: `32e47cc51c4ac2f1dafdb700e089ee9399a4cca6162966a8368af7ba11a69f79`.
- Selected package verified_engine_sha256: `5e862aa10e85caeb67ae69e1692f7451893e801e0d81597032c1442bbb9deb4e`.
- Selected package zip_sha256: `ef5717b10fd719959f6cdde6e584e87b50e48b383d836869f696afbc3de2b142`.
- Private retained archive (630,292 bytes): `7831b7b385353120f3310a0a61efb26929c569dd23dd4d1d306fee5025332557`.
- match-001 replay: `05d50e12ac564b96f06ed080ba3420a90171f0c633851f4b1d8ee3c2bcbfbfc0`.
- match-002 replay: `c7bed3ffe8789bdec774db911db93c373aaeea1b1a0bd580c5443b153bf0460b`.
- match-003 replay: `e7df6976d3cacca67da489b077304c361d39117315355a8dac37f8c138d10ceb`.
- match-004 replay: `939a3abfee5dcef04dd44cb2e0652b676143691f25075b3d31930d300765faf2`.

Selected package: `package-001`, schema `bcenv.artifact.v1`, kind `source-package`,
Java package `mybot`, verified build `build-002`. The source ZIP and raw competitor
archive remain privately retained; this PR publishes only sanitized analysis and
identities. Hashes support later verification, not public access to those bytes.

## Limits and environment defects exposed

- Replay summaries validate extracted fields, not full world reconstruction or
  all schema fields. Samples are bounded/incomplete. Net resource deltas are
  not gross collection; action counts are not strategy quality or damage.
  Reading summaries and engine logs is not proof of replay comprehension.
- Robot stdout is disabled. Successful outcomes do not prove no caught bot
  exceptions. The JVM primordial-thread-stack warning was nonfatal.
- Packaged skill references to a year manifest, trial specification and local
  tools document were absent from the exported workspace. START_HERE and the
  narrowed kickoff supplied sufficient context, but this is a packaging defect
  to fix in the next export. The historical pilot remains frozen.
- The full Galaxy submission/queue/worker/callback replica was absent. No replica
  scheduling, actual backend integration, official viewer validation, or
  local-versus-queued parity was exercised.
- One package inspection looked for `artifact.json` instead of `package.json`;
  that inspection failure was retained. Build, verifier, match and packaging
  operations themselves succeeded; no failed evidence was discarded.

## CI finding separate from the four pilot matches

The first bcenv PR #4 CI run failed because the inert-fixture repeat check
incorrectly required equal final winners. At a fully tied round-2000 finish,
official `GameWorld.setWinnerArbitrary()` uses unseeded `Math.random()`.
Repeated local successes had hidden this assertion error. The correction requires
the explicit coin-flip terminal reason, retains actual winners, normalizes only
game/match winner fields, and compares all other extracted evidence. It does not
patch the official engine or assert full outcome determinism. The four pilot
games ended through island capture and are unaffected.

Implementation head `1fac75bc5a42ca5b9fab405f44c0a8e44d27efaf` has terminal
**SUCCESS** for the BC23 foundation check in
[CI run 38971645988](https://github.com/anicolao/bcenv/actions/runs/38971645988),
completed 2026-10-16 21:47:26 UTC and independently checked before publishing this
note. All six local Nix flake checks also passed after the correction. This
status belongs to that exact revision; future export fixes are a separate iteration.

## Proposed next gates and authorized comparison

1. Repair exported instruction references and freeze a complete manifest and
   trial spec for a **new** run. Keep this pilot unchanged for auditability.
2. Record requested and effective CLI model/reasoning settings, tool versions,
   task inputs, budget and immutable observer events before comparing results.
3. Run the requested `gpt-6.1-sol` / high versus `gpt-6-astra` / high comparison
   in parallel in two separate repositories **after this notes PR is published**.
   The user has now requested that comparison; this note does not claim it ran.
   Both IDs and high effort were verified in the Codex CLI 0.159.2 catalog;
   account entitlement and actual invocation remain to be tested. Use matched
   frozen inputs, independent workspaces and no cross-agent coaching or leakage.
4. Evaluate environment usability and the observed learning workflow first.
   Add active opponents and map/seed coverage before interpreting playing strength.
5. Complete replay/viewer, security isolation, replica execution and parity gates
   before claiming full acceptance of the approved plan.

These are explicitly future gates, not claims of implemented capabilities or
changes to the approved plan. The native pilot cannot identify which of the two
CLI models will perform better.

## Follow-up: paired CLI comparison 001 stopped before inference

Observed 2026-10-16, after publication of this draft PR. The future comparison
above was attempted; it produced a shared startup failure, not model-performance
results. Explicit `gpt-6.1-sol` / high and `gpt-6-astra` / high runs launched in
parallel at 21:50:01 UTC in two separate local Git repositories with independent
`.git` directories. Neither repository was published remotely. Both processes
exited with code 1 about six seconds later, before any model event, candidate
source, build, or game:

> failed to initialize in-process app-server client: Read-only file system (os error 30)

The existing authenticated `CODEX_HOME` is read-only. Ephemeral execution and
supported separate writable SQLite/log locations did not resolve initialization;
additional non-inference prompt-rendering checks failed the same way. This
identifies a runtime prerequisite, not evidence that either model refused or
could not solve the Battlecode task. Catalog recognition and an existing login
status did not establish inference entitlement. Actual backend model/version,
effective effort and token usage were unobserved. An empty usage/event log is
not proof of a particular billing amount.

The runner was preinstalled Codex CLI 0.159.2, not newly installed or represented
as Nix-pinned. Both runs received the same kickoff and refreshed diagnostic
export `bc23-local-pilot-002`. Export 002 repaired missing local instruction
references without copying the prior competitor's source/results. It retained
the verified Nix runtime package; pilot 001 remained unchanged. The audit found
zero frozen-input hash mismatches, empty candidate/work inventories and clean
Git baselines in both repositories. General agent filesystem isolation remained
behavioral; BC23 runtime commands retained their separate namespace/chroot
boundary. No credential copying, relocation or reconfiguration, new API key,
paid infrastructure, or native-agent fallback was used.

Sanitized retained evidence identities (SHA-256):

- CLI binary: `1748767b230ebfc3d4ab7e4e254920d0c0ad9691fd8c11f190e7d44511a4a92e`.
- Export release: `710265c659a519e33da55c067e457fb1a29c18256e82dcefe0930404b37113d0`.
- Kickoff: `6191901bbd82fcd850b8cfbfd01147500c0b9463e03e4ea7c4f6854941aaaa7f`.
- Comparison report: `67b63b7206da74910724c0bc845f4cb8684c9ad38f6892c80c06713b8f909b4d`.
- Launch manifest: `6289f12f7d70fd4437f485af3c5358ccdaf6c2a89805b89bc6b222dfc9544eb9`.
- Independent audit: `a5e0e4fd415ac121289ba939f6135d556c3a357e58fa5c61c38c390c01c4f7f1`.

The report, manifest, audit and observer launcher were checked against their
retained evidence checksum inventory before this summary was appended. Raw
runtime/environment records and logs remain private. No superiority, legality,
replay, behavioral-learning or playing-strength comparison is possible from
these failed starts.

Next prerequisite: a supported writable CLI runtime using the existing account
connection, with any required setup specifically authorized. Verify successful
initialization there before creating a new frozen paired run. Preserve this
failed comparison as-is; do not silently substitute native agents or treat a
catalog listing as a successful model invocation. No such rerun or setup change
is performed by this notes update.
