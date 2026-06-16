import json
from collections import Counter

INPUT_FILE = "reports/all_findings_normalized.json"
OUTPUT_FILE = "reports/summary.json"


def main():

    with open(INPUT_FILE, "r") as f:
        findings = json.load(f)

    summary = {}

    summary["total_findings"] = len(findings)

    summary["by_tool"] = dict(
        Counter(
            finding["tool"]
            for finding in findings
        )
    )

    summary["by_category"] = dict(
        Counter(
            finding["category"]
            for finding in findings
        )
    )

    summary["by_severity"] = dict(
        Counter(
            finding["severity"]
            for finding in findings
        )
    )

    with open(OUTPUT_FILE, "w") as f:
        json.dump(
            summary,
            f,
            indent=2
        )

    print(
        f"[+] Summary saved to {OUTPUT_FILE}"
    )

    print(
        json.dumps(summary, indent=2)
    )


if __name__ == "__main__":
    main()