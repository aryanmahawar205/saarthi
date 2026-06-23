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
    runtime_observations = raw_inputs.get("runtime_observations", [])

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
        f.write(f"**Overall Risk Level:** {reasoning.get('Overall Risk', 'UNKNOWN')} ({reasoning.get('Risk Score', 'N/A')}/100)\n\n")
        f.write("This report provides a comprehensive security assessment of the target application using AI-assisted runtime-aware analysis. ")
        f.write("By correlating static code analysis, dynamic scanning, and runtime observation, Saarthi has identified critical attack paths and business risks.\n\n")

        # Assessment Scope
        f.write("## Assessment Scope\n\n")
        target_url = state.get('target_url', 'N/A')
        project_root = state.get('project_root', 'N/A')
        f.write(f"- **Target URL:** {target_url}\n")
        f.write(f"- **Repository Path:** {project_root}\n")
        f.write(f"- **Discovery Mode:** {'Hybrid' if target_url != 'N/A' and project_root != 'N/A' else 'Single-Mode'}\n\n")

        # Runtime Attack Surface
        f.write("## Runtime Attack Surface\n\n")
        f.write(f"- **Discovered Endpoints:** {endpoints_count}\n")
        f.write(f"- **Observed Traffic Flows:** {len(runtime_observations)}\n\n")
        f.write("The runtime attack surface was mapped through deep crawling and traffic observation. This represents the externally reachable entry points and internal data flow patterns.\n\n")

        # Trust Boundaries
        f.write("## Trust Boundaries\n\n")
        if trust_boundaries:
            for idx, tb in enumerate(trust_boundaries):
                f.write(f"- **{tb.get('boundary', 'Boundary')}**: {tb.get('source', 'Unknown')} -> {tb.get('target', 'Unknown')}\n")
        else:
            f.write("No distinct trust boundaries were identified in the current context.\n")
        f.write("\n")

        # Observed Runtime Behaviour
        f.write("## Observed Runtime Behaviour\n\n")
        if runtime_observations:
            f.write("The following significant runtime behaviours were observed during the assessment:\n\n")
            # List first few unique observations
            unique_obs = []
            seen_urls = set()
            for obs in runtime_observations:
                if obs['url'] not in seen_urls:
                    unique_obs.append(obs)
                    seen_urls.add(obs['url'])

            for obs in unique_obs[:10]:
                f.write(f"- **{obs.get('method')} {obs.get('url')}** (Status: {obs.get('status_code')})\n")
                if obs.get("cookies"):
                    f.write(f"  - Cookies: {', '.join(obs.get('cookies').keys())}\n")
                if obs.get("form_data"):
                    f.write(f"  - Form Data: {', '.join(obs.get('form_data').keys())}\n")
        else:
            f.write("No runtime traffic was observed.\n")
        f.write("\n")

        # Static Findings (SAST)
        f.write("## Static Findings (SAST)\n\n")
        if sast_incidents:
            for inc in sast_incidents:
                f.write(f"- **{inc.get('incident', 'Unknown Finding')}**\n")
        else:
            f.write("No static findings were identified.\n")
        f.write("\n")

        # Dynamic Findings (DAST)
        f.write("## Dynamic Findings (DAST)\n\n")
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
        if attack_paths:
            for idx, path in enumerate(attack_paths):
                f.write(f"### {idx + 1}. {path.get('name', 'Unnamed Path')}\n")
                f.write(f"**Boundary Crossed:** {path.get('boundary_crossed', 'N/A')}\n")
                f.write(f"**Impact:** {path.get('impact', 'N/A')}\n\n")
                f.write("**Chain:**\n")
                for step in path.get("path", []):
                    f.write(f"- {step}\n")
                f.write("\n")
        else:
            f.write("No definitive attack chains were derived.\n\n")

        # AI-Assisted Reasoning
        f.write("## AI-Assisted Reasoning\n\n")

        f.write("### Most Likely Attack\n")
        f.write(f"{reasoning.get('Most Likely Attack', 'Not evaluated.')}\n\n")

        f.write("### Most Dangerous Attack\n")
        f.write(f"{reasoning.get('Most Dangerous Attack', 'Not evaluated.')}\n\n")

        f.write("### Exploitability Assessment\n")
        f.write(f"{reasoning.get('Exploitability Assessment', 'Not evaluated.')}\n\n")

        f.write("### Business Impact\n")
        f.write(f"{reasoning.get('Business Impact', 'Not evaluated.')}\n\n")

        # Risk Assessment
        f.write("## Risk Assessment\n\n")
        f.write(f"**Priority:** {reasoning.get('Remediation Priority', 'N/A')}\n\n")
        f.write("### Top Risks\n\n")
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
        f.write("It is highly recommended that the engineering teams prioritize the Top Risks identified in this report. ")
        f.write("The integration of runtime evidence proves that these vulnerabilities are not just theoretical but reachable in the application's current deployment. ")
        f.write("Following the Remediation Roadmap will systematically address the underlying structural vulnerabilities, reducing the overall risk exposure.")

    print(f"[ReportAgent] Saved high-quality final assessment to {OUTPUT_FILE}")

    return state
