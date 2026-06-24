import json
import os

FINDINGS_FILE = "reports/all_findings_normalized.json"
API_FILE = "reports/api_graph.json"
OUTPUT_FILE = "reports/mapped_findings.json"


def load_json(path):

    with open(path) as f:
        return json.load(f)


def build_api_lookup(api_graph):

    lookup = {}

    for entry in api_graph:

        file_name = os.path.basename(
            entry["file"]
        )

        lookup[file_name] = \
            entry["endpoints"]

    return lookup


def enrich_finding(
    finding,
    api_lookup
):

    file_path = (
        finding.get("location")
        or finding.get("file")
        or ""
    )

    file_name = os.path.basename(
        file_path
    )

    endpoints = api_lookup.get(
        file_name,
        []
    )

    finding["repository_context"] = {

        "file": file_name,

        "api_endpoints":
            endpoints

    }

    return finding


def main():
    if not os.path.exists(FINDINGS_FILE):
        print(f"[!] {FINDINGS_FILE} not found. Skipping mapping.")
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

    api_lookup = \
        build_api_lookup(
            api_graph
        )

    enriched = []

    for finding in findings:

        enriched.append(

            enrich_finding(
                finding,
                api_lookup
            )
        )

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            enriched,
            f,
            indent=2
        )

    print(
        f"[+] Findings: {len(enriched)}"
    )

    print(
        f"[+] Saved: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()