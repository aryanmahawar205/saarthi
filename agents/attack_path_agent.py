import json
import os

OUTPUT_FILE = "reports/attack_chains.json"

def run(state):
    knowledge_graph = state.get("security_knowledge_graph", {})
    nodes = knowledge_graph.get("nodes", [])
    edges = knowledge_graph.get("edges", [])

    # Ingest runtime observations for enrichment
    runtime_observations = knowledge_graph.get("raw_inputs", {}).get("runtime_observations", [])
    runtime_evidence = knowledge_graph.get("raw_inputs", {}).get("runtime_evidence", [])

    dast_incidents = []
    sast_incidents = []
    trust_boundaries = []
    endpoints = []

    for node in nodes:
        node_type = node.get("type")
        if node_type == "finding" and node.get("source") == "DAST":
            dast_incidents.append(node)
        elif node_type == "finding" and node.get("source") == "SAST":
            sast_incidents.append(node)
        elif node_type == "trust_boundary":
            trust_boundaries.append(node)
        elif node_type == "endpoint":
            endpoints.append(node)

    attack_paths = []

    for incident in dast_incidents:
        name = incident.get("label", "")

        # Check for matching runtime observations to enrich the path
        matching_obs = [obs for obs in runtime_observations if obs.get("url") in incident.get("id", "")]

        # Determine if this finding crosses a trust boundary (look at edges)
        related_boundaries = [
            n for n in trust_boundaries
            if any(e.get("source") == incident.get("id") and e.get("target") == n.get("id") for e in edges)
        ]

        boundary_info = related_boundaries[0].get("label") if related_boundaries else "Application Layer"

        if "Browser Security" in name:
            attack_paths.append({
                "name": "Browser Exploitation Chain",
                "path": [
                    "Victim Browser",
                    "Missing CSP / Security Headers",
                    "Script Injection or Clickjacking",
                    "Session Theft or State Modification"
                ],
                "impact": "Account Takeover / Reputation Damage",
                "boundary_crossed": boundary_info
            })
        elif "CSRF" in name:
            attack_paths.append({
                "name": "Cross Site Request Forgery",
                "path": [
                    "Victim Session",
                    "Forged Request via malicious link",
                    "State Change Execution",
                    "Privilege Abuse"
                ],
                "impact": "Unauthorized Actions / Privilege Escalation",
                "boundary_crossed": boundary_info
            })
        elif "Authentication" in name or "Auth" in name:
            attack_paths.append({
                "name": "Authentication Abuse",
                "path": [
                    "External Input",
                    "Exposed Login Endpoint",
                    "Weak Session Controls or Brute Force",
                    "Session Hijacking or Credential Compromise"
                ],
                "impact": "Account Compromise / Data Breach",
                "boundary_crossed": boundary_info
            })
        elif "xss" in name.lower() or "cross site scripting" in name.lower():
            attack_paths.append({
                "name": "Cross Site Scripting",
                "path": [
                    "External Input",
                    "Unsanitized User Input",
                    "Script Injection into Web Page",
                    "Browser Execution by Victim",
                    "Credential Theft or Session Hijacking"
                ],
                "impact": "Account Takeover / Lateral Movement",
                "boundary_crossed": boundary_info
            })
        else:
            # Check for runtime confirmation
            matching_evidence = [e for e in runtime_evidence if e.get("finding_id") == incident.get("label")]

            path_steps = [
                "External Input",
                "Discovery of Vulnerability",
                f"Exploitation of {name}",
                "Impact Realization"
            ]

            if matching_evidence:
                path_steps.insert(2, "RUNTIME CONFIRMED: Execution path observed")
                if any(e.get("evidence_type") == "sink_reached" for e in matching_evidence):
                     path_steps.insert(3, "RUNTIME CONFIRMED: Sensitive sink reached")

            # Enrich with runtime evidence if available
            if matching_obs:
                obs = matching_obs[0]
                if obs.get("auth_flow", {}).get("present"):
                    path_steps.insert(2, f"Acquire {obs['auth_flow']['type']}")
                if obs.get("form_data"):
                    path_steps.insert(1, f"Submit form with fields: {', '.join(obs['form_data'].keys())}")

            attack_paths.append({
                "name": f"Exploitation of {name}",
                "path": path_steps,
                "impact": "Variable based on context",
                "boundary_crossed": boundary_info
            })

    # Optional: Combine with SAST if we had SAST findings in graph
    for incident in sast_incidents:
        name = incident.get("label", "")
        matching_evidence = [e for e in runtime_evidence if e.get("finding_id") == name]

        if "sql injection" in name.lower():
             path_steps = [
                    "External Input",
                    "Malicious Payload Injection",
                    "Database Access",
                    "Sensitive Data Exposure"
             ]
             if matching_evidence:
                 path_steps.insert(2, "RUNTIME CONFIRMED: Vulnerable code path executed")
                 if any(e.get("evidence_type") == "sink_reached" for e in matching_evidence):
                     path_steps.insert(3, "RUNTIME CONFIRMED: Database sink reached")

             attack_paths.append({
                "name": "SQL Injection Chain",
                "path": path_steps,
                "impact": "Data Breach / Complete Compromise",
                "boundary_crossed": "Data Access Boundary"
            })

    state["attack_paths"] = attack_paths

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(attack_paths, f, indent=2)

    print(f"[AttackPathAgent] Generated {len(attack_paths)} attack paths derived from the knowledge graph.")

    return state
