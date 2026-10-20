# Actual fixture-only immutable source handoff

Observed 2026-10-20 UTC. All inputs are synthetic. Actual games: **0**. Actual model/provider calls: **0**. No active-repository edits, historical-fixture writes, NETLINK_ROUTE retry, paid resource, credential access or host-security changes.

## Outcome

The new actual namespace backend exports source from its own fresh fixture through a trusted read-only collector, validates bounded ZIP bytes, and hands those exact immutable bytes to the existing typed capture layer. The existing six-tool controller then submits the owned artifact to a real temporary SQLite ledger and receives accepted/withheld feedback. The durable job remains queued; no game or strength outcome is asserted.

The local suite passes **28/28** bounded tests. Independent fresh-copy review passes **38/38** in 10.284 seconds: the same 28 plus 10 additional checks, with no unresolved must-fix finding. The independent report, exact test additions/output, copied-source verification and relocation diff are included under `independent-review/`. The code is suitable for experimental fixture publication only; full deployment remains unaccepted.

## Authority path

1. Model-shaped input can request only the existing `workspace_exec` operation, with the exact reserved argv `("bcenv.fixture.export-source.v1",)` and cwd `.`. The package `fixturebot` is trusted fixture configuration.
2. The backend serializes operations through a process-local lock. It starts collection only after the preceding candidate invocation has returned through the trusted PID1/death-link supervisor. Unexpected supervisor exceptions poison subsequent export attempts instead of publishing uncertain state.
3. The fixed collector runs inside the same enforced root with source/scratch remounted read-only/noexec. It cannot choose a host path, and candidate code does not execute during collection. The collector asserts its read-only mount configuration before reading.
4. Bounded no-follow descriptor traversal accepts only regular, singly linked Java source files, checks metadata around reads, and produces a deterministic stored ZIP. Symlinks, special files, malformed names/text and over-limit trees fail closed.
5. Collector stdout is private byte transport to the trusted backend, with its own fixed 1 MiB cap. It is not candidate stdout or model-visible tool output. The existing strict source validator checks the complete archive again.
6. The backend returns the exact frozen `SourceExport` inside `ExportedExecReply`. It never provides an artifact ID. The unchanged copied `CapturingSandboxAdapter` captures the bytes in `SourceArtifactStore`, enforces existing owner/run/retention rules, and issues the handle. The controller's ordinary artifact visibility set is unchanged.

Candidate output that looks like a handle, source path or ZIP assertion never gains this authority. Failed exports return a small closed error and no handle. Subsequent source edits do not change a captured snapshot.

## Test coverage

The local tests exercise actual namespace execution and read-only collection, not merely an in-memory fake filesystem. They cover immutable snapshots after edits, deterministic archive bytes, owner/run isolation, forged stdout, exact-command matching, immutable collector code, required read-only mounts, outside symlinks, directory symlinks, hard links, FIFO nonblocking rejection, empty/invalid Unicode/NUL source, wrong tree/non-Java/reserved names, file/count/archive/depth bounds, and private collector output limits.

Failure tests assert no handle publication after collector timeout, malformed archive and supervisor setup exceptions. Two failure-injection tests use synthetic returned replies rather than actual long-running collector bugs; their role is checking non-publication. Actual output-cap and namespace-teardown tests exercise the OS path.

The process-local serialization test waits for a candidate's delayed final write before capture. The hostile teardown test makes the candidate start a new session, clear its own PDEATHSIG and close all standard descriptors; after timeout, its bounded heartbeat remains stopped while source capture proceeds. The trusted PID1 still owns the death link.

The six-tool integration uses a scripted `ModelTransport`, exact frozen initial bytes, the real namespace backend, the existing typed capture wrapper and real local SQLite. It exercises write/read/export/submit/result/replay without enabling an engine, model, hidden data or game result.

The first local run had one test assertion mismatch: the test expected internal SQLite state `accepted`, but the ledger correctly uses `queued` internally and publishes `accepted`. Only that test expectation was corrected. No implementation fix was needed for it.

Independent additions verify exact 128-file, 524,288-byte/file and 240-character path boundaries; excessive path/entry limits; case collisions; valid ZIP bytes on normal stdout still granting no authority; failed recapture not reusing an old handle; selector-poll failure cleanup; and separate-copy writes not reaching the author's fixture. Independent original/source hashes remained unchanged throughout review. The reviewer also independently ran the materializer's read-only check for all 22 runtime paths, without exercising materialization.

## Bounds and remaining sharp edges

- The collector is deliberately narrower than the general ZIP intake: stored ZIP only, 256 total traversal entries, no hard links, fixed package. A large highly compressible source set might be accepted by general compressed intake but rejected here.
- The lock covers one backend instance in one process. Other trusted host writers or other backend instances can mutate the same backing workspace. This is not cross-process atomic capture or authenticated multi-tenant ownership. Fresh per-run service-owned storage remains a deployment requirement.
- Any read/write/exec exception conservatively blocks subsequent exports through that backend instance, even when a particular failure may have been harmless. This avoids guessing that teardown is safe but limits recovery/availability.
- `SourceArtifactStore` is bounded process-local memory. It survives source mutation, not process restart. The SQLite job ledger does not turn it into durable artifact storage or authenticated ownership.
- Aggregate descendant CPU/memory/PID quotas and bounded persistent writable storage remain absent. Per-process/file rlimits and wall limits do not substitute for them. No exhaustion/stress test was run.
- Production syscall/network/IPC policy, concurrent-job lifecycle, supported real-model transport, evaluator/compiler/engine integration and holdout access remain unpassed. Real-launch and heldout hooks stay unsupported.
- The code assumes trusted host orchestration and public runtime preparation. Native agents still have host-side tools and cannot be treated as capability-limited competitors merely because this fixture exists.
- Fixed paths are explicit. `prepare_export_fixture.py` supplies exact fresh setup and refuses existing targets; only its read-only prerequisite check was run after extracting it. The tested fixture was already prepared with the documented public-runtime copy/layout operations. No unperformed clean-install result is claimed.

## Provenance and publication

The earlier reviewed five-file namespace baseline is copied exactly under `baseline/` and recorded in `baseline-sha256.json`. The historical probe's complete existing `SHA256SUMS` check still passes after this work. The new source hashes and local test inventory are in `export-results.json`.

Four trusted service files are copied with exact hashes under `trusted-services/`. They match committed source `8f2125d12db4df1f16bca721179ec52cf16273d6`; the manifest also records the earlier base revision and the staged-copy timing. Their API contracts were not bypassed or modified.

The runtime closure is public existing Python/Nix software, listed as 22 exact paths in `fixture-manifest.json`. Compact publication contains source, manifests, text/JSON evidence and review material only. It excludes runtime contents, maps/binaries, writable state, canaries, source ZIP outputs and SQLite databases. No private evaluator state or selected holdouts were present.
