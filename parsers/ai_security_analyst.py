# version 1.0 - RULE BASED

import json

INPUT_FILE = "reports/llm_contexts.json"
OUTPUT_FILE = "reports/ai_analysis.json"


def business_impact(finding):

    title = finding["title"].lower()

    if "sql" in title:
        return "Database compromise"

    if "command" in title:
        return "Remote code execution"

    if "deserialization" in title:
        return "Remote code execution"

    if "jwt" in title:
        return "Authentication bypass"

    return "Security risk"


def remediation(finding):

    title = finding["title"].lower()

    if "sql" in title:
        return "Use parameterized queries"

    if "jwt" in title:
        return "Rotate secrets and remove hardcoded keys"

    if "deserialization" in title:
        return "Avoid unsafe deserialization"

    return "Review finding and apply secure coding practices"


def attack_scenario(finding):

    return (
        f"An attacker could exploit "
        f"{finding['title']} "
        f"to impact the application."
    )


def main():

    with open(INPUT_FILE) as f:
        findings = json.load(f)

    output = []

    for finding in findings:

        output.append({

            "finding_id":
                finding["finding_id"],

            "title":
                finding["title"],

            "business_impact":
                business_impact(
                    finding
                ),

            "attack_scenario":
                attack_scenario(
                    finding
                ),

            "remediation":
                remediation(
                    finding
                ),

            "priority":
                finding["priority"]
        })

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            output,
            f,
            indent=2
        )

    print(
        f"[+] AI Analyses: {len(output)}"
    )

    print(
        f"[+] Output: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()