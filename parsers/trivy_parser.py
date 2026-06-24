import json
import uuid


INPUT_FILE = "scans/trivy.json"
OUTPUT_FILE = "reports/normalized_trivy.json"


def extract_cvss_score(vuln):
    """
    Get highest available CVSS score.
    """

    cvss = vuln.get("CVSS", {})

    scores = []

    for source in cvss.values():

        if isinstance(source, dict):

            if "V3Score" in source:
                scores.append(source["V3Score"])

            elif "V2Score" in source:
                scores.append(source["V2Score"])

    return max(scores) if scores else 0.0


def extract_cvss_vector(vuln):
    """
    Get first available CVSS vector.
    """

    cvss = vuln.get("CVSS", {})

    for source in cvss.values():

        if isinstance(source, dict):

            if "V3Vector" in source:
                return source["V3Vector"]

            if "V2Vector" in source:
                return source["V2Vector"]

    return ""


def normalize_trivy(trivy_json):

    findings = []

    results = trivy_json.get("Results", [])

    for result in results:

        target = result.get("Target", "")

        vulnerabilities = result.get("Vulnerabilities", [])

        for vuln in vulnerabilities:

            finding = {

                "finding_id": str(uuid.uuid4()),

                "tool": "Trivy",

                "category": "SCA",

                "severity":
                    vuln.get("Severity", "UNKNOWN"),

                "confidence": "HIGH",

                "title":
                    vuln.get("Title", ""),

                "description":
                    vuln.get("Description", ""),

                "cwe":
                    vuln.get("CweIDs", []),

                "owasp": [],

                "cve":
                    vuln.get("VulnerabilityID", ""),

                "package":
                    vuln.get("PkgName", ""),

                "installed_version":
                    vuln.get("InstalledVersion", ""),

                "fixed_version":
                    vuln.get("FixedVersion", ""),

                "cvss_score":
                    extract_cvss_score(vuln),

                "cvss_vector":
                    extract_cvss_vector(vuln),

                "file":
                    target,

                "line": 0,

                "likelihood": "",

                "impact": "",

                "vulnerability_class": [],

                "status": "NEW",

                "ai_analysis": None,

                "references":
                    vuln.get("References", []),

                "raw_finding":
                    vuln
            }

            findings.append(finding)

    return findings


def main():
    import os
    if not os.path.exists(INPUT_FILE):
        print(f"[!] {INPUT_FILE} not found. Skipping Trivy parsing.")
        with open(OUTPUT_FILE, "w") as f:
            json.dump([], f)
        return

    with open(INPUT_FILE, "r") as f:
        trivy_json = json.load(f)

    normalized = normalize_trivy(trivy_json)

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