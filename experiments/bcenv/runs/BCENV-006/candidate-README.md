# Battlecode 2023 cooperative development workspace

Read KICKOFF.txt and the public rules/API documentation in docs/. Create your own Java source in src/, Java tests in tests/, and records in work/. No initial bot or tests are supplied. Supplied tooling and documents are fixed inputs; do not modify them. The native environment has cooperative workspace restrictions, not hard filesystem isolation.

## Local checks

Run from this workspace, choosing your own package and test main class. Output directories must be fresh and remain inside the workspace. Replace uppercase placeholders with your chosen names.

```sh
./candidate-check build --source src --package PACKAGE --output work/build-001
./candidate-check test --build work/build-001 --tests tests --main-class TEST_MAIN --output work/test-001
```

Inspect returned status and exit code. Java tests execute actual candidate classes with assertions enabled on an uninstrumented JVM; passing does not prove game-engine equivalence, coverage, or match performance. The build includes the official verifier. Local checks do not launch scrimmages.

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

45 minutes from launch; at most eight source submissions, eight games each, 64 games total; 24 notes and 150 replay queries. Rejected builds consume a submission without games. Local checks use the same wall-time budget. Select your final submitted version yourself, leave its exact source in src/, and write work/FINAL.md as specified in KICKOFF.txt. Do not spawn agents or obtain outside advice.
