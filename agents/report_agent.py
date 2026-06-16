OUTPUT_FILE = "reports/ai_report.md"


def run(state):

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        f.write(
            "# Saarthi AI Security Assessment\n\n"
        )

        f.write(
            state["analysis"]
        )

    print(
        f"[ReportAgent] Saved {OUTPUT_FILE}"
    )

    return state