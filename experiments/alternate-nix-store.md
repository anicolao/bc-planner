# Workspace-local Nix: measured experiment

Observed in the repository-work executor on 2026-10-16. Goal: determine whether Nix can use a writable path other than `/nix`, then fetch and run software. No provisioning guarantee follows from this snapshot.

## Result

Two distinct tests succeeded:

1. **Fetch, register, execute:** Nix fetched an official Debian GNU Hello binary package. `dpkg-deb -x` extracted it in the workspace; `nix store add-path` registered the extracted tree. Running `usr/bin/hello` from that store tree printed `Hello, world!`. Extraction was performed by the host Debian tool, not a Nix derivation. This is not `nix profile install nixpkgs#hello`.
2. **Actual derivation build:** Nix invoked the host shell and compiler to build a tiny C program in the custom store. The resulting binary printed `Hello from a Nix-built alternate store!`. This is an intentionally impure host-tool build, not a complete nixpkgs bootstrap.

The second test used explicit user approval to disable **Nix build isolation for that single command**. The outer platform sandbox stayed enabled. No global Nix configuration was changed. Further unrelated builds do not inherit that approval.

## Why this approach

The [official local-store documentation](https://nix.dev/manual/nix/2.34/store/types/local-store) distinguishes relocating a physical root from changing the logical store path. A different root still logically using `/nix/store` needs Linux namespaces/chroot to execute its programs. We did not use that route. We used the documented `local?store=...&state=...&log=...` form to change the logical path itself. Normal `/nix/store` substituters are incompatible, so ordinary nixpkgs packages may require local rebuilding. Store paths can be copied between stores only when their logical store settings match.

The earlier failure to create `/nix` remains true. The user explicitly requested this separate, workspace-local experiment; it did not attempt to override protected-directory permissions.

## Bootstrap

The official Nix binary installer targets `/nix`. Instead, we downloaded Debian's [trixie nix-bin package](https://packages.debian.org/trixie/amd64/nix-bin/download) and extracted it locally with `dpkg-deb -x`, without running package maintainer scripts or modifying the system package database. Its SHA256 matched the value published by Debian. Three missing shared libraries were also extracted from Debian's official HTTPS archive.

Files fetched from `https://deb.debian.org/debian/pool/main/`:

| Relative archive path | SHA256 observed |
| --- | --- |
| `n/nix/nix-bin_2.26.3+dfsg-1_amd64.deb` | `06e8338eb0ca303802fcfe4579e184dd308d9fa89f7f0aae5974e21fac8178fb` |
| `libc/libcpuid/libcpuid17_0.7.1+repack1-0.2_amd64.deb` | `6b22af1f39da6947e8abded41617a5a59dd2aacb46328a194b985eee6757a470` |
| `b/boost1.83/libboost-context1.83.0_1.83.0-4.2_amd64.deb` | `95951c6f8509608a53f26d4ac3015c326867a43b22b1004c387ff0dad6558510` |
| `l/lowdown/liblowdown2_2.0.2-2_amd64.deb` | `8bba5d59c957be0487a8597c8f537b0bdab8036f872d7f9f19d12a501d1d67b3` |

The library hashes are recorded observations of HTTPS downloads, not a claim that signed Debian repository metadata was independently verified. Other shared-library dependencies already existed on this Debian executor. Another image may need additional dependencies. This is not a system-wide Debian package installation, and it does not establish that `apt install` works.

## Reproduction outline

Use a writable workspace directory as `BASE`; do not use a protected system path. Extract the four packages into `$BASE/bootstrap`. The measured launcher was equivalent to:

```sh
export BASE="$PWD/nix-alternate"
export LD_LIBRARY_PATH="$BASE/bootstrap/usr/lib/nix:$BASE/bootstrap/usr/lib/x86_64-linux-gnu"
export XDG_CACHE_HOME="$BASE/cache" XDG_CONFIG_HOME="$BASE/config" XDG_DATA_HOME="$BASE/data"
export NIX_CONF_DIR="$BASE/config/nix"
nix_local() {
  "$BASE/bootstrap/usr/bin/nix" --extra-experimental-features nix-command \
    --store "local?store=$BASE/store&state=$BASE/state&log=$BASE/log" "$@"
}
nix_local --version
# nix (Nix) 2.26.3
```

Nix's reported default `sandbox` was `true`, and `build-users-group` was empty. Configuration/cache locations were scoped to this experiment; no GitHub configuration was read or changed.

### Fetch/register/run test

```sh
nix_local store prefetch-file --json https://ftp.gnu.org/gnu/hello/hello-2.12.2.tar.gz
nix_local store prefetch-file --json \
  https://deb.debian.org/debian/pool/main/h/hello/hello_2.10-5_amd64.deb > "$BASE/hello-fetch.json"
deb=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["storePath"])' "$BASE/hello-fetch.json")
dpkg-deb -x "$deb" "$BASE/hello-package"
package=$(nix_local store add-path "$BASE/hello-package")
"$package/usr/bin/hello"
# Hello, world!
```

Nix reported source archive hash `sha256-WpqZbcKSzCTc9BHO6H6S9qrluNE72caBm0x6nc4IGKs=` and Debian package hash `sha256-RTaqu7dewh/+FhCZ7kuXJ0lFdwvbBoLiXsMiQhIRyl4=`. Both are recorded download hashes, not pre-specified independent expected hashes. The GNU source archive was fetched but not compiled in this experiment. The packaged Hello binary depends on host runtime libraries.

### Tiny build test

The following expression was saved as `$BASE/hello.nix`:

```nix
derivation {
  name = "workspace-hello";
  system = "x86_64-linux";
  builder = "/bin/sh";
  args = [ "-ec" ''
    export PATH=/usr/bin:/bin
    mkdir -p "$out/bin"
    printf '%s\n' '#include <stdio.h>' 'int main(void) { puts("Hello from a Nix-built alternate store!"); return 0; }' > hello.c
    cc hello.c -o "$out/bin/workspace-hello"
  '' ];
}
```

After the user approved the isolation tradeoff for this test only:

```sh
nix_local build --option sandbox false --option substituters '' \
  --file "$BASE/hello.nix" --out-link "$BASE/build-result" --print-out-paths
"$BASE/build-result/bin/workspace-hello"
# Hello from a Nix-built alternate store!
```

Nix reported a derivation being built and returned a path ending `r400f985lfp4jrpyn754z9pw6zyyvccf-workspace-hello` in this executor's alternate store. Store hashes depend on absolute store location and inputs; another workspace need not produce that hash. The result was executed successfully, not merely evaluated.

## Boundaries and next decision

- No root, `/nix` writes, system package database changes, mounts, namespaces, or chroot were used.
- Host `/bin/sh`, compiler, loader, and libraries are outside Nix's dependency closure; the result is not portable or hermetic.
- General nixpkgs builds, normal binary-cache substitution, profiles, reproducibility across machines, and Battlecode tooling were not tested.
- A practical production choice remains open: maintain this host-dependent custom-store bootstrap, investigate a properly provisioned standard Nix environment, or evaluate another supported runtime. This result demonstrates feasibility of a limited alternate store, not equivalence to a conventional Nix installation.


## Follow-up: canonical store inside a workspace root (2026-10-16)

The proposal is conceptually valid. Nix distinguishes the **logical** store path seen by programs from its **physical** location. Its [official local-store documentation](https://nix.dev/manual/nix/2.35/store/types/local-store.html) describes a local chroot store whose logical path remains `/nix/store` while files reside under a chosen root, such as `WORKSPACE/root/nix/store`. That preserves the store-path prerequisite for ordinary cache substitution; cache availability, trust and package execution still need separate verification. The documented Linux build/run implementation requires user and mount namespaces. This differs from our tested alternate **logical** store.

### Read-only capability observations

The command executor reported:

- UID/GID 1000 (`agent`).
- `chroot`, `unshare` and `bwrap` executables present; `proot` not found on PATH.
- `CapInh`, `CapPrm`, `CapEff`, `CapBnd`, and `CapAmb`: all zero.
- `NoNewPrivs: 1`; `Seccomp: 2`.
- `/proc/sys/user/max_user_namespaces`: 2147483647; `/proc/sys/kernel/unprivileged_userns_clone` unavailable.

[Linux chroot documentation](https://www.man7.org/linux/man-pages/man2/chroot.2.html) requires `CAP_SYS_CHROOT` in the calling process's user namespace. That capability is absent in the current namespace. A root-tree mirror using bind mounts also needs privileges not established here. A nonzero namespace count limit and installed tools do **not** prove that namespace creation or mounts are permitted by the platform and syscall filters. Conversely, these observations alone do not prove all unprivileged namespace creation is technically impossible.

```sh
id
command -v chroot
command -v unshare
command -v bwrap
command -v proot
grep -E '^(Cap(Inh|Prm|Eff|Bnd|Amb)|NoNewPrivs|Seccomp):' /proc/self/status
for f in /proc/sys/kernel/unprivileged_userns_clone /proc/sys/user/max_user_namespaces; do
  if test -r "$f"; then printf '%s: ' "$f"; cat "$f"; fi
done
```

### Outcome and boundary

This follow-up is a documentation and capability assessment, **not a successful or failed chroot execution test**. No chroot, user namespace, mount, ptrace emulation, root copying, or system-directory write was attempted. We could not establish a supported namespace/mount execution route consistent with the current platform restrictions, and stopped before those operations. The earlier approval to disable Nix's build sandbox covered only the tiny host-tool build, not this setup.

A practical next step is an explicitly supported runner with writable canonical `/nix`, or a documented platform-supported local-root-store namespace route that preserves the outer sandbox. A minimal package closure is preferable to copying the real root, which could expose unrelated credentials and data. The working workspace-logical-store experiment remains usable within its stated limits; this assessment does not upgrade it to ordinary cached nixpkgs execution.


### Other approaches considered

[PRoot](https://proot-me.github.io/) is a concrete userspace alternative: it translates filesystem-related system calls with `ptrace`, emulating a different root and path bindings without real privileged bind mounts or `CAP_SYS_CHROOT`. Conceptually it could map the process-visible `/nix` to workspace storage while physical accesses remain subject to the platform's restrictions. Missing chroot capability alone therefore does not rule it out.

PRoot is not installed in this runtime, and permitted tracing/path translation has not been established. Seccomp being active does not reveal which calls it permits. No PRoot, ptrace, or fake-root test has been run; installing a translator is not proof that it can execute here. A supported route must retain all outer filesystem restrictions, including denied reads, and must not depend on disabling the platform filter or exposing host credentials. Until that is established, this remains an unverified candidate rather than a working solution.

A workspace symlink alone cannot alter absolute `/nix/store` resolution. Rewriting ELF interpreter/library paths would instead modify the package artifacts and can miss embedded absolute paths; that is not a faithful canonical-store solution. The already-tested custom logical store remains the only demonstrated execution route in this experiment.
