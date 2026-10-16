# bc-planner
Planning and architecture for the Battlecode coding-agent learning system

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md). Install hooks with `npm ci`; every new commit must append the applicable exact prompt to [PROMPTS.md](PROMPTS.md). Run `npm test` to verify enforcement. The initial record is explicitly retrospective.

## License

This project is licensed under the GNU General Public License, version 3 (GPL-3.0). See [LICENSE](LICENSE) for the full text.

## Runtime experiments

[Consolidated findings and provenance](experiments/README.md): local Nix, WireGuard and SSH probes retained; usable remote access was not achieved and is deferred because there is no immediate need.

## Prior art

[Terry Van Belle’s Battlecode implementations](terry-battlecode-prior-art.md): pinned source review, implementation findings, learning-loop observations, and verification limits.

## Proposed experiments

[Battlecode 2023 experiment plan](2023-experiment-plan.md): proposed steps for local bot execution, replay understanding, and a local replica of the competition scrimmage infrastructure. Awaiting review; no implementation is included.

## Environment improvement process

[bcenv experiment loop, reusable protocol and append-only ledger](experiments/bcenv/README.md): proposed process for testing our environment changes, with an unrun replay-diagnosis proposal. Separate from the approved 2023 plan and implementation findings.
