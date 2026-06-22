# Codebase Analysis

## Current Architecture
The current orchestrator (`orchestrator/graph.py`) invokes numerous agents in a sequential, mostly DAST-focused pipeline, followed by a separate SAST pipeline:
- **Planning & Discovery:** `planning_agent`, `recon_agent`, `discovery_agent`, `trust_boundary_agent`, `api_call_chain_agent`
- **DAST:** `zap_agent`, `zap_parser_agent`, `dast_correlation_agent`, `attack_path_agent`, `attack_simulation_agent`, `multi_step_attack_chain_agent`, `attack_graph_agent`, `runtime_attack_graph_agent`
- **Reasoning/Scoring (Duplicated):** `exploitability_agent`, `business_impact_agent`, `llm_attack_reasoning_agent`, `final_risk_agent`, `attack_surface_agent`, `runtime_reasoning_agent`, `security_reasoning_agent`
- **SAST:** `pipeline_agent`, `context_agent`, `correlation_agent`, `explanation_agent`, `report_agent`

## Observations
1. **Scattered and Duplicated Reasoning:** The agents calculating risk, business impact, and exploitability are highly fragmented (`exploitability_agent.py`, `business_impact_agent.py`, `final_risk_agent.py`, `llm_attack_reasoning_agent.py`, etc.). This violates the principle of consolidating reasoning.
2. **DAST & SAST Disconnect:** The orchestrator executes DAST and its reasoning separately from SAST. Both streams should feed into a central Knowledge Graph to allow cross-correlation before reasoning.
3. **Redundant Graphs:** Multiple agents build partial attack graphs (`attack_graph_agent.py`, `runtime_attack_graph_agent.py`, `multi_step_attack_chain_agent.py`). A unified `SecurityKnowledgeGraphAgent` should consolidate this structure.
4. **Agent Bloat:** There are too many single-purpose agents that perform basic heuristic loops instead of utilizing combined AI reasoning on a single, rich context.

## Target Architecture
The goal is to streamline the execution into the following distinct phases as defined in the architectural direction:
1. **Discovery:** `recon_agent`, `discovery_agent`, `trust_boundary_agent`, `api_call_chain_agent`, `attack_surface_agent`
2. **SAST:** `pipeline_agent`, `context_agent`, `correlation_agent`
3. **DAST:** `zap_agent`, `zap_parser_agent`, `dast_correlation_agent`
4. **Knowledge Graph:** A new `security_knowledge_graph_agent` to synthesize Discovery, SAST, and DAST findings.
5. **AI Security Reasoning:** A revamped `security_reasoning_agent` replacing all the fragmented reasoning and scoring agents.
6. **Remediation:** A new `remediation_agent` for generating remediation guidance.
7. **Reporting:** A comprehensive `report_agent`.

This shift transitions the application from a "Scanner Collection" approach to a context-aware "AI-Assisted Security Assessment Platform".
