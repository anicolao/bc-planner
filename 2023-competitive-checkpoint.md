# Competitive program checkpoint

Updated 2026-10-19 23:48 UTC. Current state: M0/M1 in progress; no new competitor
trial, private benchmark or deployed service. [Roadmap](2023-competitive-program.md).

## Repository boundaries

- Planner starting point: PR11 / analysis/lecture-opponent-trial,
  4e48164081e6b9c4a3f30698183db5fc5a5789ad; current branch plan/competitive-bc23-program.
- bcenv starting point: PR6 / feat/lecture-opponent-trial,
  0213a0e, stacked on PR5; current branch feat/scrimmage-contract.
- Prior evidence retained. PRs remain open; no merges authorized or performed.

## Active work

1. Independent architecture assessment: actual native worker can read evaluator
   files with ordinary tools. No saved coding environment found; user's Mac is out
   of scope. Existing CLI path needs exact prior denial reviewed, never bypassed.
2. Public opponent provenance: official historical placements and source/license
   evidence being gathered; no actual holdout panel selected or published.
3. Service foundation: source ZIP validation, bounded public results and attack
   tests, no listener/credentials/real evaluator state. This is scaffold only.
4. Roadmap sets staged gates and budgeted experiments, competence distinct from
   finalist strength, and no candidate coaching.

## Next actions

Review independent reports; reconcile design; run adversarial unit tests; publish
separate roadmap and scaffold PRs with checks. Resolve real agent capability
boundary before exposing heldouts or launching competitive trials. If no supported
boundary exists, request the smallest specific environment/tool capability needed
and continue useful public integration work meanwhile.

## Known limitation

The host tool surface can bypass a per-command namespace/chroot. Native fresh
conversation isolation alone is inadequate. No claim of enforced isolation or
credible tournament competitiveness is currently justified.

## Published and newly established

- Roadmap PR12: https://github.com/anicolao/bc-planner/pull/12, commit 8ef1da9; prompt-hygiene CI passed.
- Independent assessment confirms no currently verified supported capability-limited inference route; see [architecture](2023-isolated-scrimmage-architecture.md). No blocked CLI route retried.
- Finalist-source research exposed a material rules mismatch: runtime 2.0.3 predates the final-season 3.x rules. Final tournament release provenance and migration are being checked before competitive execution. Old diagnostic evidence remains tied to 2.0.3.

- Service scaffold PR7: https://github.com/anicolao/bcenv/pull/7, commit f91e1ce.
  Pinned Nix Python check passed 57 tests, including 39 new facade tests. Independent
  malformed-archive and concurrency review found a bounded allocation-hardening
  opportunity, now fixed before parsing ZIP directory objects. No actual service
  listener, durable queue, raw replay release or agent isolation is claimed.
- [Public opponent candidates](2023-public-opponent-candidates.md) links six licensed
  source pools and historical performance evidence. No sealed panel is selected.
  Actual packages must be chosen carefully; repository default matches can launch
  example players, and working packages may contain post-tournament edits.
- Public 3.0.13 official engine/API artifacts have been acquired through Nix with
  normal TLS and pinned hashes. Final-rule/legacy diagnostic test tracks are being
  finalized separately. Private 3.0.14 artifacts returned HTTP403 and were not
  accessed; public source equivalence does not imply identical private finals maps.
- Fixed-tool controller simulation and sanitized gameplay feedback are in progress.
  A supported capability-limited inference transport remains the real launch blocker.
