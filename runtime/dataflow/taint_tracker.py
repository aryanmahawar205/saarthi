from typing import List, Dict, Any
from runtime.models.runtime_event import RuntimeEvent, EventType
from runtime.dataflow.models import RuntimeFlowEvidence, TaintSource, TaintSink
from runtime.dataflow.source_detector import SourceDetector
from runtime.dataflow.sink_detector import SinkDetector
from runtime.dataflow.sanitizer_detector import SanitizerDetector
from runtime.dataflow.flow_graph import RuntimeFlowGraph

class TaintTracker:
    def __init__(self):
        self.source_detector = SourceDetector()
        self.sink_detector = SinkDetector()
        self.sanitizer_detector = SanitizerDetector()
        self.flow_graph = RuntimeFlowGraph()
        self.evidence: List[RuntimeFlowEvidence] = []

    def track_traces(self, events: List[RuntimeEvent]) -> List[RuntimeFlowEvidence]:
        # Group events by trace
        traces: Dict[str, List[RuntimeEvent]] = {}
        for event in events:
            if event.trace_id:
                if event.trace_id not in traces:
                    traces[event.trace_id] = []
                traces[event.trace_id].append(event)

        for trace_id, trace_events in traces.items():
            self._process_trace(trace_id, trace_events)

        return self.evidence

    def _process_trace(self, trace_id: str, events: List[RuntimeEvent]):
        sources: List[TaintSource] = []
        sinks: List[TaintSink] = []
        sanitization_detected = False
        boundary_crossed = False

        # Sort events by timestamp
        events.sort(key=lambda x: x.timestamp)

        last_node_id = None

        for event in events:
            # 1. Detect Sources
            detected_sources = self.source_detector.detect(event)
            for src in detected_sources:
                sources.append(src)
                self.flow_graph.add_source(src)
                last_node_id = src.source_id

            # 2. Detect Trust Boundary Crossing
            if event.event_type == EventType.TRUST_BOUNDARY_CROSSING:
                boundary_crossed = True

            # 3. Detect Sanitization
            if self.sanitizer_detector.detect(event):
                sanitization_detected = True

            # 4. Function calls as middle nodes
            if event.event_type == EventType.FUNCTION_CALL:
                func_id = self.flow_graph.add_function(trace_id, event.metadata.get("name", "unknown"), event.event_id)
                if last_node_id:
                    self.flow_graph.add_edge(last_node_id, func_id, trace_id)
                last_node_id = func_id

            # 5. Detect Sinks
            sink = self.sink_detector.detect(event)
            if sink:
                sinks.append(sink)
                self.flow_graph.add_sink(sink)
                if last_node_id:
                    self.flow_graph.add_edge(last_node_id, sink.sink_id, trace_id)
                last_node_id = sink.sink_id

        # If we have both source and sink in the same trace, we have a flow
        if sources and sinks:
            for src in sources:
                for sink in sinks:
                    # Check if there is a path in the flow graph
                    path = self.flow_graph.get_flow_path(src.source_id, sink.sink_id)
                    if path:
                        evidence = RuntimeFlowEvidence(
                            evidence_id=f"FLOW_{trace_id}_{src.source_id}_{sink.sink_id}",
                            source=src,
                            sink=sink,
                            trace_id=trace_id,
                            flow_type="tainted_path",
                            confidence=0.9 if not sanitization_detected else 0.4,
                            boundary_crossed=boundary_crossed,
                            sanitization_detected=sanitization_detected,
                            metadata={"path": path}
                        )
                        self.evidence.append(evidence)
