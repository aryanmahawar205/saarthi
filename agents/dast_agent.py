import subprocess
import os


TARGET_URL = "http://localhost:8080"

OUTPUT_DIR = "scans"

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "zap.json"
)


def run(state):

    print(
        "[DASTAgent] Starting ZAP scan"
    )

    cmd = [

        "docker",
        "run",
        "--rm",

        "-v",
        f"{os.getcwd()}/{OUTPUT_DIR}:/zap/wrk",

        "ghcr.io/zaproxy/zaproxy:stable",

        "zap-baseline.py",

        "-t",
        TARGET_URL,

        "-J",
        "zap.json"
    ]

    subprocess.run(
        cmd,
        check=False
    )

    print(
        f"[DASTAgent] Output -> {OUTPUT_FILE}"
    )

    state["zap_report"] = OUTPUT_FILE

    return state