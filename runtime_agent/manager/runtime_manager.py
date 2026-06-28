import uuid
from typing import Dict, List, Optional
from runtime_agent.registry.adapter_registry import AdapterRegistry
from runtime_agent.sessions.runtime_session import RuntimeSession
from runtime.models.runtime_event import RuntimeEvent
from runtime.correlation.runtime_correlator import RuntimeCorrelator

class RuntimeManager:
    def __init__(self, registry: AdapterRegistry):
        self.registry = registry
        self.sessions: Dict[str, RuntimeSession] = {}
        self.correlator = RuntimeCorrelator()

    def discover_applications(self):
        # Placeholder for application discovery logic (Docker, K8s, etc.)
        pass

    def create_session(self, app_name: str, adapter_name: str, **metadata) -> RuntimeSession:
        session_id = str(uuid.uuid4())
        session = RuntimeSession(
            session_id=session_id,
            application=app_name,
            adapter=adapter_name,
            metadata=metadata
        )
        self.sessions[session_id] = session
        return session

    def start_session(self, session_id: str) -> None:
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found.")
        session = self.sessions[session_id]

        adapter = self.registry.load_adapter(session.adapter)
        adapter.initialize()
        adapter.start()

        session.health = "running"
        session.active_sensors = adapter.capabilities()

    def stop_session(self, session_id: str) -> None:
        if session_id not in self.sessions:
            return
        session = self.sessions[session_id]

        adapter = self.registry.load_adapter(session.adapter)
        adapter.stop()

        session.health = "stopped"

    def collect_events(self, session_id: str) -> List[RuntimeEvent]:
        if session_id not in self.sessions:
            return []
        session = self.sessions[session_id]
        adapter = self.registry.load_adapter(session.adapter)
        return adapter.collect_events()

    def forward_events(self, events: List[RuntimeEvent], state: Dict = None) -> None:
        """
        Forward events to Runtime Intelligence Platform.
        In a real orchestrator flow, the events would be pushed to a shared state
        or directly to the correlator. We simulate passing them to the correlator directly.
        """
        # We can run a correlation against empty findings just to produce data flow evidence
        if state is None:
            state = {}

        state["runtime_events"] = events

        # We invoke the correlation pipeline logic here to make the events available
        # to the Runtime Intelligence platform without bypassing it.
        # This mirrors the behavior expected in run_correlation.
        from runtime.correlation.runtime_correlator import run_correlation
        run_correlation(state)
