import subprocess
import os


def run(state):

    repo = state["project_root"]

    os.makedirs("scans", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    print("\n========== SAST Pipeline ==========\n")

    #
    # Run Semgrep
    #
    print("[1/11] Running Semgrep Scan...")

    subprocess.run([
        "semgrep",
        "--config=auto",
        repo,
        "--json",
        "--output",
        "scans/semgrep.json"
    ], check=False)
    print("[✓] Semgrep Scan Complete")

    #
    # Run Trivy
    #
    print("[2/11] Running Trivy Scan...")

    subprocess.run([
        "trivy",
        "fs",
        "--format",
        "json",
        "--output",
        "scans/trivy.json",
        repo
    ], check=False)
    print("[✓] Trivy Scan Complete")

    #
    # Run Gitleaks
    #
    print("[3/11] Running Gitleaks Scan...")

    # Gitleaks often fails if not in a git repo, use --no-git if needed,
    # but the prompt says it is tracked by git in semgrep output
    subprocess.run([
        "gitleaks",
        "detect",
        "--source",
        repo,
        "--report-format",
        "json",
        "--report-path",
        "scans/gitleaks.json",
        "--no-git"
    ], check=False)
    print("[✓] Gitleaks Scan Complete")

    #
    # Parse scanner outputs
    #
    print("[4/11] Parsing Semgrep...")
    subprocess.run(["python3", "parsers/semgrep_parser.py"], check=False)

    print("[5/11] Parsing Trivy...")
    subprocess.run(["python3", "parsers/trivy_parser.py"], check=False)

    print("[6/11] Parsing Gitleaks...")
    subprocess.run(["python3", "parsers/gitleaks_parser.py"], check=False)
    print("[✓] Normalize Findings Complete")

    #
    # Merge findings
    #
    print("[7/11] Merging Findings...")
    subprocess.run(["python3", "parsers/merge_findings.py"], check=False)
    print("[✓] Merge Findings Complete")

    #
    # Normalize severities
    #
    print("[8/11] Normalizing Findings...")
    subprocess.run(["python3", "parsers/severity_normalizer.py"], check=False)

    #
    # Map findings
    #
    print("[9/11] Mapping Findings...")
    subprocess.run(["python3", "parsers/finding_mapper.py"], check=False)

    #
    # Build attack surface
    #
    print("[10/11] Building Attack Surface...")
    subprocess.run(["python3", "parsers/attack_surface_mapper.py"], check=False)

    #
    # Remaining enrichment
    #
    print("[11/11] Context + Reachability + Prioritization...")

    subprocess.run(["python3", "parsers/context_pack_builder.py"], check=False)
    subprocess.run(["python3", "parsers/graph_linker_v2.py"], check=False)
    subprocess.run(["python3", "parsers/reachability_engine.py"], check=False)
    subprocess.run(["python3", "parsers/final_prioritizer.py"], check=False)

    print("[✓] Reachability Analysis Complete")
    print("[✓] Prioritization Complete")

    print("\n========== SAST Pipeline Complete ==========\n")

    return state
