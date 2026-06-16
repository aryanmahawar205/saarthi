# test_ollama.py

from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen2.5:7b"
)

print("calling")

result = llm.invoke(
    "hello in one sentence"
)

print(result.content)