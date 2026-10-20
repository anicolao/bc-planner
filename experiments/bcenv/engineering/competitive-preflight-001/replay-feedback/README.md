# Existing public-game replay feedback demonstration

This evidence demonstrates the reviewed bounded feedback projector on an already
completed public Battlecode 2023 game under official public rules version 3.0.13.
**Zero new games ran.** No bot was edited, heldout gate opened, listener started,
service deployed or model-learning loop executed.

The fixed inclusive window was rounds **35–40**, selected before inspecting its
rows. The pinned existing Java ReplayQuery producer parsed the same persisted
replay twice, once with a 10,000-record cap and once with a 32-record cap. Both
processes exited 0; both source hashes matched the original observer evidence.
The complete window contains **455 records**, and every requested positive round
is present. The parser validated the complete source's extracted core arrays;
it did not validate every FlatBuffers schema field.

## Shareable outputs

| File | Rows | Encoded bytes | Truncation |
| --- | ---: | ---: | --- |
| `feedback.json` | 64 | 15,639 | Projection record cap |
| `feedback-window-complete.json` | 455 | 104,406 | None within the selected window |
| `feedback-source-capped.json` | 32 | 7,988 | Source query record cap |
| `feedback-byte-capped.json` | 13 | 4,026 | Projection record and 4,096-byte caps |

All four retain exact raw source prefixes, signed values and own/opponent slot
attribution. Source matching counts continue to report all 455 window records.
Coverage distinguishes source completeness, requested-round coverage, source
prefix truncation and additional projection truncation. The source-capped
response has no additional projection truncation. Missing rows must not be
interpreted as absent gameplay.

`verification.json` records the compact checks, per-kind counts, byte sizes,
output hashes, negative controls and limitations. `SHA256SUMS` binds this README,
the verification record and the four feedback JSON files.

`feedback-evidence.zip` contains only those seven text files. It includes no
map, engine, bot, compiled class, raw replay, raw query, log or private observer
record. The ZIP is an evidence delivery bundle, not a runnable environment.

## Checks performed

- All eight original bridge offline checks passed without invoking a new game.
- Original job files, match files, bridge files and recorded runtime fingerprints
  were identical before and after replay parsing and projection.
- Both ReplayQuery results identify the same original compressed replay hash.
- Host-selected `expected_spec_version` was explicitly `3.0.13`; using `2.0.3`
  against these records was rejected.
- The demonstration submission/job handles were randomly generated independently
  of hidden source content. The own-team mapping came from the existing game
  evidence. They are demonstration identifiers, not authenticated credentials.
- Every returned row and every coverage field matched the permitted source data.
  Complete-window kind counts were independently recounted. The 32-row source
  result matched the exact prefix of the 455-row result.
- Output byte/row caps and final canonical JSON encoding were checked.
- Source names, packages, map names, runtime paths, replay/engine/map hashes,
  raw provenance fields and URLs were absent from each feedback payload.
- Nested private-metadata injection left the projected response unchanged.
- Incomplete source evidence and a corrupt row beyond the local output cap were
  rejected without partial feedback.

Both parser invocations emitted the same JVM stack-location warning and exited
successfully with complete core evidence. Raw stderr and its hashes are retained
privately. This is not a claim of a warning-free JVM run.

The projector source is bound to bcenv commit
`04c815954154a9be691bb531245f74e35cbd6edf`. This evidence uses the already preserved,
reviewed 3.0.13 producer from the earlier public-game bridge. It does not claim
that this commit's diagnostic-only Java parser was upgraded during this exercise.

## Local recheck

The original scratch directory also retains `prove_feedback.py`,
`verify_feedback.py` and a private `observer/` directory. These are deliberately
excluded from the shareable ZIP. Observer evidence contains the immutable-input
snapshots, exact parser commands, runtime/source provenance hashes, raw query
JSON and parser diagnostics. No source replay or executable binary was copied
into this feedback directory.

From the original feedback evidence directory, with the original bridge inputs
still available:

```sh
python3 -B verify_feedback.py
```

This recheck reads persisted artifacts and regenerates projected JSON in memory.
It invokes neither ReplayQuery nor the engine. Do not rerun the guarded proof
driver merely to recheck the evidence.

The two scripts contain public engineering code, fixed scratch/runtime paths and
test markers, with no credentials or engine/map/replay binary content. They can
be retained separately with the planner's engineering evidence. Their fixed path
constants must be adjusted explicitly if artifacts are relocated.

Reproducing the initial parse requires the original bridge's report, Python
bridge/facade/test code, preserved runtime root (Java, engine JAR and query
classes), original match replay/results/summary/logs, and job build/source
inventories. The eight bridge checks also require the original public source
staging referenced by that bridge. Rechecking this recorded result additionally
requires the private `observer/` query JSON, provenance and before/after snapshots,
plus the projector checkout at the recorded commit. These raw dependencies are
not distributed in the shareable ZIP; their hashes are retained locally. The
proof driver refuses to overwrite an already recorded success.

## Limits of the result

This is a real persisted-replay integration check, not a strategy evaluation or
an unbiased sample. The fixed window and prefix can omit later adverse events.
Raw movement/action/resource records do not establish intent, damage, mining
efficiency or causal conclusions. Removed identity metadata does not prevent
recognizable gameplay from fingerprinting a bot or map.

Checksums detect drift; they are not cryptographic attestations against a party
able to rewrite both data and records. The experimental namespace/chroot is not
an independently audited isolation boundary. The projection itself does not
provide authentication, ownership checks, authorization, full replay verification
or a deployed feedback route. The existing facade still withholds replay access,
and the real-heldout gate remains closed.
