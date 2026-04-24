---
name: run-forecast
description: Run the weekly pipeline forecast. Requires that /bootstrap-pipeline has already been run at least once (Notion database must exist). Pulls all open deals, dispatches a sub-agent per deal with 7-day lookback, reads prior Notion dossiers for context, synthesizes results, and updates Notion.
---

Run the weekly pipeline forecast using the /forecasting skill. Follow these steps exactly:

1. Read skills/forecasting/SKILL.md and all its reference files before doing anything.
2. **CHECK FOR EXISTING NOTION DATABASE:** Search Notion for a database called "Pipeline Intelligence". If it does NOT exist, STOP and tell the user: "No Pipeline Intelligence database found in Notion. Run /bootstrap-pipeline first to create the database and build initial deal dossiers. The weekly forecast requires existing dossiers to diff against."
3. Execute Layer 1: Pull the deal list from Salesforce via Glean.
4. Execute Layer 2: For EACH deal, read the prior Notion dossier, then dispatch the deal-analyzer sub-agent (NOT the deal-bootstrapper). Each sub-agent runs in its own isolated context with a 7-day lookback window.
5. Collect all sub-agent results.
6. Execute Layer 3: Synthesize the results, update existing Notion rows, append changelog entries, send notification.
