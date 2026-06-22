# SAARTHI

## What This Project Is

Saarthi is an AI-Assisted Security Assessment Platform.

The objective is NOT to become another scanner.

The objective is to behave like a security analyst that combines:

* SAST
* DAST
* Runtime Discovery
* Attack Surface Mapping
* Trust Boundary Analysis
* AI Security Reasoning

to produce analyst-quality security reports.

---

## Current Status

Implemented:

* Semgrep Integration

* Trivy Integration

* Gitleaks Integration

* OWASP ZAP Integration

* Finding Normalization

* Correlation Engine

* Prioritization Engine

* Runtime Discovery

* Attack Surface Discovery

* Trust Boundary Mapping

* API Call Chain Mapping

* DAST Correlation

* Attack Path Generation

* AI Report Generation

Current primary target:

WebGoat

---

## Before Making Changes

You MUST first understand:

1. orchestrator/graph.py
2. all agents/
3. all parsers/
4. report generation flow
5. DAST flow
6. SAST flow

Generate:

docs/CODEBASE_ANALYSIS.md

before making architectural changes.

---

## Long-Term Architecture

Collection Layer

* ReconAgent
* DiscoveryAgent
* ZapAgent
* PipelineAgent

Knowledge Layer

* TrustBoundaryAgent
* APICallChainAgent
* SecurityKnowledgeGraphAgent

Reasoning Layer

* AttackPathAgent
* RuntimeReasoningAgent
* SecurityReasoningAgent

Remediation Layer

* RemediationCodeAgent

Reporting Layer

* ReportAgent

---

## Important Rule

Prefer improving reasoning quality over adding more agents.

Avoid duplicate:

* Risk scoring
* Business impact
* Attack reasoning
* Prioritization

The project should converge toward a centralized SecurityReasoningAgent.

---

## Final Goal

Input:

Repository Path
+
Running Application URL

Output:

* Runtime Attack Surface
* Static Findings
* Dynamic Findings
* Correlated Incidents
* Attack Chains
* Risk Assessment
* Remediation Guidance
* Executive Security Report

The entire flow should run through:

python3 -m orchestrator.graph
