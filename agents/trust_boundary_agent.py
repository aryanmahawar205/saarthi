import json


OUTPUT_FILE = (
    "reports/trust_boundaries.json"
)


def run(state):

    endpoints = state.get(
        "discovered_endpoints",
        []
    )

    boundaries = []

    if endpoints:

        boundaries.append({

            "source":
                "Internet",

            "target":
                "Web Application",

            "boundary":
                "External Input"
        })

    if state.get(
        "assessment_plan",
        {}
    ).get(
        "contains_authentication"
    ):

        boundaries.append({

            "source":
                "Web Application",

            "target":
                "Authentication Layer",

            "boundary":
                "Identity Boundary"
        })

    if state.get(
        "assessment_plan",
        {}
    ).get(
        "contains_database"
    ):

        boundaries.append({

            "source":
                "Application Layer",

            "target":
                "Database",

            "boundary":
                "Data Access Boundary"
        })

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            boundaries,
            f,
            indent=2
        )

    state[
        "trust_boundaries"
    ] = boundaries

    print(
        f"[TrustBoundaryAgent] "
        f"{len(boundaries)} boundaries"
    )

    return state