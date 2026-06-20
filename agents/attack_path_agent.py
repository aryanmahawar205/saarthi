def run(state):

    incidents = state.get(
        "dast_incidents",
        []
    )

    attack_paths = []

    for incident in incidents:

        name = incident[
            "incident"
        ]

        if name == \
            "Weak Browser Security Controls":

            attack_paths.append({

                "name":
                    "Browser Exploitation Chain",

                "path": [

                    "Victim Browser",

                    "Missing CSP",

                    "Script Injection",

                    "Session Theft"
                ],

                "impact":
                    "Account Takeover"
            })

        elif name == \
            "CSRF Exposure":

            attack_paths.append({

                "name":
                    "Cross Site Request Forgery",

                "path": [

                    "Victim Session",

                    "Forged Request",

                    "State Change",

                    "Privilege Abuse"
                ],

                "impact":
                    "Unauthorized Actions"
            })

        elif name == \
            "Authentication Surface":

            attack_paths.append({

                "name":
                    "Authentication Abuse",

                "path": [

                    "Login Endpoint",

                    "Weak Session Controls",

                    "Session Hijacking"
                ],

                "impact":
                    "Account Compromise"
            })

        elif "xss" in \
            name.lower():

            attack_paths.append({

                "name":
                    "Cross Site Scripting",

                "path": [

                    "User Input",

                    "Script Injection",

                    "Browser Execution",

                    "Credential Theft"
                ],

                "impact":
                    "Account Takeover"
            })

    state[
        "attack_paths"
    ] = attack_paths

    print(

        f"[AttackPathAgent] "

        f"{len(attack_paths)} attack paths"
    )

    return state