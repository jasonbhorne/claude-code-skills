# Bill Tracker Skill

## Description
Track Tennessee education legislation. Uses the official TN Legislature website (wapp.capitol.tn.gov) as the primary data source for status, votes, fiscal notes, and amendments. Optionally seeds bill lists from State Affairs Pro reports.

## Trigger
Activate when the user says "track bills", "bill tracker", "legislative tracker", provides a State Affairs Pro report URL, or asks to check bill status.

## Arguments
- URL to a State Affairs Pro report (to get initial bill list)
- OR: specific bill numbers to track
- Optional: "update" to refresh status on previously tracked bills

## Instructions

### Step 1: Identify Bills to Track
Option A: If a State Affairs Pro report URL is provided:
1. Use Puppeteer MCP to navigate (JS-heavy SPA, requires browser rendering)
2. Extract text via `puppeteer_evaluate` on `document.querySelector('body').innerText`
3. The page content is long; extract in chunks (0-15000, 15000-30000, etc.)
4. Parse bill numbers from the report

Option B: If specific bill numbers are given, use those directly.

Option C: If "update" mode, read the most recent tracker from the Legislative folder and use those bill numbers.

### Step 2: Look Up Each Bill on TN Legislature Website
For each bill, fetch from `https://wapp.capitol.tn.gov/apps/Billinfo/Default?BillNumber={BILL}&ga=114`
- Use WebFetch with a prompt to extract: bill number, caption, sponsors, full status history with dates, current status, companion bill, amendments, vote results, and fiscal impact
- Note: Most current bills are GA 114. Carryover bills from 2024-2025 may also be GA 114. If "Bill Not Found", try GA 113.
- Batch fetches in parallel (8 at a time works well) for efficiency

Extract for each bill:
- Bill number and companion bill number
- Short title/description
- Sponsor(s) with party
- Full status history with dates
- Current status in both chambers
- Amendment numbers and descriptions
- Vote results (committee and floor, with counts)
- Fiscal impact statement
- Next scheduled hearing/vote

### Step 3: Categorize and Assess Impact
Assign each bill to a $DISTRICT_NAME-relevant category:
- **Funding** - budget, funding formulas, weighted allocations
- **Safety/Security** - school safety, threats, searches, SROs
- **Nutrition** - food service, meal programs
- **Staffing/HR** - licensure, tenure, salary, hiring, bonuses
- **Curriculum** - standards, instruction
- **Technology/Digital** - devices, virtual schools, internet policy, AI
- **Charter/Choice** - charter schools, vouchers, private school access
- **Student Services** - special education, attendance, truancy, health
- **Governance** - board operations, committees, reporting deadlines
- **Other**

Rate district impact as:
- **High** - Directly affects district operations, budget, or compliance
- **Medium** - May require policy changes or has indirect effects
- **Low** - Minimal direct impact
- **Watch** - Caption bill or broad scope; could evolve

### Step 4: Generate Tracking Spreadsheet
Create an Excel file using `openpyxl` with these sheets:

**Sheet 1: "Bill Tracker"** (main tracking sheet)
Columns: Bill #, Companion, Short Title, Sponsor, Category, District Impact, House Status, Senate Status, Last Action, Last Action Date, Next Hearing, Caption Bill, Fiscal Impact, Key Votes, Notes

Format:
- Header row: bold, dark blue fill (#1F3864), white text, frozen panes
- Auto-filter on all columns
- Color-code District Impact: High=red fill (#FFC7CE), Medium=yellow (#FFE699), Low=green (#C6EFCE)
- Column widths sized appropriately
- Thin borders on all cells

**Sheet 2: "By Category"**
- Pivot-style summary: category, bill count, high-impact bills, all bills

**Sheet 3: "Timeline"**
- Bills sorted by next hearing/action date
- Color bands by day (blue, green, orange)
- Include votes and fiscal columns

**Sheet 4: "Full Details"**
- All fields including amendments, full summary, and district notes
- Word-wrapped cells for long text

**Sheet 5: "Vote Detail"**
- Bills sorted by impact, with vote breakdown and fiscal impact
- Highlight rows with close votes (margins < 5) in red

### Step 5: Save and Report
- Save to: `$ONEDRIVE_WORK/Legislative/Bill Tracker - {date_range}.xlsx`
- Also save to: `~/Documents/Research/Legislative/` (create if needed)
- Print summary to console: total bills, impact breakdown, notable fiscal notes, close votes, high-impact bill list

### Update Mode
When user says "update" or provides a new report URL:
1. Load the most recent existing tracker from the Legislative folder
2. Compare bill numbers: new, removed, status changes
3. Re-fetch each bill from the legislature website for current status
4. Flag changes in a "Status Changed" column
5. Save as a new dated file (don't overwrite)

## Output Format
Excel (.xlsx) via openpyxl. Never save plain text as .xlsx.

## Dependencies
- WebFetch (for TN Legislature website lookups)
- Puppeteer MCP (only if scraping State Affairs Pro for bill lists)
- Python 3 with openpyxl
