# TISA Monitoring Skill

## Description
Monitor and analyze Tennessee Investment in Student Achievement (TISA) funding data for Greeneville City Schools (District 301). Compare SWORD current data against monthly TISA estimates, track ADM trends, flag discrepancies, and produce funding impact analysis.

## Trigger
Activate when the user says "TISA", "SWORD", "ADM", "funding estimate", "TEDS", "base ADM", "ED ADM", "funding projection", or references TISA-related files or reports.

## Arguments
- "monitor" or "check" -- compare latest SWORD data against most recent TISA estimate
- "trend" -- show ADM trends across reporting periods
- "compare" -- side-by-side SWORD vs estimate analysis
- "ed" -- ED-specific analysis (hold harmless, regional comparison)
- "school [name]" -- school-level detail
- "pull" -- guidance on pulling fresh SWORD data
- File path to a new SWORD export or TISA estimate to analyze

## Key Directories

```
~/Library/CloudStorage/OneDrive-GreenevilleCitySchools/Finance/TISA/
  ├── FY27 TISA Reports/           # Current year estimates and projections
  │   ├── March Projection/        # Latest estimate files
  │   ├── February Projection/
  │   ├── GCS_FY27_TISA_Prediction_updated.xlsx   # Julie's analysis workbook
  │   └── Greeneville_301_TISA_FY27_*.xlsx/pdf     # State-generated files
  ├── FY26 Outcomes/                # Prior year final outcomes and bonuses
  ├── FY25 TISA Reports/           # Historical
  ├── FY24 TISA Reports/           # Historical
  ├── ED Research/                  # ED code analysis and peer comparisons
  ├── TEDS Reports 25-26/          # TEDS base ADM exports
  └── Reports/                      # Misc (TACIR, etc.)

~/Downloads/sword/                  # SWORD exports (dated files)
```

## GCS District and School Codes

| Combo Code | School | Grades | Notes |
|-----------|--------|--------|-------|
| 301-8 | C. Hal Henard Elementary (HH) | K-5 | |
| 301-15 | EastView Elementary (EV) | K-5 | March 2026: K-2 ADM dip Mar 6-19 |
| 301-20 | Greeneville High School (GHS) | 9-12 | Largest school by ADM |
| 301-25 | Greeneville Middle School (GMS) | 6-8 | |
| 301-30 | Highland Elementary (HI) | K-5 | Smallest traditional elementary |
| 301-33 | TOPS Greeneville | K-12 | Virtual school, all grades, tiny ED |
| 301-35 | Tusculum View Elementary (TV) | K-5 | |
| 301-4850 | GCTA | CTE | CTE center for GHS students |
| 301-45 | Greeneville Special Ed Service School | K, 7 | Cost center only (~1 ADM) |

## TISA Data Flow and Timing

```
PowerSchool (SIS) --> SWORD (state warehouse) --> TEDS weekly files (TNShare)
                                                      |
                                          Monthly pull on the 16th
                                                      |
                                              TISA Estimate Letter
                                           (prelim xlsx + pdf)
```

### Critical Calendar
- **Weekly**: TEDS ADM files posted to TNShare (Julie downloads these)
- **16th of each month**: State pulls SWORD snapshot for that month's TISA estimate
- **~End of month**: TISA estimate letter and data files released
- **Fiscal year**: July 1 - June 30
- **9 Reporting Periods**: Correspond to roughly monthly windows during the school year

### Why Timing Matters
The March 2026 incident: EastView K-2 ADM was reported at roughly half their actual counts in the March Preliminary state file. Grades K, 1, and 2 showed ~21-26 ADM each instead of ~59-64. This was caught during the April projection update by cross-checking student-level aggregates against the state file. The error affected Base ADM (2,724 vs correct ~2,838) and K-3 Literacy (788 vs correct ~900). Always cross-check school/grade totals when merging new data.

**Action**: Monitor SWORD/TEDS weekly in the days before the 16th. If ADM looks wrong, fix it in PowerSchool before the pull date.

## TISA Funding Formula (FY27)

### Base Funding
- Base amount per student: **$7,530** (FY27), up from $7,295 (FY26)
- Applied to Base ADM (average daily membership across reporting periods)

### Weights (multiplied by base amount, applied to qualifying ADM)
| Weight Category | Description |
|----------------|-------------|
| Economically Disadvantaged (ED) | Students qualifying via direct cert (SNAP, foster, homeless, etc.) |
| Concentrated Poverty (CP) | Schools above poverty threshold |
| English Learners (EL) | Students with EL status |
| Students with Disabilities (ULN 1-10) | By ULN option/service level |
| K-3 Literacy | Early literacy support |
| 4th Grade Supports | Transition year support |
| Small/Sparse | Small district and geographic sparsity adjustments |
| CTE | By level (1-4) and year, higher funding for advanced CTE |

### Key FY27 Provisions
- **ED Hold Harmless**: 100% (FY27), was 75% in FY26. This is critical -- actual ED ADM is ~440 but hold harmless applies FY26 baseline (~864), nearly doubling the funded ED count.
- **Funding Floor**: Ensures district doesn't lose more than a set % year-over-year. GCS is currently on the funding floor.
- **High Performing LEA Bonus**: Based on school letter grades. GCS has 6 eligible schools, 4 "A" schools. Qualifies for $1M tier, pro-rated at ~$607K.
- **Outcome Bonuses**: Performance-based (TCAP growth, ACT benchmarks, EPSO credits). FY26 total: $307,119.50.

### FY27 Known Risks (from Julie's prediction workbook)
| Risk | Impact | Status |
|------|--------|--------|
| ED ADM decline (51.5% drop from FY26) | High | Mitigated by 100% hold harmless |
| CTE ADM decline (~$63K loss) | High | Monitor CTE enrollment |
| ULN 9 decline (~$111K) | Moderate | Track SPED placements |
| High-cost CTE dropped to 0 | Moderate | No Level 4 CTE programs |
| Base ADM down 4.7% from FY26 | High | Enrollment trend, funding floor applies |

## SWORD Export File Structures

### SWORD ADM Data (sword adm data [date].xlsx)
- **Granularity**: School x Grade level
- **Columns**: School Code, School Year, District, School Name, Grade, Period 1-9 ADM, Report Period Average
- **Use**: Current ADM by school and grade, period-over-period trends

### ED Data (ed data [date].xlsx)
- **Granularity**: School x Grade level
- **Columns**: Similar to ADM but for ED-qualifying students only
- **Use**: Track ED ADM, compare to hold harmless baseline

### Submitted Base ADM Report (submitted base adm report [date].xlsx)
- **Note**: May export as empty stub if filters are wrong. Verify SWORD export settings.
- **Expected content**: Student-level base ADM with entry/exit dates and per-period values

### SPED Data (sped data [date].xlsx)
- **Note**: May export as empty stub. Check SWORD filters.
- **Expected content**: Student-level SPED data with ULN option assignments

### CTE Data (cte data [date].xlsx)
- **Note**: May export as empty stub. Check SWORD filters.
- **Expected content**: Student-level CTE enrollment by program/level/year

### Weekly Student-Level Downloads (for /tisa update projection)

These are the files Jason downloads weekly. They land in ~/Downloads/:

**Base ADM by Student.xlsx** (+ data.xlsx aggregated version)
- Skip 2 rows (title + headers). Columns: School Code, School Year, District Number, (blank), District Name, School Number, School Name, EdFi ID, Legacy ID, First Name, Last Name, Grade, Entry Date, Withdraw Date, 1-9 (period columns), Report Period Average
- Includes P3/P4 (Pre-K) and Sped Service School (301-4850)
- data.xlsx has same data pre-aggregated by school+grade

**SPED ADM by Student.xlsx**
- Skip 2 rows. Same base columns plus Option, Primary Indicator
- Includes P and S (primary/secondary) service records
- **Pre-K (P3/P4) must be filtered out** -- in SWORD but not TISA-funded
- One row per student-option (pre-aggregated); state file may have multiple enrollment segments
- EdFi IDs use a different format than the state projection file

**CTE ADM by Student.csv** (or .xlsx)
- CSV has headers in row 0. Columns: school_code, school_year, district_id, DISTRICT_NAME, school_id, SCHOOL_NAME, eduid, legacy_id, first_name, last_name, grade_level_adm, entry_date, exit_withdraw_date, type_of_service, course_code, ID1-ID9, Textbox15 (student avg), Textbox67 (district avg)
- **Course codes differ from state projection** (e.g., C25X06 vs C25600). Cannot match row-by-row on course.
- May have multiple rows per (student, course) -- sum period values across segments
- legacy_id = state_student_id in the projection

## State-Generated TISA Estimate Files (MarPrelim, FebPrelim, etc.)

### Key Sheets in the Prelim xlsx
| Sheet | Purpose | What to Check |
|-------|---------|---------------|
| 9 Period Summary | ADM by category across all periods | Period-over-period trends, avg vs FY26 final |
| TISA Calc | Full funding calculation | Total allocation, state/local split |
| Base_ADM | School x grade x period detail | Spot ADM drops by school |
| ED_ADM | Student-level ED eligibility | Compare count to SWORD ED data |
| District$ | One-row funding summary (74 columns) | Total TISA, weights, direct allocations |
| SchoolCounts | School-level ADM by grade, all periods | Cross-check with SWORD |
| Support Provisions | Funding floor and safety net | Whether floor is active |

## Instructions

### Mode: Monitor / Check
Compare the latest SWORD export against the most recent TISA estimate.

1. Find the most recent files:
   - SWORD exports in `~/Downloads/sword/` (look for latest date)
   - TISA estimate in the current FY folder (e.g., `FY27 TISA Reports/March Projection/`)
2. Read both with Python (openpyxl). Use `/opt/anaconda3/bin/python3`.
3. Compare base ADM totals: SWORD current vs estimate snapshot
4. Compare ED ADM: SWORD current vs estimate, note hold harmless impact
5. Flag any school where the difference exceeds 5% or 10 ADM
6. Calculate estimated funding impact of the difference: `ADM_diff x $7,530`
7. Report in a clean table with school-level breakdown

### Mode: Trend
Show ADM movement across reporting periods.

1. Read the 9 Period Summary from the latest TISA estimate file
2. Plot or table: Base ADM, ED ADM, CTE ADM by period
3. Flag any period-over-period drops > 2%
4. Compare current period average to FY26 final (% change column exists in file)

### Mode: ED Analysis
Deep dive on Economically Disadvantaged funding.

1. Read ED data from SWORD export and TISA estimate ED_ADM sheet
2. Show current ED ADM vs hold harmless baseline
3. Calculate funding difference: `(hold_harmless_ADM - actual_ED_ADM) x ED_weight x $7,530`
4. Reference regional peer comparison from `ED Research/ED_State_Change.xlsx`:
   - GCS down 51.5%, Johnson City down 45.3%, Hamblen down 12.3%
   - Sullivan County is the outlier (+13.4%)
5. Note: ED decline is driven by changes to MF and MR eligibility codes at the state level, not local enrollment changes

### Mode: School Detail
Drill into a specific school.

1. Filter SWORD ADM and ED data for the requested school code
2. Show grade-level ADM breakdown with period trends
3. Compare to same school in the TISA estimate
4. Flag any grades with ADM below expected (compare to prior year if available)

### Mode: Pull Guidance
Help the user pull fresh data from SWORD.

SWORD is accessed via web browser at the TN DOE portal. It is NOT an API -- data must be exported manually through the SWORD interface.

Steps:
1. Log into SWORD through the TN DOE portal
2. Select School Year 2025-2026 and District 301
3. For each report type (Base ADM, ED, SPED, CTE), export to xlsx
4. Save to `~/Downloads/sword/` with naming convention: `[report type] [date].xlsx`
   - Examples: `sword adm data 3-26-2026.xlsx`, `ed data 3-26-2026.xlsx`
5. If a file exports as an empty stub (header row only, no data), check:
   - School year filter is set correctly
   - District filter shows 301 - Greeneville City
   - The report view has been submitted/refreshed before exporting

**Recommended timing**: Pull SWORD data on the 14th-15th of each month (before the state's monthly pull on the 16th) and again at end of month (to compare against the released estimate).

### Mode: Update Projection (Weekly)
Update the TISA projection file with new period data from SWORD student-level downloads.

**Inputs (downloaded from SWORD weekly):**
- `Base ADM by Student.xlsx` -- student-level base ADM
- `data.xlsx` -- aggregated base ADM by school+grade (same data, pre-pivoted)
- `SPED ADM by Student.xlsx` -- student-level SPED with options
- `CTE ADM by Student.csv` or `.xlsx` -- student-level CTE with course codes
- Current TISA projection file (state-generated xlsx with Base_ADM, ED_ADM, SPED_ADM, EL_ADM, CoD_ADM, CTE_ADM, SchoolCounts, 9 Period Summary, TISA Calc sheets)

**CRITICAL: All updates must happen in a single openpyxl wb load/save cycle.** Loading the file in a second script and saving will overwrite changes from the first script.

**Steps:**

1. **Backup** the original TISA projection file (append `_BACKUP_YYYYMMDD`).

2. **Cross-check data before merging** (CRITICAL):
   - Aggregate ALL periods from the new student-level data by school + grade
   - Compare rp_1 through rp_N against the existing Base_ADM values
   - Flag any school/grade where old vs new differ by more than ~5 students
   - If discrepancies exist, replace ALL period data from the new source, not just the new period
   - See `feedback_tisa_data_validation.md` for why this matters (Eastview incident, April 2026)
   - **SPED**: Exclude Pre-K (P3/P4) students -- they appear in SWORD but are NOT in TISA calculations (confirmed TDASC Apr 2026 and JC TISA Guide). The existing projection already excludes them.
   - **CTE**: Course codes differ between SWORD exports and state projection files (e.g., C25X06 vs C25600). Do NOT match CTE row-by-row on (ssid, course_code). Use school-level ratio scaling instead.

3. **Update Base_ADM sheet**:
   - Aggregate student-level data by school_name + grade_level for each reporting period
   - Fill in all period columns (rp_1 through rp_N)
   - Set average column = student-level average aggregates (sum of individual averages)
   - Add rows for any new school/grade combinations (e.g., Special Ed Service School)
   - Set cp_eligible (col U) = 'Y' for eligible rows, virtual (col S) = 'Y' for TOPS

3b. **Update SPED_ADM sheet** (when SPED student-level download available):
   - Filter out Pre-K grades (P3, P4) -- these are in SWORD but NOT funded by TISA
   - The new file has 1 row per student-option; the existing may have multiple rows per student (enrollment segments). Both are valid formats -- full reload is fine.
   - Clear existing SPED_ADM data rows and write new data
   - Only populate periods with actual data (e.g., rp_1 through rp_7 for RP7). Leave future periods as None.
   - Recalculate average = sum(filled periods) / N
   - Column layout: geo_lea(1), combo_code(2), school_year(3), district_id(4), district_name(5), school_id(6), school_name(7), edfi_id(8), state_student_id(9), first_name(10), last_name(11), grade_level(12), option(13), primary_indicator(14), service_begin(15), service_end(16), rp_1(17)..rp_9(25), average(26)

3c. **Update CTE_ADM sheet** (when CTE student-level download available):
   - WARNING: SWORD CTE exports use different course codes than the state projection file (e.g., C25X06 vs C25600, C25801 vs C25X08). Row-level matching by (ssid, course_code) WILL FAIL.
   - Instead, use school-level ratio scaling: for each school, compute ratio = new_school_P7_total / old_school_P6_total, then apply to each existing row: new_P7 = old_P6 * ratio
   - This preserves the existing funding tier assignments (which are not in the SWORD export)
   - Recalculate average = sum(filled periods) / N
   - Column layout: geo_lea(1), combo_code(2), school_year(3), district_id(4), district_name(5), school_id(6), school_name(7), edfi_id(8), state_student_id(9), first_name(10), last_name(11), grade_level(12), course_code(13), rp_1(14)..rp_9(22), average(23), funding_tier(24), cte_funding_tier(25), cte_additional(26)
   - CTE Crosswalk sheet maps course_code -> funding tier (for any new rows that need tier assignment)

4. **Project weight category Period N** (if state hasn't released weight data):
   - For ED_ADM, EL_ADM, CoD_ADM (when no student-level download available):
     - Set each student's rp_N = their rp_(N-1) value (present last period = present this period)
     - Recalculate average = sum(rp_1..rp_N) / N
   - Column layouts vary by sheet:
     - ED_ADM: rp_1=col13, rp_7=col19, avg=col22
     - EL_ADM: rp_1=col17, rp_7=col23, avg=col26, el_tier=col28
     - CoD_ADM: rp_1=col13, rp_7=col19, avg=col22

5. **Update SchoolCounts sheet** (all static values, not formulas):
   - Grade-level columns (H=K, I=1, ..., T=12): set to Base_ADM averages by school+grade
   - total_adm (U=21): sum of grade averages per school
   - cp (X=24): same as total_adm for non-virtual schools, 0 for TOPS
   - k-3_literacy (AO=41): sum of Base_ADM averages for grades K, 01, 02, 03 per school
     - Per TISA Guide: "same data pull used in the base ADM, filtered down to K-3 grades"
   - 4th_grade_supports (AP=42): TCAP-based, actual student counts, do NOT recalculate
   - ed (V=22): aggregate from ED_ADM averages by combo_code
   - sped_1..sped_10 (AA=27..AJ=36): aggregate from SPED_ADM by combo_code and option
   - el_tier1..el_tier3 (AK=37..AM=39): aggregate from EL_ADM by combo_code and tier
   - cod (AN=40): aggregate from CoD_ADM by combo_code
   - CTE tiers (AQ=43..BB=54): aggregate from CTE_ADM by combo_code and funding_tier
   - cte_additional (BC=55): aggregate CTE_ADM where additional='Y'

6. **Verify** (run all checks):
   - Base_ADM period values match student-level aggregates
   - Averages = sum(periods) / N for every row in every ADM sheet
   - SchoolCounts totals match ADM sheet aggregates (base, ED, SPED, EL, CoD, CTE)
   - District total matches source file's Total sheet
   - Period totals match source pivot sheet
   - All formulas in TISA Calc and 9 Period Summary are intact (not overwritten with values)

7. **Generate comparison** vs prior projection:
   - Side-by-side table: element, old count, old funding, new count, new funding, change
   - Use $7,530 base, weight percentages, $500/student for K-3 and 4th grade, CTE tier rates
   - Include Outcomes and LEA Bonus as carry-forward estimates

**Formula chain (do not break):**
```
Base_ADM --> 9 Period Summary (SUMIFS formulas)
ED/SPED/EL/CoD_ADM --> 9 Period Summary (SUMIFS formulas)
SchoolCounts --> TISA Calc (SUMIFS formulas)
TISA Calc --> final funding numbers
```

**Things that auto-recalculate in Excel** (formula-driven):
- 9 Period Summary: all rows pull from ADM sheets via SUMIFS
- TISA Calc: C4 (base students) from SchoolCounts!U, T2 from C4, all weights from SchoolCounts

**Things that must be manually updated** (static values):
- Base_ADM: all period and average values
- All weight ADM sheets: period and average values
- SchoolCounts: all columns (grades, total_adm, weights, CTE tiers)

### General Analysis Notes
- **TDASC Training Materials** (April 2026): `OneDrive-GCS/Meeting Notes/TDASC/2025-2026/` contains TISA Funding Overview, Data Best Practices & Reconciliation, and Data Integrity & Troubleshooting docs
- Use `/opt/anaconda3/bin/python3` with openpyxl for all xlsx reading
- Never modify original state files -- copy to a working location if edits are needed
- Triple-check all funding calculations. ADM x base amount = raw funding, but weights and provisions change the final number significantly
- The funding floor provision means GCS may receive more than the formula calculates -- always check Support Provisions sheet
- When reporting dollar impacts, clarify whether it's a total or per-student figure
- ED hold harmless is the single biggest factor in FY27 funding stability. If hold harmless drops below 100% in future years, the ED decline becomes a major budget risk

## Terminology Quick Reference

| Term | Meaning |
|------|---------|
| ADM | Average Daily Membership -- funded student count |
| Base ADM | Total ADM across all students (not weighted) |
| ED | Economically Disadvantaged |
| CP | Concentrated Poverty (school-level threshold) |
| EL | English Learner |
| ULN | Unique Learning Need (SPED service options 1-10) |
| SWORD | Statewide Operations Reporting Dashboard (state data warehouse) |
| TEDS | TN Education Data System (weekly ADM files) |
| TNShare | State file-sharing portal where TEDS weekly files are posted |
| SIS | Student Information System (PowerSchool for GCS) |
| Hold Harmless | Provision preventing funding loss from declining counts |
| Funding Floor | Minimum funding guarantee vs prior year |
| Reporting Period (RP) | ~Monthly ADM measurement windows (9 per year) |
| Combo Code | District-School identifier (e.g., 301-20 = GHS) |
| MF/MR Codes | ED eligibility codes that changed at state level, driving ED decline |
| Direct Cert | Automatic ED qualification via SNAP, foster, homeless status |
| TISA Calc | Master funding calculation sheet in state estimate files |
| Prelim | Preliminary monthly estimate (e.g., MarPrelim = March estimate) |
| Outcomes | Performance-based bonus funding (TCAP growth, ACT, EPSO) |
