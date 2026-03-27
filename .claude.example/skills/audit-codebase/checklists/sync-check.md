# Component Synchronization Checklist — netKB

Use this during Phase 7. For each check, verify the cross-module contract holds. Report PASS or FAIL with evidence (file:line).

---

## 1. Tool Registrations ↔ Implementations

`server/MCPServer.py` registers 3 tools. Verify each registration points to a real, importable function:

| Registration | Expected implementation | Match? |
|-------------|------------------------|--------|
| `name="search_knowledge_base"` | `tools.rag.search_knowledge_base` | |
| `name="get_ospf"` | `tools.ospf.get_ospf` | |
| `name="get_interfaces"` | `tools.operational.get_interfaces` | |

Also check:
- Are there functions in `tools/` that are NOT registered? (stale code)
- Are there registrations referencing functions that no longer exist? (broken import)

---

## 2. PLATFORM_MAP Keys ↔ cli_style Values

PLATFORM_MAP defines these cli_styles: `ios`, `eos`, `junos`, `aos`, `routeros`, `vyos`

| Source | cli_style values | All 6 present? |
|--------|-----------------|----------------|
| `platforms/platform_map.py` PLATFORM_MAP keys | ios, eos, junos, aos, routeros, vyos | baseline |
| `testing/automated/conftest.py` MOCK_DEVICES | R1→ios, R2→eos, R3→junos, R4→aos, R5→routeros, R6→vyos | |
| `TOPOLOGY.yml` device definitions | Map kind→cli_style: cisco_iol→ios, arista_ceos→eos, etc. | |

---

## 3. OSPF Query Enum ↔ PLATFORM_MAP Subkeys

`OspfQuery.query` Literal allows exactly: `neighbors`, `database`, `borders`, `config`, `interfaces`, `details`

For each cli_style, verify all 6 query types are defined under `PLATFORM_MAP[cli_style]["ospf"]`:

| cli_style | neighbors | database | borders | config | interfaces | details |
|-----------|:---------:|:--------:|:-------:|:------:|:----------:|:-------:|
| ios | | | | | | |
| eos | | | | | | |
| junos | | | | | | |
| aos | | | | | | |
| routeros | | | | | | |
| vyos | | | | | | |

Any missing cell is a FAIL — a valid tool call would raise a KeyError at runtime.

---

## 4. Vendor Literals ↔ Ingest Metadata

`KBQuery.vendor` allows: `cisco_ios`, `arista_eos`, `juniper_junos`, `aruba_aoscx`, `mikrotik_ros`

`ingest.py::extract_metadata()` derives vendor from filename prefix (e.g., `vendor_cisco_ios.md` → `cisco_ios`).

Check: Do the actual filenames in `docs/` produce vendor strings matching the `KBQuery.vendor` Literal?

Note: `KBQuery.vendor` does NOT include `vyos`. Is there a `docs/vendor_vyos.md`? If so, it's ingested but can never be filtered by vendor — potential gap.

---

## 5. CLAUDE.md Accuracy

| CLAUDE.md claim | Code reality | Match? |
|-----------------|-------------|--------|
| Tool name: `search_knowledge_base` | MCPServer.py registration | |
| Tool name: `get_ospf` | MCPServer.py registration | |
| Tool name: `get_interfaces` | MCPServer.py registration | |
| Vendor filter: `cisco_ios` | KBQuery.vendor Literal | |
| Vendor filter: `arista_eos` | KBQuery.vendor Literal | |
| Vendor filter: `juniper_junos` | KBQuery.vendor Literal | |
| Vendor filter: `aruba_aoscx` | KBQuery.vendor Literal | |
| Vendor filter: `mikrotik_ros` | KBQuery.vendor Literal | |
| Topic filter: `rfc` | KBQuery.topic Literal | |
| Topic filter: `vendor_guide` | KBQuery.topic Literal | |
| Topic filter: `intent` | KBQuery.topic Literal | |
| Topic filter: `inventory` | KBQuery.topic Literal | |
| Skill file: `skills/ospf/SKILL.md` | File exists at that path | |
