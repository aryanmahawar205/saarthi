import time
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class RuntimeSession:
    session_id: str
    application: str
    adapter: str
    start_time: float = field(default_factory=time.time)
    health: str = "starting"
    active_sensors: List[str] = field(default_factory=list)
    runtime_version: str = "unknown"
    framework: str = "unknown"
    language: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)
