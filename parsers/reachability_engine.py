import json


INPUT_FILE = "reports/linked_context.json"
OUTPUT_FILE = "reports/reachable_findings.json"


HIGH_VALUE_CALLS = {

    "execute",
    "exec",
    "query",
    "queryForObject",
    "queryForList",
    "save",
    "delete",
    "update",
    "sendRedirect",
    "forward",
    "getConnection",
    "prepareStatement",
    "createStatement",
    "Runtime",
    "ProcessBuilder",

}


def calculate_reachability(finding):

    calls = finding.get(
        "related_calls",
        []
    )

    score = 0

    for edge in calls:

        callee = edge.get(
            "callee",
            ""
        )

        if callee in HIGH_VALUE_CALLS:

            score += 20

    return score


def determine_exposure(score):

    if score >= 40:
        return "HIGH"

    if score >= 20:
        return "MEDIUM"

    return "LOW"


def main():

    with open(INPUT_FILE) as f:

        findings = json.load(f)

    for finding in findings:

        score = calculate_reachability(
            finding
        )

        finding[
            "reachability_score"
        ] = score

        finding[
            "exposure"
        ] = determine_exposure(
            score
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
        f"[+] Reachability Processed: "
        f"{len(findings)}"
    )

    print(
        f"[+] Saved: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()