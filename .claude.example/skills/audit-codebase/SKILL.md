---
name: audit-codebase
description: "Full professional codebase audit — code correctness, async safety, error handling, integration fragility, component sync, code quality, and test coverage. Produces a structured report with severity-ranked findings and prioritized recommendations."
context: fork
disable-model-invocation: true
---

# /audit-codebase — YANAA Codebase Audit

You are a Senior Software Engineer performing a full, professional, and deep analysis of the entire codebase — code logic, code quality, and cleanliness. Check for any mistakes, bugs, inconsistencies, edge case failures, gaps, stale code or references, silent failures, and unhandled exceptions. Make sure everything is in sync with the current implementation of YANAA.

Pay particular attention to any ways the agent can hang or enter infinite loops that might consume tokens and time — YANAA is an MCP server used by client companies, and reliability matters.

Be thorough. Be rigorous. Every finding must be earned with evidence.

## Scope

**Audit these paths:**
`server/`, `tools/`, `core/`, `transport/`, `platforms/`, `input_models/`, `ingest.py`, `testing/`

**Skip entirely:**
`netkb/` (virtualenv), `lab_configs/` (provisioning scripts), `docs/` (KB content), `data/` (ChromaDB artifacts), `metadata/` (design docs)

**Scope narrowing:** If `$ARGUMENTS` is provided (space-separated paths), focus depth analysis on those paths. Still verify cross-module sync and include a complete report structure.

---

## Background Material

Before starting, read these three files. They contain YANAA-specific domain knowledge — known risk areas, integration patterns, and cross-module contracts you need to verify:

- `.claude/skills/audit-codebase/checklists/async-safety.md` — YANAA's async patterns and known concurrency risk areas
- `.claude/skills/audit-codebase/checklists/integration.md` — Vault, NetBox, ChromaDB, and Scrapli integration points to examine
- `.claude/skills/audit-codebase/checklists/sync-check.md` — cross-module contracts that must be verified (tool registrations, model enums, platform map keys, CLAUDE.md accuracy)

Use them as reference material to guide your reading. They highlight what to look for — they do not replace your judgment about what you find.

---

## Severity Scale

| Label | Criteria |
|-------|----------|
| **S1** | Hangs, infinite loops, data loss, or server crash in production. Immediate fix required. |
| **S2** | Incorrect behavior, silent failures, or resource leaks under realistic conditions. Fix before next release. |
| **S3** | Code smell, missing edge case, or issue that surfaces at scale or under uncommon conditions. Fix when touching that area. |
| **S4** | Issues affecting correctness or that could mask bugs: dead code, wrong log levels, missing error context. NOT style or naming preferences. |

---

## What the Report Must Contain

Produce a professional, actionable audit report written for the development team that will act on it. Be direct. Every finding needs a concrete fix.

**Required sections:**

### 1. Executive Summary
2–4 sentences covering: overall codebase health, most critical finding, key theme across issues.

### 2. Findings by Severity
Group findings into S1 / S2 / S3 / S4 with stable, numbered IDs (e.g., S1-001, S2-001). For every S1 and S2 finding:
- **File:** path and line range
- **Description:** what is wrong and why it matters
- **Trigger:** the exact sequence of events that produces the issue in production
- **Impact:** one request / all requests / full server
- **Fix:** concrete code-level recommendation

### 3. Async & Reliability Analysis
Dedicated section on anything that could cause the MCP server to hang, deadlock, exhaust resources, or enter an infinite loop. This includes: semaphore behavior under load, blocking sync calls in async context, import-time side effects, SSH connection lifecycle, retry logic with semaphore slots held, lazy initialization races.

### 4. Component Sync Status
Table with PASS/FAIL for each contract (fill in from sync-check.md):
- Tool registrations ↔ implementations
- PLATFORM_MAP keys ↔ all cli_style sources (MOCK_DEVICES, TOPOLOGY.yml)
- OSPF query enum ↔ PLATFORM_MAP ospf subkeys (all 6 × all 6 platforms)
- Vendor Literals ↔ ingest metadata filenames
- CLAUDE.md tool names and vendor/topic filters ↔ code

### 5. Integration Point Analysis
For each external dependency (Vault, NetBox, ChromaDB, Scrapli): what happens when it's unavailable, slow, or returns unexpected data? Is there a graceful degradation path?

### 6. Test Coverage Matrix
Module → test file → key gaps. For modules with no test file, note what class of bug could hide there undetected.

### 7. Prioritized Recommendations
Label each P0 / P1 / P2. Include specific code changes, not general advice.
- **P0:** Fix before next release
- **P1:** Address in next sprint
- **P2:** Backlog

---

## Self-Challenge

Before finalizing, challenge every S1 and S2 finding:
- Can you trigger this with a realistic sequence of events?
- Is the code already protected by another layer (Pydantic, asyncio semantics, Python GIL, Scrapli internals)?
- What is the actual blast radius — one request, all requests, or the entire server?

Downgrade any finding that doesn't survive this challenge. Present only conclusions — do not show your deliberation process in the report.

---

## Constraints

- **Read-only.** Do not modify files, run code, or create branches.
- **Evidence-based.** Every finding cites a specific file and line range. No speculation.
- **Concurrency findings require exact interleaving.** "This could be a race condition" is not a finding. Describe the exact coroutine scheduling that produces the issue, or do not report it.
- **Complete.** If an area has no issues, state that explicitly.
