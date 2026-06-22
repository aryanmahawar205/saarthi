import json

OUTPUT_FILE = "reports/security_knowledge_graph.json"

def run(state):
    # Retrieve contextual components
    attack_surface = state.get("attack_surface", {})
    trust_boundaries = state.get("trust_boundaries", [])
    api_call_chains = state.get("api_call_chains", [])

    # Retrieve findings
    sast_incidents = state.get("incidents", []) # from correlation agent
    dast_incidents = state.get("dast_incidents", [])

    # The Security Knowledge Graph binds contextual information, trust boundaries,
    # SAST insights, and DAST incidents together for comprehensive analysis.
    knowledge_graph = {
        "attack_surface": attack_surface,
        "trust_boundaries": trust_boundaries,
        "api_call_chains": api_call_chains,
        "sast_incidents": sast_incidents,
        "dast_incidents": dast_incidents
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(knowledge_graph, f, indent=2)

    state["security_knowledge_graph"] = knowledge_graph
    print(f"[SecurityKnowledgeGraphAgent] Knowledge graph generated with {len(sast_incidents)} SAST incidents and {len(dast_incidents)} DAST incidents.")

    return state
