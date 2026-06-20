import json


OUTPUT_FILE = (
    "reports/runtime_reasoning.json"
)


def determine_risk(

    incidents,
    attack_paths

):

    if len(
        attack_paths
    ) >= 4:

        return "HIGH"

    if len(
        attack_paths
    ) >= 2:

        return "MEDIUM"

    return "LOW"


def run(state):

    incidents = state.get(
        "dast_incidents",
        []
    )

    attack_paths = state.get(
        "attack_paths",
        []
    )

    endpoints = state.get(
        "discovered_endpoints",
        []
    )

    result = {

        "risk_level":
            determine_risk(
                incidents,
                attack_paths
            ),

        "attack_surface_size":
            len(endpoints),

        "incident_count":
            len(incidents),

        "attack_path_count":
            len(attack_paths),

        "exposed_assets":
            endpoints[:20],

        "recommended_actions": [

            "Enable CSP",

            "Enable CSRF protection",

            "Review session management",

            "Review authentication controls"
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
        "runtime_reasoning"
    ] = result

    print(
        "[RuntimeReasoningAgent]"
    )

    print(
        json.dumps(
            result,
            indent=2
        )
    )

    return state