import json
import os
from langchain_ollama import ChatOllama

OUTPUT_FILE = "reports/security_reasoning.json"

def run(state):
    knowledge_graph = state.get("security_knowledge_graph", {})
    attack_paths = state.get("attack_paths", [])

    # Other context
    sast_incidents = state.get("incidents", [])
    if isinstance(sast_incidents, str):
        try:
            sast_incidents = json.loads(sast_incidents)
        except:
            sast_incidents = []

    dast_incidents = state.get("dast_incidents", [])
    attack_surface = state.get("attack_surface", {})
    trust_boundaries = state.get("trust_boundaries", [])

    # We pass minimal structure to avoid blowing up context window
    nodes_summary = [
        {"id": n.get("id"), "type": n.get("type"), "label": n.get("label")}
        for n in knowledge_graph.get("nodes", [])
    ]
    edges_summary = [
        {"source": e.get("source"), "target": e.get("target"), "relationship": e.get("relationship")}
        for e in knowledge_graph.get("edges", [])
    ]

    prompt = f"""
You are an expert Application Security Architect.

Evaluate the consolidated Security Knowledge Graph, the identified Attack Paths, and other assessment data to provide a final security reasoning.

KNOWLEDGE GRAPH NODES (Summary):
{json.dumps(nodes_summary, indent=2)[:2000]}

KNOWLEDGE GRAPH EDGES (Summary):
{json.dumps(edges_summary, indent=2)[:2000]}

ATTACK PATHS:
{json.dumps(attack_paths, indent=2)[:2000]}

SAST FINDINGS:
{json.dumps(sast_incidents, indent=2)[:2000]}

DAST FINDINGS:
{json.dumps(dast_incidents, indent=2)[:2000]}

ATTACK SURFACE:
{json.dumps(attack_surface, indent=2)[:1000]}

TRUST BOUNDARIES:
{json.dumps(trust_boundaries, indent=2)[:1000]}

Synthesize a comprehensive security reasoning that addresses the following:
1. Overall Risk (CRITICAL, HIGH, MEDIUM, LOW).
2. Most Likely Attack (Which attack path is the easiest for an attacker to execute).
3. Most Dangerous Attack (Which attack path has the highest business impact).
4. Business Impact (What happens to the business if these vulnerabilities are exploited).
5. Prioritized Findings (List the top 3 findings that need immediate attention).
6. Remediation Order (High-level order of operations for fixing the issues).

Return ONLY valid JSON in exactly this format:
{{
  "Overall Risk": "...",
  "Most Likely Attack": "...",
  "Most Dangerous Attack": "...",
  "Business Impact": "...",
  "Prioritized Findings": ["...", "...", "..."],
  "Remediation Order": ["...", "...", "..."]
}}
"""
    print("[SecurityReasoningAgent] Calling AI model for comprehensive reasoning...")

    try:
        llm = ChatOllama(model="qwen2.5:7b", temperature=0)
        response = llm.invoke(prompt)

        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            # Fallback if markdown formatting is present
            content = response.content.replace('```json', '').replace('```', '').strip()
            result = json.loads(content)

    except Exception as e:
        print(f"[SecurityReasoningAgent] Model invocation failed: {e}")
        result = {
            "Overall Risk": "UNKNOWN",
            "Most Likely Attack": "Failed to determine.",
            "Most Dangerous Attack": "Failed to determine.",
            "Business Impact": "Failed to generate business impact.",
            "Prioritized Findings": [],
            "Remediation Order": []
        }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    state["security_reasoning"] = result
    print("[SecurityReasoningAgent] Complete")
    return state
