import json


API_GRAPH = (
    "reports/api_graph.json"
)

CALL_GRAPH = (
    "reports/call_graph.json"
)

OUTPUT_FILE = (
    "reports/api_call_chains.json"
)


def load_json(path):

    with open(path) as f:
        return json.load(f)


def run(state):

    apis = load_json(
        API_GRAPH
    )

    calls = load_json(
        CALL_GRAPH
    )

    chains = []

    for api in apis:

        endpoints = api.get(
            "endpoints",
            []
        )

        file_name = api.get(
            "file",
            ""
        )

        related_calls = []

        file_token = (
            file_name
            .split("/")[-1]
            .replace(".java", "")
        )

        for call in calls:

            caller = call.get(
                "caller",
                ""
            )

            callee = call.get(
                "callee",
                ""
            )

            if (
                file_token.lower()
                in caller.lower()
            ):

                related_calls.append({

                    "caller":
                        caller,

                    "callee":
                        callee
                })

        chains.append({

            "file":
                file_name,

            "endpoints":
                endpoints,

            "call_chain":
                related_calls[:50]
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
        "api_call_chains"
    ] = chains

    print(
        f"[APICallChainAgent] "
        f"{len(chains)} chains"
    )

    return state