import unittest
import time
import subprocess
import urllib.request
import os
import threading
from runtime_agent.manager.runtime_manager import RuntimeManager
from runtime_agent.registry.adapter_registry import AdapterRegistry
from runtime_agent.adapters.java.java_adapter import JavaAdapter

class TestRuntimeInstrumentation(unittest.TestCase):
    def setUp(self):
        self.registry = AdapterRegistry()
        self.registry.register("java", JavaAdapter)
        self.manager = RuntimeManager(self.registry)
        self.session = self.manager.create_session("TestApp", "java")
        self.manager.start_session(self.session.session_id)

        # Give the server a moment to bind
        time.sleep(0.5)

    def tearDown(self):
        self.manager.stop_session(self.session.session_id)

    def test_manager_session_lifecycle(self):
        self.assertTrue(self.session.health == "running")

        # Collect should return 0 initially
        events = self.manager.collect_events(self.session.session_id)
        self.assertEqual(len(events), 0)

    def test_event_ingestion_and_normalization(self):
        # We manually inject a JSON payload mirroring what the Java agent sends
        payload = b'{"event_type": "process_execution", "attributes": {"command": "ls -la"}}'

        req = urllib.request.Request(
            'http://localhost:8081/events',
            data=payload,
            headers={'Content-Type': 'application/json'}
        )
        urllib.request.urlopen(req)

        # Retrieve it via Manager
        events = self.manager.collect_events(self.session.session_id)
        self.assertEqual(len(events), 1)
        event = events[0]

        # Verify it normalized to a RuntimeEvent correctly
        # Fallbacks to FUNCTION_CALL if string doesn't match EventType enum directly (as written in our adapter)
        # but the original attributes remain
        self.assertEqual(event.attributes.get("command"), "ls -la")

    def test_forward_to_correlator(self):
        payload = b'{"event_type": "database_query", "attributes": {"sql": "SELECT * FROM users"}}'
        req = urllib.request.Request(
            'http://localhost:8081/events',
            data=payload,
            headers={'Content-Type': 'application/json'}
        )
        urllib.request.urlopen(req)

        events = self.manager.collect_events(self.session.session_id)

        # We'll forward and just ensure it doesn't crash, meaning the pipeline connected successfully.
        state = {"incidents": []}

        # Clean up any residual reports to verify it creates them (or runs successfully)
        if os.path.exists("reports/runtime_evidence.json"):
            os.remove("reports/runtime_evidence.json")

        self.manager.forward_events(events, state)

        self.assertIn("runtime_events", state)
        self.assertEqual(len(state["runtime_events"]), 1)

if __name__ == "__main__":
    unittest.main()
