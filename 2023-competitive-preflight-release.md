# Competitive preflight release guide

Frozen 2026-10-20 01:34 UTC after independent route review and integrated checks.
The competitive-bot goal is **not achieved**. No autonomous competitor trial or
private benchmark panel exists in this program checkpoint.

## What this release is for

A coherent, reviewable foundation for the next approved deployment: public 2023
runtime and local development tools, fixed-capability model/controller contracts,
immutable source intake, durable job ownership/recovery, bounded replay learning
interfaces and executable evidence. It must not be used as an approved live
launcher merely because its tests pass.

The integrated baseline is bcenv `d769760da47cedb4acf6c44b24497a7f29ef1fc5`
([PR13](https://github.com/anicolao/bcenv/pull/13)); paged replay production is
`f3963b7f16857bf6aad837196b8262441ff7c1e3`
([PR14](https://github.com/anicolao/bcenv/pull/14)). The final composed preflight pin is
**`59242ba9935d777f787596adfc0b2b1efc34650d`**
([PR15](https://github.com/anicolao/bcenv/pull/15)), with reviewed durable replay
routing and green CI. No PR has been merged into main or another PR.

[Portable route review and proof](experiments/bcenv/engineering/competitive-preflight-001/durable-replay-v2/README.md)
retains the executable probes, exact source hashes, logs and reproduction command.
The older PR13 source manifest is a historical baseline; PR15 records changed
controller/ledger/transport and all eleven final trusted-module hashes separately.

## Verified components and narrower demonstrations

- Official public engine 3.0.13; explicitly separate 2.0.3 diagnostic profile.
  Private finals 3.0.14 artifacts were not obtained. Public-source equivalence
  does not prove identical private binaries/maps.
- Exact reviewed source/test provenance, all 13 x86_64 flake checks, 230 baseline
  Python tests, and package exclusion of seven trusted implementation modules.
  aarch64 remains untested. Replay-page slice has 256 Python tests; final PR15
  passes all 13 x86_64 checks, 286 Python tests and 27 independent probes, with
  all eleven trusted modules excluded from the packaged runtime. The 27 probes
  were rerun against the exact published commit. Timestamp overflow, a legacy
  cross-run existence leak and boolean continuation acceptance were found and
  corrected before publication.
- Fixed six-tool controller, offline Responses codec, strict source ZIP intake,
  immutable scoped artifacts, SQLite jobs, conservative expiry/fencing and an
  inert synthetic worker seam. A valid fabricated worker receipt can complete a
  synthetic record; it is not authentic match evidence.
- Actual disposable namespace fixture: private filesystem/process/network view,
  reduced capabilities, no-new-privileges, descriptor/environment cleanup and
  trusted PID1 teardown regressions. Separate trusted source export reached a
  queued SQLite job with 38 independent bounded tests.
- Offline model-protocol fixture: all six tools, immutable capture, scoped reads,
  restart result, failure handling and retained unknown-attempt reservations.
  It uses scripted model messages and an inert workspace. The reviewed v2
  composition also exercises capture, durable completion and five replay pages
  over all six tools: 196 synthetic records, 11 calls, largest complete envelope
  11,476 bytes and aggregate output 50,406 bytes. These are fixture measurements,
  not model capability, real game evidence or a sufficient long-session budget.
- Genuine replay-page offsets validate/count the full source while releasing a
  bounded window/filter slice. Both pinned profiles and later-than-10,000-record
  pages are tested. Existing public windows reconstruct exactly over capped
  pages. No additional public match was run for this evidence.

These are separate demonstrations. They do not silently combine into a real
model + isolated worker + authentic new game + authenticated replay learning loop.
The six extracted raw event kinds are not a complete game-state reconstruction;
coverage markers explicitly distinguish validated stream, selected window and
released page. Budget exhaustion is not proof that an agent examined all events.

## What still blocks a live autonomous trial

1. An approved supported Linux execution environment with independently tested
   aggregate descendant CPU/memory/PID/disk enforcement, fresh per-run workspace
   ownership/lifecycle, reliable process-tree termination, and reviewed production
   network/syscall/IPC policy. Existing per-process limits and process-local locks
   are insufficient. No denial or platform mask may be bypassed.
2. An authorized OpenAI API account/model capability and secure host-side secret
   handling, a reviewed live Responses sender, accurate provider token counting,
   durable spending/attempt accounting and a hard deadline/response-stream bound.
   The offline counter is a fixture assertion, not a tokenizer. Native inherited
   host tools cannot substitute for the fixed-capability runner.
3. Authenticated service routing, a real supervised season worker and a match
   validator tying accepted source, compiler/runtime, map/specification, complete
   new execution and replay to its reservation. Hash echoes alone do not prove
   execution or protect against a compromised trusted worker.
4. Independent end-to-end deployment acceptance using synthetic secrets/canaries,
   followed by a frozen environment/tool-schema/kickoff and prospective budget.
   Do not expose real holdouts while acceptance is incomplete.

The [deployment options](2023-supported-deployment-options.md) are read-only
proposals. The user has not answered the existing-VM/API versus hosted-setup
question. No paid resource, key configuration or security change is authorized by
that document. A hosted choice requires actual cost/terms/security confirmation;
credentials must not be requested or stored in chat or candidate files.

## First approved deployment sequence

- Reproduce exact pinned builds and run all unit/protocol checks without granting
  the competitor host tools. Preserve negative results and mismatched pins.
- Provision/configure only the specifically approved environment and capabilities.
  Keep provider secrets, service implementation, evaluator state and opponent
  artifacts outside the competitor filesystem and tool set.
- Test cross-owner/run/job/view denials, forged artifacts/receipts, missing or
  changed sources, stale workers, uncertain commits, oversized outputs, full
  descendant teardown and aggregate resource caps. Inspect actual enforcement;
  behavioral instructions are not an access boundary.
- Validate model/account compatibility with a small separately approved integration
  budget. Current illustrative caps are not a competence-trial budget or proof
  that a long coding session fits the bounded transport/context.
- Run a prospective public integration protocol before protected evaluation.
  The earlier 12-attempt public compatibility/bridge budget is exhausted; it must
  not be silently extended. Existing replay reads and synthetic unit fixtures are
  distinct from additional public opponent matches.

## Competitive evaluation after acceptance

Use the [program roadmap](2023-competitive-program.md), not fixture scores. Before
claiming strength, qualify active licensed opponents on the pinned runtime,
record exact source/lineage/public availability, and privately freeze evaluation
selection/schedule outside the competitor. Historical rank is not proof of exact
server submission identity, present strength or training novelty.

Preregister paired maps/sides, independent fresh-agent replications, failure
handling and cluster-aware uncertainty. Verify any claimed seed control in the
actual engine/runner; do not call ignored or unsupported seed values independent
replications. Public-map familiarity and source/training contamination remain
limitations. No private finals maps or novel-opponent generalization are implied.

A fresh competitor receives only its frozen environment and kickoff. It owns its
bot, hypotheses, proposed changes, edge-case/progress tests, code review and replay
analysis. Evaluators observe evidence and revise the environment between trials;
they do not repair or coach that competitor's strategy. Record counterexamples
and adverse outcomes, not only wins or game counts. Do not request hidden chain of
thought; assess code, tests, public explanations and replay-linked claims.

## Resume/stop rule

The bounded replay route, independent review and integrated freeze are complete.
Dependent live work is paused while approved deployment/model capabilities remain
missing. Do not continue unrelated scaffold polishing to imply progress toward
competence. Keep the exact blocked action, required capability/authorization and
resumable next step visible in the checkpoint.
