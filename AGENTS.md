# Working on bc-planner

- Record every user task prompt in PROMPTS.md verbatim, in chronological order, including follow-up instructions. Preserve spelling, punctuation, whitespace, and line breaks; do not summarize or correct prompts.
- PROMPTS.md is append-only. Never modify or remove existing bytes. Put metadata outside the verbatim prompt text, and use a longer Markdown fence if a prompt contains code fences.
- New entry headings may optionally include a 3–6-word summary, such as `## Prompt 4: Clarify prompt heading summaries`. Keep the complete verbatim prompt below the heading; a summary never replaces it. Do not retrofit summaries onto existing entries.
- Every commit must include a staged addition to PROMPTS.md. If one prompt leads to multiple commits, append another entry with that exact prompt and explain the repetition outside its text.
- Install development tooling with npm ci to enable Husky. Do not bypass the prompt-record hooks.
- Run npm test when changing the prompt-record enforcement.

- See CONTRIBUTING.md for retrospective voice transcription, sensitive-data exceptions, and CI limits. Never invent exact quotes or publish secrets. Record a clearly marked omission instead and explain it outside the prompt.
- Historical commits before this policy are not rewritten or represented as compliant. Keep design PRs open until the user approves merging.

## Completeness before every commit

- Reconcile every available task-related user message since the last recorded source boundary with PROMPTS.md, including questions, clarifications, status requests, corrections, and follow-ups, not only instructions that directly changed a file.
- Before committing, list the messages checked and map each to an existing or new prompt entry. Record the source coverage, missing context, and any exclusions outside the verbatim text; do not claim an audit covers inaccessible history.
- When work is delegated, pass exact relevant user prompts and require the worker to report which entries capture them. A summary of an instruction is not a substitute for its transcript. Obtain missing exact text from the coordinating conversation before claiming complete provenance.
- If an older omission is discovered, append it with its original relative occurrence and retrospective capture metadata. Do not reorder or edit existing entries to repair chronology.
- Byte-level hooks and CI cannot detect an omitted conversation message. Perform this source-to-record reconciliation even when all automated checks pass.

## Software installation

Use the repository's pinned Nix flake for all software installs, including language toolchains and new dependency acquisition where applicable. Do not silently fall back to apt, direct-download installers, or another package manager. If the flake cannot provide a required tool, report the concrete blocker and update the flake through the normal review process. Earlier bootstrap experiments are historical evidence, not an ongoing exception. Never replace or expose authentication configuration while preparing tools.
