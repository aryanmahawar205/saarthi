import json

RISKS_FILE = "reports/enriched_risks.json"
PATHS_FILE = "reports/attack_paths.json"

OUTPUT_FILE = "reports/executive_report.md"


def write_header(f):

    f.write("# Saarthi Security Assessment\n\n")


def write_summary(f, risks, paths):

    critical = len([
        r for r in risks
        if r["priority"] == "CRITICAL"
    ])

    high = len([
        r for r in risks
        if r["priority"] == "HIGH"
    ])

    f.write("## Executive Summary\n\n")

    f.write(
        f"- Critical Risks: {critical}\n"
    )

    f.write(
        f"- High Risks: {high}\n"
    )

    f.write(
        f"- Attack Paths Identified: {len(paths)}\n\n"
    )


def write_top_risks(f, risks):

    f.write("## Top Risks\n\n")

    for risk in risks[:10]:

        f.write(
            f"### {risk['group_key']}\n"
        )

        f.write(
            f"- Priority: {risk['priority']}\n"
        )

        f.write(
            f"- Score: {risk['risk_score']}\n"
        )

        f.write(
            f"- Findings: {risk['finding_count']}\n\n"
        )

        examples = risk.get(
            "top_examples",
            []
        )

        if examples:

            f.write(
                "Evidence:\n\n"
            )

            for example in examples:

                title = example.get(
                    "title",
                    "Unknown"
                )

                file_name = example.get(
                    "file",
                    "Unknown"
                )

                f.write(
                    f"- {title}\n"
                )

                f.write(
                    f"  File: {file_name}\n\n"
                )

        f.write("\n")


def write_attack_paths(f, paths):

    f.write(
        "## Attack Paths\n\n"
    )

    for path in paths:

        f.write(
            f"### {path['name']}\n"
        )

        f.write(
            f"Impact: {path['impact']}\n\n"
        )

        f.write(
            "Chain:\n"
        )

        for c in path["components"]:

            f.write(
                f"- {c}\n"
            )

        f.write("\n")


def main():

    with open(RISKS_FILE) as f:
        risks = json.load(f)

    with open(PATHS_FILE) as f:
        paths = json.load(f)

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        write_header(f)

        write_summary(
            f,
            risks,
            paths
        )

        write_top_risks(
            f,
            risks
        )

        write_attack_paths(
            f,
            paths
        )

    print(
        f"[+] Report written to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()