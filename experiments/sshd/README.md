# Bounded localhost OpenSSH probe

Measured 2026-10-16: Nix-installed OpenSSH 10.3p1 passed `sshd -t`, listened on IPv4 loopback at an ephemeral high port, and returned `SSH-2.0-OpenSSH_10.3`. The daemon was stopped and temporary host keys removed. Authenticated login, SSH key exchange completion, forwarding, and external reachability were not tested.

The repository flake supplies `openssh` from its existing locked nixpkgs input. Fetch and verify its signed cache closure with the existing bootstrap/runtime:

```sh
export BC_NIX_BOOTSTRAP=/absolute/path/to/existing/bootstrap
export BC_RUNTIME=/absolute/path/to/existing/runtime
scripts/nix-root build path:$PWD#openssh --no-write-lock-file --no-link --max-jobs 0 --print-out-paths
export BC_OPENSSH=/nix/store/bayms28s5qgq8nygm88csikkqrlcvpnj-openssh-10.3p1
scripts/nix-root store verify --recursive --sigs-needed 1 "$BC_OPENSSH"
python3 experiments/sshd/test.py
```

Python is the runtime's pre-existing orchestration tool; no Python packages are installed. The script uses the pinned package's physical store location and glibc loader because this workspace does not have host `/nix`. The explicit loader is tied to this lock snapshot. Library search uses existing runtime store library directories. Refresh these assumptions when changing the flake lock.

The first startup attempt validated configuration but failed because the compiled canonical `sshd-session` path was absent. OpenSSH's packaged manual documents `SshdSessionPath` and `SshdAuthPath` as test overrides. Temporary wrappers invoke those same unmodified Nix-provided helpers through their loader. No system configuration, root filesystem, privilege separation policy, or sandbox setting is altered.

All authentication methods configured by this probe are disabled: password, keyboard-interactive, and public key. PAM, root login, TTY, and forwarding are disabled, and no authorized keys are loaded. It uses the existing unprivileged account. Temporary host keys identify only this short-lived local test and are never printed or committed. The TCP probe reads only the banner and immediately disconnects. Startup polling is bounded; `finally` terminates the daemon, and temporary-directory cleanup deletes keys/config/wrappers. Failure to obtain a banner is a failed test, not evidence that authentication works.

A free loopback port is selected before startup, leaving a small port-allocation race; a conflict fails the test safely. This is an experiment, not a deployable SSH service. Any usable authenticated or persistent service needs separate configuration and authorization.

## Related diagnostics

The coordinating task observed no SSH listener on loopback port 22 before this experiment. It also observed proxied HTTPS succeeding and outbound UDP sends to three specifically tested destinations returning `ENETUNREACH` (errno 101). Those observations do not prove all TCP succeeds or all UDP is blocked; the successful local SSH banner is an independent, narrower result. No public egress address is recorded here.
