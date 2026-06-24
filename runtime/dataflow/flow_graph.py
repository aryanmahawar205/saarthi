from typing import List, Dict, Any
from runtime.dataflow.models import TaintSource, TaintSink, DataFlowEdge

class RuntimeFlowGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_source(self, source: TaintSource):
        self.nodes[source.source_id] = {
            "type": "source",
            "data": source
        }

    def add_sink(self, sink: TaintSink):
        self.nodes[sink.sink_id] = {
            "type": "sink",
            "data": sink
        }

    def add_function(self, trace_id: str, func_name: str, event_id: str):
        func_id = f"func_{trace_id}_{event_id}"
        self.nodes[func_id] = {
            "type": "function",
            "name": func_name,
            "trace_id": trace_id
        }
        return func_id

    def add_edge(self, source_id: str, target_id: str, trace_id: str, confidence: float = 1.0):
        edge = DataFlowEdge(source_id, target_id, trace_id, confidence)
        self.edges.append(edge)

    def get_flow_path(self, source_id: str, sink_id: str) -> List[str]:
        # Simple BFS to find path between source and sink
        queue = [[source_id]]
        visited = set()

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node == sink_id:
                return path

            if node not in visited:
                visited.add(node)
                for edge in self.edges:
                    if edge.source_id == node:
                        new_path = list(path)
                        new_path.append(edge.target_id)
                        queue.append(new_path)
        return []
