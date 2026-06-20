import json

from langchain_ollama import ChatOllama


OUTPUT_FILE = (
    "reports/security_reasoning.json"
)


def load_top_findings():

    try:

        with open(
            "reports/final_prioritized_findings.json"
        ) as f:

            findings = json.load(f)

        return findings[:20]

    except Exception:

        return []


def run(state):

    attack_surface = state.get(
        "attack_surface",
        {}
    )

    trust_boundaries = state.get(
        "trust_boundaries",
        []
    )

    api_call_chains = state.get(
        "api_call_chains",
        []
    )

    dast_findings = state.get(
        "dast_findings",
        []
    )

    dast_incidents = state.get(
        "dast_incidents",
        []
    )

    attack_paths = state.get(
        "attack_paths",
        []
    )

    runtime_reasoning = state.get(
        "runtime_reasoning",
        {}
    )

    top_findings = load_top_findings()

    prompt = f"""
You are a senior application security architect.

Analyze the following information.

ATTACK SURFACE:
{json.dumps(attack_surface, indent=2)}

TRUST BOUNDARIES:
{json.dumps(trust_boundaries[:20], indent=2)}

API CALL CHAINS:
{json.dumps(api_call_chains[:20], indent=2)}

DAST FINDINGS:
{json.dumps(dast_findings[:20], indent=2)}

DAST INCIDENTS:
{json.dumps(dast_incidents, indent=2)}

ATTACK PATHS:
{json.dumps(attack_paths, indent=2)}

RUNTIME REASONING:
{json.dumps(runtime_reasoning, indent=2)}

TOP SAST FINDINGS:
{json.dumps(top_findings, indent=2)}

Determine:

1. Overall Risk
2. Most Likely Attack Scenario
3. Most Dangerous Attack Chain
4. Business Impact
5. Top 5 Security Findings
6. Recommended Fix Order

Return ONLY valid JSON.

Example:

{{
  "overall_risk": "HIGH",
  "most_likely_attack": "...",
  "attack_chain": [
    "...",
    "..."
  ],
  "business_impact": "...",
  "top_findings": [
    "...",
    "..."
  ],
  "recommended_fix_order": [
    "...",
    "..."
  ]
}}
"""

    print(
        "[SecurityReasoningAgent] Calling model"
    )

    llm = ChatOllama(
        model="qwen2.5:7b",
        temperature=0
    )

    response = llm.invoke(
        prompt
    )

    result = {

        "analysis":
            response.content
    }

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            result,
            f,
            indent=2
        )

    state[
        "security_reasoning"
    ] = result

    print(
        "[SecurityReasoningAgent] Complete"
    )

    return state


if __name__ == "__main__":

    run({})