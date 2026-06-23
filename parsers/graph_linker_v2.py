import json
import os

CONTEXT_PACKS = "reports/context_packs.json"
METHOD_INDEX = "reports/method_index.json"
CALL_GRAPH = "reports/call_graph.json"

OUTPUT_FILE = "reports/linked_context.json"


def load_json(path):

    with open(path) as f:
        return json.load(f)


def build_method_lookup(index):

    lookup = {}

    for item in index:

        filename = os.path.basename(
            item["file"]
        )

        lookup[filename] = item["methods"]

    return lookup


def main():
    if not os.path.exists(CONTEXT_PACKS):
        print(f"[!] {CONTEXT_PACKS} not found. Skipping linking.")
        with open(OUTPUT_FILE, "w") as f:
            json.dump([], f)
        return

    contexts = load_json(
        CONTEXT_PACKS
    )

    method_index = []
    if os.path.exists(METHOD_INDEX):
        method_index = load_json(
            METHOD_INDEX
        )

    call_graph = []
    if os.path.exists(CALL_GRAPH):
        call_graph = load_json(
            CALL_GRAPH
        )

    method_lookup = build_method_lookup(
        method_index
    )

    for ctx in contexts:

        filename = os.path.basename(
            ctx["file"]
        )

        methods = method_lookup.get(
            filename,
            []
        )

        related_calls = []

        for edge in call_graph:

            if edge["caller"] in methods:

                related_calls.append(
                    edge
                )

        ctx["methods"] = methods[:20]

        ctx["related_calls"] = \
            related_calls[:50]

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            contexts,
            f,
            indent=2
        )

    print(
        f"[+] Linked Contexts: "
        f"{len(contexts)}"
    )

    print(
        f"[+] Output: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()