# Salesforce Field Formatting Standards

> **Note on user tokens:** This reference file uses `[USER_INITIALS]` where the original hardcoded "AL" and `[USER_FIRST_NAME]` where it hardcoded "Ally". The lead `forecasting` skill resolves these tokens in its Step 0 (Resolve the Runtime User) block, and the `deal-analyzer` and `deal-bootstrapper` sub-agents resolve them from their dispatch payload. If the runtime user is Ally Lyman, `[USER_INITIALS]` → `AL` and `[USER_FIRST_NAME]` → `Ally`; if Jamie Smith, `[USER_INITIALS]` → `JS` and `[USER_FIRST_NAME]` → `Jamie`. Do NOT leave the literal tokens in any field value written to Salesforce — always substitute before writing.

[USER_FIRST_NAME] has a specific format for Salesforce fields. Always use this exact format.

## Next Steps

Always start with today's date, "[USER_INITIALS]" initials, and the header "Next Steps & Action Items:"
Then list action items with dates (if scheduled) or "(not scheduled)" if not yet booked.

Format:
```
[M/D/YY] [USER_INITIALS] Next Steps & Action Items:
- [date] [action item — who, what, when]
- [date] [action item]
- (not scheduled) [action item that needs to be scheduled]
```

Example (resolved for Ally Lyman, initials `AL`):
```
4/15/26 AL Next Steps & Action Items:
- 4/21 Pricing review call with procurement (Sarah + Mike)
- 4/23 Exec demo with CIO
- (not scheduled) Setup final implementation scoping meeting with legal
```

Example (resolved for Jamie Smith, initials `JS`):
```
4/15/26 JS Next Steps & Action Items:
- 4/21 Pricing review call with procurement (Sarah + Mike)
- 4/23 Exec demo with CIO
- (not scheduled) Setup final implementation scoping meeting with legal
```

## Sales Notes (Completed Steps)

This is a RUNNING LOG. Never delete existing content. Always add new entries on top.

Format:
```
[M/D/YY] [USER_INITIALS] Completed Steps:
- [date completed] [what was completed]
- [date completed] [what was completed]

[ALL EXISTING SALES NOTES CONTENT PRESERVED BELOW — DO NOT DELETE OR SUMMARIZE]
```

Example (resolved for Ally Lyman):
```
4/15/26 AL Completed Steps:
- 4/10 Pricing review call with Jonathan — presented $92K package
- 4/7 Business case deck sent to Jonathan for internal circulation

2/26/26 AL Completed Steps:
- 2/20 Payer Use Case Sync with Joe and team
- 2/11 Product & Use Case Deep Dive
```

Note that historical Sales Notes entries retain whichever initials the previous owner used — do not rewrite older entries. Only the new entry at the top uses the current runtime user's initials.

The workflow: Whatever was in Next Steps that is now done → move it to Sales Notes as a completed step with the date it happened. Then update Next Steps with new forward-looking action items.

## Red Flags

Format:
```
[M/D/YY] [USER_INITIALS] Red Flags:
- [red flag description] — [action plan to mitigate]
```

Example (resolved for Ally Lyman):
```
4/15/26 AL Red Flags:
- New head of legal starting 5/1 which may stall the project — Meeting with current champion on 4/28 to discuss transition plan and get intro to new HoL
```

When resolved, set to:
```
None
```

And move the resolved flag to Sales Notes with a note that it was resolved.
