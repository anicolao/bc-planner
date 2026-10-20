# Competitive program checkpoint

Updated 2026-10-20 00:11 UTC. **The competitive goal is not achieved.** No new
competitor model trial, private benchmark selection or deployed service exists.
[Roadmap](2023-competitive-program.md) and
[boundary design](2023-isolated-scrimmage-architecture.md) remain authoritative.

## Reviewable work

- Planner [PR12](https://github.com/anicolao/bc-planner/pull/12), branch
  `plan/competitive-bc23-program`, stacked on PR11: roadmap, threat model and
  [public opponent provenance](2023-public-opponent-candidates.md). CI passed at
  `6da144d`. Prior experiments and evidence remain unchanged.
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

A supported model inference transport with only the fixed controller tools is
still missing. Credentials must remain outside the candidate sandbox. The current
native tools and blocked CLI cannot be substituted for that capability boundary.
No provider account, key, paid infrastructure or persistent access was created.

## Resume next

1. Finish publishing compact preflight evidence and reviewed executable fixture
   adapter/tests; preserve failed probes and exact fixes, not just passing totals.
2. Implement and independently review durable ownership/job reservation,
   idempotency/quotas and crash recovery in the separate service worktree. Use
   synthetic principals only; this does not create authentication or a listener.
3. Research named supported model/worker deployment options and explicit cost and
   setup decisions, using official documentation without provisioning anything.
4. Integrate and retest runtime/services only after their separate changes are
   reviewed. Keep heldout and real-model launch gates closed until the complete
   deployed boundary passes, then freeze a new trial protocol before a fresh
   autonomous attempt. Provisioning alone does not complete the engineering.
