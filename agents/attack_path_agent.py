def run(state):
    knowledge_graph = state.get("security_knowledge_graph", {})

    dast_incidents = knowledge_graph.get("dast_incidents", [])

    # We will build realistic attack paths based on the incidents in the knowledge graph.
    attack_paths = []

    for incident in dast_incidents:
        name = incident.get("incident", "")

        if name == "Weak Browser Security Controls":
            attack_paths.append({
                "name": "Browser Exploitation Chain",
                "path": [
                    "Victim Browser",
                    "Missing CSP / Security Headers",
                    "Script Injection or Clickjacking",
                    "Session Theft or State Modification"
                ],
                "impact": "Account Takeover / Reputation Damage"
            })
        elif name == "CSRF Exposure":
            attack_paths.append({
                "name": "Cross Site Request Forgery",
                "path": [
                    "Victim Session",
                    "Forged Request via malicious link",
                    "State Change Execution",
                    "Privilege Abuse"
                ],
                "impact": "Unauthorized Actions / Privilege Escalation"
            })
        elif name == "Authentication Surface":
            attack_paths.append({
                "name": "Authentication Abuse",
                "path": [
                    "Exposed Login Endpoint",
                    "Weak Session Controls or Brute Force",
                    "Session Hijacking or Credential Compromise"
                ],
                "impact": "Account Compromise / Data Breach"
            })
        elif "xss" in name.lower():
            attack_paths.append({
                "name": "Cross Site Scripting",
                "path": [
                    "Unsanitized User Input",
                    "Script Injection into Web Page",
                    "Browser Execution by Victim",
                    "Credential Theft or Session Hijacking"
                ],
                "impact": "Account Takeover / Lateral Movement"
            })
        else:
            # Generic path generation for other incidents
            attack_paths.append({
                "name": f"Exploitation of {name}",
                "path": [
                    "Discovery of Vulnerability",
                    f"Exploitation of {name}",
                    "Impact Realization"
                ],
                "impact": "Variable based on context"
            })

    state["attack_paths"] = attack_paths

    print(f"[AttackPathAgent] Generated {len(attack_paths)} attack paths derived from the knowledge graph.")

    return state
