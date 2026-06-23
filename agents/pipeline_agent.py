import subprocess


PIPELINE_STEPS = [

    "parsers/merge_findings.py",

    "parsers/severity_normalizer.py",

    "parsers/finding_mapper.py",

    "parsers/attack_surface_mapper.py",

    "parsers/context_pack_builder.py",

    "parsers/graph_linker_v2.py",

    "parsers/reachability_engine.py",

    "parsers/final_prioritizer.py"
]


def run(state):

    print(
        "\n[PipelineAgent] Running pipeline\n"
    )

    for script in PIPELINE_STEPS:

        print(
            f"[PipelineAgent] Executing {script}"
        )

        result = subprocess.run(
            [
                "python3",
                script
            ]
        )

        if result.returncode != 0:

            raise RuntimeError(
                f"Pipeline failed at {script}"
            )

    print(
        "\n[PipelineAgent] Pipeline completed"
    )

    state[
        "pipeline_complete"
    ] = True

    # Load the prioritized findings into state
    import json
    import os
    PRIORITIZED_FINDINGS_FILE = "reports/final_prioritized_findings.json"
    if os.path.exists(PRIORITIZED_FINDINGS_FILE):
        try:
            with open(PRIORITIZED_FINDINGS_FILE, "r") as f:
                findings = json.load(f)
                state["findings"] = findings
                print(f"[PipelineAgent] Loaded {len(findings)} findings into state")

                # Now run the CorrelationAgent logic if findings exist
                from agents.correlation_agent import run as correlation_agent
                state = correlation_agent(state)
        except Exception as e:
            print(f"[PipelineAgent] Error loading findings: {e}")
    else:
        print(f"[PipelineAgent] {PRIORITIZED_FINDINGS_FILE} not found. No findings to load.")

    return state