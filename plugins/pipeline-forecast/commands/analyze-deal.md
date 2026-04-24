---
name: analyze-deal
description: Analyze a single deal ad-hoc. Provide an account name and this will research Gong, Gmail, Calendar, and Drive, then update the Notion dossier for that deal.
---

Run the deal-analyzer sub-agent for the specified deal. The user will provide an account name.

1. Read skills/forecasting/SKILL.md and its reference files.
2. Search Glean (app: salescloud) for the specified account to get current Salesforce data.
3. Check Notion for a prior dossier on this deal.
4. Dispatch the deal-analyzer sub-agent with the Salesforce data and prior dossier.
5. Write the sub-agent's output to Notion.
