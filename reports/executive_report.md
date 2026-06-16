# Saarthi Security Assessment

## Executive Summary

- Critical Risks: 2
- High Risks: 6
- Attack Paths Identified: 5

## Top Risks

### CWE-78
- Priority: CRITICAL
- Score: 134
- Findings: 4

Evidence:

- XStream: remote code execution due to insecure XML deserialization
  File: pom.xml

- XStream: remote code execution due to insecure XML deserialization when relying on blocklists
  File: pom.xml

- XStream: arbitrary file deletion on the local host when unmarshalling
  File: pom.xml


### CWE-502
- Priority: CRITICAL
- Score: 120
- Findings: 28

Evidence:

- XStream: allow a remote attacker to cause DoS only by manipulating the processed input stream
  File: pom.xml

- XStream: remote command execution attack by manipulating the processed input stream
  File: pom.xml

- xstream: Arbitrary code execution via unsafe deserialization of Xalan xsltc.trax.TemplatesImpl
  File: pom.xml


### CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')
- Priority: HIGH
- Score: 118
- Findings: 18

Evidence:

- java.spring.security.injection.tainted-sql-string.tainted-sql-string
  File: src/main/java/org/owasp/webgoat/lessons/challenges/challenge5/Assignment5.java

- java.lang.security.audit.formatted-sql-string.formatted-sql-string
  File: src/main/java/org/owasp/webgoat/lessons/challenges/challenge5/Assignment5.java

- java.spring.security.injection.tainted-sql-string.tainted-sql-string
  File: src/main/java/org/owasp/webgoat/lessons/sqlinjection/advanced/SqlInjectionChallenge.java


### CWE-321: Use of Hard-coded Cryptographic Key
- Priority: HIGH
- Score: 108
- Findings: 13

Evidence:

- generic.secrets.security.detected-jwt-token.detected-jwt-token
  File: src/it/java/org/owasp/webgoat/playwright/webwolf/JwtUITest.java

- generic.secrets.security.detected-jwt-token.detected-jwt-token
  File: src/main/resources/lessons/jwt/documentation/JWT_decode.adoc

- generic.secrets.security.detected-jwt-token.detected-jwt-token
  File: src/main/resources/lessons/jwt/documentation/JWT_libraries.adoc


### CWE-94
- Priority: HIGH
- Score: 108
- Findings: 3

Evidence:

- XStream: remote command execution attack by manipulating the processed input stream
  File: pom.xml

- xstream: Arbitrary code execution via unsafe deserialization of sun.tracing.*
  File: pom.xml

- XStream: Unsafe deserizaliation of com.sun.corba.se.impl.activation.ServerTableEntry
  File: pom.xml


### CWE-434
- Priority: HIGH
- Score: 105
- Findings: 15

Evidence:

- xstream: Arbitrary code execution via unsafe deserialization of Xalan xsltc.trax.TemplatesImpl
  File: pom.xml

- xstream: Arbitrary code execution via unsafe deserialization of com.sun.xml.internal.ws.client.sei.*
  File: pom.xml

- xstream: Arbitrary code execution via unsafe deserialization of com.sun.jndi.ldap.LdapBindingEnumeration
  File: pom.xml


### CWE-1336
- Priority: HIGH
- Score: 103
- Findings: 3

Evidence:

- thymeleaf: Thymeleaf: Server-Side Template Injection via security bypass in expression execution
  File: pom.xml

- thymeleaf: Thymeleaf: Server-Side Template Injection via expression execution bypass
  File: pom.xml

- Sandboxed Thymeleaf expressions vulnerable to improper recognition of unauthorized syntax patterns
  File: pom.xml


### CWE-918
- Priority: HIGH
- Score: 100
- Findings: 5

Evidence:

- xstream: Server-side request forgery (SSRF) via unsafe deserialization of com.sun.xml.internal.ws.client.sei.*
  File: pom.xml

- xstream: Server-side request forgery (SSRF) via unsafe deserialization of jdk.nashorn.internal.runtime.Source$URLData
  File: pom.xml

- XStream: Server-Side Forgery Request vulnerability can be activated when unmarshalling
  File: pom.xml


### Cryptographic Issues
- Priority: MEDIUM
- Score: 85
- Findings: 23

Evidence:

- html.security.audit.missing-integrity.missing-integrity
  File: docs/index.html

- generic.secrets.security.detected-jwt-token.detected-jwt-token
  File: src/it/java/org/owasp/webgoat/playwright/webwolf/JwtUITest.java

- java.lang.security.audit.crypto.weak-random.weak-random
  File: src/main/java/org/owasp/webgoat/lessons/challenges/challenge1/ImageServlet.java


### Secret Exposure
- Priority: MEDIUM
- Score: 85
- Findings: 95

Evidence:

- generic-api-key
  File: src/main/java/org/owasp/webgoat/lessons/securitymisconfiguration/ActuatorExposureTask.java

- jwt
  File: src/it/java/org/owasp/webgoat/playwright/webwolf/JwtUITest.java

- jwt
  File: robot/goat.robot


## Attack Paths

### Secrets → RCE
Impact: Remote Code Execution

Chain:
- Secret Exposure
- CWE-321
- CWE-78

### SQL Injection
Impact: Database Compromise

Chain:
- SQL Injection

### Upload → RCE
Impact: Remote Code Execution

Chain:
- CWE-434
- CWE-78

### SSRF → Internal Access
Impact: Internal Network Access

Chain:
- CWE-918

### Deserialization → RCE
Impact: Remote Code Execution

Chain:
- CWE-502
- CWE-94

