# BCENV-009 public tutorial preflight result review

2026-10-22. **Independent recorded-evidence gate passed.** No new game, query,
source submission, service start or candidate execution was performed by reviewer.
This review covers official tutorial engineering fixtures only, not candidate
strategy/performance or evaluator material. Parent readiness approval and a fresh
live empty-state/parity check are still required before candidate launch.

## Independently recomputed

- Four complete results, eight games each: exactly 32 existing games. Rehashed
  all 32 replay files and matched their public-result SHA256 identities.
- Both eight-game training replay hash arrays match the previous official
  tutorial integration fixture in order: 16 exact replay matches. Both training
  IDs are distinct; all four jobs retain the same source hash.
- All 296 audit events have continuous sequence/previous-hash bindings and valid
  recomputed event hashes. Counts: two submissions, 32 game attempts, one lock,
  two validation completions, one selection and 110 successful replay receipts.
- Recomputed feedback hashes on all 110 replay responses; validation/training
  response IDs match their reference IDs. Every page reports complete source
  stream, match footer, source round coverage and requested positive rounds.
  Existing returned movement/action records establish both-team activity for
  all 32 games. No additional replay extraction was requested.
- The 32 per-game replay-check records distinguish early/terminal windows,
  continuation offsets and selected-window enumeration from source coverage.
  Two-page/window cap and 110 actual requests remain below the 150 quota.
- Five negative responses have exact reasons: validation_incomplete,
  training_closed, selection_complete, and finalists_locked twice. No replacement
  submission or validation batch is represented in the audit.
- Terminal persisted phase is selected, with 16 training and 16 validation
  attempts. Recorded selection decision precedes the common deadline.
- Preflight launch probe passed. Current service/runtime Python hashes still
  match its identity. Same host Python 3.12, repository cwd, fixed offline 7yh
  adapter command, 120-second per-child cap and 2700-second service budget are
  recorded. `development/service009-config.json` is byte-identical to the tested
  integration configuration; this does not itself prove a future launch.
- Freeze records driver exit 0 and explicit service interruption exit 130,
  service stopped and no native candidate instantiated. Process-list spotcheck
  found no remaining integration launcher/driver. Exit 130 is not described as
  a graceful shutdown marker.

The mechanical audit reports no failures and 182 deadline process receipts; its
stated count includes repeated build snapshots, not 182 unique launches. These
are cooperative application observations, not complete native-access tracing,
hard-real-time kernel timestamps, or proof of every rejected request's logging.
The real single-lock run does not replace synthetic concurrency testing.

## Fixed reviewed record hashes

- config.json: `52464602026d5660085fd4159e49f45531dc770960756db1e1c5ee782a9269bc`
- launch/launch.json: `08b4454bac40bd274b066a73be55d536b3640cac5ff88d9ebc20e57f6dd456f6`
- completed-summary.json: `e205a053f80d5eae7a900d82da30d88ee11665d11dc966150cc0556165635d6c`
- replay-checks.json: `ae5e379a32643398c4baa2867f8040b89cbdcd451d124dccd04366e367b32cd7`
- mechanical-audit.json: `f422537a32be8f1d76e9695de686f4465122431f61f1bab9537d101d685e152b`
- freeze.json: `952dbb2c7614650e1e7e95094a56c64f01559e4dbdcc66ebcb8148634a36158c`

All paths above are under `integration009/`. No fixed earlier review was edited.
