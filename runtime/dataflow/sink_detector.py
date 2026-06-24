from typing import List, Optional
from runtime.models.runtime_event import RuntimeEvent, EventType
from runtime.dataflow.models import TaintSink

class SinkDetector:
    def detect(self, event: RuntimeEvent) -> Optional[TaintSink]:
        trace_id = event.trace_id or "unknown"

        if event.event_type == EventType.DATABASE_QUERY:
            return TaintSink(
                sink_id=f"sink_{trace_id}_db_{event.event_id}",
                sink_type="database_query",
                trace_id=trace_id,
                location=event.attributes.get("db.statement", "unknown_query"),
                metadata={"system": event.attributes.get("db.system")}
            )

        if event.event_type == EventType.EXTERNAL_SERVICE_CALL:
            return TaintSink(
                sink_id=f"sink_{trace_id}_ext_{event.event_id}",
                sink_type="external_service_call",
                trace_id=trace_id,
                location=event.attributes.get("http.url", "unknown_url"),
                metadata={"method": event.attributes.get("http.method")}
            )

        if event.event_type == EventType.FUNCTION_CALL:
            # Detect sensitive functions by name
            func_name = event.metadata.get("name", "").lower()
            sensitive_sinks = {
                "os.system": "command_execution",
                "subprocess.run": "command_execution",
                "eval": "code_execution",
                "exec": "code_execution",
                "open": "file_write", # Could also be read, needs better heuristic
                "yaml.load": "deserialization",
                "pickle.load": "deserialization"
            }

            for sink_pattern, sink_type in sensitive_sinks.items():
                if sink_pattern in func_name:
                    return TaintSink(
                        sink_id=f"sink_{trace_id}_func_{event.event_id}",
                        sink_type=sink_type,
                        trace_id=trace_id,
                        location=func_name,
                        metadata={"arguments": event.attributes.get("args")}
                    )

        return None
