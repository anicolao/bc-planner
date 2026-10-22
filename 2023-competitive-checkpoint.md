# Competitive program checkpoint

Updated 2026-10-22 21:29 UTC. **The competitive goal is not achieved.**
The existing VM runs the cooperative scrimmage service; missing host/provider access is not the current execution blocker. This is not hard filesystem isolation. Historical statements below describe their dates, not current state.

[BCENV-012 is incomplete after a native-reported exec transport failure](2023-continuity-012-preflight-and-launch.md#interruption-checkpoint--2026-10-22-2010-utc). Native FINAL was observed at 19:59:08 UTC, about 30 minutes after the observed spawn response—not six-hour continuity. The original owned service PTY returned exit 1 / `^C` at 19:59:28 after operator interruption, without a graceful-stop marker. Helper quiescence remains **unknown**, not a demonstrated survivor or termination; a working observer connection does not restore native author continuity. No full freeze, final selection, fallback, private evaluation, author resume or replacement is established or authorized.

The interrupted point-in-time snapshot records 108 attempts and 107 completed **result artifacts** (96 training + 11 validation), not independently validated full-game outcomes. One attempted validation result is unresolved; four reserved cells have no recorded attempt/result. Separately, 13 complete batch receipts cover 104 game entries. All 57 fixed inputs match; the checkpoint was bounded/hash-only. Zero scan warnings do not prove stopped helpers or atomic capture. The previously passed B preflight and code/protocol gates remain historical readiness evidence; the [frozen protocol](2023-continuity-capacity-feasibility-012.md) is unchanged. [bcenv PR24](https://github.com/anicolao/bcenv/pull/24) and [planner PR19](https://github.com/anicolao/bc-planner/pull/19) remain draft and unmerged. Further trial execution is blocked by actual transport/ownership limitations, not new user permission or missing VM access; narrow remote engineering qualification has progressed as recorded below, but the actual VM lifecycle and native continuity limits remain unresolved. No private outcomes or candidate strategy/source are included.

## Narrow cooperative lifecycle qualification — 2026-10-22

[bcenv PR25](https://github.com/anicolao/bcenv/pull/25), exact head
`47ba6442f3432f7f0e80de7ed0728917c0b02130`, passed
[CI39855389436](https://github.com/anicolao/bcenv/actions/runs/39855389436)
on its first attempt: **544 unit tests**, exactly one five-case remote qualification
sequence, and six unchanged standard public fixture matches. No lifecycle fixture
or runtime qualification was executed on the interrupted trial's VM.

The five cases cover packaged CLI live-writer/EOF/invalid-FD controls and source
service/runtime paths using inert adapter fixtures: nested SIGINT with queued-work
fencing, synchronous replay-dispatch SIGINT, nested SIGTERM, and cleanup followed
by intentional receipt-publication failure. Actual evidence binds inner direct
wait, fixture acknowledgment, outer owning wait/return, close and receipt order.
There were three packaged wrapper controls, one synthetic-query JVM, four source
adapter fixtures and four inner helpers. The diagnostic check was explicitly
not selected; the reviewed active-only check graph and non-building retention
avoid the previous active/diagnostic duplication. The 40/600-second case/harness checks are elapsed/admission bounds,
not hard watchdogs or unconditional reaping guarantees.

The earlier `cccec35` / [CI39853320731](https://github.com/anicolao/bcenv/actions/runs/39853320731)
ran the harness in both existing active and diagnostic check instantiations:
**ten cases**, exceeding its prospective single-sequence bound. Both records are
preserved; green CI did not erase that deviation or establish global fail-stop
ordering. One separately authorized corrected attempt used explicit active-only
selection, verified the diagnostic-negative output, and retained the deviation.
No blind rerun or new experimental game was used to repair the claim.

The [retained release artifact12460171400](https://github.com/anicolao/bcenv/actions/runs/39855389436/artifacts/12460171400)
contains `qualification-identity.json`, SHA256
`38b9fa33c6e39d510fb926e3bf636c6e5427c1e55455bc757ce8712023cc8cc7`.
It binds installed/source/fixture hashes, runtime metadata, exact PR head and
tested merge `d7fd25eeb3f28d3b4286601d340b8ebd6d6ac81c`; both trees equal
`2bfaf53e6f966bcdf0fb715479c1c988bb8612c3`. Independent actual-evidence review
passed with fixed report commitment
`2aa16eeca0853184d2e5b398dfb62fbe863edd7f65b8b18c027992dc5174f9c5`.

This qualifies only the stated remote source-fixture lifecycle and packaged FD
controls. **Installed in-flight cancellation, sole-writer/inode ownership, the
actual VM's external Nix wrapper and exec-tool PTY route, supervisor-death
containment, and BCENV-012 helper quiescence remain unqualified.** It does not
restore the interrupted author, permit a replacement/evaluation, prove six-hour
continuity or establish competitive competence. PR25 remains draft and unmerged;
the frozen012 protocol and all interrupted evidence remain unchanged.

[BCENV-011 completed its public phases and is stopped/frozen](2023-match-timeout-011-public-outcome.md): eight submitted versions, 64 training games, 16 locked-finalist validation games and no service-game failure. Both finalists trained5/8; public validation changed selection from provisional V7 (3/8) to V8 (4/8). These are adaptive public selection results, not a competence estimate. Native completion and service stop preceded the hard deadline; terminal exit1 without a graceful marker is retained explicitly. All160 engine/initial-summary children were reaped before deadline.

Independent mechanical review verified4,898 frozen files,57 fixed inputs,196 chained receipts and immutable finalist/source bindings. Six relevant final actual-class test mains passed independently; a disclosed abandoned-policy assertion remains failing. The blind review and old-runtime exact rebuild are fixed. Process evidence is substantial, while correctness and boundary assurance remain partial. No private evaluator outcome is published here.

The [011 protocol](2023-match-timeout-feasibility-011.md) changed only the trusted public match-run cap to300 seconds for both phases, under the unchanged45-minute global/max80-game limits and120-second limits for other child subprocesses. Exact code CI39796568851 passed at31ac671; protocol CI39798244799 passed at e6da0a3; readiness CI39802070137 passed at a31f8f0; launch-publication CI39805299025 passed at f40bd79. The eight-game public tutorial preflight, independent actual live parity and clean57-file input gate passed before launch. [bcenv PR23](https://github.com/anicolao/bcenv/pull/23) and [planner PR18](https://github.com/anicolao/bc-planner/pull/18) remain draft and unmerged. The installed adapter/engine closure was unchanged by this host-service-only change. No merge is authorized.

[BCENV-010 remains incomplete without a selected artifact](2023-own-diagnostics-010-public-outcome.md):62 completed games, one unscored timeout and one unattempted cell; no fallback or private evaluation. Its separate, prospectively bounded public diagnostic completed in122.407 seconds under a300-second cap, without repairing the original trial or proving its timeout cause.

[BCENV-009](2023-public-finalist-validation-009.md) also completed public phases and is stopped/frozen with blind review and exact rebuild verified. A functioning workflow is not established competence. Earlier public-development records remain in [006/007](2023-cooperative-replication-006.md) and [008](2023-cooperative-validation-008.md). Existing competitors are never resumed. The separate private evaluator-summary publication request remains pending; no such payload is included here.

## Historical checkpoint snapshot — 2026-10-20


Updated 2026-10-20 01:34 UTC. **The competitive goal is not achieved.** No new
competitor model trial, private benchmark selection or deployed service exists.
[Roadmap](2023-competitive-program.md) and
[boundary design](2023-isolated-scrimmage-architecture.md) remain authoritative.

## Reviewable work

- Planner [PR12](https://github.com/anicolao/bc-planner/pull/12), branch
  `plan/competitive-bc23-program`, stacked on PR11: roadmap, threat model and
  [public opponent provenance](2023-public-opponent-candidates.md). CI passed at
  `0bdd2a1` (31 checks); the final freeze commit adds the release guide and route
  evidence. Prior experiments and evidence remain unchanged.
- bcenv [PR7](https://github.com/anicolao/bcenv/pull/7), branch
  `feat/scrimmage-contract`, stacked on PR6: bounded source intake/public results,
  fixed-tool synthetic controller and versioned gameplay-feedback projection.
  Current head `04c8159`; all 126 pinned-Nix Python tests and CI pass. Independent review fixed
  archive allocation, response-envelope and per-match coverage defects.
- bcenv [PR8](https://github.com/anicolao/bcenv/pull/8), branch
  `feat/final-rules-runtime`, independently stacked on PR6: public official
  3.0.13 runtime, explicitly separate historical 2.0.3 diagnostic profile.
  Head `f3e37cb`; all 13 x86_64 Nix checks and CI pass. aarch64 untested.
  Private 3.0.14 release artifacts returned HTTP403; no access bypass attempted.
  Public source rule equivalence does not establish identical finals binaries/maps.

- bcenv [PR9](https://github.com/anicolao/bcenv/pull/9), branch
  `feat/durable-service-ledger`, stacked on PR7: SQLite source ownership,
  normalized idempotency, logical quotas, reservation fencing and fail-closed
  expiry/clock recovery. Head `df7a20d`; 160 tests and CI pass. Independent
  review adds 13 probes. Worker fencing does not terminate processes or enforce
  physical resources; synthetic principals are not authentication.
- bcenv [PR10](https://github.com/anicolao/bcenv/pull/10), branch
  `feat/responses-transport`, separately stacked on PR7: offline Responses codec
  for gpt-6.1-sol/high and the six fixed tools. Head `be041d3`; 155 tests and CI pass,
  with 8 independent regressions and 104 malformed-provider cases. The review
  fixed continuation IDs, reported model/tier checks and invalid clocks. There
  is no HTTP sender, credential access, live count or provider call.

- bcenv [PR11](https://github.com/anicolao/bcenv/pull/11), branch
  `feat/controller-ledger-adapter`, stacked on PR9: immutable scoped source
  artifacts connect the six tools to durable jobs. Head `8f2125d`; 181 tests and
  CI pass, plus 11 independent probes including process restart. Test SQLite
  helpers now close cleanly. Source receipts still require a trusted capture
  adapter; this module alone does not prove isolation or authentication.

- bcenv [PR12](https://github.com/anicolao/bcenv/pull/12), branch
  `feat/synthetic-worker-lifecycle`, stacked on PR11: fixed inert callback,
  reservation precheck and authoritative finish, bounded receipts and explicit
  uncertain-commit behavior. Head `287ac43`; 200 tests, 12 independent probes and
  CI pass. No process supervisor or authentic match validator is implied.
- bcenv [PR13](https://github.com/anicolao/bcenv/pull/13), branch
  `feat/competitive-service-integration`, stacked on PR8: committed integration
  baseline `d769760` copies exact reviewed code from the component branches.
  All 13 x86_64 flake checks, 230 Python tests and CI pass. Independent audit
  verifies 14 source/test origins, unchanged runtime/gates and seven trusted
  modules excluded from the package. This does not merge any component PR.

- bcenv [PR14](https://github.com/anicolao/bcenv/pull/14), branch
  `feat/replay-page-v2`, stacked on PR13: genuine producer-side offsets, v2
  projection and separate CLI page command. Head `f3963b7`; 256 Python tests and
  CI pass. Independent review covered both pinned profiles, 9,908 actual
  Java-to-projector page comparisons per profile, >10,000-row adverse events,
  exact EOF and byte-identical v1 behavior. No new games were run.

- bcenv [PR15](https://github.com/anicolao/bcenv/pull/15), branch
  `feat/replay-service-v2`, stacked on PR14: durable owner/run replay binding,
  atomic completion/source publication, bounded manifest/window/page retrieval
  and explicit controller protocol v2. Head `59242ba`; all 13 x86_64 checks,
  286 Python tests, 27 independent probes and CI pass. Exact published-commit
  probe rerun passed. All eleven trusted service modules excluded from package.
  Three independently found defects were fixed; v1 withholding/live closure remain.

No PR is merged. PR13 is an explicitly reviewed composition commit. Do not
silently infer that later changes on component branches are included or retested.

## Actual public integration evidence

The following is engineering evidence, not a competitor trial or strength estimate:

- Six licensed, unmodified public packages compile and pass the 3.0.13 verifier.
  Eleven public compatibility games were attempted: ten complete active replays,
  one v5anaconda side-A timeout at the fixed 120-second ceiling. Every package has
  activity evidence in at least one complete game; v5anaconda has not passed paired
  completion. No retry or enlarged budget conceals that failure.
- One additional service-bridge game used fresh accepted sources and fresh builds,
  then checked engine/map/source/build/replay evidence before publishing a
  156-byte aggregate result. Four negative cases and eight offline evidence tests
  pass. The matchup was chosen after a fast public smoke result, so its win has
  no unbiased competitive interpretation.
- The combined prospective public integration budget was 12 game attempts and is
  exhausted. Further games need another prospective protocol. Existing replay
  analysis does not execute another game.
- Complete artifacts remain in the disposable engineering workspace. Compact
  public evidence is retained in [preflight 001](experiments/bcenv/engineering/competitive-preflight-001/README.md). Engine/map/replay binary
  redistribution is excluded pending a clear upstream license grant.
- Recorded runtime checks cover selected files, not full toolchain attestation.
  These builder-controlled jobs do not establish hostile-code containment.
- Existing-game feedback now projects a fixed six-round window into all 455 rows
  in 104,406 bytes, plus correctly labeled bounded variants. Independent persisted
  checks pass without invoking another parser or game. No live replay route exists.

## Isolation and model connection

Native fresh agents can read sibling evaluator files through inherited tools;
clean context alone fails the access-separation requirement. Prior managed CLI
execution failed before inference. No denied CLI mode, mask or requirement was
bypassed or retried.

A synthetic bubblewrap launch failed before candidate execution because its
loopback setup required a denied NETLINK_ROUTE operation. That operation was not
retried. A separately permitted unshare launcher uses an empty network namespace
without loopback setup. It now starts the disposable fixture read-only, provides
private PID/proc, drops effective/permitted capabilities and sets NoNewPrivs.
All 21 bounded synthetic checks pass on independent rerun, including actual
controller read/write/exec. Review found and fixed setup-exception leaks, missing
outer-controller death linkage, and a confirmed hostile PID1 teardown escape.
Trusted non-dumpable init now retains PID1 and launches candidate PID2. This is
fixture-only evidence; aggregate resource containment, fresh/concurrent workspace
lifecycle and full production policy remain unpassed. No real secret is used.

The offline transport codec is reviewed; a supported live inference connection
with only the fixed controller tools is still missing. Credentials must remain outside the candidate sandbox. The current
native tools and blocked CLI cannot be substituted for that capability boundary.
No provider account, key, paid infrastructure or persistent access was created.

## Combined build checkpoint

A local, uncommitted composition of PR8's public runtime and the reviewed
PR7/9/10/11 service files passes **211 Python tests** and builds the competitor
package. Inspection finds none of the six trusted service implementation files
inside that package. [Exact commits, hashes and build log](experiments/bcenv/engineering/competitive-preflight-001/composition/README.md)
are retained. This is not a merged/frozen release, full engine requalification,
new game, model trial or complete lifecycle integration. The earlier 190-test
checkpoint is retained alongside the later result.

The later [committed integration baseline](experiments/bcenv/engineering/competitive-preflight-001/integration-baseline/README.md)
adds the reviewed synthetic worker: 230 tests plus all 13 flake checks. Historical
disposable-build evidence remains unchanged.

## Actual source handoff and offline model protocol

[Source-export evidence](experiments/bcenv/engineering/competitive-preflight-001/source-export/README.md)
now connects actual namespaced write/read, a reserved exact exec command, a
trusted read-only collector, strict ZIP validation, immutable scoped capture and
submission to a real temporary SQLite ledger. The job remains queued. All 28
local tests and 38 independent tests (28 repeated plus 10 added) pass in separate
fixture copies. Forged stdout, malformed layouts, symlinks/hard links/FIFO,
resource/read bounds, stale handles, exception cleanup and hostile teardown are
covered within stated limits. The materializer was inspected/check-only; its
materialize path was not run. No production workspace lifecycle or aggregate
resource budget is established.

[Full offline composition](experiments/bcenv/engineering/competitive-preflight-001/full-composition/README.md)
adds five executable probes combining the Responses codec, controller, artifact
adapter and real temporary SQLite. Eight fixture model turns exercise all six
tools, immutable capture after mutation and durable result reopening; failures,
cross-scope denials and unknown-attempt reservations are retained. Model messages,
token counts and completed-game evidence are fabricated fixtures, not inference,
charges or played results. This test uses an inert workspace, not the namespace
collector. No single test yet combines real model, sandbox, worker and game.

[Portable v2 page evidence](experiments/bcenv/engineering/competitive-preflight-001/replay-pages-v2/README.md)
retains exact source hashes, 67 sanitized pages and the reproduction script.
Windows 35–40 (455 rows) and 300–301 (237 rows) reconstruct exactly under
simultaneous source-row, projected-row and byte caps. Raw replay/engine/map
binaries are omitted. These remain six extracted record kinds, not complete
state reconstruction or a new competition result.

## Resume next

The [frozen preflight release guide](2023-competitive-preflight-release.md) and
[portable durable replay proof](experiments/bcenv/engineering/competitive-preflight-001/durable-replay-v2/README.md)
complete the current safe offline engineering slice. No unresolved must-fix was
found within its reviewed scope. This is not a deployment acceptance or competitive
outcome; trusted fixtures cannot authenticate themselves.

1. The [named deployment options](2023-supported-deployment-options.md) question
   remains unanswered, confirmed by the coordinator at 2026-10-20 01:32 UTC.
   Select an existing supported Linux VM and authorized OpenAI account, or review
   actual hosted cost/terms/security before any provisioning or key setup.
2. On the specifically approved host, implement and independently test aggregate
   descendant containment, workspace ownership/lifecycle, authenticated routing,
   supported live model sender/accounting and authentic supervised match validation.
   These remain engineering gates after setup, not automatic effects of provisioning.
3. Keep real-model launch and protected benchmark use closed until end-to-end
   acceptance passes with synthetic canaries. Then freeze environment/tool schema,
   kickoff and a prospective public trial budget before a fresh autonomous attempt.
4. Do not silently extend the exhausted public compatibility budget or treat
   synthetic success as competitive evidence. Preserve failures and evaluate code,
   tests, replay-linked reasoning and replicated outcomes under the roadmap.

Dependent live work is paused pending the required deployment/model capability
and authorization. No paid resource, credential configuration, security change or
merge has been performed. Resume from the exact final pin rather than assuming
new component-branch changes were tested.
