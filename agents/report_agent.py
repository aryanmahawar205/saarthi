import json

OUTPUT_FILE = "reports/ai_report.md"

def run(state):
    reasoning = state.get("security_reasoning", {})
    attack_paths = state.get("attack_paths", [])
    remediation = state.get("remediation_guidance", {})
    knowledge_graph = state.get("security_knowledge_graph", {})

    with open(OUTPUT_FILE, "w") as f:
        f.write("# Saarthi AI Security Assessment\n\n")

        # Executive Summary
        f.write("## Executive Summary\n\n")
        f.write(f"**Overall Risk Level:** {reasoning.get('overall_risk', 'UNKNOWN')}\n\n")
        f.write(f"**Business Impact:**\n{reasoning.get('business_impact', 'N/A')}\n\n")

        # Strategic Advice
        f.write("## Strategic Advice\n\n")
        f.write(f"{remediation.get('strategic_advice', 'N/A')}\n\n")

        # Security Reasoning
        f.write("## Security Reasoning & Runtime Analysis\n\n")
        f.write(f"**Exploitability:**\n{reasoning.get('exploitability', 'N/A')}\n\n")
        f.write(f"**Attack Scenario:**\n{reasoning.get('attack_scenario', 'N/A')}\n\n")
        f.write(f"**Runtime Reasoning:**\n{reasoning.get('runtime_reasoning', 'N/A')}\n\n")

        # Attack Paths
        f.write("## Attack Paths\n\n")
        for idx, path in enumerate(attack_paths):
            f.write(f"### {idx + 1}. {path.get('name', 'Unnamed Path')}\n")
            f.write(f"**Impact:** {path.get('impact', 'N/A')}\n\n")
            f.write("**Chain:**\n")
            for step in path.get("path", []):
                f.write(f"- {step}\n")
            f.write("\n")

        # Remediation Guidance
        f.write("## Incident Remediation Guidance\n\n")
        for item in remediation.get("incident_remediation", []):
            f.write(f"### {item.get('incident', 'Unknown Incident')}\n")
            f.write(f"**Priority:** {item.get('priority', 'N/A')}\n\n")
            f.write(f"**Recommendation:**\n{item.get('recommendation', 'N/A')}\n\n")

    print(f"[ReportAgent] Saved comprehensive assessment to {OUTPUT_FILE}")

    return state
