# Runtime Intelligence

Saarthi has evolved from a scanner-driven tool to a **Runtime-Aware AI Security Analyst**. This document explains the architecture and implementation of the Runtime Intelligence layer.

## Overview

Traditional security scanners often operate in a vacuum, unaware of the actual traffic and state of the application. Saarthi's Runtime Intelligence layer uses `mitmproxy` to observe application traffic during discovery and scanning phases, providing "ground truth" evidence to the AI reasoning engine.

## Architecture

```
URL
↓
Runtime Observer (mitmproxy)
↓
Runtime Evidence (reports/runtime_observations.json)
↓
Security Knowledge Graph (reports/security_graph.json)
↓
ZAP Findings (Correlation)
↓
Attack Chains (AttackPathAgent)
↓
Security Reasoning (SecurityReasoningAgent)
↓
Professional Report (final_security_assessment.md)
```

## Key Components

### 1. Runtime Observer Agent (`agents/runtime_observer_agent.py`)
This agent manages the lifecycle of `mitmdump`. It starts a proxy server before the discovery phase and stops it after the dynamic scanning (DAST) phase.

### 2. MITM Logger (`agents/mitm_logger.py`)
A custom `mitmproxy` addon that captures granular details of every HTTP transaction:
- **URL & Method**
- **Status Code**
- **Headers** (Request & Response)
- **Cookies**
- **Form Data**
- **Query Parameters**
- **Response Metadata** (Content-Type, Length)

### 3. Deep Discovery (`agents/discovery_agent.py`)
The discovery agent has been enhanced to use the runtime observer. It now specifically targets:
- `robots.txt` & `sitemap.xml`
- Swagger/OpenAPI specifications (`/swagger.json`, `/openapi.json`, etc.)
- JavaScript endpoint extraction using improved regex.

All discovery requests are routed through the proxy, ensuring they are logged as runtime evidence.

### 4. Extended Knowledge Graph
The `SecurityKnowledgeGraphAgent` now incorporates runtime observations as first-class nodes:
- `Request` & `Response`
- `Cookie`
- `Session`
- `Form`
- `Header`

These nodes are linked to `Endpoints` and `Findings`, allowing the AI to reason about how a vulnerability might be reached or what session state is required for exploitation.

## Benefits

- **Authenticity:** Findings are backed by actual observed traffic.
- **Context:** The AI understands the application's state (e.g., active sessions, auth headers).
- **Reduced False Positives:** Runtime evidence helps confirm if an endpoint is reachable and how it behaves.
- **Deeper Reasoning:** Attack chains can now include specific steps like "Submit login form" -> "Receive session cookie" -> "Access protected endpoint".
