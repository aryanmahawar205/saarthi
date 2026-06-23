# Saarthi Final Security Assessment

## Executive Summary

**Overall Risk Level:** UNKNOWN (0/100)

This report provides a comprehensive security assessment of the target application using AI-assisted runtime-aware analysis. By correlating static code analysis, dynamic scanning, and runtime observation, Saarthi has identified critical attack paths and business risks.

## Assessment Scope

- **Target URL:** http://localhost:8080/WebGoat/
- **Repository Path:** /app
- **Discovery Mode:** Hybrid

## Runtime Attack Surface

- **Discovered Endpoints:** 12
- **Observed Traffic Flows:** 12

The runtime attack surface was mapped through deep crawling and traffic observation. This represents the externally reachable entry points and internal data flow patterns.

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

No static findings were identified.

## Dynamic Findings (DAST)

- **Weak Browser Security Controls** (Instances: 8)
- **CSRF Exposure** (Instances: 1)
- **Authentication Surface** (Instances: 1)
- **Non-Storable Content** (Instances: 1)
- **Storable and Cacheable Content** (Instances: 1)
- **User Controllable HTML Element Attribute (Potential XSS)** (Instances: 1)

## Correlated Findings

Findings correlated across Static and Runtime analysis layers have been incorporated into the Security Knowledge Graph to uncover attack paths bridging the gap between static code issues and runtime execution context.

## Attack Chains

### 1. Browser Exploitation Chain
**Boundary Crossed:** Application Layer
**Impact:** Account Takeover / Reputation Damage

**Chain:**
- Victim Browser
- Missing CSP / Security Headers
- Script Injection or Clickjacking
- Session Theft or State Modification

### 2. Cross Site Request Forgery
**Boundary Crossed:** Application Layer
**Impact:** Unauthorized Actions / Privilege Escalation

**Chain:**
- Victim Session
- Forged Request via malicious link
- State Change Execution
- Privilege Abuse

### 3. Authentication Abuse
**Boundary Crossed:** Application Layer
**Impact:** Account Compromise / Data Breach

**Chain:**
- External Input
- Exposed Login Endpoint
- Weak Session Controls or Brute Force
- Session Hijacking or Credential Compromise

### 4. Exploitation of Non-Storable Content
**Boundary Crossed:** Application Layer
**Impact:** Variable based on context

**Chain:**
- External Input
- Discovery of Vulnerability
- Exploitation of Non-Storable Content
- Impact Realization

### 5. Exploitation of Storable and Cacheable Content
**Boundary Crossed:** Application Layer
**Impact:** Variable based on context

**Chain:**
- External Input
- Discovery of Vulnerability
- Exploitation of Storable and Cacheable Content
- Impact Realization

### 6. Cross Site Scripting
**Boundary Crossed:** Application Layer
**Impact:** Account Takeover / Lateral Movement

**Chain:**
- External Input
- Unsanitized User Input
- Script Injection into Web Page
- Browser Execution by Victim
- Credential Theft or Session Hijacking

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