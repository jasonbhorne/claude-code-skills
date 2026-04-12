---
name: pep-claims
description: Monthly pull of PEP Claims Metrics for Greeneville City Schools. Cycles through all insurance types, extracts summary metrics and chart data, produces a 10-year XLSX workbook with month-over-month comparison, archives to OneDrive, and logs to Obsidian. Activate when the user says "/pep-claims", "pull pep claims", "run pep claims", or "update pep claims".
---

# PEP Claims Monthly Pull

## Purpose
Pull current PEP Claims Metrics data for Greeneville City Schools (insured #0312) from the Public Entity Partners portal, build a historical tracking workbook, and compare month-over-month to surface new claims, movement in incurred loss, and policy year trends.

## Trigger
User says: `/pep-claims`, "pull pep claims", "run pep claims", "update pep claims", or "pep monthly".

## Pre-flight: User logs in manually

The Puppeteer MCP runs a separate browser. Before you do anything, say to the user:

> I'll open the PEP portal. Log in at https://www.pepartners.org/portal-welcome and navigate to the Claims Metrics page (any insurance type is fine). When you see the Claims Metrics dashboard loaded, tell me "ready".

Use `mcp__puppeteer__puppeteer_navigate` to open `https://www.pepartners.org/portal-welcome`.

Wait for user to confirm "ready". Do NOT proceed without that confirmation.

## Step 1: Capture authenticated session URL

Once the user confirms, extract the current URL and parse out the session token:

```javascript
// via mcp__puppeteer__puppeteer_evaluate
(() => {
  const url = window.location.href;
  const m = url.match(/sectoken=([^&]+)/);
  return JSON.stringify({ url, sectoken: m ? m[1] : null });
})();
```

Extract the `sectoken` value. The base URL pattern is:
```
https://pureshare.pepartners.org/amengine/amengine.aspx?config.mn=Claims_Activity_Wrapper&f=Claims_Activity_Wrapper&p_ORG=0:0:0:0312&sectoken={TOKEN}&p_RMIS={TYPE_CODE}
```

If the user isn't on the Claims page yet (no sectoken), tell them to navigate there and try again.

## Step 2: Cycle through all 8 insurance types

Insurance type codes:
- `iVOSW` = Workers' Comp
- `iVOSP` = Property
- `iVOSL` = Liability (All)
- `iVLAW` = Law Enforcement
- `iVGEN` = General Liability
- `iVEAO` = E&O
- `iVAUT` = Auto Liability
- `iVAPD` = Auto Physical Damage

For each code, navigate to the URL with that `p_RMIS` value, take a screenshot (1400x900), and extract DOM metrics using this JavaScript:

```javascript
(() => {
  const body = document.body.innerText;
  const rmisSelect = document.getElementById('p_RMIS');
  const currentType = rmisSelect ? rmisSelect.options[rmisSelect.selectedIndex].text.trim() : 'unknown';
  const metrics = { insuranceType: currentType };
  const openClaimsMatch = body.match(/(\d+)\s*Open Claims/);
  const incurredMatch = body.match(/Incurred Loss\s*\$?([\d,]+)/);
  const allClaimsMatch = body.match(/(\d+)\s*Claims totaling\s*\$([\d,]+)\s*Total Incurred/g);
  const litigatedMatch = body.match(/(\d+)\s*Litigated\s*(\d+)%/);
  const updatedMatch = body.match(/Updated as of\s*([\d/]+\s*[\d:]+\s*[AP]M)/);
  metrics.openClaims = openClaimsMatch ? parseInt(openClaimsMatch[1]) : 0;
  metrics.incurredLoss = incurredMatch ? incurredMatch[1] : '0';
  metrics.litigated = litigatedMatch ? { count: parseInt(litigatedMatch[1]), pct: parseInt(litigatedMatch[2]) } : { count: 0, pct: 0 };
  metrics.updatedAs = updatedMatch ? updatedMatch[1] : null;
  if (allClaimsMatch && allClaimsMatch.length >= 2) {
    const t = allClaimsMatch[0].match(/(\d+)\s*Claims totaling\s*\$([\d,]+)/);
    const b = allClaimsMatch[1].match(/(\d+)\s*Claims totaling\s*\$([\d,]+)/);
    metrics.topOpenClaims = { count: parseInt(t[1]), total: t[2] };
    metrics.allClaims = { count: parseInt(b[1]), total: b[2] };
  } else if (allClaimsMatch) {
    const m = allClaimsMatch[0].match(/(\d+)\s*Claims totaling\s*\$([\d,]+)/);
    metrics.topOpenClaims = { count: 0, total: '0' };
    metrics.allClaims = { count: parseInt(m[1]), total: m[2] };
  }
  return JSON.stringify(metrics);
})();
```

Store the DOM metrics in memory as you go. Label screenshots `pep_<type_slug>.png`.

## Step 3: Read chart values from screenshots

The bar charts (Claims by Year, Incurred Loss by Year, Claims by Month) are server-rendered PNGs. You can read their bar values visually from each screenshot as you view it. Capture for each type:
- Claims by Year (Count) for 2020-2025
- Incurred Loss by Year ($ amounts 2020-2025, abbreviated in the chart)
- Claims by Loss Month (last 12 months)

Also visit the Financials tab (click `img[alt="Financials"]`) to capture:
- Net Incurred by Policy Year 2016-2025 (Expense + Loss split)

## Step 4: Determine archive path and check prior month

Archive folder: `<OneDrive>/Insurance/Data/`

This month's file: `PEP_Claims_Metrics_YYYY-MM-DD.xlsx` (YYYY-MM-DD = today).

Before building, check if a prior month's file exists:
```bash
ls -t <OneDrive>/Insurance/Data/PEP_Claims_Metrics_*.xlsx 2>/dev/null | head -2
```

Read the most recent prior file (if any) to pull baseline numbers for the month-over-month diff tab.

## Step 5: Build the workbook

Use the builder script at `build_pep_workbook.py` (in the skill directory). Pass it:
- Path to output XLSX
- Path to prior month XLSX (or empty string if none)
- JSON blob with current month's extracted data

The workbook has 7 tabs:
1. **Summary** - current open claims, incurred, totals by insurance type
2. **Net Incurred (10-Year)** - 2016-2025 net incurred by line
3. **YoY Analysis** - dollar and percentage change year-over-year
4. **Claims Count by Year** - 2020-2025 claim counts
5. **Claims by Month** - last 12 months
6. **All Lines Combined** - aggregated 10-year trend with averages
7. **MoM Changes** - month-over-month diff vs. prior snapshot (new tab for skill)

## Step 6: Log to Obsidian

Create a session note at `Sessions/YYYY-MM-DD - PEP Claims Monthly Pull.md`:
- Frontmatter: `type: session`, `tags: [session, pep-claims, risk-management, monthly]`, `summary: one-line summary`
- Content:
  - Updated-as-of timestamp from PEP
  - Headline: total open claims across all lines, total open incurred
  - Month-over-month movement (from MoM Changes tab)
  - Any new open claims or significant incurred loss changes
  - Link to the archived XLSX
  - Any anomalies or flags worth Ellen's attention

Also update or create `Projects/PEP Claims Monthly Tracking.md` if it doesn't exist yet - a lightweight project tracker linking each monthly session.

## Step 7: Report to user

Print a short summary to the user:
- Total open claims and incurred across all lines
- Most notable MoM changes
- File path to archived XLSX
- Session note path in Obsidian

Offer to open the XLSX.

## Design notes

- **Auth**: The `sectoken` in the URL expires. The skill relies on the user logging in first, not scripted login.
- **Chart data**: Server-rendered PNGs require visual reading. If PEP adds a CSV/PDF export, switch to that.
- **Conservative defaults**: If a section fails to extract (missing DOM element, empty chart), log the gap but continue. Don't overwrite good data from prior month with zeros.
- **Frequency**: Monthly. PEP's "Updated as of" timestamp typically refreshes around the 10th-15th of each month.

## Related
- Workbook template and logic were first built 2026-04-12 (see Obsidian session `2026-04-12 - PEP Claims Extract and Drinnon Doc Update`)
- Risk Management section in the Drinnon onboarding doc references `PEP_Claims_Metrics_YYYY-MM-DD.xlsx`
