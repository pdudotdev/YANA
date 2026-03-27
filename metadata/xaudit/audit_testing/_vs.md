## Legacy QA audit: Basic agent prompt
```
You are a Senior QA Architect and Engineer. Please do a thorough, careful, well-thought and well-planned analysis of all of our automated tests under the testing/ directory (including live/), and see if there are any gaps in testing when it comes to our codebase and project overall - did we miss anything important that should've been part of the test suites? Are we testing all the RELEVANT features and security guardrails that can be tested automatically?

Also, VERY important - make sure that the existing automated tests are actually passing ONLY if the INTENDED functionality being tested works as expected, NOT because of a ghost condition or a silent pass. In other words, each test should actually test something, and not just invent its own pass conditions and then pass regardless - this is EXTREMELY IMPORTANT both for the project itself and for outside credibility.

CRUCIAL! Be ruthless in your analysis, be objective and cold like an external Senior QA Auditor looking to catch the internal QA team off-guard.
```

## Upgraded QA audit: Skills and checklists
See `.claude.example/skills/audit-testing/`.
> Run `/audit-testing` in the Claude Code CLI.

## Results
- `legacy_report.md` — generated with the original unstructured prompt
- `upgraded_report1.md` — v1 (over-specified skill, historical artifact)
- `upgraded_report2.md` — v2 (rewritten skill)
- `upgraded_report3.md` — v3 (final, with ghost-pass heuristic fix)

**Note:** Each report has been generated with Opus 4.6, Effort High, and in Plan Mode - **after** clearing Claude's context.

---

## Evaluation: Legacy vs. v1 vs. v2 vs. v3

### Report Versions

| Version | Source | File | Lines |
|---------|--------|------|-------|
| Legacy | Original unstructured prompt (pasted into chat) | `legacy_report.md` | 374 |
| v1 | First `/audit-testing` skill (over-specified, rigid phases) | `upgraded_report1.md` | 161 |
| v2 | Rewritten skill (persona + freedom + required sections) | `upgraded_report2.md` | 512 |
| v3 | v2 skill + targeted ghost-pass heuristic fix | `upgraded_report3.md` | 425 |

**v1 was a regression** caused by over-specification (rigid phases, prescribed checklists as steps, report format that excluded the most valuable sections). It is included here for historical reference only. The v1-to-v2 rewrite and the lesson learned are documented in the feedback memory `feedback_skill_overspecification.md`.

**v2-to-v3 change:** One paragraph added to the S1 (ghost pass) section of the skill, directing the agent to watch for trivially-true assertions (e.g., `len(x) > 0` against a pre-populated store).

---

### Overview

| Dimension | Legacy | v1 | v2 | v3 |
|-----------|--------|----|----|-----|
| S1 ghost passes found | 3 | 2 | 0 (missed 1) | 3 |
| S2 mock findings | 3 | 2 real (3 downgraded) | 2 | 0 (all cleared with evidence) |
| S3 coverage gaps | 14 | 7 | 10 | 10 |
| S4 / infrastructure issues | 3 | 7 | 5 | 5 |
| Per-suite verdicts | 11 suites | **Absent** | 12 suites | 12 suites |
| Feature-to-test traceability | 28 rows | **Absent** | 33 rows | 30 rows |
| Prioritized recommendations | 14 items | **Absent** | 15 items + code | 15 items + code |
| Security test gaps | 3 items | **Absent** | 4 items | 3 items + coverage table |
| Infrastructure issues | 3 items | **Absent** | 5 items | 5 items |
| Self-challenge in report | No (internalized) | Yes (shown — incoherent) | No (internalized) | No (internalized) |
| Internal consistency | Clean | Clean | UT-005 GOOD/P0 conflict | Clean |
| Non-ghost appendix | No | No | No | Yes (new) |

---

### Ghost Passes (S1) — The Critical Dimension

| Finding | Legacy | v1 | v2 | v3 |
|---------|--------|----|----|-----|
| RAG `test_basic_query` `len > 0` trivially true | S1 | Missed | **Missed** | S1-1 |
| Adversarial test `"error" in result` no content check | — | S1 | — | S1-2 |
| Interfaces `"raw" in result` weak assertion | — | S1 | — | S1-3 (partial) |
| EMPTY-as-pass in live tests | S1 | — | — | In LT-001 verdict |
| IT-001 silently skippable | S1 | — | — | INFRA-5 |

- **v2's critical gap was the RAG ghost pass.** The `len(result["results"]) > 0` assertion against a populated ChromaDB is trivially true — it tests database liveness, not retrieval correctness. This was the clearest S1 in the suite.
- **v3 catches it** as S1-1 and prioritizes it P0-2. The one-line skill tweak (trivially-true assertion guidance) was sufficient.
- **v3 also finds two additional S1s** not in legacy: the adversarial test content assertion gap (S1-2) and the weak `"raw" in result` check (S1-3). Both are defensible.
- **Legacy's other two S1s** (EMPTY-as-pass, silent skip) are reclassified by v3 as infrastructure/verdict issues rather than ghost passes — a reasonable judgment call.

### Mock Fidelity (S2)

- **Legacy:** 3 findings, two HIGH — SSH mock never verified with `assert_called_with`, hvac mock fragility, and missing Vault happy-path.
- **v2:** 2 findings — SSH keyword arg, hvac structure.
- **v3:** Examined all four mock patterns and cleared them all with detailed evidence. Concludes "no S2 issues that would cause a test to pass when real code fails."
- **One persistent gap across v2 and v3:** Legacy's finding 2.1 (SSH mock never verified — `get_ospf()` could stop calling `execute_ssh` entirely and tests would pass) is not flagged by either v2 or v3. This is the only legacy finding that neither skill version captures.

### Coverage Gaps (S3)

All three skill-generated reports identify the same core HIGH gaps: `core/settings.py` (zero coverage), `core/inventory.py` (import-time untested), `ingest()` main function, and semaphore concurrency. v3 adds two new MEDIUM findings not in v2: unknown query within valid category (S3-7) and KeyError catch in tools (S3-8). The count difference vs legacy (10 vs 14) comes from lower-priority gaps that v3 absorbs into other sections or omits.

### UT-005 (Vault) Rating Consistency — Fixed in v3

| Report | UT-005 Verdict | Vault Happy-Path Priority | Consistent? |
|--------|---------------|--------------------------|-------------|
| Legacy | WEAK | P0 | Yes |
| v2 | GOOD | P0 | **No** — GOOD suite shouldn't need P0 |
| v3 | SOLID | P2-7 | Yes |

v3's SOLID/P2 is the most coherent rating. The suite tests 4 of 5 critical paths well (env fallback, cache, sentinel), but the happy path is missing. SOLID with a backlog item is accurate. v2's GOOD/P0 was contradictory.

### P0 Prioritization — Improved in v3

| Report | P0 Items |
|--------|----------|
| v2 | Vault happy-path test, `settings.py` test, `run_tests.sh` fix |
| v3 | Adversarial test assertion fix (S1-2), RAG basic query assertion fix (S1-1) |

v3 correctly identifies ghost passes as the highest-priority items (credibility risk — tests that pass regardless undermine the entire suite's value). Coverage gaps and infrastructure issues move to P1/P2.

### New Findings in v3 (Not in Legacy or v2)

- **INFRA-4:** No Vault `_cache` cleanup fixture in conftest — cross-module cache pollution risk
- **S3-7:** Unknown query within valid category (valid `"ospf"`, invalid `"nonexistent_query"`) untested
- **S3-8:** KeyError catch in `get_ospf()`/`get_interfaces()` not tested end-to-end
- **Appendix:** Non-ghost verification list — shows work clearing candidates, addresses the concern that v2 over-cleared without evidence

---

### Final Scorecard

| Dimension | Legacy | v1 | v2 | v3 |
|-----------|--------|----|----|-----|
| Ghost pass detection | ✅ 3/3 | ⚠️ 2/3 | ❌ 0/3 | ✅ 3/3 |
| Mock fidelity | ✅ Strong | ⚠️ Partial | ⚠️ Partial | ⚠️ Partial (SSH gap persists) |
| Coverage gaps | ✅ 14 | ⚠️ 7 | ✅ 10 | ✅ 10 |
| Security test gaps | ✅ Present | ❌ Absent | ✅ Present | ✅ Present + coverage table |
| Infrastructure issues | ✅ Present | ❌ Absent | ✅ + fix code | ✅ + fix code |
| Per-suite verdicts | ✅ Present | ❌ Absent | ✅ (one inconsistency) | ✅ Consistent |
| Traceability matrix | ✅ 28 rows | ❌ Absent | ✅ 33 rows | ✅ 30 rows |
| Recommendations | ✅ 14 items | ❌ Absent | ✅ 15 + code | ✅ 15 + code |
| Internal consistency | ✅ | ✅ | ⚠️ UT-005 conflict | ✅ |
| New findings vs legacy | — | — | 1 (SSH strict key) | 3 |

### Verdict

**v3 is the best of the four reports.** It closes v2's critical gap (RAG ghost pass), fixes the internal consistency issue (UT-005 SOLID/P2 vs v2's GOOD/P0), improves P0 prioritization (ghost passes first, not coverage gaps), adds findings neither legacy nor v2 caught, and includes a non-ghost appendix that demonstrates analytical rigor.

The only legacy finding that persists as a blind spot across all skill versions is the SSH mock call-verification gap (legacy finding 2.1). This is a narrow issue — important, but not a structural weakness in the skill.