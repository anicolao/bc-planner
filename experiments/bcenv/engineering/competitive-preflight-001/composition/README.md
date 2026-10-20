# Reviewed component composition

2026-10-20 UTC. This local uncommitted composition combines the exact commits in
`report.json`: public 3.0.13 runtime (PR8), service/controller/replay (PR7), durable
ledger (PR9) and offline Responses codec (PR10). No PR is merged.

Pinned command from the composed worktree:

```sh
nix build .#checks.x86_64-linux.python-unit .#bcenv --no-link -L
```

The local alternate-store wrapper additionally uses `--option sandbox-paths ''`
to avoid a missing optional host bind; Nix build sandboxing stays enabled. No
credentials, new engine match or model call is used. The 190 tests are the
runtime's 127 existing component tests plus 34 ledger and 29 transport tests.
`python-unit.log` is the retained actual build/test output, not a synthetic count.

The resulting competitor package was recursively inspected for the five trusted
implementation filenames; none is present. This packaging check is not access
separation for a native agent with host tools. The services remain trusted-side
code; actual enforcement, authentication, aggregate resource controls and the
source-export/job lifecycle are not established by this build.

To reproduce the source composition without merging branches, start with the
recorded PR8 commit in a disposable worktree. Copy the three `services/*.py`,
matching test files and contracts from PR7; add `ledger.py`/`test_ledger.py` and
`ledger-v1.md` from PR9; add `responses_transport.py`/`test_responses_transport.py`,
`responses-transport-v1.md` and the updated `controller-v1.md` from PR10. Stage
new files so flake evaluation includes them. Compare all file hashes with
`report.json` before building. Do not treat this disposable tree as a release.
