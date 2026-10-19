# Competitive program checkpoint

Updated 2026-10-19 23:36 UTC. Current state: M0/M1 in progress; no new competitor
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
