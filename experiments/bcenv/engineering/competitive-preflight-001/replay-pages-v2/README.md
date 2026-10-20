# Existing-public-replay page proof

This is a read-only engineering check against the one already persisted public
3.0.13 game. It ran zero games and zero model/provider calls. The original replay
bytes remain unchanged. No authorization, deployment, isolation or trial claim
is made; actual heldout gates remain closed.

The two explicit windows were chosen before querying:

- Rounds 35–40: 455 matching rows, exactly reconstructed across 44 output pages.
- Rounds 300–301: 237 matching rows, exactly reconstructed across 23 output pages.

Every source page allowed 31 rows. Each projector call allowed 17 rows and 4,096
encoded bytes. Actual outputs held 6–12 rows, depending on coverage and row size.
The largest page was exactly 4,096 bytes. Continuation always used the number of
actually released rows, recovering the entire selected sequence without gaps or
duplicates despite the smaller byte budget. Per-kind whole-window counts and
per-match coverage agreed on every page. The actual new adapter `replay page`
command also passed at offset 100 with limit 3.

`feedback/` contains only sanitized canonical v2 responses. `verification.json`
contains compact results, source/code hashes and query provenance. These are
engineering evidence, not a public service response. `observer/` holds private
raw query JSON and stderr for local audit and is excluded from the shareable
archive. No replay, engine, map, bot binary or raw log is redistributed.

All 69 direct Java queries exited zero. Their stderr contained the same known
OpenJDK stack-location warning, not empty stderr. The extra actual CLI invocation
is recorded separately. The proof does not reconstruct world state, establish
within-round causal order, validate all schema fields, or prove player visibility.

## Reproduction

The preserved driver is `prove_existing_replay.py`. It requires a fresh output
directory, the unchanged original public bridge replay, the exact source checkout
recorded in `verification.json`, and the separately prepared pinned Java/Python
runtime root with newly compiled replay classes. It does not download, compile
or run a game. The source's absolute locations are recorded in the script and
must be adjusted explicitly after relocation. The shared archive is deliberately
not self-contained because redistributing the required replay/engine/map/bot
artifacts is outside this evidence bundle.

Run with existing Python:

```sh
python3 -B prove_existing_replay.py NEW_OUTPUT_DIRECTORY
```

`SHA256SUMS` covers this README, the verification report and every feedback page.

## Portable source snapshot

`code_snapshot/` includes the seven producer/projector/CLI files and existing
source dependencies used for the proof. `code-hash-manifest.json` records their
exact source hashes, base commit, compiled class hashes and engine hash. No
compiled class, engine or replay binary is included. `retrieval-design.md` is
the wider proposed integration design; service integration remains separately
reviewed. Paths/constants in the reproduction driver need explicit adjustment
after relocation. The pinned runtime and original authorized replay remain
external prerequisites.
