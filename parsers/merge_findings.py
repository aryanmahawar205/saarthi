import json

ZAP_FILE = "reports/normalized_zap.json"
SEMGREP_FILE = "reports/normalized_semgrep.json"
TRIVY_FILE = "reports/normalized_trivy.json"
GITLEAKS_FILE = "reports/normalized_gitleaks.json"

OUTPUT_FILE = "reports/all_findings.json"


import os

def load_json(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return []


def main():

    all_findings = []

    semgrep = load_json(SEMGREP_FILE)
    trivy = load_json(TRIVY_FILE)
    gitleaks = load_json(GITLEAKS_FILE)
    zap = load_json(ZAP_FILE)

    all_findings.extend(semgrep)
    all_findings.extend(trivy)
    all_findings.extend(gitleaks)
    all_findings.extend(zap)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(
            all_findings,
            f,
            indent=2
        )

    print(
        f"[+] Total Findings: {len(all_findings)}"
    )

    print(
        f"[+] Saved: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()