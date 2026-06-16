import json

from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0
)


def run(state):

    findings = state["findings"]

    prompt = f"""
You are a security analyst.

Group these findings into incidents.

Findings:

{json.dumps(findings, indent=2)}

Return ONLY valid JSON.

Format:

[
  {{
    "incident":"SQL Injection",
    "findings":[
      "finding title"
    ]
  }}
]
"""

    print(
        "[CorrelationAgent] Calling model"
    )

    result = llm.invoke(prompt)

    print(
        "[CorrelationAgent] Complete"
    )

    state["incidents"] = result.content

    return state