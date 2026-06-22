import json
import os

OUTPUT_FILE = "reports/security_knowledge_graph.json"

def run(state):
    attack_surface = state.get("attack_surface", {})
    discovered_endpoints = state.get("discovered_endpoints", [])
    trust_boundaries = state.get("trust_boundaries", [])
    api_call_chains = state.get("api_call_chains", [])

    sast_incidents = state.get("incidents", [])
    if isinstance(sast_incidents, str):
        try:
            sast_incidents = json.loads(sast_incidents)
        except:
            sast_incidents = []

    dast_incidents = state.get("dast_incidents", [])

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

    # API Call Chains
    for chain in api_call_chains:
        file_name = chain.get("file", "unknown")
        controller_id = f"Controller_{file_name}"
        add_node(controller_id, "controller", file_name)

        for ep in chain.get("endpoints", []):
            ep_id = f"Endpoint_{ep}"
            add_node(ep_id, "endpoint", ep)
            add_edge(ep_id, controller_id, "handled_by")

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
                # link controller to caller if first
                add_edge(controller_id, caller_id, "contains_method")

    # Trust Boundaries
    for idx, tb in enumerate(trust_boundaries):
        tb_id = f"Boundary_{idx}"
        label = tb.get("boundary", "Unknown Boundary")
        add_node(tb_id, "trust_boundary", label, source_zone=tb.get("source"), target_zone=tb.get("target"))

    # SAST Findings
    for inc in sast_incidents:
        name = inc.get("incident", "Unknown")
        inc_id = f"SAST_Incident_{name}"
        add_node(inc_id, "finding", name, source="SAST")

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

            # If finding is related to Auth, CSRF, link to boundary
            if "Authentication" in name or "Auth" in name:
                for idx, tb in enumerate(trust_boundaries):
                    if "Identity" in tb.get("boundary", ""):
                        add_edge(inc_id, f"Boundary_{idx}", "affects_boundary")

    # Deduplicate edges
    unique_edges = []
    seen_edges = set()
    for e in edges:
        sig = f"{e['source']}->{e['relationship']}->{e['target']}"
        if sig not in seen_edges:
            seen_edges.add(sig)
            unique_edges.append(e)

    knowledge_graph = {
        "nodes": list(nodes.values()),
        "edges": unique_edges,
        "raw_inputs": {
            "attack_surface": attack_surface,
            "trust_boundaries": trust_boundaries,
            "api_call_chains": api_call_chains,
            "sast_incidents": sast_incidents,
            "dast_incidents": dast_incidents
        }
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(knowledge_graph, f, indent=2)

    state["security_knowledge_graph"] = knowledge_graph
    print(f"[SecurityKnowledgeGraphAgent] Knowledge graph generated with {len(nodes)} nodes and {len(unique_edges)} edges.")

    return state
