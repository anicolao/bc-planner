# Battlecode 2023 experiment plan

**Status: proposed implementation for Alex's review.** This PR adds a plan only. It does not implement or deploy a runner, schedule scrimmages, change authentication, or provision services.

## Outcome and boundaries

Build two usable paths for the **2023 tournament edition**:

1. Build our own bot and run local, headless games with the official BC23 engine, then understand the resulting replay.
2. Submit frozen bot versions to our own **replica of Battlecode's competition infrastructure**, schedule scrimmages through its API, and retrieve durable results and replays.

“Local” means execution in the selected development runtime, initially our cloud runtime; it does not require Alex's Mac or remote-desktop access. The replica is a private test installation with synthetic teams and our artifacts, not the live Battlecode service. A local batch script alone does not meet the second requirement. Conversely, running a dashboard whose queue silently does nothing does not count as a working replica.

This plan derives from Alex's 2023 repository, the official 2023 engine and competition backend, and the existing bcenv architecture sketch. [Terry's observational review](terry-battlecode-prior-art.md) is background evidence, not authority for this system's direction. Replay understanding is the central requirement of our existing [learning architecture](battlecode-learning-architecture.md), also reflected in bcenv, and is a deliverable from the first runnable experiment. The existing learning loop requires a recorded behavioral prediction before a candidate change and replay-based verification afterward; this plan supplies its 2023 execution and evidence paths.

## Evidence and what can be reused

Inspected source snapshots on 2026-10-16; no engine, bot, viewer, or infrastructure execution is claimed by this document.

| Source | Verified snapshot and findings | Reuse / gap |
| --- | --- | --- |
| Alex's prior repository | [`anicolao/battlecode2023`, `85af2296`](https://github.com/anicolao/battlecode2023/tree/85af2296cad95443aad3925929fca70aacb650eb). Its README identifies BC23; `build.gradle` uses `org.battlecode:battlecode23`; `version.txt` is **2.0.3**; output is `.bc23`. | Correct 2023 repository, not a similarly named later-season project. Reuse bots, test inputs, and historical workflow. Private source links require repository access. |
| Local build | [Build configuration](https://github.com/anicolao/battlecode2023/blob/85af2296cad95443aad3925929fca70aacb650eb/build.gradle): Java 8 target, Scala 2.11.7 dependency, Gradle wrapper 7.6, `verify`, headless `run`, explicit team classpaths/packages/maps/replay, and `zipForSubmit`. | Good execution contract; dependency acquisition and client download are coupled to `build`. `update` consults a live episode API and must not silently change a measured environment. README's `zipForUpdate` differs from the actual task name. |
| Bots and harness | [`src/java`](https://github.com/anicolao/battlecode2023/tree/85af2296cad95443aad3925929fca70aacb650eb/src/java) includes `submission`, `jumbled`, `nullbot`, lecture and example players. [`Battle.java` and fixtures](https://github.com/anicolao/battlecode2023/tree/85af2296cad95443aad3925929fca70aacb650eb/src/javatests/battlecode) load engine properties and call `battlecode.server.Main.run`. There are 16 `.in` files, despite the README's older “one test” description. | Adapt useful fixture coverage; remove machine-specific `/home/dev/scaffold` paths. Current defaults refer to `submission_0115`, absent from the inspected source tree, so choose an explicit existing opponent. `stats` scrapes logs; it is not a typed replay-analysis or competition API layer. |
| Historical viewer | [README](https://github.com/anicolao/battlecode2023/blob/85af2296cad95443aad3925929fca70aacb650eb/README.md), [`devcon/setup`](https://github.com/anicolao/battlecode2023/blob/85af2296cad95443aad3925929fca70aacb650eb/devcon/setup), and [`devcon/viewer`](https://github.com/anicolao/battlecode2023/blob/85af2296cad95443aad3925929fca70aacb650eb/devcon/viewer) build the official schema/playback/visualizer and forward its server on port 8080. | Existing replay-viewing precedent. Historical setup uses an unpinned clone, apt/npm installation and SSH forwarding; inspect it, do not run it as our installer. Test the unusual tournament-mode replay URL rather than assuming it works unchanged. |
| Official BC23 implementation | [`battlecode/battlecode23`, tag `2.0.3`, commit `5d142a87`](https://github.com/battlecode/battlecode23/tree/5d142a87579af22c2c04ce046a3cbd448dc1869e): engine, maps, Java API, replay schema, playback and visualizer. | Start with the historical bot's engine version. A later BC23 revision is a separately labeled experiment, not a silent upgrade. This is a season implementation, not the scrimmage service. |
| Official competition infrastructure | [`battlecode/galaxy`, `51762ec8`](https://github.com/battlecode/galaxy/tree/51762ec8b982132c250aa5a603978bc7147eae67), the last repository commit before 2023-02-01, dated 2023-01-30. | Use as the initial 2023-era source baseline. Its date does **not** prove which commit production deployed. Current Galaxy has later language and development changes; do not pass those off as 2023 behavior. |
| Existing architecture | [`bcenv`, `7f868dc5`, INITIAL_DESIGN_SKETCH.md](https://github.com/anicolao/bcenv/blob/7f868dc561667a336e7eeba65ea89167d7716fa1/INITIAL_DESIGN_SKETCH.md) describes supervisor/competitor separation, Nix season tooling, frozen evaluations, replay analysis, durable records and recovery. | Architectural starting point, not evidence those services exist. This experiment can prove the season and evaluation path before multi-VM provisioning or autonomous campaigns. |

### What “replica” must include

The 2023 Galaxy source separates the Django **Siarnaq** backend from the Go **Saturn** compiler/executor and **Titan** upload scanning. Relevant verified behavior:

- [Competition models, managers, views and routes](https://github.com/battlecode/galaxy/tree/51762ec8b982132c250aa5a603978bc7147eae67/backend/siarnaq/api/compete) represent submissions, scrimmage requests, matches, participants, statuses and results. Accepting a request selects active submissions and constructs the match. A request and its executed match are distinct records.
- [Saturn payloads and status/report handling](https://github.com/battlecode/galaxy/tree/51762ec8b982132c250aa5a603978bc7147eae67/saturn/pkg/saturn) carry an episode, task type, report URL and details; Pub/Sub dispatches work, and HTTP callbacks update the backend. Queue delivery can retry.
- [Java 8 worker recipes and storage interfaces](https://github.com/battlecode/galaxy/tree/51762ec8b982132c250aa5a603978bc7147eae67/saturn/pkg/run) download source, verify/build it, store a binary, execute games from binaries, upload replay, and report scores. Storage is expressed as bucket/name references; production uses GCS. Separate interfaces exist for queue, storage and reporting.
- The worker calls `update -PonSaturn=true`, accesses protected release configuration, and expects cloud-backed authentication. These need explicit local replacements. Do not request MIT credentials or connect to its production project.
- [Development backend settings](https://github.com/battlecode/galaxy/blob/51762ec8b982132c250aa5a603978bc7147eae67/backend/siarnaq/settings.py) use SQLite and disable cloud actions; the [publisher](https://github.com/battlecode/galaxy/blob/51762ec8b982132c250aa5a603978bc7147eae67/backend/siarnaq/gcloud/saturn.py) then returns a `NullPublisher`. Starting that mode alone produces no real worker jobs.

**Proposed fidelity boundary:** reuse the historical backend's domain/API and Saturn's compile/execute protocol and recipes; replace cloud-specific queue, object storage, reporting authentication and release lookup with explicitly documented local adapters. Preserve payloads and lifecycle semantics with contract tests. This is an adapted local replica, not an assertion of byte-for-byte production equivalence. A bespoke scheduler that merely resembles the API is not the default proposal. Whether a Pub/Sub emulator or a durable local queue is preferable is a phase-0 decision; neither may be presented as production Pub/Sub validation.

## Phased implementation

Each phase should be a separately reviewable implementation PR. Paths and command names below are proposed contracts, not installed commands. No phase authorizes paid infrastructure, production API calls or credential changes.

### 0. Freeze scope and dependency manifest

**Inputs:** the source inventory above and Alex's review of this plan.

1. Record repository revisions, licenses, target `x86_64-linux`, engine/scaffold/client/schema compatibility, map identities and exact dependency hashes in a BC23 season manifest. Start from engine 2.0.3; verify release artifact identity against its source tag rather than assuming equivalence.
2. Identify and pin the official BC23 scaffold revision compatible with the worker. Audit differences against Alex's scaffold, particularly `alternateOrder`: Saturn supplies this property, and the official engine has `bc.server.alternate-order`, but Alex's inspected `run` task does not forward it. Either add/test the bridge or explicitly run both sides as separate jobs.
3. Extend the repository's pinned Nix flake through normal review for Java, Gradle/dependency closure, Node/client tools, Python/backend, Go/worker and the chosen local services. Resolve dependencies using the approved Nix workflow; do not run historical apt, Conda or direct npm setup scripts. The present flake only exposes OpenSSH, Go and Tailscale, so it is not already a BC23 environment.
4. Inventory all production URLs, buckets, email/scanning/bracket/rating side effects and authentication assumptions in the selected Galaxy revision. Define local-only replacements, synthetic accounts and a no-production-egress test. Record intentionally omitted services and any resulting fidelity limits.

**Acceptance:** reviewable manifest and dependency plan; every source pin and downloaded artifact has an identity; local endpoints are explicit; no production secrets are needed. Decide queue/storage strategy and the implementation repository before coding.

### 1. Reproduce one local build and game

**Depends on:** phase 0.

1. Create a Nix-managed BC23 environment and a clean, disposable workspace from the frozen source. Preserve the original checkout as evidence. Separate headless compilation/execution from optional GUI setup; retain official engine verification.
2. Compile `submission` and a known existing baseline, initially `nullbot` or `examplefuncsplayer`. Invoke explicit packages, class locations and a verified map; do not rely on stale `gradle.properties` defaults. Adapt one historical fixture, then the remaining applicable fixtures.
3. Capture source and binary hashes, engine/map/config identities, command and environment, exit status, stdout/stderr, elapsed time and the `.bc23` file. Use unique run directories instead of overwriting the historical name template. Package only intended bot sources and verify the package matches the evaluated candidate.
4. Keep dependency fetching outside match execution. After preparing the dependency closure, demonstrate a run with external network access disabled.

**Acceptance:** a clean build and legal headless match produce an intact replay; invalid source and invalid package fail clearly; two concurrently launched runs do not collide. Repeat an identical frozen case and compare normalized outcome/event data, explaining nondeterministic metadata instead of promising byte-identical archives. Report failed, unknown and incomplete runs separately from losses.

### 2. Make the replay understandable

**Depends on:** phase 1; required before broad evaluation.

The [BC23 2.0.3 schema](https://github.com/battlecode/battlecode23/blob/5d142a87579af22c2c04ce046a3cbd448dc1869e/schema/battlecode.fbs) and [GameMaker](https://github.com/battlecode/battlecode23/blob/5d142a87579af22c2c04ce046a3cbd448dc1869e/engine/src/main/battlecode/server/GameMaker.java) define a GZIP-compressed FlatBuffer `GameWrapper` with game/match headers, round events and footers. The schema README still says `.bc22`; use BC23 source and actual fixtures rather than that stale extension. Round data includes resources, movement, spawning/deaths, actions, islands, wells, indicators and bytecodes. This is event/state data, not a guaranteed record of a bot's intentions.

1. Build a versioned extractor using the matching generated schema, preserving the original replay. Emit typed summaries with team identity, map, rounds, winner and an explicit completeness flag. Map team IDs and player slots to candidate identities, including side swaps and multiple games in one replay.
2. Reconstruct selected round snapshots and timelines: economy, robot population, island ownership, movement and actions. Produce a concise match explanation supported by specific rounds/events; distinguish observed events from inferred causes and unavailable metrics. Do not turn missing data into zeros.
3. Make the pinned official viewer open the same artifact, and link report observations to reproducible replay positions. A headless extractor must work even when browser access is unavailable; viewer usability remains a separate acceptance check.
4. Record debug/indicator/profiler settings. Distinguish full-replay knowledge from observations available to the bot. Validate important conclusions with competition-like settings, not just debug runs.

**Acceptance:** extractor and official playback agree on winner, rounds and selected state snapshots for known fixtures; include a Team B win, side-swapped series, truncated/corrupt file, schema mismatch and absent optional data. Check errors and validity flags. A reviewer can answer what happened and where it went wrong from the report and replay, not just read a win-rate number.

### 3. Bring up the local competition replica

**Depends on:** phases 0–2.

1. Run the pinned Siarnaq backend with its migrations and synthetic BC23 episode/teams/maps. Keep accounts and artifacts private to the test installation. Choose database behavior deliberately: SQLite is a development starting point; verify locking and query compatibility, and use a local PostgreSQL service if required for concurrent semantics.
2. Connect submission and scrimmage endpoints to a real local queue. Implement/test narrowly scoped adapters for artifact storage and callbacks around the historical interfaces. Ensure callbacks target only the replica and cannot be redirected to arbitrary destinations.
3. Adapt Saturn's Java 8 pipeline to the frozen scaffold and release bundle: source upload → verified compilation → immutable binary → request acceptance → queued match → execution → stored replay → callback → queryable result. Never perform a live `update` during a job. Retain official task/status meanings and document extensions.
4. Keep archive validation, resource limits and isolation in the initial path. Decide whether Titan can be run locally or whether trusted self-owned fixtures use an explicit restricted bypass. The latter excludes untrusted uploads and is a documented fidelity/security limit, not equivalent scanning.
5. Establish trusted worker boundaries: no production credentials, no inherited GitHub token in build/game processes, no host Docker socket, bounded CPU/memory/time/output and unique workspaces. The engine verifier is not an OS sandbox.

**Acceptance:** through the replica API, submit two versions, observe compilation acceptance/rejection, create and accept a scrimmage, observe execution, and download a replay that phase 2 can analyze. No `NullPublisher` fallback is allowed. Test invalid packages, oversized/malformed archives, unauthorized access and callback rejection. Verify network traces/configuration show no calls to official competition or cloud services. Frontend polish, public signup, tournament brackets and ratings are outside the initial critical path; omitted behavior must be listed.

### 4. Schedule durable scrimmage experiments

**Depends on:** phase 3.

1. Add a small client to submit an explicit batch matrix (candidate revisions × opponents × maps × side order) through the replica, then poll/read results with a durable cursor. Freeze selected submission IDs; do not let later “active submission” changes alter an already scheduled experiment.
2. Support queued execution and an optional `not-before` time in the experiment coordinator. Timed scheduling is our extension unless the historical backend proves it supports it. Keep admission, concurrency and retry limits explicit. Separate experiment IDs, logical match IDs and attempt IDs.
3. Reconcile lost acknowledgments before resubmitting. Persist dispatch, artifacts and terminal outcomes; make duplicate callbacks safe and stop retrying invalid bots. Test worker death, queue redelivery, backend restart and interrupted replay uploads. Quarantine conflicting results rather than silently overwrite them.
4. Aggregate per-map and per-side results, preserve failures and exclusions, and connect each result to the replay explanation. Compare the same immutable input through direct execution and the replica worker. Explain any flag, ordering or packaging differences before interpreting strength.

**Acceptance:** an unattended batch survives restart, reaches a documented terminal state for each logical match and has no duplicate counted outcomes. A scheduled job does not start before its requested time. A changed bot cannot be silently substituted. Direct and queued paths agree on normalized game results for the parity suite. The report includes denominator, unknowns/failures, provenance and working replay references.

### 5. Demonstrate the complete 2023 loop

**Depends on:** phases 1–4.

Run a bounded experiment comparing two frozen versions of our bot against declared baselines on an explicit map/side suite. Use replay evidence to propose one bot change, then separately authorize and evaluate that change; this plan does not prescribe a strategy. Deliver a single runbook for local build/run/analyze and replica submit/schedule/collect/analyze, a dependency manifest, recovery instructions, a result report, and an honest fidelity matrix against historical Galaxy.

**Completion gate:** Alex can reproduce a local run and an API-scheduled scrimmage from clean setup, inspect both replays, trace every outcome to exact code, and see what remains different from official infrastructure. Local replica results are not official tournament results or evidence of a tournament ranking.

## Decisions for review and sequencing

- **Proposed first version:** reproduce 2.0.3 first. Evaluate later BC23 releases separately after a working baseline; do not conflate tournament edition with a specific patch.
- **Proposed replica:** adapt 2023-era Galaxy with local service adapters. Choose Pub/Sub emulator versus durable local queue, artifact storage implementation, and database after the phase-0 compatibility inventory. Preserve contracts and label service differences.
- **Repository ownership:** keep this review document in bc-planner. Confirm whether implementation belongs in bcenv, a dedicated runtime repository, or bc-planner before implementation starts; preserve upstream licenses and avoid publishing private bot sources accidentally.
- **Initial security/scope:** self-owned test bots, synthetic users, no external submissions. Public/multi-user hosting, full Titan integration, ratings/brackets, cloud deployment and expanded access need separate scope and approval.
- **Existing supervisor design:** expose stable run/submit/status/artifact interfaces that bcenv can later supervise. Do not make multi-agent orchestration or VM provisioning prerequisites for proving the two requested paths.

The critical path is **freeze environment → local game → replay understanding → replica lifecycle → durable scheduled batch → parity demonstration**. Broad strategy search and scalable deployment come after those gates.

## Verification of this planning change

Research used repository source inspection, including the historical engine tag and a dated Galaxy revision. It did not run installation scripts, download BC23 runtime dependencies, compile bots, replay games, deploy infrastructure or submit jobs. The implementation acceptance checks above are proposed future checks, not passing results. PR-level prompt-history and documentation checks are reported in the PR.
