import json

from langchain_ollama import ChatOllama


OUTPUT_FILE = (
    "reports/llm_attack_reasoning.json"
)


def run(state):

    findings = state.get(
        "dast_findings",
        []
    )

    incidents = state.get(
        "dast_incidents",
        []
    )

    attack_paths = state.get(
        "attack_paths",
        []
    )

    impacts = state.get(
        "business_impacts",
        []
    )

    trust_boundaries = state.get(
        "trust_boundaries",
        []
    )

    prompt = f"""
You are a senior penetration tester.

Analyze:

DAST Findings:
{json.dumps(findings[:20], indent=2)}

Incidents:
{json.dumps(incidents, indent=2)}

Attack Paths:
{json.dumps(attack_paths, indent=2)}

Business Impacts:
{json.dumps(impacts, indent=2)}

Trust Boundaries:
{json.dumps(trust_boundaries, indent=2)}

Produce:

1. Most likely attack scenario
2. Initial attack vector
3. Exploitation path
4. Business impact
5. Remediation priority

Return concise JSON.
"""

    llm = ChatOllama(
        model="qwen2.5:7b",
        temperature=0
    )
    
    result = llm.invoke(
        prompt
    )

    output = {
        "analysis":
            result.content
    }

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            output,
            f,
            indent=2
        )

    state[
        "llm_attack_reasoning"
    ] = output

    print(
        "[LLMAttackReasoningAgent] Complete"
    )

    return state