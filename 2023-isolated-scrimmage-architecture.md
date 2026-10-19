# Enforced competitor and scrimmage boundary

Status: design and feasibility assessment, 2026-10-19. No security-isolated model
trial has been launched. This design protects deployed evaluator state even when
its implementation is publicly reviewable.

## Finding and chosen direction

The current fresh native agent retains ordinary tools that can read sibling
workspaces and evaluator files. The existing namespace/chroot command wrapper
isolates the command, not its caller. A clean conversation, opaque IDs and artifact
hashes do not fix that. Do not launch another native trial and label it isolated.

Use a trusted controller with a supported inference transport and a fixed tool
allowlist. Every emitted model operation must pass through the controller's
sandbox/service dispatcher. The model never receives a general host shell,
connectors, other-agent messaging, browser, conversation search or dynamic tool
discovery. A narrow service plugin cannot help if unrestricted tools remain.

No currently verified supported inference transport in the existing VM supplies
this boundary. Prior CLI launches failed before inference, and the alternative
sandbox mode was rejected by managed requirements. Those routes will not be
retried or bypassed. No saved separate coding environment was available; the
user's computer and new paid infrastructure are outside this program's authorized
execution scope. An authorized supported transport or environment is a launch
prerequisite, not a reason to claim behavioral isolation is adequate.

## Trust and protected state

Untrusted: the model, emitted calls, generated Java, archives, source names, logs,
replays and third-party content. Trusted: the outer platform/kernel, reviewed
controller and launcher, pinned compiler/engine and service authorization layer.
Kernel zero-days and a malicious platform operator are outside this bounded
claim. The Java verifier alone is not a complete hostile-native-code sandbox.

Protect private holdout selections, schedules, rubrics, excluded prior findings,
service credentials, raw logs and cross-trial data. Protect integrity of source
snapshots, build/match receipts, engine inputs, candidate freeze and resource
budgets. General evaluator source, route names and algorithms can be public;
security cannot depend on obscurity. Published results become development cases.

## Components

1. **Controller:** constructs the fresh kickoff and frozen context from explicit
   allowlists; validates strict call schemas; denies unknown tools/fields; enforces
   model/time/token limits. Authentication remains outside all candidate-visible
   files, environment, process views and descriptors. It is not a general proxy.
2. **Competitor sandbox:** fresh empty writable workspace and temporary storage;
   read-only pinned rules/API/tool closure; no parent checkout, history, host root,
   sockets, secrets or unrestricted network. All read/write/exec operations use
   this same boundary. Private process view, closed inherited descriptors,
   descendant cleanup and aggregate resource bounds are mandatory.
3. **Scrimmage control plane:** accepts bounded source bytes and typed identifiers,
   never host paths, caller commands, credentials, URLs, precompiled classes or
   caller-declared verification. Objects belong to a trial principal; opaque IDs
   are not authorization. Atomically reserve quotas and idempotency before work.
4. **Compiler/match workers:** separately isolated, credential-free, immutable
   per-job inputs. Workers cannot see the full panel, database, other jobs or
   observer records. Sanitize results/diagnostics; bounded replay parsing cannot
   follow instructions or leak raw paths/team identities inadvertently.
5. **Protected evaluator:** selects only a server-owned frozen candidate, then
   executes sealed assignments after the competitor's development phase ends.
   There is no competitor endpoint for protected evaluation or adaptive feedback.

Resource containment must cover total CPU, memory, disk, descendants, output and
concurrency. A timeout or per-process heap limit alone is not sufficient. If the
host cannot enforce an essential limit, record that gap and keep the relevant
hostile-code/independence claim closed.

## Service semantics

Public capabilities are describe, source submission, own build status, development
scrimmage request/status, authorized replay retrieval and immutable candidate
selection. Development challenge IDs are disclosed; acceptance assignments are
not. Source/package intake is syntax/layout validation, distinct from compiler and
verifier acceptance. Compile rejection is distinct from infrastructure failure.
Missing winner evidence never becomes a loss or a successful match.

Require per-principal object authorization, exact-body idempotency, transactional
quota accounting, crash/restart recovery and append-only receipts. A client-side
self-consistent manifest cannot certify a build or alter a frozen submission.
The initial facade scaffold is deliberately in-memory and non-executing, so it
proves none of those deployment/durability properties by itself.

Replays may legitimately expose behavior. Before serving them, enumerate fields
in the actual BC23 format, retain necessary gameplay evidence and remove hidden
identity/path/log metadata. A replay-unavailable scaffold is safe but insufficient
for the intended autonomous diagnosis loop. Test both useful evidence retention
and leakage prevention.

Commit privately to benchmark bytes using a secret random nonce and retain the
recoverable original bytes and nonce. A bare hash of a small known map/opponent
set can be guessed. Public commitments must not identify the selected holdouts.
After exposure, retire the holdout and preserve the result as a regression case.

## Required adversarial evidence

Use disposable synthetic canaries, never real secrets or denied platform files.
Every test records expected and actual outcome, exact deployed input/tool hashes,
timestamp, and a positive allowed control. Test all tools actually delivered to
the model, rather than only the intended wrapper.

| Surface | Required negative evidence |
| --- | --- |
| Actual model tool inventory | No unrestricted host, connector, delegation or history route; unknown calls/extra fields denied |
| File confidentiality/integrity | Absolute/relative/encoded traversal, links, sibling workspaces, caches, trusted binaries and receipts inaccessible |
| Processes/descriptors | No supervisor environment/memory/descriptor access, signaling or unapproved sockets |
| Network | No arbitrary egress, host loopback, metadata, DNS or URL forwarding; only typed broker operations |
| Service authorization | Cross-trial, guessed/stale IDs and admin/holdout routes denied without existence leaks |
| Archive intake | Malformed, ambiguous, oversized, compressed-expansion and non-source packages rejected before extraction/execution |
| Budget and races | Concurrent/duplicate/restarted requests cannot exceed or reset quotas; conflicting idempotency body rejected |
| Worker lifecycle | Controlled low-limit timeout/output/memory/descendant probes terminate and leave no reusable state |
| Authenticity | Client hashes/results cannot change server receipts or selected source/binary |
| Holdout non-interference | Changing synthetic private assignments cannot change pre-freeze public response content |
| Context allowlist | Exact kickoff/docs/tool responses contain no observer canaries or excluded prior analyses |
| Fail-closed behavior | Missing transport, limits, policy, input pin or failed boundary test prevents launch; no native fallback |

Timing channels are not claimed eliminated by content tests. Parser tests are not
a kernel audit; a sandbox probe is not proof of the model's entire tool boundary.
Acceptance needs an actual capability-limited fresh model session using the exact
same deployment and all these tests, followed by independent review.

## Safe work while transport is blocked

Continue source intake/result contract tests, public engine compatibility checks,
public opponent provenance, durable service design and synthetic recovery tests.
Do not stage actual holdouts in the shared agent-visible filesystem, copy existing
credentials, weaken platform requirements, provision paid resources, or use the
user's computer. Report the narrow unresolved requirement: a supported inference
route with no tools outside the enforced competitor workspace and scrimmage RPC.
