from agents.planning_agent import run as planning_agent
from agents.pipeline_agent import run as pipeline_agent
from agents.context_agent import run as context_agent
from agents.correlation_agent import run as correlation_agent
from agents.explanation_agent import run as explanation_agent
from agents.report_agent import run as report_agent
from agents.recon_agent import run as recon_agent


def print_state(stage, state):

    print(
        f"\n[{stage}] State Keys:"
    )

    print(
        list(state.keys())
    )


def main():

    state = {}

    state = planning_agent(state)

    state["target_url"] = (
        "http://localhost:8080/WebGoat/"
    )

    state = recon_agent(state)

    print_state(
        "ReconAgent",
        state
    )

    print_state(
        "PlanningAgent",
        state
    )

    state = pipeline_agent(state)

    print_state(
        "PipelineAgent",
        state
    )

    state = context_agent(state)

    print_state(
        "ContextAgent",
        state
    )

    state = correlation_agent(state)

    print_state(
        "CorrelationAgent",
        state
    )

    state = explanation_agent(state)

    print_state(
        "ExplanationAgent",
        state
    )

    state = report_agent(state)

    print_state(
        "ReportAgent",
        state
    )


if __name__ == "__main__":
    main()