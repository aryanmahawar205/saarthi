def run(state):

    findings = state.get(
        "dast_findings",
        []
    )

    browser_security = []

    csrf = []

    auth = []

    others = []

    for finding in findings:

        title = finding[
            "title"
        ].lower()

        if any(

            keyword in title

            for keyword in [

                "content security",
                "clickjacking",
                "samesite",
                "permissions policy",
                "cross-origin",
                "x-content"
            ]
        ):

            browser_security.append(
                finding
            )

        elif "csrf" in title:

            csrf.append(
                finding
            )

        elif any(

            keyword in title

            for keyword in [

                "authentication",
                "session"
            ]
        ):

            auth.append(
                finding
            )

        else:

            others.append(
                finding
            )

    incidents = []

    if browser_security:

        incidents.append({

            "incident":

                "Weak Browser Security Controls",

            "findings":

                browser_security
        })

    if csrf:

        incidents.append({

            "incident":

                "CSRF Exposure",

            "findings":

                csrf
        })

    if auth:

        incidents.append({

            "incident":

                "Authentication Surface",

            "findings":

                auth
        })

    for finding in others:

        incidents.append({

            "incident":
                finding["title"],

            "findings":
                [finding]
        })

    state[
        "dast_incidents"
    ] = incidents

    print(
        f"[DASTCorrelationAgent] "
        f"{len(incidents)} incidents"
    )

    return state