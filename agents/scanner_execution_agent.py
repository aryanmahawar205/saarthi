import subprocess
import json
import os


SCANS_DIR = "scans"


def run_semgrep():

    print(
        "[ScannerAgent] Running Semgrep"
    )

    subprocess.run(
        [
            "semgrep",
            "--config=auto",
            ".",
            "--json",
            "-o",
            f"{SCANS_DIR}/semgrep.json"
        ]
    )


def run_trivy():

    print(
        "[ScannerAgent] Running Trivy"
    )

    subprocess.run(
        [
            "trivy",
            "fs",
            ".",
            "--format",
            "json",
            "-o",
            f"{SCANS_DIR}/trivy.json"
        ]
    )


def run_gitleaks():

    print(
        "[ScannerAgent] Running Gitleaks"
    )

    subprocess.run(
        [
            "gitleaks",
            "detect",
            ".",
            "--report-format",
            "json",
            "--report-path",
            f"{SCANS_DIR}/gitleaks.json"
        ]
    )


def run_zap(target_url):

    print(
        "[ScannerAgent] Running ZAP"
    )

    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--network",
            "host",
            "-v",
            f"{os.getcwd()}/scans:/zap/wrk",
            "ghcr.io/zaproxy/zaproxy:stable",
            "zap-baseline.py",
            "-t",
            target_url,
            "-J",
            "zap.json"
        ]
    )


def run(state):

    plan = state.get(
        "assessment_plan",
        {}
    )

    scanners = plan.get(
        "recommended_scanners",
        []
    )

    target_url = state.get(
        "target_url"
    )

    if "semgrep" in scanners:

        run_semgrep()

    if "trivy" in scanners:

        run_trivy()

    if "gitleaks" in scanners:

        run_gitleaks()

    if (
        "zap" in scanners
        and target_url
    ):

        run_zap(
            target_url
        )

    state[
        "executed_scanners"
    ] = scanners

    return state