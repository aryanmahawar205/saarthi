import json

CONTEXT_FILE = "reports/repository_context.json"
API_GRAPH_FILE = "reports/api_graph.json"
DEPENDENCY_FILE = "reports/dependency_graph.json"

OUTPUT_FILE = "reports/assessment_plan.json"


DB_KEYWORDS = {
    "jdbc",
    "hibernate",
    "jpa",
    "mysql",
    "postgres",
    "mongodb",
    "datasource",
    "spring-data"
}


AUTH_KEYWORDS = {
    "security",
    "jwt",
    "oauth",
    "authentication",
    "authorization"
}


def load_json(path):

    with open(path) as f:
        return json.load(f)


def detect_application_type(
    context,
    api_graph,
    dependencies
):

    if api_graph:

        for dep in dependencies:

            artifact = dep.get(
                "artifact",
                ""
            ).lower()

            if "spring" in artifact:
                return "Spring Boot"

    source_files = context.get(
        "source_files",
        []
    )

    for file_path in source_files:

        lower = file_path.lower()

        if lower.endswith(".py"):
            return "Python Application"

        if lower.endswith(".js"):
            return "Node.js Application"

        if lower.endswith(".java"):
            return "Java Application"

    return "Unknown"


def contains_database(
    dependencies
):

    for dep in dependencies:

        artifact = dep.get(
            "artifact",
            ""
        ).lower()

        group = dep.get(
            "group",
            ""
        ).lower()

        text = artifact + " " + group

        for keyword in DB_KEYWORDS:

            if keyword in text:
                return True

    return False


def contains_authentication(
    dependencies,
    context
):

    for dep in dependencies:

        artifact = dep.get(
            "artifact",
            ""
        ).lower()

        group = dep.get(
            "group",
            ""
        ).lower()

        text = artifact + " " + group

        for keyword in AUTH_KEYWORDS:

            if keyword in text:
                return True

    for source in context.get(
        "source_files",
        []
    ):

        lower = source.lower()

        for keyword in AUTH_KEYWORDS:

            if keyword in lower:
                return True

    return False


def recommend_scanners(
    contains_api
):

    scanners = [
        "semgrep",
        "trivy"
    ]

    if contains_api:

        scanners.append(
            "zap"
        )

    return scanners


def critical_components(
    contains_api,
    has_database,
    has_auth
):

    components = []

    if contains_api:

        components.append(
            "API Layer"
        )

    if has_database:

        components.append(
            "Database Layer"
        )

    if has_auth:

        components.append(
            "Authentication Layer"
        )

    return components


def reasoning(
    contains_api,
    has_database,
    has_auth,
    dependencies
):

    reasons = []

    if contains_api:

        reasons.append(
            "REST endpoints detected"
        )

    if has_database:

        reasons.append(
            "Database dependencies detected"
        )

    if has_auth:

        reasons.append(
            "Authentication components detected"
        )

    if dependencies:

        reasons.append(
            "Third-party dependencies detected"
        )

    return reasons


def build_assessment_plan():

    context = load_json(
        CONTEXT_FILE
    )

    api_graph = load_json(
        API_GRAPH_FILE
    )

    dependencies = load_json(
        DEPENDENCY_FILE
    )

    contains_api = len(
        api_graph
    ) > 0

    has_database = contains_database(
        dependencies
    )

    has_auth = contains_authentication(
        dependencies,
        context
    )

    plan = {

        "application_type":
            detect_application_type(
                context,
                api_graph,
                dependencies
            ),

        "contains_api":
            contains_api,

        "contains_database":
            has_database,

        "contains_authentication":
            has_auth,

        "contains_dependencies":
            len(dependencies) > 0,

        "recommended_scanners":
            recommend_scanners(
                contains_api
            ),

        "critical_components":
            critical_components(
                contains_api,
                has_database,
                has_auth
            ),

        "reasoning":
            reasoning(
                contains_api,
                has_database,
                has_auth,
                dependencies
            )
    }

    return plan


def run(state):

    plan = build_assessment_plan()

    state[
        "assessment_plan"
    ] = plan

    with open(
        OUTPUT_FILE,
        "w"
    ) as f:

        json.dump(
            plan,
            f,
            indent=2
        )

    print(
        "[PlanningAgent] Assessment plan created"
    )

    return state


def main():

    state = {}

    state = run(state)

    print(
        json.dumps(
            state[
                "assessment_plan"
            ],
            indent=2
        )
    )


if __name__ == "__main__":
    main()