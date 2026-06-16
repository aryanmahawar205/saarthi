import json

INPUT_FILE = "reports/final_prioritized_findings.json"


def run(state):

    with open(INPUT_FILE) as f:
        findings = json.load(f)

    findings = findings[:20]

    compact = []

    for finding in findings:

        compact.append({
            "finding_id": finding.get("finding_id"),
            "title": finding.get("title"),
            "severity": finding.get("severity"),
            "priority": finding.get("priority"),
            "file": finding.get("file"),
            "asset_type": finding.get("asset_type"),
            "reachability_score": finding.get(
                "reachability_score",
                0
            )
        })

    state["findings"] = compact

    print(
        f"[ContextAgent] Loaded {len(compact)} findings"
    )

    return state