def run(state):

    endpoints = state.get(
        "discovered_endpoints",
        []
    )

    attack_surface = {

        "application_type":
            state.get(
                "assessment_plan",
                {}
            ).get(
                "application_type"
            ),

        "endpoint_count":
            len(endpoints),

        "endpoints":
            endpoints,

        "dast_findings":
            len(
                state.get(
                    "dast_findings",
                    []
                )
            ),

        "incidents":
            len(
                state.get(
                    "dast_incidents",
                    []
                )
            ),

        "attack_paths":
            len(
                state.get(
                    "attack_paths",
                    []
                )
            )
    }

    state[
        "attack_surface"
    ] = attack_surface

    print(
        "[AttackSurfaceAgent]"
    )

    print(
        attack_surface
    )

    return state