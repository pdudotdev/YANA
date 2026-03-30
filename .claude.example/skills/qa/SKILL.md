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
- `<properties>` contain key-value pairs: `device`, `rfc_ref`, `description`, `rfc_citation`.
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
If a matching test case YAML exists in `ansible/test_cases/`, read it for additional context (optional).

### 5b — Load design intent
```
query_intent()
```
Understand the expected topology, roles, and protocol configuration for the relevant devices.

### 5c — Gather live state
Query the device(s) from the `device` property using the appropriate YANA tools (`get_ospf`, `get_routing`, `get_interfaces`, `traceroute`). Start with the device under test, then work outward toward likely causes.

### 5d — Trace the problem
Follow the diagnostic trees in the relevant skill file (`skills/ospf/SKILL.md`, `skills/routing/SKILL.md`). Let the live data guide which devices to check next.

### 5e — RFC context
```
search_knowledge_base(query="<failure-specific query>", topic="rfc")
```
Retrieve the RFC text that explains the observed behavior.

## Step 6 — Report and loop

Produce a concise report for the investigated failure:

1. **Scenario**: what was checked and what was expected
2. **Observed**: what the test failure message showed
3. **Current state**: live device state (table of findings per device)
4. **Root cause**: one clear sentence with RFC citation
5. **RFC basis**: the protocol rule that explains the failure
6. **Recovery status**: is the network still broken or has it been fixed?

If there are remaining uninvestigated failures, re-present the list (without the one just investigated) and ask the user to pick the next one. Repeat until all failures are investigated or the user stops.

After investigating a failure, if its root cause likely explains other failures still on the list, say so — the user may choose to skip those.
