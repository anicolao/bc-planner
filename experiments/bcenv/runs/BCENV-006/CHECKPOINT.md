# BCENV-006: infrastructure-invalid, frozen

The fresh competitor stopped correctly after its first accepted submission
returned `infrastructure_failure / worker_failure`. **Zero games started, zero
replays were queried, and no evaluation panel was acquired.** This is an
operator/environment failure, not evidence of model competence or weakness.

The prelaunch integration passed eight games with raw replay hashes identical
to BCENV-005. However the operator launched that integration under existing host
Python, then mistakenly wrapped the actual development service in a Nix shell.
The worker's fixed adapter command itself enters the relocated Nix runtime. This
nested invocation failed before creating a build artifact:
`error: setting up a private mount namespace: Operation not permitted`.
A minimal independent reproduction confirms the same fixed adapter help command
passes unnested and fails nested. No security change is required or authorized.
The readiness gate did not establish actual service-launch context parity.

The candidate and development service are stopped. One prospective note, one
submission, one failure completion and one result receipt form a consistent
four-event chain. All55 original static export inputs remain unchanged. The
candidate's final report honestly disclaims game/replay performance conclusions.
Its local helper verification and mock tests do not substitute for live games.
There was no retry, observer strategy advice, or candidate repair/resumption.

Corrective scope: a single shared operator launcher for integration and live
service, a bounded same-context adapter startup probe before mailbox readiness,
and a new independently reviewed prospective fresh-agent run. Preserve006 as
invalid rather than relabeling a replacement as a successful retry. Reuse of the
still-sealed evaluator regression panel requires explicit prospective adoption;
no panel source or outcomes were accessed during006. Keep all PRs unmerged.

The existing cooperative same-user access and archival limitations still apply.
Only aggregate metadata and public engineering failure details are published;
raw candidate and service records remain local for this stopped run.
