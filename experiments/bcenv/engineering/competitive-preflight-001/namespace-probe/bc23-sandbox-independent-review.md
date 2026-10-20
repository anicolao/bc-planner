# Independent review: synthetic namespace adapter

Reviewed 2026-10-20 UTC. Source directory: `/workspace/shared/bc23-sandbox-probe`.

## Verdict

Acceptable to publish as an **experimental, fixed-fixture integration probe**, with the real-agent/heldout and aggregate-resource gates closed. No remaining must-fix was identified within that narrow scope after the lifecycle corrections below. This is not acceptance of a production sandbox or permission to execute arbitrary hostile workloads.

The initial bubblewrap `NETLINK_ROUTE` denial remains a real failed attempt. It does not mean namespace execution is unavailable: the separately permitted, fixed-fixture unshare route was subsequently exercised successfully. Review did not retry bubblewrap, configure networking, modify host security, access actual secrets or heldouts, invoke a model, or run aggregate stress loads.

## Independently verified

All **21 existing bounded synthetic checks passed** on the final source snapshot. Exact observations and SHA-256 hashes of all five source/test files are recorded in `bc23-sandbox-independent-review-results.json` beside this report.

- The candidate saw a read-only root, writable `src`/`scratch` mounts, and a private proc/tmp layout. Reference/helper/runtime writes and chmod attempts failed; their hashes stayed unchanged.
- Synthetic outside-root canary paths, traversal and proc-root approaches failed. Read/write/exec shared the same fixture root; symlink reads/writes were rejected.
- After exec, CapInh/CapPrm/CapEff/CapBnd/CapAmb were zero and NoNewPrivs was 1. A separate two-exec probe also retained zero capabilities despite namespace UID0. Namespace chroot/remount attempts failed.
- Candidate descriptors were only 0/1/2, and its environment was explicitly sanitized. Its proc view contained trusted PID1 and candidate PID2; the tested outside process was unreachable.
- A fresh synthetic host-loopback listener was unreachable. This is a narrow network observation, not proof that every socket family or IPC channel is blocked.
- Combined output retention was capped at 2,048 bytes. Closing stdio did not evade the deadline. The tested address-space and file-size limits worked per process/per file only.
- Fixed synthetic controller replies successfully exercised write/read/exec. Absolute host reads/writes and a native `exec_command` request were rejected; the allowed workspace execution could not see the outside canary.

## Defects found and corrected

1. **Post-spawn setup exception leaked work and pipes.** Injecting selector construction failure originally left a live job and three open pipes. All post-Popen setup is now inside mandatory cleanup. The regression reaps the child and closes every pipe. An additional independent selector-poll exception probe also confirmed cleanup.
2. **Outer-controller death was not tied to unshare.** A trusted guard now installs its own SIGKILL parent-death signal, immediately checks the trusted expected parent PID, and execs fixed unshare. Bounded outer-controller-death tests pass.
3. **Hostile namespace PID1 could disable teardown.** The reviewer reproduced `setsid(); PR_SET_PDEATHSIG=0; close(0/1/2)` surviving a reported timeout: heartbeat grew from 38 to 44 bytes after return. A guard alone did not fix this. The immutable launcher now remains non-dumpable namespace PID1 and launches candidate PID2. On independent rerun, the hostile candidate timed out at 1.0063 seconds and its heartbeat remained stable for the observation window; the same candidate also stopped after outer-controller death. Candidate access to PID1 memory/fd0 and ptrace attach was denied. Normal candidate exit also terminated its detached descendants.

These are bounded regression observations, not a proof against every kernel failure or adversarial execution.

## Gates still unpassed

- Aggregate descendant PID, memory, CPU and disk budgets: not implemented or accepted; rlimits are not substitutes.
- Fresh per-run workspace lifecycle, cleanup and concurrent-candidate isolation: not established; this probe reuses fixed writable fixture directories.
- Explicit production kernel/syscall/IPC policy: not established; the existing host seccomp filter is inherited. Every network family was not tested.
- Artifact packaging/publication, real inference-provider integration, authenticated production service integration and real-agent trials: not implemented or exercised here.

Keep publication claims scoped to these fixtures and tests. Do not advertise a fully isolated competitor runtime or use this evidence to open the remaining gates. No implementation source was edited or committed by the reviewer; only separate review evidence and this report were written.
