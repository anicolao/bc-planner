# Integrated competitive preflight: independent audit

Audit date: 2026-10-20 (UTC)

## Verdict

No integration defect found at commit
`d769760da47cedb4acf6c44b24497a7f29ef1fc5` on
`feat/competitive-service-integration`. This is a provenance and integration
audit, not approval for deployment, model calls or hostile-code trials.

## Verified provenance and scope

- All **14 entries** in `docs/COMPETITIVE-INTEGRATION-SOURCES.json` were checked
  against their recorded SHA-256 values. Every file is byte-identical in the
  working tree, integration commit and cited source commit.
- Recorded sources are `04c815954154a9be691bb531245f74e35cbd6edf`,
  `be041d3d18ecd9fa474cbfb076c86c336d5b6ff3`,
  `8f2125d12db4df1f16bca721179ec52cf16273d6` and
  `287ac43afb8b05d4e3006b14030323a0c2f9f997`.
- Runtime, season, Nix and flake files are unchanged from the PR8 runtime base,
  `f3e37cb9f96c41334aa649a4f24813a880515ff8`.
- `launch_real` and `require_heldout_attestation` retain the exact reviewed,
  permanently closed implementations.
- Component contracts and historical independent review reports match their
  respective source commits. The controller contract correctly includes the
  already-reviewed offline Responses wording from `be041d3`. The only new
  component-contract reconciliation is the replay-feedback producer note,
  describing the integrated public `3.0.13` runtime and separate `2.0.3`
  diagnostics while retaining exact version matching.

Source-manifest SHA-256:
`7fb1fe082bdd87a1702388008d72b4ef2b117f09791f3219ee744d92ad3e9b6a`

Recorded-checks JSON SHA-256:
`6dac399109d2538f3be592d50caedd9d386fe10c2d1f15cc97cb9ca1db2ed160`

## Package and existing check evidence

The evaluated and realized competitor package is:

`/nix/store/db83y5kks77pyc5rvb3h78k23m59myp7-bcenv-2023-0.1.0`

Its complete tree was inspected. It contains no `services` subtree and none of
the seven trusted module names: `controller.py`, `controller_ledger.py`,
`ledger.py`, `replay_feedback.py`, `responses_transport.py`, `scrimmage.py` or
`worker_lifecycle.py`. The package filter/install rules are unchanged from PR8.
Packaging exclusion does not establish host filesystem or process isolation.

The existing integration log records **13 x86_64-linux flake checks** and
**230 passing Python tests**. The auditor resolved all 13 recorded derivations
and verified their output paths already exist. The log and recorded result
explicitly leave aarch64 untested. The checks preceded documentation-only result
files; this audit did not rerun games or make new model calls.

No files in the integration worktree were edited. No credentials, security
settings, network boundaries, launch gates or heldouts were changed. The
documented deployment, authentication, supervision, evidence-validation and
end-to-end trial gates remain unpassed.
