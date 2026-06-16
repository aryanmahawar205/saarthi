import json
import os

REPO_ROOT = "vulnerable_codebases/WebGoat"

OUTPUT_FILE = "reports/repository_context.json"


JAVA_EXTENSIONS = (
    ".java",
    ".kt",
)

CONFIG_EXTENSIONS = (
    ".yml",
    ".yaml",
    ".properties",
    ".xml",
    ".json",
)

DOC_EXTENSIONS = (
    ".md",
    ".adoc",
    ".txt",
)


def build_context():

    context = {
        "source_files": [],
        "config_files": [],
        "documents": [],
        "pom_files": [],
    }

    for root, dirs, files in os.walk(REPO_ROOT):

        for file in files:

            path = os.path.join(root, file)

            if file == "pom.xml":
                context["pom_files"].append(path)

            elif file.endswith(JAVA_EXTENSIONS):
                context["source_files"].append(path)

            elif file.endswith(CONFIG_EXTENSIONS):
                context["config_files"].append(path)

            elif file.endswith(DOC_EXTENSIONS):
                context["documents"].append(path)

    return context


def main():

    context = build_context()

    with open(OUTPUT_FILE, "w") as f:

        json.dump(
            context,
            f,
            indent=2
        )

    print(
        f"[+] Source Files: "
        f"{len(context['source_files'])}"
    )

    print(
        f"[+] Config Files: "
        f"{len(context['config_files'])}"
    )

    print(
        f"[+] Documents: "
        f"{len(context['documents'])}"
    )

    print(
        f"[+] POM Files: "
        f"{len(context['pom_files'])}"
    )

    print(
        f"[+] Saved: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()