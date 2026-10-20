# Public Battlecode 2023 provenance and compatibility evidence

This directory is ready to copy into a documentation repository. It records six public source candidates and a bounded integration check, not a benchmark selection, strength ranking or sealed evaluation assignment.

## Result

- Six unchanged packages compiled and passed the official verifier on public engine 3.0.13.
- Ten of eleven DefaultMap attempts completed. v5anaconda side A hit the fixed 120-second timeout; side B completed in about 22 seconds. There was no retry.
- Every package has completed-game activity evidence. v5anaconda has not passed the paired-side completion check.
- Original 128 KiB/file and 1 MiB total limits reject two packages. The corrected 512 KiB/file and 2 MiB total limits in [bcenv PR7](https://github.com/anicolao/bcenv/pull/7), change `f91e1ce`, fit all six measured packages. Original failures remain recorded.
- The actual adapter was the initial `wzmq4kaajn9bizwmy4x6n0hbjn97v46a` store output. These checks do not claim execution of the subsequently published final package.

Start with `bc23-public-opponent-candidates.md` for historical provenance and `REPORT.md` for executable evidence and its limits. The Nix/JSON catalogs bind repository revisions, source NARs, target packages, licenses and all 89 Java files. `metadata/` retains small original build/match records and logs, including the timeout. `runtime-file-hashes.json` identifies the actual tools. `evidence-manifest.json` is the inventory of separate raw scratch artifacts; those payloads are intentionally absent here.

## Licensing and contents

Bot sources remain separate AGPL-3.0 artifacts, fetched by the fixed-output catalog rather than vendored here. Their six verified root notices are in `licenses/`. The engine source has no established repository-wide engine/map redistribution grant in this audit; schema/client component notices are not treated as map permissions. This directory contains no Java bot source, class binaries, engine JARs, maps, replay payloads, Nix runtime closure, credentials or sealed assignments. It contains only public provenance, measurements, metadata, logs, notices and observer scripts.

Official engine source: [3.0.13 source revision](https://github.com/battlecode/battlecode23/tree/9b890f83672c98b81cc153f618bd56e1ab6134b5). Engine and map hashes are in every match record. Historical package-to-server-upload equality and model-training novelty remain unverified.

## Offline verification

Run from any directory:

```sh
python3 /path/to/this-directory/verify_evidence.py
```

This checks local file inventory, source/license/build linkage, successful build steps, match metadata/log digests, complete summary flags and the preserved timeout. It runs no bot and creates no game. It cannot independently rehash omitted binary/replay payloads; their recorded hashes support comparison with the separately retained originals. Hash records are integrity evidence, not a hostile-writer security boundary.

## Reproduction, only under a separately authorized game budget

The original combined integration budget has already been used. These scripts do not authorize more executions.

1. Obtain nixpkgs at the exact revision in the catalog JSON. Evaluate `reproduce/fetch-sources.nix` with that pinned `pkgs` argument and realize its six fixed-output attributes. This runs archive fetch/unpack only, never upstream Gradle. Preserve normal TLS verification; no local trust paths are embedded here.
2. Obtain the exact engine/adapter/JDK/Python closure named in `smoke-manifest.json`, with the canonical store identities intact. The catalog fetch does not supply that runtime. A normal store uses `--store-root /`; a relocated canonical store uses its explicit containing root. Old Nix paths may require rebuilding the matching source, not substituting an available newer package.
3. Create a fresh isolated root with the existing authorized namespace/chroot pattern:

```sh
python3 reproduce/materialize.py --store-root /path/containing/nix --destination /fresh/public-smoke
```

4. Only after separately authorizing compilation and up to eleven games:

```sh
python3 reproduce/run_smoke.py --root /fresh/public-smoke --execute
python3 reproduce/query_activity.py --root /fresh/public-smoke
```

Materialization copies the explicit closure and hash-checked public source files; it does not execute bots. Execution clears inherited environment values, uses a user/network namespace plus chroot, and binds no host directories. The execution script refuses repeat invocation even after a partial run. It uses a 120-second process limit and one lecture self-play plus paired positions for the five other packages. Do not remove the guard to retry. The isolation remains an experimental integration harness rather than an independently validated hostile-code service boundary.

The scripts are parameterized adaptations of the recorded harness and were syntax/help checked; they have not been used to run another reproduction. Existing outputs are the evidence of the original run. Reproduction can expose nondeterminism or environment-dependent timing rather than guarantee identical outcomes.
