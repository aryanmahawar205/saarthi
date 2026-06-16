import json
import os
import re

REPO_ROOT = "vulnerable_codebases/WebGoat"

OUTPUT_FILE = "reports/method_index.json"


METHOD_PATTERN = re.compile(
    r"(public|private|protected)\s+.*?\s+([a-zA-Z0-9_]+)\s*\(",
    re.MULTILINE
)


def extract_methods(path):

    methods = []

    try:

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            content = f.read()

        matches = METHOD_PATTERN.findall(
            content
        )

        for match in matches:

            methods.append(
                match[1]
            )

    except Exception:
        pass

    return methods


def main():

    results = []

    for root, dirs, files in os.walk(
        REPO_ROOT
    ):

        for file in files:

            if not file.endswith(".java"):
                continue

            path = os.path.join(
                root,
                file
            )

            methods = extract_methods(
                path
            )

            if methods:

                results.append({
                    "file": path,
                    "methods": methods
                })

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            results,
            f,
            indent=2
        )

    print(
        f"[+] Files Indexed: "
        f"{len(results)}"
    )

    print(
        f"[+] Saved: "
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()