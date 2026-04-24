---
name: bootstrap-pipeline
description: FIRST-TIME SETUP. Creates the Pipeline Intelligence Notion database from scratch and builds deep historical dossiers for every open deal. Looks back 90 days across Gong, Gmail, Calendar, and Drive. Takes longer than the weekly run but only needs to happen once. After this, use /run-forecast for weekly updates.
---

Bootstrap the pipeline intelligence system. This is the initial setup — run it once, then use /run-forecast weekly.

1. Read skills/forecasting/SKILL.md and all its reference files.
2. **CREATE THE NOTION DATABASE:** Create a new Notion database called "Pipeline Intelligence" with the schema defined in references/notion-schema.md. All properties, all select options, everything. If the database already exists, ask the user: "A Pipeline Intelligence database already exists. Do you want to wipe it and start fresh, or add any missing deals to the existing database?"
3. Execute Layer 1: Pull ALL open deals from Salesforce via Glean (stages 2-7, exclude renewals).
4. Execute Layer 2 (BOOTSTRAP MODE): For EACH deal, dispatch the **deal-bootstrapper** sub-agent (NOT the regular deal-analyzer). The bootstrapper looks back 90 days instead of 7 and builds a comprehensive initial dossier. Use sub-agents with isolated context — one per deal, parallel where possible.
5. Collect all sub-agent results.
6. Execute Layer 3: Create a Notion row for every deal. Populate all fields. Create a linked detail page for each deal with the initial assessment as the baseline entry.
7. Produce a bootstrap summary:

```
Pipeline Intelligence — Initial Setup Complete ([today's date])

Database created: [Notion link]
Deals bootstrapped: [count]
Deals by stage: [breakdown]
Total pipeline: $[total ARR]

Deals with pricing conversations found: [count]
Deals with ARR mismatches detected: [count] — [list account names]
Deals flagged for dead-out consideration: [count] — [list account names]

The system is now ready for weekly /run-forecast runs.
```
