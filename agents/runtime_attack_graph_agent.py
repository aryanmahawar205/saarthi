import json

OUTPUT_FILE = (
    "reports/runtime_attack_graph.json"
)


def run(state):

    paths = []

    incidents = state.get(
        "dast_incidents",
        []
    )

    api_chains = state.get(
        "api_call_chains",
        []
    )

    for incident in incidents:

        incident_name = incident.get(
            "incident",
            ""
        )

        for chain in api_chains:

            paths.append({

                "incident":
                    incident_name,

                "endpoint":
                    chain.get(
                        "endpoints",
                        []
                    ),

                "file":
                    chain.get(
                        "file"
                    ),

                "call_depth":
                    len(
                        chain.get(
                            "call_chain",
                            []
                        )
                    )
            })

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            paths,
            f,
            indent=2
        )

    state[
        "runtime_attack_graph"
    ] = paths

    print(
        f"[RuntimeAttackGraphAgent] "
        f"{len(paths)} attack relationships"
    )

    return state