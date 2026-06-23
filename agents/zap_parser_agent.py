import json


import subprocess
import os

INPUT_FILE = "scans/zap.json"
OUTPUT_FILE = "reports/normalized_zap.json"


def severity(riskcode):

    mapping = {

        "3": "HIGH",
        "2": "MEDIUM",
        "1": "LOW",
        "0": "INFO"
    }

    return mapping.get(
        str(riskcode),
        "INFO"
    )


def run(state):
    print("[ZapParserAgent] Running parsers/zap_parser.py")

    if not os.path.exists(INPUT_FILE):
        print(f"[ZapParserAgent] {INPUT_FILE} not found. Skipping.")
        state["dast_findings"] = []
        return state

    result = subprocess.run(["python3", "parsers/zap_parser.py"])

    if result.returncode != 0:
        print("[ZapParserAgent] Error: parsers/zap_parser.py failed")
        state["dast_findings"] = []
        return state

    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            findings = json.load(f)
            state["dast_findings"] = findings
            print(f"[ZapParserAgent] Loaded {len(findings)} findings from {OUTPUT_FILE}")
    else:
        print(f"[ZapParserAgent] {OUTPUT_FILE} not found after parsing.")
        state["dast_findings"] = []

    return state


if __name__ == "__main__":

    state = {}

    run(state)