from typing import List, Dict, Any
from runtime_agent.adapters.base_adapter import RuntimeAdapter
from runtime.models.runtime_event import RuntimeEvent
from runtime.adapters.otel_adapter import OTelAdapter as LegacyOTelAdapter

class OpenTelemetryAdapter(RuntimeAdapter):
    def __init__(self):
        self._legacy = LegacyOTelAdapter()
        self._is_running = False

    def initialize(self) -> None:
        pass

    def start(self) -> None:
        self._is_running = True

    def stop(self) -> None:
        self._is_running = False

    def health(self) -> bool:
        return self._is_running

    def collect_events(self) -> List[Any]:
        # Typically called with raw spans, adapted here
        # Return empty for now as it relies on input
        return []

    def collect_events_from_raw(self, raw_spans: List[Dict[str, Any]]) -> List[RuntimeEvent]:
        return self._legacy.translate(raw_spans)

    def collect_metadata(self) -> Dict[str, Any]:
        return {"adapter": "OpenTelemetry", "version": "1.0"}

    def capabilities(self) -> List[str]:
        return ["http_sensor", "database_sensor", "exception_sensor"]
