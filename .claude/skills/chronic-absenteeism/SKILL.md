---
name: chronic-absenteeism
description: Process a periodic Chronic Absenteeism Accountability spreadsheet from GCS attendance into an executive summary, per-principal packets, and a dashboard workbook. Archives to OneDrive and logs to Obsidian. Activate when the user says "/chronic-absenteeism", "chronic absenteeism snapshot", "process CA data", or "CA spreadsheet".
---

# Chronic Absenteeism Snapshot

## Purpose

The GCS attendance lead periodically sends a multi-sheet Chronic Absenteeism Accountability workbook. This skill transforms that raw snapshot into a decision-ready set of deliverables: an executive summary for the C-Team, per-principal packets for each building leader, a pivoted dashboard workbook, and an Obsidian session log.

## Trigger

User says `/chronic-absenteeism`, "process chronic absenteeism", "run CA snapshot", "chronic absenteeism analysis", "CA accountability spreadsheet", or drops a file named like `Chronic Abs Accountability Data as of *.xlsx` into Downloads.

## Input file

Expected default path: `~/Downloads/Chronic Abs Accountability Data as of <Month> <Day> <Year>.xlsx`

If the user gives a different path, use it. If no path is provided, search `~/Downloads`, `~/Desktop`, and `~/Documents` for the most recent file matching `*Chronic Abs*Accountability*.xlsx`.

### Expected workbook structure
- `School Chronic Abs %` sheet: district rollup with columns `school_name, student_group, grade_band, n_students, n_chronically_absent, pct_chronically_absent`
- One sheet per school with codes `HH, EV, HI, TV, TOPS, GMS, GHS`. Each has columns: `School, SSID, First Name, Last Name, grade, n_absences, isp_days_to_date, isp_days_projected_full_year, instructional_calendar_days, absentee_rate`
- A student is "already chronically absent" when `n_absences >= 17`
- A student is "trending" when they are flagged but below 17 days (absentee rate at or above 10%)

If the schema has drifted (column order, new sheet, different school code), pause and ask the user before guessing.

## Pre-flight

Before running the builder:

1. Confirm the input file exists. Print its modified date and size for sanity.
2. Extract the as-of date from the filename (e.g., `March 10 2026` -> `2026-03-10`). If the filename doesn't include a date, ask the user.
3. Ask the user for the instructional day count if you can't read it from the data. If every student row has the same `isp_days_to_date` and `instructional_calendar_days`, use those.

## Step 1: Load the workbook and classify students

Read the source xlsx with `openpyxl`. For every school sheet, collect rows that have a non-null SSID. Each row becomes a dict with: `school, ssid, first, last, grade, absences, isp_to_date, isp_proj, cal_days, rate`.

Classify:
- `already_ca` if `absences >= 17`
- `trending` otherwise

Compute by-school totals and by-grade-band totals (K-5, 6-8, 9-12).

## Step 2: Build the dashboard xlsx

Output path: `~/Documents/Chronic Absenteeism <YYYY-MM-DD>/Chronic Absenteeism Dashboard <YYYY-MM-DD>.xlsx`

Five tabs:

1. `District Summary` — title + as-of, rollup table (school, flagged, already CA, trending, % already CA) with district total row, plus a copy of the state-calc `% Chronically Absent` rollup for all enrolled students.
2. `Already CA (17+)` — every student at or above 17 days, sorted by absences desc, red fill (`F8CBAD`) on every row, frozen header.
3. `Trending (10%+)` — every flagged student below 17 days, sorted by absentee rate desc, yellow fill (`FFF2CC`).
4. `By Grade Band` — school x grade band matrix (counts of already CA and trending).
5. `All Flagged Students` — combined table with a `Status` column, fill color by status, sorted by absences desc.

Formatting: navy header row `1F3864` with white bold text, Arial/Calibri default, autosized columns up to a 45-char cap, frozen header on long tabs.

## Step 3: Build the executive summary .docx

Output path: `~/Documents/Chronic Absenteeism <YYYY-MM-DD>/Chronic Absenteeism Executive Summary <YYYY-MM-DD>.docx`

Sections (in order):
1. Title block: `Chronic Absenteeism Snapshot` + `Greeneville City Schools | As of <long date>, Day <N> of 167`
2. The Bottom Line paragraph: total flagged, already CA, trending, with the "trending can still avoid CA if they stabilize" framing.
3. District Rollup table: School, Flagged, Already CA, Trending, % Already CA; bold district total row.
4. School-Level % Chronically Absent table (the state calc rollup) with the note that 0% values indicate district-level ISP aggregation hasn't finalized.
5. Outliers Worth Flagging: top-10 by absence count, as a table with school, student, grade, days, rate.
6. Where the Concentration Sits: bullets calling out GHS, GMS, HH, and the small elementary/TOPS lists that are case-managed one-on-one.
7. Recommended Follow-Ups: 5 bullets — distribute packets, SART/court sequence check, GHS triage, reconcile partial-year enrollees with the attendance office, re-run in 4 weeks.

Styling: navy `1F3864` headings, no emdashes, no bold body text.

## Step 4: Build per-principal packets

One .docx per school in `SCHOOL_NAMES`. Output pattern: `Chronic Absenteeism Packet - <Full School Name>.docx`.

Each packet contains:
1. Title: `Chronic Absenteeism — <School>` + as-of subtitle.
2. Your Numbers at a Glance: flagged, already CA, trending, plus the school-level CA rate from the rollup sheet if available.
3. `Already Chronically Absent` table (only if the school has any): student, grade, days absent, rate, SSID — sorted by absences desc.
4. `Trending Toward CA` table (only if the school has any): same columns, sorted by rate desc.
5. Talking Points: 5 bullets (medical/legal vs unexcused, attendance letter sequence, partial-year ISP flags, named intervention plans, focused parent contact for trending students).
6. What I Need From You: 3 bullets (written update on top 5 already-CA names, SART/court confirmation for 25+ absences, data issues to reconcile).

Skip a table section cleanly if the school has zero students in that bucket (EastView sometimes has no already-CA students).

## Step 5: Archive to OneDrive

Target folder: `<OneDrive>/Data/Accountability Data/Chronic Absenteeism/`

Create the folder if it doesn't exist. Copy:
- The original source xlsx (preserves the attendance office's red highlighting)
- The dashboard xlsx
- The executive summary docx
- All 7 per-principal packets

## Step 6: Log to Obsidian

Write `Sessions/<YYYY-MM-DD> - Chronic Absenteeism Snapshot <M-D>.md` with:

Frontmatter:
```yaml
type: session
date: YYYY-MM-DD
summary: one-line description
tags: [session, attendance, chronic-absenteeism, accountability, data]
```

Body sections:
- Task (what the attendance office sent, what got produced)
- Key Numbers: total flagged, already CA, trending, school-by-school counts with already-CA counts, district rollup from the summary tab
- Outliers Worth a Second Look: name the top 3-5 (GHS senior at highest absence count, TOPS/GMS outliers, partial-year enrollees to flag)
- Deliverables Produced: bullet list of all files with paths
- Recommended Follow-Ups: the 5 bullets from the exec summary
- Source: original file and archive path
- Build Script: pointer to the skill's build.py

## Step 7: Report back to the user

Short summary:
- Headline counts (total flagged, already CA, trending)
- Top 1-2 concentration schools and the "where to push intervention first" call
- Paths to the deliverable folder and Obsidian session note

Do not offer to email the principals. The per-principal packets are for Jason to review and forward.

## Design notes

- **Builder script**: `build.py` in this skill directory is the canonical implementation. Copy it to the per-snapshot output folder on each run so the snapshot folder is self-contained, then execute from there. Update `SRC` and `AS_OF` at the top of the copy.
- **School codes**: HH, EV, HI, TV, TOPS, GMS, GHS. If a new sheet appears (e.g., a new building), add it to `SCHOOL_NAMES` rather than silently dropping it.
- **17-day threshold**: This matches TN's 10% chronic absenteeism definition at day 170 (17 = 10% of 170). The threshold does not scale with partial-year enrollees — a student with only 50 ISP days and 6 absences is not "already CA" by the 17-day rule, but their rate will flag them as trending.
- **Partial-year flag**: Always mention this to the user. The ISP denominator shortens for partial-year students, inflating their rate and sometimes misclassifying them. The dashboard shows `isp_days_to_date` and `instructional_calendar_days` side by side so the reader can spot it.
- **Frequency**: Ad-hoc. The attendance office sends these on its own cadence. After the first run in a month, subsequent pulls should be compared against the prior snapshot to measure movement (future enhancement: add a MoM tab).
- **No emoji, no emdashes, no bold body text** per Jason's global output style.

## Related
- First built 2026-04-20. Session log: `Sessions/2026-04-20 - Chronic Absenteeism Snapshot 3-10.md`.
- Sibling skills with similar "process periodic spreadsheet -> build deliverables -> archive -> log" pattern: `pep-claims`, `wfteada-tracker`, `tisa`.
