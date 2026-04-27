"""Update a trip's status (Pending / Submitted / Reimbursed).

Usage:
  python mark_status.py <trip_id> <status> [submission_date YYYY-MM-DD]
"""
from __future__ import annotations

import sys
from datetime import datetime

import _lib

VALID = {"Pending", "Submitted", "Reimbursed"}


def main():
    if len(sys.argv) < 3:
        print("usage: mark_status.py <trip_id> <Pending|Submitted|Reimbursed> [YYYY-MM-DD]", file=sys.stderr)
        sys.exit(2)

    trip_id = sys.argv[1]
    status = sys.argv[2]
    if status not in VALID:
        print(f"error: status must be one of {sorted(VALID)}", file=sys.stderr)
        sys.exit(2)
    sd = sys.argv[3] if len(sys.argv) > 3 else None

    wb = _lib.load_workbook()
    trips = wb["Trips"]
    row = _lib.find_trip_row(trips, trip_id)
    if row is None:
        print(f"error: trip {trip_id} not found", file=sys.stderr)
        sys.exit(1)

    trips.cell(row=row, column=15, value=status)
    if sd:
        trips.cell(row=row, column=16, value=datetime.fromisoformat(sd))
        trips.cell(row=row, column=16).number_format = "m/d/yyyy"

    _lib.save_workbook(wb)
    print(f"Updated {trip_id} status to {status}" + (f" (submitted {sd})" if sd else ""))


if __name__ == "__main__":
    main()
