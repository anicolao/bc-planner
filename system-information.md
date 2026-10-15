# dot execution environment: observed system information

Status: measured snapshot, 2026-10-15. These observations concern command-execution environments used by dot, **not the hardware running the language model**. They are not a service specification, guaranteed allocation, or benchmark.

## Repository-work executor

Read-only measurements taken directly in the executor used for GitHub CLI and this PR at approximately 23:06 UTC:

| Item | Observed value |
| --- | --- |
| OS | Debian GNU/Linux 13 (trixie), full version 13.6 |
| Kernel / architecture | Linux 6.18.44, x86_64 |
| Exposed logical CPUs | `nproc`: 9; allowed CPU list: 0–8 |
| Reported processor model | AMD EPYC 9V74 80-Core Processor |
| Memory | 9.7 GiB total; approximately 8.3 GiB available at measurement |
| Swap | None reported |
| Workspace filesystem | Overlay, 32 GiB reported size, approximately 30 GiB available |
| Temporary filesystem | `/tmp` is tmpfs, 4.9 GiB reported size, approximately 4.9 GiB available |
| CPU / memory cgroup quota files | `cpu.max` and `memory.max` not readable at the standard cgroup v2 paths |

The processor model string does **not** mean this executor has 80 cores. Exposed CPU affinity does not establish dedicated CPU capacity or an effective CPU quota. The reported memory and disk sizes may not equal enforced limits. `/tmp` is RAM-backed: its apparent capacity is not additional disk or additional independent memory.

## Separately reported voice-command executor

The voice session independently reported the following on 2026-10-15: Debian 13.6/trixie; Linux 6.18.44 x86_64; 9 logical CPUs allowed on 0–8; the same AMD EPYC model string (approximately 2596 MHz as reported at that instant); 9.7 GiB total RAM with roughly 8.4 GiB available and no swap; 32 GiB workspace overlay with about 30 GiB available; and 4.9 GiB RAM-backed `/tmp`. It could not read the standard `cpu.max`, `memory.max`, or `memory.current` files, and reported unavailable `lscpu`/sysfs topology information.

These voice measurements are a relayed observation from that executor, not an independent measurement by this repository worker. Similar values do not establish that the voice and repository executors are the same machine or share authentication, processes, or files. Do not depend on that equivalence.

## Reproduction commands

```sh
cat /etc/os-release
uname -srmo
nproc
grep -m1 'model name' /proc/cpuinfo
grep Cpus_allowed_list /proc/self/status
free -h
df -h /workspace /tmp
for f in /sys/fs/cgroup/cpu.max /sys/fs/cgroup/memory.max; do
  if test -r "$f"; then printf '%s\n' "$f"; cat "$f"; fi
done
```

Missing quota files do not mean unlimited resources. Available memory, free storage, and frequency are time-dependent. Repeat measurements in the actual target executor before sizing a job; representative workload measurements are needed before setting concurrency.

## Operational observations

- `gh` is installed and authenticated in the repository executor. This is not evidence that another executor has that authentication.
- The default GitHub CLI configuration location was not writable. A separately approved writable configuration location with restricted permissions was used; the user approved unencrypted token storage. No token, device code, credential contents, or private configuration path is included here.
- The default npm cache was also not writable. `npm ci --cache /tmp/bc-planner-npm-cache` succeeded, installed pinned Husky, and activated hooks. This cache is disposable.
- This session's workspace is usable for this task. Persistence across restarts, durable hosting, background-process lifetime, dedicated capacity, and future executor equivalence are not verified.
- These measurements do not select a Battlecode hosting platform or authorize running competitors or spending on compute.
