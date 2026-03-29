# ✨ YANA • Yet Another Network Agent

[![Version](https://img.shields.io/badge/version-1.1-1a1a2e)](https://github.com/pdudotdev/YANA/releases/tag/v1.1.0)
![License](https://img.shields.io/badge/license-GPLv3-1a1a2e)
[![Last Commit](https://img.shields.io/github/last-commit/pdudotdev/YANA?color=1a1a2e)](https://github.com/pdudotdev/YANA/commits/main/)

| | |
|---|---|
| **Platforms** | ![Cisco IOS](https://img.shields.io/badge/Cisco_IOS-0d47a1) ![Cisco IOS-XE](https://img.shields.io/badge/Cisco_IOS--XE-0d47a1) ![Arista EOS](https://img.shields.io/badge/Arista_EOS-0d47a1) ![Juniper JunOS](https://img.shields.io/badge/Juniper_JunOS-0d47a1) ![Aruba AOS](https://img.shields.io/badge/Aruba_AOS-0d47a1) ![Vyatta VyOS](https://img.shields.io/badge/Vyatta_VyOS-0d47a1) ![MikroTik RouterOS](https://img.shields.io/badge/MikroTik_RouterOS-0d47a1) ![FRR](https://img.shields.io/badge/FRR-0d47a1) |
| **Transport** | ![SSH](https://img.shields.io/badge/SSH%20CLI-1565c0) ![Scrapli](https://img.shields.io/badge/Scrapli-1565c0) |
| **Integrations** | ![NetBox](https://img.shields.io/badge/NetBox-1e88e5) ![Vault](https://img.shields.io/badge/HashiCorp_Vault-1e88e5) ![MCP](https://img.shields.io/badge/MCP-1e88e5) ![ChromaDB](https://img.shields.io/badge/ChromaDB-1e88e5) ![CI/CD](https://img.shields.io/badge/CI/CD-1e88e5) |

## Table of Contents

- [Overview](#-overview)
- [What's New](#-whats-new-in-v10)
- [Tech Stack](#tech-stack)
- [Scope](#-scope)
- [Installation & Usage](#️-installation--usage)
- [MCP Tools](#-mcp-tools)
- [Usage](#-usage)
- [Knowledge Base](#-knowledge-base)
- [Project Structure](#️-project-structure)
- [QA & Ansible](#-qa--ansible)
- [Test Network Topology](#-test-network-topology)
- [Planned Upgrades](#️-planned-upgrades)
- [Repository Lifecycle](#️-repository-lifecycle)
- [Disclaimer](#-disclaimer)
- [License](#-license)
- [Collaborations](#-collaborations)

## 🔭 Overview

RAG-powered troubleshooting assistant for multi-vendor networks. 

Combines documentation retrieval (RFCs, vendor guides) with live device queries across 5+ vendors.

▫️ **Supported models:**
- [x] Haiku 4.5
- [x] Sonnet 4.6
- [x] Opus 4.6 (default, best reasoning)

▫️ **Operational Flow:**
- [x] See [**WORKFLOW.md**](metadata/workflow/WORKFLOW.md)

▫️ **Operational Guardrails:**
- [x] See [**GUARDRAILS.md**](metadata/guardrails/GUARDRAILS.md)

## ⭐ What's New in v1.0

- [x] See [**CHANGELOG.md**](CHANGELOG.md)

## Tech Stack

| Technology | Role |
|-----------|------|
| Python | Core language |
| FastMCP | MCP server exposing 8 tools |
| Claude | Reasoning, context, troubleshooting |
| LangChain | RAG pipeline (chunking, embedding, retrieval) |
| ChromaDB | Vector database for knowledge base |
| NetBox | Device inventory (hostnames, IPs, intent) |
| HashiCorp Vault | Credential management |
| Scrapli | Multi-vendor SSH transport |

## 📋 Scope

| Protocol | What's Checked |
|----------|---------------|
| **OSPF** | Adjacencies, area and area types, config, LSDB |
| **Routing** | Table, route maps, prefix lists, PBR, ACLs |
| **Interfaces** | Up/down state, expected operational status |

## 🛠️ Installation & Usage

▫️ **Prerequisites:**
- Python 3.11+
- HashiCorp Vault
- NetBox

▫️ **Step 1 - Install:**
```bash
# Create virtualenv and install dependencies
git clone https://github.com/pdudotdev/YANA
python3 -m venv yana
yana/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
yana/bin/pip install -r requirements.txt
```

▫️ **Step 2 - Vault:**

Start Vault (dev mode, lab use):
```
vault server -dev -dev-root-token-id=<your-root-token>
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=<your-root-token>
```

Or initialize and unseal an existing Vault:
```
vault operator init -key-shares=1 -key-threshold=1   # first-time setup
vault operator unseal                                  # after every restart
```

> 🔑 Save the unseal key output from `vault operator init` somewhere safe - you'll need it every time Vault restarts or seals. Without it, a sealed Vault cannot be recovered.

> ⚠️ YANA requires Vault to be **running and unsealed** before any run. If Vault is unavailable, credential lookups fall back to env vars (see `.env.example`).

Store secrets:
```
vault kv put secret/yana/router username=<user> password=<pass>
vault kv put secret/yana/netbox token=<token>
```

▫️ **Step 3 - Configure `.env`:**
- [x] See [**example**](.env.example)
```
cp .env.example .env
```

▫️ **Step 4 - Claude auth**:

**Option A** - Anthropic account:
```
claude auth login
```
**Option B** - API key via Vault.

▫️ **Step 5 - Register the MCP server:**
```
claude mcp add yana -s user -- /path/to/yana/bin/python /path/to/YANA/server/MCPServer.py
```

▫️ **Step 6 - Ingest docs into ChromaDB:**
```
yana/bin/python ingest.py
```

## 🔧 MCP Tools

| Tool | Description |
|------|-------------|
| `get_status` | Report active data sources (inventory, credentials, intent, KB) |
| `list_devices` | List inventory devices, optionally filtered by CLI style |
| `get_ospf` | Query OSPF state (neighbors, LSDB, process config) on a live device |
| `get_interfaces` | Query interface up/down status on a live device |
| `get_routing` | Query routing table, route maps, prefix lists, PBR, and ACLs on a live device |
| `query_intent` | Retrieve network design intent from NetBox or local JSON |
| `traceroute` | Trace the forwarding path from a device to a destination IP |
| `search_knowledge_base` | Search network knowledge base (RFCs, vendor guides) with optional filters |

## 🦾 Usage

```
cd /path/to/YANA
claude

> What causes OSPF neighbors to get stuck in EXSTART state?
> D1C's OSPF neighbor with A2A is in INIT — what's wrong?
> How does MikroTik handle OSPF configuration differently from Cisco?
> Which devices are ABRs in this network? What about ASBRs?
```

## 📚 Knowledge Base

- See [**docs**](docs/)

⚠️ To update the knowledge base after editing docs:
```bash
yana/bin/python ingest.py --clean
```

## 🏗️ Project Structure

```
YANA/
├── server/
│   └── MCPServer.py              # FastMCP server (8 tools)
├── tools/                        # MCP tool implementations
│   ├── ospf.py                   # get_ospf
│   ├── operational.py            # get_interfaces, traceroute
│   ├── routing.py                # get_routing
│   ├── intent.py                 # query_intent
│   ├── status.py                 # get_status
│   ├── inventory_tool.py         # list_devices
│   └── rag.py                    # search_knowledge_base
├── core/                         # Infrastructure
│   ├── vault.py                  # Vault + env var fallback
│   ├── netbox.py                 # NetBox device inventory
│   ├── inventory.py              # Device dict
│   ├── settings.py               # Credentials + SSH config
│   └── legacy/                   # JSON fallback when NetBox unavailable
│       ├── INTENT.json
│       └── NETWORK.json
├── transport/                    # SSH execution (Scrapli)
│   ├── __init__.py               # Command dispatcher + semaphore
│   └── ssh.py                    # Multi-vendor SSH executor
├── platforms/                    # Vendor CLI command mapping
│   ├── platform_map.py           # OSPF, routing, interface + traceroute commands (6 vendors)
│   └── definitions/              # Custom Scrapli definitions
├── input_models/
│   └── models.py                 # Pydantic validation (OspfQuery, KBQuery, etc.)
├── docs/                         # OSPF knowledge base (RFCs + vendor guides)
├── lab_configs/                  # Device running configs + NetBox populator
├── metadata/
│   ├── guardrails/               # Security controls documentation
│   ├── scalability/              # Planned RAG optimizations
│   ├── topology/                 # Test network diagram
│   └── workflow/                 # RAG pipeline walkthrough
├── skills/
│   ├── ospf/                     # OSPF skill file for specific troubleshooting
│   └── routing/                  # Routing skill file for path selection issues
├── ansible/                      # Network QA health checks (NETCONF + Ansible)
│   ├── playbooks/                # network_qa.yml entry point + _run_check.yml
│   ├── test_cases/               # YAML test definitions (route checks, health checks)
│   ├── results/                  # JSON test results (used by /qa skill)
│   ├── inventory/                # Lab device inventory (E1C, C1J)
│   └── collections/              # Ansible collections (netcommon, community.general)
├── testing/
│   ├── automated/                # Unit + integration tests (169 test functions)
│   ├── live/                     # Live lab tests (65 parametrized runs) + results report
│   └── run_tests.sh              # Test runner (--live for lab tests)
├── ingest.py                     # RAG ingestion pipeline
├── CLAUDE.md                     # Troubleshooting workflow + tool reference
├── TOPOLOGY.yml                  # Containerlab topology definition
├── CHANGELOG.md                  # Version history
├── LICENSE
├── requirements.txt
└── README.md
```

## 🧪 QA & Ansible

Network QA health checks run via Ansible playbooks that query device state over NETCONF and assert expected conditions (route presence, protocol state) against design intent.

**Prerequisites:**
- `ansible-core` and `ncclient` installed in the venv (both included in `requirements.txt`)
- Ansible collections (netcommon, hashi_vault):
  ```bash
  cd ansible && ansible-galaxy collection install -r collections/requirements.yml
  ```
- HashiCorp Vault running and unsealed with credentials at `secret/yana/router` (`username`, `password`)
- `VAULT_ADDR` and `VAULT_TOKEN` env vars exported
- NETCONF-capable lab devices (IOS-XE, JunOS) reachable on port 830

**Running tests:**
```bash
cd ansible
ansible-playbook playbooks/network_qa.yml                              # all checks
ansible-playbook playbooks/network_qa.yml -e scenario_filter=route_to_a2a  # single check
```

Results are written to `ansible/results/results_<timestamp>.json`.

**Investigating failures:**

Use the `/qa` skill in Claude to load the latest results, list failures, and run a guided investigation using YANA's live OSPF and routing tools:
```
claude
> /qa
```

## 🔄 Test Network Topology

▫️ **Network diagram:**

![topology](metadata/topology/DBL-TOPOLOGY.png)

▫️ **Lab environment:**
- [x] 16 devices defined in [**TOPOLOGY.yml**](TOPOLOGY.yml)
- [x] 5 × Cisco IOS nodes
- [x] 3 × Cisco IOS-XE nodes
- [x] 4 × Arista cEOS nodes
- [x] 2 × MikroTik CHR nodes
- [x] 1 × Juniper JunOS node
- [x] 1 x Aruba AOS-CX node
- [x] OSPF multi-area, EIGRP, BGP
- [x] Device credentials stored in **Vault**
- [x] Network inventory and state in **NetBox**

## ⬆️ Planned Upgrades

- [ ] EIGRP and BGP support

## ♻️ Repository Lifecycle

**New features** are being added periodically (protocols, integrations, optimizations).

**Stay up-to-date**:
- [x] **Watch** and **Star** this repository

## 📄 Disclaimer

You are responsible for defining your own network intent via NetBox, building your test environment, and meeting the necessary conditions (Python 3.11+, Claude CLI/API, HashiCorp Vault, etc.).

## 📜 License

Licensed under the [**GNU General Public License v3.0**](LICENSE).

## 📧 Collaborations

Interested in collaborating?
- **Email:**
  - Reach out at [**hello@ainoc.dev**](mailto:hello@ainoc.dev)
- **LinkedIn:**
  - Let's discuss via [**LinkedIn**](https://www.linkedin.com/in/tmihaicatalin/)