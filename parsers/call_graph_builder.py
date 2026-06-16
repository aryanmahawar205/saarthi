import json
import os
import re

REPO_ROOT = "vulnerable_codebases/WebGoat"
CONTEXT_FILE = "reports/repository_context.json"
OUTPUT_FILE = "reports/call_graph.json"


METHOD_PATTERN = re.compile(
    r'(?:public|private|protected)\s+[\w\<\>\[\]]+\s+(\w+)\s*\([^)]*\)\s*\{',
    re.MULTILINE
)

CALL_PATTERN = re.compile(
    r'(\w+)\s*\('
)


IGNORE_CALLS = {
    "if",
    "for",
    "while",
    "switch",
    "catch",
    "return",
    "new",
    "super",
    "this",
    "try",
    "throw",
}


def load_source_files():

    with open(CONTEXT_FILE) as f:
        context = json.load(f)

    return context["source_files"]


def extract_calls(java_file):

    try:

        with open(
            java_file,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            content = f.read()

    except Exception:

        return []

    methods = list(
        METHOD_PATTERN.finditer(content)
    )

    edges = []

    for i, method in enumerate(methods):

        caller = method.group(1)

        start = method.end()

        if i < len(methods) - 1:
            end = methods[i + 1].start()
        else:
            end = len(content)

        body = content[start:end]

        calls = CALL_PATTERN.findall(body)

        seen = set()

        for callee in calls:

            if callee == caller:
                continue

            if callee in IGNORE_CALLS:
                continue

            if len(callee) < 3:
                continue

            edge_key = (caller, callee)

            if edge_key in seen:
                continue

            seen.add(edge_key)

            edges.append({
                "caller": caller,
                "callee": callee
            })

    return edges


def build_graph():

    files = load_source_files()

    graph = []

    for file in files:

        graph.extend(
            extract_calls(file)
        )

    return graph


def main():

    graph = build_graph()

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            graph,
            f,
            indent=2
        )

    print(
        f"[+] Call Edges: {len(graph)}"
    )

    print(
        f"[+] Saved: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()