from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import time

@dataclass
class TaintSource:
    source_id: str
    source_type: str # e.g., "http_parameter", "query_parameter", "header", "cookie"
    trace_id: str
    location: str # e.g., "GET /api/user?id=123" or "header: Authorization"
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TaintSink:
    sink_id: str
    sink_type: str # e.g., "sql_query", "command_execution", "file_write"
    trace_id: str
    location: str # e.g., "db.execute", "os.system"
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DataFlowEdge:
    source_id: str
    target_id: str
    trace_id: str
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RuntimeFlowEvidence:
    evidence_id: str
    source: TaintSource
    sink: TaintSink
    trace_id: str
    flow_type: str # e.g., "tainted_path"
    confidence: float
    boundary_crossed: bool
    sanitization_detected: bool
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
