from agents.zap_parser_agent import run as zap_parser
from agents.dast_correlation_agent import run as correlate
from agents.security_knowledge_graph_agent import run as knowledge_graph
from agents.attack_path_agent import run as attack_path


state = {}

state = zap_parser(state)
state = correlate(state)
state = knowledge_graph(state)
state = attack_path(state)

print()

for path in state.get("attack_paths", []):
    print(path["name"])
    print(" -> ".join(path["path"]))
    print(f"Impact: {path['impact']}")
    print()
