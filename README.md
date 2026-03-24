# ✨ netKB — Network Knowledge Base

[![Version](https://img.shields.io/badge/ver.-1.3.0-1a1a2e)](https://github.com/pdudotdev/dblCheck/releases/tag/1.3.0)
![License](https://img.shields.io/badge/license-BSL1.1-1a1a2e)
[![Last Commit](https://img.shields.io/github/last-commit/pdudotdev/dblCheck?color=1a1a2e)](https://github.com/pdudotdev/dblCheck/commits/main/)

| | |
|---|---|
| **Platforms** | ![Cisco IOS](https://img.shields.io/badge/Cisco_IOS-0d47a1) ![Cisco IOS-XE](https://img.shields.io/badge/Cisco_IOS--XE-0d47a1) ![Arista EOS](https://img.shields.io/badge/Arista_EOS-0d47a1) ![Juniper JunOS](https://img.shields.io/badge/Juniper_JunOS-0d47a1) ![Aruba AOS](https://img.shields.io/badge/Aruba_AOS-0d47a1) ![Vyatta VyOS](https://img.shields.io/badge/Vyatta_VyOS-0d47a1) ![MikroTik RouterOS](https://img.shields.io/badge/MikroTik_RouterOS-0d47a1) ![FRR](https://img.shields.io/badge/FRR-0d47a1) |
| **Transport** | ![SSH](https://img.shields.io/badge/SSH%20CLI-1565c0) ![Scrapli](https://img.shields.io/badge/Scrapli-1565c0) |
| **Integrations** | ![NetBox](https://img.shields.io/badge/NetBox-1e88e5) ![Vault](https://img.shields.io/badge/Vault-1e88e5) ![MCP](https://img.shields.io/badge/MCP-1e88e5) ![CICD](https://img.shields.io/badge/CI/CD-1e88e5) |

## 🔭 Overview
RAG-powered OSPF troubleshooting assistant for multi-vendor networks. Combines documentation retrieval (RFCs + vendor guides + network intent) with live device queries across 5+ vendors.

## Architecture

```
User question (Claude Code)
         |
    CLAUDE.md skill (OSPF investigation workflow)
         |
         +---> search_knowledge_base  -->  ChromaDB (OSPF docs + intent + inventory)
         +---> get_ospf               -->  Live devices via SSH
         +---> get_interfaces         -->  Live devices via SSH
```

## Tech Stack

| Technology | Role |
|-----------|------|
| Python | Core language |
| FastMCP | MCP server exposing 3 tools |
| Claude Code + CLAUDE.md | OSPF investigation skill |
| LangChain | RAG pipeline (chunking, embedding, retrieval) |
| ChromaDB | Vector database for OSPF knowledge base |
| HuggingFace Embeddings | Local embedding model (all-MiniLM-L6-v2) |
| NetBox | Device inventory (hostnames, IPs, platforms) |
| HashiCorp Vault | Credential management |
| Scrapli | Multi-vendor SSH transport |

## Supported Vendors

- Cisco IOS / IOS-XE
- Arista EOS
- Juniper JunOS
- Aruba AOS-CX
- MikroTik RouterOS 7

## Setup

```bash
# Create virtualenv and install dependencies
python3 -m venv netkb
netkb/bin/pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Ingest OSPF docs into ChromaDB
netkb/bin/python ingest.py

# Register MCP server with Claude Code
claude mcp add netkb -s user -- /path/to/netkb/bin/python /path/to/netKB/server/MCPServer.py
```

## Usage

```
cd /path/to/netKB
claude

> What causes OSPF neighbors to get stuck in EXSTART state?
> D1C's OSPF neighbor with A2A is in INIT — what's wrong?
> How does MikroTik handle OSPF configuration differently from Cisco?
> Which devices are ABRs in this network?
```

## Knowledge Base

**OSPF Documentation** (`docs/`):
- `rfc2328_summary.md` — OSPF protocol reference (state machine, LSAs, area types, timers)
- `rfc3101_nssa.md` — NSSA reference (Type 7, P-bit, translator election)
- `vendor_cisco_ios.md` — Cisco IOS/IOS-XE OSPF specifics
- `vendor_arista_eos.md` — Arista EOS OSPF specifics
- `vendor_juniper_junos.md` — Juniper JunOS OSPF specifics
- `vendor_aruba_aoscx.md` — Aruba AOS-CX OSPF specifics
- `vendor_mikrotik_ros.md` — MikroTik RouterOS 7 OSPF specifics

**Network Context** (`core/legacy/`):
- `INTENT.json` — Network design intent (OSPF areas, roles, links, subnets)
- `NETWORK.json` — Device inventory (hostnames, management IPs, platforms)

To update the knowledge base after editing docs:
```bash
netkb/bin/python ingest.py --clean
```

## Project Structure

```
netKB/
├── server/MCPServer.py       # FastMCP server (3 tools)
├── tools/                    # MCP tool implementations
│   ├── ospf.py               # get_ospf
│   ├── operational.py        # get_interfaces
│   └── rag.py                # search_knowledge_base
├── core/                     # Infrastructure
│   ├── vault.py              # Vault + env var fallback
│   ├── netbox.py             # NetBox device inventory
│   ├── inventory.py          # Device dict
│   ├── settings.py           # Credentials + SSH config
│   └── legacy/               # Network context (ingested into ChromaDB)
│       ├── INTENT.json
│       └── NETWORK.json
├── transport/                # SSH execution
├── platforms/                # Vendor CLI command mapping
├── input_models/models.py    # Pydantic validation
├── ingest.py                 # RAG ingestion pipeline
├── CLAUDE.md                 # OSPF investigation skill
└── docs/                     # OSPF knowledge base
```
