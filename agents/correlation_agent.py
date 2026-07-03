import json
from langchain_ollama import ChatOllama

try:
    llm = ChatOllama(model="qwen2.5:7b", temperature=0)
except Exception:
    llm = None

def run(state):
    findings = state.get("findings", [])
    if not findings:
         state["incidents"] = []
         return state

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
      {{"title": "finding title", "file": "file path"}}
    ]
  }}
]
"""

    print("[CorrelationAgent] Calling model")

    try:
        result = llm.invoke(prompt)
        content = result.content
        # Try to parse content as JSON
        try:
            incidents = json.loads(content)
        except json.JSONDecodeError:
            clean_content = content.replace('```json', '').replace('```', '').strip()
            incidents = json.loads(clean_content)
    except Exception as e:
        print(f"[CorrelationAgent] Model failed: {e}")
        # dummy fallback: one incident per finding
        incidents = []
        for f in findings:
            incidents.append({
                "incident": f.get("title"),
                "findings": [f]
            })

    print("[CorrelationAgent] Complete")

    state["incidents"] = incidents

    return state
