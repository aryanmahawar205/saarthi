from typing import List, Any
from runtime_agent.sensors.base_sensor import RuntimeSensor
from runtime.models.runtime_event import RuntimeEvent

class SessionSensor(RuntimeSensor):
    def name(self) -> str:
        return "session_sensor"

    def observe(self, data: Any) -> List[RuntimeEvent]:
        # Implementation placeholder
        return []
