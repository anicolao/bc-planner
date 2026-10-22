# Public finalist validation

This phase compares two immutable training submissions on the same additional public conditions. It is public selection evidence, not an independent held-out assessment, correctness certificate, or hard isolation. You choose your own two finalists and final bot; no strategy advice is supplied.

Query remaining time immediately:

```sh
python3 tools/service.py --mailbox mailbox validation-status
```

The clock starts at service initialization. `remaining_seconds` is a snapshot; the clock continues. All coding, local checks, training, validation and selection share the maximum21600 seconds. Leave time for validation and selection; no automatic extension applies. The phase provides at most24 training versions ×8games (192), then exactly2locked finalists ×8validation games (16), total at most208. The same existing public opponents play on two additional public maps in both slots. The schedule is fixed prospectively; you never supply trusted build, map or opponent paths.

Save each submitted source version. Wait for pending training work to finish. Lock exactly two distinct completed, verified original training IDs and your provisional choice, before seeing validation feedback:

```sh
python3 tools/service.py --mailbox mailbox lock-finalists --submission FIRST_TRAINING_ID --submission SECOND_TRAINING_ID --provisional-choice FIRST_TRAINING_ID
```

One atomic request closes training. Do not edit candidate source, submit new code, re-nominate, or request another validation batch. The response maps each original ID to a validation ID in `validation_ids`. Use those validation IDs for validation results and bounded replay pages:

```sh
python3 tools/service.py --mailbox mailbox validation-status
python3 tools/service.py --mailbox mailbox result --submission VALIDATION_ID
python3 tools/service.py --mailbox mailbox replay --submission VALIDATION_ID --game 0 --start 1 --end 5 --offset 0 --limit 64
```

Training results remain attached to original IDs. Preserve both finalists' evidence, negative results, replay coverage and receipts. The72-note/450-replay limits span both phases. Once BOTH validations complete, choose one ORIGINAL locked training ID:

```sh
python3 tools/service.py --mailbox mailbox select-finalist --submission CHOSEN_TRAINING_ID
```

Restore that exact saved source into src/ without editing, write work/FINAL.md and stop all work. Report provisional and final choices, exact hashes, separate training/validation results, actual test evidence and known failures. Choosing not to switch is valid. Validation does not erase failed tests or establish general correctness, and its selected score is not an independent performance estimate.

Stop immediately on infrastructure_failure/run_halted, deadline expiration, or uncertain request outcome. Never retry uncertain lock/submission/selection operations or bypass the interface. Failed or unfinished validation remains incomplete/unscored. No new source or game starts after expiration. Cleanup time is not added candidate time. No restart recovery, replacement cell, extra version or second batch is available.

Same-user workspace restrictions are cooperative, not a hostile filesystem sandbox. Do not inspect service/evaluator infrastructure, sibling files or any opponent source. The provided interface and rules remain the only route to scrimmages.
