# Competitive environment preflight 001

Engineering evidence, 2026-10-19–20 UTC. This is **not** a fresh autonomous bot
trial, sealed benchmark, strength estimate or accepted deployment. No candidate
model was invoked and no holdout panel was selected. Bot strategies were not edited.

## Results and scope

- [Public source qualification](public-opponents/README.md): six licensed pinned
  packages compiled/verified; ten of eleven public smoke attempts completed with
  activity. One fixed-deadline timeout is preserved. These tutorial-opponent games
  qualify integration behavior, not competitive strength.
- [Service bridge](service-bridge/README.md): one additional game after fresh
  source-only intake and build, four negative cases, eight offline verification
  tests. The real public result is 156 bytes. Original raw artifacts are retained
  separately; the compact repository bundle intentionally omits their payloads.
- [Existing-game feedback](replay-feedback/README.md): rounds 35–40 project into
  455 gameplay records in 104,406 bytes, or bounded prefixes with distinct source,
  record and byte truncation markers. No additional match ran. Scripts and
  sanitized JSON examples are included; raw parser evidence remains separate.
- [Actual namespace adapter](namespace-probe/README.md): 21 independently passing
  bounded tests using scripted controller replies. Includes executable adapter,
  trusted-init/parent-death helpers, fixture materialization instructions and tests.
  The review preserves a confirmed intermediate teardown escape and its regression.
  Aggregate resource and full deployment gates remain closed.

The combined prospective budget was eleven smoke attempts plus one bridge game;
all twelve attempts are accounted for. No retries or further matches are authorized
by these reproduction scripts. Existing replay queries and offline validations
create no game. A future game run needs a separate prospective budget/protocol.

## Reproducibility limits

The public-opponent bundle has a portable, no-execution metadata verifier.
Service-bridge tests refer to the original raw artifact tree, which is not in this
repository; copied tests are preserved exact evidence, not a self-contained CI
fixture. Their source hashes and recorded outcomes can be inspected here. Full
rehashing requires the retained original artifacts. Tool fingerprints cover
selected runtime files rather than complete supply-chain or execution attestation.
The independent [bridge review](service-bridge/INDEPENDENT-REVIEW.md) also records
that the final runtime drift comparison occurred after response publication,
failed-compile evidence is less comprehensively sealed, and error/budget handling
is demonstration wiring. These are future integration requirements, not properties
established by the eight passing offline checks.

This public bundle includes source provenance, hashes, generated operational
metadata, observer scripts and separate license notices. It omits Java source,
class files, engine/maps/replay binaries and the Nix closure. We have not established
an upstream repository-wide engine/map redistribution grant. No actual benchmark
selection, secret schedule, credential or private opponent source is included.

Hash consistency does not resist a malicious writer who can change both artifacts
and records. The builder workspace remains shared. Claims about actual competitor
access must use the separately tested full capability boundary, not these hashes.

## Repository checks

`npm test` now checks the committed compact checksum inventories, matches the five
namespace sources to the independent review snapshot, and checks recorded replay
example byte bounds/scope. These offline checks execute no bot, sandbox, parser
or network request. They detect accidental drift, not coordinated record rewrites.

## Reviewed component composition

[Composition evidence](composition/README.md) records a later 190-test build
combining the public runtime with service, ledger and offline Responses modules.
It includes exact source hashes and package-exclusion inspection, with no new game
or model invocation. It is a disposable uncommitted integration, not a release.

## Source capture and full offline protocol

[Source-export fixtures](source-export/README.md) retain actual namespaced source
collection through immutable artifacts into a queued SQLite job: 28 local and
38 independent tests (28 repeated plus 10 added), zero games/models. Production
aggregate quotas, workspace lifecycle and authentication remain unproved.

[Full offline composition](full-composition/README.md) retains five executable
model-protocol/controller/artifact/SQLite probes. Its model/count/game-result
inputs are deliberately fabricated. Its inert workspace is distinct from the
actual namespace collector. These are two narrower demonstrations, not a complete
live learning loop. The component build later passed 211 tests; earlier evidence
is preserved alongside it.
