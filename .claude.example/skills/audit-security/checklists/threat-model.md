# Threat Model — netKB

Use this during Phase 3 and Phase 8 (self-challenge). Defines the realistic threat actors, assets to protect, and STRIDE-lite analysis per component.

---

## Assets to Protect

| Asset | Value | Current protection |
|-------|-------|-------------------|
| Network device credentials | High — grants SSH access to all managed devices | Vault (primary), env vars (fallback), deny rules block .env reads |
| Device CLI access | High — read-only, but exposes network topology and configs | Pydantic validation, static command map, no run_show |
| Server availability | Medium — disruption denies network ops team their tooling | Semaphore limits concurrency, SSH timeouts, FastMCP error handling |
| Knowledge base integrity | Medium — corrupted KB gives wrong answers | Local ChromaDB, no remote write path in normal operation |
| Audit trail / observability | Low — no audit logging currently | None |

---

## Threat Actors

| Actor | Access level | Motivation | Realistic? |
|-------|-------------|------------|------------|
| **Malicious/jailbroken LLM** | Can craft arbitrary MCP tool call arguments | Exfiltrate credentials, expand scope beyond read-only queries | HIGH — any sufficiently clever prompt could achieve this |
| **Compromised NetBox** | Controls device inventory data (names, IPs, cli_style) | Redirect SSH connections, inject data into LLM context, expose wrong credentials | MEDIUM — requires internal compromise |
| **Rogue network device** | Controls SSH output content | Inject prompt-injection payloads via CLI responses | MEDIUM — requires device compromise or MITM |
| **Host-level attacker** | Filesystem and process access on the server host | Read .env directly, read ChromaDB files, read process memory | LOW — requires server compromise first; out of scope for application-layer audit |
| **Supply chain attacker** | Compromises a PyPI dependency | Arbitrary code execution in server process | LOW — requires compromising a maintained package; note lack of lockfile |
| **External network attacker** | No access beyond what the MCP transport exposes | Depends on MCP server network exposure (localhost vs all interfaces) | LOW if localhost-only; MEDIUM if exposed on network |

---

## STRIDE-Lite Analysis

### Spoofing
| Component | Risk | Notes |
|-----------|------|-------|
| MCP client identity | No authentication on MCP server | Any process that can reach the MCP socket can call tools. If MCP socket is exposed beyond localhost, this is a real risk. |
| NetBox data | No validation of NetBox responses | A compromised NetBox could supply fake device records |

### Tampering
| Component | Risk | Notes |
|-----------|------|-------|
| ChromaDB files | On-disk, no integrity check | If `data/chroma/` is writable by an attacker, KB content can be poisoned |
| NetBox device records | No integrity check on consumed data | Poisoned device records affect SSH targeting and credential lookup |
| MCP tool arguments | LLM-generated | Covered by Pydantic validation; assess bypass paths |

### Repudiation
| Component | Risk | Notes |
|-----------|------|-------|
| Tool calls | No audit log of MCP tool invocations | No record of which device was queried, when, or by which session |
| Device access | SSH connections logged at WARNING level only | No structured audit trail |

### Information Disclosure
| Component | Risk | Notes |
|-----------|------|-------|
| Error messages | May contain device names, IPs, and internal path info | Attacker-controlled device name appears in error response |
| .env file | Deny rules protect against Claude reading it | Assess whether all read paths are blocked |
| CI logs | Test output could include secrets if mocked values match real patterns | Check CI pipeline |

### Denial of Service
| Component | Risk | Notes |
|-----------|------|-------|
| Semaphore exhaustion | 5 concurrent SSH slots; no acquisition timeout | 5 slow/stalled connections block all new tool calls indefinitely |
| Blocking sync in event loop | ChromaDB/HuggingFace calls block the loop | One RAG query could delay all concurrent SSH operations |
| NetBox at startup | NetBox down = empty inventory until restart | Intentional disruption of NetBox at startup time denies all device queries |

### Elevation of Privilege
| Component | Risk | Notes |
|-----------|------|-------|
| Read-only policy | Behavioral control only (CLAUDE.md instruction) | No code-level enforcement prevents a jailbroken LLM from requesting write-like actions in future tool extensions |
| No run_show tool | Code-enforced (tool simply does not exist) | Strong control — cannot be bypassed through prompt injection |
