# BCENV-009 fresh input audit

2026-10-22. **Static source-empty export audit passed**, conditional on exact-code
CI, the authorized public integration, live service parity/empty-state check and
parent launch gate. No candidate launched and no candidate helper executed by
this reviewer. This is separate from VALIDATION-009-REVIEW.md.

Audited root: `competitor-009`. Manifest SHA256:
`b756faeeebec02e292b94f6f36df0fe984c603ca5e6588de5b5f0c0982356e1d`.

- Independently enumerated exactly 56 files and recomputed every manifest hash;
  exact key/hash equality passed. No symlinks. `src/`, `tests/`, and `work/` exist
  and are empty. No mailbox exists at this static audit point.
- Compared only static manifest metadata with the earlier export: 47 identical
  hashes, nine changed/new files. Changes are README/kickoff, generic phase doc,
  fixed service client, helper adapter/artifacts and launch paths/manifests.
  No earlier candidate source/tests/work/results were read or copied by reviewer.
- Exported service client, generic candidate-check helper, adapter and artifacts
  are byte-identical to their reviewed engineering counterparts. Fixed launchers
  contain workspace paths and runtime hashes, not bot implementation or coaching.
- Read kickoff, README, phase and replay semantics in full. They require original
  candidate strategy/tests, no outside coaching or agents, preserved failed checks,
  truthful helper semantics and bounded replay evidence. No bot-specific scenario,
  source, strategy, tactical hint, prior run result or evaluator material found in
  the changed instructions. Public rules/API bytes are unchanged by hash.
- Instructions state eight training versions/eight games each (64), exactly two
  distinct completed immutable finalists/eight same new public cells each (16),
  80 maximum games, 24 notes and 150 replay queries across phases. Rejected builds
  consume a version. No re-nomination, source edit/new submission after lock,
  second batch, retry or replacement cell is authorized.
- Clock instruction is explicit: immediately query validation-status; the maximum
  2700 seconds starts at service initialization, not first candidate command.
  Local checks, training, validation and selection share remaining time. Expiry,
  infrastructure failure or uncertain outcome requires stop, not extra time.
- Final choice must be an original locked training ID after both validations;
  restore its exact source, write evidence/limitations and stop. An incomplete
  validation is unscored, not a hidden fallback. Public selection evidence is
  expressly not an independent held-out estimate.

This audit does not attest hostile filesystem isolation or ambient environment
identity. Native wider access is candidly described as cooperatively restricted.
Static cleanliness does not prove future live state; recheck immutable input
hashes, remaining deadline, empty service records and exact launcher parity
immediately before the authorized fresh spawn. No heldout/evaluator contents or
competitor implementation were inspected for this audit.
