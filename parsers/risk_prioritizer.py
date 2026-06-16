import json

INPUT_FILE = "reports/contextualized_groups.json"
OUTPUT_FILE = "reports/prioritized_risks.json"


SEVERITY_WEIGHTS = {
    "CRITICAL": 100,
    "HIGH": 75,
    "MEDIUM": 50,
    "LOW": 25
}

GROUP_TYPE_MULTIPLIER = {
    "CWE": 1.0,
    "VULNERABILITY_CLASS": 0.9,
    "PACKAGE": 0.7
}

def calculate_risk_score(group):

    severity = group.get(
        "severity",
        "LOW"
    )

    finding_count = group.get(
        "finding_count",
        0
    )

    group_type = group.get(
        "group_type",
        "CWE"
    )

    severity_score = \
        SEVERITY_WEIGHTS.get(
            severity,
            25
        )

    count_bonus = min(
        finding_count,
        20
    )

    base_score = (
        severity_score +
        count_bonus
    )

    multiplier = \
        GROUP_TYPE_MULTIPLIER.get(
            group_type,
            1.0
        )

    exploitability_bonus = \
    group.get(
        "exploitability_bonus",
        0
    )

    final_score = int(
        (
            base_score *
            multiplier
        )
        +
        exploitability_bonus
    )

    return final_score


def determine_priority(score):

    if score >= 120:
        return "CRITICAL"

    elif score >= 90:
        return "HIGH"

    elif score >= 60:
        return "MEDIUM"

    return "LOW"


def main():

    with open(INPUT_FILE, "r") as f:
        groups = json.load(f)

    prioritized = []

    for group in groups:

        score = calculate_risk_score(
            group
        )

        group["risk_score"] = score

        group["priority"] = \
            determine_priority(score)

        prioritized.append(group)

    prioritized.sort(
        key=lambda x:
        x["risk_score"],
        reverse=True
    )

    with open(OUTPUT_FILE, "w") as f:

        json.dump(
            prioritized,
            f,
            indent=2
        )

    print(
        f"[+] Prioritized {len(prioritized)} groups"
    )

    print(
        f"[+] Saved to {OUTPUT_FILE}"
    )

    print(
        "\nTop 10 Risks:"
    )

    for group in prioritized[:10]:

        print(
            f"{group['group_id']} | "
            f"{group['group_key']} | "
            f"Score={group['risk_score']} | "
            f"{group['priority']}"
        )


if __name__ == "__main__":
    main()