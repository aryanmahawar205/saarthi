import json
from collections import defaultdict

INPUT_FILE = "reports/all_findings_normalized.json"
OUTPUT_FILE = "reports/correlated_findings.json"


groups = []
group_counter = 1


def create_group(group_type, key, findings):

    global group_counter

    group = {
        "group_id": f"GROUP-{group_counter:03d}",
        "group_type": group_type,
        "group_key": key,
        "finding_count": len(findings),
        "severity": highest_severity(findings),
        "findings": [
            f["finding_id"]
            for f in findings
        ]
    }

    group_counter += 1

    return group


def highest_severity(findings):

    ranking = {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1
    }

    highest = "LOW"

    for finding in findings:

        sev = finding.get(
            "severity",
            "LOW"
        )

        if ranking.get(
            sev,
            0
        ) > ranking.get(
            highest,
            0
        ):
            highest = sev

    return highest


def correlate_by_cwe(findings):

    cwe_map = defaultdict(list)

    for finding in findings:

        cwes = finding.get("cwe", [])

        if isinstance(cwes, str):
            cwes = [cwes]

        if not isinstance(cwes, list):
            continue

        # remove duplicates
        cwes = list(set(cwes))

        # clean values
        cwes = [
            c.strip()
            for c in cwes
            if c and c.strip()
        ]

        for cwe in cwes:
            cwe_map[cwe].append(
                finding
            )

    result = []

    for cwe, matches in cwe_map.items():

        # remove duplicate findings
        unique_matches = {}

        for m in matches:
            unique_matches[
                m["finding_id"]
            ] = m

        matches = list(
            unique_matches.values()
        )

        if len(matches) < 2:
            continue

        result.append(
            create_group(
                "CWE",
                cwe,
                matches
            )
        )

    return result


def correlate_by_vuln_class(findings):

    vuln_map = defaultdict(list)

    for finding in findings:

        classes = finding.get(
            "vulnerability_class",
            []
        )

        for vc in classes:

            vuln_map[vc].append(
                finding
            )

    result = []

    for vc, matches in vuln_map.items():

        if len(matches) < 2:
            continue

        result.append(
            create_group(
                "VULNERABILITY_CLASS",
                vc,
                matches
            )
        )

    return result


def correlate_by_package(findings):

    package_map = defaultdict(list)

    for finding in findings:

        package = finding.get(
            "package",
            ""
        )

        if package:
            package_map[package].append(
                finding
            )

    result = []

    for pkg, matches in package_map.items():

        if len(matches) < 2:
            continue

        result.append(
            create_group(
                "PACKAGE",
                pkg,
                matches
            )
        )

    return result


def main():

    with open(INPUT_FILE, "r") as f:
        findings = json.load(f)

    all_groups = []

    all_groups.extend(
        correlate_by_cwe(findings)
    )

    all_groups.extend(
        correlate_by_vuln_class(findings)
    )

    all_groups.extend(
        correlate_by_package(findings)
    )

    with open(OUTPUT_FILE, "w") as f:

        json.dump(
            all_groups,
            f,
            indent=2
        )

    print(
        f"[+] Created {len(all_groups)} correlation groups"
    )

    print(
        f"[+] Saved to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()