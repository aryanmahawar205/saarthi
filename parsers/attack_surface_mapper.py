import json

INPUT_FILE = "reports/mapped_findings.json"
OUTPUT_FILE = "reports/attack_surface_findings.json"


def classify_asset(file_path):

    file_path = file_path.lower()

    if ".github/workflows" in file_path:
        return "CI_PIPELINE"

    if "controller" in file_path:
        return "API_ENDPOINT"

    if file_path.endswith("pom.xml"):
        return "DEPENDENCY"

    if any(
        x in file_path
        for x in [
            "application.yml",
            "application.yaml",
            ".properties",
        ]
    ):
        return "CONFIGURATION"

    return "APPLICATION_CODE"


def main():

    with open(INPUT_FILE) as f:
        findings = json.load(f)

    for finding in findings:

        file_path = finding.get(
            "file",
            ""
        )

        finding[
            "attack_surface"
        ] = {

            "asset_type":
                classify_asset(
                    file_path
                )
        }

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            findings,
            f,
            indent=2
        )

    print(
        f"[+] Findings: {len(findings)}"
    )

    print(
        f"[+] Output: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()