---
name: travel-expense
description: Log a work travel trip and produce form-ready values for an employer-provided Microsoft Forms travel expense form. Maintains a Travel Expense Tracker.xlsx with one-row-per-trip history. Activate when user says "/travel-expense", "log a trip", "travel expense form", "trip reimbursement", or mentions filling out the travel expense form.
---

# Travel Expense Skill

## Purpose
Maintain a multi-trip log of work travel and produce the exact values needed to fill out an employer-provided Microsoft Forms travel expense form. The tracker carries trip history; the skill computes per-day meal eligibility from departure/return times and applies the configured mileage rate.

## Trigger
User says: `/travel-expense`, "log a trip", "travel expense form", "trip reimbursement", "I have to fill out the travel form", or similar.

Sub-commands:
- `/travel-expense` — add a new trip (interactive)
- `/travel-expense list` — show all logged trips
- `/travel-expense fill <trip-id>` — re-print form values for an existing trip
- `/travel-expense submitted <trip-id> [YYYY-MM-DD]` — mark a trip as submitted

## One-time setup

Copy `config.example.json` from this skill directory to `~/.claude/.travel-expense-config.json` and fill in:
- `tracker_path` — where the workbook lives (typically a OneDrive/SharePoint folder)
- `form_url` — your employer's Microsoft Forms expense form URL
- `personal` — street, city, state, zip, school/building, signature
- `rates` — mileage $/mile, breakfast/lunch/dinner per diems
- `eligibility` — depart/return time cutoffs for each meal

Then run `python scripts/build_tracker.py` once to create the workbook.

## Files

- Tracker: path from `tracker_path` in config
- Local config (gitignored): `~/.claude/.travel-expense-config.json`
- Scripts: `~/.claude/skills/travel-expense/scripts/`
  - `build_tracker.py` — rebuild the workbook from scratch
  - `add_trip.py` — append a trip; reads JSON on stdin
  - `form_fill.py <trip_id>` — print form values
  - `list_trips.py [--status X] [--year Y]` — list trips
  - `mark_status.py <trip_id> <Pending|Submitted|Reimbursed> [YYYY-MM-DD]` — update status

Use `/opt/anaconda3/bin/python3` to invoke (Anaconda Python).

## Reimbursement model (defaults — all configurable)

- Mileage: $0.725/mile
- Breakfast: eligible if departure ≤ 6:30 AM
- Lunch: eligible if departure ≤ 11:00 AM
- Dinner: eligible if return ≥ 7:00 PM

Personal fields (street, city, state, zip, school/building, signature) appear on every form submission. They live in config and never in source.

## Workflow: Adding a new trip

1. Confirm scope in 2-3 bullets. Show the user what you'll log before writing.

2. Gather inputs:
   - Purpose of trip (e.g., "Annual conference name")
   - City/state where travel occurred
   - Departure and return dates
   - Round-trip miles in personal vehicle
   - Travel/parking, lodging, other expenses (with receipts)
   - Per-day depart/return times OR explicit B/L/D selection
     - If user says "I left at 7am and got back at 6pm" → no breakfast (after 6:30), lunch eligible (before 11), no dinner (before 7pm)
     - For multi-day: day 1 has depart but no return; last day has no depart but a return; middle days are typically full B+L+D unless overridden

3. Generate a Trip ID using `<EVENT>-<YYYY>-<MM>` (e.g., `ANNUAL-2026-04`). Ask if unclear.

4. Build the trip JSON and pipe to `add_trip.py`:
   ```bash
   /opt/anaconda3/bin/python3 ~/.claude/skills/travel-expense/scripts/add_trip.py <<'EOF'
   {
     "trip_id": "...",
     "purpose": "...",
     "city_state": "...",
     "depart_date": "YYYY-MM-DD",
     "return_date": "YYYY-MM-DD",
     "miles": 0,
     "travel_parking": 0,
     "lodging": 0,
     "other": 0,
     "account": "",
     "status": "Pending",
     "submission_date": null,
     "notes": "",
     "days": [
       {"day": 1, "date": "YYYY-MM-DD", "depart_time": "HH:MM", "return_time": "HH:MM", "B": 0, "L": 0, "D": 1}
     ]
   }
   EOF
   ```
   Days array: one entry per travel day. Provide `depart_time`/`return_time` to auto-fill B/L/D, or set B/L/D directly to override.

5. Run `form_fill.py <trip_id>` to print the form values.

6. Tell the user the trip is logged and present the form values. Suggest they fill the form now and let you know when submitted so you can flip status with `mark_status.py`.

## Workflow: Existing trip lookup

For a trip already in the log, run `form_fill.py <trip_id>` and present output.

## Workflow: Listing

`list_trips.py` shows trip ID, dates, purpose, miles, total, status. Filters: `--status Pending`, `--year 2026`.

## Validation

Before saving:
- Confirm mileage rate × miles matches user expectation
- Per-day B/L/D max 3 (one each per meal)
- Grand total = mileage + travel/parking + lodging + other + meals
- Trip ID must be unique (script errors otherwise)
- Restate the math when presenting: "$X.XX = $Y.YY mileage + $Z.ZZ meals + ..."

## Failure modes

- Tracker missing → run `build_tracker.py`.
- Config missing → copy `config.example.json` to `~/.claude/.travel-expense-config.json` and edit.
- Duplicate Trip ID → ask user to disambiguate (e.g., suffix with `-B`).
- Round-trip vs one-way miles ambiguous → ask explicitly. The form's miles field is round-trip total.
- Account number blank → optional; leave blank.
