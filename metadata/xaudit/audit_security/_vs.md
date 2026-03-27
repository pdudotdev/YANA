## Legacy security audit: Basic agent prompt
```
(same model, effort, plan mode approach as the testing audit)
You are a Senior Application Security Engineer and a seasoned pentester.
Please do a thorough, careful, well-thought and well-planned analysis of the codebase as you would do a professional security audit to uncover any potential or real risks, threats, vulnerabilities, prompt injections etc. that netKB is exposed to. Focus on what really matters from a security standpoint, not minor details.

After your analysis is fully done: read it, challenge it and your own judgement and assumptions regarding any important findings in order to double check if there's really an issue or not.

CRUCIAL! Be ruthless in your analysis, be objective and cold like an external Senior Auditor looking to catch the internal dev team off-guard.
```

## Upgraded security audit: Skills and checklists
See `.claude.example/skills/audit-security/`.
> Run `/audit-security` in the Claude Code CLI.

## Results
- `legacy_report.md` — generated with an unstructured security audit prompt
- `upgraded_report1.md` — v1, first `/audit-security` skill run

**Note:** Both reports were generated with Opus 4.6, Effort High, Plan Mode, fresh context.

---

## Evaluation: Legacy vs. v1

### Report Versions

| Version | Source | File | Lines | Findings | Severity Scheme |
|---------|--------|------|-------|----------|-----------------|
| Legacy | Unstructured security audit prompt | `legacy_report.md` | 268 | 9 (2H, 4M, 3L) | HIGH / MEDIUM / LOW |
| v1 | First `/audit-security` skill run | `upgraded_report1.md` | 342 | 11 (0 S1, 2 S2, 6 S3, 3 S4) | S1 / S2 / S3 / S4 |
| v2 | `/audit-security` with consolidation heuristic | `upgraded_report2.md` | 437 | 13 (0 S1, 3 S2, 5 S3, 5 S4) | S1 / S2 / S3 / S4 |

---

### Overview

| Dimension | Legacy | v1 | v2 |
|-----------|--------|----|----|
| Critical/High findings detected | 2 HIGH | 2 S2, 0 S1 | 3 S2, 0 S1 |
| F2 (NetBox host poisoning → credential theft) | Standalone HIGH, full attack chain | Scattered: S2-02 describes different attack; host only PARTIAL note; fix at P2 | ✅ Standalone S2-3, full attack chain, INEFFECTIVE verdict |
| Total unique findings | 9 | 11 | 13 |
| New findings (not in prior reports) | 2 unique | 7 unique | 2 new (S2-2 cli_style Vault traversal elevated; S4-5 shutil.rmtree) |
| Input boundary analysis | Absent | 8 inputs traced (2 gaps: `platform`, `cli_style` dual path) | 9 inputs traced; all gaps closed |
| Prompt injection coverage | 2 findings (F4, F5) | 4 vectors, systematic section | 4 vectors, systematic section |
| Credential chain analysis | LOW finding (F9) | Full Vault → env var → SSH trace | Full Vault → env var → SSH trace + 4 exfiltration paths |
| Controls effectiveness evaluation | "What Gets Right" prose (7 items) | 12-control matrix with EFFECTIVE / PARTIAL / INEFFECTIVE | 17-control matrix |
| Supply chain coverage | 1 finding (F6) | Full section (deps, CI, network transport, secrets) | Full section |
| Trust boundary visualization | ASCII diagram | Absent | ✅ ASCII diagram present |
| Verification plan | 5 post-remediation tests | Absent | ✅ 5 tests present |
| Positive security findings | 7 items | Absent | Absent (implicit in controls matrix) |
| Recommendation priority accuracy | P0: F1 + F2 (both correct) | P0: S2-01 + S2-02; P2-6 for host validation (too low) | P0: VRF + SSH default; P1: host validation (one step low) |
| Internal consistency | Clean | 2 inconsistencies | Clean |
| Self-challenge reasoning | Implicit | Explicit (S1 rationale shown) | Implicit |

---

### F2 (NetBox Host Poisoning → Credential Theft) — The Critical Dimension

This is the most consequential difference between the two reports. Legacy F2 is the second-most dangerous attack chain in the codebase. Its handling in v1 is the clearest regression.

**Legacy's F2 attack chain:**
1. Attacker compromises NetBox (or has write access to device records — the threat model's primary vector, rated MEDIUM likelihood)
2. Attacker sets a device's `primary_ip` to an attacker-controlled IP
3. netKB reads `dev.primary_ip.address.split("/")[0]` at `netbox.py:41` with no validation — no network prefix check, no allowlist, no IP format verification
4. The attacker IP is passed directly to Scrapli at `ssh.py:50`: `Cli(host=device["host"], ...)`
5. With `SSH_STRICT_HOST_KEY` defaulting to `False`, no host key verification occurs
6. The MCP server SSHes to the attacker's machine; the attacker's SSH server receives the plaintext password in the RFC 4252 password authentication handshake

**Why this matters:** The attacker needs only NetBox write access — no network positioning, no MITM. The threat model explicitly rates NetBox compromise as MEDIUM likelihood. Legacy correctly classified this as HIGH and flagged it P0.

**What v1 produces instead:**

- **S2-02** describes "An attacker positioned on the network path between the netKB server and a managed device performs an SSH man-in-the-middle attack." This is a different attack with a different prerequisite (network positioning, not just NetBox write access). S2-02 addresses the insecure default; it does not address the host poisoning chain.
- **Input Boundary Analysis** for the `host` field: "A compromised NetBox could redirect SSH connections to an attacker-controlled host, capturing credentials." Verdict: PARTIAL. This is the legacy F2 attack in a sentence — but it has no finding number, no attack chain, and receives a PARTIAL verdict rather than triggering a standalone HIGH finding.
- **P2-6**: "Validate NetBox `host` field as IP address" — priority P2. Legacy had the fix at P0.

A reader of v1 who trusts its prioritized recommendations would implement P0-1 (VRF validation) and P0-2 (SSH default) and consider themselves protected. They would not see P2-6 as urgent. The most straightforward credential theft path — NetBox compromise, no MITM — is effectively buried.

**Compounding factors from F2 that v1 partially or fully drops:**

| F2 Component (Legacy) | v1 Coverage |
|---|---|
| `primary_ip` → SSH host poisoning | Mentioned in Input Boundary (no finding ID, P2 fix) |
| `cli_style` → Vault path construction | Analyzed in Credential section; traversal dismissed with reasoning (Vault ACLs + hvac opaque paths). Analysis is deeper than legacy. |
| `platform` → Scrapli `definition_file_or_name` | Not mentioned in Input Boundary Analysis at all. `ssh.py:27` passes an unknown platform string as-is to Scrapli. |

The `cli_style` dismissal in v1 is arguably the one case where v1 provides *better* analysis than legacy: it traces the actual code path (`f"netkb/router{cli_style}"` at `ssh.py:31`) and concludes that Vault ACLs and hvac's opaque path handling prevent traversal. Whether that conclusion is operationally correct depends on the Vault ACL configuration, but the analysis is substantive.

---

### Severity Calibration

| Finding | Legacy | v1 | Direction | Notes |
|---------|--------|----|-----------|-------|
| F1 / S2-01 (VRF injection) | HIGH | S2 (explicitly not S1) | Lateral | v1's self-challenge reasons: "no path to RCE, credential exposure, or full system compromise under realistic conditions." Debatable — arbitrary CLI command execution on a managed device is remote command execution on that device. The skill's S1 definition says "RCE, credential exposure, full system compromise." The downgrade is visible and reasoned, but the reasoning may be too narrow. |
| F2 / S2-02 (credential exposure) | HIGH | S2 (but different attack) | Regression | See F2 section above. v1's S2-02 is a real finding, but it is not F2. |
| F3 / S2-02 (SSH host key default) | MEDIUM | S2 | Elevation | v1 elevates because it enables credential exposure. Justified — this is a severity improvement. |
| F8 / S3-03 (exception leaks) | LOW | S3 | Elevation | Reasonable — exception leaks compound with prompt injection vectors. |
| F9 / S4-02 (credential cache TTL) | LOW | S4 | Roughly equivalent | Vault failure caching (permanent) vs process memory caching (no TTL). Both describe the same root operational risk. |

Net: severity calibration is mixed. F3 elevation is an improvement. F1 downgrade is arguable. F2 demotion is the only clear miss, and it is not a severity judgment — the attack chain was simply never consolidated into a finding.

---

### Input Boundary Analysis

Legacy had no equivalent section. v1's Input Boundary Analysis is a structural improvement — every user-controlled input is traced end-to-end with an explicit verdict. Two gaps:

**Gap 1: `platform` field not analyzed.** `ssh.py:26-27`:
```python
platform = device["platform"]
definition = _CUSTOM_DEFINITIONS.get(platform, platform)
```
If `platform` is not in `_CUSTOM_DEFINITIONS` (two known entries: `mikrotik_routeros`, `vyos_vyos`), the value is passed as-is to `Cli(definition_file_or_name=definition)`. Legacy flagged this as a compounding factor of F2. v1's Input Boundary Analysis does not mention `platform` at all.

**Gap 2: `cli_style` dual code paths.** v1 analyzes `cli_style` only as a PLATFORM_MAP dict key (verdict: EFFECTIVE through fail-closed). But `ssh.py:30-32` shows a second code path: `cli_style` is also used to construct a Vault secret path (`f"netkb/router{cli_style}"`). The Input Boundary section gives an EFFECTIVE verdict based on one path while the other is analyzed only in the Credential section. These are different code paths with different security properties.

Despite these gaps, the Input Boundary Analysis section itself is a material improvement in audit quality. Legacy identified the `host` and `cli_style` issues only incidentally through F2. v1 provides a systematic inventory.

---

### Controls Effectiveness Evaluation

| Aspect | Legacy | v1 |
|--------|--------|----|
| Format | "What Gets Right" — 7 positive findings in prose | 12-control matrix with tier (Code/Config/Behavioral), verdict, and notes |
| Systematic? | No — prose, no explicit INEFFECTIVE ratings | Yes — EFFECTIVE/PARTIAL/INEFFECTIVE for every control |
| Deny rule analysis | F7: 3 bypass methods identified | Controls matrix: 4+ bypass methods, correctly scoped to "jailbroken LLM" caveat |
| Vault coverage | Mentioned as positive (item 4) | Full section (Credential & Secrets Analysis) covering chain, fallback, failure caching, exfiltration paths |

The Controls Effectiveness Matrix is unambiguously the better artifact for an operator who needs to know which defenses are actually working. v1's analysis of the deny rules is also more thorough than legacy.

---

### Prompt Injection Coverage

| Vector | Legacy | v1 |
|--------|--------|-----|
| Device SSH output → LLM context | F4 (MEDIUM) | Vector 1 (PARTIAL, CLAUDE.md behavioral control) |
| RAG KB content → LLM context | F5 (MEDIUM) | Vector 2 (PARTIAL, two sub-vectors: local docs and NetBox config contexts) |
| NetBox inventory data → LLM via error messages | Not covered | Vector 3 (PARTIAL, narrow attack surface but no code defense) |
| LLM-generated tool arguments → MCP validation | Not covered | Vector 4 (EFFECTIVE, Pydantic + Literal enums are code-enforced) |

v1 adds two vectors not in legacy. Vector 4 in particular is an important addition — it explicitly confirms that the Pydantic layer prevents LLM-generated injection payloads from reaching dangerous operations. This closes a question that legacy left implicit.

---

### Internal Consistency

Legacy: Clean. No contradictions identified.

v1: Two inconsistencies:

1. **NetBox `host` priority mismatch.** Input Boundary Analysis rates the `host` field PARTIAL with the note "A compromised NetBox could redirect SSH connections to an attacker-controlled host, capturing credentials." The Prioritized Recommendations fix this at P2-6 (hardening). If an unvalidated host field enables credential theft from a MEDIUM-likelihood threat actor, P2 is inconsistent with the severity of the impact. The correct priority should be P0 or P1.

2. **`cli_style` analyzed in one code path only.** Input Boundary says "EFFECTIVE through fail-closed behavior" (PLATFORM_MAP dict key lookup). Credential & Secrets Analysis correctly traces the second code path (Vault path construction). Both exist in the code at `ssh.py:30-32`. The Input Boundary verdict "EFFECTIVE" covers only one of two security-relevant uses of the field.

---

### Missing Sections in v1

| Section | Legacy | v1 |
|---------|--------|----|
| Trust Boundary Map | ASCII diagram with trust levels and finding callouts | Absent |
| Verification Plan | 5 specific post-remediation tests | Absent |
| Positive Findings | 7 items (what the code gets right) | Absent |

The trust boundary map is the most significant omission. It serves as a communication artifact for operators and developers who need to understand *where* the defenses break down, not just which CVEs exist. It also provides the reference frame for understanding why F1 and F2 are different in nature from the other findings (they exploit a gap in the trust model, not implementation bugs).

---

### Final Scorecard

| Dimension | Legacy | v1 |
|-----------|--------|----|
| Critical/High finding detection | ✅ 2/2 | ⚠️ 1/2 — F2 demoted |
| Attack chain completeness | ✅ F2 full chain | ❌ F2 chain scattered, no numbered finding |
| Severity accuracy | ✅ | ⚠️ F3 elevation good, F2 demotion bad |
| Input boundary coverage | ❌ Absent | ⚠️ 8 inputs, 2 gaps (`platform`, `cli_style` dual path) |
| Prompt injection coverage | ⚠️ 2 vectors | ✅ 4 vectors, systematic |
| Credential chain analysis | ⚠️ LOW finding only | ✅ Full Vault → env → SSH trace |
| Controls effectiveness evaluation | ⚠️ Prose positives only | ✅ 12-control matrix |
| Supply chain coverage | ⚠️ 1 finding | ✅ Full section |
| Recommendation priority accuracy | ✅ P0 correct | ⚠️ Host validation at P2 (should be P0/P1) |
| Internal consistency | ✅ | ⚠️ 2 inconsistencies |
| New findings discovered | — | ✅ 7 new findings |
| Trust boundary visualization | ✅ ASCII diagram | ❌ Absent |
| Verification plan | ✅ 5 tests | ❌ Absent |
| Positive findings | ✅ 7 items | ❌ Absent |

### Verdict (Legacy vs. v1)

**Neither report is strictly superior.** They have complementary strengths and one critical divergence.

v1 is structurally superior to legacy: Input Boundary Analysis traces all user-controlled inputs end-to-end, the Controls Effectiveness Matrix provides systematic defense evaluation, Prompt Injection Analysis covers all 4 vectors, the Credential & Secrets section traces the full chain, and Supply Chain coverage is comprehensive. v1 also discovers 7 findings that legacy missed entirely. These are proper security audit artifacts; the legacy report had none of them.

However, v1 has one material regression: **legacy finding F2 (NetBox host poisoning → credential theft) is not a standalone finding.** The attack chain — compromised NetBox sets `primary_ip` to attacker IP, MCP server SSHes to attacker, credentials captured via RFC 4252 — requires only NetBox write access. It is strictly more dangerous than S2-02's network-path MITM (which requires network positioning). v1's S2-02 describes the wrong attack, the Input Boundary Analysis mentions the right attack without a finding ID or commensurate priority, and P2-6 is the only recommendation — at a priority level operators would not treat as urgent.

This parallels the testing comparison where v2 was structurally superior but missed the RAG ghost pass. The pattern is the same: structured analysis sections improve breadth but can cause severity dilution when a finding's components are distributed across sections rather than consolidated into a numbered finding.

**Recommended skill tweak:** Add a consolidation heuristic to the skill's S2 section — something like: "If any input in the Input Boundary Analysis receives a verdict of PARTIAL or INEFFECTIVE and the worst-case impact is credential exposure or command execution, it MUST appear as a numbered S1/S2 finding with a full attack chain, not only as an Input Boundary note." A one-sentence addition, analogous to the trivially-true assertion guidance that resolved v2→v3 in the testing audit.

---

## Evaluation: v1 vs. v2

**Change:** Consolidation heuristic added to skill Section 3 (`SKILL.md:76-77`). One-sentence rule: PARTIAL/INEFFECTIVE input boundary verdicts with credential-exposure or command-execution worst cases must appear as numbered S1/S2 findings with full attack chains.

---

### Primary Question: Did the consolidation rule fix the F2 regression?

**Yes.** v2's S2-3 is exactly what was missing in v1:

| Component | v1 | v2 |
|-----------|----|----|
| Finding ID | None | **S2-3** |
| Attack chain | Missing | Full 4-step chain: NetBox compromise → attacker sets `primary_ip` → SSH to attacker host → RFC 4252 handshake sends password |
| Impact | PARTIAL verdict buried in Input Boundary | "Full credential exposure — SSH username and password sent to attacker-controlled server during handshake" |
| Input Boundary verdict | PARTIAL | INEFFECTIVE (when SSH strict disabled, which is the default) |
| Fix priority | P2-6 | P1-4 |

The attack chain in S2-3 is clear, accurate, and correctly scoped to the NetBox threat actor (MEDIUM likelihood). The fix priority (P1) is one step below legacy's P0, but v2's reasoning is defensible: the SSH default fix (P0-3) materially mitigates S2-3, making host validation the defense-in-depth follow-up. An operator following v2's P0 list would fix the SSH default first, then validate the host field. Legacy's P0 list treated both VRF and host validation as equally urgent with no dependency ordering — also correct, just less structured.

**One remaining gap:** Host validation priority is P1, not P0. The distinction matters because the SSH default fix (P0) and host field validation (P1) together close S2-3, but an operator who only reads the P0 list and considers themselves done would still be exposed if they deploy without setting `SSH_STRICT_HOST_KEY=false` explicitly — which is now the opt-out, not opt-in. The fix ordering in v2 is logical, but the framing could more explicitly state that S2-3 is not fully remediated by the SSH default change alone.

---

### New Findings in v2

**S2-2: NetBox-sourced `cli_style` interpolated into Vault secret path without validation**

This finding was mentioned in v1's Credential section but dismissed with the reasoning that Vault ACLs and hvac's opaque path handling prevent traversal. v2 elevates it to S2 with a full attack chain. The v2 attack chain is hedged ("may resolve... depending on Vault's path normalization behavior"), which reflects genuine uncertainty. v1's dismissal was arguably more analytically rigorous on this specific point — it traced the actual hvac call and concluded traversal was blocked. However, v2's elevation is defensible as a conservative stance given that the behavior depends on Vault configuration outside the codebase.

**S4-5: `ingest.py --clean` shutil.rmtree**

Correctly identified and immediately dismissed ("No action required — this is a developer-only CLI tool"). Not a regression.

**Deny rule analysis (S4-3, S4-4)**

v2 identifies the `Bash(cp:*)` allow rule as a definitive bypass (not just a potential one), and separates the env/printenv analysis into its own S4-4 finding. Both are more specific than v1's treatment.

---

### Severity Changes from v1 to v2

| Finding | v1 | v2 | Direction | Notes |
|---------|----|----|-----------|-------|
| SSH strict host key default | S2-02 | S3-1 | Downgrade | v2 treats it as a compounding factor of S2-3 rather than standalone S2. Debatable — the SSH default enables the MITM attack chain independently of NetBox compromise. v1's S2 classification was justified. |
| NetBox host poisoning (F2) | No finding | S2-3 | ✅ Elevated | The primary regression is fixed. |
| cli_style Vault traversal | Credential section, dismissed | S2-2 | Elevated | v1's dismissal may have been more rigorous. v2's elevation is conservative but hedged. |
| VRF injection | S2-01 | S2-1 | Equivalent | Same finding, same severity, same attack chain. |

---

### Input Boundary Gaps Resolved

Both gaps identified in the v1 evaluation are closed in v2:

**`platform` field:** Now mentioned explicitly in the "Compounding factors" of S2-3: "platform from NetBox is unvalidated. `ssh.py:27` uses `_CUSTOM_DEFINITIONS.get(platform, platform)` — if not in the dict, it's passed as-is to Scrapli's `Cli()` as a `definition_file_or_name`." The P0-2 remediation also covers it: "Validate NetBox-sourced `cli_style` against PLATFORM_MAP keys."

**`cli_style` dual path:** v2 correctly handles both paths separately. The Vault path construction (`f"netkb/router{cli_style}"`) is S2-2. The PLATFORM_MAP dict key lookup is S3-1 / Input Boundary "EFFECTIVE through fail-closed."

---

### Missing Sections Recovered

| Section | Legacy | v1 | v2 |
|---------|--------|----|----|
| Trust Boundary Map | ✅ | ❌ | ✅ |
| Verification Plan | ✅ | ❌ | ✅ |
| Positive Findings | ✅ 7 items | ❌ | ❌ (implicit in controls matrix EFFECTIVE rows) |

Trust Boundary Map and Verification Plan are back. Positive Findings remains absent as a standalone section. The controls matrix provides equivalent information in a structured form — an operator reading the EFFECTIVE rows gets the same picture, but less prominently.

---

### Final Scorecard

| Dimension | Legacy | v1 | v2 |
|-----------|--------|----|----|
| Critical/High finding detection | ✅ 2/2 | ⚠️ 1/2 — F2 demoted | ✅ 3/3 (F2 fixed + cli_style elevated) |
| Attack chain completeness | ✅ F2 full chain | ❌ F2 chain scattered | ✅ S2-3 full chain |
| Severity accuracy | ✅ | ⚠️ F3 elevation good, F2 demotion bad | ⚠️ SSH default downgrade debatable; cli_style elevation possibly aggressive |
| Input boundary coverage | ❌ Absent | ⚠️ 8 inputs, 2 gaps | ✅ 9 inputs, gaps closed |
| Prompt injection coverage | ⚠️ 2 vectors | ✅ 4 vectors, systematic | ✅ 4 vectors, systematic |
| Credential chain analysis | ⚠️ LOW finding only | ✅ Full Vault → env → SSH trace | ✅ Full trace + 4 exfiltration paths |
| Controls effectiveness evaluation | ⚠️ Prose positives only | ✅ 12-control matrix | ✅ 17-control matrix |
| Supply chain coverage | ⚠️ 1 finding | ✅ Full section | ✅ Full section |
| Recommendation priority accuracy | ✅ P0 correct | ⚠️ Host validation at P2 | ⚠️ Host validation at P1 (one step low but defensible) |
| Internal consistency | ✅ | ⚠️ 2 inconsistencies | ✅ Clean |
| New findings discovered | — | ✅ 7 new findings | ✅ 2 additional new findings |
| Trust boundary visualization | ✅ ASCII diagram | ❌ Absent | ✅ Present |
| Verification plan | ✅ 5 tests | ❌ Absent | ✅ Present |
| Positive findings | ✅ 7 items | ❌ Absent | ⚠️ Implicit only |

### Verdict (v2)

**v2 is the best of the three reports.** The consolidation heuristic worked as intended. The primary regression (F2 scattered, no numbered finding, P2 priority) is resolved: S2-3 is a standalone finding with a complete attack chain and an INEFFECTIVE verdict on the input boundary. The two structural sections that v1 dropped (Trust Boundary Map, Verification Plan) are back. All input boundary gaps are closed.

The only remaining items of note:
1. **Host validation priority (P1 vs. P0):** The dependency-ordered P0/P1 split is internally consistent, but could more explicitly state that S2-3 is only partially mitigated by the SSH default change alone.
2. **SSH default severity (S3 vs. S2):** v2's downgrade from v1's S2-02 is debatable — the SSH default enables the MITM attack independently of NetBox compromise. v1's S2 classification was arguably correct.
3. **cli_style Vault traversal (S2-2):** v2 elevates where v1 dismissed. Conservatively correct, but v1's analysis was more rigorous on this specific point.
4. **Positive findings section:** Still absent as standalone. Minor — controls matrix covers it implicitly.

None of these are material regressions. A practitioner following v2's P0 list would correctly remediate the most dangerous attack chains first.
