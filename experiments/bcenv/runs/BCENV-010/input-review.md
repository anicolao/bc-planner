# BCENV-010 fixed-input and preflight preparation review

2026-10-22, before preflight/service initialization. **PASS for the fixed inputs and reviewed preparation; execution remains subject to prospective protocol CI, seal and parent gate.** No games, candidate source, prior candidate generated material, evaluator panel or outcomes were accessed. Earlier reviews remain unchanged.

## Fixed identities

- Export manifest `competitor010-export-manifest.json`: `671d78f3ab4869ab5a9d9865c0f1ea1cca2ea1bda75393e69d698cca1962d9ae`.
- Both `integration010/config.json` and `development/service010-config.json`: `9936ba1e9f832424a13acb3ac517c501476ccd4baaabbe8079c519958481ed5d` (exact byte equality).
- Final preparation manifest: `f2bb46c28060375ee7a88f5045d59b4f07a30eb8c81acae147fb1c76faa2573d`.
- Final gate checker: `d4a29dd5783e724e1b894b68b8215eb687d7496b2fcb5960b3ff470fddb1b045`.
- Driver: `daabd2b6b2c03a637382a22ef5ae3bb92bd3375c8a42dc302fc1fc6b9b9d2811`.
- Reviewed corrected protocol: `8782fc86ecabae7b4a4ea672ff14cd43599e90071575e1ef3965237c65c0b8c2`.
- Exact service code `66ff4650fd6481cf3a69925098e48e6abc865e53`; clean repository observed. Exact CI runtime `/nix/store/1bbk58382aq40pplbyy2fir27qnx3jxj-bcenv-2023-0.1.0`, covered by separate immutable release review.
- Prospective private commitment checked as a literal only: 9915 ASCII bytes, SHA-256 `31def260435a8be76cd49ffc72793eb7e96e0e87008e134d23f0ae780e864628`. Private contents not read or independently assessed.

## Export and instructions

Independently recomputed all 57 file hashes, rejected extra files/symlinks by inventory comparison, and confirmed empty src/tests/work and absent mailbox. Against the earlier initial-static-input manifest, 50 files are unchanged; six existing files change only for workspace rebinding/client/new generic documentation, and one diagnostic document is added. No earlier bot/test/result/review material is present. No prior generated candidate tree was read for this review.

Inspected kickoff, README, diagnostic semantics and export method. No strategic hints or required instrumentation are supplied. Diagnostics are optional; final recorded strings, null/empty/missing distinctions, untrusted text, ownership filtering and non-CPU/non-correctness limitations are accurate. Kickoff preserves the service-start deadline, immediate remaining-time query, 8 versions/64 training games, exactly 2 immutable completed finalists, 16 validation games, 80 total, 24 notes and 150 replay queries. No post-lock edits/submissions/re-nomination, retries or operator fallback are authorized. Cooperative access limits are explicitly not hard confinement.

Verified helper source/wrapper/launcher/engine/JDK hashes and client equality with the reviewed repository client. Local build/test helper code remains the earlier fixed helper, not a silent diagnostics rewrite; the service alone uses the new exact runtime. Successful local execution is not represented as assertion coverage or correctness.

## Config, one-shot driver and gate

Live and preflight configs are byte-identical. Compared with the old public preflight config, only the runtime command changes; schedules, order, public opponent paths, timeout and deadline/budgets remain unchanged. Both use the same host-Python shared launcher, and live launcher requires saved preflight launch parity.

The max_submissions=1 proposal was rejected statically because the existing validator requires 8. Neither service nor game ran with that proposal. The corrected configuration has capacity for 8 versions; **capacity is not authority** for preflight. The exclusive one-shot driver creates a non-overwritable start marker and makes exactly one official tutorial note/submission, no lock/select request and no retry. It requires eight attempted training games, zero validation games and one submission directory at completion. Polling is observation, not resubmission.

The driver performs at most 8 games × 2 windows × 2 modes × 2 pages = 64 service replay requests, below the prospective 128 maximum. It preserves each request/response, validates own raw-vector rows/counts, both slots, replay receipts, source/terminal coverage and legacy action equality. Existing tutorial source/replay parity must match public009 evidence. Two-page caps do not prove full selected-window enumeration; retained continuation responses preserve that limitation. New phase-validation matches are not run; the unchanged public009 32-game phase proof is explicitly reused.

Gate checker validates the parent authorization record, code/runtime/seal/CI flags, bound file hashes and exact script/config paths, source-empty export, shared config equality and one-shot state before launch. On review request, it was strengthened to reject added tutorial files and symlinks via the exact six-file source inventory before execution, rather than relying only on postgame source mismatch detection. All final preparation hashes and script syntax rechecked successfully. No unresolved blocking issue found.

The gate is an operator-controlled cooperative guard, not cryptographic proof of the parent's decision or independent CI verification. Parent must populate it only after exact corrected protocol CI and seal/input gates. Preflight success needs an independent result/receipt audit and parent conditional readiness; only then may live initialization start the clock, followed by independent actual live parity/empty-state review before candidate spawn. This review does not authorize those later steps.
