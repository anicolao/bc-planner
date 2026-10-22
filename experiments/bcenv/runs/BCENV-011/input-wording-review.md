# BCENV-011 narrow prelaunch wording revision

2026-10-22 14:42 UTC. **PASS.** This supplements, without modifying, `PRELAUNCH-011-INPUT-REVIEW.md` (SHA256 `0c6addf0426bf31208ecd67a0650149321207f288a5c3bbe8ffd94ae66e710f8`).

Independently reverified all 57 static file hashes and clean source/tests/work directories, absence of symlinks/mailbox, every preparation dependency hash, and absence of a preflight service/launch/driver claim/GO. Compared against the preserved pre-wording manifest: only README bytes changed. The preparation dependency change is only the export-manifest hash. No code, kickoff, schedule, quota, driver, reader or configuration change.

README and protocol now explicitly say the unchanged timeout=120 applies to child subprocesses, clipped by the same absolute deadline, **not a total-request elapsed-time guarantee**. This resolves the possible whole-request interpretation without changing actual behavior or supplying strategy. The original manifest was preserved with its exact reviewed hash; replacement manifest records this prelaunch revision and previous hash.

Final reviewed hashes:
- Export manifest: `26b216760992f4975f9d22aad152578bc854c89a11e7f20286f9631c50abff80`
- Protocol: `cb03979ef04791d0283e639bc940f8ebdf4b6011e5f5e9e5984340caef478b4c`
- Preparation manifest: `05f122d995945e8fb8ef20de391fdcc1116bbd3864c41c194578061478671104`

All previous review boundaries and remaining gates stand. Use these revised hashes in publication and parent-issued prospective GO. No games, builds, queries, tests or service initialization were performed by this review.
