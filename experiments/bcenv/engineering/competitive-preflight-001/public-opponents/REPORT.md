# Public BC23 source integration smoke: 3.0.13

All six unchanged public packages compiled and passed the official verifier. Ten of eleven bounded DefaultMap attempts completed with version-matched, structurally complete replay summaries. The v5anaconda side-A attempt hit the fixed 120-second wall-clock limit; its side-B attempt completed in about 22 seconds. All timeout logs and the failed result are preserved. No compilation or verifier failure was observed. This is active compatibility evidence, not a strength ranking or reproduction of the historical final tournament.

## Scope and isolation

The six repository/source pins, root licenses and all 89 Java-file hashes come from the verified public Nix fixed-output catalog. Each package was compiled separately, including its own utility subdirectories. No upstream Gradle task ran, no strategy was edited, and no source file was truncated or split. Each source snapshot retains its own AGPL license and provenance.

Engine: official public 3.0.13, SHA-256 `2b6db98e312e0e509d599acc46bffbb55c2569de0f12c8214a85ee57625f15f2`. DefaultMap SHA-256 `a53211fc3fb4cc6427693f6f65b0732cc4bdf9ecb90f911ffbd71b5af82bb910`. Runtime store identities and the complete closure are in `smoke-manifest.json`. These checks used the initial adapter `/nix/store/wzmq4kaajn9bizwmy4x6n0hbjn97v46a-bcenv-2023-0.1.0`. The subsequently published final package has a different store identity; these results do not claim that package was used. `runtime-file-hashes.json` preserves hashes of the actual adapter, helper source, compiled replay tools and launchers used. The launcher clears its environment and uses the previously authorized user/network-namespace plus chroot pattern, with only the curated Nix closure and public sources copied into the root and no host filesystem binds. This is a bounded integration harness, not a newly validated hostile-code security boundary.

One lectureplayer self-play match checked the reference. Five other packages each ran in A and B positions versus that lectureplayer. Eleven of the twelve authorized maximum matches were used, once each, with no retries. The per-process timeout was 120 seconds.

## Replay-observed activity

The table reports the candidate side’s raw events in rounds 1–50; ranges span the two side positions. All queries returned the complete requested record set, with all 50 requested rounds present. Pickup and attack counts are replay action events, not inferred quantities collected, successful hits or damage. Spawn records exclude initial map bodies.

| Package | Completed/attempted smoke matches | Spawn records | PICK_UP_RESOURCE events | LAUNCH_ATTACK events |
|---|---:|---:|---:|---:|
| USQualifiers | 2/2 | 33–35 | 325–461 | 117–235 |
| FB_ZZZ | 2/2 | 30–31 | 485 | 397–443 |
| MPWorking | 2/2 | 31–32 | 463–476 | 341–347 |
| submit26_final | 2/2 | 30–31 | 478–486 | 332–345 |
| lectureplayer | 1/1 | 3 | 60 | 0 |
| v5anaconda | 1/2 | 27 | 483 | 425 |

The lecture reference also placed anchors in the early replay window. The five non-lecture packages all spawned units and produced resource-pickup and attack events in their completed matches. For v5anaconda, these counts cover side B only; no complete replay exists for its timed-out side-A attempt. This demonstrates active execution of more than an inert entry point on this one public map.

## Important limits

- v5anaconda has not passed the paired-side completion check. The timeout establishes failure to finish within this harness budget, not its underlying cause. No retry or larger time allowance was used.
- The unmodified adapter disables robot stdout. Successful verification and complete matches do not establish exception-free bot behavior, absence of bytecode overruns or correctness on all reachable states. Engine logs preserve a Java startup warning about primordial thread stack location in this minimal root.
- No standings, win rates or historical-strength calibration are inferred from these smoke results. Raw match artifacts retain their actual outcomes for audit.
- A private 3.0.14 finals build injected private maps. Public 3.0.13 testing does not authenticate the exact finals server artifact or maps.
- The original proposed 128 KiB/file and 1 MiB total-source limits reject v5anaconda and MPWorking as documented in the candidate report. The corrected service profile uses 512 KiB/file and 2 MiB total, accommodating all six measured packages; the original measurements and failures remain preserved. Passing a direct adapter build does not validate a service intake implementation.
- Public-source contamination, shared lineage and exact-submission-attribution limitations remain unchanged.

## Evidence

`build-summary.json` points to all six source/build identities and compile/verifier logs. `match-summary.json` points to all eleven engine logs/results and the ten complete replays/summaries. `activity-summary.json` records query hashes and candidate-side counts; raw query outputs remain alongside each match. `source-catalog-at-launch.json` preserves the exact catalog snapshot hashed at launch; the current public catalog adds subsequent verification results. The planner-ready public evidence directory excludes engine JARs, map bytes, binary classes and replays; raw artifacts remain separately available in scratch. No repository-wide engine/map redistribution grant was established, so component notices are not treated as map permissions. Credentials, heldout assignments and secret schedules are absent.
