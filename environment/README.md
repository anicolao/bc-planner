# Pinned cloud tools

This flake pins nixpkgs through `flake.lock`; the first tool is Tailscale.
The runtime uses a workspace-backed root with canonical `/nix/store` paths.
It does not modify the host `/nix`, mirror the host root, or use bind mounts.

## Prerequisites and sync

Use Linux x86-64, permitted unprivileged user namespaces/chroot, and the
existing extracted Nix 2.26.3 bootstrap from the Nix experiments (PR #2).
This change does not recreate that bootstrap or promise all hosts support it.
Set these to absolute writable paths **outside the Git checkout**:

```sh
export BC_NIX_BOOTSTRAP=/path/to/nix-alternate/bootstrap
export BC_RUNTIME=/path/to/nix-canonical-root
./scripts/sync-environment
./scripts/tailscale-runtime version
```

Sync refuses local builds (`--max-jobs 0`), uses the committed lock without
updating it, verifies recursive cache signatures, then publishes the package
path. A cache miss is an explicit failure, not permission to weaken isolation.
`nix-root` is only for this extracted Debian bootstrap; an ordinary native Nix
installation can instead use the flake normally.

## Daemon and network boundary

```sh
./scripts/tailscale-runtime daemon
# In another terminal with the same BC_RUNTIME:
./scripts/tailscale-runtime status --json
```

The daemon is foreground, with a private state directory and Unix socket below
the workspace root. Stop it with Ctrl-C. This is userspace networking, not a
host-wide VPN: applications must opt into its loopback SOCKS5 proxy at
127.0.0.1:1055 after authorized enrollment. Do not use the proxy to bypass any
platform network restrictions. No host routes, DNS settings, exit nodes,
subnet routes, SSH service, or public listener are configured.

Enrollment is a separate approval step: select the intended tailnet/account,
then use the CLI login flow and approve the real link personally. Never put an
auth key, login link, node state or other credentials in this repository. State
is durable only while that workspace remains available. No daemon lifecycle or
workspace persistence guarantee is implied.

The minimal root may need explicit non-secret DNS resolver and CA certificate
configuration for login. Do not copy the host root, home directories, or
credentials. Package execution, daemon startup, enrollment and peer
reachability are independent validation gates.

## References

- [Nix flake locking](https://nix.dev/manual/nix/stable/command-ref/new-cli/nix3-flake-lock)
- [Tailscale userspace networking](https://tailscale.com/docs/concepts/userspace-networking)

## Observed result: 2026-10-16

- Lock resolved nixpkgs revision `b6018f87da91d19d0ab4cf979885689b469cdd41`.
- Sync fetched 58 paths (53.07 MiB download; 185.74 MiB unpacked) from the
  standard Nix cache and recursive content/signature verification passed.
- `tailscale version` ran inside the minimal root and reported **1.90.9**.
- `tailscaled --tun=userspace-networking` failed immediately with:
  `netmon.New: route ip+net: netlinkrib: operation not permitted`.
- No control socket or state file was created. No daemon remains running,
  login URL was generated, account was enrolled, or peer connectivity tested.

The denial concerns route inspection at startup, despite selecting userspace
mode. It does not prove that TUN is required, or identify the exact enforcement
layer. We stopped at the denied operation rather than weakening security or
patching around it. Installation is verified; enrollment readiness is **blocked**
in this tested runtime configuration. A supported runtime that allows Tailscale's
network inspection is needed before an enrollment test can proceed.
