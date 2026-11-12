# Python-Based Segregation of Duties (SoD) Checker

A Python-based **Segregation of Duties (SoD) Checker** that identifies incompatible role combinations within a multi-tenant SaaS Role-Based Access Control (RBAC) environment.

The project uses Python and Pandas to analyze user-role assignments, detect potential conflicts of interest, classify risks, and generate an automated CSV audit report.

## Project Overview

Segregation of Duties (SoD) is an internal security control that prevents a single user from holding combinations of responsibilities that could lead to unauthorized activities, fraud, or misuse of privileges.

For example:
- A user who can manage billing and administer the system may have excessive control.
- A user who performs billing activities and independently audits them may lack sufficient separation of responsibilities.

This project automates the identification of such incompatible role combinations using configurable SoD rules.

## Features

- **Data Integration:** Uses a combined dataset containing user IDs, names, roles, and departments.
- **Role-Based Conflict Detection:** Identifies users holding predefined incompatible role combinations.
- **Configurable Rules:** Stores incompatible role pairs and payment-related keywords in a JSON configuration file.
- **Risk Classification:** Categorizes detected conflicts into High and Medium risk levels.
- **Automated Reporting:** Generates a CSV report containing flagged users and their conflicting roles.
- **Data Analysis:** Uses Pandas for data processing, grouping, and role analysis.

## Technologies Used

- Python
- Pandas
- JSON
- CSV

## Project Structure

```text
Python-SoD-Checker/
│
├── sod_checker.py
├── employee_role_assignments.csv
├── rules.json
├── README.md
└── sod_report.csv
```

## Dataset

The project uses the Multi-Tenant SaaS RBAC Permissions dataset.

The original datasets include:

- `users.csv`
- `user_roles.csv`
- `departments.csv`
- `teams.csv`

These datasets were combined using their relationships to create `employee_role_assignments.csv`.

The final dataset contains four columns:

| Column | Description |
|---|---|
| user_id | Unique identifier of the user |
| name | User's name |
| role | Assigned role |
| department | Department associated with the user |

Each row represents one user-role assignment. Users with multiple roles appear in multiple rows.

### Dataset Statistics

- Total unique users: 491
- Total role assignments: 578
- Users with multiple roles: 87
- Duplicate user-role assignments: 0

## SoD Conflict Rules

The incompatible role combinations are maintained in `rules.json`.

The current proposed rules include:

| Incompatible Roles | Risk Level |
|---|---|
| billing + admin | High |
| billing + owner | High |
| billing + auditor | High |
| admin + auditor | Medium |

Payment-related keywords are also configured to identify High-risk combinations.

**Note:** These are proposed testing rules based on role names and responsibilities. They have not been independently verified against a detailed role-permission matrix or an approved organizational SoD policy.

## How It Works

1. **Load Data:** Reads user-role assignments from the CSV file using Pandas.
2. **Load Rules:** Reads incompatible role combinations and payment-related keywords from `rules.json`.
3. **Group Users:** Groups records by user ID to identify all roles assigned to each user.
4. **Detect Conflicts:** Checks whether a user's role combinations match any configured incompatible pairs.
5. **Classify Risk:** Assigns High risk to conflicts containing configured payment-related keywords; other detected conflicts are classified as Medium.
6. **Generate Report:** Exports the detected conflicts into `sod_report.csv`.

## Installation and Execution

### 1. Clone the Repository

```bash
git clone https://github.com/aakritisharma001/Python-SoD-Checker.git
```

### 2. Navigate to the Project Directory

```bash
cd Python-SoD-Checker
```

### 3. Install Dependencies

```bash
pip install pandas
```

### 4. Run the SoD Checker

```bash
python sod_checker.py --users employee_role_assignments.csv --rules rules.json --output sod_report.csv
```

## Sample Execution Results

The checker was executed against the combined dataset.

```text
Flagged users: 7
High risk: 5
Medium risk: 2
```

### Output Report

The generated `sod_report.csv` contains:

| Column | Description |
|---|---|
| user_id | ID of the flagged user |
| name | Name of the flagged user |
| conflicting_roles | Detected incompatible role combination |
| risk_level | High or Medium |

## Future Enhancements

- Integration with detailed role-permission mappings.
- Support for customizable risk levels and severity scoring.
- Detection of more complex multi-role conflicts.
- Interactive dashboards for visualizing SoD violations.
- Automated recommendations for resolving role conflicts.
- Support for larger enterprise RBAC datasets.

## Conclusion

This project demonstrates how Python and Pandas can be used to automate Segregation of Duties monitoring in a multi-tenant SaaS environment.

By identifying incompatible role combinations and generating structured audit reports, the system provides a foundation for improving access governance, reducing privilege-related risks, and strengthening internal security controls.

---

**Developed using Python and Pandas.**
