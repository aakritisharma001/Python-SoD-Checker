# Python SoD Checker

A small pandas-based Segregation of Duties (SoD) checker. It reads one row per
user-role assignment, detects incompatible role pairs, and writes a CSV report.

## Requirements

- Python 3.9+
- pandas

Install pandas:

```bash
python -m pip install pandas
```

## Run

From this directory:

```bash
python sod_checker.py
```

Or specify files:

```bash
python sod_checker.py --users sample_users.csv --rules rules.json --output sod_report.csv
```

The report contains `user_id`, `name`, `conflicting_roles`, and `risk_level`.
A conflict is **High** if either role name contains a configured payment keyword
(case-insensitive); otherwise it is **Medium**. The script prints total, High,
and Medium flagged-user counts.

## Rules format

`rules.json` contains `incompatible_role_pairs`, a list of two-role arrays, and
optional `payment_keywords`. Role names must match the CSV values exactly.

## Sample

The included sample flags U001 (Create Payment / Approve Payment) and U002
(Create Vendor / Pay Vendor). U001 and U002 are High risk; U003 and U004 are
not flagged.
