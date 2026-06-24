from typing import List, Optional
from runtime.models.runtime_event import RuntimeEvent, EventType
from runtime.dataflow.models import TaintSource

class SourceDetector:
    def detect(self, event: RuntimeEvent) -> List[TaintSource]:
        sources = []
        if event.event_type == EventType.HTTP_REQUEST:
            trace_id = event.trace_id or "unknown"

            # Query Parameters
            for param in event.attributes.get("http.query_params", {}):
                sources.append(TaintSource(
                    source_id=f"src_{trace_id}_query_{param}",
                    source_type="query_parameter",
                    trace_id=trace_id,
                    location=f"query:{param}",
                    metadata={"value_preview": str(event.attributes.get("http.query_params", {}).get(param))[:50]}
                ))

            # Form Data
            for field in event.attributes.get("http.form_data", {}):
                sources.append(TaintSource(
                    source_id=f"src_{trace_id}_form_{field}",
                    source_type="form_input",
                    trace_id=trace_id,
                    location=f"form:{field}",
                    metadata={"value_preview": str(event.attributes.get("http.form_data", {}).get(field))[:50]}
                ))

            # Headers
            for header in event.attributes.get("http.headers", {}):
                if header.lower() in ["user-agent", "referer", "x-forwarded-for"]:
                    sources.append(TaintSource(
                        source_id=f"src_{trace_id}_header_{header}",
                        source_type="header",
                        trace_id=trace_id,
                        location=f"header:{header}",
                        metadata={"value_preview": str(event.attributes.get("http.headers", {}).get(header))[:50]}
                    ))

            # Cookies
            for cookie in event.attributes.get("http.cookies", {}):
                sources.append(TaintSource(
                    source_id=f"src_{trace_id}_cookie_{cookie}",
                    source_type="cookie",
                    trace_id=trace_id,
                    location=f"cookie:{cookie}",
                    metadata={"value_preview": str(event.attributes.get("http.cookies", {}).get(cookie))[:50]}
                ))

        return sources
