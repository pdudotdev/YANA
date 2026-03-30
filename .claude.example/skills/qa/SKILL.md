---
name: qa
description: "Load the latest network QA results (JUnit XML), list failures, and investigate."
context: fork
---

# /qa — Network QA Failure Investigation

## Step 1 — Load results

Find the most recently modified `.xml` file in `results/`. Read it.

If no file exists, tell the user:
> No results found in `results/`. Run your tests and place JUnit XML results there.
Then stop.

## Step 2 — Parse JUnit XML

Parse the XML structure:
- Each `<testcase>` is one test scenario. The `name` attribute is the scenario name.
- `<properties>` contain key-value pairs: `device`, `rfc_ref`, `description`.
- A `<testcase>` with a `<failure>` child is a failed test. The `message` attribute and text content describe the failure.
- A `<testcase>` without `<failure>` is a pass.

## Step 3 — Triage

Count passes and failures from the parsed XML.

If all tests passed, tell the user:
> All N scenarios passed. No failures to investigate.
Then stop.

## Step 4 — Present failures

Print a summary of all results, then a numbered list of failures:

```
Network QA — N passed, M failed

Failures:
  1. <scenario>   device=<device>   <rfc_ref>   <description>
  2. <scenario>   device=<device>   <rfc_ref>   <description>

Which failure would you like to investigate? (number or name)
```

Wait for the user's response. If only one failure exists, ask anyway — the user may want to skip it.

## Step 5 — Investigate the selected failure

### 5a — Understand the test
Read the `<properties>` from the selected `<testcase>` for device, RFC reference, and description.

### 5b — Load design intent
```
query_intent()
```
Understand the expected topology, roles, and protocol configuration for the relevant devices.

### 5c — Follow the protocol skill decision tree
Load the relevant skill file (`skills/ospf/SKILL.md`, `skills/routing/SKILL.md`) and follow its diagnostic tree. At each step in the tree, call the appropriate MCP tools (`get_ospf`, `get_routing`, `get_interfaces`, `traceroute`) and `search_knowledge_base` as needed. The skill dictates what to query — live device data and KB searches happen inline as the tree is walked, not as separate phases.

Start with the device under test, then work outward toward likely causes. Let the live data guide which branch to follow next.

## Step 6 — Report and loop

Produce a concise report for the investigated failure:

1. **Scenario**: what was checked and what was expected
2. **Observed**: what the test failure message showed
3. **Current state**: live device state (table of findings per device)
4. **Root cause**: one clear sentence with RFC citation
5. **RFC basis**: the protocol rule that explains the failure
6. **Recovery status**: is the network still broken or has it been fixed?

**IMPORTANT — always loop back.** After the report, if there are remaining uninvestigated failures, you MUST immediately re-present the remaining failure list and ask the user to pick the next one — do not wait for the user to ask. The user acknowledging a fix ("ok", "got it", "I'll do that") is NOT a signal to stop. Only stop looping if the user explicitly declines (e.g. "that's all", "no more", "skip the rest") or all failures have been investigated.

After investigating a failure, if its root cause likely explains other failures still on the list, say so — the user may choose to skip those.
