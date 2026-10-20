# Durable replay route: portable offline evidence

Exact integrated source: bcenv `59242ba9935d777f787596adfc0b2b1efc34650d`, draft PR15.
No new game, real model call, authentication or accepted deployment is claimed.
The recorded composed source/result/replay association is a fabricated fixture.

The independent review records 286 repository tests and 27 external probes,
including all-six-tool Responses pagination. The final clean branch also passed
all 13 x86_64 flake checks; existing deterministic engine fixtures are included.
All 11 trusted service modules were absent from the runtime package. Historical
review source manifests and wrapper are retained unchanged; `reproduce.nix`
adds a portable wrapper around the exact published integrated commit.

On supported x86_64 Linux with Nix:

```sh
nix --extra-experimental-features 'nix-command flakes' build \
  --file ./reproduce.nix --out-link ./result -L
cat result/test.log
```

A first run may retrieve pinned public source/cache packages. This invokes only
synthetic probes, with no game or provider. The recorded local rerun uses the
same exact Git revision through a local flakeUri override, without fetching the
public GitHub default. A different caller-supplied revision is outside this proof.
Original review logs and full flake log are preserved verbatim, including any
formatting or environment paths. Hash manifests detect accidental drift only;
they are not authentication or a physical sandbox attestation.
