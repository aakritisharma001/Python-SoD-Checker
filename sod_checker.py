import argparse
import json
from itertools import combinations
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {"user_id", "name", "role", "department"}


def load_rules(source):
    if isinstance(source, dict):
        return source
    with open(source, encoding="utf-8") as file:
        return json.load(file)


def check_sod(users_csv, rules_source, output_csv):
    df = pd.read_csv(users_csv, dtype=str).fillna("")
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing CSV columns: {', '.join(sorted(missing))}")

    rules = load_rules(rules_source)
    conflicts = rules.get("incompatible_role_pairs", [])
    payment_terms = [term.lower() for term in rules.get("payment_keywords", ["payment", "pay", "wire"])]

    flagged = []
    for user_id, group in df.groupby("user_id", sort=False):
        roles = set(group["role"].str.strip())
        pairs = []
        high_risk = False

        for role_a, role_b in combinations(sorted(roles), 2):
            pair = {role_a, role_b}
            if any(pair == set(rule) for rule in conflicts):
                pairs.append(f"{role_a} ↔ {role_b}")
                text = f"{role_a} {role_b}".lower()
                high_risk |= any(term in text for term in payment_terms)

        if pairs:
            first = group.iloc[0]
            flagged.append({
                "user_id": user_id,
                "name": first["name"],
                "conflicting_roles": "; ".join(pairs),
                "risk_level": "High" if high_risk else "Medium",
            })

    report = pd.DataFrame(
        flagged,
        columns=["user_id", "name", "conflicting_roles", "risk_level"],
    )
    report.to_csv(output_csv, index=False)
    print(f"Flagged users: {len(report)}")
    print(f"High risk: {(report['risk_level'] == 'High').sum()}")
    print(f"Medium risk: {(report['risk_level'] == 'Medium').sum()}")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check user-role assignments for SoD conflicts.")
    parser.add_argument("--users", default="sample_users.csv", help="Input user-role CSV")
    parser.add_argument("--rules", default="rules.json", help="JSON rules file")
    parser.add_argument("--output", default="sod_report.csv", help="Output report CSV")
    args = parser.parse_args()
    check_sod(args.users, args.rules, args.output)
