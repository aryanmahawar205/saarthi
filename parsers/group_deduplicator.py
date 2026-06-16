import json

INPUT_FILE = "reports/correlated_findings.json"
OUTPUT_FILE = "reports/deduplicated_groups.json"


def jaccard_similarity(a, b):

    a = set(a)
    b = set(b)

    if not a or not b:
        return 0

    return len(a & b) / len(a | b)


def choose_primary_group(groups):

    priority = {
        "CWE": 3,
        "VULNERABILITY_CLASS": 2,
        "PACKAGE": 1
    }

    return max(
        groups,
        key=lambda g: (
            priority.get(
                g["group_type"],
                0
            ),
            g["finding_count"]
        )
    )


def main():

    with open(INPUT_FILE, "r") as f:
        groups = json.load(f)

    visited = set()

    final_groups = []

    for i, group in enumerate(groups):

        if i in visited:
            continue

        cluster = [group]

        visited.add(i)

        for j, other in enumerate(groups):

            if j in visited:
                continue

            similarity = jaccard_similarity(
                group["findings"],
                other["findings"]
            )

            if similarity >= 0.90:

                cluster.append(other)
                visited.add(j)

        primary = choose_primary_group(
            cluster
        )

        primary["merged_groups"] = [
            {
                "group_id": g["group_id"],
                "group_type": g["group_type"],
                "group_key": g["group_key"]
            }
            for g in cluster
        ]

        final_groups.append(primary)

    with open(OUTPUT_FILE, "w") as f:

        json.dump(
            final_groups,
            f,
            indent=2
        )

    print(
        f"[+] Reduced {len(groups)} groups -> {len(final_groups)} groups"
    )

    print(
        f"[+] Saved to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()