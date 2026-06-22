import json

OUTPUT_FILE = "reports/remediation_guidance.json"

def run(state):
    knowledge_graph = state.get("security_knowledge_graph", {})
    security_reasoning = state.get("security_reasoning", {})

    remediation_guidance = []

    # Analyze DAST incidents for remediation
    for incident in knowledge_graph.get("dast_incidents", []):
        name = incident.get("incident", "").lower()
        if "browser" in name or "csp" in name:
            remediation_guidance.append({
                "incident": incident.get("incident"),
                "recommendation": "Implement strict Content Security Policy (CSP), X-Frame-Options, and secure cookies.",
                "priority": "High"
            })
        elif "csrf" in name:
            remediation_guidance.append({
                "incident": incident.get("incident"),
                "recommendation": "Implement anti-CSRF tokens for all state-changing requests and ensure SameSite cookie attributes are set.",
                "priority": "High"
            })
        elif "xss" in name:
            remediation_guidance.append({
                "incident": incident.get("incident"),
                "recommendation": "Implement context-aware output encoding, sanitize user inputs, and deploy a strict CSP.",
                "priority": "Critical"
            })
        elif "authentication" in name or "session" in name:
            remediation_guidance.append({
                "incident": incident.get("incident"),
                "recommendation": "Enforce strong password policies, implement MFA, ensure secure session token generation and expiration, and secure session transmission.",
                "priority": "Critical"
            })
        else:
            remediation_guidance.append({
                "incident": incident.get("incident"),
                "recommendation": "Review the specific vulnerability details and apply appropriate security patches or configuration changes.",
                "priority": "Medium"
            })

    # Include high-level remediation derived from AI security reasoning
    overall_remediation = {
        "strategic_advice": "Focus on the highest risk components identified. Address critical attack chains first to break the exploitation paths.",
        "incident_remediation": remediation_guidance
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(overall_remediation, f, indent=2)

    state["remediation_guidance"] = overall_remediation
    print(f"[RemediationAgent] Generated remediation guidance for {len(remediation_guidance)} incidents.")

    return state
