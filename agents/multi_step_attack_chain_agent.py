import json

OUTPUT_FILE = (
    "reports/multi_step_attack_chains.json"
)


def run(state):

    incidents = state.get(
        "dast_incidents",
        []
    )

    chains = []

    names = [

        x.get(
            "incident",
            ""
        ).lower()

        for x in incidents
    ]

    if (

        any(
            "xss" in n
            for n in names
        )

        and

        any(
            "browser" in n
            or
            "csp" in n
            for n in names
        )
    ):

        chains.append({

            "chain":
                "Stored XSS -> Session Theft -> Account Takeover",

            "severity":
                "CRITICAL"
        })

    if any(
        "csrf" in n
        for n in names
    ):

        chains.append({

            "chain":
                "CSRF -> Unauthorized Action -> Privilege Abuse",

            "severity":
                "HIGH"
        })

    if any(
        "authentication" in n
        for n in names
    ):

        chains.append({

            "chain":
                "Authentication Weakness -> Session Hijacking",

            "severity":
                "HIGH"
        })

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            chains,
            f,
            indent=2
        )

    state[
        "multi_step_attack_chains"
    ] = chains

    print(
        f"[MultiStepAttackChainAgent] "
        f"{len(chains)} chains"
    )

    return state