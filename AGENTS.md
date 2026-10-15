# Working on bc-planner

- Record every user task prompt in PROMPTS.md verbatim, in chronological order, including follow-up instructions. Preserve spelling, punctuation, whitespace, and line breaks; do not summarize or correct prompts.
- PROMPTS.md is append-only. Never modify or remove existing bytes. Put metadata outside the verbatim prompt text, and use a longer Markdown fence if a prompt contains code fences.
- New entry headings may optionally include a 3–6-word summary, such as `## Prompt 4: Clarify prompt heading summaries`. Keep the complete verbatim prompt below the heading; a summary never replaces it. Do not retrofit summaries onto existing entries.
- Every commit must include a staged addition to PROMPTS.md. If one prompt leads to multiple commits, append another entry with that exact prompt and explain the repetition outside its text.
- Install development tooling with npm ci to enable Husky. Do not bypass the prompt-record hooks.
- Run npm test when changing the prompt-record enforcement.

- See CONTRIBUTING.md for retrospective voice transcription, sensitive-data exceptions, and CI limits. Never invent exact quotes or publish secrets. Record a clearly marked omission instead and explain it outside the prompt.
- Historical commits before this policy are not rewritten or represented as compliant. Keep design PRs open until the user approves merging.
