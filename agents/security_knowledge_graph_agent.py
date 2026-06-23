import json
import os

OUTPUT_FILE = "reports/security_graph.json"
OBSERVATIONS_FILE = "reports/runtime_observations.json"

def run(state):
    attack_surface = state.get("attack_surface", {})
    discovered_endpoints = state.get("discovered_endpoints", [])
    trust_boundaries = state.get("trust_boundaries", [])
    api_call_chains = state.get("api_call_chains", [])
    attack_paths = state.get("attack_paths", [])

    sast_incidents = state.get("incidents", [])
    if isinstance(sast_incidents, str):
        try:
            # Handle potential markdown or garbage in LLM response
            clean_incidents = sast_incidents.replace('```json', '').replace('```', '').strip()
            sast_incidents = json.loads(clean_incidents)
        except:
            sast_incidents = []

    dast_incidents = state.get("dast_incidents", [])

    # Validation: Ensure incidents are reaching the graph if findings exist
    if not sast_incidents and state.get("findings"):
        raise RuntimeError("[SecurityKnowledgeGraphAgent] SAST incidents failed to propagate to Knowledge Graph Agent despite findings being present.")

    if not dast_incidents and state.get("dast_findings"):
        raise RuntimeError("[SecurityKnowledgeGraphAgent] DAST incidents failed to propagate to Knowledge Graph Agent despite DAST findings being present.")

    # Load runtime observations
    runtime_observations = []
    if os.path.exists(OBSERVATIONS_FILE):
        try:
            with open(OBSERVATIONS_FILE, "r") as f:
                runtime_observations = json.load(f)
        except:
            pass

    nodes = {}
    edges = []

    def add_node(n_id, n_type, label, **kwargs):
        if n_id not in nodes:
            nodes[n_id] = {"id": n_id, "type": n_type, "label": label}
            nodes[n_id].update(kwargs)

    def add_edge(src, tgt, rel):
        edges.append({"source": src, "target": tgt, "relationship": rel})

    # Endpoints from attack surface
    if isinstance(attack_surface, dict) and "endpoints" in attack_surface:
        for ep in attack_surface.get("endpoints", []):
            url = ep.get("url") if isinstance(ep, dict) else ep
            if url:
                add_node(f"Endpoint_{url}", "endpoint", url)

    for ep in discovered_endpoints:
        url = ep.get("url") if isinstance(ep, dict) else ep
        if url:
            add_node(f"Endpoint_{url}", "endpoint", url)

    # Runtime Observations Integration
    for idx, obs in enumerate(runtime_observations):
        url = obs.get("url")
        obs_id = f"Obs_{idx}"
        req_id = f"Request_{idx}"
        resp_id = f"Response_{idx}"

        add_node(req_id, "request", f"{obs.get('method')} {url}", method=obs.get("method"), auth_flow=obs.get("auth_flow"))
        add_node(resp_id, "response", f"Status {obs.get('status_code')}", status=obs.get("status_code"))
        add_edge(req_id, resp_id, "generated_response")

        ep_id = f"Endpoint_{url}"
        add_node(ep_id, "endpoint", url)
        add_edge(req_id, ep_id, "targeted_at")

        # Runtime Observation -> Endpoint
        add_edge(f"Obs_{idx}", ep_id, "observed_at")

        # Cookies
        for cookie_name, cookie_val in obs.get("cookies", {}).items():
            c_id = f"Cookie_{cookie_name}"
            add_node(c_id, "cookie", cookie_name)
            add_edge(req_id, c_id, "sent_cookie")
            if "session" in cookie_name.lower() or "sid" in cookie_name.lower():
                s_id = f"Session_{cookie_val[:8]}"
                add_node(s_id, "session", "Active Session")
                add_edge(c_id, s_id, "identifies")

        # Forms
        for field in obs.get("form_data", {}).keys():
            f_id = f"Form_{field}"
            add_node(f_id, "form", f"Form Field: {field}")
            add_edge(req_id, f_id, "submitted_field")

        # Headers (Focus on security relevant ones)
        for h_name in obs.get("request_headers", {}).keys():
            if h_name.lower() in ["authorization", "x-api-key", "token"]:
                h_id = f"Header_{h_name}"
                add_node(h_id, "header", h_name)
                add_edge(req_id, h_id, "authenticated_by")

    # API Call Chains (Endpoint -> Controller -> Call Chain -> Finding)
    for chain in api_call_chains:
        file_name = chain.get("file", "unknown")
        controller_id = f"Controller_{file_name}"
        add_node(controller_id, "controller", file_name)

        for ep in chain.get("endpoints", []):
            ep_id = f"Endpoint_{ep}"
            add_node(ep_id, "endpoint", ep)
            # Endpoint -> Controller
            add_edge(ep_id, controller_id, "points_to")

        # Controller -> Call Chain
        chain_id = f"Chain_{file_name}"
        add_node(chain_id, "call_chain", f"Call Chain in {file_name}")
        add_edge(controller_id, chain_id, "initiates")

        calls = chain.get("call_chain", [])
        for call in calls:
            caller = call.get("caller")
            callee = call.get("callee")
            if caller and callee:
                caller_id = f"Method_{caller}"
                callee_id = f"Method_{callee}"
                add_node(caller_id, "method", caller)
                add_node(callee_id, "method", callee)
                add_edge(caller_id, callee_id, "calls")

    # Trust Boundaries
    for idx, tb in enumerate(trust_boundaries):
        tb_id = f"Boundary_{idx}"
        label = tb.get("boundary", "Unknown Boundary")
        add_node(tb_id, "trust_boundary", label, source_zone=tb.get("source"), target_zone=tb.get("target"))

    # SAST Findings
    for inc in sast_incidents:
        name = inc.get("incident", "Unknown")
        inc_id = f"SAST_Incident_{name}"
        add_node(inc_id, "finding", name, source="SAST", type="vulnerability")

        for f in inc.get("findings", []):
            file = f.get("file", "") if isinstance(f, dict) else f
            if file:
                # Call Chain -> Vulnerability
                chain_id = f"Chain_{file}"
                if chain_id in nodes:
                    add_edge(chain_id, inc_id, "contains_vulnerability")

                # Finding -> Trust Boundary
                for idx, tb in enumerate(trust_boundaries):
                    if "Data" in tb.get("boundary", ""):
                         add_edge(inc_id, f"Boundary_{idx}", "crosses")


    # DAST Findings
    for inc in dast_incidents:
        name = inc.get("incident", "Unknown")
        inc_id = f"DAST_Incident_{name}"
        add_node(inc_id, "finding", name, source="DAST")

        for f in inc.get("findings", []):
            file = f.get("file")
            if file:
                ep_id = f"Endpoint_{file}"
                add_node(ep_id, "endpoint", file)
                add_edge(ep_id, inc_id, "has_finding")

            # Finding -> Trust Boundary
            if "Authentication" in name or "Auth" in name:
                for idx, tb in enumerate(trust_boundaries):
                    if "Identity" in tb.get("boundary", ""):
                        add_edge(inc_id, f"Boundary_{idx}", "affects_boundary")

    # Attack Chains
    for path in attack_paths:
        name = path.get("name", "Unknown Path")
        ac_id = f"AttackChain_{name}"
        add_node(ac_id, "attack_chain", name)

        # Trust Boundary -> Attack Path
        boundary_crossed = path.get("boundary_crossed")
        if boundary_crossed:
            for idx, tb in enumerate(trust_boundaries):
                if tb.get("boundary") == boundary_crossed:
                    add_edge(f"Boundary_{idx}", ac_id, "enables")

        # Finding -> Attack Chain
        for finding in sast_incidents + dast_incidents:
            finding_name = finding.get("incident", "")
            if finding_name in path.get("path", []) or finding_name in name:
                f_id = f"SAST_Incident_{finding_name}" if finding in sast_incidents else f"DAST_Incident_{finding_name}"
                add_edge(f_id, ac_id, "leads_to")

        # Attack Chain -> Business Impact
        impact = path.get("impact")
        if impact:
            bi_id = f"BusinessImpact_{impact}"
            add_node(bi_id, "business_impact", impact)
            # Attack Path -> Business Impact
            add_edge(ac_id, bi_id, "leads_to_impact")

        # Runtime Observation -> Attack Path
        for idx, obs in enumerate(runtime_observations):
            if any(step in obs.get("url", "") for step in path.get("path", [])):
                add_edge(f"Obs_{idx}", ac_id, "evidences")

    # Deduplicate edges
    unique_edges = []
    seen_edges = set()
    for e in edges:
        sig = f"{e['source']}->{e['relationship']}->{e['target']}"
        if sig not in seen_edges:
            seen_edges.add(sig)
            unique_edges.append(e)

    # Statistics
    stats = {
        "node_count": len(nodes),
        "edge_count": len(unique_edges),
        "edge_types": list(set(e["relationship"] for e in unique_edges))
    }

    knowledge_graph = {
        "nodes": list(nodes.values()),
        "edges": unique_edges,
        "statistics": stats,
        "raw_inputs": {
            "attack_surface": attack_surface,
            "trust_boundaries": trust_boundaries,
            "api_call_chains": api_call_chains,
            "sast_incidents": sast_incidents,
            "dast_incidents": dast_incidents,
            "runtime_observations": runtime_observations
        }
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(knowledge_graph, f, indent=2)

    state["security_knowledge_graph"] = knowledge_graph
    print(f"[SecurityKnowledgeGraphAgent] Knowledge graph generated with {len(nodes)} nodes and {len(unique_edges)} edges.")

    return state
