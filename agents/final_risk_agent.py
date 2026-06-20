import json

OUTPUT_FILE = (
    "reports/final_risk.json"
)


def calculate_risk(

    exploitability,
    impacts,
    attack_paths

):

    score = 0

    score += len(
        attack_paths
    ) * 2

    for finding in exploitability:

        score += finding.get(
            "exploitability_score",
            0
        )

    if score >= 30:
        return "CRITICAL"

    if score >= 20:
        return "HIGH"

    if score >= 10:
        return "MEDIUM"

    return "LOW"


def run(state):

    exploitability = state.get(
        "exploitability_analysis",
        []
    )

    impacts = state.get(
        "business_impacts",
        []
    )

    attack_paths = state.get(
        "attack_paths",
        []
    )

    overall_risk = calculate_risk(
        exploitability,
        impacts,
        attack_paths
    )

    result = {

        "overall_risk":
            overall_risk,

        "attack_paths":
            len(
                attack_paths
            ),

        "business_impacts":
            len(
                impacts
            ),

        "critical_findings":
            len([
                x
                for x in exploitability
                if x.get(
                    "priority"
                ) == "HIGH"
            ]),

        "recommended_fix_order": [

            "Fix XSS Issues",

            "Implement CSP",

            "Implement CSRF Protection",

            "Review Session Management",

            "Review Authentication Controls"
        ]
    }

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            result,
            f,
            indent=2
        )

    state[
        "final_risk"
    ] = result

    print(
        "[FinalRiskAgent]"
    )

    print(
        json.dumps(
            result,
            indent=2
        )
    )

    return state