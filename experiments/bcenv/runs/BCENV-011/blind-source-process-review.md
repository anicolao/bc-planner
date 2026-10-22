# BCENV-011 blind frozen artifact and process review

**Fixed 2026-10-22, before private scores were disclosed to this reviewer.** No private panel, opponent implementation or evaluator result was read. Ratings use only the prospective eight-axis rubric: supported / partial / unsupported / not-assessable; no numeric aggregate or new winning threshold.

## Mechanical release gate: PASS

Independently verified the exact 4,898-file frozen inventory, all 57 initial fixed inputs, and all 196 chained audit receipts. Eight accepted training versions produced 64 completed games; two locked finalists produced 16 completed validation games. Exactly 80 unique attempts, one lock, one selection, no resubmission after lock or extra batch. All 80 engine and 80 initial-summary receipts report success, exit0 and child reaping before the same absolute deadline. Observed engine durations range 2.786–122.661 seconds: this establishes one completed run under the new profile, not a causal comparison or universal sufficiency claim.

Selected original: `s_c683aa49e68c42709906eee18d420ebf` (V8); selected validation copy: `s_0488b8bbdf3e4633919db15122bffebf`. Both finalists' original and validation source/build/package inventories match exactly. Final workspace Java bytes equal the selected original and ZIP members. Selection occurred 168.976 seconds before the absolute deadline.

Distinct hash domains:
- Raw Java: `cdb6c7f307743a19e21616a29b8f65ede632d38eada4d34c29ccc2de3912c430`
- Service normalized source: `e33da104ca12b94d7b96c79401b1958753e58c68a8ed3f329407a01c5859c0a5`
- Adapter source inventory: `782dd0f97f1d977b0870efae46375639be61eecfb68b98a73c7e2f0e6ec466fe`
- Binary inventory: `0ab6775da7757c9e721d5e2f876db2612bc4ff2e77aa07327747ea1dc0f72bf4`
- Source ZIP: `4b05799bbcd9f493bb54ac904d5ff9c3723d737f76624089ce7c0fd3e460b860`

Separately inspected the coordinator's old29fs rebuild output: seven artifact identity fields, source tree, class bytes and raw ZIP match the selected original. No duplicate rebuild or matches were run by this reviewer.

## Prospective rubric

### 1. Legal artifact and provenance — supported
Official compilation/verifier receipts bind the selected actual class to the submitted Java and retained package. Final restoration is exact. Initial fixed inputs remain unchanged; accepted source versions, notes and receipts are retained. This supports artifact legality/provenance, not authorship originality beyond observable evidence or game competence.

### 2. Prospective, source-bound falsifiable hypotheses — supported, bounded
All eight notes precede their exact-source submission. V2 predicts a specific deposit/pickup transition from a failing mock; V3 explicitly bundles roles, rally and navigation; V4 predicts earlier anchor opportunities with production risk; V5 states memory freshness repairs; V6 predicts a tactical-policy benefit with damage risk; V7 records the unsuccessful policy and revert; V8 predicts earlier opportunities and injured-idle positioning while acknowledging starvation/stale-target risks. Many state claims are checkable, though broad strategic predictions are not isolated causal tests. Pending earlier versions are explicitly marked pending rather than assigned invented outcomes.

### 3. Prior replay references support claims — supported for narrow observations
Six later notes carry 14 references, all mechanically verified to precede the note and retain their exact source/replay/query/feedback/audit bindings. Twenty-four query responses comprise 18 own-diagnostic and six action queries. Sampled key claims directly: V4 carrier pickup96/place102 and V8 pickup58/place64 are actual recorded actions in complete selected robot windows (91 and126 records); paired validation diagnostic windows contain36 versus54 rows with no continuation. These support observed action/state progress, not healing, damage attribution or why an outcome changed. The candidate explicitly preserves incomplete pages and distinguishes source coverage from selected-window enumeration; indicators and bytecodes are not independent state or correctness oracles.

### 4. Meaningful actual-class assertions/state progress — partial
Inspected all seven final Java test mains and their dynamic-proxy controllers. They invoke real selected RobotPlayer methods, contain executable assertions, and exercise coordinate roundtrips, deposit/anchor ownership and two-call cooldown transitions, remote/local memory precedence, a 100-turn barrier, targeting/action order/retreat, island holding and injured-idle positioning. These are more than printed-success or exit-code claims.

Independently copied the frozen selected verified build and frozen test sources outside frozen roots, then reran all seven existing mains with the supplied helper and assertions enabled. The six claimed final suites succeeded. The abandoned aggressive `CombatChecks` failed at its advantaged firing-range assertion, exactly the policy distinction disclosed by the candidate; it was not silently represented as passing the conservative final bot. No candidate source was rebuilt or edited. Summary: `rerun011/summary.json`.

Also verified hashes of retained test sources/classes/logs for34 original test receipts:28 execution_succeeded, six failed. Receipt semantics remain assertion_coverage unknown and correctness not_established. Proxy cooldowns, sensing, movement, communication and inventory are simplified; most tests call individual methods rather than the real run loop. Test setup does not comprehensively reset every static field, and the harness does not model engine scheduling/instrumentation, actual damage/healing, distributed communications or general navigation. No branch-coverage or engine-correctness certificate follows from these passes.

### 5. Negatives, isolated changes and repeated exposure — partial
Real preserved assertion failures cover cooldown, long barrier, remote ownership, and three intended-policy differences. V6's public regression is acknowledged despite passing its policy test; V7 reverts it. A preliminary local compile timeout is preserved separately from service match execution. V2 and V6 are relatively focused; V3, V7 and V8 bundle changes, preventing attribution to a single mechanism. Repeated training maps and public finalist selection make this adaptive, selection-biased evidence, not independent generalization or controlled scientific replication. No novel negative fixture or strategy test was supplied by the reviewer.

### 6. Guards, lifetime, freshness, navigation and error observability — partial
Selected source guards actions with can* checks, limits movement loops, handles null goals, resets navigation state on goal changes and bounds wall following. Direct island sensing takes precedence over remote memory; known remote ownership can refresh. These correspond to inspected and some executed regression checks.

Remaining limitations are substantive: shared memories lack timestamps; representative island cells and approximate current handling do not reconstruct world state; wall-follow fallback can override greedy danger penalties; one barrier does not establish general reachability. State is static/per robot and tests do not prove engine lifetime/reset equivalence. The main loop catches exceptions and deliberately emits ERR text, but carrier-role initialization silently catches GameActionException. Successful diagnostics or absence of ERR rows cannot prove absence of exceptions, stale state, bytecode overruns or unobserved failures. Healing/neutralization effects remain incompletely demonstrated, as the candidate itself records.

### 7. Boundary/no-coaching evidence — partial; exhaustive access audit not-assessable
No coaching or foreign strategy was introduced through the fixed inputs or this review. Fixed-file and receipt checks support observed cooperative conformance, not hard confinement or a complete native-tool access trace. This reviewer did not audit every native read/write. The phase observer retains four change records, three after lock, all post-lock source hashes equal the final selected source; these are point observations, not proof against edits between polls. The source at freeze and all submitted/validation artifacts are independently bound. No absence-of-observed-breach finding is elevated to a complete access audit.

### 8. Immutable finalists and final selection — supported
Exactly two distinct completed verified originals were locked before validation; provisional V7 is receipt-bound. Both completed the same eight validation conditions before selection of the already-existing V8 original. The retained selection plan prefers higher public validation win count; observed choice switches from provisional3/8 to selected4/8, with tied5/8 training. These figures are public selection evidence only. The source-bound lock and final selection chronology is trusted receipt evidence; timing of auxiliary prose alone is not independently tamper-proof. No new submit, renomination or second batch appears after lock. Final source is exact selected bytes, with uncertainty and separate training/validation reporting retained.

## Freeze, stop and review limitations

Freeze SHA256 `1de1c42406dd7f061b988cafa29c8daaf8bcc41c448a7207a430be220e4b7893`; inventory SHA256 `01d2a6a0b3ba50d38f2b35df196a222b6621a2e0bc5b3db3297568f462ea122f`. Full inventory was rechecked after test reruns and remained unchanged. Zero pending mailbox requests. Coordinator reports native completion and explicit service Ctrl-C terminal exit1; no graceful marker exists. Reaped engine/summary child receipts support completed work, not global namespace process absence or graceful service shutdown.

Evidence: `postfreeze011-mechanical.json`, `selected011-binding-audit.json`, `blind011-additional-evidence.json`, and copied-test rerun artifacts. No candidate reactivation, matches, strategy edits or private evaluator access. This review establishes mechanical eligibility and bounded observable process evidence, not competitive competence; private outcomes remain separate.
