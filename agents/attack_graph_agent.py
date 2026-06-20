import json

OUTPUT_FILE = (
    "reports/attack_graph.json"
)


def run(state):

    graph = {

        "nodes": [],

        "edges": []
    }

    attack_paths = state.get(
        "attack_paths",
        []
    )

    for path in attack_paths:

        name = path.get(
            "name",
            "Attack"
        )

        graph["nodes"].append(
            name
        )

    for i in range(
        len(graph["nodes"]) - 1
    ):

        graph["edges"].append({

            "source":
                graph["nodes"][i],

            "target":
                graph["nodes"][i + 1]
        })

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            graph,
            f,
            indent=2
        )

    state[
        "attack_graph"
    ] = graph

    print(
        f"[AttackGraphAgent] "
        f"{len(graph['nodes'])} nodes"
    )

    return state