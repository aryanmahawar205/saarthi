import json
from langchain_ollama import ChatOllama

try:
    llm = ChatOllama(model="qwen2.5:7b", temperature=0)
except Exception:
    llm = None

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

    print("[CorrelationAgent] Calling model")

    try:
        result = llm.invoke(prompt)
        content = result.content
    except Exception as e:
        print(f"[CorrelationAgent] Model failed: {e}")
        # dummy fallback
        content = json.dumps([])

    print("[CorrelationAgent] Complete")

    state["incidents"] = content

    return state
