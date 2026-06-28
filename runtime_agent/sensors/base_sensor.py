from abc import ABC, abstractmethod
from typing import List, Dict, Any
from runtime.models.runtime_event import RuntimeEvent

class RuntimeSensor(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def observe(self, data: Any) -> List[RuntimeEvent]:
        pass
