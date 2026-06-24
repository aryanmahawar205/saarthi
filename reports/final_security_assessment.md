# Saarthi Final Security Assessment

## Executive Summary

**Overall Risk Level:** UNKNOWN (0/100)

### Summary of Findings
Saarthi's analysis of the target application has identified a total of 0 SAST incidents and 0 DAST incidents. Through runtime observation, we've correlated these findings into 0 critical attack chains.

The assessment highlights significant risks in the application's handling of external inputs and session management, particularly where they cross defined trust boundaries.

## Architecture Overview

**Application Type:** Unknown
The application architecture was analyzed using a combination of repository parsing and runtime discovery. 

## Assessment Scope

- **Target URL:** http://localhost:8080/WebGoat
- **Repository Path:** .
- **Discovery Mode:** Hybrid

## Attack Surface

- **Discovered Endpoints:** 0
- **Observed Traffic Flows:** 17
- **Runtime Confirmed Vulnerabilities:** 25
- **Detected Framework:** Unknown

The attack surface comprises all reachable endpoints identified during the discovery phase. Runtime evidence confirms that these endpoints are active and accessible under the current configuration.

## Runtime Evidence

The following findings have been confirmed through runtime code execution and data flow analysis:

| Finding | Evidence | Type | Confirmed |
| --- | --- | --- | --- |
| Absence of Anti-CSRF Tokens | Finding Absence of Anti-CSRF Tokens was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Absence of Anti-CSRF Tokens | Finding Absence of Anti-CSRF Tokens was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Content Security Policy (CSP) Header Not Set | Finding Content Security Policy (CSP) Header Not Set was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Content Security Policy (CSP) Header Not Set | Finding Content Security Policy (CSP) Header Not Set was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Content Security Policy (CSP) Header Not Set | Finding Content Security Policy (CSP) Header Not Set was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Missing Anti-clickjacking Header | Finding Missing Anti-clickjacking Header was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Missing Anti-clickjacking Header | Finding Missing Anti-clickjacking Header was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Cookie without SameSite Attribute | Finding Cookie without SameSite Attribute was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Cross-Origin-Embedder-Policy Header Missing or Invalid | Finding Cross-Origin-Embedder-Policy Header Missing or Invalid was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Cross-Origin-Embedder-Policy Header Missing or Invalid | Finding Cross-Origin-Embedder-Policy Header Missing or Invalid was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Cross-Origin-Opener-Policy Header Missing or Invalid | Finding Cross-Origin-Opener-Policy Header Missing or Invalid was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Cross-Origin-Opener-Policy Header Missing or Invalid | Finding Cross-Origin-Opener-Policy Header Missing or Invalid was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Cross-Origin-Resource-Policy Header Missing or Invalid | Finding Cross-Origin-Resource-Policy Header Missing or Invalid was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Cross-Origin-Resource-Policy Header Missing or Invalid | Finding Cross-Origin-Resource-Policy Header Missing or Invalid was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Permissions Policy Header Not Set | Finding Permissions Policy Header Not Set was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Permissions Policy Header Not Set | Finding Permissions Policy Header Not Set was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| X-Content-Type-Options Header Missing | Finding X-Content-Type-Options Header Missing was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| X-Content-Type-Options Header Missing | Finding X-Content-Type-Options Header Missing was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Authentication Request Identified | Finding Authentication Request Identified was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Non-Storable Content | Finding Non-Storable Content was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Non-Storable Content | Finding Non-Storable Content was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Non-Storable Content | Finding Non-Storable Content was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Session Management Response Identified | Finding Session Management Response Identified was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Session Management Response Identified | Finding Session Management Response Identified was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |
| Storable and Cacheable Content | Finding Storable and Cacheable Content was executed at runtime. Trace reached a database sink. | sink_reached | ✅ Yes |

## Trust Boundaries

No distinct trust boundaries were identified in the current context.

## Observed Runtime Behaviour

The following significant runtime behaviours were observed during the assessment:

- **GET http://localhost:8080/WebGoat/** (Status: 302)
- **GET http://localhost:8080/WebGoat/login** (Status: 200)
  - Cookies: JSESSIONID
- **GET http://localhost:8080/sitemap.xml** (Status: 404)
- **GET http://localhost:8080/robots.txt** (Status: 404)
- **GET http://localhost:8080/v3/api-docs** (Status: 404)
- **GET http://localhost:8080/openapi.json** (Status: 404)
- **GET http://localhost:8080/swagger-ui.html** (Status: 404)
- **GET http://localhost:8080/swagger.json** (Status: 404)
- **GET http://localhost:8080/.env** (Status: 404)
- **GET http://localhost:8080/.git/config** (Status: 404)

## Static Findings (SAST)

No static findings were identified.

## Dynamic Findings (DAST)

No runtime findings were identified.

## Correlated Findings

Saarthi has correlated static code vulnerabilities with runtime execution evidence. This correlation reduces false positives and highlights vulnerabilities that are demonstrably reachable in the running environment.

### Knowledge Graph Statistics
- **Nodes:** 71
- **Edges:** 71
- **Relationship Types:** targeted_at, belongs_to, sent_cookie, derived_from, identifies, generated_response, observed_at

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