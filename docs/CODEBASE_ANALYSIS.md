# Saarthi Codebase Analysis

## Overview
Saarthi is an AI-assisted security assessment platform that integrates SAST, DAST, and runtime discovery. It uses a graph-based approach to represent the application's security state and employs AI to reason about attack paths and risks.

## Core Components

### Orchestrator
- `orchestrator/graph.py`: The central execution engine. It manages the state and sequences the execution of various agents based on the target (URL and/or Repository). It currently supports three modes: SAST only, DAST only, and SAST + DAST.

### Agents (`agents/`)
- **Discovery & Recon**: `recon_agent.py`, `discovery_agent.py`, `attack_surface_agent.py`.
- **Static Analysis (SAST)**: `pipeline_agent.py` (integrates Semgrep, Trivy, Gitleaks).
- **Dynamic Analysis (DAST)**: `zap_agent.py`, `zap_parser_agent.py`, `dast_correlation_agent.py`.
- **Knowledge Layer**: `security_knowledge_graph_agent.py`, `trust_boundary_agent.py`, `api_call_chain_agent.py`.
- **Reasoning Layer**: `attack_path_agent.py`, `security_reasoning_agent.py`.
- **Remediation & Reporting**: `remediation_agent.py`, `report_agent.py`.
- **Runtime Observation**: `runtime_observer_agent.py` and `mitm_logger.py` (using `mitmproxy`).

### Parsers (`parsers/`)
- A variety of parsers for tool outputs (Semgrep, Trivy, ZAP, etc.) and for building structural models (API graphs, call graphs, dependency graphs).

### Schemas (`schemas/`)
- Defines the data models used across the platform.

## Current Runtime Implementation
The existing runtime observation is performed at the network level using `mitmproxy`. It captures HTTP requests and responses, which are then stored in `reports/runtime_observations.json` and ingested into the `SecurityKnowledgeGraphAgent`.

## Identified Gaps for Runtime Intelligence Initiative
1. **Lack of Code-Level Visibility**: Current observation is limited to the network layer. It doesn't see internal function calls, database queries, or execution flows within the application.
2. **Missing Normalization**: While HTTP traffic is captured, there's no unified model for different types of runtime events (e.g., internal spans vs. network traffic).
3. **Implicit Correlation**: Correlation between runtime data and findings is relatively shallow.
4. **Monolithic Observation**: The current `RuntimeObserverAgent` is tightly coupled with `mitmproxy`.

## Proposed Architectural Enhancements
- **Abstraction-First Design**: Introduce `RuntimeEvent`, `RuntimeTrace`, and `RuntimeEvidence` models.
- **Pluggable Adapters**: Support multiple providers (OpenTelemetry, language-specific agents, eBPF).
- **Dedicated Correlation**: A `RuntimeCorrelator` to bridge the gap between static/dynamic findings and runtime execution evidence.
- **Runtime-Aware Reasoning**: Enhance AI agents to prioritize and reason based on confirmed runtime execution.
