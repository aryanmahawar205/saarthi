from typing import Dict, List, Type
from runtime_agent.adapters.base_adapter import RuntimeAdapter

class AdapterRegistry:
    def __init__(self):
        self._adapters: Dict[str, Type[RuntimeAdapter]] = {}
        self._instances: Dict[str, RuntimeAdapter] = {}

    def register(self, name: str, adapter_class: Type[RuntimeAdapter]) -> None:
        self._adapters[name] = adapter_class

    def get_adapter_class(self, name: str) -> Type[RuntimeAdapter]:
        return self._adapters.get(name)

    def load_adapter(self, name: str) -> RuntimeAdapter:
        if name not in self._adapters:
            raise ValueError(f"Adapter '{name}' not found in registry.")
        if name not in self._instances:
            self._instances[name] = self._adapters[name]()
        return self._instances[name]

    def discover_adapters(self) -> List[str]:
        return list(self._adapters.keys())

    def get_adapter_capabilities(self, name: str) -> List[str]:
        adapter = self.load_adapter(name)
        return adapter.capabilities()
