# BC23 implementation notes: first LLM pilot

Latest stage: [BCENV-002 tooling and BCENV-003 model-selection results](2023-model-selection-results.md).
The sections below preserve the earlier dated pilot, CLI and review history.
The later authorized foundation merge is recorded in the new results note;
earlier draft/approval statements describe their original checkpoints.

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

## Follow-up: workspace repair and supported-route investigation

Observed 2026-10-16. The user subsequently authorized fixing workspace-local
writability and finding a workaround. This investigation progressed beyond the
first generic read-only error but did **not** launch paired comparison 002 or
perform competitor inference. It does not revise either earlier frozen result.

### Implemented repair and precise remaining prerequisites

The documented per-command `CODEX_HOME` setting selected a new writable home
inside the workspace. The CLI wrote installation/migration metadata there.
Workspace-local XDG runtime, SQLite and log locations were also tested. This
applies the useful part of the earlier writable-directory approach: relocating
ordinary state through supported configuration.

Two independent blockers remained:

1. The new home reports `Not logged in`. Original authentication was untouched;
   no credential was read, copied, mounted, uploaded or reconfigured. An authorized
   account connection remains necessary in a usable executor.
2. Prompt preparation fails on the fixed `/tmp/codex-daemon-1000` socket directory.
   Local metadata showed UID 1000 ownership, mode 000 and a read-only tmpfs mask;
   the CLI requires an owned directory with mode 0700. Supported writable-home
   overrides do not relocate this security-sensitive directory.

[Official Codex socket-directory source](https://github.com/openai/codex/blob/main/codex-rs/uds/src/daemon_directory.rs)
and the [upstream nested-sandbox issue](https://github.com/openai/codex/issues/53799)
support the diagnosis. The local observations, rather than the issue alone,
establish this executor's condition. No mask, ownership, permission or outer
sandbox setting was changed. This is no longer merely a missing writable
working directory.

### Supported alternatives tested without inference

- The installed CLI documents `codex app-server --stdio`. JSON-RPC initialization
  succeeded using the empty workspace-local home. This establishes transport
  initialization, not successful model inference or shell execution.
- A standalone `command/exec` request for harmless `/bin/true` with `readOnly`
  reached inner sandbox startup and failed with the same required-mode-0700
  socket-directory error. The ordinary `workspaceWrite` CLI preparation path
  likewise remained blocked by the mask.
- [Official app-server documentation](https://learn.chatgpt.com/docs/app-server)
  describes `externalSandbox` for a server already running in an external
  sandbox; [the official implementation discussion](https://github.com/openai/codex/pull/8290)
  provides related context. This mode is a distinct API execution configuration,
  not a successful literal `codex exec` run or permission to weaken protections.
- A harmless `/bin/true` request using that documented mode with restricted
  network access was explicitly rejected by administrator policy:
  `ExternalSandbox is not in the allowed set [read-only, workspace-write]`,
  set by `/etc/codex/requirements.toml`. Investigation stopped at that denial.
  No alternate route was used to evade it and no requirement was changed.

Generated local schemas expose requested model/effort and returned model/provider/
reasoning fields, but no successful inference exercised them. There is still no
entitlement determination, effective model configuration, token-usage result,
bot artifact or playing-strength comparison. No native-agent substitution was
made. No authorized alternative executor was available in the checked catalog;
no other computer or new infrastructure was used.

### Outcome and next prerequisite

No permitted competitor execution route was established in this executor. A
supported, separately authorized executor/account connection, or resolution by
the environment owner within supported policy, is required before retrying.
Logging into the new home alone would not repair the socket/sandbox conflict.
Once both prerequisites are verified, create a new paired run with the same
frozen export, equal limits, independent repositories and no cross-agent context.
Do not alter failed comparison 001 or repair evidence 002.

Retained evidence identities (SHA-256), with raw environment/log records private:

- Repair report: `b474c658281f825c0ba3578bbc8cdce313888e40d270d1a75c235d9de1df3798`.
- Repair preflight: `18add95ef161521be6b46d24b05ee913c5f21611449478a29b1c0df88360ffc6`.
- Supported-route report: `c71b68adeb0b93824d97505259c25012562bafc33bec32c5cded8d53d36504c1`.
- Stdio initialization evidence: `218a18c8d9795fd0a26ec12743e11bf2057d73924bd01edf2c573ac04b5980cd`.
- Read-only command evidence: `6e22b557c42534871b96814a6cf8cca3ba6882dc70afc4cc76ba16a79078d188`.
- Policy-denial evidence: `56de5cbef14692888498fa8441ba22fa18316f40b0649da691721f3d87573704`.

This is the documented blocker outcome of the requested repair investigation,
not a completed comparison or evidence favoring either model.

## Authorized native comparison 001: both workflows completed

Observed 2026-10-16. After the CLI blocker was explained, the user explicitly
approved a different, native-agent harness with requested model/effort overrides.
Both `gpt-6.1-sol` / high and `gpt-6-astra` / high configurations were accepted
by the native launcher, with fresh no-history sessions (`fork_turns=none`).
The backend version and token usage were not separately exposed. These are explicitly configured
native trials, **not** successful Codex CLI trials; the CLI failures above remain
unchanged and do not become successes through this separate authorization.

The trials overlapped in time in independent local Git repositories. Sol's launch
was confirmed at 22:00:52 UTC and terminal report received at 22:04:28 UTC;
Astra's launch was confirmed at 22:01:02 UTC and terminal report received at
22:05:35 UTC. These observed timings are not a controlled speed benchmark.
Both used frozen export 002 and identical kickoff bytes, with prompt differences
limited to assigned absolute directories. Each had a 20-minute/12-game limit,
sequential games within its own trial, no inherited conversation or mid-run
strategy coaching, behavioral general-tool isolation and separately sandboxed
BC23 runtime invocations. Neither received the other's code or results.

### Audited results

Each agent authored its own bot, produced two verified candidate builds plus a
verified fixture build, ran four complete games and produced one verified source
package. The audit found zero frozen-input hash mismatches or artifact errors;
compiler, official-verifier, engine and extractor exits were successful. Selected
ZIP contents matched the agent's current candidate, and package identities matched
the selected verified build. All eight games ended in island-capture wins against
the same inert fixture; each replay recorded five anchor placements.

| Requested native model | Baseline A / B rounds | Changed A / B rounds | Agent's selected build |
| --- | --- | --- | --- |
| gpt-6.1-sol / high | 377 / 391 | 237 / 402 | Changed build-002 |
| gpt-6-astra / high | 362 / 235 | 448 / 143 | Baseline build-001 |

Sol changed its anchor-start gate from round 300 to 30. Its prediction of capture
wins before round 300 in **both** positions was refuted by the 402-round B game.
A improved by 140 rounds while B worsened by 11. Sol explicitly retained that
failed joint prediction and selected the changed build for its lower observed
two-position mean: 319.5 versus 384 rounds, despite a worse maximum of 402 versus
391. That selection criterion was the agent's choice, not a shared benchmark
criterion imposed on both models.

Astra changed its anchor-start gate from round 150 to 1. Its prediction of faster
capture wins in **both** positions was refuted by the A game: 448 versus 362
rounds, while B improved from 235 to 143. It retained the failed joint prediction
and selected the baseline for its lower observed maximum: 362 versus 448 rounds.
The changed mean was 295.5 versus baseline 298.5, only three rounds lower; Astra
did not present that as evidence of strength. Thus the two agents made different
selection tradeoffs while correctly reporting their own counterexamples.

### Interpretation and limits

The useful result is that both explicitly configured native agents completed the
same bounded build/test/inspect/change/package workflow and rejected a prediction
when one side contradicted it. This shows usable environment support and bounded
evidence handling. It does not establish either model's superiority: there was
one trial per model, different self-authored strategies and selection objectives,
one map, no repetitions, no head-to-head games and no active opponent. The inert
fixture's headquarters freeze on round 1. Faster fixture completion is not a
playing-strength estimate.

Prediction-file timestamps and retained text support ordering, but are not an
immutable precommit journal. In both runs, prediction and changed source first
appeared within the same three-second observer polling interval. There is no
strong independent observer-precommit proof. No strong preregistration claim
follows. Replay
extraction validates only selected fields, not full replay comprehension or
world reconstruction. Bounded action samples do not explain the side-dependent
regressions; suggested routing/economy explanations remain hypotheses. No full
replica acceptance, stronger general-agent isolation or CLI compatibility was
established by this native comparison.

### Selected artifact identities

All digests below are SHA-256; candidate sources and full evidence remain private.
Both packages bind to verified engine identity
`5e862aa10e85caeb67ae69e1692f7451893e801e0d81597032c1442bbb9deb4e`.

- gpt-6.1-sol: package `islandbound`, `package-002`.
  - source_sha256: `66c811fda95120d7a7abc9434d1234a965763add5e70f145b675df91b63bbcd6`.
  - binary_sha256: `9ed2346af6f3d4c030f6563ecb6a847df377ad70318f5734106d8de0c5b0414c`.
  - zip_sha256: `a1164bd70b5d1cf33fa700f81a0c1929e736b56b35e08aced16bd8ec589ebb1a`.

- gpt-6-astra: package `mybot`, `package-001`.
  - source_sha256: `15aa5a112e14aac186345ce104e132d57b0d899af08a07d3903a26f016a55327`.
  - binary_sha256: `10df8c561b16b2fc62b7a154fa20dd858e68ceef4a78071c714c8eb9afca92d6`.
  - zip_sha256: `d6f2ca7955012378eda7e895894bacd591b4522687b97aa3763a07f5c77a7f5e`.

The private evidence archive, with 589 files independently byte-verified and zero
mismatches, has SHA-256
`de6e6b20367dc18d0b0e4200b34b0fab52dc254994ae511bfbadce00d66a557e`.
It contains candidate workspaces, reports and observer evidence, excluding the
large Nix/runtime closure retained separately with frozen export 002. Additional
retained SHA-256 identities:

- Native comparison report: `36a3643070591a4c70c63e9af8265e43b02e0c43e6762afa5e810a2c687c7214`.
- Independent audit: `b4cf5c4bcd7824c1e6f77ca02a816506deea6e5deff0b9da420da6792f14d80d`.
- Launch manifest: `18fe4ad03ee91f03228fc6fdb495c20d71941901425acb3acdf6b09da13105aa`.

## Observer analysis: direct review of Sol's code and experiment

This is a post-trial observer review requested by the user, distinct from the
agent's own report and the artifact audit. No bot files were edited and no games
were rerun. The review read all 203 lines of both candidate versions, their full
diff, commands, experiment notes and reports, four result/summary records, and
relevant pinned API/rules. The complete Java diff is one constant at line 12:
`ANCHOR_START = 300` becomes `30`. No additional persisted authored Java, Python
or shell helpers were found under the candidate/work directories; the supplied
launcher, extractor and fixture are infrastructure, not Sol-authored code.

**Assessment:** good execution of the narrow legal-working-bot and truthful
local-diagnostic brief; a readable, competent prototype with modest strategic
depth. The experiment was sensible and well controlled, but shallow in explaining
why outcomes changed. Choosing the changed candidate is provisional, not a
robust improvement claim. This assessment does not compare Astra's code quality.

Source references below refer to `islandbound/RobotPlayer.java` in the preserved
baseline `build-001/source` and changed `build-002/source` artifacts; line numbers
are identical in both versions. The earlier recorded source hashes identify the
exact reviewed versions. The source itself remains private.

### What it did well

The bot has a coherent headquarters/carrier flow, guarded controller actions,
load/unload handling, deterministic ID-seeded exploration, and a finally-yield
loop that preserves liveness after caught exceptions (lines 21–35, 114–143).
Array/encoding choices fit the pinned 60×60 map, 35-island, four-HQ and 64-shared-
slot limits. It checks shared-write permission and movement legality. Lack of
combat and replacement of lost carriers limits competitiveness, but does not
violate the narrow kickoff. Its reports explicitly avoid equating successful
games with exception-free execution or full replay understanding.

### Priority findings

1. **Medium: anchor supply is not tied to delivery demand.** Headquarters build
   when their stored anchor count is zero (68–69); every eligible empty returning
   carrier takes one (124–128). An anchor-carrying unit exclusively delivers or
   explores, with no cancellation/return policy or reservation/in-flight cap
   (117, 146–159). Baselines built 20/19 anchors, picked up 18/18 and placed 5/5;
   changed games built 14/16, picked up 12/16 and placed 5/5. Under the pinned
   rules, an anchor fills the carrier's 40 kg capacity and costs 100 adamantium
   plus 100 mana. Excess assignments therefore divert mining capacity and spend
   resources. These facts do **not** establish the cause of the B-side regression.
2. **Medium: island state conflates neutral and enemy-held.** Lines 99–100 store
   only whether an island is ours, and 155–159 target the nearest island that is
   not ours. Placement at 148 requires neutral ownership. This can prioritize
   an enemy-held island over neutral alternatives without an explicit threat or
   siege policy. It was not exercised by the inert fixture. The rules allow
   occupancy-based enemy-anchor decay, so this is **not** a claim of permanent
   deadlock. Relevant pinned references: RobotController 990–993 and rules 136.
3. **Medium: remembered discoveries lack a later publication path.** Lines
   91–102 publish currently visible islands only; 103–110 read shared values.
   Discoveries made outside communication range are not explicitly flushed when
   the carrier later returns to write range, and older shared values can overwrite
   nonvisible local knowledge without freshness metadata. This weakens team
   information sharing. Relevant write-range references: rules 148 and
   RobotController 1027–1049. It is a code-path finding, not a measured cause of
   one particular game's duration.
4. **Low/medium: movement uses an approximate current model.** The loop permits
   two moves (176), while each move candidate is scored using a hypothetical
   current-pushed landing (184–193). Pinned rules 58 apply currents at end of
   turn, after movement, so the first candidate's pushed location need not be
   the actual intermediate state. This is a heuristic approximation, not an
   illegal action: movement legality and actual position are still checked.
   There is no full pathfinder, target reservation or threat avoidance. The
   provided replay summaries do not establish that this caused the regression.

### Was the improvement test well chosen?

Yes as a first local probe: the original code deliberately prevents anchors
before round 300, so testing an earlier gate addresses an obvious constraint.
The one-line change, fixed map/engine identities, identical fixture and matched
A/B positions make the test easy to interpret at the outcome level. The
prediction is falsifiable, and its rationale already recognizes the risk of
stranding miners with anchors (`001-prediction.md`, lines 18–31). Predicting five
placements adds little beyond the capture-victory condition.

The experiment measures outcome, not mechanism. It does not extract first-anchor
and placement timelines, carrier roles, or delivery/mining allocation traces.
That leaves the 140-round A improvement and 11-round B regression unexplained.
Sol correctly rejects its joint prediction (`001-result.md`, 6–18) and admits
those analysis limits (32–38). It then introduces the lower-mean selection
criterion after the joint prediction failed (20–24), rather than using a
predeclared acceptance objective. Selecting a 319.5-round mean over 384 while
accepting a worse maximum is a defensible local preference, but only provisional.

The next stronger test would specify the selection objective beforehand, inspect
allocation/timing evidence, and cover distinct scenarios or seeds. Identical
reruns are not automatically independent evidence: the pinned rules describe
reproducible identical matches, with the separately documented final coin-flip
exception. ID-seeded random exploration and changed RNG consumption following a
policy change are part of this implementation's behavior, not by themselves an
uncontrolled experimental confounder.

Overall, the review supports confidence in Sol's basic implementation and candor.
It does not yet support confidence in competitive strategy or deep causal replay
analysis. These are observer findings and proposed evaluation improvements, not
changes to the frozen candidate or the approved implementation plan.

## Observer analysis: direct review of Astra's code and experiment

This separate post-trial review read all 205 lines of both Java versions, their
complete diff, the authored `inspect_results.py`, experiment/selection notes,
commands, report and README, all four result/summary/log sets, build/package
manifests, fixture and relevant pinned rules/API. It used read-only comparison
and hash inspection: no edits, reruns, installations or coaching. Source-line
references below apply to `mybot/RobotPlayer.java` in both retained build source
snapshots; only line 8 differs. The selected editable source and ZIP match the
baseline. Raw candidate source remains private.

**Assessment:** Astra built a compact, rule-aware capture bot and handled a failed
experiment cleanly. Its strongest work is test honesty, scope control and artifact
handling. Its principal implementation weakness is allocating anchors without
allocating useful courier jobs, while communication freshness and local movement
remain brittle. This is a competent response to the narrow legal-bot/local-
diagnostic brief, not proof of a strong tournament strategy or model superiority.

### Priority findings

1. **Medium: surplus anchors and courier overcommitment.** Headquarters produce
   exactly three carriers over their lifetime, then replace any stored anchor
   that is taken (51–69). Empty carriers take anchors without a demand check,
   destination reservation or minimum mining workforce (115–124, 129–134).
   Anchor carriers exclusively deliver, with no return-anchor path (108,
   148–165). One stored anchor per HQ does not limit anchors already in transit.
   Observed builds/pickups/placements are 16/13/5 and 15/13/5 for the baselines,
   and 16/13/5 and 9/7/5 for the revisions. Each game records nine own spawns and
   only the three fixture-HQ death records. Given that code has no returns or
   other disposal path, accounting implies eight of nine carriers still hold
   anchors at the end of each baseline and revised A, versus two in revised B.
   Corresponding stored counts are three, two, three and two. These are
   **accounting deductions**, not decoded end-state observations. Baseline A's
   eleven unplaced anchors represent 1,100 adamantium plus 1,100 mana committed
   at finish (pinned Anchor.java 16; rules 132–134). This establishes surplus
   allocation, not the missing temporal cause of revised A's slowdown.
2. **Medium: shared reads can erase newer unpublished ownership knowledge.**
   `updateKnowledge` imports every nonzero shared record before sensing nearby
   islands and attempting publication (81–101). A newer ownership observation
   made outside communication range can therefore be overwritten by an older
   shared value on a later turn after leaving vision, before the carrier reaches
   a relay. No timestamp, version or dirty-local flag protects it. The finding
   is conditional: a newly discovered island whose shared entry is zero remains
   cached; current-turn visible data takes priority; successful own placement
   explicitly writes ownership (149–155). It is not true that all scouting data
   is lost. The inert fixture does not exercise enemy ownership changes, and
   this defect is not an established cause of those timings. Write-range rules:
   pinned rules 146–148 and RobotController 1027–1051.
3. **Low/medium: navigation is a thoughtful local heuristic, not robust routing.**
   The move loop checks legality/cooldown, scores eight directions, randomizes
   ties, penalizes recent visits, and considers distance, clouds, currents and
   sensed enemy HQ danger (176–203). The HQ penalty is grounded in the pinned
   passive-damage rule: four damage within squared radius nine, despite HQs not
   being active attacking units (rules 70, 202, 206). However, each of up to two
   voluntary moves is scored using a current-shifted endpoint (178, 191), while
   currents apply after voluntary movement (rules 58). Estimated endpoints check
   boundaries/passability but not robot occupancy (192), and there is no global
   obstacle routing. Recent-visit penalties can outweigh several tiles of goal
   distance. Placement is checked before movement only (149–165), so arrival
   does not trigger same-turn placement and a current could move a carrier off
   the island first. These are code-path limitations, not verified failed paths
   or replay-derived explanations of the regression.
4. **Scoped strategic limitations: crude economy and no recovery/combat policy.**
   Resource preference starts from ID parity, flips after a completed return,
   and searches only the preferred resource (24, 115–141). There is no inventory-
   demand balancing, shared well allocation, fallback resource or congestion
   control. Carriers choose the nearest known HQ at their current position
   (75–79); with isolated HQ stockpiles, per-carrier alternation does not guarantee
   the needed balance at each HQ. Lifetime production counters never replace
   losses (51, 65); there are no combat units or mobile-enemy avoidance. These
   limits are disclosed and do not violate the narrow kickoff.

### Strengths and rule correctness

Capacity and empty-before-anchor handling match the 40 kg rules. Build, transfer,
collect, take, place and move operations use legality checks. Neutral-only island
placement avoids wasting anchors replacing allied ones, even though the API
allows that replacement. Encoding, owner bits, array sizes and shared-array slot
choices fit the pinned limits; shared writes are range-gated. Per-robot static
state is legitimate, loops are bounded, and the finally-yield loop preserves
progress after handled controller exceptions (25–33). It catches
GameActionException, not arbitrary runtime errors; successful matches still do
not prove no exceptions or bytecode overruns. No disqualifying legality defect
was found in this review.

### Experiment and selection judgment

The entire candidate change is `ANCHOR_START_ROUND = 150` to `1` at line 8.
Three-carrier production and resource checks remain unchanged. All four games
share the same pinned engine, fixture and map identity
`a53211fc3fb4cc6427693f6f65b0732cc4bdf9ecb90f911ffbd71b5af82bb910`,
with matched A/B slots and verified replay hashes. This is a clean first probe
of a deliberate opening delay. The prediction explicitly requires faster
capture on each side and anticipates lost mining labor as a possible downside
(`001-prediction.md`, 10–27).

Astra correctly reports that 362/235 baseline rounds versus 448/143 changed
rounds refute the both-sides prediction. The 143-round B finish logically proves
that game's five placements preceded round 150; it does not reveal exact first-
anchor timings. Sampled action counts and net resource deltas cannot establish
throughput or navigation quality. `inspect_results.py` correctly checks artifact
status, replay hashes and selected-source/package identities (14–39), but is an
artifact-consistency audit, not a semantic or causal test.

Retaining the baseline for its lower observed worst-side duration, 362 versus
448, is a reasonable conservative choice after the failed proposal. The minimax
criterion appears after outcomes, rather than as a preregistered optimization
objective. A mean objective would instead marginally prefer the revision, 295.5
versus 298.5; neither establishes a uniquely best version or model strength.
The result note explicitly labels suggested routing/allocation explanations as
hypotheses (20–35). Broader distinct scenarios and causal traces would improve
the evaluation; identical deterministic reruns are not independent statistical
replicates. Those further tests were outside the completed workflow and were not
run for this review.

Stopping after four games and a completed workflow followed the trial stop rule;
twenty minutes was a ceiling, not an obligation to continue optimizing. Overall,
Astra demonstrated solid small-program engineering and disciplined handling of
negative evidence, with much less evidence of adaptive strategy. This is observer
analysis only, not a change to the bot, approved plan or comparison result.
