# Experimental fixed-fixture OS boundary

Date: 2026-10-20 UTC. Scope: actual Linux sandbox operations against disposable synthetic data on the existing dot executor. No model inference, credentials, real opponents, evaluator state, selected holdouts, paid resources, Mac work, or active-repository changes.

## Result and acceptance decision

**A concrete trusted-side SandboxAdapter now runs workspace read, write and exec through the same enforced root. Twenty-one bounded synthetic adversarial tests pass. This remains an experimental fixture, not an accepted autonomous-competitor deployment.** Aggregate resource budgets and the separate supported inference transport are still missing. The real-launch gate remains closed in the existing controller.

This is a safe alternative to the earlier failed bubblewrap launch: it creates an empty network namespace and never opens NETLINK_ROUTE or configures loopback. The original one-attempt bubblewrap denial remains unchanged in `REPORT.md` and `results.json`. It was not retried or bypassed; no host controls were relaxed. Those two files are historical first-attempt reports, not the outcome of the later permitted unshare work.

## Concrete implementation

- `probe_adapter.py` implements the existing controller's typed `read`, `write` and `exec` seam. Launcher path, environment, mounts and namespace flags are trusted fixed configuration. Model-controlled arguments become candidate argv only after these controls have been established.
- `parent_death_guard.py` installs SIGKILL on its own parent death, verifies the expected parent PID supplied by the adapter, and execs the fixed unshare command. This closes the race in which its controller dies before the death signal is installed.
- `namespace_launcher.py` runs inside new user, mount, PID, network, IPC and UTS namespaces. It binds only the fresh fixture root and two fresh writable subdirectories, creates private proc and a 4 MiB noexec tmpfs, remounts the fixture root read-only, and chroots into it. The empty network namespace is left unconfigured.
- It drops all bounding, inheritable, permitted, effective and ambient capabilities, enforces no-new-privileges, closes descriptors above 2, and clears the environment. Only HOME, pinned-runtime PATH, LANG and PYTHONDONTWRITEBYTECODE remain.
- The immutable trusted launcher **retains namespace PID1**, marks itself non-dumpable, and starts the untrusted candidate as PID2. It waits for the candidate and then exits; Linux destroys surviving descendants when namespace init exits. Candidate code never controls the trusted init's parent-death signal. The init receives no real secrets in its environment, input or descriptors.
- `io_worker.py`, copied into the read-only fixture at `/opt/io_worker.py`, handles bounded read/write requests inside that same launcher. Directory and leaf opens use O_NOFOLLOW. Writable roots are `src` and `scratch`; other public roots are read-only.
- The host-side supervisor uses nonblocking pipes and a combined output cap. Its deadline stays active if the candidate closes all streams. Every post-Popen setup action is inside cleanup, and all three pipes are explicitly closed even on selector setup failure.
- Per-process limits: address space 16–256 MiB, CPU 5 seconds, file size 1 MiB, 64 descriptors and no core files. Supervisor wall allowance is 1–10 seconds. These do not implement aggregate tree budgets.

All imports, launcher paths and fixture paths are explicit in the source. The host controller import is intentionally fixed to the local repository. This is not a portable installer or a production service.

## Tests and observed evidence

`PYTHONDONTWRITEBYTECODE=1 python3 test_boundary.py` completed with **21 passed, 0 failed**. `unshare-results.json` holds structured evidence and `latest-test-output.jsonl` records the latest run. These are bounded tests, not a proof against every kernel attack or resource-exhaustion strategy.

| Boundary | Evidence |
| --- | --- |
| Outside-root confidentiality | Synthetic outside canary absent via absolute path, parent traversal and proc-root aliases. No real secret was probed. |
| Immutable reference/runtime/helper | Mountinfo shows `/` as `ro,nosuid,nodev`; docs/helper/runtime writes and chmod were denied; hashes unchanged. Runtime append returned EACCES, while docs/helper append returned EROFS. The read-only mount assertion is independent of these errno differences. |
| Capabilities | After candidate exec: CapInh, CapPrm, CapEff, CapBnd and CapAmb are zero; NoNewPrivs is 1. Candidate chroot/remount attempts fail EPERM. |
| Descriptors/environment | Deliberately inheritable synthetic host-canary FD was absent; only 0/1/2 survive. Synthetic parent environment marker is absent. |
| Process visibility | Candidate sees only trusted init PID1 and itself PID2; a fresh dedicated host process is absent and signal-zero returns ESRCH. |
| Empty network namespace | Connect to a dedicated synthetic host-loopback listener returns ENETUNREACH; listener accepts no connection. No external address or network configuration was used. |
| Unified read/write/exec | A write through the adapter is read through both adapter read and candidate exec with identical contents. |
| Symlink I/O | Adapter read/write reject synthetic outside-root and read-only-reference symlink leaves; both canaries unchanged. |
| Normal exit and timeout | A setsid descendant's heartbeat stops when candidate exits or supervisor times out. |
| Output and stream handling | 100,000-byte output attempt retains at most 2,048 bytes and is terminated. Closing all streams still times out at approximately 1.004 seconds. |
| Setup failure | Injected DefaultSelector-constructor failure kills/reaps the child and closes all three pipes. |
| Controller death | SIGKILL of a fresh dedicated outer controller stops its candidate/setsid descendant well before its bounded natural lifetime. |
| Hostile death-link manipulation | Candidate calls setsid, clears its own PDEATHSIG, closes 0/1/2 and writes a bounded heartbeat. Timeout stops it at 38 bytes; a separate outer-controller-death test stops it at 1 byte. Both remain stable during a 0.25-second post-return observation before their 3-second natural end. |
| Trusted-init state | Candidate PID2 has parent PID1; opening init memory/FD0 yields EACCES and ptrace attach yields EPERM. |
| Per-process/per-file limits | An 80 MiB allocation under a 64 MiB address-space limit raises MemoryError. A synthetic file write fails EFBIG at 1 MiB. No aggregate stress test was used. |
| Actual controller integration | The unchanged controller plus scripted synthetic transport performs a real sandbox write/read/exec round-trip, preserving frozen initial-context hash. |
| Six-tool registry | Absolute host read/write rejected, native `exec_command` rejected as unknown, allowed workspace_exec sees outside canary absent. No provider/model is involved. |

## Review findings preserved and fixed

1. The first immutable-file test required EROFS for every write; the pinned executable instead returned EACCES. The assertion was corrected to require denial, unchanged hashes and an explicit read-only mount entry. This was a test expectation error, not a successful mutation.
2. Code review identified that closing stdout/stderr could leave the supervisor waiting outside its requested deadline. The event loop now also watches child lifetime; a closed-stream regression passes.
3. Independent review reproduced a selector-construction exception leaving a live child and three open pipes. All post-spawn setup now has mandatory kill/reap/close cleanup; the exact regression passes.
4. A guard was added because unshare's child-death option alone did not tie the outer controller lifetime to unshare.
5. **Independent review then found an actual timeout escape in the intermediate implementation.** Untrusted code was namespace PID1; it called setsid, cleared PDEATHSIG and closed 0/1/2. The adapter returned timeout at 1.0042 seconds, but its bounded heartbeat grew from 38 to 44 bytes 150 ms afterward. The reviewer's synthetic program had a fixed 3-second natural lifetime and was confirmed stopped. That design is rejected. The corrected implementation keeps trusted non-dumpable PID1 and runs candidate code as PID2. Both timeout and outer-controller-death hostile regressions now pass. Merely adding a parent-death guard was insufficient.

Independent re-review of this final source snapshot also passed all 21 bounded tests, plus an additional selector-poll exception cleanup probe. Its hostile timeout observation was 1.0063 seconds with a stable heartbeat, and the hostile outer-controller-death test passed. `bc23-sandbox-independent-review.md` and `bc23-sandbox-independent-review-results.json` record the separate observations and exact matching source hashes. The independent verdict permits only experimental fixed-fixture publication with the remaining deployment gates closed.

## Remaining hard gates

### Aggregate resources: not implemented or accepted

Read-only observation: `/proc/self/cgroup` reports `0::/`; `/sys/fs/cgroup` is not exposed. This does not prove that the platform has no global resource controls. It does mean this work found no delegated per-job interface and did not establish per-competitor aggregate enforcement. No cgroup creation, delegation, privileged configuration or host-security change was attempted.

The fixture lacks an aggregate process-count limit, aggregate resident-memory limit, aggregate CPU budget, and bounded persistent writable volume. Per-process rlimits, per-file limits, a wall timer and a 4 MiB temporary mount are insufficient: many descendants/files can multiply consumption before termination. No fork bomb, disk fill or memory stress run was attempted.

Minimum deployment requirement: an already authorized runtime/orchestrator must place the complete job tree, including trusted init and every descendant, under enforced aggregate CPU, memory and PID limits, using a job cgroup or a platform-enforced equivalent. It must provide reliable whole-job termination and a writable-volume byte/inode quota covering source, scratch, artifacts and temporary output. The controller should receive bounded handles/results, never authority to change those host controls. Provisioning such controls is a separate operator-supported deployment step, not a change made here.

### Model/provider capability boundary: not implemented

The model used in these tests is a scripted synthetic `ModelTransport`. There was no real inference. A native agent in this session still has unrestricted host-side tools relative to this fixture and therefore must not be used as the competitor. A supported provider integration must expose only the six registered tools and route every workspace operation through this enforced adapter. The existing CLI/provider path remains independently blocked; no credential or daemon-mask workaround was attempted. `services.controller.launch_real` remains permanently unsupported.

### Other deployment work

- Per-run workspace creation, lifecycle, ownership and concurrent-job isolation are not implemented; these tests use one fixed disposable synthetic workspace.
- No artifact publisher, safe frozen-source handoff, actual Java/BC2023 runtime, evaluator deployment, service authentication or holdout connection is provided.
- The existing platform seccomp filter is inherited; this work did not build or certify a candidate-specific syscall allowlist. It does not claim protection from kernel vulnerabilities.
- Host orchestration and fixture preparation are trusted. A host-side native agent can still edit fixture backing paths; the candidate does not receive that capability. Public evaluator architecture/source may be visible, but deployed private state and selected holdouts must never be mounted or passed into this boundary.
- Non-dumpable init and process-namespace tests protect this fixture's control state; they are not permission to place secrets in init. Production cleanup should use independently enforced job containment as well.

## Provenance and compact delivery

The Python runtime is the existing pinned Nix closure listed in `fixture-manifest.json`: 22 paths, 209,890,448 registered NAR bytes, approximately 218 MiB copied fixture size. No runtime download or installation occurred. The compact deliverable excludes this closure, writable workspace, canaries and transient process state.

`prepare_fixture.py` and the README give exact materialization steps for that existing closure, the no-follow I/O helper and synthetic layout. The script refuses existing targets; its read-only prerequisite check passed for all 22 paths. It was extracted after the current fixture was prepared, and a fresh materialization using the script was not rerun. This distinction is recorded rather than claiming an independently reproduced installation.

Controller source SHA-256: `83d585a54d1e3c8698cf7efba8ae16e494683230865b698e0677f9b7964b4929`.

Controller contract SHA-256: `fbf1e30055048fe194d252ca49bc0a19e9893abfd0158981973d7873b587b8d6`.

Repository HEAD observed during this probe: `04c815954154a9be691bb531245f74e35cbd6edf`. The source hashes identify the actual files used even when the repository contains concurrent work.

The scripts are suitable for a separate experimental trusted-side review/change, with the failed deployment gates attached. They must not be used to enable a real launch or relabeled as complete isolation.
