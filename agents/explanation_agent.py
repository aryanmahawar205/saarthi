from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0
)


def run(state):

    prompt = f"""
Explain these incidents.

{state["incidents"]}

For each incident provide:

- Business Impact
- Attack Scenario
- Remediation

Return markdown.
"""

    print(
        "[ExplanationAgent] Calling model"
    )

    result = llm.invoke(prompt)

    state["analysis"] = result.content

    return state