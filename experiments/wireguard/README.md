# Local userspace WireGuard proof

Observed 2026-10-16. **Two real WireGuard handshakes and TCP payload delivery succeeded in this runtime.** This is a bounded local capability test, not a persistent externally reachable endpoint or a whole-host VPN.

## Architecture and result

Two unmodified upstream wireguard-go devices use `tun/netstack` (gVisor userspace TCP/IP). The test supplies a small implementation of WireGuard's public `conn.Bind` interface using ordinary IPv4 loopback UDP. It accepts only numeric loopback endpoints, uses ephemeral OS-selected UDP ports, and rejects nonzero socket marks. No kernel TUN device, route changes, root privileges, namespaces, or sandbox changes are involved.

The default Linux `StdNetBind` failed with `operation not permitted` during `Device.Up()`: its optional sticky-socket route listener creates a NETLINK_ROUTE socket. Upstream explicitly does not install that listener for other Bind implementations. The custom transport does not discover or invent routes; the ordinary host UDP stack chooses the route. This proof deliberately forgoes sticky-source selection, batching, IPv6 transport, and interface-change notifications. It is not a production transport implementation.

The successful run reported:

```text
peer=0 handshake=verified rx_bytes=492 tx_bytes=452
peer=1 handshake=verified rx_bytes=548 tx_bytes=492
PASS: two real WireGuard devices exchanged TCP payload through userspace netstacks over loopback UDP; no external reachability tested
```

Byte counts vary between runs. The test checks nonzero handshake timestamps on both peers and compares an exact TCP echo payload, not merely a successful socket bind. It generates private keys in memory and never logs or writes them. All listeners/devices close on exit; a 20-second watchdog bounds the run.

## Reproduce this snapshot

The flake and lock pin the same nixpkgs revision as the separate Tailscale environment work. The `go` output resolves to Go 1.25.10. Sync verifies cache signatures recursively. `scripts/nix-root` is the common workspace-root helper from that work; it requires the already established Nix bootstrap and canonical workspace root, and does not create a host `/nix` directory.

```sh
export BC_NIX_BOOTSTRAP=/absolute/path/to/existing/bootstrap
export BC_RUNTIME=/absolute/path/to/workspace/runtime
export BC_GO_MODULE_CACHE=/absolute/path/to/existing/module/cache
./scripts/test-wireguard
```

The script runs the statically linked, Nix-installed Go tool directly with a physical `GOROOT`. This avoids needing `/dev/null` inside the minimal chroot (the initial in-chroot build failed because that device was absent). Go and the resulting program remain subject to the ordinary outer runtime restrictions.

The dependency cache was fetched during the initial experiment, before the user's flake-only correction. It is checked against the committed `go.sum` and the build uses `GOPROXY=off`, `GOSUMDB=off`, `GOTOOLCHAIN=local`, and `CGO_ENABLED=0`. No new modules or toolchains are downloaded by Go. The earlier directly downloaded Go 1.27.2 was not used for the successful final proof; Go 1.25.10 came from the flake and its signed cache closure.

**Reproducibility boundary:** this script replays the measured proof using its pre-existing module cache. It is not yet a clean-machine Nix derivation or a complete flake-managed acquisition of the Go dependency cache. A missing cache fails closed; no package-manager fallback is provided. Future new dependency acquisition must be integrated into the flake under AGENTS.md. `go.sum` pins source content, but is not itself a Nix install recipe.

## What remains unproven

- No external UDP reachability, NAT traversal, remote WireGuard interoperability, or persistent service has been tested.
- There is no Tailscale control-plane integration and no enrolled tailnet node.
- The application must use this embedded netstack; host applications do not automatically gain VPN access.
- No private key or durable endpoint identity has been retained.

For the next end-to-end test, choose an actual remote WireGuard peer, its public key, UDP address/port, tunnel addresses, and permitted service. Keep private keys out of chat, logs, and this public repository. A local handshake alone cannot establish that this cloud runtime accepts incoming internet UDP.

## Primary sources

- [Upstream userspace HTTP example](https://git.zx2c4.com/wireguard-go/tree/tun/netstack/examples/http_client.go)
- [Public Bind interface](https://git.zx2c4.com/wireguard-go/tree/conn/conn.go?id=2631ce99a06f)
- [Linux sticky route listener and custom-Bind condition](https://git.zx2c4.com/wireguard-go/tree/device/sticky_linux.go?id=2631ce99a06f)

The exact wireguard-go revision and transitive versions are recorded in go.mod/go.sum. The test code in this directory is newly written for this experiment; upstream libraries retain their own licenses.
