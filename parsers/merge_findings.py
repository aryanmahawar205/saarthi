import json

SEMGREP_FILE = "reports/normalized_semgrep.json"
TRIVY_FILE = "reports/normalized_trivy.json"
GITLEAKS_FILE = "reports/normalized_gitleaks.json"

OUTPUT_FILE = "reports/all_findings.json"


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def main():

    all_findings = []

    semgrep = load_json(SEMGREP_FILE)
    trivy = load_json(TRIVY_FILE)
    gitleaks = load_json(GITLEAKS_FILE)

    all_findings.extend(semgrep)
    all_findings.extend(trivy)
    all_findings.extend(gitleaks)

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