# 012 failed preflight: independent transport diagnosis

**Finding: confirmed infrastructure compatibility failure; preflight did not pass.** Review is read-only and uses the retained public tutorial artifacts, not private evaluation. No matches, replay retries, service starts, tests, builds, or implementation edits were performed for this diagnosis. The original failed run must remain immutable; any authorized replacement is a distinct prospective run, not continuation or repaired evidence.

## Observed sequence and accounting

The published client (`services/local_trial_client.py:54–58`, byte-identical to frozen `competitor-012/tools/service.py`) writes `requests/<32 lowercase hex>.tmp`, closes it, then atomically renames to `.json`. The continuity server at published commit `877aa5d0f38ef8e56b8d6259d0c654d5929d284b` snapshots every directory entry (`services/local_trial.py:641`), treats non-`.json` names as invalid, debits them and calls `unlink` (`647–655`). This incorrectly treats an uncommitted protocol staging file as an invalid request.

The retained server traceback terminates at line652 with `FileNotFoundError` unlinking `4f36af32c589413d8f3440104d984afa.tmp`. The client subsequently times out waiting for the response, not performing its rename. The corresponding committed `.json` remains present, the `.tmp` is absent, and no response exists. This supports the concrete ordering: directory snapshot saw staging; client successfully published; server attempted to remove the now-renamed staging path and crashed. The opposite ordering is also unsafe: server could remove staging before the client's rename.

Independent structured inspection found:
- `result.json`: complete, eight games, all eight completed.
- Audit: eight `game_attempt`, one `complete`, one submit, one experiment note, one validation-status, 24 result reads, 19 replay records, then `trial_closed`.
- `stopped.json`: 47 processed transport attempts versus 46 dispatch attempts; 44 read debits, 19 replay debits, one note and one training version. The arithmetic is exact: 1 status +24 results +19 replays =44 reads, +note+submit =46 dispatches. The one extra transport debit matches the staging-path branch.
- Pending request is the twentieth replay request, game index4, rounds1–5, mode `own_diagnostics`; there is no dispatch receipt for it. The observed failure does not implicate diagnostic extraction/parsing or the engine timeout.
- Last storage checkpoint is `mailbox_invalid_name`, status `ok`, logical/high-water bytes4,844,575 versus limit1,073,741,824. This was not a storage-limit or storage-scan failure; quotas were also far below exhaustion.

Both original tool sessions were reported terminal exit1 by the coordinator. The stopped marker and final audit corroborate cleanup entered the server's `finally`; this is not proof of global process absence, and no namespace-local PID inspection was used to claim it.

## Narrow compatible repair and required regressions

Recognize only the published client's exact canonical `<32 lowercase hex>.tmp` staging name before invalid-name accounting. Do not dispatch, debit, or delete legitimate uncommitted staging. Keep staging entries in the 32-entry queue bound and the full service-owned storage scope. Validate staging without following links; only a precisely identified disappearance during atomic publication may be ignored. Other errors must not be blanket-suppressed. Retain published `.json` debits and seen-ID bookkeeping before reading, malformed/duplicate/oversize denial, absolute deadline, and storage guards.

`unlink(missing_ok=True)` alone is **not** a fix: it preserves incorrect debits and can still delete a live producer's staging file. For committed requests that disappear, preserve consumed-ID bookkeeping; any narrowly tolerated missing cleanup must never cause redispatch or imply successful execution. Invalid-file failures must remain bounded.

Require deterministic producer/consumer tests using the actual client, not only fixtures that write final `.json` directly: hold staging visible before rename; force rename between server snapshot and inspection; verify zero staging debit/deletion, then exactly one committed dispatch/response. Also test missing committed-file read/cleanup and duplicate IDs without double execution, malformed published files consuming budget, and queue overflow including staging. Preserve storage/deadline tests and prohibit broad `OSError` suppression.

**Residual limitation:** the separately documented storage scanner (`storage_guard.py`, `_scan_directory`) can fail closed when a file disappears during `DirEntry.stat`. Recognizing staging fixes this observed transport race, not every concurrent filesystem liveness issue. Do not silently exclude staging bytes or weaken scan-failure semantics under this repair. No six-hour reliability claim follows from a passing targeted test or replacement preflight.

## Evidence hashes

- `integration012/service-stderr.log`: `cd226f8b43f02413619b1fd691416586c4349316dfb53d1e661e56cf8f895d54`
- `integration012/driver-stderr.log`: `4c3ff83c18e0d0fed79b027e70ffe21067943813ac1d002905cd06799d6f6e20`
- `integration012/mailbox/stopped.json`: `e47f6c853889700d454606b9d3f7f7f225163d5f8f0e51bde8cd924f9d7c3dfd`
- `integration012/result.json`: `1b9f53d221fc3adc96763e71eaa9ba51a5f2d3b3586da1e697bcd63db4263970`
- `integration012/service/audit.jsonl`: `77de88fdaa12b2437a7595836e52afdf580b0615fbee436fbd19f889f832a4fb`
- `integration012/service/storage-checkpoints.jsonl`: `94ce436190dcc8ec1f6ae8f623984285b14eaf3f22e4b7c17b8d730de60c0c74`
- `competitor-012/tools/service.py`: `32f25520351032ec313a50a5e87a5fb7b706075accac1f95732008b363b9e38e`
