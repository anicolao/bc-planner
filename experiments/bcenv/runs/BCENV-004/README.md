# BCENV-004: completed development phase

This fresh cooperative native-agent run started 2026-10-21 13:25:42 UTC and
finished before its 45-minute deadline. The agent returned its final selection
at 13:37:23; native status confirmed completed, the trusted service was stopped,
and observer copies were hash-frozen at 13:37:36. No selected held-out artifacts
were introduced until after that freeze. Independent evaluation is separate.

## Result and claim boundary

The VM successfully hosted the trusted service and official 3.0.13 runtime.
Separate tool invocations used bounded atomic file RPC; a separate-invocation
loopback HTTP attempt failed, which is a measured transport limitation rather
than proof that the VM cannot host services. CLI inference remained unavailable
due to local EROFS startup; fresh native agents supplied the model transport.

Six immutable source submissions were consumed: one official-verifier rejection
and five complete four-game versions. All 20 development games and the rejection
are retained. Legal versions scored 4/4, 4/4, 3/4, 4/4 and 4/4 against the public
Beaver Bois USQualifiers package on DefaultMap and Rectangle, both sides. These
are repeated fixed development games, not independent generalization samples.
The competitor autonomously selected version 6; no observer repaired its bot,
selected its strategy, or told it which version to choose. It made 49 bounded
replay requests. No infrastructure failure occurred.

The selected file hash is
`2e235e4f9c29a5b904fae2633d28e96f21126184c62ea8bf450f62db88c85b42`.
`source.zip` is the adapter's packaged source, SHA256
`743294b954d934bd20824f462ccd878cec713cefa1900ab4d8a89529a2b5b48e`.
The service normalized-source digest is separately
`0ae8c2f32053048f84537ee01bedda217abde5efc03deb8225c3f0564a22780f`.
Different digest schemes are not interchangeable. Observer comparison confirmed
final source bytes equal the selected service build's source.

## Evidence

- `launch.json`, `kickoff.txt`: exact prelaunch export hashes and input prompt.
- `integration-manifest.json`: original local pregame map/build pins, later
  published unchanged. It was not itself committed before those four games.
- `freeze.json`: stop/freeze evidence, artifact hashes and operation counts.
- `FINAL.md`, `candidate-experiments.md`, `candidate-versions.json`: candidate's
  unedited report, experiment narrative and version ledger, not observer truth.
- `candidate-final.java`, `source.zip`: selected unmodified source.
- `evidence.tar.gz`, `evidence-manifest.json`: all candidate workspace/work files,
  mailbox requests/responses, service audit/builds/results/replay queries, all
  20 development replays, four integration replays, and development source/build
  provenance. Extract into a fresh observer directory, never a future competitor
  workspace. Archive file paths map to the original local directory structure.
- `code-audit.md`: independent postfreeze code/reasoning review, fixed before
  release of held-out scores (added when completed).

Public development packages came from official lectureplayer repository
`battlecode/battlecode23-lectureplayer` at
`57063ad07b2311c21c99ba7be100a55fcdb3de6b` and
`beaverbois/battlecode23` at `4892382943da5a8527906467739a64db51ccc50d`.
Upstream README/LICENSE files and selected source are retained in the archive.
No upstream code was modified or relicensed. The tutorial integration control
lost all four games and was never represented as the model's output.

## Audit limitations

Native spawn requested `gpt-6.1-sol`, effort `high`, `fork_turns:none`; the tool
accepted the task and returned its name, not an independent identity attestation.
No native token/currency accounting was available. No paid external account or
new billable infrastructure was provisioned.

All 50 supplied kickoff/docs/tool files remained byte-identical at freeze.
Native agents nevertheless share filesystem/tool access: procedural boundaries,
not malicious-agent containment. No complete native tool transcript was
available to this observer. The agent reports no prohibited access; this is not
an independently complete access audit. Missing observation is not misconduct,
and artifact consistency does not establish hard isolation.

The experiment narrative records specific pre-change predictions, failed
hypotheses and replay citations. Service timestamps independently establish
submission/replay ordering, but the final editable narrative does not by itself
prove every prediction was recorded before outcomes. A future environment
should capture append-only prospective experiment notes through the interface;
this run's missing temporal attestation cannot be retroactively supplied.

The learning loop and code assessment must remain separate from win counts.
One successful cooperative development run neither completes the larger
three-agent competence campaign nor supplies merge permission. Held-out feedback
will not be given to this stopped competitor.

## Post-freeze outcome

The frozen candidate won **4/24** valid diagnostic held-out games, with no retries or infrastructure failures. See [aggregate evaluation summary](EVALUATION-SUMMARY.md). Detailed benchmark material remains observer-local. The cooperative environment functions; broader competitive competence is not achieved. No feedback returned to the stopped competitor.
