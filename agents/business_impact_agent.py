import json

OUTPUT_FILE = (
    "reports/business_impact.json"
)


def determine_impact(
    incident_name
):

    name = incident_name.lower()

    if "xss" in name:

        return {
            "business_impact":
                "Account Takeover",

            "risk":
                "HIGH",

            "affected_assets":
                "Authenticated Users"
        }

    if "csrf" in name:

        return {
            "business_impact":
                "Unauthorized Actions",

            "risk":
                "HIGH",

            "affected_assets":
                "Authenticated Users"
        }

    if "authentication" in name:

        return {
            "business_impact":
                "Unauthorized Access",

            "risk":
                "HIGH",

            "affected_assets":
                "Authentication System"
        }

    if "session" in name:

        return {
            "business_impact":
                "Session Hijacking",

            "risk":
                "HIGH",

            "affected_assets":
                "User Sessions"
        }

    return {
        "business_impact":
            "Information Disclosure",

        "risk":
            "MEDIUM",

        "affected_assets":
            "Web Application"
    }


def run(state):

    incidents = state.get(
        "dast_incidents",
        []
    )

    impacts = []

    for incident in incidents:

        name = incident.get(
            "incident",
            "Unknown"
        )

        impacts.append({

            "incident":
                name,

            **determine_impact(
                name
            )
        })

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            impacts,
            f,
            indent=2
        )

    state[
        "business_impacts"
    ] = impacts

    print(
        f"[BusinessImpactAgent] "
        f"{len(impacts)} impacts generated"
    )

    return state