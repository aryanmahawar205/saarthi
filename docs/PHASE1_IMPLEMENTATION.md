# Phase 1 Implementation Plan

## 1. Eliminate Duplicate Reasoning Agents
We will consolidate fragmented reasoning processes. The following scripts will be deleted:
- `agents/business_impact_agent.py`
- `agents/exploitability_agent.py`
- `agents/llm_attack_reasoning_agent.py`
- `agents/final_risk_agent.py`
- `agents/runtime_reasoning_agent.py`
- `agents/explanation_agent.py`
- `agents/attack_simulation_agent.py`

Their functionality (business impact, exploitability scoring, attack chains, and runtime/risk reasoning) will be performed by a single, centralized `agents/security_reasoning_agent.py`.

## 2. Introduce the Central Security Knowledge Graph
We will delete redundant and fragmented graph builders:
- `agents/attack_graph_agent.py`
- `agents/runtime_attack_graph_agent.py`
- `agents/multi_step_attack_chain_agent.py`

Instead, a new `agents/security_knowledge_graph_agent.py` will gather discovery boundaries, call chains, SAST findings, and DAST incidents into a single cohesive structure (`reports/security_knowledge_graph.json`), to be consumed by the reasoning layer.

## 3. Centralize Attack Path Reasoning
`agents/attack_path_agent.py` will be rewritten to read from the newly generated `security_knowledge_graph.json` and optionally the AI-generated attack reasoning to determine definitive, context-aware attack paths.

## 4. Comprehensive Security Reasoning Agent
`agents/security_reasoning_agent.py` will evaluate the centralized Security Knowledge Graph alongside generated attack paths to compute risk scores, summarize business impact, determine exploitability, and provide human-readable reasoning.

## 5. Remediation Agent
A new `agents/remediation_agent.py` will be created to read from the reasoning outputs and propose detailed remediation strategies, acting entirely within the remediation layer.

## 6. Report Agent Restructuring
`agents/report_agent.py` will be updated to output a high-quality Markdown report that consumes the central reasoning, attack paths, and remediation guidance, presenting a unified Executive Report + Technical Report structure.

## 7. Orchestrator Streamlining
`orchestrator/graph.py` will be rebuilt. It will execute:
1. Discovery (Recon, Discovery, Attack Surface, Trust Boundaries, Call Chains)
2. SAST (Pipeline, Context, Correlation)
3. DAST (ZAP, ZAP Parser, DAST Correlation)
4. Knowledge Layer (Security Knowledge Graph Agent)
5. Reasoning Layer (Attack Path Agent, Security Reasoning Agent)
6. Remediation Layer (Remediation Agent)
7. Reporting Layer (Report Agent)

This sequence aligns strictly with the overarching architectural direction.
