import json
import os
import re

REPO_ROOT = "vulnerable_codebases/WebGoat"

OUTPUT_FILE = "reports/class_method_index.json"


CLASS_PATTERN = re.compile(
    r"class\s+([A-Za-z0-9_]+)"
)

METHOD_PATTERN = re.compile(
    r"(public|private|protected)\s+.*?\s+([A-Za-z0-9_]+)\s*\(",
    re.MULTILINE
)


def extract_class_and_methods(path):

    try:

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            content = f.read()

        class_match = CLASS_PATTERN.search(
            content
        )

        if not class_match:
            return None

        class_name = class_match.group(1)

        methods = []

        for match in METHOD_PATTERN.findall(
            content
        ):

            methods.append(
                match[1]
            )

        return {
            "file": path,
            "class": class_name,
            "methods": methods
        }

    except Exception:

        return None


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

            data = extract_class_and_methods(
                path
            )

            if data:

                results.append(
                    data
                )

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
        f"[+] Classes Indexed: "
        f"{len(results)}"
    )

    print(
        f"[+] Saved: "
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()