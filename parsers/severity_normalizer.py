import json

INPUT_FILE = "reports/all_findings.json"
OUTPUT_FILE = "reports/all_findings_normalized.json"


SEMGREP_MAP = {
    "ERROR": "HIGH",
    "WARNING": "MEDIUM",
    "INFO": "LOW"
}

TRIVY_MAP = {
    "CRITICAL": "CRITICAL",
    "HIGH": "HIGH",
    "MEDIUM": "MEDIUM",
    "LOW": "LOW",
    "UNKNOWN": "LOW"
}

GITLEAKS_MAP = {
    "HIGH": "HIGH"
}


def normalize_severity(finding):

    tool = finding.get("tool", "")
    severity = finding.get("severity", "")

    if tool == "Semgrep":
        return SEMGREP_MAP.get(
            severity,
            "MEDIUM"
        )

    elif tool == "Trivy":
        return TRIVY_MAP.get(
            severity,
            "MEDIUM"
        )

    elif tool == "Gitleaks":
        return GITLEAKS_MAP.get(
            severity,
            "HIGH"
        )

    return severity


def main():
    import os
    if not os.path.exists(INPUT_FILE):
        print(f"[!] {INPUT_FILE} not found. Skipping normalization.")
        with open(OUTPUT_FILE, "w") as f:
            json.dump([], f)
        return

    with open(INPUT_FILE, "r") as f:
        findings = json.load(f)

    for finding in findings:

        finding["original_severity"] = \
            finding["severity"]

        finding["severity"] = \
            normalize_severity(finding)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(
            findings,
            f,
            indent=2
        )

    print(
        f"[+] Normalized {len(findings)} findings"
    )

    print(
        f"[+] Saved to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()