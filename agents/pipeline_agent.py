import subprocess


PIPELINE_STEPS = [

    "parsers/zap_parser.py",

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

    return state