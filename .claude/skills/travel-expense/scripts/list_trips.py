"""List trips in the tracker.

Usage:
  python list_trips.py [--status STATUS] [--year YEAR]
"""
from __future__ import annotations

import argparse
from datetime import datetime

import _lib


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--status")
    p.add_argument("--year", type=int)
    args = p.parse_args()

    wb = _lib.load_workbook()
    trips = wb["Trips"]
    days = wb["Days"]

    rows = []
    for r in range(2, trips.max_row + 1):
        if trips.cell(row=r, column=1).value is None:
            continue
        s = _lib.trip_summary(trips, r)
        if args.status and (s["status"] or "").lower() != args.status.lower():
            continue
        if args.year and isinstance(s["depart"], datetime) and s["depart"].year != args.year:
            continue

        miles = s["miles"] or 0
        mileage = miles * _lib.MILEAGE_RATE
        meals = 0
        for dr in _lib.find_day_rows(days, s["trip_id"]):
            b = days.cell(row=dr, column=6).value or 0
            l = days.cell(row=dr, column=7).value or 0
            d = days.cell(row=dr, column=8).value or 0
            meals += b * _lib.BREAKFAST + l * _lib.LUNCH + d * _lib.DINNER
        gt = mileage + (s["travel_parking"] or 0) + (s["lodging"] or 0) + (s["other"] or 0) + meals

        rows.append((s, miles, mileage, meals, gt))

    if not rows:
        print("No trips match.")
        return

    print(f"{'Trip ID':<20} {'Depart':<11} {'Return':<11} {'Purpose':<35} {'Miles':>6} {'Total':>10} {'Status':<11}")
    print("-" * 110)
    for s, miles, mileage, meals, gt in rows:
        print(
            f"{(s['trip_id'] or ''):<20} "
            f"{_lib.fmt_date(s['depart']):<11} "
            f"{_lib.fmt_date(s['return']):<11} "
            f"{(s['purpose'] or '')[:34]:<35} "
            f"{miles:>6} "
            f"{_lib.fmt_money(gt):>10} "
            f"{(s['status'] or ''):<11}"
        )


if __name__ == "__main__":
    main()
