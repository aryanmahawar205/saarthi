from agents.planning_agent import run as planning_agent

from agents.recon_agent import run as recon_agent
from agents.discovery_agent import run as discovery_agent
from agents.zap_agent import run as zap_agent
from agents.zap_parser_agent import run as zap_parser_agent
from agents.dast_correlation_agent import run as dast_correlation_agent
from agents.attack_path_agent import run as attack_path_agent
from agents.attack_surface_agent import run as attack_surface_agent

from agents.pipeline_agent import run as pipeline_agent
from agents.context_agent import run as context_agent
from agents.correlation_agent import run as correlation_agent
from agents.explanation_agent import run as explanation_agent
from agents.report_agent import run as report_agent
from agents.runtime_reasoning_agent import run as runtime_reasoning_agent
from agents.trust_boundary_agent import run as trust_boundary_agent
from agents.api_call_chain_agent import run as api_call_chain_agent


def print_state(stage, state):

    print(
        f"\n[{stage}] State Keys:"
    )

    print(
        list(state.keys())
    )


def main():

    state = {}

    # ---------------------------------
    # Planning
    # ---------------------------------

    state = planning_agent(state)

    print_state(
        "PlanningAgent",
        state
    )

    # ---------------------------------
    # Runtime Target
    # ---------------------------------

    state["target_url"] = (
        "http://localhost:8080/WebGoat/"
    )

    state["project_root"] = (
        "/workspaces/saarthi"
    )

    # ---------------------------------
    # DAST Pipeline
    # ---------------------------------

    state = recon_agent(state)

    print_state(
        "ReconAgent",
        state
    )

    state = discovery_agent(state)

    print_state(
        "DiscoveryAgent",
        state
    )

    state = trust_boundary_agent(state)

    print_state(
        "TrustBoundaryAgent",
        state
    )

    state = api_call_chain_agent(state)

    print_state(
        "APICallChainAgent",
        state
    )

    state = zap_agent(state)

    print_state(
        "ZapAgent",
        state
    )

    state = zap_parser_agent(state)

    print_state(
        "ZapParserAgent",
        state
    )

    state = dast_correlation_agent(state)

    print_state(
        "DASTCorrelationAgent",
        state
    )

    state = attack_path_agent(state)

    print_state(
        "AttackPathAgent",
        state
    )

    state = attack_surface_agent(state)

    print_state(
        "AttackSurfaceAgent",
        state
    )

    state = runtime_reasoning_agent(state)

    print_state(
        "RuntimeReasoningAgent",
        state
    )

    # ---------------------------------
    # Existing SAST Pipeline
    # ---------------------------------

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