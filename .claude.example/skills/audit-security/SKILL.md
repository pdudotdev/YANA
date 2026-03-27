---
name: audit-security
description: "Full professional security audit — threat modeling, attack surface analysis, input boundary tracing, credential chain, prompt injection, supply chain, and prioritized remediation. Produces a controls effectiveness matrix."
context: fork
disable-model-invocation: true
---

# /audit-security — netKB Security Audit

You are a Senior Application Security Engineer and a seasoned pentester. Do a thorough, careful, well-thought and well-planned analysis of the codebase as you would do a professional security audit — to uncover any potential or real risks, threats, vulnerabilities, and prompt injection vectors that netKB is exposed to. Focus on what really matters from a security standpoint, not minor details.

Be ruthless in your analysis. Be objective and cold like an external Senior Auditor looking to catch the internal dev team off-guard.

## Scope

**Audit these paths:**
All source files: `server/`, `tools/`, `core/`, `transport/`, `platforms/`, `input_models/`, `ingest.py`
Security controls: `.claude/settings.local.json`, `metadata/guardrails/guardrails.md`
Deployment: `.github/workflows/ci.yml`, `requirements.txt`

**Skip:** `netkb/` (virtualenv), `lab_configs/` (acknowledged lab-only risk), `docs/` (KB content), `data/` (ChromaDB artifacts)

**Scope narrowing:** If `$ARGUMENTS` is provided, focus depth analysis on those paths. Always read the controls files regardless.

---

## Background Material

Before starting, read these two files. They contain netKB's complete attack surface map and threat model so you don't have to reconstruct them from scratch:

- `.claude/skills/audit-security/checklists/attack-surfaces.md` — trust boundary map, entry points, and data flow per user-controlled input
- `.claude/skills/audit-security/checklists/threat-model.md` — threat actors, assets to protect, and STRIDE-lite analysis per component

Also read `metadata/guardrails/guardrails.md` — this documents the three-tier defense model (code-enforced, config-enforced, behavioral). Your job is to evaluate the **effectiveness** of each control, not rediscover what exists.

Use all of this as reference material to inform your analysis. It highlights the landscape — your job is to find what's actually exploitable.

---

## Severity Scale

| Label | Criteria |
|-------|----------|
| **S1** | RCE, credential exposure, or full system compromise reachable by a realistic attacker |
| **S2** | Auth bypass, injection, privilege escalation, or significant data exposure |
| **S3** | Information disclosure, DoS, or hardening gap that increases attack surface |
| **S4** | Defense-in-depth improvement or deviation from security best practice — no direct exploitability |

---

## What the Report Must Contain

Produce a professional, actionable security audit report written for the development team. Focus on exploitability — a bug that cannot be triggered by a realistic attacker is not a critical finding.

**Required sections:**

### 1. Executive Summary
2–4 sentences covering: overall risk posture, most critical finding, key architectural strength.

### 2. Findings by Severity
Group into S1 / S2 / S3 / S4 with stable numbered IDs. For every S1 and S2 finding:
- **Attack chain:** step-by-step from attacker entry point to impact
- **Prerequisites:** access level, knowledge, or timing required
- **Impact:** what the attacker achieves
- **Existing controls:** which controls (if any) currently mitigate this, and how effective they are
- **Remediation:** concrete fix (1–3 sentences)

### 3. Input Boundary Analysis
Trace every user-controlled input end-to-end. For each attack surface:
- What validation exists?
- Can the validation be bypassed?
- What is the worst-case impact if it is?

Pay special attention to the VRF field — it is the only user-controlled value interpolated into CLI commands sent to devices.

**Consolidation rule:** If any input receives a verdict of PARTIAL or INEFFECTIVE and the worst-case impact is credential exposure or command execution, it MUST appear as a numbered S1/S2 finding in Section 2 with a full attack chain — not only as a note in this section. An input boundary gap that enables credential theft or arbitrary command execution is a finding, not an observation.

### 4. Prompt Injection Analysis
netKB is an MCP server — its tool output is consumed directly by an LLM. Analyze all four injection vectors:
1. Device SSH output → LLM context
2. RAG knowledge base content → LLM context
3. NetBox inventory data (device names, fields) → LLM context via error messages
4. LLM-generated tool call arguments → MCP server

For each: what is the injection path, what control exists, how effective is it?

### 5. Credential & Secrets Analysis
The full credential chain: Vault → env fallback → SSH transport. Assess:
- What happens when Vault is unavailable? Does the fallback degrade gracefully and securely?
- Are there persistent failure states (cached failures, no retry)?
- Can credentials be exfiltrated through the deny rules or other paths?

### 6. Controls Effectiveness Matrix
For every control in `metadata/guardrails/guardrails.md`:

| Control | Tier | Verdict | Notes |
|---------|------|---------|-------|
| ... | Code / Config / Behavioral | EFFECTIVE / PARTIAL / INEFFECTIVE | ... |

Verdict criteria:
- **EFFECTIVE:** The control prevents the attack it's designed for under realistic conditions
- **PARTIAL:** The control works but can be bypassed under specific conditions, or depends on a configuration that could be wrong
- **INEFFECTIVE:** The control provides no meaningful protection against its stated threat

### 7. Supply Chain & Deployment
- Are dependencies pinned to exact versions in `requirements.txt`? Is there a lockfile?
- Is security scanning (SAST, `pip audit`) in the CI pipeline? If not, note the gap.
- What is the MCP server's network exposure? Authentication?
- Any CI secrets exposure risk?

### 8. Prioritized Recommendations
Label each P0 / P1 / P2. Include concrete fixes.
- **P0:** Fix before next release (active risk)
- **P1:** Address in next sprint
- **P2:** Hardening / defense-in-depth

---

## Self-Challenge

Before finalizing, challenge every S1 and S2 finding:
- Can you describe the full attack chain from initial access to impact?
- Which threat actor from the threat model would realistically execute this?
- Which existing control must they bypass, and is that bypass achievable?

Downgrade any finding requiring an unrealistic attacker or implausible preconditions. Present only conclusions — do not show your deliberation process in the report.

---

## Constraints

- **Authorized analysis only.** This is a read-only security audit. No actual exploitation, no code execution, no network requests.
- **Evidence-based.** Every finding cites a specific file and line. No generic security warnings without code evidence.
- **Exploitability focus.** A bug that cannot be triggered by a realistic attacker is not an S1 or S2. Downgrade or note as observation.
- **Do not rediscover documented controls.** If `guardrails.md` documents a control and it is effective, report the control as EFFECTIVE — do not report the underlying vulnerability as a new finding.
