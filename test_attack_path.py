from agents.zap_parser_agent import run as zap_parser
from agents.dast_correlation_agent import run as correlate
from agents.attack_path_agent import run


state = {}

state = zap_parser(state)

state = correlate(state)

state = run(state)

print()

for path in state[
    "attack_paths"
]:

    print(
        path["name"]
    )

    print(
        " -> ".join(
            path["path"]
        )
    )

    print(
        f"Impact: "
        f"{path['impact']}"
    )

    print()