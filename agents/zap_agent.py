import subprocess
import os


def run(state):
    target = state.get("target_url")

    if not target:
        raise ValueError("target_url not found in state")

    print(f"[ZapAgent] {target}")

    # --------------------------------------------------
    # Resolve project root
    # --------------------------------------------------

    project_root = os.path.abspath(
        state.get("project_root", os.getcwd())
    )

    if not os.path.isdir(project_root):
        project_root = os.getcwd()

    # --------------------------------------------------
    # Create scans directory
    # --------------------------------------------------

    scans_dir = os.path.join(
        project_root,
        "scans"
    )

    os.makedirs(
        scans_dir,
        exist_ok=True
    )

    # --------------------------------------------------
    # Ensure permissions
    # --------------------------------------------------

    try:
        os.chmod(scans_dir, 0o777)
    except Exception as e:
        print(
            f"[ZapAgent] Warning: chmod failed: {e}"
        )

    # --------------------------------------------------
    # Remove stale files
    # --------------------------------------------------

    report_path = os.path.join(
        scans_dir,
        "zap.json"
    )

    yaml_path = os.path.join(
        scans_dir,
        "zap.yaml"
    )

    for file_path in [report_path, yaml_path]:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(
                    f"[ZapAgent] Removed stale file: {file_path}"
                )
        except Exception as e:
            print(
                f"[ZapAgent] Warning removing {file_path}: {e}"
            )

    # --------------------------------------------------
    # Launch ZAP
    # --------------------------------------------------

    command = [
        "docker",
        "run",
        "--rm",
        "--network",
        "host",
        "-v",
        f"{scans_dir}:/zap/wrk:rw",
        "ghcr.io/zaproxy/zaproxy:stable",
        "zap-baseline.py",
        "-t",
        target,
        "-J",
        "zap.json"
    ]

    print(
        f"[ZapAgent] Scans Directory: {scans_dir}"
    )

    print(
        f"[ZapAgent] Running ZAP..."
    )

    result = subprocess.run(
        command,
        capture_output=False
    )

    # --------------------------------------------------
    # Validate output
    # --------------------------------------------------

    print(
        f"[ZapAgent] Exit Code: {result.returncode}"
    )

    # ZAP baseline returns:
    # 0 = success
    # 1 = fail alerts
    # 2 = warning alerts
    # 3 = fail + warning alerts

    if result.returncode not in [0, 1, 2, 3]:
        raise RuntimeError(
            f"ZAP execution failed with exit code {result.returncode}"
        )

    if not os.path.exists(report_path):
        raise FileNotFoundError(
            f"Expected ZAP report not found: {report_path}"
        )

    report_size = os.path.getsize(report_path)

    if report_size < 100:
        raise RuntimeError(
            f"ZAP report appears invalid ({report_size} bytes)"
        )

    print(
        f"[ZapAgent] Report Generated: {report_path}"
    )

    print(
        f"[ZapAgent] Report Size: {report_size} bytes"
    )

    # --------------------------------------------------
    # Update state
    # --------------------------------------------------

    state["zap_report"] = report_path
    state["zap_complete"] = True

    print("[ZapAgent] Scan Complete")

    return state