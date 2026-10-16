# Battlecode 2023 experiment plan

**Status: proposed implementation for Alex's review.** This PR adds a plan only. It does not implement or deploy a runner, schedule scrimmages, change authentication, or provision services.

## Outcome, ownership and experimental question

**Can a truly fresh agent use only a pinned bcenv release and an explicit kickoff prompt to autonomously build, test, explain and improve a Battlecode 2023 competitor, then submit it and schedule scrimmages on our replica?** The experiment evaluates the environment and its instructions through the agent's observable behavior. It is not an experiment in a parent agent coaching a bot to completion.

- **bc-planner** owns this plan, research, evaluation specifications and tooling about building/evaluating the LLM environment. It does not become the competitor repository or runtime distribution.
- **bcenv** implements and packages the self-contained environment, pinned season tooling, local execution and replica services, skills, agent-facing runbooks and trial launch contract. Environment builders work here, using bc-planner's research and evaluation requirements.
- **The fresh competitor agent** reads bcenv, creates its own competitor in a disposable trial workspace, chooses and implements strategy, runs experiments, interprets replays, improves its code, freezes a candidate and uses the supplied submission/scheduling interfaces. Builders do not write or patch that candidate on its behalf.
- **The observer/evaluator** starts the agent once, records permitted objective evidence and scores the frozen trial after it ends. No inherited conversation, hidden parent context, additional hints, manual candidate edits, corrective tool results or mid-run rescue are permitted. If the agent or environment fails, end and classify that trial, revise bcenv, and start a new agent from a clean workspace.

Both requested capabilities are mandatory: **local headless BC23 games with understandable replays**, and **API submission and scheduled scrimmages against a replica of Battlecode's competition infrastructure**. “Local” means the selected development runtime, initially our cloud runtime, not Alex's Mac. A local batch script alone is not the replica; a dashboard backed by a non-executing queue is not a working service. Use synthetic teams and private artifacts, never the live Battlecode service.

[Terry's observational review](terry-battlecode-prior-art.md) is background evidence, not authority for direction. The [learning architecture](battlecode-learning-architecture.md) supplies the replay-based learning requirement: the competitor must record its behavioral prediction before its own candidate change and check it against replay evidence afterward. Historical bots are declared fixtures/opponents or disclosed starting material, not an undisclosed builder-authored solution. This plan's default is a minimal scaffold plus fixed opponents, with Alex's old strategies retained as research/opponent evidence rather than copied into the candidate.

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
| Existing architecture | [`bcenv`, `7f868dc5`, INITIAL_DESIGN_SKETCH.md](https://github.com/anicolao/bcenv/blob/7f868dc561667a336e7eeba65ea89167d7716fa1/INITIAL_DESIGN_SKETCH.md) describes supervisor/competitor separation, Nix season tooling, frozen evaluations, replay analysis, durable records and recovery. | Architectural starting point, not evidence those services exist. Use it to design bcenv; the actual acceptance experiment must still launch a fresh autonomous competitor. Multi-VM scaling is not required for the first trial. |

### What “replica” must include

The 2023 Galaxy source separates the Django **Siarnaq** backend from the Go **Saturn** compiler/executor and **Titan** upload scanning. Relevant verified behavior:

- [Competition models, managers, views and routes](https://github.com/battlecode/galaxy/tree/51762ec8b982132c250aa5a603978bc7147eae67/backend/siarnaq/api/compete) represent submissions, scrimmage requests, matches, participants, statuses and results. Accepting a request selects active submissions and constructs the match. A request and its executed match are distinct records.
- [Saturn payloads and status/report handling](https://github.com/battlecode/galaxy/tree/51762ec8b982132c250aa5a603978bc7147eae67/saturn/pkg/saturn) carry an episode, task type, report URL and details; Pub/Sub dispatches work, and HTTP callbacks update the backend. Queue delivery can retry.
- [Java 8 worker recipes and storage interfaces](https://github.com/battlecode/galaxy/tree/51762ec8b982132c250aa5a603978bc7147eae67/saturn/pkg/run) download source, verify/build it, store a binary, execute games from binaries, upload replay, and report scores. Storage is expressed as bucket/name references; production uses GCS. Separate interfaces exist for queue, storage and reporting.
- The worker calls `update -PonSaturn=true`, accesses protected release configuration, and expects cloud-backed authentication. These need explicit local replacements. Do not request MIT credentials or connect to its production project.
- [Development backend settings](https://github.com/battlecode/galaxy/blob/51762ec8b982132c250aa5a603978bc7147eae67/backend/siarnaq/settings.py) use SQLite and disable cloud actions; the [publisher](https://github.com/battlecode/galaxy/blob/51762ec8b982132c250aa5a603978bc7147eae67/backend/siarnaq/gcloud/saturn.py) then returns a `NullPublisher`. Starting that mode alone produces no real worker jobs.

**Proposed fidelity boundary:** reuse the historical backend's domain/API and Saturn's compile/execute protocol and recipes; replace cloud-specific queue, object storage, reporting authentication and release lookup with explicitly documented local adapters. Preserve payloads and lifecycle semantics with contract tests. This is an adapted local replica, not an assertion of byte-for-byte production equivalence. A bespoke scheduler that merely resembles the API is not the default proposal. Whether a Pub/Sub emulator or a durable local queue is preferable is a phase-0 decision; neither may be presented as production Pub/Sub validation.

## Implementation plan: prepare bcenv before launching a competitor

All phases below are proposed, separately reviewable implementation PRs. **Environment implementation belongs in bcenv.** Evaluation specifications and research belong in bc-planner, with the exact agent-visible materials exported into the bcenv release. No phase authorizes paid infrastructure, production API calls, credential changes or a trial launch now. Paths/commands are proposed interfaces, not existing capabilities.

### 0. Define and freeze the environment contract

**Builder work in bcenv:**

1. Add a BC23 season manifest covering source revisions, licenses, target `x86_64-linux`, engine 2.0.3, scaffold, client/schema compatibility, maps, dependencies and artifact hashes. Verify release artifacts against their pinned sources. Pin an official scaffold revision; do not treat Alex's customized scaffold as automatically worker-compatible.
2. Provide a Nix flake/lock and reproducible dependency closure for Java, Gradle, Node/viewer tooling, Python/backend, Go/worker and selected local services. The inspected bc-planner flake exposes only OpenSSH, Go and Tailscale, so it is not a BC23 runtime. All tooling installation/dependency acquisition must use the approved pinned Nix workflow; do not run historical apt, Conda or direct npm installer scripts.
3. Package a minimal legal scaffold, Java API/rules documentation, verified maps and fixed baseline opponents separately from the writable candidate workspace. Disclose every included example. Declare whether a trial is scaffold-only or reuses a supplied candidate; never compare those as equivalent starting conditions.
4. Inventory production URLs, buckets, release lookup, authentication, email/scanning/bracket/rating side effects. Replace with local-only adapters and synthetic fixtures. Choose queue/storage/database after compatibility testing; record fidelity limits. No MIT or production credentials are required.
5. Define release layout: `seasons/2023/manifest`, `skills/`, `runbooks/`, `fixtures/`, `prompts/`, tool entry points and a machine-readable trial specification. These are proposed bcenv paths. Keep evaluator-only fixtures, scores and revision diagnoses outside the competitor-visible release.

**Gate:** another builder can materialize the same release from its pins with no undocumented setup; all competitor-visible dependencies/docs are included or explicitly pinned resources. Freeze the allowed tool/network interface. If a prerequisite is unavailable, label setup blocked rather than asking the competitor to improvise infrastructure.

### 1. Package reliable local execution and replay capabilities

**Builder work:** provide and test tools the competitor can invoke, not a finished competitor.

- Expose build/verify/package/run interfaces with explicit source, package, classpath, map, side order and replay destination. Separate headless execution from optional GUI setup. Remove historical absolute paths and stale `submission_0115` defaults. Preserve official verification and package only intended sources.
- Audit `alternateOrder`: Saturn supplies it and the engine has `bc.server.alternate-order`, but Alex's inspected task does not forward it. Test the bridge or run each side explicitly. Freeze engine/config behavior identically for direct and worker paths.
- Use unique run directories and typed results with source/binary/engine/map/config hashes, exact command, exit status, logs, timing and replay references. Distinguish loss, invalid bot, infrastructure failure and unknown outcome. Prepare dependencies before games and prove offline execution afterward.
- Build a pinned replay extractor and official viewer. The [BC23 schema](https://github.com/battlecode/battlecode23/blob/5d142a87579af22c2c04ce046a3cbd448dc1869e/schema/battlecode.fbs) and [GameMaker](https://github.com/battlecode/battlecode23/blob/5d142a87579af22c2c04ce046a3cbd448dc1869e/engine/src/main/battlecode/server/GameMaker.java) define a GZIP-compressed FlatBuffer `GameWrapper`; the schema README's `.bc22` extension is stale. Extract team/slot identities, rounds, winner, resources, movement, actions, population and island/well state with completeness flags. Do not confuse event observations with bot intentions or fill missing metrics with zeros.
- Provide round/event references and reconstruct selected snapshots. Keep headless analysis usable without browser access; official viewer support is a separate gate. Record debug/indicator/profiler settings and distinguish full replay knowledge from observations available to a robot during play.

**Builder fixture checks:** known bots compile and play; invalid packages fail clearly; concurrent runs do not collide; frozen repeats agree on normalized outcome/events or document deviations. Extractor and viewer agree on winner, rounds and selected snapshots. Cover a Team B win, side swaps, multi-game replays, corrupt/truncated files, schema mismatch and absent optional fields. These tests establish tool readiness, not autonomous-agent success.

**Competitor responsibility during a later trial:** create its candidate, select experiments, invoke these tools, explain outcomes from replay evidence and decide its own changes. Builders must not precompute its explanation or choose its next strategy.

### 2. Provision the private BC23 competition replica

**Builder work in bcenv:**

1. Package pinned Siarnaq migrations and synthetic BC23 episode/teams/maps; choose SQLite only if locking/query semantics pass, otherwise provide local PostgreSQL. Keep accounts and artifacts isolated to the test installation.
2. Wire real local queue, object-storage and callback adapters to the historical interfaces. Preserve submission/request/match/status semantics and test payload contracts. Prevent callbacks from targeting arbitrary URLs; forbid `NullPublisher` fallback.
3. Adapt Saturn's Java 8 flow to the frozen scaffold/release bundle: source upload → verified compilation → immutable binary → accepted scrimmage request → queued match → execution → stored replay → callback → queryable result. Never perform a live `update` inside a job. Explicitly document adapters and all differences from production Galaxy.
4. Include archive validation, scoped access, resource limits and isolated workspaces. Decide whether Titan runs locally or trusted self-owned fixtures use a restricted, documented bypass. That bypass excludes untrusted uploads and is not equivalent scanning. Do not inherit GitHub tokens or expose host Docker sockets; the engine verifier is not an OS sandbox.
5. Provide submission/status/artifact and scheduling clients. Persist explicit frozen submission IDs, candidate/opponent/map/side matrices, experiment IDs, logical match IDs and attempt IDs. A coordinator `not-before` time is our extension unless historical source proves otherwise. Freeze active submissions when scheduling; later edits must not substitute another bot.
6. Persist dispatch and results; reconcile lost acknowledgments before resubmitting, make duplicate callbacks safe, quarantine conflicting results, and bound retries. Invalid candidates are not retried as infrastructure failures. Preserve denominator, exclusions and replay links in aggregate reports.

**Builder fixture gate:** submit two fixture versions through the API, observe compile acceptance/rejection, schedule/accept a scrimmage, observe real execution and retrieve an analyzable replay. A timed job must not start early. Test malformed/oversized archives, authorization/callback rejection, worker death, queue redelivery, backend restart and interrupted replay uploads. Every logical match reaches a documented terminal state without double-counting. Direct and queued frozen cases agree on normalized results, with any ordering/flag differences explained. Confirm no production/cloud-service calls. Public signup, full scanning, ratings/brackets and public hosting remain excluded unless separately implemented and reviewed.

### 3. Package skills and the exact kickoff prompt

**Builder work:** write discoverable skills in bcenv that a fresh agent can follow without this conversation. Cover:

- Where to read BC23 rules/API and create a candidate from the minimal scaffold.
- How to build, verify, run local games, choose explicit opponents/maps/sides, and interpret tool errors.
- How to open/extract replays, cite rounds/events, separate observations from hypotheses, and record a prediction before changing code.
- How to freeze/package a candidate, submit to the replica, schedule scrimmages, collect terminal results and reconcile interrupted jobs within the trial budget.
- Artifact layout, honest reporting, dependency/network boundaries and stopping behavior. The agent may debug its own candidate and use documented recovery; it may not edit the pinned environment or ask the observer for strategy/setup rescue.

Skills should teach interfaces and workflow, not prescribe a winning strategy or reveal evaluation outcomes. Check skill discovery from a blank workspace. Readiness tests may use fixture bots and scripted clients; they must not be reported as a fresh-agent trial.

Store the following proposed kickoff text verbatim as a versioned bcenv asset. Trial-specific budgets/endpoints and allowed fixtures live in the pinned trial specification, not in extra parent messages. Record the actual prompt bytes and hash in every trial manifest; any later prompt revision is a new experimental input.

```text
You are a fresh autonomous Battlecode 2023 competitor operating in the supplied bcenv release. Read its entry instructions, season manifest, trial specification and relevant packaged skills. Use only this environment, its declared tools/resources and your trial workspace. Do not seek information or coaching from a parent conversation.

Create your own legal BC23 competitor from the provided starting scaffold. Build and test it locally against the declared practice opponents and maps. Inspect the resulting replays and explain observed behavior with round/event evidence. Record a concrete behavioral prediction before making a candidate change, implement your own change, and test whether the replay evidence supports that prediction. Report failures and uncertainty honestly; improvement in win rate is not guaranteed.

Freeze the candidate you choose, verify and package that exact source, submit it to the private replica, and schedule the required scrimmage suite through its API. Collect results and replays within the trial budget. Preserve the relationship between source, binary, submission, scheduled matches and replays. Follow the packaged recovery and stopping rules without changing the pinned environment or requesting manual corrections.

Leave your candidate sources, experiment/prediction log, commands and result references, submission and scheduling identifiers, and a final evidence-based report in the specified output location. Explain what succeeded, what failed, and what remains incomplete. Stop when the trial's completion or budget/failure condition is reached.
```

**Gate:** bcenv includes all instructions the prompt refers to; endpoint/resource/budget configuration is explicit and validated before launch. No references to unavailable parent notes or unpinned research are necessary to complete the task.

## Clean-room trial protocol

### 4. Freeze and launch a genuinely fresh agent

The builder/evaluator prepares the following before starting the competitor:

1. Freeze an immutable bcenv commit/release and dependency closure, trial-spec hash, kickoff prompt hash and evaluator-version hash. Allocate a unique immutable trial ID. Record model/version where available, runtime/tool configuration, sampling settings where exposed, start/budget limits, fixture/map/opponent identities and all visible inputs. Record unavailable model/runtime fields honestly; reproducible inputs do not promise identical LLM behavior.
2. Create a new agent session with **no inherited chat history or parent context**, fresh writable candidate/output directories and freshly seeded replica state. Mount the pinned bcenv package read-only. No prior candidate code, memory, transcripts, caches containing generated candidate artifacts, previous trial results or parent filesystem access may leak in. Shared immutable dependency caches are allowed only if content-addressed and incapable of carrying trial-specific information.
3. Ensure every competitor-visible file/tool response comes from the declared release and trial state. Remove unrelated credentials, connectors and internet search access; any necessary allowed network endpoints/resources must be declared in advance. Synthetic replica identities are trial-local. The observer retains no route for injecting instructions through logs, files or tool output.
4. Verify isolation, quotas, service health and fixture readiness before launch. Launch with exactly the recorded kickoff text plus the pinned bcenv content/configuration. Record any unavoidable platform/system instructions and capabilities in the manifest; an unrecorded inherited context invalidates the clean-room claim.
5. Observe until a terminal condition. No follow-up prompts, edits to the candidate or environment, suggested fixes, manual resubmissions, strategy hints or mid-run rescue. The agent's own autonomous debugging and documented retries are permitted within the fixed budget. Even a helpful human correction would invalidate this trial; terminate and restart cleanly instead.

**Fair resets:** reset queues, database, storage namespaces, accounts, candidate/output directories and session memory between trials. Restore the same baseline versions, maps, side suite, budgets and declared service resources for comparisons. Report deliberate changes and all trials, including failed starts; do not quietly discard unfavorable runs. Use a predeclared number of independent trials and success threshold in the trial spec. Compare environment revisions across independent fresh agents, not an increasingly coached long-lived agent.

### 5. Observe objectively and evaluate without leakage

Instrumentation records timestamps, process/tool calls and outputs, file/artifact hashes, resource consumption, declared candidate revisions, submissions, match attempts and terminal status. Capture externally visible behavior and deliverables; do not require private chain-of-thought. Preserve append-only observer records outside the agent-writable workspace. The agent sees its ordinary practice match results, logs and replays because replay-driven improvement is part of the task.

Keep held-out evaluation maps/opponent selection, scores, acceptance annotations and human diagnoses inaccessible until the candidate and trial are frozen. Reveal only predeclared task requirements and budgets, not hidden outcomes. Do not select trials or alter thresholds after seeing results. If the evaluator runs additional held-out games after completion, use the frozen candidate without edits; those runs measure strength/generalization separately and cannot repair missing autonomous steps.

Evaluate two layers separately:

| Gate | Required evidence |
| --- | --- |
| Environment readiness | Builder fixture checks from phases 0–3 passed for the exact release before launch. A fixture pass is not a competitor pass. |
| Clean-room integrity | Manifest accounts for all visible inputs; no inherited history, undeclared artifacts, observer edits or coaching. Any breach invalidates the trial regardless of bot strength. |
| Skill discovery and legal build | Agent found packaged guidance, authored candidate sources and produced a verified legal build using supplied tooling. |
| Local execution and replay understanding | Agent ran local games and produced correct round/event-backed observations tied to preserved replays, not only a win rate. |
| Autonomous learning loop | Agent recorded a prediction before its own code change, tested the changed version and assessed that prediction against replay evidence. A well-supported negative result counts as a valid loop; a claimed improvement without evidence does not. |
| Replica submission and scheduling | Agent froze and packaged its own candidate, obtained submission/compile identity, scheduled the required suite via the replica API and retrieved terminal results/replays. A queue receipt alone is partial progress, not completion. |
| Provenance and honest reporting | Hashes link candidate, binary, submission, matches and replay artifacts; report distinguishes failures/unknowns from losses and identifies incomplete work. |

Define numerical wall-clock/token/tool/CPU/memory/storage and match limits in the trial spec before launch, plus a predeclared collection deadline for queued scrimmages. Required workflow gates are pass/fail with explicit incomplete/invalid categories. Competitive strength is a separate metric on declared suites; do not equate functioning workflow with tournament quality or official ranking.

**Stopping and failure conditions:** stop on the agent's completion/final report; exhaustion of a declared budget or collection deadline; unrecoverable service/setup failure under documented retry limits; agent request for human help when it cannot continue autonomously; no progress beyond a predeclared timeout; safety/isolation violation; or any observer intervention/context contamination. A failed compilation or loss alone is not terminal if the agent can recover within budget. On termination, freeze outputs, stop/cancel outstanding trial jobs, snapshot statuses and mark unfinished jobs incomplete. Safety may require immediate intervention, but that run cannot count as successful autonomous completion. Classify environment defect, instruction gap, competitor failure, infrastructure failure and invalid experiment separately; preserve evidence and uncertainty about cause.

### 6. Revise bcenv, then restart from scratch

After a trial ends, evaluate its artifacts and observed workflow against the frozen rubric. Record where the packaged instructions/tooling failed to enable the intended behavior. A change to a skill, interface, dependency, fixture, documentation or kickoff prompt must be an explicit reviewed bcenv revision with a new identity and a falsifiable expectation for the next trial.

Do not fix the old candidate, resume the old agent with hints, or transplant its solution into the next workspace. Re-run affected builder fixture checks, then start a wholly new trial under phase 4. Maintain a ledger connecting environment revision → kickoff/spec hashes → trial IDs → observed failure/success → proposed revision. Keep historical reports immutable. Test general workflow improvements on held-out cases or additional fresh trials to reduce overfitting to one agent's failure; preserve comparability and disclose changed conditions.

**Completion gate for the proposed experiment:** the predeclared fresh-agent acceptance threshold is met with evidence of all workflow gates, including autonomous local build/test/replay-based iteration and replica submission/scheduling/result collection, without coaching. Deliver the pinned bcenv release, builder readiness results, exact kickoff/spec assets, clean-room launch/reset procedure, immutable trial ledger, artifact reports and honest Galaxy fidelity matrix. Alex can inspect and reproduce the setup and trial protocol. Success is an environment that enables autonomous competition, not a builder-produced bot or manually rescued demonstration.

## Decisions for review and sequencing

- **Fixed ownership:** bc-planner plans and evaluates environment construction; bcenv packages and provisions the environment/skills; the fresh agent builds the competitor. Implementation repository ownership is no longer an open choice.
- **Initial season:** BC23 engine 2.0.3, with later patches as separately pinned experiments.
- **Replica:** adapt the 2023-era Galaxy interfaces with local services. Choose queue/storage/database after compatibility checks and document deviations. Local execution and API-scheduled replica scrimmages are both required.
- **Starting material:** minimal scaffold plus disclosed fixed opponents; confirm any alternative reuse track explicitly and evaluate it separately. Preserve upstream licenses and keep private source fixtures from accidental publication.
- **Before launch:** review numerical budgets, required suite, independent-trial count/success threshold, exact kickoff, allowed tool/network surface and recovery limits. No clean-room trial is launched by this documentation PR.
- **Scope:** self-owned fixtures/synthetic users in a cloud runtime; no Mac dependency, public hosting, production services or scaling prerequisites.

The critical path is **package bcenv → validate local/replay tools and real replica lifecycle → freeze skills/prompt/trial contract → launch a fresh competitor → observe without intervention → evaluate artifacts → revise bcenv and restart fresh if needed**.

## Verification of this planning change

Research used repository source inspection, including the historical engine tag and a dated Galaxy revision. This revision preserves those findings and corrects the ownership and experimental method. It does not install runtime dependencies, implement bcenv, compile a candidate, deploy a replica, launch a trial or submit/schedule games. All readiness/acceptance checks above are proposed future work, not passing results. PR-level prompt-history and documentation checks are reported separately. Keep this PR open and unmerged for Alex's review.
