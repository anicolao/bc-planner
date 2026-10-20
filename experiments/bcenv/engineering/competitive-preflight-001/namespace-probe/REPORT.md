# Actual sandbox deployment probe

Date: 2026-10-19 UTC. Scope: disposable synthetic fixtures on the existing dot executor. No model invocation, real opponent, holdout, credential, provider, host security change, or active-repository edit.

## Result

**The actual immutable-root sandbox launch is blocked on a platform-denied networking inspection/setup operation.** The first bubblewrap attempt exited 1 before the synthetic Python program ran:

```
bwrap: loopback: Failed to create NETLINK_ROUTE socket: Operation not permitted
```

The probe stopped at this denial. No retry, capability elevation, syscall-filter change, network weakening, daemon-mask bypass, or alternate route was attempted. A fixed SandboxAdapter was not represented as working, and no end-to-end controller isolation claim is made.

## Work actually performed

1. Read-only checks found bubblewrap 0.12.0 and util-linux unshare 2.41.5. The executor has no effective/permitted/bounding capabilities, `NoNewPrivs=1`, and active seccomp filtering.
2. This standard namespace-only probe returned exit 0:

   ```
   unshare --user --map-root-user --mount --pid --fork --net -- /usr/bin/true
   ```

   This establishes that these namespaces can be created for a trivial child. It does not establish successful immutable mounts, proc isolation, credential separation, resource quotas, descendant cleanup, or safe arbitrary execution.
3. Copied only the existing registered Python 3.13.15 Nix closure into `fixture-root/`: 22 store paths, 209,890,448 registered NAR bytes. No download, new software acquisition, host installation, or authentication copy occurred. `fixture-manifest.json` lists the exact existing store paths. The source was the already prepared canonical-root Nix store; its database was opened read-only.
4. Created new empty `writable/src` and `writable/scratch` directories. The fixture contains a synthetic read-only reference canary; `host-canary.txt` is a separate synthetic outside-root marker. No sensitive files were used as test targets.
5. Attempted one actual launch with an explicit user/PID/network/IPC/UTS namespace set, dropped capabilities, new session, parent-death behavior, cleared environment, read-only fixture root, two writable fixture subdirectories, private proc/dev, and a 4 MiB temporary filesystem. Only these fresh fixture paths were requested as bind sources; no host root, home, existing workspace, credentials, or host socket was exposed.
6. The launch failed with the NETLINK_ROUTE denial above. The command's intended output markers (`fixture-started` and the reference canary) were absent. No synthetic adversarial workload or model was executed afterward.

## Exact attempted launch

```sh
bwrap \
  --unshare-user --unshare-pid --unshare-net --unshare-ipc --unshare-uts \
  --cap-drop ALL --new-session --die-with-parent --clearenv \
  --ro-bind /workspace/shared/bc23-sandbox-probe/fixture-root / \
  --bind /workspace/shared/bc23-sandbox-probe/writable/src /workspace/src \
  --bind /workspace/shared/bc23-sandbox-probe/writable/scratch /workspace/scratch \
  --proc /proc --dev /dev --size 4194304 --tmpfs /tmp \
  --setenv HOME /workspace \
  --setenv PATH /nix/store/h3l4z7p6wny3phbckwwhy1i2g52pdnj4-python3-3.13.15/bin \
  --setenv PYTHONDONTWRITEBYTECODE 1 --chdir /workspace -- \
  /nix/store/h3l4z7p6wny3phbckwwhy1i2g52pdnj4-python3-3.13.15/bin/python3 \
  -c 'import os;print("fixture-started",os.getpid()); print(open("/workspace/docs/canary.txt").read().strip())'
```

This records a failed attempt, not a recommended retry command. Do not rerun or weaken it to work around the denied operation.

## Gate status

| Gate | Status | Evidence |
| --- | --- | --- |
| Basic user/mount/PID/network namespace creation | Passed, narrow probe only | `/usr/bin/true` exited 0 |
| Start an immutable-root sandbox using the standard wrapper | Blocked | NETLINK_ROUTE EPERM, exit 1 |
| Read-only runtime protection under hostile commands | Not run | Sandbox startup failed |
| Outside-root canary confidentiality | Not run | Sandbox startup failed |
| Same enforced root for read/write/exec | Not implemented or tested | Requires a working launcher |
| Private proc/process/descriptor boundary | Not run | Sandbox startup failed |
| No-network behavior under hostile commands | Not run | Creating a network namespace alone is not this acceptance test |
| Bounded descendant termination and output | Not run | No candidate process launched |
| Aggregate CPU/memory/PID/disk enforcement | Unverified | No `/sys/fs/cgroup` interface exposed by targeted checks |
| Real controller integration | Not run | OS boundary unavailable; provider transport separately blocked |

`/proc/self/cgroup` returned `0::/`; this does not establish delegated cgroup control or an aggregate limit. A Python timeout, Java heap cap, per-process rlimit, or process-group kill cannot substitute for proving aggregate descendant/resource containment. No stress workload was attempted.

## Safe next step

Keep the prepared synthetic fixture and the service/controller unit tests as development evidence. The current boundary remains unaccepted. A supported runtime/launcher that can establish immutable inputs, process and descriptor isolation, no-network operation, descendant cleanup, and aggregate budgets is needed before implementing and claiming a real SandboxAdapter. Do not use a namespace-only success or the older per-command chroot wrapper to claim those missing guarantees. The separate supported inference-transport gate must also pass before an autonomous competitor runs.
