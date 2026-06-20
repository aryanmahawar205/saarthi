import subprocess


OUTPUT_FILE = "scans/zap.json"


def run(state):

    target = state.get(
        "target_url"
    )

    print(
        f"[ZapAgent] {target}"
    )

    command = [

        "docker",
        "run",
        "--rm",

        "--network",
        "host",

        "-v",
        f"{state['project_root']}/scans:/zap/wrk",

        "ghcr.io/zaproxy/zaproxy:stable",

        "zap-baseline.py",

        "-t",
        target,

        "-J",
        "zap.json"
    ]

    result = subprocess.run(
        command,
        capture_output=False
    )

    print(
        "[ZapAgent] Scan Complete"
    )

    print(
        f"[ZapAgent] Exit Code: "
        f"{result.returncode}"
    )

    state["zap_report"] = (
        "scans/zap.json"
    )

    state["zap_complete"] = True

    print(
        "[ZapAgent] Complete"
    )

    return state