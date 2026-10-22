# BCENV-009 prospective public validation map selection

Metadata prepared before any009 candidate export, launch or validation games. This procedure did not inspect map geometry, scores, evaluator schedules or any heldout files. Existing raw public-map bytes were read solely to compute file hashes and sizes; no dependencies or opponents were acquired.

## Inventory and exact ranking

The pinned public official Battlecode23 engine3.0.13 inventory contains103 `.map23` regular files. Engine source revision: `9b890f83672c98b81cc153f618bd56e1ab6134b5`; engine JAR SHA256: `2b6db98e312e0e509d599acc46bffbb55c2569de0f12c8214a85ee57625f15f2`.

For each map, calculate SHA256 of its exact raw file bytes, represented as64 lowercase hexadecimal ASCII characters. Calculate a second SHA256 over this exact UTF-8 string:

```text
BCENV-009-public-validation-v1\n<exact filename including .map23>\n<lowercase file SHA256 hex>\n
```

Here `\n` denotes one literal LF byte0x0a, including the final LF. There is no BOM. Filenames retain exact case. The map digest contributes its hexadecimal text, not raw digest bytes. Sort by the resulting ranking hash ascending, with exact filename ascending as deterministic tie-breaker. Exclude **only** `Quiet.map23` and `BowAndArrow.map23`, the training maps. Select the first2 of101 eligible maps. The full103-file inventory, all file/ranking hashes, sizes and eligible ranking are retained in `validation009-public-map-plan.json`.

## Selected public maps

| Order | Filename | Raw-file SHA256 | Ranking SHA256 |
| --- | --- | --- | --- |
| 1 | Elephant.map23 | 87c0f362b047d31ae4887cb8aef43d84a83045aca9b9b878f1beee95ea9cc4e2 | 0c9c9208ea316302da5618ec4051014cedac0d075d286e75a38e111cbb1c76cf |
| 2 | Spiderweb.map23 | 07f4cc645a86982b1d37f2209b1a539be397c3bcf8cf42e1133499749a6e84c4 | 0c9efdb66a50545abadcd9256c41812149d05195aa69b1219eae9636d409419d |

The identical ordered8cells for each of2 locked finalists are: existing Beaver public pin first, existing Musketeers public pin second; for each opponent, Elephant then Spiderweb; for each map, candidate slots A then B. No opponent source changes. Exact trusted build paths and public opponent revisions are recorded in the operator JSON, not competitor-supplied paths.

## Budget and interpretation

Maximum64 existing training games plus16 public validation games =80, within the45minute task budget. Per-game timeout remains120seconds and engine heap512MiB. No retries or replacement maps; infrastructure failure stops the phase. No games were run to prepare these metadata.

These are public selection conditions new relative to the2 training maps. They are not an independent final holdout, not claimed globally unseen, and not filtered against private evaluator membership. Once validation informs the candidate's final choice, its resulting score is selection-conditioned evidence. Same-user filesystem restrictions remain cooperative; withholding exact validation cells until nominations lock would be procedural, not hard secrecy.

Plan SHA256 at preparation: `243283d229fadfc252a407b17178e4bc6bdf29d1dfa980519cd59ea283ea9d63`.
