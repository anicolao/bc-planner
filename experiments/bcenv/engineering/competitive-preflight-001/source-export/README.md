# Fixture-only immutable source export

This artifact connects an actual namespace-backed source collector to the existing six-tool controller and the synthetic scoped-artifact/SQLite adapters. It invokes no model, compiler, engine, opponent or game. It does not open the real-launch or holdout gates.

Local tests: 28/28 passing. Independent fresh-copy tests: 38/38 passing (28 plus 10 additions), with no unresolved must-fix in this narrow scope. See `REPORT.md` and `independent-review/REVIEW.md` for acceptance limits and exact evidence.

## Exact operation and authority

The existing `workspace_exec` tool recognizes exactly:

```json
{"argv":["bcenv.fixture.export-source.v1"],"cwd":".","timeout_seconds":2}
```

The Java package is fixed trusted configuration, `fixturebot`; callers cannot supply a package, source path, ZIP path, handle or collector command to this operation. Source files must live below `src/fixturebot/`. Other exec requests run as ordinary candidate commands and always return no export side channel, regardless of stdout claims.

`ExportingFixtureBackend` serializes its operations, waits for the previous namespace job to return, then runs the immutable collector in a fresh instance of the same enforced root with both source and scratch read-only/noexec. The collector checks that root/source/scratch mounts are read-only, reads bounded regular files through no-follow directory/file descriptors, and emits a deterministic stored ZIP to a private host-side pipe. This ZIP is never model-visible stdout.

After strict source validation, the backend returns the exact frozen `SourceExport(package, archive: bytes)` inside `ExportedExecReply`. The copied existing `CapturingSandboxAdapter` alone calls `SourceArtifactStore.capture`, applies its owner/run/quota logic, and mints the opaque handle. The backend neither supplies nor chooses an artifact ID. The controller retains the same six tools and only trusts the adapter's typed handle field. Subsequent candidate edits cannot mutate an already captured byte snapshot.

The normal candidate output cap remains unchanged. The separate fixed collector path has a private 1 MiB pipe cap. Failed collector runs, malformed ZIPs, timeouts and invalid source publish no handle. Supervisor exceptions conservatively poison future exports through that backend instance until a fresh fixture/backend is created; this includes read/write exceptions, which may be an availability limitation.

## Bounds and intentional restrictions

- ZIP: 1,048,576 bytes, stored/uncompressed entries, deterministic metadata.
- Files: 128; each 1–524,288 bytes; total source at most 2,097,152 bytes.
- Traversal: at most 256 total directory entries, depth 16, ASCII path length 240.
- Only regular `.java` files, no symlinks, special files or hard links.
- UTF-8, nonempty, no NUL; strict existing intake rechecks package/layout/case collisions and archive structure.
- The stored-ZIP cap can reject source sets that a compressed archive might fit. The 256-entry cap is deliberately narrower than the general intake's path model.
- Collector reads compare inode/type/link/size/time metadata before/after each file. This is defense in depth; the security premise is completed candidate teardown plus read-only collector mounts and process-local serialization.

## Scope and remaining gates

The operation lock covers only calls through one backend instance in one process. It does not exclude another backend instance or trusted host process writing the same backing directory. This prototype uses a fresh synthetic fixture; authenticated multi-process workspace ownership and concurrent-job isolation are not established.

Aggregate CPU/memory/PID budgets, bounded persistent writable storage, production syscall/network policy, supported real-model transport and actual evaluator integration remain unpassed. Artifact snapshots are bounded process-local memory, not a durable artifact service. The SQLite ledger is real local storage, but principal/run values are trusted synthetic configuration, not authentication. A queued job is not a game result.

The trusted init retains PID1 and candidate code starts as PID2. The original teardown escape and its trusted-init correction are documented in the prior reviewed sandbox artifact. This export layer preserves that mechanism. It is accepted only for bounded synthetic probing, not arbitrary hostile production workloads.

## Files and provenance

- `export_backend.py`, `source_collector.py`: new export implementation.
- `probe_adapter.py`, `namespace_launcher.py`: derived namespace adapter with private collector cap and read-only-workspace mode.
- `parent_death_guard.py`, `io_worker.py`: unchanged reviewed components.
- `baseline/` and `baseline-sha256.json`: exact five-file source snapshot from the historical reviewed probe. Baseline scripts are evidence only; do not run them against the historical fixture.
- `trusted-services/services/`: exact copied controller, controller-ledger adapter, durable ledger and source validator. `trusted-services/source-sha256.json` identifies their source checkout, base revision and file hashes.
- `test_source_export.py`, `test-output.txt`: actual bounded tests, including the six-tool controller round-trip.
- `independent-review/`: final 38-test report, structured results, independent test source/output, baseline verification, original/relocated hashes and relocation diff.
- `fixture-manifest.json`: exact 22-path public Python runtime closure; runtime contents are excluded from compact publication.

Historical reviewed probe/evidence and active repositories were not edited. The new fixture was made by copying the historical public immutable root into a different directory and creating new empty writable directories. The collector was then copied into the new root only.

The four service files were copied while changes were staged above base commit `df7a20d63d04faae829b97e786f4cb4f985b0071`. The subsequent committed source `8f2125d12db4df1f16bca721179ec52cf16273d6` was verified to contain identical copied service hashes. The manifest records both facts; it does not imply the added adapter existed unchanged in the earlier base commit.

## Reproduction

Paths are deliberately fixed to `/workspace/shared/bc23-source-export-probe`. This is a fixture artifact, not a portable production installer. A trusted integrator moving it must relocate the fixed BASE/REPO constants consistently and keep exact before/after hashes. Candidate inputs cannot configure those paths.

The materialization helper copies only the 22 manifest-selected public runtime paths, creates fresh mount points/workspaces, copies the two trusted helpers, and writes synthetic markers. It does not copy an existing writable workspace, install/download anything or change host security. It refuses to replace any existing fixture target.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 prepare_export_fixture.py --check
# On a fresh absent destination only:
PYTHONDONTWRITEBYTECODE=1 python3 prepare_export_fixture.py --materialize
PYTHONDONTWRITEBYTECODE=1 python3 test_source_export.py
```

The helper's read-only prerequisite check was run. It was extracted after the current fixture was prepared; this is not a claim that the materialization command was rerun over a new destination. The default source is the earlier reviewed fixture's public runtime; another explicitly trusted existing source root must contain all exact pinned manifest paths.

The tests reset only the new synthetic source directory and create small synthetic files and temporary SQLite databases. They do not access actual secrets or use NETLINK_ROUTE, change host controls, or run aggregate stress workloads. Compact publication excludes both fixture trees, writable data, canaries and SQLite files.
