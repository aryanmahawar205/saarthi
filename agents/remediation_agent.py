import json
import os

OUTPUT_FILE = "reports/remediation_guidance.json"

def run(state):
    incidents = state.get("incidents", [])
    if isinstance(incidents, str):
        try:
            incidents = json.loads(incidents)
        except:
            incidents = []

    guidance = []

    for incident in incidents:
        name = incident.get("incident", "Unknown")

        remediation = {
            "incident": name,
            "priority": "HIGH" if "SQL" in name or "Auth" in name or "CSRF" in name else "MEDIUM",
            "action": f"Remediate {name} by implementing proper input validation and security controls.",
            "effort": "Medium"
        }

        if "SQL" in name:
            remediation["action"] = "Use Parameterized Queries or ORMs to prevent SQL injection."
        elif "CSRF" in name:
            remediation["action"] = "Implement Anti-CSRF tokens and SameSite cookie attributes."
        elif "Secret" in name:
            remediation["action"] = "Rotate the exposed secret and use a secure vault for secret management."

        guidance.append(remediation)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(guidance, f, indent=2)

    state["remediation_guidance"] = guidance
    print(f"[RemediationAgent] Generated remediation guidance for {len(guidance)} incidents.")

    return state
