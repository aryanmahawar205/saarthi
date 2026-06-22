# Phase 3 Changes

## Overview
This document outlines the architectural enhancements and cleanups performed in Phase 3 of the Saarthi platform development. The goal was to establish a fully robust, multi-mode AI-assisted security analyst.

## Multi-Mode Execution
`orchestrator/graph.py` was refactored to support conditional execution of different analysis pipelines. Using `argparse`, the orchestrator now accepts `--url` and `--repo` arguments.
* **Mode A (URL Only)**: Executes the DAST pipeline (Recon, Discovery, ZAP) followed by the unified Knowledge and Reasoning tail.
* **Mode B (Repo Only)**: Executes the SAST pipeline (Context Builder, API Graph, Dependency Graph, Semgrep, Trivy, Gitleaks via `pipeline_agent`) followed by the unified tail.
* **Mode C (Hybrid Mode)**: Executes both DAST and SAST paths, correlating findings centrally before reasoning.

## Security Knowledge Graph Overhaul
The `security_knowledge_graph_agent.py` was structurally enhanced to become the central ground truth of the system.
* It now enforces explicit edge schemas linking: `Endpoint -> Controller -> Method -> Sink -> Finding -> Attack Chain / Trust Boundary`.
* Attack Chains were linked directly to Business Impact.
* The output is strictly formatted into a hierarchical JSON with explicit `nodes` and `edges` lists.

## Runtime Discovery Enhancements
The `discovery_agent.py` was improved to perform deep discovery:
* Iterate and query specific high-value paths: `/sitemap.xml`, `/robots.txt`, `/v3/api-docs`, `/openapi.json`, `/swagger-ui.html`, `/swagger.json`.
* Scan `.js` JavaScript files to extract internal API routing utilizing regex endpoint matchers.

## Security Reasoning Consolidation
`security_reasoning_agent.py` became the platform's primary AI core. It was updated to inject all layers of information into its context window:
* SAST Findings
* DAST Findings
* Attack Surface context
* Discovered Trust Boundaries
* Generated Security Graph
* Generated Attack Chains
* Outputs unified JSON structures standardizing Risk, Danger, Impact, and Remediation steps.

## Executive Reporting Alignment
`report_agent.py` was aligned to produce high-level consultant-style markdown reports (`reports/final_security_assessment.md`).
* Sections explicitly define the scope, environment, boundaries, and static/runtime findings before providing AI-backed Attack Scenarios, Business Impacts, and Prioritized Executive Recommendations.

## Clean Up
Redundant and standalone procedural agents previously scattered across `parsers/` and `agents/` were deleted to unify the logic into the sequential layer pattern:
* Removed `agents/dast_agent.py` (replaced by unified zap orchestrator blocks).
* Removed `agents/scanner_execution_agent.py`.
* Removed `parsers/ai_security_analyst.py` (duplicate reasoning).
* Removed `parsers/report_generator.py` (duplicate reporting).
