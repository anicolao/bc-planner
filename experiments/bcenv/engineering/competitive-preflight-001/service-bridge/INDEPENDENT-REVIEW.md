# Independent review: public BC23 service plumbing experiment

Reviewed 2026-10-20 UTC. Scope: `bridge.py`, `service_facade.py`, `test_bridge.py`,
README, report, launchers, and persisted outputs under
`/workspace/shared/bc23-service-integration`. No files in that directory changed.

## Result

Suitable evidence of the narrowly stated **trusted, public-source plumbing
experiment**. It is not acceptance evidence for an adversarial worker, complete
runtime attestation, autonomous agent loop, hidden-opponent service, or strength
measurement. No blocking contradiction was found in the stored positive result.

I ran exactly the eight offline tests with
`PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest test_bridge -v`: **8 passed**.
Every entry in `sha256sum -c SHA256SUMS` also passed. I executed **zero games,
compiles, verifier processes or replay-parser processes**. The review only read
existing artifacts and exercised the supplied eight offline tests.

The persisted root contains one match and three jobs: two successful public
builds and the intentional compiler-rejection case. Its engine log records
USQualifiers in slot A winning at round 318 by island capture. Stored summary,
result, expected identities and hashes agree. The current original build/match
inventories equal the observer seals. Damaged copies are rejected by the supplied
tests. The compiler-error log contains the expected syntax errors; it is not
reported as a competitive loss.

## Required claim precision and remaining gaps

1. **Selected runtime files, not complete toolchain attestation.**
   `bridge.py:255–261` hashes the launcher, facade, bridge and `/opt` inventory,
   including engine/map/parser/adapter bytes. It does not rehash the copied
   `/nix/store` JDK, Python or native dependency closure. Fixed path strings in
   command records do not establish those executables' byte identity. Describe
   the demonstrated check as “selected-runtime-file and artifact drift checks.”
   Keep the original records unchanged; do not imply a retrospective full seal.

2. **Final runtime comparison occurs after the public response is recorded.**
   `bridge.py:287–292` projects and writes the positive public result;
   `bridge.py:350` performs the after-run runtime comparison only later, following
   the negative checks. The comparison passed for this recorded experiment, so
   this does not invalidate its observed result. However, avoid claiming that
   every runtime check gates feedback publication. A future integration must
   complete the applicable after-run checks before accepting a terminal score.

3. **The failed-compile evidence is less comprehensively sealed.**
   `bridge.py:307–313` and `test_bridge.py:51–58` check the failed artifact/exit
   code and no-score response, but do not independently compare that failed job's
   full inventory, compile-log digest and source/command binding to an original
   observer seal. The successful jobs/match receive stronger validation. The
   current compiler log supports the reported failure; the eight passing tests
   should not be described as equal-strength tamper coverage for every negative
   artifact or launcher log. Add this coverage prospectively without rewriting
   the original run's evidence.

4. **Failure projection and one-shot control remain demonstration wiring.**
   The two damaged-copy cases manually record infrastructure failure after
   validation exceptions (`bridge.py:340–343`). General real build/match errors
   elsewhere raise and can leave an accepted facade record without a terminal
   result. The report-exists guard is not an atomic game-budget/concurrency
   control. These are consistent with the stated process-local prototype, but
   cannot support claims of resilient service orchestration or enforced quotas
   across workers/restarts. No additional game is needed to document this gap.

## Public response and limitations

The actual public response is **156 compact-JSON bytes**. It contains only
schema, opaque submission ID, terminal status and integer game/win/draw/loss
counts. The implementation builds that response from a closed allowlist rather
than copying unknown fields; opponent identity, paths and raw-log keys inserted
into observer evidence are dropped. Public replay access remains unavailable.
The real-heldout gate unconditionally raises `BoundaryUnverified`.

The detailed observer report intentionally contains public-opponent names,
source provenance, paths and raw-artifact references. It must remain separate
from the submission-result API; publishing it as a clearly labeled public
research artifact does not demonstrate that a deployed service protects it.

The README/report correctly disclose selected public opponents, matchup-selection
bias, experimental shared-filesystem isolation, no durable/authenticated service,
no provider/controller integration, no sanitized replay-learning loop, partial
schema verification and no tournament/strength claim. Preserve those caveats.
Hashes demonstrate agreement with trusted observer records; they cannot prevent
coordinated rewrites or establish enforcement against a hostile process.
