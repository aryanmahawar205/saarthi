# Codebase Cleanup Report

During Phase 2 implementation of the Saarthi Platform, several obsolete files and redundant logic blocks were identified and removed. This cleanup ensures that the codebase aligns tightly with the unified Collection -> Knowledge -> Reasoning -> Remediation -> Reporting layered architecture.

## Files Removed

1. `parsers/exploitability_engine.py`
   - **Reason for Removal:** Exploitability reasoning is now centralized. The `security_reasoning_agent.py` takes the full context (Knowledge Graph and Attack Paths) and intrinsically evaluates the exploitability, eliminating the need for a separate parser step.

2. `parsers/risk_prioritizer_v2.py`
   - **Reason for Removal:** Risk prioritization is handled directly by the AI model in `agents/security_reasoning_agent.py` during the unified reasoning phase. A standalone script to prioritize risk outside the centralized model causes duplicate logic and fragmentation.

## Obsolete Agents Confirmed Removed
The following files were confirmed to be fully removed (or never implemented in this iteration) to prevent duplicate reasoning:
- `business_impact_agent.py`
- `exploitability_agent.py`
- `final_risk_agent.py`
- `llm_attack_reasoning_agent.py`
- `runtime_reasoning_agent.py`
- `explanation_agent.py`
- `attack_simulation_agent.py`
- `attack_graph_agent.py`
- `runtime_attack_graph_agent.py`
- `multi_step_attack_chain_agent.py`

Their logic has been successfully consolidated into the new `security_knowledge_graph_agent.py`, `attack_path_agent.py`, and `security_reasoning_agent.py`.

## Redundant Logic Removed
- Duplicate logic regarding attack chain construction (from older implementations) was consolidated directly into the `attack_path_agent.py`, which now acts purely on the formalized Graph Nodes and Edges.
- Duplication in risk assignment was eliminated. The system relies entirely on the Qwen model output in the reasoning phase for assessing risk.
