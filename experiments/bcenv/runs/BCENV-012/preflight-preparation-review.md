# Independent BCENV-012 preflight preparation review

2026-10-22. **PASS for static preparation; no execution authorized by this review.** No gate checker, launcher/probe, driver, compiler, helper, replay extraction or game was run. Python driver/checker syntax was parsed as text only. Calibration termination and explicit parent GO remain prerequisites.

## Bound inputs

- Preparation `integration012/preparation.json`: `42291e089116ab37196c133c6deef12461ba3dc17ba60434ecbe4e5f8f0a4ad9` (supersedes the earlier66451615 snapshot before counter assertions).
- Driver `integration012/run-check.py`: `1d3ce5683da76f90cd8a537da6890b545ef860ab74dd3da63bc14311b98adfef`.
- Preflight/live configuration bytes are identical, SHA256 `7fafdf738f2a1dca89fff7ea60acdcc1ce960b7a69404f5a27f2a4774d7be84a`.
- All15 preparation-listed file hashes verified, including the exact tutorial fixture inventory by hash only. No tutorial/opponent implementation analysis was performed. Independent raw-vector reader files remain byte-identical to011.
- Local clean code HEAD is `877aa5d0f38ef8e56b8d6259d0c654d5929d284b`; reviewed source bytes remain unchanged. Saved release evidence reports exact-head CI39823862662 success and unchanged1bbk runtime. This review inspected that saved evidence, not a separate remote CI poll.
- The protocol change is exactly the added three-line PR24 implementation link paragraph: removing it reproduces previously reviewed SHA79537285… . Current protocol SHA256 is `c51b3d4c1cc73e5be8851208c99915fdd3f5c9561dd9f733fd15eb9469d6d0c1`.

Exact per-file bindings and static results: `reviewer/PREPARATION-012-MECHANICAL.json`.

## Gates and actual intended workload

The wrappers call the read-only checker before initialization, use the same fixed host Python/shared launcher, and live launch requires the actual preflight launch identity. The checker binds exact code/root cleanliness, profile/runtime, protocol/input/preparation/driver hashes, independently reviewed inputs, CI attestations and explicit calibration-resource-hold clearance. It requires fresh service/launch/driver state. The exact tutorial file inventory and initial candidate hashes are checked. These are trusted operator gates, not a hostile-filesystem authorization boundary.

At review, no GO, service, mailbox, launch, driver-started, live service or READY012 existed. Config differs from011 only in the reviewed continuity profile/capacity fields; worker command/runtime, both schedules and120/300 child limits are unchanged. Full service capacity is21600 seconds/24 versions/208 attempts, **not** preflight authorization to use that capacity.

The driver creates an exclusive start marker, submits exactly one source-bound note and one unchanged tutorial source, never locks finalists, and never retries an uncertain request. It stops on rejection/incomplete results. At most540 result polls are made; exhausting that smaller observation budget fails rather than grants another attempt or promises six-hour polling.

Replay loops structurally permit at most64 requests (8 games×2 windows×2 modes×2 pages), below the authorized128. Including two status requests, worst-case driver reads are606 and mailbox requests608, safely within2000/2200. It checks all eight replay hashes against009, both-slot own diagnostic rows/counts against independent raw vectors, old-runtime action projection equality, positive activity from both teams, source/terminal-round coverage, and replay/result byte immutability. Two-page windows are bounded samples, not proof every selected window is fully enumerated.

## Corrected finding

Initial driver only checked presence of usage metadata. Before this fixed review, coordinator added exact initial and final counter assertions **without new requests/games**. Initial usage must show read/dispatch/mailbox1 and notes/versions/replays0. Final reads must equal result polls+replays+2, mailbox/dispatch must equal reads+2, notes/versions1 and replay debits exactly the query count. Service resolved profile must equal actual launcher identity both initially and finally. Final attempted-game accounting requires8 training/0 validation and exactly one submission directory.

## Remaining gates

The corrected preparation must be published with successful exact protocol CI before GO. Calibration must be terminal and the resource hold explicitly cleared. A successful future driver still does not attest service shutdown: explicit terminal process-stop evidence, retained receipts/inventory, independent postflight review and clean inputs are required afterward. Live clock initialization additionally requires parent conditional readiness and independent actual empty-state/parity review. No old frozen review or candidate input was modified here.
