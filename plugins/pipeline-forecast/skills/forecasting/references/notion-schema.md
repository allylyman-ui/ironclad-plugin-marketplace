# Notion Database Schema: Pipeline Intelligence

> **Note on user tokens:** This reference file uses `[USER_INITIALS]` where the original hardcoded "AL". The lead `forecasting` skill resolves this token in its Step 0 (Resolve the Runtime User) block before reading this file. If the runtime user is Ally Lyman, `[USER_INITIALS]` → `AL`; if Jamie Smith, `[USER_INITIALS]` → `JS`. Do NOT leave the literal `[USER_INITIALS]` token in any Notion property value — always substitute.

## Database Properties

| Property | Type | Purpose |
|---|---|---|
| Deal Name | Title | Account Name |
| Opportunity Name | Rich Text | Full Salesforce opportunity name |
| Stage | Select | Current Salesforce stage: 2-Assessing, 3-Validating, 4-Developing MAP, 5-Firming Terms, 6-Verbal, 7-Pending |
| Recommended Stage | Select | Same options — only populate if different from current |
| ARR | Number (USD) | Current Salesforce ARR |
| Recommended ARR | Number (USD) | If pricing discussed and different — only populate if mismatch |
| ARR Mismatch | Checkbox | True if recommended ARR differs from current ARR |
| ARR Source | Rich Text | Gong call reference: "[call title], [date] — $[amount] discussed" |
| Close Date | Date | Current Salesforce close date |
| Recommended Close Date | Date | If working date discussed and different |
| Close Date Mismatch | Checkbox | True if recommended differs from current |
| Forecast Category | Select | Current: Omitted, Pipeline, Best Case, Commit |
| Recommended Category | Select | Based on evidence |
| Quarter | Select | Ironclad fiscal quarter: Q1-FY27, Q2-FY27, Q3-FY27, Q4-FY27, etc. |
| Next Steps | Rich Text | Copy-paste ready, [USER_INITIALS] format |
| Sales Notes | Rich Text | Copy-paste ready, running log preserved |
| Red Flags | Rich Text | Copy-paste ready, [USER_INITIALS] format |
| Evidence Summary | Rich Text | Condensed Gong/Email/Calendar/Drive findings |
| Last Updated | Date | Date of this analysis run |
| Status | Select | Active, Needs Update, Dead Out Candidate, Closed/Removed |
| Confidence | Select | High, Medium, Low |

## Update Rules

**Existing deal (row already exists):**
- Update all property values with current findings
- Append a new dated section to the page body (not the properties — the page content below):
  ```
  ## [Date] Weekly Update
  [Full evidence summary]
  [Changes since last run]
  [Field update recommendations]
  ```
- Never overwrite existing page body content — always append on top

**New deal (no row exists):**
- Create new row with all properties
- Add initial page body content as "Initial Baseline" entry

**Removed deal (was in Notion but not in this week's Salesforce pull):**
- Change Status to "Closed/Removed"
- Add a final page body entry: "[Date] — Deal no longer in open pipeline. Marked as closed."
- Do not delete the row

## How the Lead Agent Reads Prior Dossiers

Before dispatching a sub-agent for a deal, the lead agent should:
1. Search the Pipeline Intelligence database for a row where Deal Name matches the account name
2. If found, read the row's properties (especially Evidence Summary, Last Updated, Next Steps, Sales Notes, Red Flags)
3. Pass this to the sub-agent as "prior dossier" context, including the resolved user tokens (`user_full_name`, `user_first_name`, `user_initials`) so the sub-agent uses the correct initials in its field outputs
4. The sub-agent uses this to produce a "Changes Since Last Run" section
