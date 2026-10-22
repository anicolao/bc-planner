# BCENV-010: own-team diagnostic observation feasibility

Prospective protocol, 2026-10-22, before any010 preflight or fresh candidate.
This continues the authorized long-running environment work on the existing VM.
No new monetary spending, merge permission, access relaxation or prior-candidate
resumption is inferred. The competitive goal remains unmet; a functioning
workflow or well-recorded process is not evidence of competitive quality.

## Narrow change and hypothesis

Public engine/source inspection and existing public tutorial replay evidence
identify an observation gap: the action projection omitted recorded own-robot
indicator strings and bytecode counts. In the pinned 2023 engine, ordinary robot
output is not a reliable replay exception transcript. Trusted mixed-team stderr
must not be exposed as a substitute. The new read-only `own_diagnostics` replay
mode exposes only bounded, ownership-validated records already in the replay.
The hypothesis is that more accurate observation can support autonomous testing
and replay-grounded iteration. It is not a claim that diagnostics cause better
play or explain any earlier candidate's performance.

Indicators require deliberate bot emission and retain the final recorded string,
not every intermediate update. Strings are untrusted escaped data, not tool
instructions or correctness attestations. Bytecode usage is not CPU time,
automatic exception capture or a correctness assertion; counts can exceed the
nominal robot budget. Empty, missing and null observations differ. Absence of an
error event or diagnostic does not prove error-free execution. Generic interface
semantics are documented without prescribing instrumentation, strategy or fixes.

Own-team filtering precedes counts and pagination. The trusted service derives
the team from the game slot; the candidate cannot supply a team, artifact path or
opponent selector. Initial/spawn/death identity validation covers same-round
lifecycle events. No opponent diagnostics, filtered counts, raw vector indices,
stdout/stderr, profiler names or private artifacts cross this interface.
Existing action queries retain their behavior. Both modes share the existing
150-query quota and hard deadline; a failed query is not partial evidence.

## Frozen comparison profile

Retain [009's public finalist-validation design](2023-public-finalist-validation-009.md):

- Fresh fork-none requested gpt-6.1-sol/high; requested settings are not an
  independent runtime attestation. One fresh feasibility run, not causal proof.
- Conservative live-service-start 45-minute hard deadline, including startup.
  The candidate receives remaining time, at most45 minutes. No clock reset after
  any candidate work. All queued/child work is bounded by remaining time.
- Up to8 accepted source versions, each receiving the same8 training games;
  64 maximum training games. Build rejection consumes a version, not replacements.
- Exactly2 eligible completed immutable finalists locked together before any
  validation feedback; provisional choice and rationale precede validation.
  Each receives the same8 public-validation cells, reserving16 games atomically.
- No new source submissions, re-nomination, extra validation or accepted source
  edits after lock. Final choice must be a completed original finalist; restore
  exact selected bytes and stop. No operator fallback for incomplete validation.
- 80 total public games maximum,24 notes,150 replay queries, public match cap
  120 seconds/512MiB, stop on first phase failure, no retries or substitutions.
- Same training maps, public opponent revisions, order and public-validation
  maps as009. Retain the original public map selection seed/algorithm/inventory:
  [009 map plan](experiments/bcenv/runs/BCENV-009/validation009-public-map-plan.json).
  Do not select new maps or filter them using evaluator membership. They are
  novel to the training schedule, not necessarily unknown to the model or panel.

Only the diagnostic observation mode and accurate generic documentation change.
Engine JAR/settings/API/rules, opponent builds, phase logic and budgets do not.
The default action projection and public result semantics remain unchanged.
The new development runtime is
`/nix/store/1bbk58382aq40pplbyy2fir27qnx3jxj-bcenv-2023-0.1.0`.
The independent evaluator retains its older frozen runtime, not this new service
closure. Same-user native workspace restrictions remain cooperative; this is
not hard filesystem confinement or a complete historical access/edit trace.

## Existing engineering evidence and new launch gates

[bcenv PR22](https://github.com/anicolao/bcenv/pull/22), exact
`66ff4650fd6481cf3a69925098e48e6abc865e53`, passed
[CI39783686439](https://github.com/anicolao/bcenv/actions/runs/39783686439).
420 local tests plus31 final focused tests passed. Independent review checked
negative/lifecycle/differential ownership fixtures and106,573 raw-vector rows
across46 queries on2 existing public tutorial replays. Replay/result hashes and
legacy action output were unchanged. No new experimental games were needed.
Unchanged ordinary CI may run up to6 uncached fixture matches:3 under the active
engine and3 under the legacy diagnostic engine; no workflow/game scope expansion.

CI and local clean-Git runtime NAR and references match exactly:
`sha256-1MzBzVI1R4gsIv6dpxJceQfgznGm4zyvUMJlyXvUNxo=`.
The separately smoke-tested local wrapper differs only by its own store prefix;
all other54 of55 installed entries are identical. The candidate uses the exact
CI runtime above, with no silent closure substitution. The frozen engine hash is
`2b6db98e312e0e509d599acc46bffbb55c2569de0f12c8214a85ee57625f15f2`.

See the [engineering record](experiments/bcenv/runs/BCENV-010/diagnostics-engineering-readiness.json),
[independent implementation review](experiments/bcenv/runs/BCENV-010/diagnostics-engineering-review.md)
and [release identity review](experiments/bcenv/runs/BCENV-010/diagnostics-release-review.md).
Their relative local evidence paths identify retained operator artifacts, not
files supplied to a competitor.

Before any fresh launch:

1. Freeze this prospective protocol/private commitment; exact code/protocol CI
   green and independent fresh-input/kickoff/config review. No prior candidate
   code, tests, reviews, scores or evaluator material in the source-empty export.
2. Run exactly8 public tutorial preflight games using one unchanged official
   tutorial snapshot through the shared host-Python launcher and new runtime.
   This separate engineering budget is not part of the candidate's80 maximum.
   Preserve every attempt; no automatic retries or extra games. Check both
   slots' diagnostics against trusted raw replay vectors and action/replay parity
   against existing public fixtures. Use at most128 bounded replay requests,
   recording continuation/coverage honestly. No lock-phase games are added:
   unchanged phase logic is covered by009's independent32-game preflight.
3. Independently audit source/config/runtime identity, receipts and preflight
   result. Preflight caps accepted versions at1 to enforce its8-game budget;
   live permits8. This is the sole allowlisted preflight/live configuration
   difference, independently checked; full configuration-byte equality is not
   claimed. Runtime/command/launcher parity still must match. Obtain parent
   conditional readiness before live initialization.
   Start the conservative45-minute clock, verify actual live/integration parity
   and empty service/input state independently, then promptly spawn fork-none
   with the exact fixed kickoff. Only a never-used empty pre-candidate service
   may be restarted after a delay, with that attempt explicitly retained.
4. Observe without strategy intervention. Stop candidate and service by the
   shared hard deadline; retain incomplete/no-selection states rather than
   manufacture completion. Freeze versions, selected source/binary, receipts
   and static inputs. Verify source identities and independent selected rebuild.
5. Fix blind source/process review before receiving independent outcome scores;
   only after stopped/frozen confirmation may the private plan be materialized.

## Prospective observations and private regression commitment

Retain009's endpoints: provisional/final choice, both finalists' paired public
results, source-bound reasoning/replay references, tests and known tradeoffs,
versions/time/game/query use, interface failures and exact selected-source proof.
Additionally record action/diagnostic query counts, returned diagnostic coverage
and whether later notes/tests actually use source-bound observations. Do not
require emission, force tool use or award correctness merely for emitting text.
No required selection switch, new numeric win threshold, or causal inference
from a single009/010 pair is introduced. Functionality, process, correctness and
performance remain separate assessments with their own limitations.

Private010 adoption:9915 ASCII bytes, SHA256
`31def260435a8be76cd49ffc72793eb7e96e0e87008e134d23f0ae780e864628`.
Same evaluator-observed panel/order/pins/rubric and old evaluation runtime as009;
24 serial games maximum, uniform300-second cap/512MiB, stop first failure,
no retry, substitution or timeout-as-loss conversion. No private plan file in
shared workspace before stop/freeze; no pristine holdout or generalization claim.

This document publishes no private evaluation outcomes or raw benchmark material.
Denied outcome-summary publication remains pending separately; its local commit
is not in this branch's ancestry. Public engineering/prospective records are not
an alternate route for that payload. No merge is authorized.
