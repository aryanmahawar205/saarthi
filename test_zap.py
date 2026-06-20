from agents.zap_agent import run

state = {

    "target_url":
        "http://localhost:8080/WebGoat/",

    "project_root":
        "/workspaces/saarthi"
}

run(state)

# java -jar target/webgoat-2026.2-SNAPSHOT.jar