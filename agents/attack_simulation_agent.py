import json

OUTPUT_FILE = (
    "reports/attack_simulation.json"
)


def simulate(path):

    name = path.get(
        "name",
        ""
    ).lower()

    if "xss" in name:

        return {
            "success_probability": 0.85,
            "impact": "Account Takeover"
        }

    if "csrf" in name:

        return {
            "success_probability": 0.75,
            "impact": "Unauthorized Actions"
        }

    if "authentication" in name:

        return {
            "success_probability": 0.90,
            "impact": "Account Compromise"
        }

    return {
        "success_probability": 0.40,
        "impact": "Information Disclosure"
    }


def run(state):

    attack_paths = state.get(
        "attack_paths",
        []
    )

    simulations = []

    for path in attack_paths:

        simulations.append({

            "attack_path":
                path,

            **simulate(path)
        })

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            simulations,
            f,
            indent=2
        )

    state[
        "attack_simulations"
    ] = simulations

    print(
        f"[AttackSimulationAgent] "
        f"{len(simulations)} simulations"
    )

    return state