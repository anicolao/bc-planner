# Competitive program checkpoint

Updated 2026-10-20 00:47 UTC. **The competitive goal is not achieved.** No new
competitor model trial, private benchmark selection or deployed service exists.
[Roadmap](2023-competitive-program.md) and
[boundary design](2023-isolated-scrimmage-architecture.md) remain authoritative.

## Reviewable work

- Planner [PR12](https://github.com/anicolao/bc-planner/pull/12), branch
  `plan/competitive-bc23-program`, stacked on PR11: roadmap, threat model and
  [public opponent provenance](2023-public-opponent-candidates.md). CI passed at
  `f89d249`. Prior experiments and evidence remain unchanged.
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

No PR is merged. Do not silently combine independently stacked branches without
retesting the integrated runtime and trusted services.

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

## Resume next

1. Finish the synthetic durable-worker seam now under implementation: fixed
   trusted specification and immutable source, reservation/fencing checks,
   bounded closed receipts, conservative expiry and no implicit retry. Its
   callback remains inert; it cannot establish process supervision or actual
   game authenticity. Independently review before publishing.
2. Replay projection exists but the service route still withholds replay.
   Authenticated routing, durable model/controller/artifact recovery, physical
   resource budgets, worker supervision and live model transport remain open.
   Do not equate typed receipts, host fixture scopes or packaging exclusion with
   complete access enforcement.
3. [Named deployment options](2023-supported-deployment-options.md) document
   official capabilities and a small integration cost estimate. The setup
   choice remains pending; no resource, credential, security change or spending
   is authorized by that report. Continue synthetic-safe engineering meanwhile.
4. Keep heldout and real-model launch gates closed until the deployed boundary
   passes. Then freeze a prospective trial protocol before a fresh autonomous
   attempt. Provisioning and these passing component tests do not complete the
   engineering or establish competitive strength.
