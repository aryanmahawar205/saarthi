import json

INPUT_FILE = "reports/reachable_findings.json"
OUTPUT_FILE = "reports/prioritized_findings_v2.json"

SEVERITY_SCORE = {
    "CRITICAL": 100,
    "HIGH": 75,
    "MEDIUM": 50,
    "LOW": 25
}


def calculate_score(finding):

    severity = finding.get(
        "severity",
        "LOW"
    )

    score = SEVERITY_SCORE.get(
        severity,
        25
    )

    score += finding.get(
        "reachability_score",
        0
    )

    return score


def determine_priority(score):

    if score >= 120:
        return "CRITICAL"

    if score >= 90:
        return "HIGH"

    if score >= 60:
        return "MEDIUM"

    return "LOW"


def main():

    with open(INPUT_FILE) as f:
        findings = json.load(f)

    for finding in findings:

        score = calculate_score(
            finding
        )

        finding[
            "final_score"
        ] = score

        finding[
            "priority"
        ] = determine_priority(
            score
        )

    findings.sort(
        key=lambda x:
        x["final_score"],
        reverse=True
    )

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            findings,
            f,
            indent=2
        )

    print(
        f"[+] Prioritized: {len(findings)}"
    )

    print(
        f"[+] Output: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()