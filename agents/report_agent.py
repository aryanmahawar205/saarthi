import json
import os

OUTPUT_FILE = "reports/final_security_assessment.md"

def run(state):
    reasoning = state.get("security_reasoning", {})
    attack_paths = state.get("attack_paths", [])
    knowledge_graph = state.get("security_knowledge_graph", {})

    # We will use raw inputs from the graph generation to get counts/details
    raw_inputs = knowledge_graph.get("raw_inputs", {})
    attack_surface = state.get("attack_surface", raw_inputs.get("attack_surface", {}))
    trust_boundaries = state.get("trust_boundaries", raw_inputs.get("trust_boundaries", []))
    sast_incidents = state.get("incidents", raw_inputs.get("sast_incidents", []))
    dast_incidents = state.get("dast_incidents", raw_inputs.get("dast_incidents", []))

    if isinstance(sast_incidents, str):
        try:
            sast_incidents = json.loads(sast_incidents)
        except:
            sast_incidents = []

    endpoints_count = attack_surface.get("endpoint_count", 0) if isinstance(attack_surface, dict) else len(attack_surface)
    if endpoints_count == 0:
        # Fallback if attack_surface structure is different
        endpoints_count = len(state.get("discovered_endpoints", []))

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        f.write("# Saarthi Final Security Assessment\n\n")

        # Executive Summary
        f.write("## Executive Summary\n\n")
        f.write(f"The overall risk level for the application is assessed as **{reasoning.get('Overall Risk', 'UNKNOWN')}**. ")
        f.write("This report outlines the discovered attack surface, identifies trust boundaries, and highlights "
                "the critical vulnerabilities that pose a risk to the business.\n\n")

        # Assessment Scope
        f.write("## Assessment Scope\n\n")
        target_url = state.get('target_url', 'N/A')
        project_root = state.get('project_root', 'N/A')
        f.write(f"- **Target URL:** {target_url}\n")
        f.write(f"- **Repository Path:** {project_root}\n\n")

        # Application Overview
        f.write("## Application Overview\n\n")
        f.write("The platform performed an AI-assisted analysis of the target application. ")
        f.write("By mapping the application components, API calls, and trust boundaries, we established a "
                "comprehensive understanding of the architecture prior to deep security reasoning.\n\n")

        # Attack Surface
        f.write("## Attack Surface\n\n")
        f.write(f"Total endpoints discovered: {endpoints_count}\n\n")
        f.write("The discovered endpoints represent the entry points available to a potential attacker. "
                "Securing these points is critical to reducing the overall attack surface.\n\n")

        # Trust Boundaries
        f.write("## Trust Boundaries\n\n")
        if trust_boundaries:
            for idx, tb in enumerate(trust_boundaries):
                f.write(f"- **{tb.get('boundary', 'Boundary')}**: {tb.get('source', 'Unknown')} -> {tb.get('target', 'Unknown')}\n")
        else:
            f.write("No distinct trust boundaries were identified in the current context.\n")
        f.write("\n")

        # Static Findings (SAST)
        f.write("## Static Findings\n\n")
        if sast_incidents:
            for inc in sast_incidents:
                f.write(f"- **{inc.get('incident', 'Unknown Finding')}**\n")
        else:
            f.write("No static findings were identified.\n")
        f.write("\n")

        # Runtime Findings (DAST)
        f.write("## Runtime Findings\n\n")
        if dast_incidents:
            for inc in dast_incidents:
                f.write(f"- **{inc.get('incident', 'Unknown Finding')}** (Instances: {len(inc.get('findings', []))})\n")
        else:
            f.write("No runtime findings were identified.\n")
        f.write("\n")

        # Correlated Findings
        f.write("## Correlated Findings\n\n")
        f.write("Findings correlated across Static and Runtime analysis layers have been incorporated into the Security Knowledge Graph to uncover attack paths bridging the gap between static code issues and runtime execution context.\n\n")

        # Attack Chains
        f.write("## Attack Chains\n\n")
        for idx, path in enumerate(attack_paths):
            f.write(f"### {idx + 1}. {path.get('name', 'Unnamed Path')}\n")
            f.write(f"**Boundary Crossed:** {path.get('boundary_crossed', 'N/A')}\n")
            f.write(f"**Impact:** {path.get('impact', 'N/A')}\n\n")
            f.write("**Chain:**\n")
            for step in path.get("path", []):
                f.write(f"- {step}\n")
            f.write("\n")

        # Most Likely Attack Scenario
        f.write("## Most Likely Attack Scenario\n\n")
        f.write(f"{reasoning.get('Most Likely Attack', 'Not evaluated.')}\n\n")

        # Most Dangerous Attack Scenario
        f.write("## Most Dangerous Attack Scenario\n\n")
        f.write(f"{reasoning.get('Most Dangerous Attack', 'Not evaluated.')}\n\n")

        # Business Impact
        f.write("## Business Impact\n\n")
        f.write(f"{reasoning.get('Business Impact', 'Not evaluated.')}\n\n")

        # Top Risks
        f.write("## Top Risks\n\n")
        prioritized = reasoning.get("Prioritized Findings", [])
        if prioritized:
            for risk in prioritized:
                f.write(f"- {risk}\n")
        else:
            f.write("No prioritized risks were provided.\n")
        f.write("\n")

        # Remediation Roadmap
        f.write("## Remediation Roadmap\n\n")
        remediation_order = reasoning.get("Remediation Order", [])
        if remediation_order:
            for step in remediation_order:
                f.write(f"1. {step}\n")
        else:
            f.write("No remediation steps were provided.\n")
        f.write("\n")

        # Executive Recommendations
        f.write("## Executive Recommendations\n\n")
        f.write("It is highly recommended that the engineering teams prioritize the Top Risks identified in this report. "
                "Following the Remediation Roadmap will systematically address the underlying structural vulnerabilities, "
                "reducing the overall risk exposure of the application.")

    print(f"[ReportAgent] Saved high-quality final assessment to {OUTPUT_FILE}")

    return state
