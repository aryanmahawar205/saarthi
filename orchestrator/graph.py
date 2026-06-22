from agents.planning_agent import run as planning_agent

# Discovery
from agents.recon_agent import run as recon_agent
from agents.discovery_agent import run as discovery_agent
from agents.trust_boundary_agent import run as trust_boundary_agent
from agents.api_call_chain_agent import run as api_call_chain_agent
from agents.attack_surface_agent import run as attack_surface_agent

# SAST
from agents.pipeline_agent import run as pipeline_agent
from agents.context_agent import run as context_agent
from agents.correlation_agent import run as correlation_agent

# DAST
from agents.zap_agent import run as zap_agent
from agents.zap_parser_agent import run as zap_parser_agent
from agents.dast_correlation_agent import run as dast_correlation_agent

# Knowledge Graph
from agents.security_knowledge_graph_agent import run as security_knowledge_graph_agent

# Reasoning
from agents.attack_path_agent import run as attack_path_agent
from agents.security_reasoning_agent import run as security_reasoning_agent

# Remediation & Reporting
from agents.remediation_agent import run as remediation_agent
from agents.report_agent import run as report_agent


def print_state(stage, state):
    print(f"\n[{stage}] State Keys:")
    print(list(state.keys()))


def main():
    state = {}

    # ---------------------------------
    # Planning
    # ---------------------------------
    state = planning_agent(state)
    print_state("PlanningAgent", state)

    # ---------------------------------
    # Runtime Target Setup
    # ---------------------------------
    state["target_url"] = "http://localhost:8080/WebGoat/"
    state["project_root"] = "/workspaces/saarthi"

    # ---------------------------------
    # Phase 1: Discovery
    # ---------------------------------
    state = recon_agent(state)
    print_state("ReconAgent", state)

    state = discovery_agent(state)
    print_state("DiscoveryAgent", state)

    state = trust_boundary_agent(state)
    print_state("TrustBoundaryAgent", state)

    state = api_call_chain_agent(state)
    print_state("APICallChainAgent", state)

    state = attack_surface_agent(state)
    print_state("AttackSurfaceAgent", state)

    # ---------------------------------
    # Phase 2: SAST Pipeline
    # ---------------------------------
    state = pipeline_agent(state)
    print_state("PipelineAgent", state)

    state = context_agent(state)
    print_state("ContextAgent", state)

    state = correlation_agent(state)
    print_state("CorrelationAgent", state)

    # ---------------------------------
    # Phase 3: DAST Pipeline
    # ---------------------------------
    state = zap_agent(state)
    print_state("ZapAgent", state)

    state = zap_parser_agent(state)
    print_state("ZapParserAgent", state)

    state = dast_correlation_agent(state)
    print_state("DASTCorrelationAgent", state)

    # ---------------------------------
    # Phase 4: Knowledge Graph
    # ---------------------------------
    state = security_knowledge_graph_agent(state)
    print_state("SecurityKnowledgeGraphAgent", state)

    # ---------------------------------
    # Phase 5: AI Security Reasoning
    # ---------------------------------
    state = attack_path_agent(state)
    print_state("AttackPathAgent", state)

    state = security_reasoning_agent(state)
    print_state("SecurityReasoningAgent", state)

    # ---------------------------------
    # Phase 6: Remediation
    # ---------------------------------
    state = remediation_agent(state)
    print_state("RemediationAgent", state)

    # ---------------------------------
    # Phase 7: Reporting
    # ---------------------------------
    state = report_agent(state)
    print_state("ReportAgent", state)


if __name__ == "__main__":
    main()
