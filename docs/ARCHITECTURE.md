# Architecture

Saarthi operates as an AI-Assisted Security Assessment Platform modeled after a sequential data pipeline. The architecture is explicitly designed to move from raw data collection to high-level reasoning and reporting.

The architecture is divided into five distinct layers:

## 1. Collection Layer
This layer is responsible for gathering raw data about the application. It discovers endpoints, maps trust boundaries, constructs call chains, and executes security scanners.
- **Runtime Observer**: Uses mitmproxy to capture live traffic, providing empirical evidence of application behavior.
- **Recon / Discovery**: Identifies what the application is and its surface area, enhanced by deep crawling (Robots, Sitemaps, Swagger).
- **SAST / DAST**: Discovers potential vulnerabilities from source code and runtime behavior.
- **Outputs**: Discovered endpoints, raw incidents, call graphs, and **Runtime Observations**.

## 2. Knowledge Layer
The Knowledge Layer takes the disparate data points from the Collection Layer and synthesizes them into a unified, graph-based structure.
- **SecurityKnowledgeGraphAgent**: Combines attack surfaces, runtime observations (Requests, Responses, Cookies), trust boundaries, call chains, and incidents into a formalized set of `nodes` and `edges`.
- **Outputs**: `security_knowledge_graph.json`

## 3. Security Reasoning Layer
This is the core "brain" of the platform. It evaluates the relationships defined in the Knowledge Layer.
- **AttackPathAgent**: Ingests the knowledge graph and traces realistic attack chains (e.g., from an external input, crossing a trust boundary, exploiting a vulnerability, leading to a business impact).
- **SecurityReasoningAgent**: A centralized AI evaluation component. It reads the graph and the attack chains to compute the overall risk, most likely attack scenarios, the business impact, and prioritize the findings.
- **Outputs**: `attack_chains.json`, `security_reasoning.json`

## 4. Remediation Layer
Translates the prioritized reasoning into actionable guidance.
- **RemediationAgent**: Reviews the prioritized risks and provides strategic advice and specific incident remediation steps.
- **Outputs**: Remediation Guidance mapping.

## 5. Reporting Layer
Generates the human-readable output of the entire platform's effort.
- **ReportAgent**: Formats the reasoning, attack paths, boundaries, and remediation strategies into a cohesive, professional-grade Markdown document intended for executive and engineering review.
- **Outputs**: `final_security_assessment.md`

## Converged Pipeline Execution Flow
The orchestrator (`orchestrator/graph.py`) executes these layers sequentially.

```
Collection Layer (Recon/Discovery/SAST/DAST)
       ↓
Knowledge Layer (Graph generation)
       ↓
Reasoning Layer (Attack paths & AI Risk Evaluation)
       ↓
Remediation Layer (Actionable steps)
       ↓
Reporting Layer (Final Assessment Document)
```
