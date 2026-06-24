# Runtime Intelligence

Saarthi has evolved from a scanner-driven tool to a **Runtime-Aware AI Security Analyst**. This document explains the architecture and implementation of the Runtime Intelligence layer.

## Overview

Traditional security scanners often operate in a vacuum, unaware of the actual traffic and internal state of the application. Saarthi's Runtime Intelligence layer provides code-level visibility and execution evidence to the AI reasoning engine.

It is designed with an **abstraction-first** approach, ensuring that Saarthi can ingest runtime data from multiple sources without being tied to a specific technology.

## Architecture

The Runtime Intelligence layer consists of:

1.  **Collectors & Adapters**: Pluggable components that ingest data from various sources (OpenTelemetry, Language-specific agents, eBPF) and normalize them into `RuntimeEvent` objects.
2.  **Normalized Models**: Provider-agnostic models (`RuntimeEvent`, `RuntimeTrace`, `RuntimeEvidence`).
3.  **Runtime Correlator**: A dedicated engine that bridges SAST/DAST findings with runtime execution evidence.
4.  **Runtime-Aware Knowledge Graph**: An extension of the Security Knowledge Graph that incorporates execution flows and confirmed sinks.
5.  **Runtime-Aware Reasoning**: AI-driven analysis that prioritizes runtime-confirmed attack paths.

```
Runtime Sources (OTel, Java Agent, etc.)
↓
Runtime Adapters
↓
Normalized RuntimeEvents
↓
Runtime Correlator ← (SAST/DAST Findings)
↓
Runtime Evidence
↓
Security Knowledge Graph
↓
Attack Path Agent (Prioritized Paths)
↓
Security Reasoning Agent (Runtime Risk Scoring)
↓
Professional Report
```

## Key Components

### 1. Runtime Models (`runtime/models/`)
Defines the core, provider-agnostic data structures:
- **RuntimeEvent**: A single unit of execution (e.g., function call, HTTP request, DB query).
- **RuntimeTrace**: A collection of related events forming an execution chain.
- **RuntimeEvidence**: A high-level object representing a runtime-confirmed security state (e.g., "Vulnerability X was executed and reached Sink Y").

### 2. Runtime Adapters (`runtime/adapters/`)
Implementations for specific collection technologies.
- **OpenTelemetry Adapter**: Consumes OTel spans and converts them to `RuntimeEvent` objects.
- **Future Adapters**: Java Agent, Python middleware, Node instrumentation, Go, .NET, eBPF.

### 3. Runtime Correlator (`runtime/correlation/`)
The primary engine for matching findings to execution evidence. It answers questions like:
- "Did this specific SAST finding execute at runtime?"
- "Was the sink of this DAST finding reached within the code?"
- "Did this request cross a trust boundary as predicted?"

### 4. Runtime Observer Agent (`agents/runtime_observer_agent.py`)
Continues to provide network-level visibility via `mitmproxy`, augmenting the code-level visibility provided by the Runtime Intelligence layer.

### 5. Extended Knowledge Graph
The `SecurityKnowledgeGraphAgent` incorporates `RuntimeEvidence` and `RuntimeEvent` nodes:
- `RuntimeEndpoint`, `RuntimeFunction`, `RuntimeTrace`, `RuntimeException`, `DatabaseCall`.
- Relationships like `evidences`, `reached_sink`, `crossed_boundary`.

## Orchestration Modes

- **Mode 1**: SAST Only
- **Mode 2**: DAST Only
- **Mode 3**: SAST + DAST
- **Mode 4**: SAST + DAST + Runtime Intelligence (The full Saarthi experience)

## Benefits

- **Authenticity**: Findings are backed by actual observed code execution.
- **Precision**: Drastically reduces false positives by confirming reachability.
- **Deeper Reasoning**: Attack chains trace from external input through internal logic to sensitive sinks.
- **Risk-Based Prioritization**: Runtime-confirmed vulnerabilities are automatically prioritized.

## Benefits

- **Authenticity:** Findings are backed by actual observed traffic.
- **Context:** The AI understands the application's state (e.g., active sessions, auth headers).
- **Reduced False Positives:** Runtime evidence helps confirm if an endpoint is reachable and how it behaves.
- **Deeper Reasoning:** Attack chains can now include specific steps like "Submit login form" -> "Receive session cookie" -> "Access protected endpoint".
