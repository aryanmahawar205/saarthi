# Java Runtime Instrumentation Provider

The Java adapter captures runtime behavior from Java applications without requiring any code changes, operating as a passive `-javaagent`.

## Building the Agent

From the `runtime_agent/adapters/java/agent` directory, run:

```bash
mvn clean package
```

This will produce `target/saarthi-java-agent-1.0-SNAPSHOT.jar` and the shaded fat JAR `target/saarthi-java-agent-1.0-SNAPSHOT-shaded.jar`.

## Execution Environments

You can configure the event reporting endpoint via the `endpoint` argument. If omitted, it defaults to `http://localhost:8081/events`.

### Bare-Metal JVM

For standard execution where both the app and the Saarthi orchestration platform are running on the same host:

```bash
java -javaagent:saarthi-java-agent-1.0-SNAPSHOT.jar=endpoint=http://localhost:8081/events -Xbootclasspath/a:saarthi-java-agent-1.0-SNAPSHOT.jar -jar your-application.jar
```

### Docker

When the Java application is inside a Docker container, but Saarthi is running on the host machine:

```bash
docker run \
  -v $(pwd)/saarthi-java-agent-1.0-SNAPSHOT.jar:/agent.jar \
  -e JAVA_TOOL_OPTIONS="-javaagent:/agent.jar=endpoint=http://host.docker.internal:8081/events -Xbootclasspath/a:/agent.jar" \
  your-image-name
```

*Note: Ensure `host.docker.internal` is resolving properly, depending on your Docker environment.*

### Docker Compose

In a compose setup where the application and Saarthi are running in different containers, use Saarthi's service name as the host:

```yaml
services:
  saarthi:
    image: saarthi
    ports:
      - "8081:8081"

  my-app:
    image: my-app
    volumes:
      - ./saarthi-java-agent-1.0-SNAPSHOT.jar:/agent.jar
    environment:
      - JAVA_TOOL_OPTIONS=-javaagent:/agent.jar=endpoint=http://saarthi:8081/events -Xbootclasspath/a:/agent.jar
```

### GitHub Codespaces

In GitHub Codespaces, `localhost` generally works between forwarded ports:

```bash
java -javaagent:saarthi-java-agent-1.0-SNAPSHOT.jar=endpoint=http://localhost:8081/events -Xbootclasspath/a:saarthi-java-agent-1.0-SNAPSHOT.jar -jar your-application.jar
```

### Kubernetes

In Kubernetes, inject the agent using an init container, and target the Saarthi service:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    spec:
      initContainers:
        - name: agent-init
          image: my-agent-image
          command: ["cp", "/saarthi-java-agent-1.0-SNAPSHOT.jar", "/shared/agent.jar"]
          volumeMounts:
            - name: agent-volume
              mountPath: /shared
      containers:
        - name: my-app
          image: my-app-image
          env:
            - name: JAVA_TOOL_OPTIONS
              value: "-javaagent:/shared/agent.jar=endpoint=http://saarthi-service.default.svc.cluster.local:8081/events -Xbootclasspath/a:/shared/agent.jar"
          volumeMounts:
            - name: agent-volume
              mountPath: /shared
      volumes:
        - name: agent-volume
          emptyDir: {}
```
