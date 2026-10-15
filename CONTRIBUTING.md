# Contributing

## Setup and checks

Use Node.js 20 or newer. Run `npm ci` to install pinned Husky tooling and activate the pre-commit and pre-merge-commit hooks. Run `npm test` after changes to enforcement; `npm run check:prompts` checks the current Git index. Do not bypass hooks.

## Prompt record

Record every user task prompt, including follow-ups, in `PROMPTS.md` in chronological order. Preserve spelling, punctuation, whitespace and line breaks exactly as available. The file is append-only: never change or remove existing bytes. Each commit must stage a non-whitespace addition. For multiple commits responding to the same instruction, append that exact prompt again and explain the repetition outside the quoted text. Optional 3–6-word summaries belong in headings, never in place of full prompts. Use a fence longer than any fence in the prompt.

For voice, preserve the available transcript and identify it as such; a transcript is not a guarantee of verbatim audio. Retrospective records identify capture date, source, gaps, and uncertainty. Do not reconstruct missing words from summaries or memory. Duplicated delivery of the same utterance may be recorded once with that fact stated outside the quotation. Corrections are new entries, never edits to previous ones.

Never publish credentials, device-login codes, or unrelated private conversation. If a task prompt contains sensitive material, stop before publishing it, record an explicit omission marker and its reason, and obtain guidance; never silently claim the redacted text is verbatim.

## Enforcement and limits

Local hooks verify a regular non-executable staged PROMPTS.md file, preservation of existing bytes, and a non-whitespace append. They reject unstaged-only additions, deletion and rewriting. A merge commit also requires an append; if automatic merge preparation fails, append and stage the applicable prompt and finish the merge commit. Fast-forward merges create no new commit.

CI runs tests and validates prompt additions in every post-adoption commit in the PR/push range, rather than just the aggregate diff. Commits predating policy adoption are explicitly grandfathered; this first provenance commit is retrospective, not a claim of earlier compliance. The history validator requires the policy to have been adopted by the checked head and rejects removal after adoption.

Hooks can be bypassed and CI workflows can be changed. These checks cannot prove a prompt is a faithful transcript or prevent every malicious edit. Making the CI check required through branch protection/rulesets is a separate repository setting; it has not been configured by this change. Reviewers should inspect changes to the policy, validator, and workflows themselves.

The initial local hook and test implementation is adapted from anicolao/bcenv (GPL-3.0-only). bcenv is unchanged.

## Pre-commit completeness checklist

1. Read AGENTS.md and gather the available task-related user messages since the last recorded source boundary, including questions and follow-ups.
2. Compare exact text against PROMPTS.md. Map each message to an existing entry or append a new entry; record coverage and any unavailable source material outside quotations. Do not silently narrow the record to implementation commands.
3. For historical omissions, append the exact recovered text and note where it occurred relative to existing entries. Preserve all old bytes. Never invent a missing ending.
4. Ensure delegated work returns both its changes and the exact prompts it used. Request unavailable wording before describing provenance as complete.
5. Stage the record with the changes, run the hooks and tests, and review the source-to-entry reconciliation separately. A passing byte check is not a completeness check.

For this correction, the nine supplied voice utterances map in conversation order to entries 23, 24, 25, 20, 26, 22, 27, 28, and 29. Entries 20 and 22 already existed; the others were recovered append-only. The scope is those supplied transcripts, not an assertion that all historical audio or messages were available.
