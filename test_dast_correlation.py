from agents.zap_parser_agent import run as zap_parser
from agents.dast_correlation_agent import run


state = {}

state = zap_parser(state)

state = run(state)

print()

for incident in state[
    "dast_incidents"
]:

    print(
        incident["incident"]
    )

    print(
        len(
            incident["findings"]
        )
    )

    print()