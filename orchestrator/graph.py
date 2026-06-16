from agents.context_agent import run as context_agent
from agents.correlation_agent import run as correlation_agent
from agents.explanation_agent import run as explanation_agent
from agents.report_agent import run as report_agent


def main():

    state = {}

    state = context_agent(state)

    state = correlation_agent(state)

    state = explanation_agent(state)

    state = report_agent(state)


if __name__ == "__main__":
    main()