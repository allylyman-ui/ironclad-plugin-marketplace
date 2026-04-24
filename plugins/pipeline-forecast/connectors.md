# Connectors

This plugin depends on five connectors. All must be authenticated before running `/bootstrap-pipeline`, `/run-forecast`, or `/analyze-deal`. If any are missing, the lead agent should pause and surface the missing connector before dispatching sub-agents.

## Required

### Glean
**Required.** Primary search layer for Salesforce opportunities (`app:salescloud`) and Gong call transcripts (`app:gong`). All Salesforce and Gong access is mediated through Glean filters — there is no direct Salesforce or Gong MCP in this plugin. Without Glean, the deal list cannot be pulled and per-deal sub-agents have no call evidence to analyze.

**Used in:** Layer 1 (deal list), `deal-analyzer` Step 1 (Gong), `deal-bootstrapper` Step 1 (Gong, 90-day lookback)

### Gmail
**Required.** Searches email threads with deal contacts to surface pricing discussions, procurement engagement, champion sentiment, and new contacts not yet in Salesforce. Sub-agents query Gmail per-contact (not per-account) using specific email addresses.

**Used in:** `deal-analyzer` Step 2, `deal-bootstrapper` Step 2

### Google Calendar
**Required.** Pulls completed and upcoming meetings per account to confirm Gong coverage, identify gaps (meetings without transcripts), and validate next-step momentum.

**Used in:** `deal-analyzer` Step 3, `deal-bootstrapper` Step 3

### Google Drive
**Required.** Searches for deal-specific documents — decks, business cases, redlines, security questionnaires — and saves the weekly pipeline intelligence PDF to a "Pipeline Intelligence" folder for archival.

**Used in:** `deal-analyzer` Step 4, `deal-bootstrapper` Step 4, Layer 3b (PDF archive)

### Notion
**Required.** Hosts the **Pipeline Intelligence** and **Closed Deals** databases. Stores per-deal dossiers, changelog entries, and source links across runs. The weekly `/run-forecast` command refuses to start without an existing Pipeline Intelligence database — run `/bootstrap-pipeline` first to create it.

**Used in:** Layer 2 (read prior dossiers), Layer 3c (write updated rows, archive removed deals)

## Setup checklist

Before running any command in this plugin:

- [ ] Glean is authenticated and `app:salescloud` + `app:gong` filters return results
- [ ] Gmail is authenticated against Ally's Ironclad mailbox
- [ ] Google Calendar is authenticated against Ally's Ironclad calendar
- [ ] Google Drive is authenticated and the "Pipeline Intelligence" folder exists (or can be created)
- [ ] Notion is authenticated against the workspace that holds (or will hold) the Pipeline Intelligence and Closed Deals databases

## Notes

- **No direct Salesforce MCP.** All Salesforce reads happen through Glean. Field updates produced by the sub-agents are returned as copy-paste-ready text blocks for Ally to paste into Salesforce manually.
- **No direct Gong MCP.** All Gong call evidence comes through Glean's `app:gong` filter.
