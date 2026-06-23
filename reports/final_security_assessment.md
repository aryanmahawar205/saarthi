# Saarthi Final Security Assessment

## Executive Summary

**Overall Risk Level:** UNKNOWN (0/100)

### Summary of Findings
Saarthi's analysis of the target application has identified a total of 1 SAST incidents and 0 DAST incidents. Through runtime observation, we've correlated these findings into 0 critical attack chains.

The assessment highlights significant risks in the application's handling of external inputs and session management, particularly where they cross defined trust boundaries.

## Architecture Overview

**Application Type:** Unknown
The application architecture was analyzed using a combination of repository parsing and runtime discovery.

## Assessment Scope

- **Target URL:** http://localhost:8080/WebGoat/
- **Repository Path:** .
- **Discovery Mode:** Hybrid

## Attack Surface

- **Discovered Endpoints:** 12
- **Observed Traffic Flows:** 12
- **Detected Framework:** Unknown

The attack surface comprises all reachable endpoints identified during the discovery phase. Runtime evidence confirms that these endpoints are active and accessible under the current configuration.

## Trust Boundaries

- **External Input**: Internet -> Web Application

## Observed Runtime Behaviour

The following significant runtime behaviours were observed during the assessment:

- **GET http://localhost:8080/WebGoat/** (Status: 502)
- **GET http://localhost:8080/sitemap.xml** (Status: 502)
- **GET http://localhost:8080/robots.txt** (Status: 502)
- **GET http://localhost:8080/v3/api-docs** (Status: 502)
- **GET http://localhost:8080/openapi.json** (Status: 502)
- **GET http://localhost:8080/swagger-ui.html** (Status: 502)
- **GET http://localhost:8080/swagger.json** (Status: 502)
- **GET http://localhost:8080/.env** (Status: 502)
- **GET http://localhost:8080/.git/config** (Status: 502)
- **GET http://localhost:8080/actuator** (Status: 502)

## Static Findings (SAST)

### Dummy Incident


## Dynamic Findings (DAST)

No runtime findings were identified.

## Correlated Findings

Saarthi has correlated static code vulnerabilities with runtime execution evidence. This correlation reduces false positives and highlights vulnerabilities that are demonstrably reachable in the running environment.

### Knowledge Graph Statistics
- **Nodes:** 38
- **Edges:** 36
- **Relationship Types:** generated_response, observed_at, targeted_at

## Attack Chains

No definitive attack chains were derived.

## AI-Assisted Reasoning

### Most Likely Attack
Failed to determine.

### Most Dangerous Attack
Failed to determine.

### Exploitability Assessment
Failed to assess.

### Business Impact
Failed to generate business impact.

## Risk Assessment

**Priority:** Unknown

### Top Risks

No prioritized risks were provided.

## Remediation Roadmap

No remediation steps were provided.

## Executive Recommendations

It is highly recommended that the engineering teams prioritize the Top Risks identified in this report. The integration of runtime evidence proves that these vulnerabilities are not just theoretical but reachable in the application's current deployment. Following the Remediation Roadmap will systematically address the underlying structural vulnerabilities, reducing the overall risk exposure.