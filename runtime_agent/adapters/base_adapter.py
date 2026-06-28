from abc import ABC, abstractmethod
from typing import List, Dict, Any

class RuntimeAdapter(ABC):
    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def health(self) -> bool:
        pass

    @abstractmethod
    def collect_events(self) -> List[Any]:
        pass

    @abstractmethod
    def collect_metadata(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def capabilities(self) -> List[str]:
        pass
