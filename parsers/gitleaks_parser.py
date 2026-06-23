import json
import uuid


INPUT_FILE = "scans/gitleaks.json"
OUTPUT_FILE = "reports/normalized_gitleaks.json"


def normalize_gitleaks(gitleaks_json):

    findings = []

    for finding in gitleaks_json:

        normalized = {

            "finding_id": str(uuid.uuid4()),

            "tool": "Gitleaks",

            "category": "SECRETS",

            "severity": "HIGH",

            "confidence": "HIGH",

            "title":
                finding.get("RuleID", ""),

            "description":
                finding.get("Description", ""),

            "cwe": [],

            "owasp": [],

            "cve": "",

            "package": "",

            "installed_version": "",

            "fixed_version": "",

            "cvss_score": 0.0,

            "cvss_vector": "",

            "secret_type":
                finding.get("RuleID", ""),

            "file":
                finding.get("File", ""),

            "line":
                finding.get("StartLine", 0),

            "likelihood": "HIGH",

            "impact": "HIGH",

            "vulnerability_class": [
                "Secret Exposure"
            ],

            "status": "NEW",

            "ai_analysis": None,

            "references": [],

            "raw_finding":
                finding
        }

        findings.append(normalized)

    return findings


def main():
    import os
    if not os.path.exists(INPUT_FILE):
        print(f"[!] {INPUT_FILE} not found. Skipping Gitleaks parsing.")
        with open(OUTPUT_FILE, "w") as f:
            json.dump([], f)
        return

    with open(INPUT_FILE, "r") as f:
        gitleaks_json = json.load(f)

    normalized = normalize_gitleaks(
        gitleaks_json
    )

    with open(OUTPUT_FILE, "w") as f:
        json.dump(
            normalized,
            f,
            indent=2
        )

    print(
        f"[+] Parsed {len(normalized)} findings"
    )

    print(
        f"[+] Saved to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()