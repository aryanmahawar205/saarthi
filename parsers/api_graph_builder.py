import json
import re

CONTEXT_FILE = "reports/repository_context.json"
OUTPUT_FILE = "reports/api_graph.json"


PATTERNS = [
    r'@GetMapping\("([^"]+)"\)',
    r'@PostMapping\("([^"]+)"\)',
    r'@PutMapping\("([^"]+)"\)',
    r'@DeleteMapping\("([^"]+)"\)',
    r'@RequestMapping\("([^"]+)"\)',
]


def extract_endpoints(java_file):

    endpoints = []

    try:

        with open(
            java_file,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            content = f.read()

        for pattern in PATTERNS:

            matches = re.findall(
                pattern,
                content
            )

            for match in matches:

                endpoints.append(
                    match
                )

    except Exception:
        pass

    return endpoints


def main():

    with open(CONTEXT_FILE) as f:

        context = json.load(f)

    api_graph = []

    for source_file in context[
        "source_files"
    ]:

        endpoints = extract_endpoints(
            source_file
        )

        if endpoints:

            api_graph.append({
                "file": source_file,
                "endpoints": endpoints
            })

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            api_graph,
            f,
            indent=2
        )

    total = sum(
        len(x["endpoints"])
        for x in api_graph
    )

    print(
        f"[+] API Files: {len(api_graph)}"
    )

    print(
        f"[+] Endpoints: {total}"
    )

    print(
        f"[+] Saved: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()