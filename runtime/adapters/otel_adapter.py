from typing import List, Dict, Any
from runtime.adapters.base import RuntimeAdapter
from runtime.models.runtime_event import RuntimeEvent, EventType

class OTelAdapter(RuntimeAdapter):
    def name(self) -> str:
        return "OpenTelemetry"

    def translate(self, raw_spans: List[Dict[str, Any]]) -> List[RuntimeEvent]:
        events = []
        for span in raw_spans:
            event = self._map_span_to_event(span)
            if event:
                events.append(event)
        return events

    def _map_span_to_event(self, span: Dict[str, Any]) -> RuntimeEvent:
        attributes = span.get("attributes", {})
        kind = span.get("kind")
        name = span.get("name", "")

        event_type = EventType.FUNCTION_CALL

        # Heuristics for mapping OTel span kinds/attributes to RuntimeEvent types
        if "http.method" in attributes:
            event_type = EventType.HTTP_REQUEST
        elif "db.system" in attributes or "db.statement" in attributes:
            event_type = EventType.DATABASE_QUERY
        elif kind == "CLIENT":
            event_type = EventType.EXTERNAL_SERVICE_CALL
        elif "exception.type" in attributes:
            event_type = EventType.EXCEPTION

        return RuntimeEvent(
            event_id=span.get("span_id", ""),
            event_type=event_type,
            timestamp=span.get("start_time", 0) / 1e9, # Assume nanoseconds
            trace_id=span.get("trace_id"),
            span_id=span.get("span_id"),
            parent_span_id=span.get("parent_span_id"),
            attributes=attributes,
            metadata={
                "name": name,
                "kind": kind,
                "status": span.get("status")
            }
        )
