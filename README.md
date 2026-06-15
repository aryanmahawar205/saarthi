# SAARTHI

## Security Assessment and AI Reasoning for Threat Hunting & Intelligence

> An AI-assisted software assurance platform for secure, sovereign, and air-gapped environments.

SAARTHI combines application context analysis, graph-based software understanding, automated security tooling, vulnerability correlation, attack-path reasoning, and human oversight to improve the effectiveness of software security assessments.

Unlike traditional security pipelines that simply aggregate scanner outputs, SAARTHI attempts to understand the application before initiating analysis, enabling context-aware security assessments and more meaningful findings.

---

# Vision

Modern security programs often rely on a growing collection of scanners, dashboards, and reports. While these tools are valuable, they frequently produce fragmented results that lack context, prioritization, and actionable insight.

SAARTHI aims to bridge this gap by combining deterministic security tooling with local AI reasoning capabilities.

The platform is designed to function as an AI-assisted security analyst that can:

- Understand application architecture
- Build software context
- Coordinate security tooling
- Correlate findings across multiple sources
- Identify attack paths
- Explain risks in business and technical terms
- Generate remediation guidance
- Maintain human oversight throughout the assessment lifecycle

SAARTHI is built for environments where security, explainability, sovereignty, and auditability are mandatory.

---

# About Movement Anti-Mythos

SAARTHI is developed under the **Movement Anti-Mythos** initiative.

The initiative challenges several common assumptions found in modern software security programs:

- More scanners do not automatically create better security.
- More vulnerabilities do not automatically indicate greater risk.
- AI should not replace security engineers.
- Security decisions should not be based on opaque models.
- Findings without context create noise rather than insight.

Movement Anti-Mythos promotes:

- Evidence-driven security assessment
- Explainable AI-assisted reasoning
- Human-centered decision making
- Repository-level understanding
- Traceable and auditable analysis

Inspired by lessons learned from modern AI systems and software assurance research, SAARTHI treats AI as a reasoning assistant—not as an unquestionable authority.

---

# Core Principles

## Human-in-the-Loop Security

AI assists.

Humans decide.

AI may:

- Analyze
- Explain
- Correlate
- Recommend
- Prioritize

Humans must:

- Validate findings
- Approve custom rules
- Authorize remediation
- Review reports
- Make security decisions

---

## Deterministic Tools Remain the Source of Truth

Security findings originate from deterministic security tools.

AI does not replace scanners.

Instead, it enhances them by providing:

- Context
- Correlation
- Prioritization
- Explanation
- Repository-level reasoning

---

## Fully Air-Gapped by Design

SAARTHI is designed for deployment within secure and disconnected environments.

### Guarantees

- No internet connectivity required
- No cloud AI services
- No external APIs
- No source code leaves the environment
- No findings are transmitted externally
- Local inference only
- Local databases only

---

# Key Capabilities

## Application Context Analysis

Before scanning begins, SAARTHI attempts to understand the application itself.

Questions it seeks to answer include:

- Is this a web application?
- Does it expose APIs?
- Is authentication implemented?
- Are containers used?
- Are there multiple microservices?
- Is there a database layer?
- Are trust boundaries present?
- Which components are business critical?

This context becomes the foundation for all downstream analysis.

---

## Graph-Based Software Understanding

SAARTHI constructs higher-level software representations.

### Call Graph

Maps execution flow through the application.

```text
Controller
    │
    ▼
Service
    │
    ▼
Repository
    │
    ▼
Database
```

Used for:

- Attack path analysis
- Data flow understanding
- Trust boundary discovery

---

### Dependency Graph

Represents relationships between:

- Libraries
- Services
- Containers
- Infrastructure

Used for:

- Supply chain analysis
- Blast radius estimation
- Risk prioritization

---

### API Graph

Represents communication pathways.

```text
Client
    │
    ▼
API Gateway
    │
    ▼
Service
    │
    ▼
Database
```

Used for:

- API attack surface mapping
- Authentication analysis
- Authorization analysis

---

# Architecture

## Architecture Option 1
### AI-Assisted Security Analysis

The initial deployment architecture.

```text
Repository
      │
      ▼

Security Tools
(CodeQL, Semgrep, SCA, etc.)

      │
      ▼

AI Security Analyst

      │
      ▼

Human Review

      │
      ▼

Security Report
```

### AI Responsibilities

- Correlate findings across scanners
- Remove duplicate findings
- Explain vulnerabilities
- Prioritize risks
- Generate remediation guidance
- Produce executive reports
- Map findings to:
  - CWE
  - OWASP
  - MITRE ATT&CK

### Advantages

- Easy to deploy
- Easy to accredit
- Deterministic workflows
- Fully auditable
- Human oversight preserved

### Limitation

The AI receives findings after scanners complete execution and therefore has limited understanding of application architecture.

---

## Architecture Option 2
### AI-Orchestrated Security Assessment

Recommended long-term direction.

```text
Repository
      │
      ▼

Context Builder

      │
      ▼

AI Security Orchestrator

      ├── CodeQL
      ├── Semgrep
      ├── SCA
      ├── Trivy
      ├── Grype
      ├── OWASP ZAP
      └── Custom Rules

      │
      ▼

Findings Correlation

      │
      ▼

Attack Path Analysis

      │
      ▼

Reporting
```

Instead of blindly executing every tool, the AI first attempts to understand the application and then builds an assessment strategy.

This transforms SAARTHI from a scanner aggregation platform into an AI-assisted software assurance system.

---

# Context Builder

The Context Builder is the foundation of SAARTHI.

Most security tools operate at:

- File level
- Function level
- Module level

The Context Builder creates repository-wide understanding.

Outputs include:

- Call graphs
- Dependency graphs
- API graphs
- Service maps
- Trust boundary maps
- Authentication maps
- Data flow relationships

These artifacts provide context for both scanners and AI agents.

---

# AI Security Orchestrator

The AI Security Orchestrator acts as the central decision-making component.

Instead of a fixed workflow, it dynamically determines:

- Which tools should run
- Which repositories require deeper inspection
- Which components are critical
- Which findings require escalation
- Whether runtime testing is needed
- Which attack paths deserve investigation

---

## Example

For a Spring Boot application exposing REST APIs:

SAARTHI may automatically:

- Run CodeQL
- Run Semgrep
- Generate API inventory
- Analyze authentication flows
- Schedule OWASP ZAP scanning
- Prioritize exposed endpoints

For embedded firmware:

SAARTHI may:

- Skip ZAP
- Focus on:
  - Static analysis
  - Binary analysis
  - Dependency analysis

---

# Agentic AI Framework

SAARTHI's orchestration layer is designed around LangGraph.

## Why LangGraph?

- Open source
- Fully local deployment
- Stateful workflows
- Multi-agent architecture
- Strong Python ecosystem
- Air-gap friendly

---

## Agent Workflow

```text
Repository Submitted
          │
          ▼

Planning Agent

          ▼

Context Analysis Agent

          ▼

Scanner Execution Agent

          ▼

Findings Correlation Agent

          ▼

Attack Path Agent

          ▼

Reporting Agent
```

Each agent specializes in a particular responsibility while sharing contextual information.

---

# IRIS-Inspired Neuro-Symbolic Analysis

SAARTHI incorporates concepts inspired by the IRIS research framework for vulnerability detection.

IRIS demonstrated that large language models can significantly improve static analysis when combined with repository-wide reasoning.

Rather than replacing static analysis, IRIS combines:

- Large Language Models
- Static Taint Analysis
- Contextual Reasoning

to improve vulnerability detection.

---

## AI-Assisted Source Discovery

Identify:

- User-controlled inputs
- External entry points
- API endpoints
- Trust boundaries

---

## AI-Assisted Sink Discovery

Identify:

- Command execution
- Dynamic evaluation
- File operations
- Database operations
- Dangerous APIs

---

## Contextual Vulnerability Analysis

Instead of trusting every static-analysis result, SAARTHI evaluates:

- Exploitability
- Authentication requirements
- Business context
- Trust boundaries
- Existing controls

This reduces false positives while preserving traceability.

---

# AI-Assisted Rule Discovery

Future capability inspired by IRIS.

Traditional scanners rely on manually maintained rules.

This creates challenges:

- Missed vulnerabilities
- Limited framework coverage
- Difficulty adapting to custom applications

SAARTHI introduces:

```text
Repository
      │
      ▼

Context Builder

      │
      ▼

Custom API Discovery

      │
      ▼

AI Confidence Scoring

      │
      ▼

Human Validation

      │
      ▼

Security Knowledge Base

      │
      ▼

Custom Scanner Rules

      │
      ▼

Security Assessment
```

---

## Important Security Principle

AI-generated rules are never automatically trusted.

Every generated rule must pass:

1. AI Confidence Scoring
2. Human Security Review
3. Approval Workflow

before becoming active.

This ensures:

- Auditability
- Traceability
- Security compliance

---

# Security Knowledge Base

SAARTHI maintains a continuously evolving local knowledge base.

Stores:

- Validated custom APIs
- Internal security patterns
- Custom rules
- Historical assessments
- Attack paths
- Approved exceptions

All knowledge remains local to the deployment environment.

---

# Security Tooling

Current and planned integrations include:

### Static Analysis

- CodeQL
- Semgrep

### Software Composition Analysis

- OWASP Dependency-Check
- Trivy
- Grype

### Dynamic Analysis

- OWASP ZAP

### Custom Analysis

- Organization-specific rules
- AI-assisted rule generation
- Knowledge-base-driven checks

---

# AI Models

## Primary Model

### Qwen2.5-Coder-32B

Selected for:

- Strong code understanding
- Excellent reasoning
- Open-weight availability
- Offline deployment support

---

## Optional Secondary Model

### DeepSeek-Coder-V2

Used for:

- Complex repositories
- Deep architectural reasoning
- Advanced vulnerability analysis

---

# Reporting

SAARTHI generates multiple report types.

---

## Executive Report

Audience:

- Leadership
- Program Managers
- Risk Officers

Includes:

- Risk summary
- Business impact
- Critical findings
- Compliance posture

---

## Technical Report

Audience:

- Developers
- Security Engineers

Includes:

- Vulnerability details
- CWE mappings
- OWASP mappings
- Remediation guidance
- Data-flow explanations

---

## Attack Path Report

Audience:

- Security Architects
- Red Teams

Includes:

- Chained vulnerabilities
- Trust boundary violations
- Lateral movement opportunities
- Exploitation paths

---

# Repository Structure

```text
saarthi/
│
├── agents/
├── orchestrator/
├── context-builder/
├── scanners/
├── knowledge-base/
├── reporting/
├── integrations/
├── docs/
│
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

---

# Security Philosophy

SAARTHI does not seek to replace security engineers.

It seeks to amplify them.

The objective is not autonomous security.

The objective is **explainable, auditable, AI-assisted software assurance** that can operate within highly secure and air-gapped environments while preserving human authority over security decisions.

---

# License

MIT License

---

# Motto

> "Context before conclusions. Evidence before assumptions. Humans before automation."
