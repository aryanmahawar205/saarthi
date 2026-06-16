import json
import uuid

INPUT_FILE = "scans/semgrep.json"
OUTPUT_FILE = "reports/normalized_semgrep.json"


def ensure_list(value):
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, str):
        return [value]

    return [str(value)]


with open(INPUT_FILE, "r") as f:
    data = json.load(f)

normalized = []

for finding in data["results"]:

    meta = finding.get("extra", {}).get("metadata", {})
    extra = finding.get("extra", {})

    normalized_finding = {

        "finding_id": str(uuid.uuid4()),

        "tool": "Semgrep",
        "category": "SAST",

        "severity": extra.get("severity", ""),

        "confidence": meta.get("confidence", ""),

        "title": finding.get("check_id", ""),
        "description": extra.get("message", ""),

        "cwe": ensure_list(
            meta.get("cwe", [])
        ),

        "owasp": ensure_list(
            meta.get("owasp", [])
        ),

        "file": finding.get("path", ""),

        "line": finding.get(
            "start",
            {}
        ).get(
            "line",
            0
        ),

        "likelihood": meta.get(
            "likelihood",
            ""
        ),

        "impact": meta.get(
            "impact",
            ""
        ),

        "vulnerability_class": ensure_list(
            meta.get(
                "vulnerability_class",
                []
            )
        ),

        "status": "NEW",

        "ai_analysis": None,

        "references": ensure_list(
            meta.get(
                "references",
                []
            )
        ),

        "raw_finding": finding
    }

    normalized.append(
        normalized_finding
    )

with open(
    OUTPUT_FILE,
    "w"
) as f:
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