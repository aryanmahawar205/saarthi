import json

FINDINGS_FILE = "reports/all_findings_normalized.json"
RISKS_FILE = "reports/prioritized_risks.json"

OUTPUT_FILE = "reports/enriched_risks.json"


def build_finding_lookup(findings):

    lookup = {}

    for finding in findings:

        finding_id = finding.get(
            "finding_id"
        )

        if finding_id:
            lookup[finding_id] = finding

    return lookup


def extract_example(finding):

    return {
        "finding_id": finding.get(
            "finding_id"
        ),

        "title": finding.get(
            "title",
            ""
        ),

        "severity": finding.get(
            "severity",
            ""
        ),

        "file": finding.get(
            "file",
            finding.get(
                "location",
                ""
            )
        ),

        "scanner": finding.get(
            "scanner",
            ""
        )
    }


def enrich_group(group, lookup):

    examples = []

    for finding_id in group.get(
        "findings",
        []
    )[:3]:

        finding = lookup.get(
            finding_id
        )

        if not finding:
            continue

        examples.append(
            extract_example(
                finding
            )
        )

    group["top_examples"] = examples

    return group


def main():

    with open(FINDINGS_FILE) as f:
        findings = json.load(f)

    with open(RISKS_FILE) as f:
        risks = json.load(f)

    lookup = build_finding_lookup(
        findings
    )

    enriched = []

    for group in risks:

        enriched.append(
            enrich_group(
                group,
                lookup
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
        f"[+] Enriched {len(enriched)} groups"
    )

    print(
        f"[+] Output: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()