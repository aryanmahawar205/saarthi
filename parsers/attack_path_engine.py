'''
TODO (Phase 2)

Current attack path discovery is rule-based.

This works for MVP because attack chains are defined
using common CWE combinations:

- Secrets -> RCE
- Upload -> RCE
- SSRF -> Internal Access
- SQL Injection -> DB Compromise
- Deserialization -> RCE

Future upgrade:

CWE
  -> ATT&CK Technique
  -> ATT&CK Tactic
  -> Attack Graph

Example:

CWE-78
  -> T1059 Command Execution

CWE-918
  -> T1190 Exploit Public Facing App

Then dynamically generate attack paths from
technique relationships rather than hardcoded chains.

This will allow Saarthi to work across arbitrary
codebases and technologies.
'''

import json

INPUT_FILE = "reports/prioritized_risks.json"
OUTPUT_FILE = "reports/attack_paths.json"

ATTACK_CHAINS = [

    {
        "name": "Secrets → RCE",

        "requires": [
            "Secret Exposure",
            "CWE-321",
            "CWE-78"
        ],

        "impact": "Remote Code Execution"
    },

    {
        "name": "SQL Injection",

        "requires": [
            "SQL Injection"
        ],

        "impact": "Database Compromise"
    },

    {
        "name": "Upload → RCE",

        "requires": [
            "CWE-434",
            "CWE-78"
        ],

        "impact": "Remote Code Execution"
    },

    {
        "name": "SSRF → Internal Access",

        "requires": [
            "CWE-918"
        ],

        "impact": "Internal Network Access"
    },

    {
        "name": "Deserialization → RCE",

        "requires": [
            "CWE-502",
            "CWE-94"
        ],

        "impact": "Remote Code Execution"
    }
]


def chain_exists(chain, present):

    for requirement in chain["requires"]:

        found = False

        for key in present:

            if requirement in key:
                found = True
                break

        if not found:
            return False

    return True


def main():

    with open(INPUT_FILE) as f:

        groups = json.load(f)

    present = set()

    for group in groups:

        present.add(
            group["group_key"]
        )

    paths = []

    for chain in ATTACK_CHAINS:

        if chain_exists(
            chain,
            present
        ):

            paths.append({

                "name":
                    chain["name"],

                "impact":
                    chain["impact"],

                "components":
                    chain["requires"]

            })

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            paths,
            f,
            indent=2
        )

    print(
        f"[+] Found {len(paths)} attack paths"
    )

    print(
        f"[+] Saved to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()