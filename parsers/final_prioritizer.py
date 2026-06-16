import json

INPUT_FILE = "reports/reachable_findings.json"
OUTPUT_FILE = "reports/final_prioritized_findings.json"


SEVERITY_SCORES = {
    "CRITICAL": 50,
    "HIGH": 40,
    "MEDIUM": 20,
    "LOW": 10
}


ATTACK_SURFACE_SCORES = {
    "APPLICATION_CODE": 20,
    "CI_PIPELINE": 15,
    "DEPENDENCY": 10,
    "CONFIGURATION": 10
}


ATTACK_PATH_KEYWORDS = [
    "CWE-78",
    "CWE-89",
    "CWE-502",
    "CWE-918",
    "CWE-434",
    "CWE-321",
    "SQL",
    "Command Injection",
    "Deserialization"
]


def calculate_score(finding):

    score = 0

    score += SEVERITY_SCORES.get(
        finding.get("severity", "LOW"),
        10
    )

    score += finding.get(
        "reachability_score",
        0
    )

    asset_type = finding.get(
        "asset_type",
        ""
    )

    score += ATTACK_SURFACE_SCORES.get(
        asset_type,
        0
    )

    exposure = finding.get(
        "exposure",
        "LOW"
    )

    if exposure == "HIGH":
        score += 30

    elif exposure == "MEDIUM":
        score += 15

    title = finding.get(
        "title",
        ""
    )

    for keyword in ATTACK_PATH_KEYWORDS:

        if keyword.lower() in title.lower():

            score += 25
            break

    return score


def priority(score):

    if score >= 100:
        return "CRITICAL"

    if score >= 80:
        return "HIGH"

    if score >= 50:
        return "MEDIUM"

    return "LOW"


def main():

    with open(INPUT_FILE) as f:
        findings = json.load(f)

    results = []

    for finding in findings:

        final_score = calculate_score(
            finding
        )

        finding[
            "final_score"
        ] = final_score

        finding[
            "priority"
        ] = priority(
            final_score
        )

        results.append(
            finding
        )

    results.sort(
        key=lambda x:
        x["final_score"],
        reverse=True
    )

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            results,
            f,
            indent=2
        )

    print(
        f"[+] Prioritized {len(results)} findings"
    )

    print(
        f"[+] Output: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()