"""Print the form-ready values for an existing trip.

Usage:
  python form_fill.py <trip_id>

Output: a labeled list matching the Microsoft Form fields in order, ready to
copy/type into https://forms.office.com/Pages/ResponsePage.aspx?id=...
"""
from __future__ import annotations

import sys

import _lib

STATIC = {
    "1. Street Address": _lib.PERSONAL["street"],
    "2. City": _lib.PERSONAL["city"],
    "3. State": _lib.PERSONAL["state"],
    "4. Zip Code": _lib.PERSONAL["zip"],
    "5. School/Building": _lib.PERSONAL["school"],
    "26. Signature": _lib.PERSONAL["signature"],
}

FORM_URL = _lib.FORM_URL


def meal_label(b, l, d):
    parts = []
    if b:
        parts.append("Breakfast")
    if l:
        parts.append("Lunch")
    if d:
        parts.append("Dinner")
    return " + ".join(parts) if parts else "(none)"


def compute_meals_total(day_rows):
    total = 0
    for row in day_rows:
        total += row["B"] * _lib.BREAKFAST + row["L"] * _lib.LUNCH + row["D"] * _lib.DINNER
    return total


def main():
    if len(sys.argv) < 2:
        print("usage: form_fill.py <trip_id>", file=sys.stderr)
        sys.exit(2)

    trip_id = sys.argv[1]
    wb = _lib.load_workbook()
    trips = wb["Trips"]
    days = wb["Days"]

    trow = _lib.find_trip_row(trips, trip_id)
    if trow is None:
        print(f"error: trip {trip_id} not found", file=sys.stderr)
        sys.exit(1)

    summary = _lib.trip_summary(trips, trow)

    day_rows = []
    for r in _lib.find_day_rows(days, trip_id):
        day_rows.append({
            "day": days.cell(row=r, column=3).value,
            "date": days.cell(row=r, column=2).value,
            "B": days.cell(row=r, column=6).value or 0,
            "L": days.cell(row=r, column=7).value or 0,
            "D": days.cell(row=r, column=8).value or 0,
        })
    day_rows.sort(key=lambda d: d["day"] or 0)

    miles = summary["miles"] or 0
    mileage = miles * _lib.MILEAGE_RATE
    travel_parking = summary["travel_parking"] or 0
    lodging = summary["lodging"] or 0
    other = summary["other"] or 0
    meals = compute_meals_total(day_rows)
    grand_total = mileage + travel_parking + lodging + other + meals

    out = []
    out.append(f"Trip: {trip_id}")
    out.append(f"Status: {summary['status']}")
    out.append("")
    out.append("Form: " + FORM_URL)
    out.append("")
    out.append("--- Form values (in order) ---")
    for k in ("1. Street Address", "2. City", "3. State", "4. Zip Code", "5. School/Building"):
        out.append(f"{k}: {STATIC[k]}")
    out.append(f"6. Purpose of Trip: {summary['purpose']}")
    out.append(f"7. City/State Where Travel Occurred: {summary['city_state']}")
    out.append(f"8. Departure Date: {_lib.fmt_date(summary['depart'])}")
    out.append(f"9. Return Date: {_lib.fmt_date(summary['return'])}")
    out.append(f"10. Number of Miles in Personal Vehicle: {miles}")
    out.append(f"11. Mileage Reimbursement: {_lib.fmt_money(mileage)}")
    out.append(f"12. Air/Taxi/Uber/Lyft/Bus/Parking/Other: {_lib.fmt_money(travel_parking)}")
    out.append(f"13. Hotel/Lodging Reimbursement: {_lib.fmt_money(lodging)}")
    out.append(f"14. Other Expenses: {_lib.fmt_money(other)}")

    n = len(day_rows)
    if n >= 1:
        out.append(f"15. Day 1: {meal_label(day_rows[0]['B'], day_rows[0]['L'], day_rows[0]['D'])}")
    out.append(f"16. Add additional meals?: {'Yes' if n > 1 else 'No'}")
    field_n = 17
    for i in range(1, 7):
        if i < n:
            d = day_rows[i]
            out.append(f"{field_n}. Day {i+1}: {meal_label(d['B'], d['L'], d['D'])}")
        else:
            out.append(f"{field_n}. Day {i+1}: (skip)")
        field_n += 1

    out.append(f"23. Grand Total of Expenses: {_lib.fmt_money(grand_total)}")
    out.append(f"25. Account Number: {summary['account'] or '(leave blank)'}")
    out.append(f"26. Signature: {STATIC['26. Signature']}")
    out.append("")
    out.append("--- Math check ---")
    out.append(f"Mileage: {miles} miles × $0.725 = {_lib.fmt_money(mileage)}")
    out.append(f"Meals total: {_lib.fmt_money(meals)}")
    for d in day_rows:
        per_day = d["B"] * _lib.BREAKFAST + d["L"] * _lib.LUNCH + d["D"] * _lib.DINNER
        out.append(f"  Day {d['day']} ({_lib.fmt_date(d['date'])}): {meal_label(d['B'], d['L'], d['D'])} = {_lib.fmt_money(per_day)}")
    out.append(f"Grand Total: {_lib.fmt_money(grand_total)}")

    print("\n".join(out))


if __name__ == "__main__":
    main()
