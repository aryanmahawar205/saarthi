import argparse
import os
from agents.planning_agent import run as planning_agent

# Runtime Observation
from agents.runtime_observer_agent import start as start_runtime_observer
from agents.runtime_observer_agent import stop as stop_runtime_observer

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

# Runtime Intelligence
from runtime.collector.otel_collector import OTelFileCollector
from runtime.correlation.runtime_correlator import run_correlation as runtime_correlation

# Knowledge Graph
from agents.security_knowledge_graph_agent import run as security_knowledge_graph_agent

# Reasoning
from agents.attack_path_agent import run as attack_path_agent
from agents.security_reasoning_agent import run as security_reasoning_agent

# Remediation & Reporting
from agents.remediation_agent import run as remediation_agent
from agents.report_agent import run as report_agent
import subprocess

def print_state(stage, state):
    print(f"\n[{stage}] State Keys:")
    print(list(state.keys()))


def main():
    parser = argparse.ArgumentParser(description="Saarthi Security Orchestrator")
    parser.add_argument("--url", type=str, help="Target URL for DAST/Discovery")
    parser.add_argument("--repo", type=str, help="Target Repository Path for SAST")
    parser.add_argument("--runtime", type=str, help="Path to runtime intelligence feed (e.g., otel_spans.json)")
    args = parser.parse_args()

    state = {}

    if args.url:
        state["target_url"] = args.url
    if args.repo:
        state["project_root"] = args.repo
    else:
        state["project_root"] = os.getcwd() # default project root for things like zap

    run_url = args.url is not None
    run_repo = args.repo is not None
    run_runtime = args.runtime is not None

    # Determine Orchestration Mode
    mode = "Unknown"
    if run_repo and not run_url and not run_runtime:
        mode = "Mode 1 (SAST Only)"
    elif run_url and not run_repo and not run_runtime:
        mode = "Mode 2 (DAST Only)"
    elif run_repo and run_url and not run_runtime:
        mode = "Mode 3 (Hybrid SAST + DAST)"
    elif run_repo and run_url and run_runtime:
        mode = "Mode 4 (Full Spectrum: SAST + DAST + Runtime Intelligence)"

    print(f"\n[Orchestrator] Starting Saarthi in {mode}")

    if run_repo:
        # Parsers execution for context/dependency/api graphs
        print("\n[Orchestrator] Running Repository Parsers...")
        subprocess.run(["python3", "parsers/context_builder.py"], check=False)
        subprocess.run(["python3", "parsers/api_graph_builder.py"], check=False)
        subprocess.run(["python3", "parsers/dependency_graph_builder.py"], check=False)
        subprocess.run(["python3", "parsers/method_index_builder.py"], check=False)
        subprocess.run(["python3", "parsers/call_graph_builder.py"], check=False)

    # Planning
    state = planning_agent(state)
    print_state("PlanningAgent", state)

    if run_url:
        # Start Runtime Observer
        state = start_runtime_observer(state)
        print_state("RuntimeObserverStarted", state)

        # Phase 1: Discovery
        state = recon_agent(state)
        print_state("ReconAgent", state)

        state = discovery_agent(state)
        print_state("DiscoveryAgent", state)

        # Trust Boundary and Attack Surface need endpoints
        state = trust_boundary_agent(state)
        print_state("TrustBoundaryAgent", state)

        state = attack_surface_agent(state)
        print_state("AttackSurfaceAgent", state)

        # Phase 3: DAST Pipeline
        try:
            state = zap_agent(state)
            print_state("ZapAgent", state)

            state = zap_parser_agent(state)
            print_state("ZapParserAgent", state)

            state = dast_correlation_agent(state)
            print_state("DASTCorrelationAgent", state)
        except Exception as e:
            print(f"[Orchestrator] Warning: DAST Pipeline failed: {e}")

        # Stop Runtime Observer after DAST
        state = stop_runtime_observer(state)
        print_state("RuntimeObserverStopped", state)

    if run_repo:
        # Phase 2: SAST Pipeline
        try:
            state = pipeline_agent(state)
            print_state("PipelineAgent", state)
        except Exception as e:
            print(f"[Orchestrator] Warning: PipelineAgent (SAST) failed: {e}")

    if run_repo or run_url:
        # Context builder and correlation
        try:
            state = context_agent(state)
            print_state("ContextAgent", state)
        except Exception as e:
            print(f"[Orchestrator] Warning: ContextAgent failed: {e}")

        try:
            state = correlation_agent(state)
            print_state("CorrelationAgent", state)
        except Exception as e:
            print(f"[Orchestrator] Warning: CorrelationAgent failed: {e}")

        if not run_url:
            # If we didn't run URL discovery, we might need these agents for repo endpoints
            state = trust_boundary_agent(state)
            print_state("TrustBoundaryAgent", state)
            state = attack_surface_agent(state)
            print_state("AttackSurfaceAgent", state)

        state = api_call_chain_agent(state)
        print_state("APICallChainAgent", state)

    if run_runtime:
        print("\n[Orchestrator] Phase 3.5: Runtime Intelligence...")
        # 1. Collect and Normalize
        collector = OTelFileCollector(args.runtime)
        collector.start()
        events = collector.collect()
        state["runtime_events"] = events
        print(f"[Orchestrator] Collected {len(events)} normalized runtime events.")
        collector.stop()

        # 2. Correlate
        state = runtime_correlation(state)
        print_state("RuntimeCorrelator", state)


    # Phase 4: Knowledge Graph
    state = security_knowledge_graph_agent(state)
    print_state("SecurityKnowledgeGraphAgent", state)

    # Phase 5: AI Security Reasoning
    state = attack_path_agent(state)
    print_state("AttackPathAgent", state)

    state = security_reasoning_agent(state)
    print_state("SecurityReasoningAgent", state)

    # Phase 6: Remediation
    state = remediation_agent(state)
    print_state("RemediationAgent", state)

    # Phase 7: Reporting
    state = report_agent(state)
    print_state("ReportAgent", state)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Orchestrator] Interrupted by user. Cleaning up...")
        stop_runtime_observer({})
