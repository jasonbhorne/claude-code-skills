#!/usr/bin/env python3
"""
Financial file migration script.
Copies (not moves) files from scattered OneDrive locations into the organized
Financial Reports directory structure. Preserves timestamps via shutil.copy2.
Skips files that already exist at the destination.

Usage:
    python3 migrate_files.py           # dry-run (preview only)
    python3 migrate_files.py --execute # actually copy files
"""

import os
import sys
import shutil
import glob

PERSONAL = os.path.expanduser(
    "~/Library/CloudStorage/OneDrive-EastTennesseeStateUniversity/Personal"
)
FR = os.path.join(PERSONAL, "Financial Reports")

# Source pattern -> destination subfolder
# Each entry: (glob_pattern, dest_subfolder)
MAPPINGS = [
    # Pay Stubs from Bank Statements/Paystub
    (os.path.join(PERSONAL, "Bank Statements", "Paystub", "*.pdf"), "Pay Stubs"),

    # Banking files -> Bank Statements
    (os.path.join(PERSONAL, "Banking", "stmt.csv"), "Bank Statements"),
    (os.path.join(PERSONAL, "Banking", "transactions.xlsx"), "Bank Statements"),
    (os.path.join(PERSONAL, "Banking", "eStmt_*.pdf"), "Bank Statements"),

    # Mortgage escrow docs
    (os.path.join(PERSONAL, "Banking", "Mortgage - Escrow Docs", "*"), "Mortgage"),

    # House bank statements
    (os.path.join(PERSONAL, "House", "eStmt_*.pdf"), "Bank Statements"),

    # Credit card statement
    (os.path.join(PERSONAL, "CreditCardStatement.pdf"), "Credit Card Statements"),

    # Debt tracking files
    (os.path.join(PERSONAL, "Debt.xlsx"), "Debt Tracking"),
    (os.path.join(PERSONAL, "Debt_Amortization_Schedule.csv"), "Debt Tracking"),
    (os.path.join(PERSONAL, "Out of Debt.xlsx"), "Debt Tracking"),

    # Investments from House
    (os.path.join(PERSONAL, "House", "Edward Jones*.pdf"), "Investments"),
    (os.path.join(PERSONAL, "House", "Edward Jones*.xlsx"), "Investments"),
    (os.path.join(PERSONAL, "House", "Liquidity of Roth IRA.pdf"), "Investments"),
    (os.path.join(PERSONAL, "House", "XXXX7338*edj*.pdf"), "Investments"),

    # Investments from Stonks
    (os.path.join(PERSONAL, "Stonks", "Indices.xlsx"), "Investments"),

    # Retirement -> Investments
    (os.path.join(PERSONAL, "Retirement", "*.pdf"), "Investments"),

    # Deerfield Bonds
    (os.path.join(PERSONAL, "Deerfield Bonds.pdf"), "Investments"),

    # American Fidelity -> Insurance
    (os.path.join(PERSONAL, "American Fidelity", "*.pdf"), "Insurance"),

    # Loan Forgiveness
    (os.path.join(PERSONAL, "Loan Forgiveness", "*"), "Loan Forgiveness"),

    # Credit Reports -> Credit Score
    (os.path.join(PERSONAL, "Credit Report", "*.pdf"), "Credit Score"),

    # W2s and paystubs from House -> Pay Stubs
    (os.path.join(PERSONAL, "House", "*W2*.pdf"), "Pay Stubs"),
    (os.path.join(PERSONAL, "House", "*W2*.png"), "Pay Stubs"),
    (os.path.join(PERSONAL, "House", "*W2*.png.pdf"), "Pay Stubs"),
    (os.path.join(PERSONAL, "House", "*paystub*"), "Pay Stubs"),
    (os.path.join(PERSONAL, "House", "*Paystub*"), "Pay Stubs"),
    (os.path.join(PERSONAL, "House", "JASON HORNE CHECK STUBS.pdf"), "Pay Stubs"),
    (os.path.join(PERSONAL, "House", "gcsstub.pdf"), "Pay Stubs"),

    # Other
    (os.path.join(PERSONAL, "Child Support.xlsx"), "Other"),
    (os.path.join(PERSONAL, "Horne - Travel.xlsx"), "Other"),
]


def collect_files():
    """Resolve all glob patterns and return list of (source, dest_dir, filename) tuples."""
    results = []
    seen = set()
    for pattern, dest_subfolder in MAPPINGS:
        matches = glob.glob(pattern)
        for src in sorted(matches):
            if not os.path.isfile(src):
                continue
            filename = os.path.basename(src)
            dest_dir = os.path.join(FR, dest_subfolder)
            key = (src, dest_dir, filename)
            if key not in seen:
                seen.add(key)
                results.append((src, dest_dir, filename))
    return results


def main():
    execute = "--execute" in sys.argv

    files = collect_files()
    if not files:
        print("No files found to migrate.")
        return

    # Group by destination for summary
    by_dest = {}
    for src, dest_dir, filename in files:
        subfolder = os.path.basename(dest_dir)
        by_dest.setdefault(subfolder, []).append((src, dest_dir, filename))

    # Print summary
    mode = "EXECUTING" if execute else "DRY RUN (use --execute to copy)"
    print(f"\nFinancial File Migration - {mode}")
    print("=" * 60)

    total = 0
    skipped = 0
    copied = 0

    for subfolder in sorted(by_dest.keys()):
        items = by_dest[subfolder]
        print(f"\n  {subfolder}/ ({len(items)} files)")
        for src, dest_dir, filename in items:
            dest_path = os.path.join(dest_dir, filename)
            exists = os.path.exists(dest_path)
            total += 1

            if exists:
                status = "SKIP (exists)"
                skipped += 1
            else:
                status = "COPY" if execute else "WOULD COPY"

            # Shorten source path for display
            short_src = src.replace(PERSONAL + "/", "")
            print(f"    {status}: {short_src} -> {subfolder}/{filename}")

            if execute and not exists:
                os.makedirs(dest_dir, exist_ok=True)
                shutil.copy2(src, dest_path)
                copied += 1

    print(f"\n{'=' * 60}")
    print(f"Total files: {total}")
    print(f"Skipped (already exist): {skipped}")
    if execute:
        print(f"Copied: {copied}")
    else:
        print(f"Would copy: {total - skipped}")
        print("\nRun with --execute to perform the copy.")


if __name__ == "__main__":
    main()
