from typing import List, Dict, Any
from runtime_agent.adapters.base_adapter import RuntimeAdapter
from runtime.models.runtime_event import RuntimeEvent

class NodeAdapter(RuntimeAdapter):
    def initialize(self) -> None:
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def health(self) -> bool:
        return True

    def collect_events(self) -> List[Any]:
        return []

    def collect_metadata(self) -> Dict[str, Any]:
        return {"language": "Node.js"}

    def capabilities(self) -> List[str]:
        return []
