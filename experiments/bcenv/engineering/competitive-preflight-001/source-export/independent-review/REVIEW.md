# Independent source-export boundary review

Reviewed 2026-10-20 UTC. Original artifact: `/workspace/shared/bc23-source-export-probe`.

## Verdict

Accept for bounded synthetic, fixed-fixture publication. No unresolved must-fix finding was identified. This is not acceptance of a production sandbox, authenticated multi-tenant service, live model trial, or aggregate resource boundary.

The reviewer did not edit the author's implementation, tests, writable fixture, or historical baseline. Execution used a separate copied fixture at `/workspace/shared/source-export-independent-review/fixture`; the only implementation differences were the fixed BASE/REPO relocation in two files. Original/relocated hashes and the exact deltas are retained beside this report.

## Verified result

**38 tests passed in 10.284 seconds:** all 28 author tests plus 10 additional independent tests. Final output is `test-output.txt`; structured evidence is `results.json`; independent additions are in `test_independent_export.py`.

- Actual fixed namespace collection produced a deterministic valid ZIP and an immutable, owner/run-scoped source snapshot. Only the typed capture adapter minted a handle. Subsequent source mutation did not alter the old bytes.
- Normal exec could print a forged handle or a fully valid ZIP without minting a handle. Extra/aliased operation argv and an alternate cwd did not enter the export route. The fixed collector command invoked as ordinary exec could not export.
- Source collection checked read-only root/source/scratch mounts. Collector mutation failed. No-follow directory/file opens, inode/type/link/size/time checks, and strict intake rejected outside-root symlinks, directory symlinks, hardlinks, FIFO files, invalid text, NUL, non-Java files, wrong package trees, reserved identifiers, and case collisions.
- Exact 128-file, 524,288-byte per-file, and 240-character archive-path boundaries were accepted. Excess file count/size/path length, directory depth, 256-entry traversal count, and ZIP size were rejected. Private pipe output caps were enforced.
- Failed, malformed, or timed-out export never published a handle, including failure after an earlier successful capture. ZIP bytes did not appear in the export tool's stdout; the successful tool response was only a small confirmation.
- A same-instance operation lock made export wait for the prior candidate call. The tested hostile detached candidate stopped after timeout before capture, with a stable heartbeat through the bounded post-return observation.
- Constructor and poll-stage selector exceptions triggered cleanup. The independent poll exception test reaped its child, closed all three pipes, and caused subsequent export to fail closed as cleanup-unverified.
- A write through the relocated fixture appeared only in its own backing source tree; the original fixture lacked the unique marker. Copied collector files had distinct inodes. This establishes independence of the manually prepared copies, not an automatic per-run workspace lifecycle.
- The six-tool controller completed a synthetic capture/submit/result/replay flow into a local SQLite ledger. The queued job was not executed; replay remained withheld. **Zero games and zero model calls.**

## Provenance and reproduction

All five historical namespace baseline files and four trusted-service snapshot files matched their recorded SHA-256 values and the corresponding current source files. See `baseline-verification.json`. The source checkout later committed the identical service bytes at `8f2125d12db4df1f16bca721179ec52cf16273d6`; the original manifest's `base_commit` identifies the earlier working-tree base, not necessarily the final source snapshot commit.

The seven original implementation/test hashes in `original-sha256.txt` were checked again after the final tests and remained unchanged. `relocated-sha256.txt` records the independent copy. The copied in-root collector and IO helper matched their host-side trusted source files.

Execution command:

```sh
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=/workspace/shared/source-export-independent-review/fixture \
python3 /workspace/shared/source-export-independent-review/test_independent_export.py
```

The supervisor used the existing host runtime, while namespace work used the exact already installed manifest-selected Nix Python closure. No new dependency, model call, game, credential, netlink operation, network setup, cgroup change, host-security change, or aggregate stress workload was used. No denied operation was retried.

The publication-only materialization helper was inspected and its read-only `--check` independently returned `prerequisites_present` for 22 runtime paths. Its `--materialize` path was **not executed** in this review; the independent test fixture was explicitly copied and relocated. This distinction is documented in the author's README.

## Remaining limits

- One backend instance's process-local lock does not exclude another backend instance/process or a trusted host writer of the same backing directories. Stable capture relies on teardown plus read-only collector mounts and that limited serialization premise.
- This fixture does not establish fresh per-run allocation/cleanup, multi-candidate isolation, authenticated workspace ownership, durable artifact storage, or durable capture/ledger atomicity.
- Aggregate descendant CPU, memory, process-count, and persistent disk quotas remain absent. Per-process rlimits and bounded reads are not substitutes.
- Production syscall/IPC/network policy, every possible descendant failure mode, and arbitrary hostile workloads were not established. The heartbeat observation is bounded evidence, not a universal teardown proof.
- Java syntax, package declarations, compilation, match execution, opponent confidentiality in a deployed evaluator, real inference transport, and competitiveness remain untested here.
- Real-launch and holdout gates stay closed. The new source-export evidence advances only this narrow integration step.
