# Synthetic namespace probe artifact

Start with `UNSHARE-REPORT.md` and `unshare-results.json` for the current result: 21 passing bounded tests; actual fixed-fixture adapter; full deployment still blocked by aggregate quotas and supported provider transport.

`REPORT.md` and `results.json` preserve the initial failed bubblewrap attempt. No NETLINK_ROUTE retry or host-security change occurred. `unshare-first-results.json` preserves the first unshare test pass, including an overly narrow errno assertion subsequently corrected.

## Files

- `probe_adapter.py`: experimental implementation of the existing controller's SandboxAdapter.
- `parent_death_guard.py`: trusted controller-to-unshare lifetime link.
- `namespace_launcher.py`: fixed namespace mounts, chroot, capability drops, rlimits and trusted PID1.
- `io_worker.py`: no-follow read/write helper inside the immutable root.
- `test_boundary.py`: bounded synthetic probes and actual-controller/scripted-transport integration.
- `prepare_fixture.py`: trusted exact-closure copy and synthetic-fixture materialization; refuses existing targets.
- `fixture-manifest.json`: exact already-installed runtime closure paths, not the closure itself.
- `latest-test-output.jsonl`, `unshare-results.json`: latest actual run evidence.
- `bc23-sandbox-independent-review.md` and matching JSON: independent final review, including 21 passing checks and additional setup/poll cleanup observations.

## Reproduction scope

This is intentionally a fixed-fixture artifact, not a portable deployment package. Paths in source identify the actual synthetic probe directory, existing local controller checkout and existing host/Python runtime. The prepared fixture lives at `/workspace/shared/bc23-sandbox-probe/fixture-root`, with the listed Nix paths, empty `proc/dev/tmp`, `/opt/io_worker.py`, a synthetic reference at `workspace/docs/canary.txt`, and writable `src/scratch` backed by fresh directories outside the immutable root. No host home, credentials, daemon socket, evaluator state or holdout data belongs in it.

The existing source root used here is `/workspace/scratch/1523a3f802eb/nix-canonical-root/root`. It already contains the 22 exact registered public Nix paths. The helper does not download or install anything. With scripts at the fixed probe directory, check prerequisites read-only:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 prepare_fixture.py --check
```

On a fresh absent destination, materialize the exact fixture:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 prepare_fixture.py --materialize
```

This copies each manifest path to the same `/nix/store/...` location beneath `fixture-root`, preserving symlinks; creates the listed empty mount points and workspace directories; copies `io_worker.py` to `fixture-root/opt/io_worker.py`; and writes only the two documented synthetic markers. Existing `fixture-root`, `writable` or outside-marker targets cause a hard refusal, with no replacement or cleanup. A trusted integrator may explicitly supply another already prepared source root using `--source-root`, but it must contain every exact pinned path. Runtime/source selection is not exposed through a model tool.

The materializer's read-only prerequisite check was executed successfully here. The existing fixture was created by the same copy/layout operations before this script was extracted; materialization was not rerun over it. There is no hidden installer step. The launcher itself applies the read-only root bind and the two writable subdirectory binds in its private mount namespace on every operation.

With this already authorized disposable fixture present, run from the probe directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 test_boundary.py
```

Tests create small synthetic files in the disposable writable fixture and short dedicated test processes. They do not require a model, a provider login, external network access, changes to host security, or an aggregate-resource stress workload. They preserve the real-launch gate.

The compact archive deliberately omits `fixture-root/`, `writable/`, host canaries and any installed runtime contents. Preparing another runtime/job environment requires a separate trusted integration step with its own authorization and acceptance tests. Never substitute live private inputs for the synthetic markers.
