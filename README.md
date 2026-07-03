# Saarthi

Saarthi is an AI-Assisted Security Assessment Platform that shifts the paradigm from simply aggregating scanner outputs to behaving like an intelligent security analyst. It combines SAST, DAST, runtime discovery, and context-aware reasoning to produce high-quality, actionable security reports.

## Architecture Diagram
```
Runtime-Aware AI Analysis
       ↓
Knowledge Layer (Graph)
       ↓
Security Reasoning Layer
       ↓
Remediation Layer
       ↓
Reporting Layer
```

For more detailed architecture information, please see [ARCHITECTURE.md](docs/ARCHITECTURE.md) and [RUNTIME_INTELLIGENCE.md](docs/RUNTIME_INTELLIGENCE.md).

## Agent Responsibilities
- **Runtime Observer Agent**: Captures live application traffic using mitmproxy.
- **Recon & Discovery Agents**: Map the application's attack surface and runtime behavior, utilizing the observer.
- **Trust Boundary & API Chain Agents**: Identify data flow boundaries and endpoint logic.
- **Scanner Agents (ZAP, Pipeline)**: Execute DAST and SAST tools.
- **Security Knowledge Graph Agent**: Synthesizes findings, boundaries, and surfaces into a unified graph format (`nodes` and `edges`).
- **Attack Path Agent**: Derives realistic attack chains from the knowledge graph and runtime evidence.
- **Security Reasoning Agent**: The central AI "brain". Computes overall risk, business impact, exploitability, and prioritizes findings based on runtime awareness.
- **Remediation Agent**: Formulates strategies to fix identified risks.
- **Report Agent**: Generates the final, comprehensive Markdown assessment.

## Data Flow & Example Execution Flow
1. **Setup**: The target URL and project root are defined.
2. **Phase 1 (Discovery)**: The platform crawls endpoints and maps boundaries.
3. **Phase 2 & 3 (SAST/DAST)**: Analyzers find vulnerabilities.
4. **Phase 4 (Knowledge)**: The `security_knowledge_graph.json` is generated, linking endpoints to vulnerabilities.
5. **Phase 5 (Reasoning)**: `attack_chains.json` and `security_reasoning.json` are created based on the AI's contextual evaluation of the graph.
6. **Phase 6 & 7 (Remediation & Reporting)**: Actionable guidance is generated, culminating in `final_security_assessment.md`.

## Example Reports
The platform generates several artifacts during execution:
- `reports/security_knowledge_graph.json`: Nodes and edges representing the application state.
- `reports/attack_chains.json`: Realistic exploitation sequences.
- `reports/security_reasoning.json`: Structured AI evaluation of risk and impact.
- `reports/final_security_assessment.md`: A consultant-grade executive and technical summary.

## Future Roadmap
- Deeper native integrations with modern frameworks (e.g., GraphQL, gRPC).
- AI-Assisted Custom Rule Discovery and continuous knowledge base updates.
- Extended Cloud-Native (Kubernetes/AWS) runtime boundary mapping.
- Enhanced Remediation via Automated Pull Requests.

## Execution
To run the full assessment pipeline:
```bash
python3 -m orchestrator.graph
```
