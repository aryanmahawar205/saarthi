from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import time

class EventType(Enum):
    HTTP_REQUEST = "http_request"
    HTTP_RESPONSE = "http_response"
    FUNCTION_CALL = "function_call"
    DATABASE_QUERY = "database_query"
    EXTERNAL_SERVICE_CALL = "external_service_call"
    EXCEPTION = "exception"
    TRUST_BOUNDARY_CROSSING = "trust_boundary_crossing"
    AUTHENTICATION_DECISION = "authentication_decision"
    AUTHORIZATION_DECISION = "authorization_decision"

@dataclass
class RuntimeEvent:
    event_id: str
    event_type: EventType
    timestamp: float = field(default_factory=time.time)
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    parent_span_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RuntimeTrace:
    trace_id: str
    events: List[RuntimeEvent] = field(default_factory=list)

    def add_event(self, event: RuntimeEvent):
        self.events.append(event)
        self.events.sort(key=lambda x: x.timestamp)

@dataclass
class RuntimeEvidence:
    evidence_id: str
    finding_id: str # Link to SAST/DAST incident
    description: str
    confirmed: bool
    evidence_type: str # e.g., "reachability", "sink_reached", "boundary_crossed"
    timestamp: float = field(default_factory=time.time)
    related_trace_ids: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
