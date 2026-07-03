import json
import uuid

INPUT_FILE = "scans/zap.json"
OUTPUT_FILE = "reports/normalized_zap.json"


RISK_MAP = {
    "0": "INFO",
    "1": "LOW",
    "2": "MEDIUM",
    "3": "HIGH",
    "4": "CRITICAL"
}


def normalize_alert(alert):

    findings = []

    severity = RISK_MAP.get(
        str(alert.get("riskcode", "1")),
        "LOW"
    )

    instances = alert.get(
        "instances",
        []
    )

    for instance in instances:

        finding = {

            "finding_id":
                str(uuid.uuid4()),

            "tool":
                "ZAP",

            "category":
                "DAST",

            "severity":
                severity,

            "confidence":
                "MEDIUM",

            "title":
                alert.get(
                    "alert",
                    ""
                ),

            "description":
                alert.get(
                    "desc",
                    ""
                ),

            "cwe": [alert.get("cweid")] if alert.get("cweid") else [],

            "owasp": [],

            "cve": "",

            "package": "",

            "installed_version": "",

            "fixed_version": "",

            "cvss_score": 0.0,

            "cvss_vector": "",

            "secret_type": "",

            "file":
                instance.get(
                    "uri",
                    ""
                ),

            "line": 0,

            "likelihood": "",

            "impact": "",

            "vulnerability_class": [
                "DAST"
            ],

            "status":
                "NEW",

            "ai_analysis":
                None,

            "references": [],

            "raw_finding":
                alert
        }

        findings.append(
            finding
        )

    return findings


def main():
    import os
    if not os.path.exists(INPUT_FILE):
        print(f"[!] {INPUT_FILE} not found. Skipping ZAP parsing.")
        with open(OUTPUT_FILE, "w") as f:
            json.dump([], f)
        return

    with open(INPUT_FILE) as f:
        data = json.load(f)

    output = []

    sites = data.get(
        "site",
        []
    )

    for site in sites:

        alerts = site.get(
            "alerts",
            []
        )

        for alert in alerts:

            output.extend(
                normalize_alert(
                    alert
                )
            )

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
        f"[+] Parsed {len(output)} findings"
    )

    print(
        f"[+] Output: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
