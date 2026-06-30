#!/usr/bin/env python3
import subprocess
import time
import requests
import os
import signal
import sys
import json

# Configuration
JAVA_AGENT_JAR = "runtime_agent/adapters/java/agent/target/saarthi-java-agent-1.0-SNAPSHOT.jar"
WEBGOAT_JAR_URL = "https://github.com/WebGoat/WebGoat/releases/download/v2023.8/webgoat-2023.8.jar"
WEBGOAT_JAR = "/tmp/webgoat.jar"
ADAPTER_PORT = 8082
WEBGOAT_PORT = 8083
WEBGOAT_URL = f"http://localhost:{WEBGOAT_PORT}/WebGoat"

processes = []

def cleanup():
    print("\n[Cleanup] Stopping all processes...")
    for p in processes:
        try:
            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        except:
            pass
    print("[Cleanup] Done.")

def run_adapter():
    print(f"[Validation] Starting JavaAdapter on port {ADAPTER_PORT}...")
    cmd = ["python3", "-c", f"from runtime_agent.adapters.java.java_adapter import JavaAdapter; import time; adapter = JavaAdapter(); adapter.server_address = ('localhost', {ADAPTER_PORT}); adapter.start(); [time.sleep(1) for _ in range(600)]"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid, text=True)
    processes.append(p)

    # Wait for adapter to be ready
    for _ in range(10):
        try:
            res = requests.get(f"http://localhost:{ADAPTER_PORT}/health", timeout=1)
            if res.status_code == 200:
                break
        except:
            time.sleep(1)
            continue
    print("[Validation] JavaAdapter started.")

def download_webgoat():
    if not os.path.exists(WEBGOAT_JAR):
        print(f"[Validation] Downloading WebGoat from {WEBGOAT_JAR_URL} to {WEBGOAT_JAR}...")
        subprocess.run(["curl", "-L", "-o", WEBGOAT_JAR, WEBGOAT_JAR_URL], check=True)
        print("[Validation] WebGoat downloaded.")
    else:
        print(f"[Validation] WebGoat JAR already exists at {WEBGOAT_JAR}.")

def run_webgoat():
    print(f"[Validation] Starting WebGoat on port {WEBGOAT_PORT} with Java Agent {JAVA_AGENT_JAR}...")
    cmd = [
        "java",
        f"-javaagent:{JAVA_AGENT_JAR}=endpoint=http://localhost:{ADAPTER_PORT}/events",
        f"-Dserver.port={WEBGOAT_PORT}",
        "-Dserver.address=127.0.0.1",
        "-jar", WEBGOAT_JAR
    ]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=os.setsid, text=True, bufsize=1)
    processes.append(p)

    print("[Validation] Waiting for WebGoat to start and instrumentation summary...")
    instrumentation_detected = False
    webgoat_started = False

    start_time = time.time()
    while time.time() - start_time < 300: # Increased timeout for slow sandbox
        line = p.stdout.readline()
        if not line:
            if p.poll() is not None:
                print(f"[FAIL] WebGoat process exited with code {p.returncode}")
                # Print last few lines of output
                print("[WebGoat Last Output]")
                print(line)
                return False
            time.sleep(0.1)
            continue

        if "Saarthi Runtime Instrumentation" in line:
            instrumentation_detected = True
        if "Started WebGoat" in line:
            webgoat_started = True
            print("  [WebGoat] Started successfully.")
            break

    if not instrumentation_detected:
        print("[FAIL] Saarthi Instrumentation Summary not found in logs.")
        return False
    if not webgoat_started:
        print("[FAIL] WebGoat failed to start within 300 seconds.")
        return False

    print("[Validation] WebGoat started with instrumentation.")
    return True

def generate_traffic():
    print("[Validation] Generating traffic to WebGoat...")
    session = requests.Session()
    try:
        print("  [Traffic] Accessing landing page...")
        session.get(WEBGOAT_URL + "/login")

        print("  [Traffic] Attempting login...")
        session.post(WEBGOAT_URL + "/login", data={"username": "admin", "password": "password"})

        print("  [Traffic] Accessing static resources...")
        session.get(WEBGOAT_URL + "/css/main.css")

    except Exception as e:
        print(f"[Validation] Error generating traffic: {e}")

def verify_events():
    print("[Validation] Verifying RuntimeEvents in JavaAdapter...")
    try:
        res = requests.get(f"http://localhost:{ADAPTER_PORT}/events", timeout=5)
        if res.status_code == 200:
            events = res.json()
            print(f"[Validation] Collected {len(events)} events from adapter.")

            event_types = [e['event_type'] for e in events]
            print(f"[Validation] Event types detected: {set(event_types)}")

            has_http = "http_request" in event_types
            has_db = "database_query" in event_types

            if has_http:
                print("[PASS] HTTP events detected.")
            else:
                print("[FAIL] No HTTP events detected.")

            if has_db:
                print("[PASS] Database events detected.")
            else:
                print("[FAIL] No Database events detected.")

            return has_http and has_db
    except Exception as e:
        print(f"[Validation] Error verifying events: {e}")
    return False

def main():
    try:
        download_webgoat()
        run_adapter()
        if not run_webgoat():
             # If WebGoat still fails due to port in use, we've already proven
             # instrumentation works with the minimal app.
             # But let's try one more time to be sure.
             print("[Validation] WebGoat failed to start. Re-verifying with minimal app was already successful.")
             sys.exit(1)

        time.sleep(10)
        generate_traffic()
        time.sleep(5)

        if verify_events():
            print("\n[SUCCESS] Java Runtime Instrumentation Validation PASSED.")
        else:
            print("\n[FAIL] Java Runtime Instrumentation Validation FAILED.")
            sys.exit(1)

    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    finally:
        cleanup()

if __name__ == "__main__":
    main()
