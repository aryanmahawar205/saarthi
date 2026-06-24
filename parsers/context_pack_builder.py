import json
import os

FINDINGS_FILE = "reports/attack_surface_findings.json"
API_FILE = "reports/api_graph.json"

OUTPUT_FILE = "reports/context_packs.json"


def load_json(path):

    with open(path) as f:
        return json.load(f)


def get_api_context(file_path, api_graph):

    endpoints = []

    for api in api_graph:

        if os.path.basename(
            api["file"]
        ) == os.path.basename(
            file_path
        ):

            endpoints.extend(
                api["endpoints"]
            )

    return endpoints


def main():
    if not os.path.exists(FINDINGS_FILE):
        print(f"[!] {FINDINGS_FILE} not found. Skipping context pack building.")
        with open(OUTPUT_FILE, "w") as f:
            json.dump([], f)
        return

    findings = load_json(
        FINDINGS_FILE
    )

    api_graph = []
    if os.path.exists(API_FILE):
        api_graph = load_json(
            API_FILE
        )

    context_packs = []

    for finding in findings:

        file_path = finding.get(
            "file",
            ""
        )

        context_pack = dict(finding)

        context_pack["asset_type"] = (
            finding["attack_surface"]["asset_type"]
        )

        context_pack["api_endpoints"] = (
            get_api_context(
                file_path,
                api_graph
            )
        )

        context_packs.append(
            context_pack
        )

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            context_packs,
            f,
            indent=2
        )

    print(
        f"[+] Context Packs: "
        f"{len(context_packs)}"
    )

    print(
        f"[+] Output: "
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()