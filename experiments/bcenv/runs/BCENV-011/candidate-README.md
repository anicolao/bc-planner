# Battlecode 2023 cooperative development workspace

Read KICKOFF.txt and the public rules/API documentation in docs/. Create your own Java source in src/, Java tests in tests/, and records in work/. No initial bot or tests are supplied. Supplied tooling and documents are fixed inputs; do not modify them. The native environment has cooperative workspace restrictions, not hard filesystem isolation.

## Local checks

Run from this workspace, choosing your own package and test main class. Output directories must be fresh and remain inside the workspace. Replace uppercase placeholders with your chosen names.

```sh
./candidate-check build --source src --package PACKAGE --output work/build-001
./candidate-check test --build work/build-001 --tests tests --main-class TEST_MAIN --output work/test-001
```

Inspect returned status and exit code. The build includes the official verifier. Local checks do not launch scrimmages. Java tests execute actual candidate classes with assertions enabled on an uninstrumented JVM. A zero-exit test with unchanged snapshots reports `execution_succeeded`, not correctness: receipts always state `assertion_coverage: "unknown"` and `correctness: "not_established"`. `assertions_enabled: true` records configuration, not that an assertion or even the JVM ran. Empty mains, printed success messages, and successful assertions cannot be distinguished as correctness evidence from exit status alone. Successful execution does not prove game-engine equivalence, coverage, or match performance. Failed assertions, compilation failure, timeout, output overflow, and integrity failures still return nonzero.

For each correctness claim, keep a concise candidate-authored inventory:

| Claim / scenario ID | Expected condition | Executable check | Observed result | Evidence and limitation |
| --- | --- | --- | --- | --- |

Identify the actual assertion or explicit failure condition and its test source location; cite the receipt, exact tested source/binary hashes and relevant logs. Distinguish printed observations from executable checks. Mark claims with no executed check **untested**; label manually inspected outputs as manual observations. Preserve failed and incomplete checks as well as successful executions. Do not infer per-scenario success from the overall process exit code. This inventory is review evidence, not machine-verified coverage or a trusted correctness oracle. No bot scenarios or strategic tests are supplied.

## Scrimmage interface

The service mailbox will be provided at mailbox/. Use only this client, not direct mailbox manipulation. The note text file is your own concise prospective plan/prediction; notes bind to exact source bytes. Preserve returned receipts and use the note ID and hash for the same source submission.

```sh
python3 tools/service.py --mailbox mailbox note --source src --package PACKAGE --text-file work/prediction.txt
python3 tools/service.py --mailbox mailbox submit --source src --package PACKAGE --note-id NOTE_ID --note-sha256 NOTE_SHA256
python3 tools/service.py --mailbox mailbox result --submission SUBMISSION_ID
python3 tools/service.py --mailbox mailbox replay --submission SUBMISSION_ID --game 0 --start 1 --end 5 --offset 0 --limit 64
```

A later note may link returned replay-reference IDs using repeated `--replay-reference REFERENCE_ID`. See tool `--help` and docs/replay-semantics.md. No automatic resubmission after uncertain outcomes. Stop on infrastructure_failure/run_halted or an uncertain request outcome and report the exact error.

## Fixed development schedule and budget

Each submitted version plays eight games: Beaver USQualifiers and Musketeers MPWorking, each on Quiet and BowAndArrow, in both A/B slots. These are public development opponents. No opponent source is available through the interface. The schedule is fixed; it is not a held-out performance estimate.

The service budget is at most45minutes from service initialization. Immediately run `python3 tools/service.py --mailbox mailbox validation-status` to learn the remaining time and deadline; startup delay is not extra time. Training permits at most8source submissions ×8games =64games. Rejected builds consume a submission without games. Local checks share this wall budget. Across both phases:24notes and150replay queries.

The trusted match-run allowance is up to300seconds for the engine and its initial replay summary separately, in both training and validation. Every step is also clipped by the same remaining45-minute global deadline; these are not extra time allowances. Build, package and later replay-query requests retain the existing timeout=120 parameter for their child subprocesses, also clipped by the same absolute deadline; this is not a total-request elapsed-time guarantee. A longer game can leave fewer completed games within the global budget; the maximum game count is not a completion promise. Stop on timeout or infrastructure failure as above.

Then lock exactly2distinct completed, verified training IDs and a provisional choice in one request. Both immutable finalists receive the same8new public validation conditions =16additional games, at most80total. Training closes at lock: no edits, new submissions, re-nomination or second validation batch. Wait for both validations to complete, use `select-finalist` to choose one original locked training ID, restore its exact source without editing, and stop. Full commands and evidence limits: docs/public-finalist-validation.md. Preserve training and validation scores separately; neither is an independent held-out estimate. No operator chooses or repairs your bot. Do not spawn agents or obtain outside advice.

## Optional own-team replay diagnostics

The existing replay action mode remains the default. Optional own-team indicator
strings and recorded bytecode usage are available through the same replay client:

```sh
python3 tools/service.py --mailbox mailbox replay --submission SUBMISSION_ID --game 0 --start 1 --end 32 --offset 0 --limit 64 --mode own_diagnostics
```

This shares the existing replay-query quota and wall deadline; it adds no games or
time. See docs/own-team-diagnostics.md for record, pagination and evidence limits.
It provides recorded observations, not automatic exception capture or proof of
correctness. You may choose whether to use this mode.
