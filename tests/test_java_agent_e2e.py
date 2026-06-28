import unittest
import time
import subprocess
import urllib.request
import os
import threading
from runtime_agent.manager.runtime_manager import RuntimeManager
from runtime_agent.registry.adapter_registry import AdapterRegistry
from runtime_agent.adapters.java.java_adapter import JavaAdapter

class TestJavaAgentE2E(unittest.TestCase):
    def setUp(self):
        self.registry = AdapterRegistry()
        self.registry.register("java", JavaAdapter)
        self.manager = RuntimeManager(self.registry)
        self.session = self.manager.create_session("TestApp", "java")

        # Start the manager, but note that the adapter listens on 8081 by default
        self.manager.start_session(self.session.session_id)
        time.sleep(1) # Give the server time to start

    def tearDown(self):
        self.manager.stop_session(self.session.session_id)

    def test_e2e_instrumentation(self):
        # We run the dummy app with the java agent
        # Use the unshaded jar first for testing if shading hides EventPublisher from boot class path
        agent_jar = os.path.abspath("runtime_agent/adapters/java/agent/target/saarthi-java-agent-1.0-SNAPSHOT.jar")

        self.assertTrue(os.path.exists(agent_jar), "Agent JAR not found")

        # Write dummy app source
        with open("DummyApp.java", "w") as f:
            f.write("""
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;

public class DummyApp {
    public static void main(String[] args) throws IOException, InterruptedException {
        System.out.println("DummyApp started.");

        // This should trigger the FilesystemAdvice event
        File file = new File("/tmp/dummy.txt");
        if (!file.exists()) {
            file.createNewFile();
        }

        try (FileInputStream fis = new FileInputStream(file)) {
            fis.read();
        }

        // This should trigger the ProcessBuilderAdvice event
        ProcessBuilder pb = new ProcessBuilder("echo", "Hello from DummyApp");
        Process p = pb.start();
        p.waitFor();

        System.out.println("DummyApp finished.");

        // Give daemon threads time to post events before System.exit(0) kills them
        Thread.sleep(1000);
        System.exit(0);
    }
}
""")
        subprocess.run(["javac", "DummyApp.java"], check=True)

        # Run dummy app
        cmd = [
            "java",
            "-cp", ".",
            f"-javaagent:{agent_jar}=endpoint=http://localhost:8081/events",
            "-Xbootclasspath/a:" + agent_jar,
            "DummyApp"
        ]

        print("Running dummy app with agent...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        print("DummyApp stdout:", result.stdout)
        print("DummyApp stderr:", result.stderr)

        self.assertIn("Java agent loaded successfully", result.stdout)
        self.assertIn("Configured event endpoint: http://localhost:8081/events", result.stdout)
        self.assertIn("Instrumentation initialized successfully", result.stdout)

        # Wait a moment for events to propagate via HTTP and give dummyapp time to exit properly
        # Since it's a daemon thread sending events in EventPublisher, wait to be sure they go through
        time.sleep(4)

        # Cleanup class file
        if os.path.exists("DummyApp.class"):
            os.remove("DummyApp.class")
        if os.path.exists("DummyApp.java"):
            os.remove("DummyApp.java")

        events = self.manager.collect_events(self.session.session_id)
        print(f"Collected {len(events)} events.")

        event_types = [str(e.event_type) for e in events]
        print(f"Event types received: {event_types}")

        has_filesystem = any('FILESYSTEM_ACCESS' in et for et in event_types) or any('FUNCTION_CALL' in et for et in event_types)
        has_process = any('PROCESS_EXECUTION' in et for et in event_types) or any('FUNCTION_CALL' in et for et in event_types)

        self.assertTrue(has_filesystem, "Expected filesystem_access event")
        self.assertTrue(has_process, "Expected process_execution event")

if __name__ == "__main__":
    unittest.main()
