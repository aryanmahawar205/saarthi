import json
from langchain_ollama import ChatOllama

OUTPUT_FILE = "reports/security_reasoning.json"

def run(state):
    knowledge_graph = state.get("security_knowledge_graph", {})
    attack_paths = state.get("attack_paths", [])

    prompt = f"""
You are an expert Application Security Architect.

Evaluate the consolidated Security Knowledge Graph and the identified Attack Paths:

KNOWLEDGE GRAPH:
{json.dumps(knowledge_graph, indent=2)[:4000]}

ATTACK PATHS:
{json.dumps(attack_paths, indent=2)[:2000]}

Synthesize a comprehensive security reasoning that addresses the following:
1. Overall Risk Level (CRITICAL, HIGH, MEDIUM, LOW).
2. Business Impact of the vulnerabilities if successfully exploited.
3. Exploitability context based on trust boundaries and attack surface.
4. Most dangerous attack chain / realistic attack scenario.
5. High-level runtime reasoning (what happens if these paths are actively exploited in production).

Return ONLY valid JSON in the following format:
{{
  "overall_risk": "...",
  "business_impact": "...",
  "exploitability": "...",
  "attack_scenario": "...",
  "runtime_reasoning": "..."
}}
"""
    print("[SecurityReasoningAgent] Calling AI model for comprehensive reasoning...")

    try:
        llm = ChatOllama(model="qwen2.5:7b", temperature=0)
        response = llm.invoke(prompt)

        # We assume the model reliably outputs valid JSON when prompted correctly.
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            # Fallback if markdown formatting is present
            content = response.content.replace('```json', '').replace('```', '').strip()
            result = json.loads(content)

    except Exception as e:
        print(f"[SecurityReasoningAgent] Model invocation failed: {e}")
        result = {
            "overall_risk": "UNKNOWN",
            "business_impact": "Failed to generate business impact.",
            "exploitability": "Failed to determine exploitability.",
            "attack_scenario": "Failed to generate scenario.",
            "runtime_reasoning": "Failed to analyze runtime aspects."
        }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    state["security_reasoning"] = result
    print("[SecurityReasoningAgent] Complete")
    return state
