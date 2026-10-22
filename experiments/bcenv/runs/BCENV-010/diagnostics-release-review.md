# Own-team diagnostics release identity review

2026-10-22. **PASS — no release-identity discrepancy found.** Read-only verification of saved CI evidence and local committed/store bytes; no new games, builds, full test reruns, candidate launch or private evaluation access.

- PR22 exact head: `66ff4650fd6481cf3a69925098e48e6abc865e53`. Every source hash in the independent engineering review matches that committed revision.
- Saved CI run `39783686439` is completed/success and names that exact head. Saved release revision is CI merge `5c254eb4dad9942d0c7712d5cc6dded12184f37d`; its recorded parent includes the exact head. The CI merge tree equals locally resolved head tree `fecf508d573cd92a779c102e1c18c55dbe00e97d`. Retained CI flake.lock matches committed bytes.
- CI and local clean-Git metadata agree on store path `/nix/store/1bbk58382aq40pplbyy2fir27qnx3jxj-bcenv-2023-0.1.0`, deriver, 306,584-byte NAR size and complete dependency-reference list.
- Independently recomputed the actual installed tree's NAR hash with `nix hash path`: `sha256-1MzBzVI1R4gsIv6dpxJceQfgznGm4zyvUMJlyXvUNxo=` — exactly the CI artifact and saved local hash.
- Independently compared all 55 installed entries against smoke-tested `ir2mliawfvi6gg07rgrx1pfcp0bf3f0f`: matching paths/modes and bytes except the wrapper's own store-prefix substitution, which normalizes exactly. No engine/dependency substitution appears in the matched metadata.
- All evidence hashes listed in `engineering/own-diagnostics-implementation-ready.json` validate, including the unchanged engineering review SHA-256 `b1fc3f9453a6409c90e49337248638acd3ea7f7647dcd114462918b05d860897`.

Evidence scope: this verifies retained CI records, their consistency with exact source, and actual local store content; it does not recontact GitHub or independently reproduce the full CI execution. Registration timestamps differ between stores as expected and are not content identity. Draft PR/merge permission and any future trial authorization remain separate; the readiness record explicitly does not authorize candidate launch. Earlier engineering and frozen reviews were not modified.
