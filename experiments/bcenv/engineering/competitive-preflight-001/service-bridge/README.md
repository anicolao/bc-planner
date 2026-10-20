# Scratch public-engine service integration

This directory contains a completed, scratch-only integration experiment. It is
not a deployed service or a real-agent trial, and nothing here enables heldouts.
No files were added to the bcenv repository for this prototype.

## What actually ran

`bridge.py` submitted a source-only ZIP for the unmodified public
beaverbois `USQualifiers` package through a snapshotted `ScrimmageFacade`, staged
only the accepted normalized bytes into a fresh observer-owned job, then ran the
real pinned Java compiler and Battlecode verifier. It separately ingested and
fresh-built the unmodified public `lectureplayer` fixture. It then executed
**one new real game**, with candidate in slot A, on DefaultMap using final-rule
engine 3.0.13. Existing smoke-game outputs were not reused for this positive chain.

The selected matchup had already completed quickly in a public compatibility
smoke. It was chosen to test wiring, not as an unbiased strength measurement.
The bounded public response reports one complete game (one win); it is not a
ranking, performance estimate, accepted opponent evaluation or claim about
historical tournament submissions. No strategy/source bytes were edited.

The original namespace launcher and runtime directories were copied unchanged
from `/workspace/shared/bc23-public-smoke` into this separate fresh root.
The launcher clears the environment and invokes an existing user/network
namespace plus chroot, with no host bind mounts. No credentials, listener,
model inference or runtime security changes were introduced. Original smoke
artifacts were not modified. Parent-approved combined game budget was eleven
public smoke games plus this one integration game, twelve total.

## Evidence and validation

- `integration-report.json`: private observer record of fixed runtime hashes,
  source provenance, accepted content identities, build inventories, commands,
  log hashes, map/input/replay identity checks, game completeness evidence,
  snapshots and all four negative checks
- `public-result.json`: the actual bounded public response, with opaque ID and
  aggregate counts only; no opponent identity, paths, logs or schedule
- `root/workspace/jobs/`: newly staged sources and actual compiler/verifier outputs
- `root/workspace/matches/`: the one new real match, original replay and summary
- `negative-copies/`: copies of real outputs deliberately damaged for testing;
  originals remain preserved
- `provenance/`: source revisions, file digests, separate AGPL licenses and copied
  runtime-origin record; licenses were never inserted into source-only ZIP intake
- `service_facade.py`: exact code snapshot used for the run

Before publishing feedback, the bridge checks accepted source → build source and
binary identities, pinned compiler/verifier commands and successful exits,
input immutability before/after the game, pinned engine/map digests and version,
match input snapshots/configuration, process and extractor log hashes, replay and
summary hashes, expected teams, consistent winner evidence, complete game/match
footers and contiguous covered rounds. It then projects through the facade's
closed public result schema. Missing/invalid evidence does not become a loss.

Four negative checks passed:
1. Traversal ZIP rejected before staging or compiler execution.
2. Valid-layout but invalid Java passed intake, then the actual compiler failed;
   the public terminal state is `rejected: compile_rejected`.
3. An altered class file in a copy of the real build is rejected as binary drift;
   its public projection is infrastructure failure without counts.
4. A real-match copy with missing winner evidence is rejected; its public
   projection is infrastructure failure without counts.

## Recheck without executing another game

```sh
cd /workspace/shared/bc23-service-integration
python3 -m unittest test_bridge.py -v
```

These eight checks validate the persisted real outputs and negative copies. They
never call the engine. The driver refuses a second recorded demonstration; do not
remove the guard/report to rerun, and do not expand the game budget implicitly.
`SHA256SUMS` binds the small observer deliverables; artifact inventories are inside
the report. These hashes detect accidental or observed drift, not malicious
rewrites of both data and records by a process with shared filesystem access.

## Remaining gaps

The existing namespace/chroot is experimental, not an independently audited
host/tool/filesystem/network boundary. The public sources were selected and
already inspected, rather than arbitrary adversarial submissions. Hidden-corpus
execution remains blocked. There is no durable queue/store, authenticated owner,
service transport, crash recovery, real provider/controller integration or
sanitized replay publication. Core replay extraction has its documented scope
and is not a complete FlatBuffers schema verifier. The service remains
process-local, and hashes do not enforce isolation. The complete autonomous
learning/evaluation loop has not been demonstrated.
