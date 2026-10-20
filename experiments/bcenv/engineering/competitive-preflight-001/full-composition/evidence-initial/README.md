# Full offline controller composition smoke

Date: 20 October 2026 UTC. Result: **all 5 independent composition tests passed**
under the repository-pinned Python 3.13.15 / SQLite 3.51.2 toolchain.

This reproduction combines the published offline Responses transport, existing
fixed-tool controller, durable SQLite ledger, and a stable snapshot of the new
controller-to-ledger bridge. It was created outside author worktrees and changed
none of their files.

## Outcome

1. **Full continuity:** eight fixture model turns and seven application calls
   exercised all six functions: write, read, exec/export, submit, result and replay.
   A second write changed the workspace after export; the real SQLite ledger still
   retained the exact original captured source. A trusted fixture completed the
   job, its bounded result survived database reopening, and replay stayed withheld.
   The initial context, fixed registry, opaque reasoning state, assistant phase,
   function IDs and result history remained consistent across the eight turns.
2. **Failed export:** malformed ZIP bytes produced the fixed adapter error, minted
   no usable handle, and created no database job. A guessed handle was rejected.
   All three model-fixture attempts retained their full reservations.
3. **Owner/run denials:** cross-owner and cross-run artifact, result and replay
   requests were uniformly refused. A direct cross-owner ledger read returned
   `not_found`. The existing one-job count did not change.
4. **Unknown model outcome:** a synthetic timeout ended the first controller run
   without automatic retry or tool execution. An explicit test-operator retry used
   the identical request. The first attempt remained `unknown`; the second was
   `reported`. Both full input/output reservations remained consumed.
5. **Launch gate:** supplying all composed adapters still raised
   `real_launch_unsupported`, with no job created.

The happy-path fixture reserved 128,000 input / 64,000 output tokens over eight
attempts, compared with fabricated numeric usage of 800 / 128. The unknown-outcome
case retained 32,000 / 16,000 across its two attempts. These are local accounting
assertions, not real token measurements, charges, or a dollar-spending guarantee.

## Exact inputs and retained evidence

- `snapshot/services/`: the five exact modules imported by the reproduction
- `source-manifest.json`: SHA-256 and byte length of every imported source, plus
  origin commit/status; the script verifies each before importing
- `smoke.py`: executable unittest reproduction with in-memory source/model fixtures
- `smoke.nix`: pinned Nix derivation for the reproduction
- `run.sh`: runs the derivation and copies its result from the configured alternate
  physical Nix store into this directory; cached builds still print `test.log`
- `test.log`: retained successful five-test output
- `results.json`: machine-readable assertions, scope limits, versions and hashes
- `flake.lock`: retained toolchain lock from the published transport commit
- `controller-ledger-contract.md`: author's contract snapshot for interface context

Published transport/controller/scrimmage origin:
`be041d3d18ecd9fa474cbfb076c86c336d5b6ff3`.

Published ledger origin:
`df7a20d63d04faae829b97e786f4cb4f985b0071`.

The bridge was copied after its author confirmed a stable uncommitted checkpoint,
with SHA-256 `738c263437acb3427b8543f4481622c9966a7ce1ee42897fbc899c7a2badc2ff`.
This result applies to that exact snapshot. Later revisions need a new snapshot
and rerun; this report does not silently claim their coverage.

The controller and scrimmage modules in both origin branches had identical hashes.
Nixpkgs is locked to `21a67dc470149f337cecafbe965d8d252a390518`.

## Reproduce in the current approved workspace

Run `./run.sh` from this directory. It uses the existing configured runner at
`/workspace/scratch/1523a3f802eb/nix-canonical-root/nix-root` and the immutable
published transport revision for its flake inputs. No additional package or
unapproved installer is introduced. The retained source snapshot means adapter
edits in author worktrees do not alter this test's inputs.

## Scope limits

All model messages, counts, byte exports and completion evidence are synthetic.
The `exec` fixture only packages in-memory bytes; it does not compile or execute a
candidate. The completed one-game/one-win summary is deliberately fabricated
trusted evidence to test projection, not a played match or bot-strength result.

SQLite is real and temporary. Reopening its file is tested, then its temporary
files are removed. It does not make process-local model accounting or artifact
visibility durable. Owner/run strings are host-supplied fixture scopes, not proof
of service authentication. Socket creation and subprocess launch are patched to
raise during the tests; this is a test guard, not a candidate security boundary.

No provider call, game, credentials, account, security setting, network service,
sandbox implementation or live-launch path was created or used. Passing these
probes establishes fixture-level interface composition only, not isolation,
provider entitlement, accurate tokenization, deployment readiness or competitive
strength. The real launch gate remains closed.
