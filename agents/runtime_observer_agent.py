import subprocess
import os
import signal
import time
import sys

PROXY_PORT = 8081
OUTPUT_FILE = "reports/runtime_observations.json"

class RuntimeObserverAgent:
    def __init__(self):
        self.process = None

    def start(self):
        if self.process:
            print("[RuntimeObserverAgent] Already running.")
            return

        print(f"[RuntimeObserverAgent] Starting mitmdump on port {PROXY_PORT}...")

        # Cross-platform port cleanup (best effort)
        try:
            if sys.platform == "win32":
                # Windows port cleanup logic could be added here
                pass
            else:
                subprocess.run(["fuser", "-k", f"{PROXY_PORT}/tcp"], capture_output=True)
        except:
            pass

        # Start mitmdump
        # Note: on Windows, preexec_fn=os.setsid is not supported.
        kwargs = {}
        if sys.platform != "win32":
            kwargs["preexec_fn"] = os.setsid

        self.process = subprocess.Popen(
            ["mitmdump", "-s", "agents/mitm_logger.py", "-p", str(PROXY_PORT)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            **kwargs
        )
        # Give it a moment to initialize
        time.sleep(3)
        print("[RuntimeObserverAgent] Runtime Observer is active and logging to reports/runtime_observations.json")

    def stop(self):
        if self.process:
            print("[RuntimeObserverAgent] Stopping Runtime Observer...")
            try:
                if sys.platform == "win32":
                    self.process.terminate()
                else:
                    os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            except (ProcessLookupError, AttributeError):
                try:
                    self.process.terminate()
                except:
                    pass
            self.process = None
            print("[RuntimeObserverAgent] Runtime Observer stopped.")
        else:
            print("[RuntimeObserverAgent] Not running.")

# Global instance
observer = RuntimeObserverAgent()

def start(state):
    observer.start()
    state["runtime_observer_active"] = True
    return state

def stop(state):
    observer.stop()
    state["runtime_observer_active"] = False
    return state

def run(state):
    print("[RuntimeObserverAgent] Use start() and stop() to manage the observer.")
    return state
