# Runtime experiments: consolidated conclusion

Decision, 2026-10-16: **We failed to provide usable remote access in this runtime. There is no immediate need for it, so further remote-access work is deferred.** This is a bounded outcome of these experiments, not a claim that remote access is impossible everywhere.

## What remains useful

- [Nix experiments](alternate-nix-store.md): workspace-local store evaluation, signed-cache realization and verified canonical-path execution in a minimal root. Earlier failed approaches and runtime limitations remain documented.
- [Pinned environment and Tailscale](../environment/README.md): pinned tools and reusable helpers; stock Tailscale userspace startup failed before login because interface enumeration requires a denied netlink operation. No successful enrollment or remote session.
- [Userspace WireGuard](wireguard/README.md): encrypted local userspace tunnel and application exchange succeeded. This does not establish external UDP reachability, a remote peer, or a usable remote-access service.
- [Local OpenSSH](sshd/README.md): Nix OpenSSH configuration and ephemeral loopback banner succeeded. Authentication, complete key exchange, forwarding and external reachability were not tested.

Observed UDP errors apply only to the tested destinations. Proxied HTTPS success does not establish general direct TCP or inbound connectivity. No network restrictions, access controls or persistent remote service were changed to reach this conclusion.

## Consolidation and provenance

PRs [#2](https://github.com/anicolao/bc-planner/pull/2), [#3](https://github.com/anicolao/bc-planner/pull/3), [#4](https://github.com/anicolao/bc-planner/pull/4), and stacked [#5](https://github.com/anicolao/bc-planner/pull/5) are combined into one linear change based on current main. Original source branches and commits remain available; they are not rewritten or deleted.

[The provenance manifest](consolidation-provenance.json) identifies exact source heads, source-relative file hashes and prompt-append hashes. Every experiment source/document is preserved byte-for-byte. The shared lock and Nix helper are identical across their source branches; the final flake is the superset from PR #5 (Tailscale, Go and OpenSSH). The prompt record retains main's original bytes and each branch's exact additions, tagged by source to disambiguate repeated entry numbers. This integration does not pretend the independent branch records formed one global chronological transcript.

The repository's GitHub workflow verifies prompt hygiene only. It is not evidence of remote connectivity or an end-to-end Battlecode run. New Battlecode prior-art research is separate from these concluded infrastructure experiments.

## Consolidated-tree verification (2026-10-16)

- `npm test`: 9 tests passed, including prompt-history/hook regression fixtures and environment-helper checks. Existing installed Husky tooling and enabled hooks were reused; no package-manager installation was performed.
- `scripts/test-wireguard`: recursive Nix cache signature verification, Go 1.25.10, module checksums, unit tests, build, two real local handshakes and exact TCP payload exchange all passed using the pre-existing dependency cache with downloads disabled.
- `python3 experiments/sshd/test.py`: pinned OpenSSH configuration validation and ephemeral loopback banner passed; daemon terminated and temporary keys/config removed.
- `sh -n scripts/test-wireguard`: passed. The staged/base-relative whitespace check flags one historical trailing space in `experiments/sshd/test.py:25`; it is deliberately retained to preserve the exact source snapshot. The initial unstaged check did not include that then-untracked source file. This is not a clean whitespace-check result.
- Independent comparison against all source commits: 22 retained source-relative file hashes matched; all four source prompt additions occur byte-for-byte in the consolidated record; main's prompt record remains its exact prefix. The only superseded source file versions are the narrower PR #3/#4 flakes; PR #5 adds their outputs without changing the lock.
- Tailscale startup, previously denied netlink operations and external connectivity were not retried; their historical evidence and limitations remain unchanged. No Battlecode implementation/evaluation is part of these checks.
