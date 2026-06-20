import json


INPUT_FILE = "scans/zap.json"


def severity(riskcode):

    mapping = {

        "3": "HIGH",
        "2": "MEDIUM",
        "1": "LOW",
        "0": "INFO"
    }

    return mapping.get(
        str(riskcode),
        "INFO"
    )


def run(state):

    with open(INPUT_FILE) as f:

        zap = json.load(f)

    findings = []

    sites = zap.get(
        "site",
        []
    )

    for site in sites:

        alerts = site.get(
            "alerts",
            []
        )

        for alert in alerts:

            findings.append({

                "tool":
                    "ZAP",

                "title":
                    alert.get(
                        "alert",
                        ""
                    ),

                "severity":
                    severity(
                        alert.get(
                            "riskcode",
                            "0"
                        )
                    ),

                "description":
                    alert.get(
                        "desc",
                        ""
                    ),

                "solution":
                    alert.get(
                        "solution",
                        ""
                    ),

                "reference":
                    alert.get(
                        "reference",
                        ""
                    ),

                "instances":
                    len(
                        alert.get(
                            "instances",
                            []
                        )
                    )
            })

    state[
        "dast_findings"
    ] = findings

    print(
        f"[ZapParserAgent] "
        f"{len(findings)} findings"
    )

    return state


if __name__ == "__main__":

    state = {}

    run(state)